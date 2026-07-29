import os
import sys
import time
import subprocess
import atexit
import threading
from datetime import datetime, timezone
from dotenv import load_dotenv
from pathlib import Path
import requests
from supabase import create_client, Client

PROJECT_ROOT = Path(__file__).resolve().parent
if not (PROJECT_ROOT / "config.py").exists():
    PROJECT_ROOT = PROJECT_ROOT.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

load_dotenv(PROJECT_ROOT / ".env")

SUPABASE_URL = os.getenv("SUPABASE_URL", "https://nfhtmfhckctuyhfolhou.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_SECRET_KEY") or os.getenv("SUPABASE_PUBLISHABLE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY or "")

try:
    import scripts.db_init as db_init
    import parsers.parser_hardware as parser_hardware
    import parsers.parser as parser
    import core.filter_ads as filter_ads
    import core.pc_evaluator as pc_evaluator
    import scripts.clean_archive as clean_archive
    import core.seller_analyzer as seller_analyzer
    import core.competitor_finder as competitor_finder
    import core.price_hardware as price_hardware
except ImportError as e:
    print(f"[ПОМИЛКА ІМПОРТУ] Переконайся в правильності шляхів: {e}")
    sys.exit(1)

server_process = None
frontend_process = None
is_heavy_analysis_running = False


def start_web_servers():
    global server_process, frontend_process

    server_dir = PROJECT_ROOT / "server"
    frontend_dir = PROJECT_ROOT / "server/frontend"

    print("\n🌐 [SERVERS] Запуск FastAPI бекенду (uvicorn)...")
    try:
        server_process = subprocess.Popen(
            [sys.executable, "-m", "uvicorn", "server:app", "--reload", "--port", "8000"],
            cwd=str(server_dir),
            shell=True if os.name == "nt" else False
        )
    except Exception as e:
        print(f"❌ Не вдалося запустити FastAPI сервер: {e}")

    print("🎨 [SERVERS] Запуск React фронтенду (npm run dev)...")
    try:
        npm_cmd = "npm.cmd" if os.name == "nt" else "npm"
        frontend_process = subprocess.Popen(
            [npm_cmd, "run", "dev"],
            cwd=str(frontend_dir),
            shell=True if os.name == "nt" else False
        )
    except Exception as e:
        print(f"❌ Не вдалося запустити React фронтенд: {e}")

    print("⏳ Очікування 5 секунд для ініціалізації веб-серверів...")
    time.sleep(5)


def cleanup_servers():
    global server_process, frontend_process
    print("\n🛑 [SERVERS] Зупинка веб-серверів...")
    if server_process:
        server_process.terminate()
    if frontend_process:
        frontend_process.terminate()


atexit.register(cleanup_servers)


def count_unprocessed_ads() -> int:
    """Підраховує кількість нових активних оголошень, які потребують оцінки заліза та продавця."""
    try:
        res = supabase.table("ads") \
            .select("id", count="exact") \
            .eq("status", "active") \
            .or_("seller_risk_score.is.null,estimated_fair_price.is.null") \
            .execute()
            
        return res.count or 0
    except Exception as e:
        print(f"⚠️ [ORCHESTRATOR] Помилка підрахунку неоцінених лотів: {e}")
        return 0


def broadcast_updated_ads(updated_ids: list[int]):
    """Отримує актуальні оновлені оголошення з Supabase та тригерить їх трансляцію на веб-сайт."""
    if not updated_ids:
        return

    try:
        response = supabase.table("ads") \
            .select("*") \
            .in_("id", updated_ids) \
            .eq("status", "active") \
            .execute()
        rows = response.data or []
    except Exception as e:
        print(f"⚠️ [ORCHESTRATOR] Помилка отримання оновлених лотів з Supabase: {e}")
        return

    ads_to_broadcast = []
    for ad_dict in rows:
        ad_dict["seller_successful_deals"] = ad_dict.get("seller_successful_deals") or 0
        ad_dict["seller_rating"] = ad_dict.get("seller_rating") or "немає оцінок"
        ad_dict["seller_risk_score"] = ad_dict.get("seller_risk_score") or ad_dict.get("seller_risk") or "neutral"
        ad_dict["deal_status"] = ad_dict.get("deal_status") or "regular"
        ads_to_broadcast.append(ad_dict)

    if ads_to_broadcast:
        print(f"🚀 [BROADCAST] Пушимо пачку з {len(ads_to_broadcast)} повних лотів на Live-сайт...")
        try:
            requests.post("http://localhost:8000/api/trigger-new-ad", json=ads_to_broadcast, timeout=5)
        except Exception as e:
            print(f"   ⚠️ Помилка пакетного пушу: {e}")


def run_step(step_name: str, step_function, *args, **kwargs):
    print(f"\n" + "="*60)
    print(f"🚀 [КРОК] ЗАПУСК ЕТАПУ: {step_name.upper()}")
    print("="*60)
    
    start_time = time.time()
    try:
        result = step_function(*args, **kwargs)
        elapsed = time.time() - start_time
        print(f"✅ [УСПІХ] {step_name.upper()} завершено за {elapsed:.2f} сек.")
        return result
    except Exception as e:
        print(f"❌ [ПОМИЛКА] Під час виконання {step_name}: {e}")
        return None


def run_heavy_analysis_in_background():
    """Фоновий потік для важких тривалих розрахунків ринку."""
    global is_heavy_analysis_running
    if is_heavy_analysis_running:
        return

    is_heavy_analysis_running = True
    try:
        run_step("Визначення ринкової ціни продажів (конкуренти)", competitor_finder.main)
        run_step("Перерахунок прайсів заліза", price_hardware.main)
        run_step("Верифікація активності оголошень (архів)", clean_archive.main)
    except Exception as e:
        print(f"❌ [ФОНОВИЙ АНАЛІЗ ПОМИЛКА]: {e}")
    finally:
        is_heavy_analysis_running = False


def run_pipeline_iteration(is_first_run: bool = False):
    today_str = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n⚡ [24/7 LOOP] Перевірка OLX та залізо-ринку ({today_str})...")

    # 1. Визначення кількості сторінок залежно від запуску
    pages_to_parse = 4 if is_first_run else 1
    if is_first_run:
        print("🚀 [ПЕРШИЙ ЗАПУСК] Парсимо 4 сторінки для глибокого первинного збору...")
    else:
        print("🔄 [РЕГУЛЯРНИЙ ЗАПУСК] Парсимо 1 першу сторінку (40 найновіших)...")

    # 2. Швидкі етапи: парсинг та фільтрація
    run_step("Парсинг сирих оголошень ПК", parser.main, pages_to_parse=pages_to_parse)
    run_step("Парсинг комплектуючих", parser_hardware.main, pages_to_parse=pages_to_parse)
    run_step("Фільтрація бан-слів", filter_ads.main)

    # 3. Аналіз та швидкий пуш нових лотів
    unprocessed_count = count_unprocessed_ads()
    print(f"🔎 [АНАЛІЗ] Нових релевантних лотів для оцінки: {unprocessed_count}")

    if unprocessed_count > 0:
        run_step("Оцінка вигідності ПК", pc_evaluator.main)
        updated_ids = run_step("Оцінка продавців", seller_analyzer.run_seller_analysis)

        if updated_ids:
            run_step("Пуш нових лотів на Live-сайт", broadcast_updated_ads, updated_ids)
    else:
        print("💤 Нових лотів не виявлено. Пропускаємо швидку оцінку.")

    # 4. Важка аналітика у фоновому потоці (не блокує наступні ітерації парсингу)
    if is_first_run or (not is_heavy_analysis_running):
        threading.Thread(target=run_heavy_analysis_in_background, daemon=True).start()

    if pages_to_parse == 4:
        print(f"\n⏳ Пауза 25 сек для скидання ліміту DataDome...\n")
        time.sleep(25)


def main():
    print(f"==========================================================")
    print(f"🏁     СТАРТ СИСТЕМИ АВТОМАТИЗАЦІЇ 24/7 (ALL-IN-ONE)       ")
    print(f"==========================================================")

    # Запускаємо Uvicorn + React
    start_web_servers()

    CYCLE_DELAY_SECONDS = 20
    is_first_run = True

    try:
        while True:
            cycle_start = time.time()
            
            run_pipeline_iteration(is_first_run=is_first_run)
            is_first_run = False  # Наступні ітерації працюватимуть в режимі 1 сторінки

            elapsed = time.time() - cycle_start
            print(f"\n⏱️ Ітерацію збору завершено за {elapsed:.2f} сек. Наступна перевірка через {CYCLE_DELAY_SECONDS} сек...")
            time.sleep(CYCLE_DELAY_SECONDS)

    except KeyboardInterrupt:
        print("\n👋 Ручна зупинка програми (Ctrl+C). Очищення ресурсів...")


if __name__ == "__main__":
    main()
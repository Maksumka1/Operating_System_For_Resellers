import sys
import time
import sqlite3
import subprocess
import os
import atexit
import time
from datetime import datetime, timezone
from pathlib import Path
import requests

PROJECT_ROOT = Path(__file__).resolve().parent
if not (PROJECT_ROOT / "config.py").exists():
    PROJECT_ROOT = PROJECT_ROOT.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from config import DB_FILE

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


def start_web_servers():
    """Запускає FastAPI бекенд та React фронтенд у фонових процесах"""
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
    """Зупиняє фонові вебсервери при виході"""
    global server_process, frontend_process
    print("\n🛑 [SERVERS] Зупинка веб-серверів...")
    if server_process:
        server_process.terminate()
    if frontend_process:
        frontend_process.terminate()


atexit.register(cleanup_servers)


def should_calculate_prices() -> bool:
    """Перевіряє, чи пройшов тиждень від останнього розрахунку цін у component_prices"""
    if not DB_FILE.exists():
        return True

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT MAX(date) FROM component_prices")
        row = cursor.fetchone()
        
        if not row or not row[0]:
            print("[ORCHESTRATOR] Таблиця 'component_prices' порожня. Потрібно порахувати ціни.")
            return True
            
        latest_date_str = row[0] 
        latest_date = datetime.strptime(latest_date_str, "%Y-%m-%d").replace(tzinfo=timezone.utc)
        today = datetime.now(timezone.utc)
        
        days_passed = (today - latest_date).days
        
        if days_passed >= 7:
            print(f"[ORCHESTRATOR] Ціни рахувалися {days_passed} днів тому (>= 7). Запускаємо price_hardware.")
            return True
        else:
            print(f"[ORCHESTRATOR] Ціни заліза актуальні ({latest_date_str}, {days_passed} дн. тому). Пропускаємо price_hardware.")
            return False
            
    except sqlite3.OperationalError:
        return True
    finally:
        conn.close()


def count_unprocessed_ads() -> int:
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM ads WHERE seller_id IS NULL AND status = 'active' AND has_defects = 0")
    count = cursor.fetchone()[0]
    conn.close()
    return count


def broadcast_updated_ads(updated_ids: list[int]):
    if not updated_ids:
        return

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    placeholders = ','.join('?' for _ in updated_ids)
    cursor.execute(f"""
        SELECT 
            id, url, title, description, price, item_type, city, created_at_olx, photo_url,
            seller_name, seller_created_at, seller_successful_deals, seller_rating, seller_risk_score,
            estimated_fair_price, competitor_price, saving_uah, saving_percent, evaluated_at
        FROM ads 
        WHERE id IN ({placeholders}) AND status = 'active'
    """, updated_ids)
    
    rows = cursor.fetchall()
    conn.close()

    ads_to_broadcast = [
        {
            "id": r[0], "url": r[1], "title": r[2], "description": r[3], "price": r[4], "item_type": r[5],
            "city": r[6], "created_at_olx": r[7], "photo_url": r[8],
            "seller_name": r[9], "seller_created_at": r[10], "seller_successful_deals": r[11] or 0,
            "seller_rating": r[12] or "немає оцінок", "seller_risk": r[13] or "neutral",
            "estimated_fair_price": r[14], "competitor_price": r[15],
            "saving_uah": r[16], "saving_percent": r[17], "evaluated_at": r[18]
        }
        for r in rows
    ]

    if ads_to_broadcast:
        print(f"🚀 [BROADCAST] Пушимо пачку з {len(ads_to_broadcast)} лотів на Live-сайт...")
        try:
            requests.post("http://localhost:8000/api/trigger-new-ad", json=ads_to_broadcast, timeout=5)
        except Exception as e:
            print(f"  ⚠️ Помилка пакетного пушу: {e}")


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


def run_pipeline_iteration():
    today_str = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n⚡ [24/7 LOOP] Перевірка OLX та залізо-ринку ({today_str})...")

    # 2. Парсинг готових ПК
    run_step("Парсинг сирих оголошень ПК", parser.main)

    # 1. Парсинг заліза (кожні N секунд)
    run_step("Парсинг комплектуючих", parser_hardware.main)

    # 3. Фільтрація бан-слів
    run_step("Фільтрація бан-слів", filter_ads.main)

    # 4. Аналіз нових лотів
    unprocessed_count = count_unprocessed_ads()
    print(f"🔎 [АНАЛІЗ] Нових релевантних лотів для повної оцінки: {unprocessed_count}")

    if unprocessed_count > 0:
        run_step("Оцінка вигідності ПК", pc_evaluator.main)
        run_step("Визначення ринкової ціни продажів", competitor_finder.main)
        updated_ids = run_step("Оцінка продавців", seller_analyzer.run_seller_analysis)

        if updated_ids:
            run_step("Пуш нових лотів на Live-сайт", broadcast_updated_ads, updated_ids)
    else:
        print("💤 Нових лотів не виявлено. Пропускаємо етапи глибокого аналізу.")
    
    # 5. Розрахунок прайсів заліза (раз на 7 днів)
    if should_calculate_prices():
        run_step("Перерахунок прайсів заліза", price_hardware.main)

    print(f"\n⏳Пауза 25 сек для скидання ліміту DataDome...\n")
    time.sleep(25)
    # 6. Очищення архіву
    run_step("Верифікація активності оголошень", clean_archive.main)


def main():
    print(f"==========================================================")
    print(f"🏁    СТАРТ СИСТЕМИ АВТОМАТИЗАЦІЇ 24/7 (ALL-IN-ONE)       ")
    print(f"==========================================================")

    run_step("Ініціалізація бази даних", db_init.init_db)

    # Запускаємо Uvicorn + React
    start_web_servers()

    # Пауза між повторними скануваннями OLX (рекомендовано 15-30 сек)
    CYCLE_DELAY_SECONDS = 20

    try:
        while True:
            cycle_start = time.time()
            run_pipeline_iteration()
            
            elapsed = time.time() - cycle_start
            print(f"\n⏱️ Ітерацію завершено за {elapsed:.2f} сек. Наступна перевірка через {CYCLE_DELAY_SECONDS} сек...")
            time.sleep(CYCLE_DELAY_SECONDS)

    except KeyboardInterrupt:
        print("\n👋 Ручна зупинка програми (Ctrl+C). Очищення ресурсів...")


if __name__ == "__main__":
    main()
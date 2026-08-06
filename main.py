import os
import sys
import time
import asyncio
import subprocess
import atexit
from datetime import datetime, timezone
from pathlib import Path

import requests
from dotenv import load_dotenv
from supabase import create_client, Client

PROJECT_ROOT = Path(__file__).resolve().parent
if not (PROJECT_ROOT / "config.py").exists():
    PROJECT_ROOT = PROJECT_ROOT.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

load_dotenv(PROJECT_ROOT / ".env")

SUPABASE_URL = os.getenv("SUPABASE_URL", "https://nfhtmfhckctuyhfolhou.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_SECRET_KEY") or os.getenv("SUPABASE_PUBLISHABLE_KEY")
OLX_PROXY_URL = os.getenv("OLX_PROXY_URL") or None

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY or "")

try:
    import parsers.parser_hardware as parser_hardware
    import parsers.parser as parser
    import core.filter_ads as filter_ads
    import core.pc_evaluator as pc_evaluator
    import scripts.clean_archive as clean_archive
    import core.seller_analyzer as seller_analyzer
    import core.competitor_finder as competitor_finder
    import core.price_hardware as price_hardware
    from core import hardware_evaluator
except ImportError as e:
    print(f"[ПОМИЛКА ІМПОРТУ] Переконайся в правильності шляхів: {e}")
    sys.exit(1)

# Глобальний замок для усунення гонки даних під час запису в БД
db_write_lock = asyncio.Lock()


class AdaptiveRateLimiter:
    """Динамічний контроль частоти запитів до OLX (AIMD)."""
    def __init__(self, min_rate=40, max_rate=80, initial_rate=60):
        self.min_rate = min_rate
        self.max_rate = max_rate
        self.current_rate = initial_rate
        self.consecutive_403 = 0
        self.success_streak = 0
        self._lock = asyncio.Lock()
        self.is_cooldown = False

    async def acquire(self):
        async with self._lock:
            while self.is_cooldown:
                await asyncio.sleep(1)
            await asyncio.sleep(60.0 / self.current_rate)

    async def report_result(self, status_code: int):
        async with self._lock:
            if status_code == 403:
                self.consecutive_403 += 1
                self.success_streak = 0
                if self.consecutive_403 >= 3:
                    print("🛑 [DATADOME BLOCK] 3x403! Перерва 60 секунд...")
                    self.is_cooldown = True
                    self.current_rate = max(self.min_rate, self.current_rate * 0.85)
                    await asyncio.sleep(60)
                    self.consecutive_403 = 0
                    self.is_cooldown = False
            elif status_code == 200:
                self.consecutive_403 = 0
                self.success_streak += 1
                if self.success_streak >= 15 and self.current_rate < self.max_rate:
                    self.current_rate = min(self.max_rate, self.current_rate + 2.0)
                    self.success_streak = 0


primary_limiter = AdaptiveRateLimiter()
server_process = None


def start_web_servers():
    global server_process
    server_dir = PROJECT_ROOT / "server"
    print("\n🌐 [SERVERS] Запуск FastAPI бекенду (uvicorn)...")
    try:
        server_process = subprocess.Popen(
            [sys.executable, "-m", "uvicorn", "server:app", "--reload", "--port", "8000"],
            cwd=str(server_dir),
            shell=(os.name == "nt")
        )
    except Exception as e:
        print(f"❌ Не вдалося запустити сервер: {e}")
    time.sleep(3)


def cleanup_servers():
    global server_process
    if server_process:
        server_process.terminate()


atexit.register(cleanup_servers)


async def count_unprocessed_ads() -> int:
    def _db_query():
        try:
            res = (
                supabase.table("ads")
                .select("id", count="exact")
                .eq("status", "active")
                .or_("seller_risk_score.is.null,estimated_fair_price.is.null")
                .execute()
            )
            return res.count or 0
        except Exception:
            return 0
    return await asyncio.to_thread(_db_query)


async def broadcast_updated_ads(updated_ids: list[int]):
    if not updated_ids:
        return
    def _get_rows():
        try:
            res = supabase.table("ads").select("*").in_("ad_id", updated_ids).eq("status", "active").execute()
            return res.data or []
        except Exception:
            return []

    rows = await asyncio.to_thread(_get_rows)
    if rows:
        await asyncio.to_thread(
            lambda: requests.post("http://localhost:8000/api/trigger-new-ad", json=rows, timeout=5)
        )


# =====================================================================
# ФОНОВІ ДЕМОНИ (АРХІВ ТА ПРАЙСИ ЗАЛІЗА)
# =====================================================================
async def background_archive_checker():
    """Фонова перевірка архівних оголошень кожні 5 хвилин."""
    while True:
        await asyncio.sleep(300)
        print("\n🧹 [BACKGROUND] Перевірка деактивованих лотів (clean_archive)...")
        await clean_archive.main_async(db_lock=db_write_lock)


async def background_price_hardware():
    """Фоновий перерахунок ринкових цін заліза кожні 5 хвилин."""
    while True:
        await asyncio.sleep(300)
        print("\n📊 [BACKGROUND] Оновлення середніх прайсів заліза (price_hardware)...")
        await price_hardware.main_async(db_lock=db_write_lock)


# =====================================================================
# ОСНОВНИЙ ЦИКЛ ПАРСИНГУ ТА ОЦІНКИ
# =====================================================================
async def run_pipeline_iteration(is_first_run: bool = False):
    today_str = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n🔄 [24/7 ASYNC LOOP] Ітерація ({today_str}) | Ліміт: {primary_limiter.current_rate:.1f} req/min")

    pages_to_parse = 4 if is_first_run else 1

    # 1. Запуск двох парсерів
    print(f"🚀 [ЕТАП 1] Запуск парсингу ПК та комплектуючих...")
    await asyncio.gather(
        parser.main_async(pages_to_parse=pages_to_parse, db_lock=db_write_lock, rate_limiter=primary_limiter),
        parser_hardware.main_async(pages_to_parse=pages_to_parse, db_lock=db_write_lock, rate_limiter=primary_limiter)
    )

    # 2. Фільтрація
    await filter_ads.main_async(db_lock=db_write_lock)

    # 3. Аналіз та оцінка
    unprocessed_count = await count_unprocessed_ads()
    print(f"📊 [АНАЛІЗ] Нових релевантних лотів: {unprocessed_count}")

    if unprocessed_count > 0:
        # Паралельна оцінка вигідності ПК та комплектуючих
        await asyncio.gather(
            pc_evaluator.main_async(db_lock=db_write_lock),
            hardware_evaluator.main_async(db_lock=db_write_lock)
        )

        # 4. Продавці та конкуренти
        results = await asyncio.gather(
            seller_analyzer.main_async(db_lock=db_write_lock),
            competitor_finder.main_async(db_lock=db_write_lock)
        )
        
        updated_seller_ids, updated_comp_ids = results[0], results[1]
        all_updated = list(set((updated_seller_ids or []) + (updated_comp_ids or [])))
        
        if all_updated:
            await broadcast_updated_ads(all_updated)


async def main():
    print("==========================================================")
    print(" 🚀 СТАРТ АСИНХРОННОГО ОРКЕСТРАТОРА 24/7 ")
    print("==========================================================")

    start_web_servers()
    
    # Запуск фонових демонів (Архів + Прайси заліза)
    asyncio.create_task(background_archive_checker())
    asyncio.create_task(background_price_hardware())

    is_first_run = True
    while True:
        try:
            cycle_start = time.time()
            await run_pipeline_iteration(is_first_run=is_first_run)
            is_first_run = False

            elapsed = time.time() - cycle_start
            print(f"\n⏱️ Ітерацію завершено за {elapsed:.2f} сек. Пауза 20 сек...")
            await asyncio.sleep(20)
        except Exception as ex:
            print(f"❌ [КРИТИЧНА ПОМИЛКА ЦИКЛУ]: {ex}")
            await asyncio.sleep(10)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 Зупинка оркестратора.")
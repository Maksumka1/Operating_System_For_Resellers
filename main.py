import os
import sys
import time
import inspect
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

# Шлях до файлу детального дебаг-логу
DEBUG_DIR = PROJECT_ROOT / "debug"
DEBUG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = DEBUG_DIR / "main-debug.md"

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


def get_current_time_str() -> str:
    """Повертає поточний локальний час у форматі HH:MM:SS."""
    return datetime.now().strftime("%H:%M:%S")


def append_to_debug_file(text: str) -> None:
    """Синхронно дописує рядок у debug/main-debug.md."""
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(text + "\n")


def log_section_header(title: str) -> None:
    """Записує заголовок секції/ітерації в Markdown."""
    timestamp = get_current_time_str()
    header = f"\n---\n## 🔄 [{timestamp}] {title}\n"
    append_to_debug_file(header)


def _format_input_args(kwargs: dict) -> str:
    """Форматує аргументи функції для красивого виводу в лог."""
    clean_kwargs = {
        k: v for k, v in kwargs.items() 
        if k not in ("db_lock", "rate_limiter")
    }
    if not clean_kwargs:
        return "без особливих параметрів"
    return ", ".join(f"`{k}={v}`" for k, v in clean_kwargs.items())


def _summarize_result(result) -> str:
    """Аналізує результат роботи модуля і повертає коротке резюме."""
    if result is None:
        return "завершено (без повернення даних)"
    if isinstance(result, (list, tuple, set)):
        return f"оброблено/повернуто `{len(result)}` елементів"
    if isinstance(result, dict):
        return f"згенеровано словник із `{len(result)}` ключів"
    if isinstance(result, (int, float)):
        return f"результат = `{result}`"
    return f"повернуто `{str(result)[:60]}`"


async def run_logged_module(module_name: str, coro_or_func, *args, **kwargs):
    """Розширена обгортка для детального дебагу запуску та результатів кожного модуля."""
    start_time_str = get_current_time_str()
    start_perf = time.perf_counter()
    
    input_desc = _format_input_args(kwargs)
    
    # 1. Запис про старт
    log_start = f"- ⏳ **[{start_time_str}]** `СТАРТ` **{module_name}** | Вхідні дані: {input_desc}"
    await asyncio.to_thread(append_to_debug_file, log_start)

    try:
        if inspect.iscoroutinefunction(coro_or_func):
            result = await coro_or_func(*args, **kwargs)
        else:
            result = coro_or_func(*args, **kwargs)

        duration = time.perf_counter() - start_perf
        end_time_str = get_current_time_str()
        result_desc = _summarize_result(result)

        # 2. Запис про успішний фініш
        log_end = f"  - ✅ **[{end_time_str}]** `УСПІХ` **{module_name}** | Тривалість: `{duration:.2f}s` | Результат: {result_desc}"
        await asyncio.to_thread(append_to_debug_file, log_end)
        return result

    except Exception as e:
        duration = time.perf_counter() - start_perf
        end_time_str = get_current_time_str()
        
        # 3. Запис про помилку
        log_err = f"  - ❌ **[{end_time_str}]** `ПОМИЛКА` **{module_name}** | Тривалість: `{duration:.2f}s` | Причина: `{str(e)}`"
        await asyncio.to_thread(append_to_debug_file, log_err)
        raise e


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
                    msg = f"🛑 **[{get_current_time_str()}] [DATADOME BLOCK]** 3x403! Cooldown 60 секунд..."
                    await asyncio.to_thread(append_to_debug_file, f"  - {msg}")
                    print(f"🛑 [{get_current_time_str()}] [DATADOME BLOCK] 3x403! Перерва 60 секунд...")
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
    print(f"\n🌐 [{get_current_time_str()}] [SERVERS] Запуск FastAPI бекенду (uvicorn)...")
    try:
        server_process = subprocess.Popen(
            [sys.executable, "-m", "uvicorn", "server:app", "--reload", "--port", "8000"],
            cwd=str(server_dir),
            shell=(os.name == "nt")
        )
        append_to_debug_file(f"🌐 **[{get_current_time_str()}] [SERVERS]** Успішно запущено FastAPI (uvicorn).")
    except Exception as e:
        print(f"❌ Не вдалося запустити сервер: {e}")
        append_to_debug_file(f"❌ **[{get_current_time_str()}] [SERVERS]** Помилка запуску: `{e}`")
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
        await run_logged_module("BACKGROUND_CLEAN_ARCHIVE", clean_archive.main_async, db_lock=db_write_lock)


async def background_price_hardware():
    """Фоновий перерахунок ринкових цін заліза кожні 5 хвилин."""
    while True:
        await asyncio.sleep(300)
        await run_logged_module("BACKGROUND_PRICE_HARDWARE", price_hardware.main_async, db_lock=db_write_lock)


# =====================================================================
# ОСНОВНИЙ ЦИКЛ ПАРСИНGU ТА ОЦІНКИ
# =====================================================================
iteration_counter = 0

async def run_pipeline_iteration(is_first_run: bool = False):
    global iteration_counter
    iteration_counter += 1
    
    today_str = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    log_section_header(f"Ітерація #{iteration_counter} ({today_str}) | req_limit={primary_limiter.current_rate:.1f}/min")
    
    print(f"\n🔄 [{get_current_time_str()}] [24/7 ASYNC LOOP] Ітерація #{iteration_counter} | Ліміт: {primary_limiter.current_rate:.1f} req/min")

    pages_to_parse = 4 if is_first_run else 1

    # 1. Запуск двох парсерів паралельно
    await asyncio.gather(
        run_logged_module("PARSER_PC", parser.main_async, pages_to_parse=pages_to_parse, db_lock=db_write_lock, rate_limiter=primary_limiter),
        run_logged_module("PARSER_HARDWARE", parser_hardware.main_async, pages_to_parse=pages_to_parse, db_lock=db_write_lock, rate_limiter=primary_limiter)
    )

    # 2. Фільтрація
    await run_logged_module("FILTER_ADS", filter_ads.main_async, db_lock=db_write_lock)

    # 3. Аналіз та оцінка
    unprocessed_count = await count_unprocessed_ads()
    await asyncio.to_thread(append_to_debug_file, f"📊 **[{get_current_time_str()}] [АНАЛІЗ]** Нових релевантних лотів для обробки: `{unprocessed_count}`")
    print(f"📊 [{get_current_time_str()}] [АНАЛІЗ] Нових релевантних лотів: {unprocessed_count}")

    if unprocessed_count > 0:
        # Паралельна оцінка вигідності ПК та комплектуючих
        await asyncio.gather(
            run_logged_module("PC_EVALUATOR", pc_evaluator.main_async, db_lock=db_write_lock),
            run_logged_module("HARDWARE_EVALUATOR", hardware_evaluator.main_async, db_lock=db_write_lock)
        )

        # 4. Продавці та конкуренти
        results = await asyncio.gather(
            run_logged_module("SELLER_ANALYZER", seller_analyzer.main_async, db_lock=db_write_lock),
            run_logged_module("COMPETITOR_FINDER", competitor_finder.main_async, db_lock=db_write_lock)
        )
        
        updated_seller_ids, updated_comp_ids = results[0], results[1]
        all_updated = list(set((updated_seller_ids or []) + (updated_comp_ids or [])))
        
        if all_updated:
            await run_logged_module("WEBSOCKET_BROADCAST", broadcast_updated_ads, updated_ids=all_updated)


async def main():
    start_msg = f"# 🚀 [СТАРТ СИСТЕМИ] Асинхронний Оркестратор ({get_current_time_str()})"
    await asyncio.to_thread(append_to_debug_file, f"\n{start_msg}\n")
    
    print("==========================================================")
    print(f" 🚀 [{get_current_time_str()}] СТАРТ АСИНХРОННОГО ОРКЕСТРАТОРА 24/7 ")
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
            await asyncio.to_thread(append_to_debug_file, f"⏱️ **[{get_current_time_str()}]** Ітерацію завершено за `{elapsed:.2f}s`. Пауза 20s...\n")
            print(f"\n⏱️ [{get_current_time_str()}] Ітерацію завершено за {elapsed:.2f} сек. Пауза 20 сек...")
            await asyncio.sleep(20)
        except Exception as ex:
            await asyncio.to_thread(append_to_debug_file, f"❌ **[{get_current_time_str()}] [КРИТИЧНА ПОМИЛКА ЦИКЛУ]**: `{ex}`\n")
            print(f"❌ [{get_current_time_str()}] [КРИТИЧНА ПОМИЛКА ЦИКЛУ]: {ex}")
            await asyncio.sleep(10)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        append_to_debug_file(f"\n🛑 **[{get_current_time_str()}]** Зупинка оркестратора за запитом користувача.")
        print(f"\n🛑 [{get_current_time_str()}] Зупинка оркестратора.")
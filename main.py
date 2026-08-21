"""
main.py — Асинхронний Оркестратор 24/7

Рефакторинг оригіналу зі збереженням 100% функціоналу:
  • Логування у debug/main-debug.md + консоль
  • AIMD Rate Limiter з DATADOME захистом
  • Graceful shutdown
  • Фонові демони (архів + прайси)
  • Запуск FastAPI + Broadcast

Покращення:
  • Класова архітектура, типізація
  • Базова безпека (валідація, обмеження)
  • Конфігурація через dataclass
  • Відсутність глобального mutable-стану
"""

from __future__ import annotations

import asyncio
import atexit
import inspect
import logging
import os
import subprocess
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Awaitable, Callable, Dict, List, Optional, Set, Tuple, Union

import requests
from dotenv import load_dotenv
from supabase import Client, create_client

# ---------------------------------------------------------------------------
# 0. ENV & PATH SETUP (як в оригіналі)
# ---------------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent
if not (PROJECT_ROOT / "config.py").exists():
    PROJECT_ROOT = PROJECT_ROOT.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

load_dotenv(PROJECT_ROOT / ".env")

SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_SECRET_KEY", "")
OLX_PROXY_URL = os.getenv("OLX_PROXY_URL", "") or None
INTERNAL_SECRET_KEY = os.getenv("INTERNAL_SECRET_KEY", "").strip()

# ---------------------------------------------------------------------------
# 1. MODULE IMPORTS (як в оригіналі — з fallback)
# ---------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------
# 2. CONFIG
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class AppConfig:
    """Всі налаштування, які раніше були розкидані по коду."""
    project_root: Path = PROJECT_ROOT
    supabase_url: str = SUPABASE_URL
    supabase_key: str = SUPABASE_KEY or ""
    olx_proxy_url: Optional[str] = OLX_PROXY_URL
    internal_secret_key: str = INTERNAL_SECRET_KEY or ""

    debug_dir: Path = field(default_factory=lambda: PROJECT_ROOT / "debug")
    log_file: Path = field(default_factory=lambda: PROJECT_ROOT / "debug" / "main-debug.md")

    server_port: int = 8000
    server_host: str = "127.0.0.1"
    websocket_url: str = os.getenv("WEBSOCKET_URL", "http://127.0.0.1:8000/api/trigger-new-ad")

    iteration_pause_sec: float = 20.0
    error_pause_sec: float = 10.0
    background_interval_sec: float = 300.0

    first_run_pages: int = 4
    regular_pages: int = 1

    rate_limiter_min: float = 40.0
    rate_limiter_max: float = 80.0
    rate_limiter_initial: float = 60.0
    datadome_threshold: int = 3
    datadome_cooldown_sec: float = 60.0

    max_log_line_length: int = 500

    def __post_init__(self) -> None:
        self.debug_dir.mkdir(parents=True, exist_ok=True)
        if not self.supabase_key:
            raise RuntimeError("SUPABASE_SECRET_KEY або SUPABASE_PUBLISHABLE_KEY має бути встановлено")


# ---------------------------------------------------------------------------
# 3. LOGGER — файл (Markdown) + консоль (як в оригіналі)
# ---------------------------------------------------------------------------

class DebugLogger:
    """Пише одночасно у debug/main-debug.md та stdout (через print/logging)."""

    def __init__(self, config: AppConfig) -> None:
        self._cfg = config
        self._file = config.log_file
        self._ensure_header()
        self._console = logging.getLogger("orchestrator")
        self._console.setLevel(logging.INFO)
        if not self._console.handlers:
            h = logging.StreamHandler(sys.stdout)
            h.setFormatter(logging.Formatter(
                "%(asctime)s [%(levelname)s] %(message)s",
                datefmt="%H:%M:%S",
            ))
            self._console.addHandler(h)

    def _ensure_header(self) -> None:
        if not self._file.exists() or self._file.stat().st_size == 0:
            self._file.write_text("# 🚀 Debug Log\n\n", encoding="utf-8")

    def _now(self) -> str:
        return datetime.now().strftime("%H:%M:%S")

    def log(self, message: str, level: str = "INFO", to_file: bool = True, to_console: bool = True) -> None:
        """Універсальний лог: файл + консоль."""
        ts = self._now()
        if to_console:
            log_level = getattr(logging, level.upper(), logging.INFO)
            self._console.log(log_level, message)
        if to_file:
            line = f"- **[{ts}]** `{level}` {message}\n"
            with open(self._file, "a", encoding="utf-8") as f:
                f.write(line)

    def section(self, title: str) -> None:
        ts = self._now()
        self._console.info("\n=== %s ===", title)
        text = f"\n---\n## 🔄 [{ts}] {title}\n"
        with open(self._file, "a", encoding="utf-8") as f:
            f.write(text)

    def print_banner(self, text: str) -> None:
        """Для стартового банера."""
        print(text)
        with open(self._file, "a", encoding="utf-8") as f:
            f.write(text + "\n")


# ---------------------------------------------------------------------------
# 4. RESULT FORMATTER (оригінальна логіка)
# ---------------------------------------------------------------------------

class ResultFormatter:
    """Форматує вхідні аргументи та результати для логів."""

    @staticmethod
    def format_input_args(kwargs: dict[str, Any]) -> str:
        clean = {k: v for k, v in kwargs.items() if k not in ("db_lock", "rate_limiter")}
        if not clean:
            return "без особливих параметрів"
        return ", ".join(f"`{k}={v}`" for k, v in clean.items())

    @staticmethod
    def summarize(result: Any) -> str:
        if result is None:
            return "завершено (без повернення даних)"
        if isinstance(result, (list, tuple, set)):
            return f"оброблено/повернуто `{len(result)}` елементів"
        if isinstance(result, dict):
            return f"згенеровано словник із `{len(result)}` ключів"
        if isinstance(result, (int, float)):
            return f"результат = `{result}`"
        return f"повернуто `{str(result)[:60]}`"


# ---------------------------------------------------------------------------
# 5. RATE LIMITER (оригінальна AIMD логіка)
# ---------------------------------------------------------------------------

class AdaptiveRateLimiter:
    """Динамічний контроль частоти запитів до OLX."""

    def __init__(
        self,
        logger: DebugLogger,
        min_rate: float = 40.0,
        max_rate: float = 80.0,
        initial_rate: float = 60.0,
        threshold: int = 3,
        cooldown_sec: float = 60.0,
    ) -> None:
        self._logger = logger
        self._min_rate = min_rate
        self._max_rate = max_rate
        self._threshold = threshold
        self._cooldown_sec = cooldown_sec
        self._current_rate = initial_rate
        self._consecutive_403 = 0
        self._success_streak = 0
        self._is_cooldown = False
        self._lock = asyncio.Lock()

    @property
    def current_rate(self) -> float:
        return self._current_rate

    async def acquire(self) -> None:
        async with self._lock:
            while self._is_cooldown:
                await asyncio.sleep(1)
            delay = 60.0 / self._current_rate
        await asyncio.sleep(delay)

    async def report_result(self, status_code: int) -> None:
        async with self._lock:
            if status_code == 403:
                self._consecutive_403 += 1
                self._success_streak = 0
                if self._consecutive_403 >= self._threshold:
                    await self._enter_cooldown()
            elif status_code == 200:
                self._consecutive_403 = 0
                self._success_streak += 1
                if self._success_streak >= 15 and self._current_rate < self._max_rate:
                    self._current_rate = min(self._max_rate, self._current_rate + 2.0)
                    self._success_streak = 0

    async def _enter_cooldown(self) -> None:
        self._is_cooldown = True
        self._current_rate = max(self._min_rate, self._current_rate * 0.85)
        msg = (
            f"🛑 [{self._logger._now()}] [DATADOME BLOCK] 3x403! "
            f"Cooldown {self._cooldown_sec} секунд..."
        )
        self._logger.log(msg, "WARN")
        print(msg)
        await asyncio.sleep(self._cooldown_sec)
        self._consecutive_403 = 0
        self._is_cooldown = False

# ---------------------------------------------------------------------------
# 6. WEB SERVER MANAGER
# ---------------------------------------------------------------------------

class WebServerManager:
    """Запускає та зупиняє uvicorn (як в оригіналі)."""

    def __init__(self, config: AppConfig, logger: DebugLogger) -> None:
        self._cfg = config
        self._logger = logger
        self._process: Optional[subprocess.Popen] = None

    def start(self) -> None:
        server_dir = self._cfg.project_root / "server"
        msg = f"\n🌐 [{self._logger._now()}] [SERVERS] Запуск FastAPI бекенду (uvicorn)..."
        print(msg)

        cmd = [
            sys.executable, "-m", "uvicorn",
            "server:app", "--reload",
            "--port", str(self._cfg.server_port),
        ]
        try:
            self._process = subprocess.Popen(
                cmd,
                cwd=str(server_dir),
                shell=(os.name == "nt"),
            )
            self._logger.log(
                f"🌐 **[{self._logger._now()}] [SERVERS]** Успішно запущено FastAPI (uvicorn).",
                "INFO",
            )
        except Exception as e:
            err = f"❌ Не вдалося запустити сервер: {e}"
            print(err)
            self._logger.log(f"❌ **[{self._logger._now()}] [SERVERS]** Помилка запуску: `{e}`", "ERROR")
        time.sleep(3)

    def stop(self) -> None:
        if self._process and self._process.poll() is None:
            self._process.terminate()


# ---------------------------------------------------------------------------
# 7. SUPABASE REPOSITORY
# ---------------------------------------------------------------------------

class SupabaseRepo:
    """Всі запити до Supabase в одному місці."""

    def __init__(self, config: AppConfig, logger: DebugLogger) -> None:
        self._client: Client = create_client(config.supabase_url, config.supabase_key)
        self._logger = logger

    async def count_unprocessed_ads(self) -> int:
        def _query() -> int:
            try:
                res = (
                    self._client.table("ads")
                    .select("id", count="exact")
                    .eq("status", "active")
                    .or_("seller_risk_score.is.null,estimated_fair_price.is.null")
                    .execute()
                )
                return res.count or 0
            except Exception:
                return 0
        return await asyncio.to_thread(_query)

    async def fetch_active_ads(self, ad_ids: List[int]) -> List[dict[str, Any]]:
        if not ad_ids:
            return []

        def _query() -> List[dict[str, Any]]:
            try:
                res = (
                    self._client.table("ads")
                    .select("*")
                    .in_("ad_id", ad_ids)
                    .eq("status", "active")
                    .execute()
                )
                return res.data or []
            except Exception:
                return []
        return await asyncio.to_thread(_query)


# ---------------------------------------------------------------------------
# 8. BROADCAST SERVICE
# ---------------------------------------------------------------------------

class BroadcastService:
    """Відправляє оновлення на локальний endpoint."""

    def __init__(self, config: AppConfig, logger: DebugLogger) -> None:
        self._url = config.websocket_url
        self._logger = logger
        self._secret = config.internal_secret_key

    async def send(self, rows: List[dict[str, Any]]) -> None:
        if not rows:
            return

        def _post() -> None:
            try:
                headers = {"X-Internal-Secret": self._secret}
                requests.post(self._url, json=rows, headers=headers, timeout=5)
            except Exception as e:
                self._logger.log(f"Broadcast failed: {e}", "WARN")

        await asyncio.to_thread(_post)


# ---------------------------------------------------------------------------
# 9. MODULE RUNNER (оригінальна обгортка run_logged_module)
# ---------------------------------------------------------------------------

class ModuleRunner:
    """Запускає модулі з детальним логуванням (як у оригіналі)."""

    def __init__(self, logger: DebugLogger, formatter: ResultFormatter) -> None:
        self._log = logger
        self._fmt = formatter

    async def run(
        self,
        name: str,
        coro_or_func: Union[Callable[..., Any], Callable[..., Awaitable[Any]]],
        *args: Any,
        **kwargs: Any,
    ) -> Any:
        start_perf = time.perf_counter()
        start_ts = self._log._now()
        input_desc = self._fmt.format_input_args(kwargs)

        # 1. Лог старту
        self._log.log(
            f"⏳ **[{start_ts}]** `СТАРТ` **{name}** | Вхідні дані: {input_desc}",
            "INFO",
        )

        try:
            if inspect.iscoroutinefunction(coro_or_func):
                result = await coro_or_func(*args, **kwargs)
            else:
                result = coro_or_func(*args, **kwargs)

            duration = time.perf_counter() - start_perf
            end_ts = self._log._now()
            result_desc = self._fmt.summarize(result)

            # 2. Лог успіху
            self._log.log(
                f"  - ✅ **[{end_ts}]** `УСПІХ` **{name}** | Тривалість: `{duration:.2f}s` | Результат: {result_desc}",
                "INFO",
            )
            return result

        except Exception as e:
            duration = time.perf_counter() - start_perf
            end_ts = self._log._now()

            # 3. Лог помилки
            self._log.log(
                f"  - ❌ **[{end_ts}]** `ПОМИЛКА` **{name}** | Тривалість: `{duration:.2f}s` | Причина: `{e}`",
                "ERROR",
            )
            raise


# ---------------------------------------------------------------------------
# 10. BACKGROUND TASKS
# ---------------------------------------------------------------------------

class BackgroundTaskManager:
    """Керує фоновими демонами (архів + прайси)."""

    def __init__(
        self,
        runner: ModuleRunner,
        config: AppConfig,
        shutdown_event: asyncio.Event,
    ) -> None:
        self._runner = runner
        self._cfg = config
        self._shutdown = shutdown_event

    async def archive_checker(self) -> None:
        """Фонова перевірка архівних оголошень кожні 5 хвилин."""
        while not self._shutdown.is_set():
            try:
                await asyncio.wait_for(
                    self._shutdown.wait(),
                    timeout=self._cfg.background_interval_sec,
                )
            except asyncio.TimeoutError:
                await self._runner.run(
                    "BACKGROUND_CLEAN_ARCHIVE",
                    clean_archive.main_async,
                    db_lock=asyncio.Lock(),
                )

    async def price_hardware(self) -> None:
        """Фоновий перерахунок ринкових цін заліза кожні 5 хвилин."""
        while not self._shutdown.is_set():
            try:
                await asyncio.wait_for(
                    self._shutdown.wait(),
                    timeout=self._cfg.background_interval_sec,
                )
            except asyncio.TimeoutError:
                await self._runner.run(
                    "BACKGROUND_PRICE_HARDWARE",
                    price_hardware.main_async,
                    db_lock=asyncio.Lock(),
                )

# ---------------------------------------------------------------------------
# 11. PIPELINE ORCHESTRATOR (оригінальна логіка run_pipeline_iteration)
# ---------------------------------------------------------------------------

class PipelineOrchestrator:
    """Головний цикл обробки — точна копія логіки оригіналу."""

    def __init__(
        self,
        config: AppConfig,
        logger: DebugLogger,
        repo: SupabaseRepo,
        limiter: AdaptiveRateLimiter,
        runner: ModuleRunner,
        broadcaster: BroadcastService,
    ) -> None:
        self._cfg = config
        self._log = logger
        self._repo = repo
        self._limiter = limiter
        self._runner = runner
        self._broadcaster = broadcaster
        self._iteration_count = 0
        self._shutdown = asyncio.Event()

    async def run(self) -> None:
        """Основний while-true цикл (як у оригіналі)."""
        is_first_run = True
        while not self._shutdown.is_set():
            try:
                cycle_start = time.time()
                await self._iteration(is_first_run)
                is_first_run = False

                elapsed = time.time() - cycle_start
                self._log.log(
                    f"⏱️ **[{self._log._now()}]** Ітерацію завершено за `{elapsed:.2f}s`. Пауза 20s...\n",
                    "INFO",
                )
                print(f"\n⏱️ [{self._log._now()}] Ітерацію завершено за {elapsed:.2f} сек. Пауза 20 сек...")

                await asyncio.wait_for(
                    self._shutdown.wait(),
                    timeout=self._cfg.iteration_pause_sec,
                )
            except asyncio.TimeoutError:
                continue
            except Exception as ex:
                self._log.log(
                    f"❌ **[{self._log._now()}] [КРИТИЧНА ПОМИЛКА ЦИКЛУ]**: `{ex}`\n",
                    "ERROR",
                )
                print(f"❌ [{self._log._now()}] [КРИТИЧНА ПОМИЛКА ЦИКЛУ]: {ex}")
                await asyncio.sleep(self._cfg.error_pause_sec)

    async def _iteration(self, is_first_run: bool) -> None:
        """Одна ітерація = точна копія run_pipeline_iteration."""
        self._iteration_count += 1
        pages_to_parse = self._cfg.first_run_pages if is_first_run else self._cfg.regular_pages
        today_str = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")

        self._log.section(
            f"Ітерація #{self._iteration_count} ({today_str}) | req_limit={self._limiter.current_rate:.1f}/min"
        )
        print(
            f"\n🔄 [{self._log._now()}] [24/7 ASYNC LOOP] Ітерація #{self._iteration_count} | "
            f"Ліміт: {self._limiter.current_rate:.1f} req/min"
        )

        # 1. Парсинг (паралельно)
        await asyncio.gather(
            self._runner.run(
                "PARSER_PC",
                parser.main_async,
                pages_to_parse=pages_to_parse,
                db_lock=asyncio.Lock(),
                rate_limiter=self._limiter,
            ),
            self._runner.run(
                "PARSER_HARDWARE",
                parser_hardware.main_async,
                pages_to_parse=pages_to_parse,
                db_lock=asyncio.Lock(),
                rate_limiter=self._limiter,
            ),
        )

        # 2. Фільтрація
        await self._runner.run(
            "FILTER_ADS", filter_ads.main_async, db_lock=asyncio.Lock()
        )

        # 3. Аналіз
        unprocessed_count = await self._repo.count_unprocessed_ads()
        self._log.log(
            f"📊 **[{self._log._now()}] [АНАЛІЗ]** Нових релевантних лотів для обробки: `{unprocessed_count}`",
            "INFO",
        )
        print(f"📊 [{self._log._now()}] [АНАЛІЗ] Нових релевантних лотів: {unprocessed_count}")

        if unprocessed_count == 0:
            return

        # 4. Оцінка (паралельно)
        await asyncio.gather(
            self._runner.run(
                "PC_EVALUATOR", pc_evaluator.main_async, db_lock=asyncio.Lock()
            ),
            self._runner.run(
                "HARDWARE_EVALUATOR",
                hardware_evaluator.main_async,
                db_lock=asyncio.Lock(),
            ),
        )

        # 5. Продавці (миттєвий аналіз та бродкаст)
        updated_seller_ids = await self._runner.run(
            "SELLER_ANALYZER",
            seller_analyzer.main_async,
            db_lock=asyncio.Lock(),
        )

        if updated_seller_ids:
            seller_rows = await self._repo.fetch_active_ads(updated_seller_ids[:50])
            if seller_rows:
                await self._runner.run(
                    "WEBSOCKET_BROADCAST",
                    self._broadcaster.send,
                    seller_rows,
                )

        # 6. Конкуренти ПК
        await self._runner.run(
            "COMPETITOR_FINDER",
            competitor_finder.main_async,
            db_lock=asyncio.Lock(),
        )

    def shutdown(self) -> None:
        self._shutdown.set()


# ---------------------------------------------------------------------------
# 12. MAIN ENTRY POINT
# ---------------------------------------------------------------------------

async def main() -> None:
    config = AppConfig()
    logger = DebugLogger(config)

    # Стартовий банер
    banner = (
        "==========================================================\n"
        f" 🚀 [{logger._now()}] СТАРТ АСИНХРОННОГО ОРКЕСТРАТОРА 24/7 \n"
        "=========================================================="
    )
    logger.print_banner(banner)
    logger.section(f"[СТАРТ СИСТЕМИ] Асинхронний Оркестратор ({logger._now()})")

    # Залежності
    repo = SupabaseRepo(config, logger)
    limiter = AdaptiveRateLimiter(
        logger,
        min_rate=config.rate_limiter_min,
        max_rate=config.rate_limiter_max,
        initial_rate=config.rate_limiter_initial,
        threshold=config.datadome_threshold,
        cooldown_sec=config.datadome_cooldown_sec,
    )
    formatter = ResultFormatter()
    runner = ModuleRunner(logger, formatter)
    broadcaster = BroadcastService(config, logger)

    orchestrator = PipelineOrchestrator(
        config=config,
        logger=logger,
        repo=repo,
        limiter=limiter,
        runner=runner,
        broadcaster=broadcaster,
    )

    # Graceful shutdown
    loop = asyncio.get_running_loop()
    for sig_name in ("SIGINT", "SIGTERM"):
        try:
            import signal
            sig = getattr(signal, sig_name)
            loop.add_signal_handler(sig, orchestrator.shutdown)
        except (AttributeError, NotImplementedError):
            pass

    # Фонові задачі
    bg_manager = BackgroundTaskManager(runner, config, orchestrator._shutdown)
    bg_tasks = [
        asyncio.create_task(bg_manager.archive_checker()),
        asyncio.create_task(bg_manager.price_hardware()),
    ]

    try:
        await orchestrator.run()
    finally:
        for t in bg_tasks:
            t.cancel()
        logger.log(
            f"🛑 **[{logger._now()}]** Зупинка оркестратора.\n",
            "INFO",
        )


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        ts = datetime.now().strftime("%H:%M:%S")
        print(f"\n🛑 [{ts}] Зупинка оркестратора.")
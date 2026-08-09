"""
OLX PC Parser — Production Ready
=================================
Асинхронний збір оголошень готових ПК з OLX GraphQL API (category_id=78).

Архітектура:
  • DI + Repository Pattern
  • Pydantic-валідація
  • Metrics + Tracing + Structured Logging
  • Graceful shutdown
  • Без глобального стану

Залежності:
  pip install pydantic supabase-py python-dotenv curl_cffi aiohttp structlog
"""

from __future__ import annotations

import asyncio
import hashlib
import json
import logging
import os
import re
import signal
import sys
import time
from abc import ABC, abstractmethod
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

import aiohttp
from curl_cffi.requests import AsyncSession
from dotenv import load_dotenv
from pydantic import BaseModel, Field, field_validator
from supabase import Client, create_client

try:
    import structlog
    _HAS_STRUCTLOG = True
except ImportError:
    _HAS_STRUCTLOG = False

# ---------------------------------------------------------------------------
# Зовнішні залежності
# ---------------------------------------------------------------------------
try:
    from config import STATS_FILE
except ImportError:
    _project_root = Path(__file__).resolve().parent.parent
    if str(_project_root) not in sys.path:
        sys.path.insert(0, str(_project_root))
    try:
        from config import STATS_FILE
    except ImportError:
        STATS_FILE = Path("stats.json")


# ===========================================================================
# 0. OBSERVABILITY
# ===========================================================================
class TraceIdFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        if not hasattr(record, "trace_id"):
            record.trace_id = "system"
        return True


def _setup_logging() -> None:
    """Налаштування логування: консоль + файл з ротацією.

    Сторонні бібліотеки (httpx, httpcore, hpack) — тільки WARNING+,
    щоб не захламлювати логи HTTP/2 debug-шумом.
    """
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    log_file = str(log_dir / "parser.log")

    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s trace=%(trace_id)s — %(message)s",
        datefmt="%H:%M:%S",
    )

    root = logging.getLogger()

    # Чистимо старі хендлери, щоб уникнути дублікатів
    for old_handler in root.handlers[:]:
        root.removeHandler(old_handler)
        old_handler.close()

    # Консоль
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    console.addFilter(TraceIdFilter())
    console.setFormatter(formatter)
    root.addHandler(console)

    # Файл з ротацією (10MB, 5 бекапів)
    from logging.handlers import RotatingFileHandler
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=10 * 1024 * 1024,
        backupCount=5,
        encoding="utf-8",
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.addFilter(TraceIdFilter())
    file_handler.setFormatter(formatter)
    root.addHandler(file_handler)

    root.setLevel(logging.DEBUG)

    # 🔇 Глушимо шум сторонніх бібліотек
    for noisy in ("httpx", "httpcore", "hpack", "hpack.table", "asyncio"):
        logging.getLogger(noisy).setLevel(logging.WARNING)


_setup_logging()


class PrettyMetrics:
    """Форматує метрики у зрозумілу таблицю."""

    LABELS: dict[str, str] = {
        "db_fetch_urls": "🗄️  DB fetch URLs",
        "db_upsert_pcs": "🗄️  DB upsert PCs",
        "olx_fetch_page": "🌐 OLX fetch page",
        "parser_total": "⏱️  Total runtime",
    }

    @classmethod
    def format(cls, snapshot: dict[str, Any]) -> str:
        lines = ["\n📊 Performance Breakdown"]
        timers = snapshot.get("timers", {})
        for key, label in cls.LABELS.items():
            if key in timers:
                t = timers[key]
                lines.append(f"   {label:<20} : {t['avg_ms']:>6.1f}ms  ({t['count']} call{'s' if t['count'] > 1 else ''})")
        counters = snapshot.get("counters", {})
        if "olx_listings_received" in counters:
            lines.append(f"   📥 OLX listings received : {counters['olx_listings_received']}")
        if "db_upsert_pcs_count" in counters:
            lines.append(f"   💾 PCs saved to DB       : {counters['db_upsert_pcs_count']}")
        return "\n".join(lines)


class TracingContext:
    def __init__(self) -> None:
        self.trace_id = hashlib.sha256(
            f"{time.time()}{os.urandom(8)}".encode()
        ).hexdigest()[:16]


def _get_logger(name: str, trace: TracingContext | None = None) -> Any:
    """Завжди використовуємо стандартний logging (structlog може конфліктувати з FileHandler)."""
    extra = {"trace_id": trace.trace_id} if trace else {}
    logger = logging.getLogger(name)
    if extra:
        return logging.LoggerAdapter(logger, extra)
    return logger


class MetricsCollector:
    """Thread-safe/async-safe метрики."""

    def __init__(self) -> None:
        self._counters: dict[str, int] = defaultdict(int)
        self._timers: dict[str, dict[str, float]] = defaultdict(lambda: {"count": 0.0, "total_sec": 0.0})
        self._lock = asyncio.Lock()

    async def inc(self, name: str, value: int = 1) -> None:
        async with self._lock:
            self._counters[name] += value

    async def time(self, name: str, duration_sec: float) -> None:
        async with self._lock:
            s = self._timers[name]
            s["count"] += 1
            s["total_sec"] += duration_sec

    def snapshot(self) -> dict[str, Any]:
        return {
            "counters": dict(self._counters),
            "timers": {
                k: {
                    "count": int(v["count"]),
                    "avg_ms": round((v["total_sec"] / v["count"]) * 1000, 2) if v["count"] else 0,
                }
                for k, v in self._timers.items()
            },
        }


# ===========================================================================
# 1. CONFIG
# ===========================================================================
class EnvConfig(BaseModel):
    """Валідація змінних оточення."""

    supabase_url: str = Field(default="", min_length=1)
    supabase_secret_key: str = Field(default="", min_length=1)
    olx_proxy_url: str = Field(default="")
    request_timeout: int = Field(default=15, gt=0)
    max_retries: int = Field(default=5, ge=1, le=10)
    pages_to_parse: int = Field(default=1, ge=1, le=20)
    impersonate_browser: str = Field(default="chrome124")
    stats_file: Path = Field(default=Path("stats.json"))
    websocket_trigger_url: str = Field(default="http://localhost:8000/api/trigger-new-ad")

    @field_validator("supabase_url")
    @classmethod
    def _url_https(cls, v: str) -> str:
        if v and not v.startswith("https://"):
            raise ValueError("SUPABASE_URL має починатися з https://")
        return v.rstrip("/") if v else v


@dataclass(frozen=True)
class PcParserConfig:
    """Бізнес-конфігурація парсера ПК."""

    category_id: str = "78"
    not_a_pc_words: tuple[str, ...] = field(default_factory=lambda: (
        "материнська плата", "материнская плата", "материнка", "мать",
        "блок питания", "блок живлення", "дбж", "ups", "бесперебойник",
        "оперативна память", "оперативная память", "озу", "ram",
        "кулер", "вентилятор", "корпус без", "видеокарта", "відеокарта",
        "процессор", "процесор", "ssd", "hdd", "жесткий диск", "жорсткий диск",
    ))
    pc_indicators: tuple[str, ...] = field(default_factory=lambda: (
        "пк", "комп", "системний блок", "системный блок", "компьютер",
        "комп'ютер", "системник", "pc", "mac", "блок", "сервер", "станці",
        "workstation", "игров", "ігров", "ноутбук",
    ))
    headers: dict[str, str] = field(default_factory=lambda: {
        "accept": "application/json",
        "accept-language": "uk",
        "content-type": "application/json",
        "origin": "https://www.olx.ua",
        "referer": "https://www.olx.ua/",
        "user-agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        ),
        "x-client": "DESKTOP",
    })
    graphql_query: str = (
        "query ListingSearchQuery($searchParameters: [SearchParameter!] = []) {"
        "  clientCompatibleListings(searchParameters: $searchParameters) {"
        "    ... on ListingSuccess {"
        "      data {"
        "        id title status url created_time last_refresh_time description business"
        "        location { city { name } }"
        "        photos { link }"
        "        user { id uuid name created }"
        "        params {"
        "          key name"
        "          value {"
        "            ... on PriceParam { value currency label }"
        "          }"
        "        }"
        "      }"
        "    }"
        "  }"
        "}"
    )


# ===========================================================================
# 2. DOMAIN MODEL
# ===========================================================================
class ParsedPc(BaseModel):
    """Одне розпізнане оголошення ПК."""

    ad_id: int | None = None
    url: str = Field(min_length=1)
    parsed_date: str = Field(min_length=1)
    status: str = "active"
    title: str = Field(min_length=1)
    description: str = ""
    price: int = Field(default=0, ge=0, le=1_000_000_000)
    item_type: str = "pc"
    component_name: str | None = None
    city: str = "Невідомо"
    created_at_olx: str = "Невідомо"
    last_refresh_time: str = "Невідомо"
    photo_url: str = "Невідомо"
    photos: str | None = None
    all_photos: str | None = None
    seller_id: str | None = None
    seller_uuid: str | None = None
    seller_name: str = "Невідомо"
    seller_created_at: str | None = None
    seller_type: str = "private_person"
    seller_price_clean: int = Field(default=0, ge=0)


# ===========================================================================
# 3. REPOSITORY
# ===========================================================================
class PcAdsRepository(ABC):
    """Інтерфейс для роботи з оголошеннями ПК в БД."""

    @abstractmethod
    async def fetch_seen_urls(self) -> set[str]:
        ...

    @abstractmethod
    async def upsert_pcs(self, pcs: list[ParsedPc]) -> int:
        ...


class SupabasePcAdsRepository(PcAdsRepository):
    def __init__(self, client: Client, metrics: MetricsCollector, trace: TracingContext) -> None:
        self._client = client
        self._metrics = metrics
        self._trace = trace
        self._logger = _get_logger(__name__, trace)

    async def fetch_seen_urls(self) -> set[str]:
        def _fetch() -> set[str]:
            try:
                resp = self._client.table("ads").select("url").execute()
                return {row["url"] for row in (resp.data or [])}
            except Exception as exc:
                self._logger.error("fetch_seen_urls_failed: %s", str(exc))
                return set()

        t0 = time.monotonic()
        result = await asyncio.to_thread(_fetch)
        await self._metrics.time("db_fetch_urls", time.monotonic() - t0)
        await self._metrics.inc("db_fetch_urls_count", len(result))
        self._logger.info("seen_urls_loaded: count=%s", len(result))
        return result

    async def upsert_pcs(self, pcs: list[ParsedPc]) -> int:
        if not pcs:
            return 0

        dicts = [p.model_dump(exclude_none=True) for p in pcs]

        def _upsert() -> None:
            self._client.table("ads").upsert(dicts, on_conflict="ad_id").execute()

        try:
            t0 = time.monotonic()
            await asyncio.to_thread(_upsert)
            duration = time.monotonic() - t0
            await self._metrics.time("db_upsert_pcs", duration)
            await self._metrics.inc("db_upsert_pcs_count", len(pcs))
            self._logger.info("pcs_upserted: count=%s", len(pcs))
            return len(pcs)
        except Exception as exc:
            self._logger.error("pcs_upsert_failed: %s", str(exc))
            await self._metrics.inc("db_upsert_pcs_failures")
            return 0


class StatsRepository(ABC):
    """Інтерфейс для збереження статистики."""

    @abstractmethod
    async def update(self, section: str, metrics: dict[str, Any]) -> None:
        ...


class JsonStatsRepository(StatsRepository):
    """Зберігає статистику у JSON-файл."""

    def __init__(self, file_path: Path, trace: TracingContext) -> None:
        self._file = file_path
        self._logger = _get_logger(__name__, trace)

    async def update(self, section: str, metrics: dict[str, Any]) -> None:
        def _write() -> None:
            today = datetime.now(timezone.utc).strftime("%d-%m-%Y")
            stats: dict[str, Any] = {}
            if self._file.exists():
                try:
                    stats = json.loads(self._file.read_text(encoding="utf-8"))
                except json.JSONDecodeError:
                    stats = {}

            if today not in stats:
                stats[today] = {
                    "parsing": {"parsed_total_new": 0, "duplicates_skipped": 0, "avg_parsing_time_ms": 0.0, "total_time_seconds": 0.0},
                    "filtering": {"banned_words_triggered": 0, "filtered_total_active": 0},
                    "market_analysis": {"avg_ad_price_uah": 0, "min_price_today": 0, "max_price_today": 0},
                    "system_health": {"network_errors": 0, "parsing_errors": 0},
                }

            if section in stats[today]:
                stats[today][section].update(metrics)

            self._file.write_text(json.dumps(stats, ensure_ascii=False, indent=2), encoding="utf-8")

        try:
            await asyncio.to_thread(_write)
            self._logger.info("stats_updated: section=%s", section)
        except Exception as exc:
            self._logger.warning("stats_update_failed: %s", str(exc))


# ===========================================================================
# 4. PURE FUNCTIONS
# ===========================================================================
def clean_url(url: str) -> str:
    parsed = urlparse(url)
    return f"{parsed.scheme}://{parsed.netloc}{parsed.path}"


def extract_price(price_val: str | int | float) -> int:
    if isinstance(price_val, (int, float)):
        return int(price_val)
    digits = re.sub(r"\D", "", str(price_val))
    return int(digits) if digits else 0


def is_real_pc(title: str, cfg: PcParserConfig) -> tuple[bool, str]:
    if not title:
        return False, "empty_title"

    title_lower = title.lower()
    for bad_word in cfg.not_a_pc_words:
        if bad_word in title_lower:
            if title_lower.startswith(bad_word):
                return False, f"starts_with_banned_word: {bad_word}"
            if not any(indicator in title_lower for indicator in cfg.pc_indicators):
                return False, f"banned_word_without_pc_indicator: {bad_word}"

    return True, "valid_pc"


# ===========================================================================
# 5. ORCHESTRATOR
# ===========================================================================
class OlxPcParser:
    """Головний парсер готових ПК з OLX."""

    def __init__(
        self,
        env: EnvConfig,
        cfg: PcParserConfig,
        metrics: MetricsCollector,
        trace: TracingContext,
        repo: PcAdsRepository,
        stats_repo: StatsRepository,
        rate_limiter: Any = None,
    ) -> None:
        self._env = env
        self._cfg = cfg
        self._metrics = metrics
        self._trace = trace
        self._repo = repo
        self._stats = stats_repo
        self._rate_limiter = rate_limiter
        self._logger = _get_logger(__name__, trace)
        self._seen_urls: set[str] = set()
        self._today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    async def parse_all(self, shutdown_event: asyncio.Event | None = None) -> list[ParsedPc]:
        self._logger.info("pc_parser_started")
        t_start = time.monotonic()

        self._seen_urls = await self._repo.fetch_seen_urls()
        await self._metrics.inc("parser_seen_urls", len(self._seen_urls))

        proxy_kwargs = {}
        if self._env.olx_proxy_url:
            proxy_kwargs["proxies"] = {
                "http": self._env.olx_proxy_url,
                "https": self._env.olx_proxy_url,
            }

        all_pcs: list[ParsedPc] = []
        total_duplicates = 0
        total_net_errors = 0
        total_parse_errors = 0

        async with AsyncSession(
            headers=self._cfg.headers,
            impersonate=self._env.impersonate_browser,  # type: ignore[arg-type]
            **proxy_kwargs,
        ) as session:
            self._logger.info("session_warmed_up")
            try:
                await session.get("https://www.olx.ua/", timeout=self._env.request_timeout)
                await asyncio.sleep(0.5)
            except Exception:
                pass

            for page in range(self._env.pages_to_parse):
                if shutdown_event and shutdown_event.is_set():
                    self._logger.info("shutdown_requested_skip_page: %s", page)
                    break

                offset = page * 40
                self._logger.info("page_start: page=%s/%s offset=%s", page + 1, self._env.pages_to_parse, offset)

                t0 = time.monotonic()
                items, dups, net_err, parse_err = await self._fetch_page(session, offset)
                await self._metrics.time("olx_fetch_page", time.monotonic() - t0)
                await self._metrics.inc("olx_fetch_page_count")

                all_pcs.extend(items)
                total_duplicates += dups
                total_net_errors += net_err
                total_parse_errors += parse_err

                if self._env.pages_to_parse > 1 and page < self._env.pages_to_parse - 1:
                    await asyncio.sleep(1.5)

        elapsed = time.monotonic() - t_start
        await self._metrics.time("parser_total", elapsed)
        self._logger.info(
            "pc_parser_finished: parsed=%s unique=%s dups=%s net_err=%s parse_err=%s duration_sec=%.2f",
            len(all_pcs), len({p.url for p in all_pcs}), total_duplicates, total_net_errors, total_parse_errors, elapsed,
        )
        return all_pcs

    async def _fetch_page(
        self,
        session: AsyncSession,
        offset: int,
        limit: int = 40,
    ) -> tuple[list[ParsedPc], int, int, int]:
        payload = {
            "query": self._cfg.graphql_query,
            "variables": {
                "searchParameters": [
                    {"key": "category_id", "value": self._cfg.category_id},
                    {"key": "limit", "value": str(limit)},
                    {"key": "sort_by", "value": "created_at:desc"},
                    {"key": "offset", "value": str(offset)},
                ]
            },
        }

        new_items: list[ParsedPc] = []
        duplicates = 0
        net_errors = 0
        parse_errors = 0

        for attempt in range(1, self._env.max_retries + 1):
            try:
                if self._rate_limiter:
                    await self._rate_limiter.acquire()

                resp = await session.post(
                    "https://www.olx.ua/apigateway/graphql",
                    json=payload,
                    timeout=self._env.request_timeout,
                )

                if self._rate_limiter:
                    await self._rate_limiter.report_result(resp.status_code)

                if resp.status_code in (401, 403):
                    self._logger.warning("olx_403: attempt=%s", attempt)
                    net_errors += 1
                    try:
                        await session.get("https://www.olx.ua/uk/elektronika/", timeout=10)
                    except Exception:
                        pass
                    await asyncio.sleep(10)
                    continue

                if resp.status_code != 200:
                    self._logger.warning("olx_http_error: status=%s attempt=%s", resp.status_code, attempt)
                    net_errors += 1
                    await asyncio.sleep(attempt * 3)
                    continue

                data = resp.json()
                listings = data.get("data", {}).get("clientCompatibleListings", {}).get("data", [])
                await self._metrics.inc("olx_listings_received", len(listings))

                for item in listings:
                    pc = self._try_parse_item(item)
                    if pc:
                        new_items.append(pc)
                    elif pc is None and item.get("url"):
                        pass

                return new_items, duplicates, net_errors, parse_errors

            except Exception as exc:
                net_errors += 1
                self._logger.warning("olx_network_error: attempt=%s error=%s", attempt, str(exc))
                await asyncio.sleep(attempt * 2)

        self._logger.error("fetch_page_failed_after_retries: max_retries=%s", self._env.max_retries)
        return new_items, duplicates, net_errors, parse_errors

    def _try_parse_item(self, item: dict) -> ParsedPc | None:
        try:
            raw_id = item.get("id")
            ad_id = int(raw_id) if raw_id and str(raw_id).isdigit() else None

            raw_url = item.get("url", "")
            if not raw_url:
                return None
            if not raw_url.startswith("http"):
                raw_url = "https://www.olx.ua" + raw_url
            advert_url = clean_url(raw_url)

            if advert_url in self._seen_urls:
                self._logger.debug("duplicate_skipped: url=%s", advert_url)
                return None

            title = str(item.get("title") or "").replace("'", "").strip()
            is_pc, reason = is_real_pc(title, self._cfg)
            if not is_pc:
                self._logger.info("filtered_not_pc: reason=%s title=%s...", reason, title[:40])
                return None

            description = str(item.get("description") or "").strip().replace("<br />", "").replace("<br>", "")

            price = 0
            for param in item.get("params", []) or []:
                if param.get("key") == "price":
                    price = extract_price(param.get("value", {}).get("value", 0))
                    break

            loc = item.get("location") or {}
            city = (loc.get("city") or {}).get("name", "Невідомо") if loc.get("city") else "Невідомо"

            created_raw = str(item.get("created_time") or "")
            created_at = created_raw.split("T")[0] if "T" in created_raw else "Невідомо"
            last_refresh = str(item.get("last_refresh_time") or "Невідомо")

            photos = item.get("photos", []) or []
            formatted = [
                p.get("link", "").replace("{width}", "1000").replace("{height}", "750")
                for p in photos if p and p.get("link")
            ]

            user = item.get("user") or {}
            seller_id = str(user.get("id")) if user.get("id") else None
            seller_uuid = str(user.get("uuid")) if user.get("uuid") else None
            user_created = str(user.get("created") or "")
            seller_created = user_created.split("-")[0] if user_created else None

            is_business = item.get("business", False)

            pc = ParsedPc(
                ad_id=ad_id,
                url=advert_url,
                parsed_date=self._today,
                status="active",
                title=title,
                description=description,
                price=price,
                item_type="pc",
                component_name=None,
                city=city,
                created_at_olx=created_at,
                last_refresh_time=last_refresh,
                photo_url=formatted[0] if formatted else "Невідомо",
                photos=",".join(formatted[1:]) if len(formatted) > 1 else None,
                all_photos=",".join(formatted) if formatted else None,
                seller_id=seller_id,
                seller_uuid=seller_uuid,
                seller_name=user.get("name") or "Невідомо",
                seller_created_at=seller_created,
                seller_type="shop" if is_business else "private_person",
                seller_price_clean=price,
            )

            self._seen_urls.add(advert_url)
            self._logger.info("pc_parsed: ad_id=%s price=%s title=%s...", ad_id, price, title[:40])
            return pc

        except Exception as exc:
            self._logger.warning("parse_item_failed: error=%s", str(exc))
            return None

    async def trigger_websocket(self, pcs: list[ParsedPc]) -> bool:
        """Надсилає тригер на WebSocket-сервер."""
        if not pcs:
            return False

        try:
            async with aiohttp.ClientSession() as session:
                await session.post(
                    self._env.websocket_trigger_url,
                    json=[p.model_dump(exclude_none=True) for p in pcs],
                    timeout=5,
                )
            self._logger.info("websocket_triggered: count=%s", len(pcs))
            return True
        except Exception as exc:
            self._logger.warning("websocket_trigger_failed: %s", str(exc))
            return False


# ===========================================================================
# 6. FACTORY
# ===========================================================================
def _validate_env() -> EnvConfig:
    env_path = Path(".env")
    if not env_path.exists():
        env_path = Path(__file__).resolve().parent / ".env"
    load_dotenv(env_path)

    cfg = EnvConfig(
        supabase_url=os.getenv("SUPABASE_URL", "").strip(),
        supabase_secret_key=os.getenv("SUPABASE_SECRET_KEY", "").strip(),
        olx_proxy_url=(os.getenv("OLX_PROXY_URL") or "").strip(),
        stats_file=STATS_FILE,
    )

    if not cfg.supabase_url:
        raise RuntimeError("❌ SUPABASE_URL не знайдено у .env")
    if not cfg.supabase_secret_key:
        raise RuntimeError("❌ SUPABASE_SECRET_KEY не знайдено у .env")

    return cfg


async def create_pc_parser_from_env(
    shutdown_event: asyncio.Event | None = None,
    pages_to_parse: int | None = None,
    rate_limiter: Any = None,
) -> tuple[OlxPcParser, MetricsCollector]:
    env = _validate_env()
    if pages_to_parse is not None:
        env = env.model_copy(update={"pages_to_parse": pages_to_parse})

    trace = TracingContext()
    metrics = MetricsCollector()
    logger = _get_logger("factory", trace)
    logger.info("dependencies_created")

    supabase_client: Client = create_client(env.supabase_url, env.supabase_secret_key)
    repo = SupabasePcAdsRepository(supabase_client, metrics, trace)
    stats_repo = JsonStatsRepository(env.stats_file, trace)
    cfg = PcParserConfig()

    parser = OlxPcParser(
        env=env,
        cfg=cfg,
        metrics=metrics,
        trace=trace,
        repo=repo,
        stats_repo=stats_repo,
        rate_limiter=rate_limiter,
    )
    return parser, metrics


# ===========================================================================
# 7. ENTRY POINT
# ===========================================================================
async def main_async(
    pages_to_parse: int | None = None,
    db_lock: Any = None,
    rate_limiter: Any = None,
) -> None:
    logger = _get_logger("main")
    logger.info("pc_parser_system_start")

    shutdown_event = asyncio.Event()

    def _signal_handler(sig: int) -> None:
        logger.info("shutdown_signal_received: signal=%s", signal.Signals(sig).name)
        shutdown_event.set()

    if sys.platform != "win32":
        for sig in (signal.SIGTERM, signal.SIGINT):
            try:
                asyncio.get_running_loop().add_signal_handler(sig, _signal_handler, sig)
            except NotImplementedError:
                pass

    parser, metrics = await create_pc_parser_from_env(
        shutdown_event=shutdown_event,
        pages_to_parse=pages_to_parse,
        rate_limiter=rate_limiter,
    )

    try:
        pcs = await parser.parse_all(shutdown_event=shutdown_event)

        if pcs:
            upserted = await parser._repo.upsert_pcs(pcs)
            await parser.trigger_websocket(pcs)

            avg_time = round((metrics.snapshot()["timers"].get("parser_total", {}).get("avg_ms", 0) or 0) / max(len(pcs), 1), 2)
            await parser._stats.update("parsing", {
                "parsed_total_new": len(pcs),
                "avg_parsing_time_ms": avg_time,
            })
            logger.info("final_stats: parsed=%s upserted=%s", len(pcs), upserted)
        else:
            logger.info("final_stats: no_new_pcs")
            await parser._stats.update("parsing", {"parsed_total_new": 0})

        logger.info("%s", PrettyMetrics.format(metrics.snapshot()))

    except Exception as exc:
        logger.error("fatal_error: %s", str(exc))
        raise


def main() -> None:
    try:
        asyncio.run(main_async())
    except KeyboardInterrupt:
        _get_logger("main").info("shutdown_by_user")


if __name__ == "__main__":
    main()
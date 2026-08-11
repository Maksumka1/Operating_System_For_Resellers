"""
OLX Hardware Parser — Production Ready
======================================
Асинхронний збір оголошень комплектуючих з OLX GraphQL API.

Архітектура:
  • DI + Repository Pattern
  • Pydantic-валідація env та доменних моделей
  • Metrics + Tracing + Structured Logging
  • Graceful shutdown
  • Без глобального стану
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
# Зовнішні залежності проєкту (Гарантований імпорт)
# ---------------------------------------------------------------------------
_project_root = Path(__file__).resolve().parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

try:
    from config import CHIPSET_TO_SOCKET, HARDWARE_TARGETS, LEGACY_PRE_SORTED_TARGETS, SOCKETS, STATS_FILE
    from hardware_matchers import (
        detect_bundle_components,
        extract_cpu,
        extract_gpu,
        extract_motherboard,
        extract_psu,
        extract_ram,
        extract_storage,
        normalize_title,
    )
except ImportError as e:
    logging.error(f"❌ [CRITICAL IMPORT ERROR in parser_hardware]: {e}")
    HARDWARE_TARGETS = getattr(sys.modules.get("config"), "HARDWARE_TARGETS", {})
    LEGACY_PRE_SORTED_TARGETS = getattr(sys.modules.get("config"), "LEGACY_PRE_SORTED_TARGETS", [])
    SOCKETS = getattr(sys.modules.get("config"), "SOCKETS", [])
    CHIPSET_TO_SOCKET = getattr(sys.modules.get("config"), "CHIPSET_TO_SOCKET", {})
    STATS_FILE = Path("stats.json")

    def normalize_title(t: str) -> str:
        return t.lower()

    def detect_bundle_components(t: str, ht: dict | None = None) -> dict | None:
        return None

    def extract_gpu(t: str) -> list[str]:
        return []

    def extract_cpu(t: str) -> list[str]:
        return []

    def extract_motherboard(t: str) -> list[str]:
        return []

    def extract_psu(t: str) -> list[str]:
        return []

    def extract_storage(t: str) -> list[str]:
        return []

    def extract_ram(t: str) -> list[str]:
        return []


# ===========================================================================
# 0. OBSERVABILITY — Logging, Metrics, Tracing
# ===========================================================================
class TraceIdFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        if not hasattr(record, "trace_id"):
            record.trace_id = "system"
        return True


_handler = logging.StreamHandler()
_handler.addFilter(TraceIdFilter())

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s trace=%(trace_id)s — %(message)s",
    datefmt="%H:%M:%S",
    handlers=[_handler],
)


class TracingContext:
    def __init__(self) -> None:
        self.trace_id = hashlib.sha256(
            f"{time.time()}{os.urandom(8)}".encode()
        ).hexdigest()[:16]


def _get_logger(name: str, trace: TracingContext | None = None) -> Any:
    extra = {"trace_id": trace.trace_id} if trace else {}
    if _HAS_STRUCTLOG:
        return structlog.get_logger(name, **extra)
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
    internal_secret_key: str = Field(default="")
    olx_proxy_url: str = Field(default="")
    request_timeout: int = Field(default=12, gt=0)
    max_retries: int = Field(default=3, ge=1, le=10)
    pages_to_parse: int = Field(default=1, ge=1, le=20)
    impersonate_browser: str = Field(default="chrome124")
    websocket_trigger_url: str = Field(default="http://localhost:8000/api/trigger-new-ad")

    @field_validator("supabase_url")
    @classmethod
    def _url_https(cls, v: str) -> str:
        if v and not v.startswith("https://"):
            raise ValueError("SUPABASE_URL має починатися з https://")
        return v.rstrip("/") if v else v


@dataclass(frozen=True)
class ParserConfig:
    """Конфігурація бізнес-логіки парсера."""

    subcategories: tuple[dict[str, str], ...] = (
        {"item_type": "gpu", "subcategory": "videokarty", "name": "Відеокарти"},
        {"item_type": "cpu", "subcategory": "protsessory", "name": "Процесори"},
        {"item_type": "motherboard", "subcategory": "materinskie-platy", "name": "Материнські плати"},
        {"item_type": "psu", "subcategory": "bloki-pitaniya", "name": "Блоки живлення"},
        {"item_type": "storage", "subcategory": "zhestkie-diski", "name": "Накопичувачі"},
        {"item_type": "ram", "subcategory": "moduli-pamyati", "name": "Оперативна пам'ять"},
    )
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
        "        id title url status created_time last_refresh_time description"
        "        location { city { name } }"
        "        photos { link }"
        "        user { id uuid name created }"
        "        params {"
        "          key name"
        "          value {"
        "            ... on PriceParam { value currency label }"
        "            ... on GenericParam { key label }"
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
class ParsedAd(BaseModel):
    """Одне розпізнане оголошення для збереження в БД."""

    ad_id: int | None = None
    url: str = Field(min_length=1)
    title: str = Field(min_length=1)
    description: str = ""
    price: int = Field(ge=0, le=1_000_000_000)
    item_type: str = Field(min_length=1)
    component_name: str = Field(min_length=1)
    socket: str | None = None
    has_defects: int = Field(default=0, ge=0, le=1)
    city: str = "Невідомо"
    created_at_olx: str = "Невідомо"
    photo_url: str = "Невідомо"
    all_photos: str | None = None
    parsed_date: str = Field(min_length=1)
    status: str = "active"
    seller_id: str | None = None
    seller_uuid: str | None = None
    seller_name: str = "Невідомо"
    seller_created_at: str | None = None
    seller_type: str = "private_person"
    seller_price_clean: int = Field(default=0, ge=0)
    bundle_components: dict[str, str | None] | None = None


# ===========================================================================
# 3. REPOSITORY PATTERN
# ===========================================================================
class AdsRepository(ABC):
    @abstractmethod
    async def fetch_seen_urls(self) -> set[str]:
        ...

    @abstractmethod
    async def upsert_ads(self, ads: list[ParsedAd]) -> int:
        ...


class SupabaseAdsRepository(AdsRepository):
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

    async def upsert_ads(self, ads: list[ParsedAd]) -> int:
        if not ads:
            return 0

        dicts = [a.model_dump(exclude_none=True) for a in ads]

        def _upsert() -> None:
            self._client.table("ads").upsert(dicts, on_conflict="ad_id").execute()

        try:
            t0 = time.monotonic()
            await asyncio.to_thread(_upsert)
            duration = time.monotonic() - t0
            await self._metrics.time("db_upsert_ads", duration)
            await self._metrics.inc("db_upsert_ads_count", len(ads))
            self._logger.info("ads_upserted: count=%s", len(ads))
            return len(ads)
        except Exception as exc:
            self._logger.error("ads_upsert_failed: %s", str(exc))
            await self._metrics.inc("db_upsert_ads_failures")
            return 0


# ===========================================================================
# 4. PURE FUNCTIONS
# ===========================================================================
BROKEN_PATTERN = re.compile(
    r"неробоч|не робоч|запчастин|запчасть|запчасти|дефект|відновлен|восстановлен|"
    r"артефакт|поломан|неисправн|не справн|на детал|запчасті|прогрів|не стартует|"
    r"не включа|не включається|не включается|не працює|не работает|не робочий|"
    r"на\s+запчаст\w*|под\s+восстановление|під\s+відновлення|под\s+ремонт|під\s+ремонт|"
    r"непрацю\w*|\bремонт\w*",
    re.IGNORECASE,
)

CLEAN_PATTERNS = re.compile(
    r"(?:"
    r"без\s+(?:будь-яких\s+|будь\s+яких\s+)?(?:проблем|дефект\w*|артефакт\w*|ремонт\w*|нюанс\w*)|"
    r"без\s+майнинга\s+и\s+ремонтов|"
    r"не\s+(?:був|были?|было)\s+в\s+ремонт\w*|"
    r"в\s+ремонт\w*\s+не\s+(?:був|был)|"
    r"не\s+ремонтував\w*|не\s+ремонтировал\w*|не\s+вскрывался\w*|не\s+розбирався|"
    r"дефект\w*\s+(?:не|нет)\s+\w*|"
    r"без\s+физических\s+повреждений"
    r")",
    re.IGNORECASE,
)

COMPARISON_PATTERN = re.compile(
    r"(?:сильніше\s+за|мощнее\s+чем|быстрее\s+чем|аналог|замість|вмісто|вместо|похожа\s+на|як|как|рівень|уровень|мощнее|быстрее|сильнее)\s+[a-z0-9\s_-]+|\(.*?\)",
    re.IGNORECASE,
)

MULTILOT_PATTERN = re.compile(r"\d+\s*(?:gb|гб)\s*,\s*\d+\s*(?:gb|гб)", re.IGNORECASE)


def is_broken_ad(text: str) -> bool:
    if not text:
        return False
    clean_text = CLEAN_PATTERNS.sub("", text)
    return bool(BROKEN_PATTERN.search(clean_text))


def clean_url(url: str) -> str:
    parsed = urlparse(url)
    return f"{parsed.scheme}://{parsed.netloc}{parsed.path}"


def detect_socket(
    title: str,
    description: str,
    component_name: str,
    sockets: list[str] | None = None,
    chipset_map: dict[str, str] | None = None,
) -> str | None:
    sockets = sockets or SOCKETS
    chipset_map = chipset_map or CHIPSET_TO_SOCKET

    full_text = f"{title} {description}".lower()
    for sock in sockets:
        pattern = r"(?<![a-z0-9])" + re.escape(sock.lower().replace("-", " ")) + r"(?![a-z0-9])"
        if re.search(pattern, full_text.replace("-", " ")):
            return sock.replace("socket", "lga").lower()
    mb_key = component_name.lower().replace("_", "")
    return chipset_map.get(mb_key)


def match_ad_to_hardware_target(title: str, target_items_for_type: dict | None = None) -> tuple[str, dict] | None:
    if not title or not HARDWARE_TARGETS:
        return None

    title_clean = normalize_title(title)
    if MULTILOT_PATTERN.search(title_clean):
        return None

    title_for_match = COMPARISON_PATTERN.sub("", title_clean)

    bundle_data = detect_bundle_components(title_for_match, HARDWARE_TARGETS)
    if bundle_data:
        return bundle_data["bundle_key"], {
            "item_type": "bundle",
            "subcategory": "komplektuyushchie-set",
            "components": bundle_data["components"],
        }

    if "x99" in title_for_match and "x99" in HARDWARE_TARGETS:
        return "x99", HARDWARE_TARGETS["x99"]

    for cand in extract_gpu(title_for_match):
        if cand in HARDWARE_TARGETS:
            return cand, HARDWARE_TARGETS[cand]
    for cand in extract_cpu(title_for_match):
        if cand in HARDWARE_TARGETS:
            return cand, HARDWARE_TARGETS[cand]
    for cand in extract_motherboard(title_for_match):
        if cand in HARDWARE_TARGETS:
            return cand, HARDWARE_TARGETS[cand]
    for cand in extract_psu(title_for_match):
        if cand in HARDWARE_TARGETS:
            return cand, HARDWARE_TARGETS[cand]
    for cand in extract_storage(title_for_match):
        if cand in HARDWARE_TARGETS:
            return cand, HARDWARE_TARGETS[cand]
    for cand in extract_ram(title_for_match):
        if cand in HARDWARE_TARGETS:
            return cand, HARDWARE_TARGETS[cand]

    targets_to_check = (
        LEGACY_PRE_SORTED_TARGETS
        if target_items_for_type is None or not target_items_for_type
        else sorted(target_items_for_type.items(), key=lambda x: len(x[0]), reverse=True)
    )

    for target_name, cfg in targets_to_check:
        compiled_patt = cfg.get("compiled_pattern")
        if cfg.get("item_type") == "storage":
            parts = target_name.split("_")
            if len(parts) < 2:
                continue
            st_type, capacity_raw = parts[0], parts[1]
            cap_num = re.sub(r"\D", "", capacity_raw)
            cap_unit = "tb" if "tb" in capacity_raw else "gb"

            has_type = False
            if st_type == "ssd":
                has_type = any(w in title_for_match for w in ["ssd", "ссд", "nvme", "m.2", "m2"])
            elif st_type == "hdd":
                has_type = any(w in title_for_match for w in [
                    "hdd", "хдд", "жорстк", "жестк", "винчестер", "toshiba",
                    "barracuda", "hitachi", "seagate", "ironwolf",
                ])
            if not has_type:
                continue

            pattern = (
                r"(?<![a-z0-9])(1\s*(tb|тб|терабайт)|(1000|1024)\s*(gb|гб|гігабайт|гигабайт))(?![a-z0-9])"
                if capacity_raw == "1tb"
                else r"(?<![a-z0-9])" + cap_num + r"\s*(" + cap_unit + r"|тб|терабайт|гб|гігабайт)(?![a-z0-9])"
            )
            if re.search(pattern, title_for_match):
                return target_name, cfg
        else:
            if compiled_patt and bool(compiled_patt.search(title_for_match)):
                return target_name, cfg

    return None


# ===========================================================================
# 5. ORCHESTRATOR — OLX GraphQL Parser
# ===========================================================================
class OlxGraphqlParser:
    """Головний парсер комплектуючих."""

    def __init__(
        self,
        env: EnvConfig,
        parser_config: ParserConfig,
        metrics: MetricsCollector,
        trace: TracingContext,
        repo: AdsRepository,
        rate_limiter: Any = None,
    ) -> None:
        self._env = env
        self._cfg = parser_config
        self._metrics = metrics
        self._trace = trace
        self._repo = repo
        self._rate_limiter = rate_limiter
        self._logger = _get_logger(__name__, trace)
        self._seen_urls: set[str] = set()
        self._today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    async def parse_all(self, shutdown_event: asyncio.Event | None = None) -> list[ParsedAd]:
        self._logger.info("parser_started")
        t_start = time.monotonic()

        self._seen_urls = await self._repo.fetch_seen_urls()
        await self._metrics.inc("parser_seen_urls", len(self._seen_urls))

        hardware_items = {k: v for k, v in HARDWARE_TARGETS.items() if not k.startswith("pc_")}
        await self._metrics.inc("parser_target_models", len(hardware_items))

        if not hardware_items:
            self._logger.error("❌ [CRITICAL] HARDWARE_TARGETS порожній! Перевірте імпорти з config.py")

        proxy_kwargs = {}
        if self._env.olx_proxy_url:
            proxy_kwargs["proxies"] = {
                "http": self._env.olx_proxy_url,
                "https": self._env.olx_proxy_url,
            }

        all_results: list[ParsedAd] = []

        async with AsyncSession(
            headers=self._cfg.headers,
            impersonate=self._env.impersonate_browser,  # type: ignore[arg-type]
            **proxy_kwargs,
        ) as session:
            self._logger.info("session_warmed_up")
            try:
                await session.get("https://www.olx.ua/uk/elektronika/", timeout=10)
            except Exception:
                pass

            for subcat in self._cfg.subcategories:
                if shutdown_event and shutdown_event.is_set():
                    self._logger.info("shutdown_requested_skip_subcat: %s", subcat["name"])
                    break

                parsed = await self._parse_subcategory(session, subcat, hardware_items, shutdown_event)
                all_results.extend(parsed)

        elapsed = time.monotonic() - t_start
        await self._metrics.time("parser_total", elapsed)
        self._logger.info(
            "parser_finished: total=%s unique=%s duration_sec=%.2f",
            len(all_results),
            len({a.url for a in all_results}),
            elapsed,
        )
        return all_results

    async def _parse_subcategory(
        self,
        session: AsyncSession,
        subcat: dict[str, str],
        hardware_items: dict,
        shutdown_event: asyncio.Event | None,
    ) -> list[ParsedAd]:
        subcat_key = subcat["subcategory"]
        item_type = subcat["item_type"]
        cat_name = subcat["name"]
        self._logger.info("subcat_start: name=%s key=%s pages=%s", cat_name, subcat_key, self._env.pages_to_parse)

        targets_for_type = {k: v for k, v in hardware_items.items() if v.get("item_type") == item_type}
        results: list[ParsedAd] = []

        for page in range(self._env.pages_to_parse):
            if shutdown_event and shutdown_event.is_set():
                break

            t0 = time.monotonic()
            page_results = await self._fetch_page(session, subcat, targets_for_type, page)
            await self._metrics.time("olx_fetch_page", time.monotonic() - t0)
            await self._metrics.inc("olx_fetch_page_count")
            await self._metrics.inc(f"olx_parsed_{item_type}", len(page_results))

            results.extend(page_results)

            if self._env.pages_to_parse > 1 and page < self._env.pages_to_parse - 1:
                await asyncio.sleep(1.0)

        self._logger.info("subcat_done: name=%s parsed=%s", cat_name, len(results))
        return results

    async def _fetch_page(
        self,
        session: AsyncSession,
        subcat: dict[str, str],
        targets_for_type: dict,
        page: int,
    ) -> list[ParsedAd]:
        subcat_key = subcat["subcategory"]
        item_type = subcat["item_type"]
        limit = 40
        offset = page * limit

        search_params = [
            {"key": "category_id", "value": "458"},
            {"key": "filter_enum_subcategory[0]", "value": subcat_key},
            {"key": "currency", "value": "UAH"},
            {"key": "sort_by", "value": "created_at:desc"},
            {"key": "limit", "value": str(limit)},
            {"key": "offset", "value": str(offset)},
        ]
        payload = {"query": self._cfg.graphql_query, "variables": {"searchParameters": search_params}}

        listings: list[dict] = []
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
                    self._logger.warning("olx_403: subcat=%s attempt=%s", subcat_key, attempt)
                    await asyncio.sleep(10)
                    continue

                if resp.status_code != 200:
                    self._logger.warning("olx_http_error: status=%s subcat=%s", resp.status_code, subcat_key)
                    await asyncio.sleep(2)
                    continue

                data = resp.json()
                listings = data.get("data", {}).get("clientCompatibleListings", {}).get("data", [])
                break
            except Exception as exc:
                self._logger.warning("olx_network_error: subcat=%s attempt=%s error=%s", subcat_key, attempt, str(exc))
                await asyncio.sleep(2)
                if attempt == self._env.max_retries:
                    return []

        await self._metrics.inc("olx_listings_received", len(listings))

        parsed_page: list[ParsedAd] = []
        stats = {
            "received": len(listings),
            "skipped_duplicate": 0,
            "skipped_subcat_mismatch": 0,
            "skipped_no_target_match": 0,
            "parse_errors": 0,
        }

        for item in listings:
            ad, reason = self._try_parse_item_with_reason(item, subcat_key, item_type, targets_for_type)
            if ad:
                parsed_page.append(ad)
            else:
                if reason in stats:
                    stats[reason] += 1

        self._logger.info(
            "page_parse_stats: subcat=%s page=%s | received=%s parsed=%s (dups=%s, subcat_mismatch=%s, no_target_match=%s, errs=%s)",
            subcat_key,
            page + 1,
            stats["received"],
            len(parsed_page),
            stats["skipped_duplicate"],
            stats["skipped_subcat_mismatch"],
            stats["skipped_no_target_match"],
            stats["parse_errors"],
        )

        return parsed_page

    def _try_parse_item_with_reason(
        self,
        item: dict,
        subcat_key: str,
        item_type: str,
        targets_for_type: dict,
    ) -> tuple[ParsedAd | None, str]:
        try:
            ad_subcat = None
            for param in item.get("params", []) or []:
                if param.get("key") == "subcategory":
                    ad_subcat = (param.get("value") or {}).get("key")
                    break

            if ad_subcat and ad_subcat != subcat_key and ad_subcat not in (subcat_key, "komplektuyushchie-set"):
                return None, "skipped_subcat_mismatch"

            title = str(item.get("title") or "Без назви").replace("'", "").strip()
            raw_url = item.get("url", "")
            if not raw_url:
                return None, "parse_errors"
            if not raw_url.startswith("http"):
                raw_url = "https://www.olx.ua" + raw_url
            advert_url = clean_url(raw_url)

            if advert_url in self._seen_urls:
                return None, "skipped_duplicate"

            matched = match_ad_to_hardware_target(title, targets_for_type)
            if not matched:
                return None, "skipped_no_target_match"

            target_name, cfg = matched
            description = str(item.get("description") or "").replace("<br />", " ")
            full_text = f"{title} {description}"
            has_defects = 1 if is_broken_ad(full_text) else 0

            price = 0
            for param in item.get("params", []) or []:
                if param.get("key") == "price":
                    val = param.get("value", {}).get("value", 0)
                    if isinstance(val, (int, float)) and val <= 1_000_000_000:
                        price = int(val)
                    break

            loc = item.get("location") or {}
            city = (loc.get("city") or {}).get("name", "Невідомо") if loc.get("city") else "Невідомо"
            created_raw = str(item.get("created_time") or "")
            ad_date = created_raw if created_raw else "Невідомо"

            photos = item.get("photos", []) or []
            photo_urls = []
            for p in photos:
                if p and isinstance(p, dict) and p.get("link"):
                    clean_link = p.get("link", "").replace("{width}", "1000").replace("{height}", "750")
                    if clean_link.startswith("//"):
                        clean_link = "https:" + clean_link
                    elif not clean_link.startswith("http"):
                        clean_link = "https://www.olx.ua" + clean_link
                    photo_urls.append(clean_link)

            user = item.get("user") or {}
            seller_id = str(user.get("id")) if user.get("id") else None
            seller_uuid = str(user.get("uuid")) if user.get("uuid") else None
            user_created = str(user.get("created") or "")
            seller_created = user_created.split("-")[0] if "-" in user_created else None

            detected_socket = None
            if item_type in ("motherboard", "cpu"):
                detected_socket = detect_socket(title, description, target_name)

            bundle_components = cfg.get("components") if item_type == "bundle" or target_name.startswith("bundle_") else None
            raw_ad_id = item.get("id")
            ad_id = int(raw_ad_id) if raw_ad_id and str(raw_ad_id).isdigit() else None

            ad = ParsedAd(
                ad_id=ad_id,
                url=advert_url,
                title=title,
                description=description,
                price=price,
                item_type=cfg.get("item_type", item_type),
                component_name=target_name,
                socket=detected_socket,
                has_defects=has_defects,
                city=city,
                created_at_olx=ad_date,
                photo_url=photo_urls[0] if photo_urls else "Невідомо",
                all_photos=",".join(photo_urls) if photo_urls else None,
                parsed_date=self._today,
                status="active",
                seller_id=seller_id,
                seller_uuid=seller_uuid,
                seller_name=user.get("name") or "Невідомо",
                seller_created_at=seller_created,
                seller_type="shop" if item.get("business", False) else "private_person",
                seller_price_clean=price,
                bundle_components=bundle_components,
            )

            self._seen_urls.add(advert_url)
            self._logger.info("ad_parsed: component=%s price=%s title=%s...", target_name, price, title[:40])
            return ad, "ok"

        except Exception as exc:
            self._logger.warning("parse_item_failed: error=%s", str(exc))
            return None, "parse_errors"

    async def trigger_websocket(self, ads: list[ParsedAd]) -> bool:
        if not ads:
            return False

        try:
            secret_key = self._env.internal_secret_key
            headers = {"X-Internal-Secret": secret_key} if secret_key else {}

            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self._env.websocket_trigger_url,
                    json=[a.model_dump(exclude_none=True) for a in ads],
                    headers=headers,
                    timeout=5,
                ) as resp:
                    if resp.status == 200:
                        self._logger.info("websocket_triggered: count=%s", len(ads))
                        return True
                    else:
                        self._logger.warning("websocket_trigger_failed: status=%s", resp.status)
                        return False
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
        internal_secret_key=os.getenv("INTERNAL_SECRET_KEY", "").strip(),
        olx_proxy_url=(os.getenv("OLX_PROXY_URL") or "").strip(),
    )

    if not cfg.supabase_url:
        raise RuntimeError("❌ SUPABASE_URL не знайдено у .env")
    if not cfg.supabase_secret_key:
        raise RuntimeError("❌ SUPABASE_SECRET_KEY не знайдено у .env")

    return cfg


async def create_parser_from_env(
    shutdown_event: asyncio.Event | None = None,
    pages_to_parse: int | None = None,
    rate_limiter: Any = None,
) -> tuple[OlxGraphqlParser, MetricsCollector]:
    env = _validate_env()
    if pages_to_parse is not None:
        env = env.model_copy(update={"pages_to_parse": pages_to_parse})

    trace = TracingContext()
    metrics = MetricsCollector()
    logger = _get_logger("factory", trace)
    logger.info("dependencies_created")

    supabase_client: Client = create_client(env.supabase_url, env.supabase_secret_key)
    repo = SupabaseAdsRepository(supabase_client, metrics, trace)
    parser_config = ParserConfig()

    parser = OlxGraphqlParser(
        env=env,
        parser_config=parser_config,
        metrics=metrics,
        trace=trace,
        repo=repo,
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
    logger.info("parser_system_start")

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

    parser, metrics = await create_parser_from_env(
        shutdown_event=shutdown_event,
        pages_to_parse=pages_to_parse,
        rate_limiter=rate_limiter,
    )

    try:
        ads = await parser.parse_all(shutdown_event=shutdown_event)

        if ads:
            upserted = await parser._repo.upsert_ads(ads)
            await parser.trigger_websocket(ads)
            logger.info("final_stats: parsed=%s upserted=%s", len(ads), upserted)
        else:
            logger.info("final_stats: no_new_ads")

        logger.info("metrics_snapshot: %s", metrics.snapshot())

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
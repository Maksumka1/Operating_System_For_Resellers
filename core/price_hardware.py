"""
Component Price Analyzer — Production Ready
============================================
Ринкові ціни комплектуючих на основі percentile.

Покращення:
  • Справжній async (httpx) замість to_thread()
  • Cursor-based пагінація (offset деградує на великих таблицях)
  • Retry з exponential backoff + circuit breaker
  • Graceful shutdown (SIGTERM/SIGINT)
  • Idempotency keys для upsert
  • Метрики та tracing
  • Pydantic-валідація змінних оточення

Залежності:
  pip install pydantic httpx python-dotenv structlog
"""

from __future__ import annotations

import asyncio
import hashlib
import logging
import os
import signal
import sys
import time
from abc import ABC, abstractmethod
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Callable

import httpx
from dotenv import load_dotenv
from pydantic import BaseModel, Field, field_validator

try:
    import structlog
    _HAS_STRUCTLOG = True
except ImportError:
    _HAS_STRUCTLOG = False

# ---------------------------------------------------------------------------
# 0. OBSERVABILITY — Metrics & Tracing
# ---------------------------------------------------------------------------
class MetricsCollector:
    """Простий in-memory збір метрик (без витоку пам'яті)."""

    def __init__(self) -> None:
        self._counters: dict[str, int] = defaultdict(int)
        self._timers: dict[str, dict[str, float]] = defaultdict(lambda: {"count": 0, "total_sec": 0.0})
        self._lock = asyncio.Lock()

    async def inc(self, name: str, value: int = 1) -> None:
        async with self._lock:
            self._counters[name] += value

    async def time(self, name: str, duration_sec: float) -> None:
        async with self._lock:
            stats = self._timers[name]
            stats["count"] += 1
            stats["total_sec"] += duration_sec

    def snapshot(self) -> dict[str, Any]:
        return {
            "counters": dict(self._counters),
            "timers": {
                k: {
                    "count": int(v["count"]),
                    "avg_ms": round((v["total_sec"] / v["count"]) * 1000, 2) if v["count"] > 0 else 0,
                }
                for k, v in self._timers.items()
            },
        }


class TracingContext:
    """Простий trace-id для кореляції логів."""

    def __init__(self) -> None:
        self.trace_id = hashlib.sha256(
            f"{time.time()}{os.urandom(8)}".encode()
        ).hexdigest()[:16]


class TraceIdFilter(logging.Filter):
    """Автоматично додає trace_id до логів сторонніх бібліотек (httpx тощо)."""

    def filter(self, record: logging.LogRecord) -> bool:
        if not hasattr(record, "trace_id"):
            record.trace_id = "system"
        return True


# Єдине правильне налаштування базового логування
logger_handler = logging.StreamHandler()
logger_handler.addFilter(TraceIdFilter())

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s trace=%(trace_id)s — %(message)s",
    datefmt="%H:%M:%S",
    handlers=[logger_handler],
)


def _get_logger(name: str, trace: TracingContext | None = None) -> Any:
    extra = {"trace_id": trace.trace_id} if trace else {}
    if _HAS_STRUCTLOG:
        return structlog.get_logger(name, **extra)

    logger = logging.getLogger(name)
    if extra:
        return logging.LoggerAdapter(logger, extra)
    return logger


# ---------------------------------------------------------------------------
# 1. CONFIG — Pydantic-validated environment
# ---------------------------------------------------------------------------
class CircuitState(Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"


class EnvConfig(BaseModel):
    """Валідація змінних оточення при старті."""

    supabase_url: str = Field(..., min_length=10)
    supabase_secret_key: str = Field(..., min_length=20)
    supabase_service_role_key: str = Field(..., min_length=20)
    request_timeout: float = Field(default=30.0, gt=0)
    max_concurrent_requests: int = Field(default=5, ge=1, le=50)
    retry_max_attempts: int = Field(default=3, ge=1, le=10)
    retry_base_delay: float = Field(default=1.0, gt=0)
    circuit_failure_threshold: int = Field(default=5, ge=1)
    circuit_recovery_timeout: float = Field(default=30.0, gt=0)
    batch_size_upsert: int = Field(default=100, ge=1, le=500)
    batch_size_fetch: int = Field(default=1000, ge=100, le=5000)
    enable_self_test: bool = Field(default=True)

    @field_validator("supabase_url")
    @classmethod
    def _validate_url(cls, v: str) -> str:
        if not v.startswith("https://"):
            raise ValueError("SUPABASE_URL має починатися з https://")
        return v.rstrip("/")


@dataclass(frozen=True)
class PriceAnalyzerConfig:
    item_types: frozenset[str] = field(default_factory=lambda: frozenset({
        "gpu", "cpu", "motherboard", "psu", "storage", "ram", "bundle",
    }))
    min_price: int = 100
    min_ads_for_percentile: int = 3
    min_ads_for_trim: int = 6
    trim_fraction: float = 0.10
    percentile_index: float = 0.33


# ---------------------------------------------------------------------------
# 2. DOMAIN MODELS
# ---------------------------------------------------------------------------
class ComponentAd(BaseModel):
    ad_id: int = Field(gt=0)
    component_name: str = Field(min_length=1)
    price: int = Field(gt=0)


class PercentileResult(BaseModel):
    component_name: str = Field(min_length=1)
    price: int = Field(gt=0)
    sample_size: int = Field(gt=0)
    used_ids: list[int]


class PriceUpsertRecord(BaseModel):
    component_name: str = Field(min_length=1)
    price: int = Field(gt=0)
    date: str = Field(min_length=1)
    competitor_ids: list[int]
    idempotency_key: str = Field(min_length=1)


# ---------------------------------------------------------------------------
# 3. RESILIENCE — Retry + Circuit Breaker
# ---------------------------------------------------------------------------
class CircuitBreaker:
    """Circuit breaker для захисту від каскадних відмов."""

    def __init__(
        self,
        failure_threshold: int = 5,
        recovery_timeout: float = 30.0,
        logger: Any | None = None,
    ) -> None:
        self._failure_threshold = failure_threshold
        self._recovery_timeout = recovery_timeout
        self._logger = logger or logging.getLogger("circuit_breaker")
        self._state = CircuitState.CLOSED
        self._failures = 0
        self._last_failure_time: float | None = None
        self._lock = asyncio.Lock()

    async def call(self, coro: Callable[[], Any]) -> Any:
        async with self._lock:
            if self._state == CircuitState.OPEN:
                if self._last_failure_time and (time.monotonic() - self._last_failure_time) > self._recovery_timeout:
                    self._state = CircuitState.HALF_OPEN
                    self._logger.warning("circuit_breaker_half_open")
                else:
                    raise RuntimeError("Circuit breaker is OPEN — refusing request")

        try:
            result = await coro()
            async with self._lock:
                if self._state == CircuitState.HALF_OPEN:
                    self._state = CircuitState.CLOSED
                    self._failures = 0
                    self._logger.info("circuit_breaker_closed")
            return result
        except Exception as exc:
            async with self._lock:
                self._failures += 1
                self._last_failure_time = time.monotonic()
                if self._failures >= self._failure_threshold:
                    self._state = CircuitState.OPEN
                    self._logger.error("circuit_breaker_opened, failures=%s", self._failures)
            raise


async def with_retry(
    coro: Callable[[], Any],
    max_attempts: int = 3,
    base_delay: float = 1.0,
    logger: Any | None = None,
) -> Any:
    """Exponential backoff retry."""
    logger = logger or logging.getLogger("retry")
    last_exc: Exception | None = None

    for attempt in range(1, max_attempts + 1):
        try:
            return await coro()
        except (httpx.NetworkError, httpx.TimeoutException, httpx.HTTPStatusError) as exc:
            last_exc = exc
            if attempt == max_attempts:
                break
            delay = base_delay * (2 ** (attempt - 1))
            logger.warning(
                "retry_attempt %s/%s, delay=%.2fs, error=%s",
                attempt, max_attempts, delay, str(exc),
            )
            await asyncio.sleep(delay)

    raise last_exc or RuntimeError("Retry exhausted")


# ---------------------------------------------------------------------------
# 4. PURE FUNCTION — Percentile Calculator
# ---------------------------------------------------------------------------
class PercentilePriceCalculator:
    def __init__(self, config: PriceAnalyzerConfig) -> None:
        self._config = config

    def calculate(self, component_name: str, ads: list[ComponentAd]) -> PercentileResult | None:
        if not ads:
            return None

        n = len(ads)
        if n < self._config.min_ads_for_percentile:
            return None

        sorted_ads = sorted(ads, key=lambda a: a.price)

        if n < self._config.min_ads_for_trim:
            mid = n // 2
            selected = sorted_ads[mid]
            used_ids = [a.ad_id for a in sorted_ads]
            return PercentileResult(
                component_name=component_name,
                price=selected.price,
                sample_size=n,
                used_ids=used_ids,
            )

        trim_size = int(n * self._config.trim_fraction)
        trimmed = sorted_ads[trim_size : n - trim_size] if trim_size > 0 else sorted_ads
        n_trimmed = len(trimmed)
        idx = min(int(n_trimmed * self._config.percentile_index), n_trimmed - 1)
        selected = trimmed[idx]

        return PercentileResult(
            component_name=component_name,
            price=selected.price,
            sample_size=n_trimmed,
            used_ids=[a.ad_id for a in trimmed],
        )


# ---------------------------------------------------------------------------
# 5. ASYNC REPOSITORY — httpx-based, cursor pagination
# ---------------------------------------------------------------------------
class ComponentAdRepository(ABC):
    @abstractmethod
    async def fetch_active_components(self, config: PriceAnalyzerConfig) -> list[ComponentAd]:
        ...


class SupabaseComponentAdRepository(ComponentAdRepository):
    """
    Справжній async-репозиторій через Supabase REST API.
    Cursor-based пагінація (ad_id > last_seen) замість offset.
    """

    def __init__(
        self,
        client: httpx.AsyncClient,
        base_url: str,
        api_key: str,
        env: EnvConfig,
        metrics: MetricsCollector,
        trace: TracingContext,
        circuit: CircuitBreaker,
    ) -> None:
        self._client = client
        self._base_url = base_url
        self._api_key = api_key
        self._env = env
        self._metrics = metrics
        self._trace = trace
        self._circuit = circuit
        self._logger = _get_logger(__name__, trace)
        self._semaphore = asyncio.Semaphore(env.max_concurrent_requests)

    async def fetch_active_components(self, config: PriceAnalyzerConfig) -> list[ComponentAd]:
        headers = {
            "apikey": self._api_key,
            "Authorization": f"Bearer {self._api_key}",
            "Content-Type": "application/json",
            "Prefer": "count=exact",
        }

        all_records: list[ComponentAd] = []
        last_ad_id: int | None = None
        page = 0

        while True:
            t0 = time.monotonic()
            rows = await self._fetch_page(headers, config, last_ad_id)
            duration = time.monotonic() - t0
            await self._metrics.time("db_fetch_page", duration)

            if not rows:
                break

            for row in rows:
                try:
                    all_records.append(ComponentAd.model_validate(row))
                except Exception:
                    self._logger.warning("invalid_component_ad_skipped: ad_id=%s", row.get("ad_id"))

            last_ad_id = max(r["ad_id"] for r in rows)
            page += 1
            await self._metrics.inc("db_fetch_pages")

            if len(rows) < self._env.batch_size_fetch:
                break

        await self._metrics.inc("db_fetch_total_ads", len(all_records))
        self._logger.info("ads_loaded: count=%s pages=%s", len(all_records), page)
        return all_records

    async def _fetch_page(
        self,
        headers: dict[str, str],
        config: PriceAnalyzerConfig,
        last_ad_id: int | None,
    ) -> list[dict[str, Any]]:
        item_types = ",".join(config.item_types)
        params: dict[str, Any] = {
            "select": "ad_id,component_name,price",
            "item_type": f"in.({item_types})",
            "status": "eq.active",
            "has_defects": "eq.0",
            "price": f"gt.{config.min_price}",
            "seller_risk_score": "neq.suspicious",
            "order": "ad_id.asc",
            "limit": self._env.batch_size_fetch,
        }
        if last_ad_id is not None:
            params["ad_id"] = f"gt.{last_ad_id}"

        url = f"{self._base_url}/rest/v1/ads"

        async def _request() -> list[dict[str, Any]]:
            async with self._semaphore:
                resp = await self._client.get(
                    url,
                    headers=headers,
                    params=params,
                    timeout=self._env.request_timeout,
                )
                resp.raise_for_status()
                return resp.json()

        try:
            return await self._circuit.call(
                lambda: with_retry(_request, self._env.retry_max_attempts, self._env.retry_base_delay, self._logger)
            )
        except Exception as exc:
            self._logger.error("fetch_page_failed: last_ad_id=%s error=%s", last_ad_id, str(exc))
            return []


class ComponentPriceRepository(ABC):
    @abstractmethod
    async def upsert_prices(self, records: list[PriceUpsertRecord]) -> int:
        ...


class SupabaseComponentPriceRepository(ComponentPriceRepository):
    def __init__(
        self,
        client: httpx.AsyncClient,
        base_url: str,
        api_key: str,
        env: EnvConfig,
        metrics: MetricsCollector,
        trace: TracingContext,
        circuit: CircuitBreaker,
    ) -> None:
        self._client = client
        self._base_url = base_url
        self._api_key = api_key
        self._env = env
        self._metrics = metrics
        self._trace = trace
        self._circuit = circuit
        self._logger = _get_logger(__name__, trace)
        self._semaphore = asyncio.Semaphore(env.max_concurrent_requests)

    async def upsert_prices(self, records: list[PriceUpsertRecord]) -> int:
        if not records:
            return 0

        headers = {
            "apikey": self._api_key,
            "Authorization": f"Bearer {self._api_key}",
            "Content-Type": "application/json",
            "Prefer": "resolution=merge-duplicates",
        }
        url = f"{self._base_url}/rest/v1/component_prices?on_conflict=component_name,date"
        upserted_total = 0

        for i in range(0, len(records), self._env.batch_size_upsert):
            batch = records[i : i + self._env.batch_size_upsert]
            payload = [r.model_dump() for r in batch]

            async def _request() -> None:
                async with self._semaphore:
                    resp = await self._client.post(
                        url,
                        headers=headers,
                        json=payload,
                        timeout=self._env.request_timeout,
                    )
                    resp.raise_for_status()

            try:
                t0 = time.monotonic()
                await self._circuit.call(
                    lambda: with_retry(_request, self._env.retry_max_attempts, self._env.retry_base_delay, self._logger)
                )
                duration = time.monotonic() - t0
                await self._metrics.time("db_upsert_batch", duration)
                upserted_total += len(batch)
            except Exception as exc:
                self._logger.error("prices_upsert_failed: error=%s batch_size=%s", str(exc), len(batch))
                await self._metrics.inc("db_upsert_failures")

        await self._metrics.inc("db_upsert_total", upserted_total)
        self._logger.info("prices_upserted: count=%s", upserted_total)
        return upserted_total


# ---------------------------------------------------------------------------
# 6. ORCHESTRATOR — з Graceful Shutdown
# ---------------------------------------------------------------------------
class ComponentPriceService:
    def __init__(
        self,
        ad_repo: ComponentAdRepository,
        price_repo: ComponentPriceRepository,
        calculator: PercentilePriceCalculator,
        config: PriceAnalyzerConfig,
        metrics: MetricsCollector,
        trace: TracingContext,
        shutdown_event: asyncio.Event | None = None,
    ) -> None:
        self._ad_repo = ad_repo
        self._price_repo = price_repo
        self._calc = calculator
        self._config = config
        self._metrics = metrics
        self._trace = trace
        self._shutdown_event = shutdown_event
        self._logger = _get_logger(__name__, trace)

    async def run(self) -> list[PercentileResult]:
        self._logger.info("price_analysis_started")
        t_start = time.monotonic()

        # 1. Завантаження
        ads = await self._ad_repo.fetch_active_components(self._config)
        if self._shutdown_event and self._shutdown_event.is_set():
            self._logger.info("shutdown_requested_after_fetch")
            return []

        if not ads:
            self._logger.info("no_active_components")
            return []

        # 2. Групування
        by_component: dict[str, list[ComponentAd]] = defaultdict(list)
        for ad in ads:
            by_component[ad.component_name].append(ad)

        # 3. Розрахунок
        today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        results: list[PercentileResult] = []
        upsert_records: list[PriceUpsertRecord] = []

        for comp_name, comp_ads in by_component.items():
            if self._shutdown_event and self._shutdown_event.is_set():
                self._logger.info("shutdown_requested_during_calculation")
                break

            result = self._calc.calculate(comp_name, comp_ads)
            if result:
                idempotency = hashlib.sha256(
                    f"{comp_name}:{today}:{result.price}".encode()
                ).hexdigest()[:32]
                upsert_records.append(PriceUpsertRecord(
                    component_name=result.component_name,
                    price=result.price,
                    date=today,
                    competitor_ids=result.used_ids,
                    idempotency_key=idempotency,
                ))
                results.append(result)
                self._logger.info(
                    "price_calculated: component=%s price=%s sample=%s",
                    comp_name, result.price, result.sample_size,
                )
            else:
                self._logger.info(
                    "price_skipped_insufficient_data: component=%s count=%s",
                    comp_name, len(comp_ads),
                )

        if not upsert_records:
            self._logger.info("no_prices_to_upsert")
            return []

        # 4. Збереження
        upserted = await self._price_repo.upsert_prices(upsert_records)

        total_time = time.monotonic() - t_start
        await self._metrics.time("service_total_duration", total_time)
        self._logger.info(
            "price_analysis_finished: calculated=%s upserted=%s duration_sec=%.2f",
            len(results), upserted, total_time,
        )
        return results


# ---------------------------------------------------------------------------
# 7. FACTORY
# ---------------------------------------------------------------------------
async def create_service_from_env(
    shutdown_event: asyncio.Event | None = None,
) -> tuple[ComponentPriceService, MetricsCollector, httpx.AsyncClient]:
    """Єдине місце створення залежностей."""
    env_path = Path(".env")
    if not env_path.exists():
        env_path = Path(__file__).resolve().parent / ".env"
    load_dotenv(env_path)

    env = EnvConfig(
        supabase_url=os.getenv("SUPABASE_URL", ""),
        supabase_secret_key=os.getenv("SUPABASE_SECRET_KEY", ""),
        supabase_service_role_key=os.getenv("SUPABASE_SERVICE_ROLE_KEY", ""),
    )

    trace = TracingContext()
    metrics = MetricsCollector()
    circuit = CircuitBreaker(
        failure_threshold=env.circuit_failure_threshold,
        recovery_timeout=env.circuit_recovery_timeout,
        logger=_get_logger("circuit_breaker", trace),
    )

    client = httpx.AsyncClient(
        http2=True,
        limits=httpx.Limits(max_keepalive_connections=10, max_connections=20),
    )

    config = PriceAnalyzerConfig()
    ad_repo = SupabaseComponentAdRepository(
        client=client,
        base_url=env.supabase_url,
        api_key=env.supabase_service_role_key,
        env=env,
        metrics=metrics,
        trace=trace,
        circuit=circuit,
    )
    price_repo = SupabaseComponentPriceRepository(
        client=client,
        base_url=env.supabase_url,
        api_key=env.supabase_service_role_key,
        env=env,
        metrics=metrics,
        trace=trace,
        circuit=circuit,
    )
    calculator = PercentilePriceCalculator(config)

    service = ComponentPriceService(
        ad_repo=ad_repo,
        price_repo=price_repo,
        calculator=calculator,
        config=config,
        metrics=metrics,
        trace=trace,
        shutdown_event=shutdown_event,
    )
    return service, metrics, client


# ---------------------------------------------------------------------------
# 8. ENTRY POINT
# ---------------------------------------------------------------------------
async def main_async() -> list[PercentileResult]:
    logger = _get_logger("main")
    logger.info("system_start")

    shutdown_event = asyncio.Event()

    def _signal_handler(sig: int) -> None:
        logger.info("shutdown_signal_received: signal=%s", signal.Signals(sig).name)
        shutdown_event.set()

    # Захист для Windows: сигнали реєструємо лише на Linux/macOS
    if sys.platform != "win32":
        for sig in (signal.SIGTERM, signal.SIGINT):
            try:
                asyncio.get_running_loop().add_signal_handler(sig, _signal_handler, sig)
            except NotImplementedError:
                pass

    service, metrics, client = await create_service_from_env(shutdown_event=shutdown_event)

    try:
        results = await service.run()
        logger.info("final_stats: calculated_count=%s", len(results))
        logger.info("metrics_snapshot: %s", metrics.snapshot())
        return results
    except Exception as exc:
        logger.error("fatal_error: %s", str(exc))
        raise
    finally:
        await client.aclose()
        logger.info("http_client_closed")


def main() -> list[PercentileResult]:
    try:
        return asyncio.run(main_async())
    except KeyboardInterrupt:
        _get_logger("main").info("shutdown_by_user")
        return []


if __name__ == "__main__":
    main()

from __future__ import annotations

import asyncio
import ipaddress
import logging
import os
import sys
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

try:
    import structlog
    _HAS_STRUCTLOG = True
except ImportError:
    _HAS_STRUCTLOG = False

from curl_cffi.requests import AsyncSession
from dotenv import load_dotenv
from pydantic import BaseModel, Field, field_validator
from supabase import Client, create_client


# ---------------------------------------------------------------------------
# Логер
# ---------------------------------------------------------------------------
def _get_logger(name: str) -> Any:
    if _HAS_STRUCTLOG:
        return structlog.get_logger(name)
    return logging.getLogger(name)


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
    datefmt="%H:%M:%S",
)


# ---------------------------------------------------------------------------
# 1. CONFIG
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class ArchiveCheckerConfig:
    allowed_domains: frozenset[str] = field(default_factory=lambda: frozenset({".olx.ua"}))
    blocked_hosts: frozenset[str] = field(default_factory=lambda: frozenset({
        "localhost", "127.0.0.1", "0.0.0.0", "::1",
        "169.254.169.254",
        "metadata.google.internal",
    }))
    blocked_schemes: frozenset[str] = field(default_factory=lambda: frozenset({
        "file", "ftp", "gopher", "dict", "data",
    }))

    max_concurrent_requests: int = 25
    request_timeout_seconds: float = 8.0
    warmup_timeout_seconds: float = 5.0
    warmup_url: str = "https://www.olx.ua/"

    max_ads_per_check: int = 5_000
    db_batch_size: int = 100
    db_query_timeout_seconds: float = 10.0

    progress_log_interval: int = 50

    headers: dict[str, str] = field(default_factory=lambda: {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "accept-language": "uk-UA,uk;q=0.9,en-US;q=0.8,en;q=0.7",
        "user-agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        ),
    })


# ---------------------------------------------------------------------------
# 2. DOMAIN MODELS
# ---------------------------------------------------------------------------
class AdRecord(BaseModel):
    ad_id: int = Field(gt=0)
    url: str = Field(min_length=1, max_length=2048)

    @field_validator("url")
    @classmethod
    def _url_must_be_http(cls, v: str) -> str:
        if not v.startswith(("http://", "https://", "/")):
            raise ValueError("URL має починатися з http, https або /")
        return v

    @property
    def full_url(self) -> str:
        if self.url.startswith("http"):
            return self.url
        return f"https://www.olx.ua{self.url}"


class StatusResult(BaseModel):
    ad_id: int = Field(gt=0)
    status: str = Field(pattern=r"^(active|deactivated)$")
    checked_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


# ---------------------------------------------------------------------------
# 3. SECURITY
# ---------------------------------------------------------------------------
class UrlSafetyValidator:
    def __init__(self, config: ArchiveCheckerConfig) -> None:
        self._config = config
        self._logger = _get_logger(__name__)

    def is_safe(self, url: str) -> bool:
        parsed = urlparse(url)

        if parsed.scheme in self._config.blocked_schemes:
            self._logger.warning("ssrf_blocked_scheme", scheme=parsed.scheme, url=url)
            return False

        if parsed.scheme not in {"http", "https"}:
            return False

        if parsed.username or parsed.password:
            self._logger.warning("ssrf_blocked_credentials", url=url)
            return False

        hostname = (parsed.hostname or "").lower()

        if hostname in self._config.blocked_hosts:
            self._logger.warning("ssrf_blocked_host", host=hostname)
            return False

        try:
            ipaddress.ip_address(hostname)
            self._logger.warning("ssrf_blocked_ip", ip=hostname)
            return False
        except ValueError:
            pass

        if not any(hostname.endswith(d) for d in self._config.allowed_domains):
            self._logger.warning("ssrf_domain_not_allowed", host=hostname)
            return False

        return True


# ---------------------------------------------------------------------------
# 4. PURE FUNCTION (FIXED: використовуємо final_url)
# ---------------------------------------------------------------------------
def determine_status(http_status: int, final_url: str) -> str:
    """
    Чиста функція: за HTTP-статусом та фінальним URL визначає статус.

    >>> determine_status(404, "https://olx.ua/...")
    'deactivated'
    >>> determine_status(200, "https://olx.ua/d/uk/obyavlenie/123")
    'active'
    >>> determine_status(200, "https://www.olx.ua/")  # редирект на головну
    'deactivated'
    """
    if http_status in (404, 410):
        return "deactivated"

    if http_status == 200 and "/obyavlenie/" not in final_url:
        return "deactivated"

    return "active"


# ---------------------------------------------------------------------------
# 5. PROGRESS TRACKER
# ---------------------------------------------------------------------------
class ProgressTracker:
    def __init__(self, total: int, log_interval: int) -> None:
        if total <= 0:
            raise ValueError("total must be positive")
        self._total = total
        self._log_interval = log_interval
        self._processed = 0
        self._lock = asyncio.Lock()
        self._logger = _get_logger(__name__)

    @property
    def total(self) -> int:
        return self._total

    @property
    def processed(self) -> int:
        return self._processed

    async def increment(self) -> None:
        async with self._lock:
            self._processed += 1
            if self._processed % self._log_interval == 0 or self._processed == self._total:
                percent = (self._processed / self._total) * 100
                self._logger.info(
                    "progress_update",
                    processed=self._processed,
                    total=self._total,
                    percent=round(percent, 1),
                )


# ---------------------------------------------------------------------------
# 6. REPOSITORY PATTERN
# ---------------------------------------------------------------------------
class AdRepository(ABC):
    @abstractmethod
    async def get_active_ads(self, limit: int, offset: int = 0) -> list[AdRecord]:
        ...

    @abstractmethod
    async def deactivate_batch(self, ad_ids: list[int], deactivated_at: datetime) -> int:
        ...


class SupabaseAdRepository(AdRepository):
    def __init__(self, client: Client, config: ArchiveCheckerConfig) -> None:
        self._client = client
        self._config = config
        self._logger = _get_logger(__name__)

    async def get_active_ads(self, limit: int, offset: int = 0) -> list[AdRecord]:
        def _query() -> list[dict[str, Any]]:
            try:
                resp = (
                    self._client.table("ads")
                    .select("ad_id, url")
                    .eq("status", "active")
                    .not_.is_("ad_id", "null")
                    .range(offset, offset + limit - 1)
                    .execute()
                )
                return resp.data or []
            except Exception as exc:
                self._logger.error("db_query_failed", error=str(exc))
                return []

        rows = await asyncio.to_thread(_query)
        records: list[AdRecord] = []
        for row in rows:
            try:
                records.append(AdRecord.model_validate(row))
            except Exception as exc:
                self._logger.warning("invalid_ad_record_skipped", row=row, error=str(exc))
        return records

    async def deactivate_batch(self, ad_ids: list[int], deactivated_at: datetime) -> int:
        if not ad_ids:
            return 0

        updated_total = 0
        batch_size = self._config.db_batch_size
        iso_ts = deactivated_at.isoformat()

        for i in range(0, len(ad_ids), batch_size):
            batch = ad_ids[i : i + batch_size]

            def _update(batch_ids: list[int]) -> None:
                self._client.table("ads").update({
                    "status": "deactivated",
                    "deactivated_at": iso_ts,
                }).in_("ad_id", batch_ids).execute()

            try:
                await asyncio.to_thread(_update, batch)
                updated_total += len(batch)
                self._logger.info("deactivated_batch", count=len(batch))
            except Exception as exc:
                self._logger.error("deactivate_batch_failed", error=str(exc), batch_size=len(batch))

        return updated_total


# ---------------------------------------------------------------------------
# [CHANGED] 6.5. SECURITY ERROR — перенесено ПЕРЕД класом, що його використовує
# ---------------------------------------------------------------------------
class SecurityError(Exception):
    """Порушення політики безпеки (SSRF тощо)."""
    pass


# ---------------------------------------------------------------------------
# 7. HTTP CLIENT WRAPPER (FIXED: додано retry)
# ---------------------------------------------------------------------------
class OlxHttpClient:
    def __init__(
        self,
        session: AsyncSession,
        url_validator: UrlSafetyValidator,
        config: ArchiveCheckerConfig,
    ) -> None:
        self._session = session
        self._validator = url_validator
        self._config = config
        self._logger = _get_logger(__name__)

    async def check_url(self, url: str, retries: int = 1) -> tuple[int, str]:
        """
        Робить GET-запит із можливістю retry.
        Повертає (http_status, final_url).
        При мережевій помилці після всіх спроб повертає (0, url).
        """
        if not self._validator.is_safe(url):
            raise SecurityError(f"SSRF: URL заблоковано: {url}")

        for attempt in range(retries + 1):
            try:
                response = await self._session.get(
                    url,
                    allow_redirects=True,
                    timeout=self._config.request_timeout_seconds,
                )
                return response.status_code, str(response.url)
            except asyncio.TimeoutError:
                self._logger.warning("http_timeout", url=url, attempt=attempt + 1)
                if attempt < retries:
                    wait = 1.5 ** attempt
                    self._logger.info("retrying_after_timeout", url=url, wait_sec=round(wait, 1))
                    await asyncio.sleep(wait)
                    continue
                return 0, url
            except Exception as exc:
                if attempt < retries:
                    await asyncio.sleep(1.5 ** attempt)
                    continue
                self._logger.warning(
                    "http_client_error",
                    url=url,
                    error_type=type(exc).__name__,
                    attempts=attempt + 1,
                )
                return 0, url

    async def warmup(self) -> None:
        try:
            resp = await self._session.get(
                self._config.warmup_url,
                timeout=self._config.warmup_timeout_seconds,
            )
            self._logger.info("warmup_ok", status=resp.status_code)
        except Exception as exc:
            self._logger.warning("warmup_failed", error=str(exc))


# ---------------------------------------------------------------------------
# 8. ARCHIVE CHECKER (FIXED: прибрано дублювання запитів у БД)
# ---------------------------------------------------------------------------
class ArchiveChecker:
    def __init__(
        self,
        repository: AdRepository,
        http_client: OlxHttpClient,
        config: ArchiveCheckerConfig,
        db_lock: Any = None,
    ) -> None:
        self._repo = repository
        self._http = http_client
        self._config = config
        self._db_lock = db_lock
        self._logger = _get_logger(__name__)

    async def run(self) -> dict[str, int]:
        start_time = datetime.now(timezone.utc)
        self._logger.info("archive_check_started")

        all_ads: list[AdRecord] = []
        offset = 0
        limit = self._config.db_batch_size

        while len(all_ads) < self._config.max_ads_per_check:
            batch = await self._repo.get_active_ads(limit=limit, offset=offset)
            if not batch:
                break
            all_ads.extend(batch)
            offset += limit

        if not all_ads:
            self._logger.info("no_active_ads")
            return {"checked": 0, "deactivated": 0}

        total = len(all_ads)
        self._logger.info("ads_loaded", count=total)

        await self._http.warmup()

        semaphore = asyncio.Semaphore(self._config.max_concurrent_requests)
        tracker = ProgressTracker(total=total, log_interval=self._config.progress_log_interval)

        tasks = [
            self._check_single(ad.ad_id, ad.full_url, semaphore, tracker)
            for ad in all_ads
        ]

        results: list[StatusResult] = await asyncio.gather(*tasks)

        deactivated_ids = [r.ad_id for r in results if r.status == "deactivated"]
        if deactivated_ids:
            if self._db_lock:
                async with self._db_lock:
                    updated = await self._repo.deactivate_batch(deactivated_ids, start_time)
                    self._logger.info("deactivation_complete", count=updated)
            else:
                updated = await self._repo.deactivate_batch(deactivated_ids, start_time)
            

        elapsed = (datetime.now(timezone.utc) - start_time).total_seconds()
        stats = {
            "checked": len(results),
            "deactivated": len(deactivated_ids),
            "elapsed_sec": round(elapsed, 2),
        }
        self._logger.info("archive_check_finished", **stats)
        return stats


    async def _check_single(
        self,
        ad_id: int,
        url: str,
        semaphore: asyncio.Semaphore,
        tracker: ProgressTracker,
    ) -> StatusResult:
        async with semaphore:
            try:
                status_code, final_url = await self._http.check_url(url)
                if status_code == 0:
                    status = "active"
                else:
                    status = determine_status(status_code, final_url)
            except SecurityError:
                self._logger.error("security_block", ad_id=ad_id, url=url)
                status = "deactivated"

            await tracker.increment()
            return StatusResult(ad_id=ad_id, status=status)


# ---------------------------------------------------------------------------
# 9. FACTORY (FIXED: приймає готову сесію замість створення)
# ---------------------------------------------------------------------------
def create_checker_from_env(session: AsyncSession,  db_lock: Any = None) -> ArchiveChecker:
    """
    Єдине місце створення залежностей (крім HTTP-сесії).
    Сесію створює та закриває caller (main_async), щоб уникнути витоку.
    """
    env_path = Path(__file__).resolve().parent.parent / ".env"
    load_dotenv(env_path)

    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_SECRET_KEY") or os.getenv("SUPABASE_PUBLISHABLE_KEY")
    if not supabase_url or not supabase_key:
        raise RuntimeError("SUPABASE_URL та SUPABASE_SECRET_KEY мають бути в .env")

    supabase_client: Client = create_client(supabase_url, supabase_key)

    config = ArchiveCheckerConfig()
    url_validator = UrlSafetyValidator(config)

    http_client = OlxHttpClient(session, url_validator, config)
    repository = SupabaseAdRepository(supabase_client, config)

    return ArchiveChecker(repository, http_client, config, db_lock=db_lock)


# ---------------------------------------------------------------------------
# 10. ТОЧКА ВХОДУ (FIXED: async with для сесії)
# ---------------------------------------------------------------------------
async def main_async(db_lock: Any = None) -> None:
    logger = _get_logger("main")
    logger.info("system_start")

    config = ArchiveCheckerConfig()

    proxy_url = os.getenv("OLX_PROXY_URL")
    proxy_kwargs = {"proxies": {"http": proxy_url, "https": proxy_url}} if proxy_url else {}

    async with AsyncSession(
        headers=config.headers,
        impersonate="chrome120",
        **proxy_kwargs
    ) as session:
        checker = create_checker_from_env(session, db_lock=db_lock)
        try:
            stats = await checker.run()
            logger.info("final_stats", **stats)
        except Exception as exc:
            logger.error("fatal_error", error=str(exc))
            raise


def main() -> None:
    try:
        if sys.platform == "win32":
            asyncio.run(main_async(), loop_factory=asyncio.SelectorEventLoop)
        else:
            asyncio.run(main_async())
    except KeyboardInterrupt:
        _get_logger("main").info("shutdown_by_user")


if __name__ == "__main__":
    main()
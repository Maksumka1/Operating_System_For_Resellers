"""
Seller Analyzer — Refactored
=============================
Аналіз продавців OLX: рейтинг, угоди, ризик-скор.
Clean Code + DI + Repository + Pydantic + Secure.

Залежності:
  pip install pydantic supabase-py python-dotenv structlog curl_cffi
"""

from __future__ import annotations

import asyncio
import logging
import os
import random
import re
import sys
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    import structlog
    _HAS_STRUCTLOG = True
except ImportError:
    _HAS_STRUCTLOG = False

from curl_cffi.requests import AsyncSession
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from supabase import Client, create_client


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
class SellerAnalyzerConfig:
    """Єдине джерело правди для аналізу продавців."""

    concurrent_requests: int = 5
    request_timeout: float = 8.0
    rate_limit_delay: tuple[float, float] = (0.1, 0.2)

    # Thresholds для ризику
    safe_deals_threshold: int = 20
    safe_stars_threshold: float = 4.0
    safe_age_threshold: int = 2
    neutral_deals_threshold: int = 10
    neutral_stars_threshold: float = 3.0
    neutral_age_threshold: int = 2

    # Thresholds для типу продавця
    shop_deals_threshold: int = 50
    shop_stars_threshold: float = 4.0
    reseller_deals_threshold: int = 30

    # API URLs
    delivery_api_template: str = "https://khonor.eu-sharedservices.olxcdn.com/api/olx/ua/user/{seller_id}/badge/delivery"
    rating_api_template: str = "https://rating-cdn.css.olx.io/ratings/v1/public/olxua/user/{seller_uuid}/eligibleClusters?includeScores=true"

    headers: dict[str, str] = field(default_factory=lambda: {
        "accept": "application/json, text/plain, */*",
        "accept-language": "uk-UA,uk;q=0.9,en-US;q=0.8,en;q=0.7",
        "origin": "https://www.olx.ua",
        "referer": "https://www.olx.ua/",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "x-client": "DESKTOP",
    })

    impersonate: str = "chrome124"
    db_batch_size: int = 100


# ---------------------------------------------------------------------------
# 2. DOMAIN MODELS
# ---------------------------------------------------------------------------
class SellerRawData(BaseModel):
    """Сирий запис продавця з БД."""

    ad_id: int = Field(gt=0)
    seller_id: str | None = Field(default=None)
    seller_uuid: str | None = Field(default=None)
    seller_created_at: str | None = Field(default=None)
    seller_type_raw: str | None = Field(default=None)


class SellerApiData(BaseModel):
    """Дані, отримані з API OLX."""

    successful_deals: int = Field(default=0, ge=0)
    rating_str: str = Field(default="немає оцінок")


class SellerAnalysisResult(BaseModel):
    """Результат аналізу одного продавця."""

    ad_id: int = Field(gt=0)
    successful_deals: int = Field(ge=0)
    seller_rating: str
    seller_type: str = Field(pattern=r"^(shop|reseller|private_person)$")
    seller_risk: str = Field(pattern=r"^(safe|neutral|suspicious)$")


# ---------------------------------------------------------------------------
# 3. PURE FUNCTIONS
# ---------------------------------------------------------------------------
class RatingParser:
    """Чистий клас: парсить рядок рейтингу."""

    @staticmethod
    def parse(rating_str: str) -> tuple[float, bool]:
        """
        Повертає (stars, has_rating).
        >>> RatingParser.parse("4.5/5.0 (120 оцінок)")
        (4.5, True)
        >>> RatingParser.parse("немає оцінок")
        (0.0, False)
        """
        if not rating_str or rating_str == "немає оцінок":
            return 0.0, False
        match = re.match(r"([0-9.]+)/5\.0", rating_str)
        if match:
            return float(match.group(1)), True
        return 0.0, False


class YearExtractor:
    """Чистий клас: витягує рік з рядка."""

    @staticmethod
    def extract(text: str | None) -> int | None:
        """
        >>> YearExtractor.extract("Зареєстрований у 2019 році")
        2019
        >>> YearExtractor.extract(None)
        None
        """
        if not text:
            return None
        match = re.search(r"\b(19|20)\d{2}\b", str(text))
        if match:
            return int(match.group(0))
        return None


class RiskClassifier:
    """Чистий клас: визначає ризик-скор."""

    def __init__(self, config: SellerAnalyzerConfig) -> None:
        self._config = config

    def classify(self, deals: int, stars: float, has_rating: bool, age_years: int | None) -> str:
        """
        safe:       deals >= 20 AND stars >= 4.0 AND age > 2 (з наявним рейтингом)
        neutral:    (deals >= 10 AND stars > 3.0 AND age >= 2) АБО (НЕМАЄ рейтингу AND deals >= 20 AND age >= 2)
        suspicious: everything else
        """
        age = age_years if age_years is not None else 0
        stars_val = stars if has_rating else 0.0

        if deals >= self._config.safe_deals_threshold and stars_val >= self._config.safe_stars_threshold and age > self._config.safe_age_threshold:
            return "safe"

        if deals >= self._config.neutral_deals_threshold and stars_val > self._config.neutral_stars_threshold and age >= self._config.neutral_age_threshold:
            return "neutral"

        if not has_rating and deals >= 20 and age >= 2:
            return "neutral"

        return "suspicious"


class SellerTypeClassifier:
    """Чистий клас: визначає тип продавця."""

    def __init__(self, config: SellerAnalyzerConfig) -> None:
        self._config = config

    def classify(self, is_shop_raw: bool, deals: int, stars: float, has_rating: bool) -> str:
        """
        shop: is_shop_raw=True OR (deals > 50 AND stars >= 4.0)
        reseller: NOT shop AND deals > 30
        private_person: everything else
        """
        stars_val = stars if has_rating else 0.0
        if is_shop_raw or (deals > self._config.shop_deals_threshold and stars_val >= self._config.shop_stars_threshold):
            return "shop"
        if not is_shop_raw and deals > self._config.reseller_deals_threshold:
            return "reseller"
        return "private_person"


# ---------------------------------------------------------------------------
# 4. HTTP CLIENT — абстракція над OLX API
# ---------------------------------------------------------------------------
class OlxSellerApiClient(ABC):
    """Інтерфейс для запитів до OLX API."""

    @abstractmethod
    async def fetch_delivery_deals(self, seller_id: str) -> int:
        ...

    @abstractmethod
    async def fetch_seller_rating(self, seller_uuid: str) -> str:
        ...


class CurlCffiOlxApiClient(OlxSellerApiClient):
    """Реалізація через curl_cffi із захистом від блокувань."""

    def __init__(self, session: AsyncSession, config: SellerAnalyzerConfig) -> None:
        self._session = session
        self._config = config
        self._logger = _get_logger(__name__)

    def _is_valid_id(self, value: str | None) -> bool:
        if not value:
            return False
        return str(value).strip() not in ("", "failed", "None", "null")

    async def fetch_delivery_deals(self, seller_id: str) -> int:
        if not self._is_valid_id(seller_id):
            return 0

        url = self._config.delivery_api_template.format(seller_id=seller_id)
        try:
            resp = await self._session.get(url, timeout=self._config.request_timeout)
            
            if resp.status_code == 200:
                try:
                    data = resp.json()
                    for badge in data.get("body", []):
                        if badge.get("name") == "delivery":
                            return int(badge.get("data", {}).get("amount", 0))
                except Exception:
                    self._logger.warning("delivery_json_parse_error", seller_id=seller_id)
                    return 0
            elif resp.status_code in (403, 429):
                self._logger.error("olx_rate_limit_or_blocked", status_code=resp.status_code, seller_id=seller_id)
            else:
                self._logger.warning("delivery_non_200", status_code=resp.status_code, seller_id=seller_id)

        except Exception as exc:
            self._logger.warning("delivery_fetch_failed", seller_id=seller_id, error=type(exc).__name__)
        return 0

    async def fetch_seller_rating(self, seller_uuid: str) -> str:
        if not self._is_valid_id(seller_uuid):
            return "немає оцінок"

        url = self._config.rating_api_template.format(seller_uuid=seller_uuid)
        try:
            resp = await self._session.get(url, timeout=self._config.request_timeout)
            
            if resp.status_code == 200:
                try:
                    data = resp.json()
                    clusters = data.get("clusters", [])
                    if clusters:
                        score_details = clusters[0].get("scoreDetails", {})
                        score = score_details.get("value")
                        total_ratings = score_details.get("ratings", {}).get("totalCount", 0)
                        if score is not None and total_ratings > 0:
                            return f"{score}/5.0 ({total_ratings} оцінок)"
                except Exception:
                    self._logger.warning("rating_json_parse_error", seller_uuid=seller_uuid)
                    return "немає оцінок"
            elif resp.status_code in (403, 429):
                self._logger.error("olx_rating_blocked", status_code=resp.status_code, seller_uuid=seller_uuid)
            else:
                self._logger.warning("rating_non_200", status_code=resp.status_code, seller_uuid=seller_uuid)

        except Exception as exc:
            self._logger.warning("rating_fetch_failed", seller_uuid=seller_uuid, error=type(exc).__name__)
        return "немає оцінок"


# ---------------------------------------------------------------------------
# 5. REPOSITORY PATTERN
# ---------------------------------------------------------------------------
class SellerRepository(ABC):
    """Інтерфейс сховища продавців."""

    @abstractmethod
    async def fetch_unchecked_sellers(self) -> list[SellerRawData]:
        ...

    @abstractmethod
    async def update_seller_analysis_batch(self, updates: list[SellerAnalysisResult], batch_size: int) -> int:
        ...


class SupabaseSellerRepository(SellerRepository):
    def __init__(self, client: Client) -> None:
        self._client = client
        self._logger = _get_logger(__name__)

    async def fetch_unchecked_sellers(self) -> list[SellerRawData]:
        def _fetch() -> list[dict[str, Any]]:
            try:
                # 🛡️ Беремо до 50 продавців за ітерацію
                resp = (
                    self._client.table("ads")
                    .select("ad_id, seller_id, seller_uuid, seller_created_at, seller_type")
                    .not_.is_("seller_id", "null")
                    .neq("seller_id", "failed")
                    .eq("status", "active")
                    .eq("seller_checked", 0)
                    .order("created_at_olx", desc=True)
                    .limit(50)
                    .execute()
                )
                return resp.data or []
            except Exception as exc:
                self._logger.error("fetch_unchecked_sellers_failed: %s", str(exc))
                return []

        rows = await asyncio.to_thread(_fetch)
        return [SellerRawData.model_validate(r) for r in rows if r.get("ad_id")]

    async def update_seller_analysis_batch(self, updates: list[SellerAnalysisResult], batch_size: int) -> int:
        if not updates:
            return 0

        payload_list = [
            {
                "ad_id": up.ad_id,
                "seller_successful_deals": up.successful_deals,
                "seller_rating": up.seller_rating,
                "seller_type": up.seller_type,
                "seller_risk_score": up.seller_risk,
                "seller_checked": 1,
            }
            for up in updates
        ]

        def _upsert() -> None:
            self._client.table("ads").upsert(payload_list, on_conflict="ad_id").execute()

        try:
            await asyncio.to_thread(_upsert)
            self._logger.info("sellers_upserted_successfully: count=%s", len(payload_list))
            return len(payload_list)
        except Exception as exc:
            self._logger.error("sellers_upsert_failed: %s", str(exc))
            return 0


# ---------------------------------------------------------------------------
# 6. WORKER — аналіз одного продавця
# ---------------------------------------------------------------------------
class SellerAnalyzerWorker:
    """Аналізує одного продавця: HTTP + бізнес-логіка."""

    def __init__(
        self,
        api_client: OlxSellerApiClient,
        risk_classifier: RiskClassifier,
        type_classifier: SellerTypeClassifier,
        year_extractor: YearExtractor,
        rating_parser: RatingParser,
        config: SellerAnalyzerConfig,
    ) -> None:
        self._api = api_client
        self._risk = risk_classifier
        self._type = type_classifier
        self._year = year_extractor
        self._parser = rating_parser
        self._config = config
        self._logger = _get_logger(__name__)

    async def analyze(self, seller: SellerRawData, semaphore: asyncio.Semaphore) -> SellerAnalysisResult | None:
        async with semaphore:
            delay_min, delay_max = self._config.rate_limit_delay
            await asyncio.sleep(random.uniform(delay_min, delay_max))

            deals, rating_str = await asyncio.gather(
                self._api.fetch_delivery_deals(seller.seller_id or ""),
                self._api.fetch_seller_rating(seller.seller_uuid or ""),
            )

        stars, has_rating = self._parser.parse(rating_str)
        reg_year = self._year.extract(seller.seller_created_at)
        today_year = datetime.now(timezone.utc).year
        age_years = max(0, today_year - reg_year) if reg_year else None

        risk = self._risk.classify(deals, stars, has_rating, age_years)
        is_shop_raw = seller.seller_type_raw == "shop"
        seller_type = self._type.classify(is_shop_raw, deals, stars, has_rating)

        self._logger.info(
            "seller_analyzed",
            ad_id=seller.ad_id,
            deals=deals,
            rating=rating_str,
            risk=risk,
            type=seller_type,
        )

        return SellerAnalysisResult(
            ad_id=seller.ad_id,
            successful_deals=deals,
            seller_rating=rating_str,
            seller_type=seller_type,
            seller_risk=risk,
        )


# ---------------------------------------------------------------------------
# 7. ORCHESTRATOR
# ---------------------------------------------------------------------------
class SellerAnalysisService:
    """Головний use-case: завантажити, проаналізувати, зберегти."""

    def __init__(
        self,
        repository: SellerRepository,
        worker: SellerAnalyzerWorker,
        config: SellerAnalyzerConfig,
        db_lock: asyncio.Lock | None = None,
    ) -> None:
        self._repo = repository
        self._worker = worker
        self._config = config
        self._db_lock = db_lock
        self._logger = _get_logger(__name__)

    async def run(self) -> list[int]:
        self._logger.info("seller_analysis_started")
        start_time = time.time()

        sellers = await self._repo.fetch_unchecked_sellers()
        if not sellers:
            self._logger.info("no_unchecked_sellers")
            return []

        self._logger.info("sellers_loaded", count=len(sellers))

        semaphore = asyncio.Semaphore(self._config.concurrent_requests)
        tasks = [self._worker.analyze(s, semaphore) for s in sellers]
        results = await asyncio.gather(*tasks)

        updates = [r for r in results if r is not None]
        if not updates:
            self._logger.info("no_successful_analyses")
            return []

        self._logger.info("sellers_analyzed", count=len(updates))

        if self._db_lock:
            async with self._db_lock:
                updated = await self._repo.update_seller_analysis_batch(
                    updates, self._config.db_batch_size
                )
        else:
            updated = await self._repo.update_seller_analysis_batch(
                updates, self._config.db_batch_size
            )

        elapsed = time.time() - start_time
        updated_ids = [u.ad_id for u in updates]
        self._logger.info("seller_analysis_finished", updated_count=updated, total=len(updates), elapsed_sec=round(elapsed, 2))
        return updated_ids


# ---------------------------------------------------------------------------
# 8. FACTORY
# ---------------------------------------------------------------------------
def create_seller_analysis_service_from_env() -> tuple[SellerAnalyzerConfig, SellerRepository]:
    """Єдине місце створення реальних залежностей."""
    project_root = Path(__file__).resolve().parent.parent
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))

    load_dotenv(project_root / ".env")

    supabase_url = os.getenv("SUPABASE_URL", "").strip()
    supabase_key = os.getenv("SUPABASE_SECRET_KEY", "").strip()

    if not supabase_url: raise RuntimeError("Відсутній SUPABASE_URL у змінних оточення (.env)")
    if not supabase_key: raise RuntimeError("Для виконання оновлень у БД потрібен SUPABASE_SECRET_KEY (service_role key) у .env")    

    supabase_client: Client = create_client(supabase_url, supabase_key)

    config = SellerAnalyzerConfig()
    repository = SupabaseSellerRepository(supabase_client)

    # HTTP-сесію створює caller (main_async), щоб гарантувати закриття
    # Повертаємо config, щоб caller міг створити сесію
    return config, repository


def create_worker(session: AsyncSession, config: SellerAnalyzerConfig) -> SellerAnalyzerWorker:
    """Створює worker з готовою HTTP-сесією."""
    api_client = CurlCffiOlxApiClient(session, config)
    risk = RiskClassifier(config)
    seller_type = SellerTypeClassifier(config)
    year = YearExtractor()
    parser = RatingParser()
    return SellerAnalyzerWorker(api_client, risk, seller_type, year, parser, config)


# ---------------------------------------------------------------------------
# 9. ENTRY POINT
# ---------------------------------------------------------------------------
async def main_async(db_lock: asyncio.Lock | None = None) -> list[int]:
    logger = _get_logger("main")
    logger.info("system_start")

    config, repository = create_seller_analysis_service_from_env()

    proxy_url = os.getenv("OLX_PROXY_URL")
    proxy_kwargs = {"proxies": {"http": proxy_url, "https": proxy_url}} if proxy_url else {}

    async with AsyncSession(
        headers=config.headers,
        impersonate=config.impersonate,
        **proxy_kwargs
    ) as session:
        worker = create_worker(session, config)
        service = SellerAnalysisService(repository, worker, config, db_lock=db_lock)    
        try:
            updated_ids = await service.run()
            logger.info("final_stats", updated_count=len(updated_ids))
            return updated_ids
        except Exception as exc:
            logger.error("fatal_error", error=str(exc))
            raise


def run_seller_analysis() -> list[int]:
    try:
        if sys.platform == "win32":
            return asyncio.run(main_async(), loop_factory=asyncio.SelectorEventLoop)
        else:
            return asyncio.run(main_async())
    except KeyboardInterrupt:
        _get_logger("main").info("shutdown_by_user")
        return []


if __name__ == "__main__":
    run_seller_analysis()
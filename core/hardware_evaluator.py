"""
Hardware Evaluator — Refactored
================================
Оцінка вигідності комплектуючих з Clean Code + DI + Repository.

Залежності:
  pip install pydantic supabase-py python-dotenv structlog
"""

from __future__ import annotations

import asyncio
import logging
import os
import sys
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

try:
    import structlog
    _HAS_STRUCTLOG = True
except ImportError:
    _HAS_STRUCTLOG = False

from dotenv import load_dotenv
from pydantic import BaseModel, Field, field_validator
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
class HardwareEvaluatorConfig:
    """Єдине джерело правди для оцінки комплектуючих."""

    item_types: frozenset[str] = field(default_factory=lambda: frozenset({
        "gpu", "cpu", "motherboard", "psu", "storage", "ram", "bundle",
    }))
    min_price: int = 100
    db_batch_size: int = 100
    page_size: int = 1000

    # Thresholds для deal_status
    super_deal_threshold: float = 15.0      # saving_percent >= 20%
    good_deal_threshold: float = 5.0       # saving_percent >= 10%
    overpriced_threshold: float = -5.0      # saving_percent <= -5%

    # Clamp для відсотка
    min_saving_percent: float = -100.0
    max_saving_percent: float = 100.0


# ---------------------------------------------------------------------------
# 2. DOMAIN MODELS
# ---------------------------------------------------------------------------
class HardwareAdRecord(BaseModel):
    """Один запис комплектуючого з БД."""

    ad_id: int = Field(gt=0)
    component_name: str = Field(min_length=1)
    price: int = Field(gt=0)
    estimated_fair_price: int | None = Field(default=None)
    deal_status: str | None = Field(default=None)


class DealMetrics(BaseModel):
    """Результат розрахунку вигідності."""

    saving_uah: int
    saving_percent: int
    deal_status: str = Field(pattern=r"^(🔥 SUPER DEAL|⭐ GOOD DEAL|❌ OVERPRICED|regular)$")


class DealMetricsUpdate(BaseModel):
    """Одне оновлення для запису в БД."""

    ad_id: int = Field(gt=0)
    estimated_fair_price: int = Field(gt=0)
    saving_uah: int
    saving_percent: int
    deal_status: str


# ---------------------------------------------------------------------------
# 3. PURE FUNCTION — DealCalculator
# ---------------------------------------------------------------------------
class DealCalculator:
    """Чистий клас: розраховує метрики угоди. Немає побічних ефектів."""

    def __init__(self, config: HardwareEvaluatorConfig) -> None:
        self._config = config

    def calculate(self, seller_price: int, fair_price: int) -> DealMetrics:
        """
        Розраховує економію, відсоток та статус угоди.

        >>> calc = DealCalculator(HardwareEvaluatorConfig())
        >>> calc.calculate(8000, 10000)
        DealMetrics(saving_uah=2000, saving_percent=20, deal_status='🔥 SUPER DEAL')
        """
        safe_seller = max(int(seller_price), 1)
        safe_fair = max(int(fair_price), 1)

        saving = safe_fair - safe_seller
        saving_pct = (saving / safe_fair) * 100.0

        # Clamp
        saving_pct = max(self._config.min_saving_percent, min(self._config.max_saving_percent, saving_pct))

        if saving_pct >= self._config.super_deal_threshold:
            status = "🔥 SUPER DEAL"
        elif saving_pct >= self._config.good_deal_threshold:
            status = "⭐ GOOD DEAL"
        elif saving_pct <= self._config.overpriced_threshold:
            status = "❌ OVERPRICED"
        else:
            status = "regular"

        return DealMetrics(
            saving_uah=int(round(saving)),
            saving_percent=int(round(saving_pct)),
            deal_status=status,
        )


# ---------------------------------------------------------------------------
# 4. REPOSITORY PATTERN
# ---------------------------------------------------------------------------
class FairPriceRepository(ABC):
    """Інтерфейс сховища ринкових цін комплектуючих."""

    @abstractmethod
    async def fetch_latest_prices(self) -> dict[str, int]:
        """Повертає словник {component_name: latest_price}."""
        ...


class ComponentPricesRepository(FairPriceRepository):
    """Реалізація через таблицю component_prices."""

    def __init__(self, client: Client) -> None:
        self._client = client
        self._logger = _get_logger(__name__)

    async def fetch_latest_prices(self) -> dict[str, int]:
        def _query() -> list[dict[str, Any]]:
            try:
                resp = (
                    self._client.table("component_prices")
                    .select("component_name, price")
                    .order("date", desc=True)
                    .execute()
                )
                return resp.data or []
            except Exception as exc:
                self._logger.error("fair_prices_fetch_failed", error=str(exc))
                return []

        rows = await asyncio.to_thread(_query)
        prices: dict[str, int] = {}
        for row in rows:
            name = row.get("component_name")
            if name and name not in prices:
                try:
                    prices[name] = int(row["price"])
                except (ValueError, TypeError):
                    self._logger.warning("invalid_price_skipped", row=row)
        return prices


class HardwareAdRepository(ABC):
    """Інтерфейс сховища оголошень комплектуючих."""

    @abstractmethod
    async def fetch_active_hardware(self, config: HardwareEvaluatorConfig) -> list[HardwareAdRecord]:
        """Пагінаційне завантаження активних комплектуючих."""
        ...

    @abstractmethod
    async def update_deal_metrics_batch(self, updates: list[DealMetricsUpdate], batch_size: int) -> int:
        """Оновлює estimated_fair_price, saving_uah, saving_percent, deal_status пачками."""
        ...


class SupabaseHardwareAdRepository(HardwareAdRepository):
    """Реалізація через Supabase."""

    def __init__(self, client: Client) -> None:
        self._client = client
        self._logger = _get_logger(__name__)

    async def fetch_active_hardware(self, config: HardwareEvaluatorConfig) -> list[HardwareAdRecord]:
        def _fetch_page(offset: int, limit: int) -> list[dict[str, Any]]:
            try:
                resp = (
                    self._client.table("ads")
                    .select("ad_id, component_name, price, estimated_fair_price, deal_status")
                    .in_("item_type", list(config.item_types))
                    .eq("status", "active")
                    .gt("price", config.min_price)
                    .not_.is_("component_name", "null")
                    .range(offset, offset + limit - 1)
                    .execute()
                )
                return resp.data or []
            except Exception as exc:
                self._logger.error("hardware_ads_fetch_failed", offset=offset, error=str(exc))
                return []

        all_records: list[HardwareAdRecord] = []
        offset = 0

        while True:
            rows = await asyncio.to_thread(_fetch_page, offset, config.page_size)
            if not rows:
                break

            for row in rows:
                try:
                    all_records.append(HardwareAdRecord.model_validate(row))
                except Exception:
                    self._logger.warning(
                        "invalid_hardware_record_skipped",
                        ad_id=row.get("ad_id"),
                        component=row.get("component_name"),
                    )

            if len(rows) < config.page_size:
                break
            offset += config.page_size

        return all_records

    async def update_deal_metrics_batch(self, updates: list[DealMetricsUpdate], batch_size: int) -> int:
        if not updates:
            return 0

        # Групуємо за payload щоб мінімізувати кількість запитів
        from collections import defaultdict
        by_payload: dict[tuple[int, int, int, str], list[int]] = defaultdict(list)
        for up in updates:
            key = (up.estimated_fair_price, up.saving_uah, up.saving_percent, up.deal_status)
            by_payload[key].append(up.ad_id)

        updated_total = 0

        for (fair_p, sav_uah, sav_pct, d_status), ad_ids in by_payload.items():
            update_data = {
                "estimated_fair_price": fair_p,
                "saving_uah": sav_uah,
                "saving_percent": sav_pct,
                "deal_status": d_status,
            }

            for i in range(0, len(ad_ids), batch_size):
                batch = ad_ids[i : i + batch_size]

                def _update(batch_ids: list[int]) -> None:
                    self._client.table("ads").update(update_data).in_("ad_id", batch_ids).execute()

                try:
                    await asyncio.to_thread(_update, batch)
                    updated_total += len(batch)
                    self._logger.info(
                        "deal_metrics_batch_updated",
                        count=len(batch),
                        status=d_status,
                        fair_price=fair_p,
                    )
                except Exception as exc:
                    self._logger.error("deal_metrics_batch_failed", error=str(exc), batch_size=len(batch))

        return updated_total


# ---------------------------------------------------------------------------
# 5. ORCHESTRATOR
# ---------------------------------------------------------------------------
class HardwareEvaluatorService:
    """Головний use-case: оцінити вигідність комплектуючих та зберегти."""

    def __init__(
        self,
        fair_price_repo: FairPriceRepository,
        hardware_repo: HardwareAdRepository,
        calculator: DealCalculator,
        config: HardwareEvaluatorConfig,
        db_lock: asyncio.Lock | None = None,
    ) -> None:
        self._fair_repo = fair_price_repo
        self._hw_repo = hardware_repo
        self._calc = calculator
        self._config = config
        self._db_lock = db_lock
        self._logger = _get_logger(__name__)

    async def run(self) -> list[int]:
        """Повертає список ad_id, для яких оновлено метрики."""
        self._logger.info("hardware_evaluation_started")

        # --- 1. Завантажуємо ринкові ціни ---
        fair_prices = await self._fair_repo.fetch_latest_prices()
        if not fair_prices:
            self._logger.warning("no_fair_prices_available")
            return []

        self._logger.info("fair_prices_loaded", count=len(fair_prices))

        # --- 2. Завантажуємо активні комплектуючі ---
        ads = await self._hw_repo.fetch_active_hardware(self._config)
        if not ads:
            self._logger.info("no_hardware_ads_to_evaluate")
            return []

        self._logger.info("hardware_ads_loaded", count=len(ads))

        # --- 3. Оцінюємо та формуємо оновлення ---
        updates: list[DealMetricsUpdate] = []
        updated_ids: set[int] = set()

        for ad in ads:
            fair_price = fair_prices.get(ad.component_name)
            if not fair_price or fair_price <= 0:
                continue

            metrics = self._calc.calculate(ad.price, fair_price)

            # Пропускаємо, якщо ціна та статус у БД вже відповідають розрахованим
            if ad.estimated_fair_price == fair_price and ad.deal_status == metrics.deal_status:
                continue

            updates.append(DealMetricsUpdate(
                ad_id=ad.ad_id,
                estimated_fair_price=fair_price,
                saving_uah=metrics.saving_uah,
                saving_percent=metrics.saving_percent,
                deal_status=metrics.deal_status,
            ))
            updated_ids.add(ad.ad_id)

        if not updates:
            self._logger.info("no_updates_needed")
            return []

        self._logger.info("updates_prepared", count=len(updates))

        # --- 4. Зберігаємо ---
        if self._db_lock:
            async with self._db_lock:
                updated = await self._hw_repo.update_deal_metrics_batch(
                    updates, self._config.db_batch_size
                )
        else:
            updated = await self._hw_repo.update_deal_metrics_batch(
                updates, self._config.db_batch_size
            )

        self._logger.info("hardware_evaluation_finished", updated_count=updated, total=len(updates))
        return list(updated_ids)


# ---------------------------------------------------------------------------
# 6. FACTORY
# ---------------------------------------------------------------------------
def create_hardware_evaluator_from_env(db_lock: asyncio.Lock | None = None) -> HardwareEvaluatorService:
    """Єдине місце створення реальних залежностей."""
    project_root = Path(__file__).resolve().parent
    if not (project_root / "config.py").exists():
        project_root = project_root.parent

    load_dotenv(project_root / ".env")

    supabase_url = os.getenv("SUPABASE_URL", "").strip()
    supabase_key = os.getenv("SUPABASE_SECRET_KEY", "").strip()

    if not supabase_url: raise RuntimeError("Відсутній SUPABASE_URL у змінних оточення (.env)")
    if not supabase_key: raise RuntimeError("Для виконання оновлень у БД потрібен SUPABASE_SECRET_KEY (service_role key) у .env")

    supabase_client: Client = create_client(supabase_url, supabase_key)

    config = HardwareEvaluatorConfig()
    fair_repo = ComponentPricesRepository(supabase_client)
    hw_repo = SupabaseHardwareAdRepository(supabase_client)
    calculator = DealCalculator(config)

    return HardwareEvaluatorService(fair_repo, hw_repo, calculator, config, db_lock=db_lock)


# ---------------------------------------------------------------------------
# 7. ENTRY POINT
# ---------------------------------------------------------------------------
async def main_async(db_lock: asyncio.Lock | None = None) -> list[int]:
    logger = _get_logger("main")
    logger.info("system_start")

    service = create_hardware_evaluator_from_env(db_lock=db_lock)
    try:
        updated_ids = await service.run()
        logger.info("final_stats", updated_count=len(updated_ids))
        return updated_ids
    except Exception as exc:
        logger.error("fatal_error", error=str(exc))
        raise


def main() -> list[int]:
    try:
        if sys.platform == "win32":
            return asyncio.run(main_async(), loop_factory=asyncio.SelectorEventLoop)
        else:
            return asyncio.run(main_async())
    except KeyboardInterrupt:
        _get_logger("main").info("shutdown_by_user")
        return []


if __name__ == "__main__":
    main()
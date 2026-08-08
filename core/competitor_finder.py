"""
PC Competitor Price Analyzer — Refactored v2
=============================================
Аналіз конкурентних цін з підтримкою:
  • GPU + CPU → точне співпадіння
  • Тільки CPU → пошук по CPU (без GPU)
  • Без CPU → skip

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
class CompetitorConfig:
    """Єдине джерело правди для аналізу конкурентів."""

    min_price: int = 1000
    db_batch_size: int = 100
    excluded_risk_score: str = "suspicious"
    item_type: str = "pc"
    status: str = "active"


# ---------------------------------------------------------------------------
# 2. DOMAIN MODELS
# ---------------------------------------------------------------------------
class PcBuildRecord(BaseModel):
    """
    Один ПК з розпізнаним залізом.
    GPU — опціональне (може бути null/порожнім).
    CPU — обов'язкове (якщо немає — запис відсіється Pydantic).
    """

    ad_id: int = Field(gt=0)
    gpu_detected: str | None = Field(default=None)
    cpu_detected: str = Field(min_length=1)
    price: int = Field(gt=0)

    @field_validator("cpu_detected")
    @classmethod
    def _cpu_no_unknown(cls, v: str) -> str:
        if "unknown" in v.lower():
            raise ValueError("cpu must not contain 'unknown'")
        return v

    @field_validator("gpu_detected")
    @classmethod
    def _gpu_none_or_valid(cls, v: str | None) -> str | None:
        if v is None:
            return None
        v = v.strip()
        if not v or "unknown" in v.lower():
            return None
        return v

    @property
    def build_key(self) -> str:
        cpu_part = self.cpu_detected.lower()
        if self.gpu_detected:
            return f"{self.gpu_detected.lower()}_{cpu_part}"
        return f"_{cpu_part}"


class CompetitorPriceUpdate(BaseModel):
    """Один запис оновлення ціни конкурента."""

    ad_id: int = Field(gt=0)
    competitor_price: int = Field(gt=0)


# ---------------------------------------------------------------------------
# 3. PURE FUNCTION — обчислення ціни конкурента
# ---------------------------------------------------------------------------
class CompetitorPriceCalculator:
    """Чистий клас: обчислює середню ціну конкурентів для кожної збірки."""

    def calculate(self, records: list[PcBuildRecord]) -> list[CompetitorPriceUpdate]:
        if not records:
            return []

        from collections import defaultdict
        by_build: dict[str, list[PcBuildRecord]] = defaultdict(list)
        for rec in records:
            by_build[rec.build_key].append(rec)

        updates: list[CompetitorPriceUpdate] = []

        for build_key, items in by_build.items():
            for i, current in enumerate(items):
                other_prices = [it.price for j, it in enumerate(items) if j != i]
                
                avg_price = (
                    current.price 
                    if not other_prices 
                    else int(sum(other_prices) / len(other_prices))
                )
                
                updates.append(CompetitorPriceUpdate(
                    ad_id=current.ad_id,
                    competitor_price=avg_price,
                ))

        return updates


# ---------------------------------------------------------------------------
# 4. REPOSITORY PATTERN
# ---------------------------------------------------------------------------
class AdRepository(ABC):
    """Інтерфейс сховища оголошень."""

    @abstractmethod
    async def fetch_pcs_with_hardware(self, config: CompetitorConfig) -> list[PcBuildRecord]:
        """
        Повертає активні ПК.
        CPU обов'язковий, GPU — опціональний.
        """
        ...

    @abstractmethod
    async def update_competitor_prices(self, updates: list[CompetitorPriceUpdate], batch_size: int) -> int:
        """Оновлює competitor_price пачками. Повертає кількість оновлених."""
        ...


class SupabaseAdRepository(AdRepository):
    """Реалізація через Supabase."""

    def __init__(self, client: Client) -> None:
        self._client = client
        self._logger = _get_logger(__name__)

    async def fetch_pcs_with_hardware(self, config: CompetitorConfig) -> list[PcBuildRecord]:
        def _query() -> list[dict[str, Any]]:
            try:
                resp = (
                    self._client.table("ads")
                    .select("ad_id, gpu_detected, cpu_detected, price")
                    .eq("item_type", config.item_type)
                    .eq("status", config.status)
                    .eq("has_defects", 0)
                    .neq("cpu_detected", "Unknown CPU")      # CPU обов'язковий
                    .gt("price", config.min_price)
                    .execute()
                )
                return resp.data or []
            except Exception as exc:
                self._logger.error("db_fetch_failed", error=str(exc))
                return []

        rows = await asyncio.to_thread(_query)
        records: list[PcBuildRecord] = []
        for row in rows:
            try:
                records.append(PcBuildRecord.model_validate(row))
            except Exception:
                # Короткий лог без traceback
                self._logger.warning(
                    "invalid_pc_record_skipped",
                    ad_id=row.get("ad_id"),
                    gpu=row.get("gpu_detected"),
                    cpu=row.get("cpu_detected"),
                )
        return records

    async def update_competitor_prices(self, updates: list[CompetitorPriceUpdate], batch_size: int) -> int:
        if not updates:
            return 0

        from collections import defaultdict
        by_price: dict[int, list[int]] = defaultdict(list)
        for up in updates:
            by_price[up.competitor_price].append(up.ad_id)

        updated_total = 0

        for price_val, ids in by_price.items():
            for i in range(0, len(ids), batch_size):
                batch = ids[i : i + batch_size]

                def _update(batch_ids: list[int]) -> None:
                    self._client.table("ads").update({
                        "competitor_price": price_val,
                    }).in_("ad_id", batch_ids).execute()

                try:
                    await asyncio.to_thread(_update, batch)
                    updated_total += len(batch)
                    self._logger.info("competitor_price_batch_updated", price=price_val, count=len(batch))
                except Exception as exc:
                    self._logger.error("competitor_price_batch_failed", price=price_val, error=str(exc))

        return updated_total


# ---------------------------------------------------------------------------
# 5. ORCHESTRATOR
# ---------------------------------------------------------------------------
class PcCompetitorService:
    """
    Головний use-case: завантажити ПК, обчислити ціни конкурентів, зберегти.
    db_lock ін'єктується — якщо є, використовуємо при записі в БД.
    """

    def __init__(
        self,
        repository: AdRepository,
        calculator: CompetitorPriceCalculator,
        config: CompetitorConfig,
        db_lock: asyncio.Lock | None = None,
    ) -> None:
        self._repo = repository
        self._calc = calculator
        self._config = config
        self._db_lock = db_lock
        self._logger = _get_logger(__name__)

    async def run(self) -> list[int]:
        """Повертає список ad_id, для яких оновлено ціну конкурента."""
        self._logger.info("competitor_analysis_started")

        records = await self._repo.fetch_pcs_with_hardware(self._config)
        if not records:
            self._logger.info("no_pcs_with_hardware")
            return []

        self._logger.info("pcs_loaded", count=len(records))

        updates = self._calc.calculate(records)
        if not updates:
            self._logger.info("no_competitor_prices_calculated")
            return []

        self._logger.info("prices_calculated", count=len(updates))

        if self._db_lock:
            async with self._db_lock:
                updated = await self._repo.update_competitor_prices(
                    updates, self._config.db_batch_size
                )
        else:
            updated = await self._repo.update_competitor_prices(
                updates, self._config.db_batch_size
            )

        updated_ids = [u.ad_id for u in updates]
        self._logger.info("competitor_analysis_finished", updated_count=updated, total=len(updates))
        return updated_ids


# ---------------------------------------------------------------------------
# 6. FACTORY
# ---------------------------------------------------------------------------
def create_competitor_service_from_env(db_lock: asyncio.Lock | None = None) -> PcCompetitorService:
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

    config = CompetitorConfig()
    repository = SupabaseAdRepository(supabase_client)
    calculator = CompetitorPriceCalculator()

    return PcCompetitorService(repository, calculator, config, db_lock=db_lock)


# ---------------------------------------------------------------------------
# 7. ТОЧКА ВХОДУ
# ---------------------------------------------------------------------------
async def main_async(db_lock: asyncio.Lock | None = None) -> list[int]:
    logger = _get_logger("main")
    logger.info("system_start")

    service = create_competitor_service_from_env(db_lock=db_lock)
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
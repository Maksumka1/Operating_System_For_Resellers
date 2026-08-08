"""
PC Evaluator — Refactored
==========================
Оцінка ПК на основі розпізнаних комплектуючих.
Clean Code + DI + Repository + Pydantic + Secure.

Залежності:
  pip install pydantic supabase-py python-dotenv structlog
"""

from __future__ import annotations

import asyncio
import logging
import os
import re
import sys
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

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
class PcEvaluatorConfig:
    """Єдине джерело правди для оцінки ПК."""

    hardware_targets: frozenset[str] = field(default_factory=frozenset)
    min_price: int = 100
    db_batch_size: int = 100
    page_size: int = 1000

    # Вартості за замовчуванням
    base_case_cooler_cost: int = 1200
    base_pc_cost_no_extras: int = 3800

    # Thresholds для deal_status
    super_deal_saving_pct: float = 20.0
    super_deal_saving_uah: int = 2000
    good_deal_saving_pct: float = 8.0
    good_deal_saving_uah: int = 800
    overpriced_threshold: float = -5.0


# ---------------------------------------------------------------------------
# 2. DOMAIN MODELS
# ---------------------------------------------------------------------------
class PcAdRecord(BaseModel):
    """Один ПК для оцінки."""

    ad_id: int = Field(gt=0)
    title: str = Field(default="")
    description: str | None = Field(default=None)
    price: int = Field(gt=0)
    url: str | None = Field(default=None)

    @property
    def full_text(self) -> str:
        text = f"{self.title} {self.description or ''}".strip()
        # Обрізаємо додаткові опції
        return re.split(r"додатков|опці|за доплат|доплати", text, flags=re.IGNORECASE)[0]


class ExtractedComponents(BaseModel):
    """Розпізнані комплектуючі з тексту."""

    gpu: str | None = Field(default=None)
    cpu: str | None = Field(default=None)
    motherboard: str | None = Field(default=None)
    ram: str | None = Field(default=None)
    storage: str | None = Field(default=None)
    psu: str | None = Field(default=None)


class PcEvaluationResult(BaseModel):
    """Результат оцінки одного ПК."""

    ad_id: int = Field(gt=0)
    seller_price_clean: int = Field(gt=0)

    gpu_detected: str = Field(default="Unknown GPU")
    gpu_market_price: int = Field(default=0)
    cpu_detected: str = Field(default="Unknown CPU")
    cpu_market_price: int = Field(default=0)
    mb_detected: str | None = Field(default=None)
    motherboard_detected: str | None = Field(default=None)
    mb_market_price: int = Field(default=0)
    ram_detected: str | None = Field(default=None)
    ram_market_price: int = Field(default=0)
    psu_detected: str | None = Field(default=None)
    psu_market_price: int = Field(default=0)
    storage_detected: str | None = Field(default=None)
    ssd_detected: str | None = Field(default=None)
    storage_market_price: int = Field(default=0)
    ssd_market_price: int = Field(default=0)

    estimated_fair_price: int = Field(gt=0)
    saving_uah: int
    saving_percent: int
    deal_status: str = Field(pattern=r"^(🔥 SUPER DEAL|⭐ GOOD DEAL|❌ OVERPRICED|regular)$")
    evaluated_at: str


# ---------------------------------------------------------------------------
# 3. HARDWARE EXTRACTOR — абстракція над парсером заліза
# ---------------------------------------------------------------------------
class HardwareExtractor(ABC):
    """Інтерфейс для розпізнавання комплектуючих у тексті."""

    @abstractmethod
    def extract(self, text: str) -> ExtractedComponents:
        ...


class HardwareMatchersExtractor(HardwareExtractor):
    """Адаптер для модуля hardware_matchers."""

    def __init__(
        self,
        hardware_targets: frozenset[str],
        extract_gpu_fn: Callable[[str], list[str]],
        extract_cpu_fn: Callable[[str], list[str]],
        extract_motherboard_fn: Callable[[str], list[str]],
        extract_ram_fn: Callable[[str], list[str]],
        extract_storage_fn: Callable[[str], list[str]],
        extract_psu_fn: Callable[[str], list[str]],
        normalize_fn: Callable[[str], str],
    ) -> None:
        self._targets = hardware_targets
        self._extract_gpu = extract_gpu_fn
        self._extract_cpu = extract_cpu_fn
        self._extract_mb = extract_motherboard_fn
        self._extract_ram = extract_ram_fn
        self._extract_storage = extract_storage_fn
        self._extract_psu = extract_psu_fn
        self._normalize = normalize_fn

    def _first_match(self, candidates: list[str]) -> str | None:
        for c in candidates:
            if c in self._targets:
                return c
        return None

    def extract(self, text: str) -> ExtractedComponents:
        clean = self._normalize(text)
        return ExtractedComponents(
            gpu=self._first_match(self._extract_gpu(clean)),
            cpu=self._first_match(self._extract_cpu(clean)),
            motherboard=self._first_match(self._extract_mb(clean)),
            ram=self._first_match(self._extract_ram(clean)),
            storage=self._first_match(self._extract_storage(clean)),
            psu=self._first_match(self._extract_psu(clean)),
        )


# ---------------------------------------------------------------------------
# 4. PRICE REPOSITORY
# ---------------------------------------------------------------------------
class ComponentPriceRepository(ABC):
    """Інтерфейс сховища цін комплектуючих."""

    @abstractmethod
    async def fetch_prices(self) -> dict[str, int]:
        """Повертає {component_name: price}."""
        ...


class SupabaseComponentPriceRepository(ComponentPriceRepository):
    """Реалізація через Supabase з fallback."""

    def __init__(self, client: Client) -> None:
        self._client = client
        self._logger = _get_logger(__name__)

    async def fetch_prices(self) -> dict[str, int]:
        # Спроба 1: component_prices
        prices = await self._fetch_from_component_prices()
        if prices:
            return prices

        # Спроба 2: fallback на ads
        self._logger.warning("component_prices_empty_fallback_to_ads")
        return await self._fetch_from_ads()

    async def _fetch_from_component_prices(self) -> dict[str, int]:
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
                self._logger.error("component_prices_fetch_failed", error=str(exc))
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

    async def _fetch_from_ads(self) -> dict[str, int]:
        def _query() -> list[dict[str, Any]]:
            try:
                resp = (
                    self._client.table("ads")
                    .select("component_name, competitor_price")
                    .in_("item_type", ["gpu", "cpu", "motherboard", "psu", "storage", "ram", "bundle"])
                    .eq("status", "active")
                    .gt("competitor_price", 0)
                    .not_.is_("component_name", "null")
                    .execute()
                )
                return resp.data or []
            except Exception as exc:
                self._logger.error("ads_prices_fetch_failed", error=str(exc))
                return []

        rows = await asyncio.to_thread(_query)
        prices: dict[str, int] = {}
        for row in rows:
            name = row.get("component_name")
            if name:
                try:
                    prices[name] = int(row["competitor_price"])
                except (ValueError, TypeError):
                    pass
        return prices


# ---------------------------------------------------------------------------
# 5. PC AD REPOSITORY
# ---------------------------------------------------------------------------
class PcAdRepository(ABC):
    """Інтерфейс сховища ПК-оголошень."""

    @abstractmethod
    async def fetch_unrated_pcs(self, config: PcEvaluatorConfig) -> list[PcAdRecord]:
        """Пагінаційне завантаження ПК без estimated_fair_price."""
        ...

    @abstractmethod
    async def update_evaluations(self, evaluations: list[PcEvaluationResult], batch_size: int) -> int:
        """Пакетне оновлення оцінок. Повертає кількість оновлених."""
        ...


class SupabasePcAdRepository(PcAdRepository):
    def __init__(self, client: Client) -> None:
        self._client = client
        self._logger = _get_logger(__name__)

    async def fetch_unrated_pcs(self, config: PcEvaluatorConfig) -> list[PcAdRecord]:
        def _fetch_page(offset: int, limit: int) -> list[dict[str, Any]]:
            try:
                resp = (
                    self._client.table("ads")
                    .select("ad_id, title, description, price, url")
                    .eq("item_type", "pc")
                    .eq("status", "active")
                    .or_("has_defects.eq.0,has_defects.is.null")
                    .is_("estimated_fair_price", "null")
                    .range(offset, offset + limit - 1)
                    .execute()
                )
                return resp.data or []
            except Exception as exc:
                self._logger.error("unrated_pcs_fetch_failed", offset=offset, error=str(exc))
                return []

        all_records: list[PcAdRecord] = []
        offset = 0

        while True:
            rows = await asyncio.to_thread(_fetch_page, offset, config.page_size)
            if not rows:
                break

            for row in rows:
                try:
                    all_records.append(PcAdRecord.model_validate(row))
                except Exception:
                    self._logger.warning(
                        "invalid_pc_record_skipped",
                        ad_id=row.get("ad_id"),
                    )

            if len(rows) < config.page_size:
                break
            offset += config.page_size

        return all_records

    async def update_evaluations(self, evaluations: list[PcEvaluationResult], batch_size: int) -> int:
        if not evaluations:
            return 0

        from collections import defaultdict

        # Групуємо за payload щоб мінімізувати запити
        by_payload: dict[tuple, list[int]] = defaultdict(list)
        for ev in evaluations:
            key = (
                ev.seller_price_clean,
                ev.gpu_detected, ev.cpu_detected,
                ev.gpu_market_price, ev.cpu_market_price,
                ev.mb_detected, ev.mb_market_price,
                ev.ram_detected, ev.ram_market_price,
                ev.psu_detected, ev.psu_market_price,
                ev.storage_detected, ev.storage_market_price,
                ev.estimated_fair_price, ev.saving_uah, ev.saving_percent,
                ev.deal_status, ev.evaluated_at,
            )
            by_payload[key].append(ev.ad_id)

        updated_total = 0

        for payload_tuple, ad_ids in by_payload.items():
            payload = {
                "seller_price_clean": payload_tuple[0],
                "gpu_detected": payload_tuple[1],
                "cpu_detected": payload_tuple[2],
                "gpu_market_price": payload_tuple[3],
                "cpu_market_price": payload_tuple[4],
                "mb_detected": payload_tuple[5],
                "motherboard_detected": payload_tuple[5],
                "mb_market_price": payload_tuple[6],
                "motherboard_market_price": payload_tuple[6],
                "ram_detected": payload_tuple[7],
                "ram_market_price": payload_tuple[8],
                "psu_detected": payload_tuple[9],
                "psu_market_price": payload_tuple[10],
                "storage_detected": payload_tuple[11],
                "ssd_detected": payload_tuple[11],
                "storage_market_price": payload_tuple[12],
                "ssd_market_price": payload_tuple[12],
                "estimated_fair_price": payload_tuple[13],
                "saving_uah": payload_tuple[14],
                "saving_percent": payload_tuple[15],
                "deal_status": payload_tuple[16],
                "evaluated_at": payload_tuple[17],
            }

            for i in range(0, len(ad_ids), batch_size):
                batch = ad_ids[i : i + batch_size]

                def _update(batch_ids: list[int]) -> None:
                    self._client.table("ads").update(payload).in_("ad_id", batch_ids).execute()

                try:
                    await asyncio.to_thread(_update, batch)
                    updated_total += len(batch)
                    self._logger.info("evaluation_batch_updated", count=len(batch), status=payload_tuple[16])
                except Exception as exc:
                    self._logger.error("evaluation_batch_failed", error=str(exc), batch_size=len(batch))

        return updated_total


# ---------------------------------------------------------------------------
# 6. PURE FUNCTION — оцінка одного ПК
# ---------------------------------------------------------------------------
class PcEvaluator:
    """Чистий клас: оцінює один ПК. Немає побічних ефектів."""

    def __init__(self, config: PcEvaluatorConfig) -> None:
        self._config = config

    def evaluate(
        self,
        ad: PcAdRecord,
        components: ExtractedComponents,
        component_prices: dict[str, int],
    ) -> PcEvaluationResult:
        gpu_price = component_prices.get(components.gpu, 0) if components.gpu else 0
        cpu_price = component_prices.get(components.cpu, 0) if components.cpu else 0
        mb_price = component_prices.get(components.motherboard, 0) if components.motherboard else 0
        ram_price = component_prices.get(components.ram, 0) if components.ram else 0
        storage_price = component_prices.get(components.storage, 0) if components.storage else 0
        psu_price = component_prices.get(components.psu, 0) if components.psu else 0

        known_extra = mb_price + ram_price + storage_price + psu_price

        if known_extra > 0:
            fair_price = gpu_price + cpu_price + known_extra + self._config.base_case_cooler_cost
        else:
            fair_price = gpu_price + cpu_price + self._config.base_pc_cost_no_extras

        safe_seller = max(ad.price, 1)
        saving = fair_price - safe_seller
        saving_pct = (saving / fair_price * 100) if fair_price > 0 else 0

        if saving_pct >= self._config.super_deal_saving_pct or saving >= self._config.super_deal_saving_uah:
            deal_status = "🔥 SUPER DEAL"
        elif saving_pct >= self._config.good_deal_saving_pct or saving >= self._config.good_deal_saving_uah:
            deal_status = "⭐ GOOD DEAL"
        elif saving_pct <= self._config.overpriced_threshold:
            deal_status = "❌ OVERPRICED"
        else:
            deal_status = "regular"

        cpu_display = components.cpu or "Unknown CPU"
        if cpu_display == "Unknown CPU":
            deal_status = "regular"
            saving = 0
            saving_pct = 0

        now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M")

        return PcEvaluationResult(
            ad_id=ad.ad_id,
            seller_price_clean=safe_seller,
            gpu_detected=components.gpu or "Unknown GPU",
            gpu_market_price=gpu_price,
            cpu_detected=cpu_display,
            cpu_market_price=cpu_price,
            mb_detected=components.motherboard,
            motherboard_detected=components.motherboard,
            mb_market_price=mb_price,
            ram_detected=components.ram,
            ram_market_price=ram_price,
            psu_detected=components.psu,
            psu_market_price=psu_price,
            storage_detected=components.storage,
            ssd_detected=components.storage,
            storage_market_price=storage_price,
            ssd_market_price=storage_price,
            estimated_fair_price=int(fair_price),
            saving_uah=int(round(saving)),
            saving_percent=int(round(saving_pct)),
            deal_status=deal_status,
            evaluated_at=now,
        )


# ---------------------------------------------------------------------------
# 7. ORCHESTRATOR
# ---------------------------------------------------------------------------
class PcEvaluationService:
    """Головний use-case: завантажити ціни, оцінити ПК, зберегти."""

    def __init__(
        self,
        price_repo: ComponentPriceRepository,
        pc_repo: PcAdRepository,
        extractor: HardwareExtractor,
        evaluator: PcEvaluator,
        config: PcEvaluatorConfig,
        db_lock: asyncio.Lock | None = None,
    ) -> None:
        self._price_repo = price_repo
        self._pc_repo = pc_repo
        self._extractor = extractor
        self._evaluator = evaluator
        self._config = config
        self._db_lock = db_lock
        self._logger = _get_logger(__name__)

    async def run(self) -> list[int]:
        self._logger.info("pc_evaluation_started")

        # --- 1. Ціни ---
        prices = await self._price_repo.fetch_prices()
        if not prices:
            self._logger.warning("no_component_prices_available")
            return []

        self._logger.info("prices_loaded", count=len(prices))

        # --- 2. ПК для оцінки ---
        pcs = await self._pc_repo.fetch_unrated_pcs(self._config)
        if not pcs:
            self._logger.info("no_unrated_pcs")
            return []

        self._logger.info("unrated_pcs_loaded", count=len(pcs))

        # --- 3. Оцінка ---
        evaluations: list[PcEvaluationResult] = []
        for pc in pcs:
            components = self._extractor.extract(pc.full_text)
            result = self._evaluator.evaluate(pc, components, prices)
            evaluations.append(result)

        self._logger.info("pcs_evaluated", count=len(evaluations))

        # --- 4. Збереження ---
        if self._db_lock:
            async with self._db_lock:
                updated = await self._pc_repo.update_evaluations(
                    evaluations, self._config.db_batch_size
                )
        else:
            updated = await self._pc_repo.update_evaluations(
                evaluations, self._config.db_batch_size
            )

        updated_ids = [e.ad_id for e in evaluations]
        self._logger.info("pc_evaluation_finished", updated_count=updated, total=len(evaluations))
        return updated_ids


# ---------------------------------------------------------------------------
# 8. FACTORY
# ---------------------------------------------------------------------------
def create_pc_evaluation_service_from_env(
    db_lock: asyncio.Lock | None = None,
) -> PcEvaluationService:
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

    # Імпортуємо hardware_matchers та HARDWARE_TARGETS
    try:
        from config import HARDWARE_TARGETS
        from hardware_matchers import (
            extract_cpu,
            extract_gpu,
            extract_motherboard,
            extract_psu,
            extract_ram,
            extract_storage,
            normalize_title,
        )
    except ImportError as exc:
        raise RuntimeError(f"Не вдалося імпортувати hardware_matchers: {exc}")

    config = PcEvaluatorConfig(
        hardware_targets=frozenset(HARDWARE_TARGETS),
    )

    extractor = HardwareMatchersExtractor(
        hardware_targets=config.hardware_targets,
        extract_gpu_fn=extract_gpu,
        extract_cpu_fn=extract_cpu,
        extract_motherboard_fn=extract_motherboard,
        extract_ram_fn=extract_ram,
        extract_storage_fn=extract_storage,
        extract_psu_fn=extract_psu,
        normalize_fn=normalize_title,
    )

    price_repo = SupabaseComponentPriceRepository(supabase_client)
    pc_repo = SupabasePcAdRepository(supabase_client)
    evaluator = PcEvaluator(config)

    return PcEvaluationService(price_repo, pc_repo, extractor, evaluator, config, db_lock=db_lock)


# ---------------------------------------------------------------------------
# 9. ENTRY POINT
# ---------------------------------------------------------------------------
async def main_async(db_lock: asyncio.Lock | None = None) -> list[int]:
    logger = _get_logger("main")
    logger.info("system_start")

    service = create_pc_evaluation_service_from_env(db_lock=db_lock)
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
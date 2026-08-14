"""
PC Category Categorizer — Refactored
======================================
Категоризація ПК з Clean Code + DI + Repository + Pydantic.

Залежності:
  pip install pydantic supabase-py python-dotenv structlog
"""

from __future__ import annotations

import asyncio
import json
import logging
import os
import re
import sys
from abc import ABC, abstractmethod
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone
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
# 1. CONFIG (Оновлені та збалансовані патерни)
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class PcCategoryConfig:
    """Конфігурація патернів для точної категоризації ПК."""

    # 1. Майнінг обладнання (ASIC, ферми, крипта)
    mining_pattern: re.Pattern = field(default_factory=lambda: re.compile(
        r"(?i)\b(antminer|асик|асік|майнер|майнинг\s*ферм\w*|майнінг\s*ферм\w*|майнінг\s*р[іи]г|хешрейт|hashrate|\d+\s*th\b|\d+\s*gh/s)\b"
    ))
    
    # 2. Реальний ОПТ / Гурт / Barebone (вищий пріоритет за бренди!)
    wholesale_pattern: re.Pattern = field(default_factory=lambda: re.compile(
        r"(?i)\b(гурт\b|оптом?|зі\s*складу|со\s*склада|партией|партією|в\s*наявності\s*\d+\s*шт|"
        r"від\s*\d+\s*шт|от\s*\d+\s*шт|розпродаж\s*офісу|распродажа\s*офиса|barebone|тушка)\b"
    ))

    # 3. Застаріле (Тільки DDR1/2, SDRAM, Socket 775/старі, Core 2 Duo, старі 2-ядерні пентіуми та карти 8xxx/9xxx GT)
    obsolete_pattern: re.Pattern = field(default_factory=lambda: re.compile(
        r"(?i)\b(ddr\s*[-_]?[12](?!\d)|sdram|core\s*2\s*duo|core2duo|athlon\s*(?:ii|x[234]|64)?|"
        r"socket\s*(?:7|370|478|775)|lga\s*775|\b775\b|am[23]\+?|fm1\b|2\s*ядерн\w*|двохядерн\w*|"
        r"g2020|g2030|g1610|g1620|g1820|g860|g840|pentium\s*[1234]\b|"
        r"geforce\s*[6789]\d{3}|8600\s*gt|9600\s*gt|9800\s*gt|застаріл\w*|устаревш\w*)\b"
    ))

    # 4. Брендові офісні ПК та Моноблоки (якщо НЕ опт)
    brand_office_pattern: re.Pattern = field(default_factory=lambda: re.compile(
        r"(?i)\b(optiplex|lenovo|dell|fujitsu|prodesk|elitedesk|thinkcentre|thinkstation|precision|esprimo|"
        r"veriton|ideacentre|legion\s*[tctg]?\d*|alienware|omen|z\d{3}|моноблок|all-in-one|aio)\b"
    ))

    # 5. Ігрові ПК (дискретні GPU, ігрові CPU та ключові слова)
    gaming_pattern: re.Pattern = field(default_factory=lambda: re.compile(
        r"(?i)\b(rtx\s*\d{3,4}|gtx\s*(?:1660|1650|1060|1070|1080|970|980|780|770)|"
        r"rx\s*(?:4[78]0|5[789]0|[567]\d{3})|3060\s*т[іi]|3070\s*т[іi]|4060\s*т[іi]|4070\s*т[іi]|"
        r"для\s*ігор|для\s*игр|ігров\w+|игров\w+|геймерс\w+|gaming|ryzen\s*[579]|"
        r"5600x?|5500x?|5700x?|7500f|7600x?|7800x3d|5800x3d|5500x3d|"
        r"12400f?|10400f?|11400f?|13400f?|14400f?)\b"
    ))

    # Мережа / БД
    db_batch_size: int = 100
    db_query_timeout_seconds: float = 10.0
    stats_file: Path | None = None


# ---------------------------------------------------------------------------
# 2. DOMAIN MODELS
# ---------------------------------------------------------------------------
class AdRecord(BaseModel):
    """Один запис оголошення з БД."""

    ad_id: int = Field(gt=0)
    title: str = Field(default="")
    description: str = Field(default="")

    @property
    def full_text(self) -> str:
        return f"{self.title} {self.description}".strip()


class CategoryResult(BaseModel):
    """Результат категоризації одного оголошення."""

    ad_id: int = Field(gt=0)
    category: str = Field(pattern=r"^(obsolete|wholesale|brand_office|gaming|home_office|mining)$")


class CategoryStats(BaseModel):
    """Звіт по категоріях."""

    obsolete: int = 0
    wholesale: int = 0
    brand_office: int = 0
    gaming: int = 0
    home_office: int = 0
    mining: int = 0

    def increment(self, category: str) -> None:
        if hasattr(self, category):
            setattr(self, category, getattr(self, category) + 1)


# ---------------------------------------------------------------------------
# 3. PURE FUNCTION — Детектор категорії з оновленою ієрархією
# ---------------------------------------------------------------------------
class PcCategoryDetector:
    def __init__(self, config: PcCategoryConfig) -> None:
        self._config = config

    def detect(self, text: str | None) -> str:
        if not text:
            return "home_office"

        full_text = text.strip()

        if self._config.mining_pattern.search(full_text):
            return "mining"

        if self._config.wholesale_pattern.search(full_text):
            return "wholesale"

        if self._config.obsolete_pattern.search(full_text):
            return "obsolete"

        if self._config.brand_office_pattern.search(full_text):
            return "brand_office"

        if self._config.gaming_pattern.search(full_text):
            return "gaming"

        return "home_office"


# ---------------------------------------------------------------------------
# 4. REPOSITORY PATTERN — абстракція над БД
# ---------------------------------------------------------------------------
class AdRepository(ABC):
    """Інтерфейс сховища оголошень."""

    @abstractmethod
    async def fetch_uncategorized_pcs(self) -> list[AdRecord]:
        ...

    @abstractmethod
    async def update_category_batch(self, category: str, ad_ids: list[int]) -> int:
        """Повертає кількість оновлених записів."""
        ...

    @abstractmethod
    async def count_active_clean(self) -> int:
        """Кількість активних ПК без дефектів і не obsolete."""
        ...


class SupabaseAdRepository(AdRepository):
    """Реалізація через Supabase."""

    def __init__(self, client: Client, config: PcCategoryConfig) -> None:
        self._client = client
        self._config = config
        self._logger = _get_logger(__name__)

    async def fetch_uncategorized_pcs(self) -> list[AdRecord]:
        def _query() -> list[dict[str, Any]]:
            try:
                resp = (
                    self._client.table("ads")
                    .select("ad_id, title, description")
                    .eq("item_type", "pc")
                    .eq("status", "active")
                    .or_("pc_category.eq.uncategorized,pc_category.is.null")
                    .execute()
                )
                return resp.data or []
            except Exception as exc:
                self._logger.error("db_fetch_failed", error=str(exc))
                return []

        rows = await asyncio.to_thread(_query)
        records: list[AdRecord] = []
        for row in rows:
            try:
                records.append(AdRecord.model_validate(row))
            except Exception as exc:
                self._logger.warning("invalid_ad_record_skipped", row=row, error=str(exc))
        return records

    async def update_category_batch(self, category: str, ad_ids: list[int]) -> int:
        if not ad_ids:
            return 0

        updated_total = 0
        batch_size = self._config.db_batch_size

        for i in range(0, len(ad_ids), batch_size):
            batch = ad_ids[i : i + batch_size]

            def _update(batch_ids: list[int]) -> None:
                self._client.table("ads").update({
                    "pc_category": category,
                }).in_("ad_id", batch_ids).execute()

            try:
                await asyncio.to_thread(_update, batch)
                updated_total += len(batch)
                self._logger.info("category_batch_updated", category=category, count=len(batch))
            except Exception as exc:
                self._logger.error("category_batch_failed", category=category, error=str(exc))

        return updated_total

    async def count_active_clean(self) -> int:
        def _query() -> int:
            try:
                resp = (
                    self._client.table("ads")
                    .select("ad_id", count="exact")
                    .eq("item_type", "pc")
                    .eq("status", "active")
                    .eq("has_defects", 0)
                    .neq("pc_category", "obsolete")
                    .execute()
                )
                return resp.count or 0
            except Exception as exc:
                self._logger.error("db_count_failed", error=str(exc))
                return 0

        return await asyncio.to_thread(_query)


# ---------------------------------------------------------------------------
# 5. STATS REPOSITORY — абстракція над файлом статистики
# ---------------------------------------------------------------------------
class StatsRepository(ABC):
    @abstractmethod
    async def update_statistics(self, section: str, metrics: dict[str, Any]) -> None:
        ...


class JsonStatsRepository(StatsRepository):
    """Запис статистики у JSON-файл."""

    def __init__(self, stats_file: Path) -> None:
        self._stats_file = stats_file
        self._logger = _get_logger(__name__)

    async def update_statistics(self, section: str, metrics: dict[str, Any]) -> None:
        def _file_io() -> None:
            today_str = datetime.now(timezone.utc).strftime("%d-%m-%Y")
            stats: dict[str, Any] = {}

            if self._stats_file.exists():
                try:
                    stats = json.loads(self._stats_file.read_text(encoding="utf-8"))
                except json.JSONDecodeError:
                    stats = {}

            if today_str not in stats:
                stats[today_str] = {
                    "parsing": {"parsed_total_new": 0, "duplicates_skipped": 0},
                    "filtering": {"defects_found": 0, "filtered_total_active": 0},
                    "categories": {},
                    "market_analysis": {"avg_ad_price_uah": 0, "min_price_today": 0, "max_price_today": 0},
                }

            if section in stats[today_str]:
                stats[today_str][section].update(metrics)

            self._stats_file.write_text(
                json.dumps(stats, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )

        await asyncio.to_thread(_file_io)
        self._logger.info("stats_updated", section=section, file=str(self._stats_file))


# ---------------------------------------------------------------------------
# 6. ORCHESTRATOR — тільки координує
# ---------------------------------------------------------------------------
class PcCategoryService:
    """Головний use-case: завантажити, категоризувати, зберегти."""

    def __init__(
        self,
        repository: AdRepository,
        detector: PcCategoryDetector,
        stats_repo: StatsRepository,
        db_lock: asyncio.Lock | None = None,
    ) -> None:
        self._repo = repository
        self._detector = detector
        self._stats_repo = stats_repo
        self._db_lock = db_lock
        self._logger = _get_logger(__name__)

    async def run(self) -> CategoryStats:
        self._logger.info("categorization_started")

        # --- 1. Завантаження ---
        unfiltered = await self._repo.fetch_uncategorized_pcs()
        if not unfiltered:
            self._logger.info("no_uncategorized_pcs")
            return CategoryStats()

        self._logger.info("pcs_loaded", count=len(unfiltered))

        # --- 2. Категоризація ---
        stats = CategoryStats()
        ids_by_category: dict[str, list[int]] = defaultdict(list)

        for ad in unfiltered:
            category = self._detector.detect(ad.full_text)
            stats.increment(category)
            ids_by_category[category].append(ad.ad_id)

        # --- 3. Оновлення БД ---
        updated_total = 0
        for category, ids in ids_by_category.items():
            if not ids:
                continue
            if self._db_lock:
                async with self._db_lock:
                    updated_total += await self._repo.update_category_batch(category, ids)
            else:
                updated_total += await self._repo.update_category_batch(category, ids)

        self._logger.info("categories_saved", total_updated=updated_total)

        # --- 4. Статистика ---
        active_clean_total = await self._repo.count_active_clean()

        await self._stats_repo.update_statistics("filtering", {
            "filtered_total_active": active_clean_total,
        })
        await self._stats_repo.update_statistics("categories", stats.model_dump())

        self._logger.info("categorization_finished", **stats.model_dump())
        return stats


# ---------------------------------------------------------------------------
# 7. FACTORY
# ---------------------------------------------------------------------------
def create_categorizer_from_env(db_lock: asyncio.Lock | None = None) -> PcCategoryService:
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

    # STATS_FILE імпортується з config.py, якщо доступний
    stats_file: Path | None = None
    try:
        sys.path.insert(0, str(project_root))
        from config import STATS_FILE as _sf
        stats_file = _sf
    except ImportError:
        pass

    config = PcCategoryConfig(stats_file=stats_file)
    detector = PcCategoryDetector(config)
    repository = SupabaseAdRepository(supabase_client, config)

    stats_repo: StatsRepository
    if stats_file:
        stats_repo = JsonStatsRepository(stats_file)
    else:
        # Якщо файл статистики не знайдено — no-op репозиторій
        stats_repo = _NoOpStatsRepository()

    return PcCategoryService(repository, detector, stats_repo, db_lock=db_lock)


class _NoOpStatsRepository(StatsRepository):
    """Заглушка, якщо файл статистики недоступний."""

    async def update_statistics(self, section: str, metrics: dict[str, Any]) -> None:
        pass


# ---------------------------------------------------------------------------
# 8. ТОЧКА ВХОДУ
# ---------------------------------------------------------------------------
async def main_async(db_lock: asyncio.Lock | None = None) -> None:
    logger = _get_logger("main")
    logger.info("system_start")

    service = create_categorizer_from_env(db_lock=db_lock)

    try:
        stats = await service.run()
        logger.info("final_stats", **stats.model_dump())
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
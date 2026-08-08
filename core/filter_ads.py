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
# 1. CONFIG
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class PcCategoryConfig:
    """Єдине джерело правди для категоризації."""

    obsolete_words: frozenset[str] = field(default_factory=lambda: frozenset({
        "athlon", "ddr2", "ddr1", "ddr 2", "ddr 1", "ddr-2", "ddr-1",
        "core2duo", "core 2 duo", "core 2duo", "f2a55m", "fm2a88", "fm2a85",
        "fm2a75", "fm2a68", "fm2a55", "athlon ii", "athlon x2", "athlon x4",
        "athlon x6", "athlon x8", "775", "lga775", "lga 775", "socket 775",
        "am2", "am2+", "am3", "am3+", "fm1", "fm2", "fm2+",
    }))

    wholesale_words: frozenset[str] = field(default_factory=lambda: frozenset({
        "опт", "оптом", "склад", "пачка", "пачкою", "партией", "партія",
        "комплектом", "кілька шт", "несколько шт", "розпродаж офісу",
        "распродажа офиса",
    }))

    brand_words: frozenset[str] = field(default_factory=lambda: frozenset({
        "dell", "optiplex", "hp", "prodesk", "elitedesk", "workstation",
        "lenovo", "thinkcentre", "fujitsu", "esprimo", "acer veriton", "acer"
    }))

    gaming_words: frozenset[str] = field(default_factory=lambda: frozenset({
        "ігровий", "игровой", "gaming", "rtx", "gtx", "rx 5", "rx 6",
        "rx 7", "rx 4", "геймерский", "геймерський", "ігровий пк", "игровой пк",
    }))

    maining_words: frozenset[str] = field(default_factory=lambda: frozenset({
        "майнинг", "майнінг", "майнер", "майнит",
    }))

    # Мережа / БД
    db_batch_size: int = 100
    db_query_timeout_seconds: float = 10.0

    # Файл статистики
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
    category: str = Field(pattern=r"^(obsolete|wholesale|brand_office|gaming|home_office|maining)$")


class CategoryStats(BaseModel):
    """Звіт по категоріях."""

    obsolete: int = 0
    wholesale: int = 0
    brand_office: int = 0
    gaming: int = 0
    home_office: int = 0
    maining: int = 0

    def increment(self, category: str) -> None:
        if hasattr(self, category):
            setattr(self, category, getattr(self, category) + 1)


# ---------------------------------------------------------------------------
# 3. PURE FUNCTION — детектор категорії
# ---------------------------------------------------------------------------
class PcCategoryDetector:
    """Чистий клас: аналізує текст і повертає категорію. Немає побічних ефектів."""

    def __init__(self, config: PcCategoryConfig) -> None:
        self._config = config

    def detect(self, text: str | None) -> str:
        if not text:
            return "home_office"

        lowered = text.lower()

        if any(word in lowered for word in self._config.obsolete_words):
            return "obsolete"
        if any(word in lowered for word in self._config.wholesale_words):
            return "wholesale"
        if any(word in lowered for word in self._config.brand_words):
            return "brand_office"
        if any(word in lowered for word in self._config.gaming_words):
            return "gaming"
        if any(word in lowered for word in self._config.maining_words):
            return "maining"

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
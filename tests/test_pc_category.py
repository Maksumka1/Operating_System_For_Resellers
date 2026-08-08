"""
Unit-тести для pc_category_refactored.py

Запуск:
    pytest tests/test_pc_category.py -v
    pytest tests/test_pc_category.py -v --cov=pc_category_refactored --cov-report=term-missing
"""

import asyncio
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from unittest.mock import AsyncMock, MagicMock

import pytest

from core.filter_ads import (
    AdRecord,
    CategoryResult,
    CategoryStats,
    JsonStatsRepository,
    PcCategoryConfig,
    PcCategoryDetector,
    PcCategoryService,
    StatsRepository,
)


# ===========================================================================
# 1. PcCategoryDetector — чиста функція
# ===========================================================================
class TestPcCategoryDetector:
    """Тести детектора категорій на основі тексту."""

    @pytest.fixture
    def detector(self) -> PcCategoryDetector:
        return PcCategoryDetector(PcCategoryConfig())

    # --- Пріоритетні категорії ---
    @pytest.mark.parametrize("text", [
        "Продам Athlon x4 + DDR2",
        "Материнка FM2A88 + Athlon II",
        "Сокет 775, Core2Duo, DDR-2",
    ])
    def test_detects_obsolete(self, detector: PcCategoryDetector, text: str) -> None:
        assert detector.detect(text) == "obsolete"

    @pytest.mark.parametrize("text", [
        "Продам оптом 10 системників",
        "Склад, пачкою, партией",
        "Розпродаж офісу, комплектом",
    ])
    def test_detects_wholesale(self, detector: PcCategoryDetector, text: str) -> None:
        assert detector.detect(text) == "wholesale"

    @pytest.mark.parametrize("text", [
        "Dell Optiplex 7020",
        "HP ProDesk 600 G1",
        "Lenovo ThinkCentre M93p",
    ])
    def test_detects_brand_office(self, detector: PcCategoryDetector, text: str) -> None:
        assert detector.detect(text) == "brand_office"

    @pytest.mark.parametrize("text", [
        "Ігровий ПК з RTX 3060",
        "Геймерский комп, GTX 1660",
        "Gaming PC, RX 6600",
    ])
    def test_detects_gaming(self, detector: PcCategoryDetector, text: str) -> None:
        assert detector.detect(text) == "gaming"

    @pytest.mark.parametrize("text", [
        "Майнінг ферма на 6 карт",
        "Майнинг риг, продам",
    ])
    def test_detects_maining(self, detector: PcCategoryDetector, text: str) -> None:
        assert detector.detect(text) == "maining"

    # --- За замовчуванням ---
    @pytest.mark.parametrize("text", [
        "",
        None,
        "   ",
        "Звичайний комп'ютер для дому",
        "Intel i5, 16GB RAM, SSD",
    ])
    def test_defaults_to_home_office(self, detector: PcCategoryDetector, text: str | None) -> None:
        assert detector.detect(text) == "home_office"

    # --- Пріоритет: obsolete > wholesale > brand > gaming > maining ---
    def test_obsolete_beats_gaming(self, detector: PcCategoryDetector) -> None:
        """Якщо в тексті є і obsolete, і gaming — перемагає obsolete (перший у списку)."""
        text = "Athlon x4 + GTX 1080, ігровий"
        assert detector.detect(text) == "obsolete"

    def test_brand_beats_gaming(self, detector: PcCategoryDetector) -> None:
        text = "Dell Optiplex, gaming, rtx"
        assert detector.detect(text) == "brand_office"


# ===========================================================================
# 2. Pydantic Models
# ===========================================================================
class TestAdRecord:
    """Тести валідації моделі оголошення."""

    def test_valid_record(self) -> None:
        record = AdRecord(ad_id=123, title="Test", description="Desc")
        assert record.ad_id == 123
        assert record.full_text == "Test Desc"

    def test_full_text_strips_whitespace(self) -> None:
        record = AdRecord(ad_id=1, title="  Title  ", description="")
        assert record.full_text == "Title"

    def test_ad_id_must_be_positive(self) -> None:
        with pytest.raises(Exception):  # pydantic.ValidationError
            AdRecord(ad_id=0, title="Test")

    def test_missing_fields_use_defaults(self) -> None:
        record = AdRecord(ad_id=1)
        assert record.title == ""
        assert record.description == ""


class TestCategoryResult:
    """Тести моделі результату категоризації."""

    @pytest.mark.parametrize("cat", ["obsolete", "wholesale", "brand_office", "gaming", "home_office", "maining"])
    def test_valid_categories(self, cat: str) -> None:
        result = CategoryResult(ad_id=1, category=cat)
        assert result.category == cat

    def test_invalid_category_rejected(self) -> None:
        with pytest.raises(Exception):
            CategoryResult(ad_id=1, category="invalid")


class TestCategoryStats:
    """Тести агрегатора статистики."""

    def test_all_counters_start_at_zero(self) -> None:
        stats = CategoryStats()
        assert stats.obsolete == 0
        assert stats.home_office == 0

    def test_increment_increases_counter(self) -> None:
        stats = CategoryStats()
        stats.increment("gaming")
        stats.increment("gaming")
        stats.increment("obsolete")
        assert stats.gaming == 2
        assert stats.obsolete == 1
        assert stats.home_office == 0

    def test_model_dump_returns_dict(self) -> None:
        stats = CategoryStats(gaming=5)
        data = stats.model_dump()
        assert data["gaming"] == 5
        assert data["wholesale"] == 0


# ===========================================================================
# 3. PcCategoryService — оркестратор з моками
# ===========================================================================
class TestPcCategoryService:
    """Тести сервісу категоризації ізольовано (з моками репозиторіїв)."""

    @pytest.fixture
    def mock_repo(self) -> MagicMock:
        repo = MagicMock()
        repo.fetch_uncategorized_pcs = AsyncMock(return_value=[])
        repo.update_category_batch = AsyncMock(return_value=0)
        repo.count_active_clean = AsyncMock(return_value=42)
        return repo

    @pytest.fixture
    def mock_stats_repo(self) -> MagicMock:
        repo = MagicMock()
        repo.update_statistics = AsyncMock()
        return repo

    @pytest.fixture
    def detector(self) -> PcCategoryDetector:
        return PcCategoryDetector(PcCategoryConfig())

    @pytest.fixture
    def service(
        self,
        mock_repo: MagicMock,
        detector: PcCategoryDetector,
        mock_stats_repo: MagicMock,
    ) -> PcCategoryService:
        return PcCategoryService(
            repository=mock_repo,
            detector=detector,
            stats_repo=mock_stats_repo,
        )

    @pytest.mark.asyncio
    async def test_empty_list_returns_zero_stats(self, service: PcCategoryService, mock_repo: MagicMock) -> None:
        mock_repo.fetch_uncategorized_pcs.return_value = []
        stats = await service.run()
        assert stats.home_office == 0
        mock_repo.update_category_batch.assert_not_called()

    @pytest.mark.asyncio
    async def test_single_ad_categorized_and_saved(self, service: PcCategoryService, mock_repo: MagicMock) -> None:
        mock_repo.fetch_uncategorized_pcs.return_value = [
            AdRecord(ad_id=1, title="Dell Optiplex", description="")
        ]
        stats = await service.run()

        assert stats.brand_office == 1
        mock_repo.update_category_batch.assert_awaited_once_with("brand_office", [1])
        mock_repo.count_active_clean.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_multiple_ads_grouped_by_category(self, service: PcCategoryService, mock_repo: MagicMock) -> None:
        mock_repo.fetch_uncategorized_pcs.return_value = [
            AdRecord(ad_id=1, title="Dell Optiplex"),
            AdRecord(ad_id=2, title="Dell ProDesk"),
            AdRecord(ad_id=3, title="Ігровий ПК RTX"),
            AdRecord(ad_id=4, title="Звичайний ПК"),
        ]
        stats = await service.run()

        assert stats.brand_office == 2
        assert stats.gaming == 1
        assert stats.home_office == 1

        # Перевіряємо, що batch-виклики були по категоріям
        calls = mock_repo.update_category_batch.await_args_list
        categories_called = {call.args[0] for call in calls}
        assert categories_called == {"brand_office", "gaming", "home_office"}

    @pytest.mark.asyncio
    async def test_stats_written_to_repo(self, service: PcCategoryService, mock_stats_repo: MagicMock) -> None:
        mock_repo = service._repo
        mock_repo.fetch_uncategorized_pcs.return_value = [
            AdRecord(ad_id=1, title="Dell"),
        ]
        await service.run()

        assert mock_stats_repo.update_statistics.await_count == 2
        # Перевіряємо, що categories записано
        cat_call = mock_stats_repo.update_statistics.await_args_list[1]
        assert cat_call.args[0] == "categories"
        assert cat_call.args[1]["brand_office"] == 1

    @pytest.mark.asyncio
    async def test_db_lock_used_when_provided(self, detector: PcCategoryDetector, mock_repo: MagicMock, mock_stats_repo: MagicMock) -> None:
        lock = asyncio.Lock()
        service = PcCategoryService(mock_repo, detector, mock_stats_repo, db_lock=lock)
        mock_repo.fetch_uncategorized_pcs.return_value = [
            AdRecord(ad_id=1, title="Dell"),
        ]
        await service.run()
        # Якщо lock працює — виклик пройшов без deadlock
        mock_repo.update_category_batch.assert_awaited()


# ===========================================================================
# 4. JsonStatsRepository — робота з файловою системою
# ===========================================================================
class TestJsonStatsRepository:
    """Тести запису статистики у JSON через тимчасовий файл."""

    @pytest.fixture
    def stats_file(self, tmp_path: Path) -> Path:
        return tmp_path / "stats.json"

    @pytest.fixture
    def repo(self, stats_file: Path) -> JsonStatsRepository:
        return JsonStatsRepository(stats_file)

    @pytest.mark.asyncio
    async def test_creates_file_if_not_exists(self, repo: JsonStatsRepository, stats_file: Path) -> None:
        assert not stats_file.exists()
        await repo.update_statistics("categories", {"gaming": 5})
        assert stats_file.exists()

    @pytest.mark.asyncio
    async def test_writes_today_section(self, repo: JsonStatsRepository, stats_file: Path) -> None:
        await repo.update_statistics("categories", {"gaming": 5})
        data = json.loads(stats_file.read_text(encoding="utf-8"))
        today = datetime.now(timezone.utc).strftime("%d-%m-%Y")
        assert today in data
        assert data[today]["categories"]["gaming"] == 5

    @pytest.mark.asyncio
    async def test_merges_existing_data(self, repo: JsonStatsRepository, stats_file: Path) -> None:
        today = datetime.now(timezone.utc).strftime("%d-%m-%Y")
        pre_existing = {today: {"categories": {"gaming": 2}, "parsing": {"parsed_total_new": 10}}}
        stats_file.write_text(json.dumps(pre_existing), encoding="utf-8")

        await repo.update_statistics("categories", {"gaming": 5, "obsolete": 1})
        data = json.loads(stats_file.read_text(encoding="utf-8"))
        assert data[today]["categories"]["gaming"] == 5
        assert data[today]["categories"]["obsolete"] == 1
        assert data[today]["parsing"]["parsed_total_new"] == 10  # не затерто

    @pytest.mark.asyncio
    async def test_overwrites_section_metrics(self, repo: JsonStatsRepository, stats_file: Path) -> None:
        today = datetime.now(timezone.utc).strftime("%d-%m-%Y")
        pre_existing = {today: {"filtering": {"defects_found": 3, "filtered_total_active": 100}}}
        stats_file.write_text(json.dumps(pre_existing), encoding="utf-8")

        await repo.update_statistics("filtering", {"filtered_total_active": 200})
        data = json.loads(stats_file.read_text(encoding="utf-8"))
        assert data[today]["filtering"]["filtered_total_active"] == 200
        assert data[today]["filtering"]["defects_found"] == 3  # не змінилось, бо не передано

    @pytest.mark.asyncio
    async def test_handles_corrupted_json(self, repo: JsonStatsRepository, stats_file: Path) -> None:
        stats_file.write_text("not json{{", encoding="utf-8")
        await repo.update_statistics("categories", {"gaming": 1})
        data = json.loads(stats_file.read_text(encoding="utf-8"))
        today = datetime.now(timezone.utc).strftime("%d-%m-%Y")
        assert today in data


# ===========================================================================
# 5. PcCategoryConfig — frozen, незмінна
# ===========================================================================
class TestPcCategoryConfig:
    """Тести конфігурації."""

    def test_config_is_frozen(self) -> None:
        config = PcCategoryConfig()
        with pytest.raises(Exception):  # FrozenInstanceError
            config.db_batch_size = 50  # type: ignore[misc]

    def test_default_batch_size(self) -> None:
        config = PcCategoryConfig()
        assert config.db_batch_size == 100

    def test_custom_words_work(self) -> None:
        custom = PcCategoryConfig(
            gaming_words=frozenset({"rtx", "gtx"}),
            obsolete_words=frozenset(),
            wholesale_words=frozenset(),
            brand_words=frozenset(),
            maining_words=frozenset(),
        )
        detector = PcCategoryDetector(custom)
        assert detector.detect("Відеокарта RTX") == "gaming"
        assert detector.detect("Athlon x4") == "home_office"  # obsolete порожній
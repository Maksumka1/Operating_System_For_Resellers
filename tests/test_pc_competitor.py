"""
Unit-тести для pc_competitor_refactored_v2_1.py

Запуск:
    pytest tests/test_pc_competitor.py -v
"""

import asyncio
from typing import Any
from unittest.mock import AsyncMock, MagicMock

import pytest

from core.competitor_finder import (
    CompetitorConfig,
    CompetitorPriceCalculator,
    CompetitorPriceUpdate,
    PcBuildRecord,
    PcCompetitorService,
    SupabaseAdRepository,
)


# ===========================================================================
# 1. PcBuildRecord
# ===========================================================================
class TestPcBuildRecord:
    """Тести моделі ПК з розпізнаним залізом."""

    def test_full_gpu_cpu(self) -> None:
        """Є і GPU, і CPU — build_key містить обидва через _."""
        rec = PcBuildRecord(ad_id=1, gpu_detected="gtx_1060_3_gb", cpu_detected="i5_6400", price=15000)
        assert rec.build_key == "gtx_1060_3_gb_i5_6400"

    def test_no_gpu_only_cpu(self) -> None:
        """Немає GPU — build_key = '_cpu' (пошук тільки по CPU)."""
        rec = PcBuildRecord(ad_id=2, gpu_detected=None, cpu_detected="i5_6400", price=8000)
        assert rec.build_key == "_i5_6400"

    def test_empty_gpu_string_becomes_none(self) -> None:
        """Порожній рядок GPU → None."""
        rec = PcBuildRecord(ad_id=3, gpu_detected="   ", cpu_detected="i3_10100", price=5000)
        assert rec.gpu_detected is None
        assert rec.build_key == "_i3_10100"

    def test_unknown_gpu_becomes_none(self) -> None:
        """'Unknown GPU' → None (валідатор нормалізує)."""
        rec = PcBuildRecord(ad_id=4, gpu_detected="Unknown GPU", cpu_detected="i5_7500", price=6000)
        assert rec.gpu_detected is None
        assert rec.build_key == "_i5_7500"

    def test_rtx_3050_format(self) -> None:
        """Формат з БД: rtx_3050, i5_6400."""
        rec = PcBuildRecord(ad_id=5, gpu_detected="rtx_3050", cpu_detected="i5_6400", price=12000)
        assert rec.build_key == "rtx_3050_i5_6400"

    def test_cpu_required(self) -> None:
        """Без CPU — ValidationError."""
        with pytest.raises(Exception):
            PcBuildRecord(ad_id=1, gpu_detected="gtx_1060", cpu_detected="", price=1000)

    def test_cpu_cannot_be_unknown(self) -> None:
        """CPU = 'Unknown CPU' — ValidationError."""
        with pytest.raises(Exception):
            PcBuildRecord(ad_id=1, gpu_detected="gtx_1060", cpu_detected="Unknown CPU", price=1000)

    def test_ad_id_must_be_positive(self) -> None:
        with pytest.raises(Exception):
            PcBuildRecord(ad_id=0, gpu_detected="gtx_1060", cpu_detected="i5_6400", price=1000)

    def test_price_must_be_positive(self) -> None:
        with pytest.raises(Exception):
            PcBuildRecord(ad_id=1, gpu_detected="gtx_1060", cpu_detected="i5_6400", price=0)


# ===========================================================================
# 2. CompetitorPriceUpdate
# ===========================================================================
class TestCompetitorPriceUpdate:
    def test_valid_update(self) -> None:
        up = CompetitorPriceUpdate(ad_id=1, competitor_price=12000)
        assert up.ad_id == 1
        assert up.competitor_price == 12000

    def test_price_must_be_positive(self) -> None:
        with pytest.raises(Exception):
            CompetitorPriceUpdate(ad_id=1, competitor_price=0)


# ===========================================================================
# 3. CompetitorPriceCalculator
# ===========================================================================
class TestCompetitorPriceCalculator:
    @pytest.fixture
    def calc(self) -> CompetitorPriceCalculator:
        return CompetitorPriceCalculator()

    def test_empty_list(self, calc: CompetitorPriceCalculator) -> None:
        assert calc.calculate([]) == []

    def test_single_pc(self, calc: CompetitorPriceCalculator) -> None:
        records = [
            PcBuildRecord(ad_id=1, gpu_detected="gtx_1060_3_gb", cpu_detected="i5_6400", price=15000),
        ]
        result = calc.calculate(records)
        assert len(result) == 1
        assert result[0].competitor_price == 15000

    def test_two_same_build_swap_prices(self, calc: CompetitorPriceCalculator) -> None:
        """Два ПК з однаковим GPU+CPU — кожен отримує ціну іншого."""
        records = [
            PcBuildRecord(ad_id=1, gpu_detected="gtx_1060_3_gb", cpu_detected="i5_6400", price=10000),
            PcBuildRecord(ad_id=2, gpu_detected="gtx_1060_3_gb", cpu_detected="i5_6400", price=20000),
        ]
        result = calc.calculate(records)
        by_id = {r.ad_id: r.competitor_price for r in result}
        assert by_id[1] == 20000
        assert by_id[2] == 10000

    def test_gpu_pc_and_no_gpu_pc_are_separate_groups(self, calc: CompetitorPriceCalculator) -> None:
        """
        ПК з gtx_1060+i5_6400 і ПК без GPU+i5_6400 — різні групи.
        Вони НЕ є конкурентами один одному.
        """
        records = [
            PcBuildRecord(ad_id=1, gpu_detected="gtx_1060_3_gb", cpu_detected="i5_6400", price=15000),
            PcBuildRecord(ad_id=2, gpu_detected=None, cpu_detected="i5_6400", price=8000),
        ]
        result = calc.calculate(records)
        by_id = {r.ad_id: r.competitor_price for r in result}
        assert by_id[1] == 15000
        assert by_id[2] == 8000

    def test_two_no_gpu_same_cpu_compete(self, calc: CompetitorPriceCalculator) -> None:
        """Два ПК без GPU, але з однаковим CPU — конкуренти."""
        records = [
            PcBuildRecord(ad_id=1, gpu_detected=None, cpu_detected="i5_6400", price=7000),
            PcBuildRecord(ad_id=2, gpu_detected=None, cpu_detected="i5_6400", price=9000),
        ]
        result = calc.calculate(records)
        by_id = {r.ad_id: r.competitor_price for r in result}
        assert by_id[1] == 9000
        assert by_id[2] == 7000

    def test_different_cpu_separate_groups(self, calc: CompetitorPriceCalculator) -> None:
        """Різні CPU — різні групи навіть з однаковим GPU."""
        records = [
            PcBuildRecord(ad_id=1, gpu_detected="gtx_1060_3_gb", cpu_detected="i5_6400", price=10000),
            PcBuildRecord(ad_id=2, gpu_detected="gtx_1060_3_gb", cpu_detected="i7_7700", price=20000),
        ]
        result = calc.calculate(records)
        by_id = {r.ad_id: r.competitor_price for r in result}
        assert by_id[1] == 10000
        assert by_id[2] == 20000

    def test_three_pcs_average(self, calc: CompetitorPriceCalculator) -> None:
        records = [
            PcBuildRecord(ad_id=1, gpu_detected="gtx_1060_3_gb", cpu_detected="i5_6400", price=10000),
            PcBuildRecord(ad_id=2, gpu_detected="gtx_1060_3_gb", cpu_detected="i5_6400", price=20000),
            PcBuildRecord(ad_id=3, gpu_detected="gtx_1060_3_gb", cpu_detected="i5_6400", price=30000),
        ]
        result = calc.calculate(records)
        by_id = {r.ad_id: r.competitor_price for r in result}
        assert by_id[1] == 25000
        assert by_id[2] == 20000
        assert by_id[3] == 15000


# ===========================================================================
# 4. PcCompetitorService
# ===========================================================================
class TestPcCompetitorService:
    @pytest.fixture
    def mock_repo(self) -> MagicMock:
        repo = MagicMock()
        repo.fetch_pcs_with_hardware = AsyncMock(return_value=[])
        repo.update_competitor_prices = AsyncMock(return_value=0)
        return repo

    @pytest.fixture
    def calc(self) -> CompetitorPriceCalculator:
        return CompetitorPriceCalculator()

    @pytest.fixture
    def config(self) -> CompetitorConfig:
        return CompetitorConfig()

    @pytest.fixture
    def service(self, mock_repo: MagicMock, calc: CompetitorPriceCalculator, config: CompetitorConfig) -> PcCompetitorService:
        return PcCompetitorService(repository=mock_repo, calculator=calc, config=config)

    @pytest.mark.asyncio
    async def test_empty_list(self, service: PcCompetitorService, mock_repo: MagicMock) -> None:
        mock_repo.fetch_pcs_with_hardware.return_value = []
        result = await service.run()
        assert result == []
        mock_repo.update_competitor_prices.assert_not_called()

    @pytest.mark.asyncio
    async def test_successful_run(self, service: PcCompetitorService, mock_repo: MagicMock) -> None:
        mock_repo.fetch_pcs_with_hardware.return_value = [
            PcBuildRecord(ad_id=1, gpu_detected="gtx_1060_3_gb", cpu_detected="i5_6400", price=10000),
            PcBuildRecord(ad_id=2, gpu_detected="gtx_1060_3_gb", cpu_detected="i5_6400", price=20000),
        ]
        result = await service.run()
        assert sorted(result) == [1, 2]
        mock_repo.update_competitor_prices.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_mixed_gpu_and_no_gpu(self, service: PcCompetitorService, mock_repo: MagicMock) -> None:
        mock_repo.fetch_pcs_with_hardware.return_value = [
            PcBuildRecord(ad_id=1, gpu_detected="gtx_1060_3_gb", cpu_detected="i5_6400", price=15000),
            PcBuildRecord(ad_id=2, gpu_detected=None, cpu_detected="i5_6400", price=8000),
            PcBuildRecord(ad_id=3, gpu_detected=None, cpu_detected="i5_6400", price=9000),
        ]
        result = await service.run()
        assert sorted(result) == [1, 2, 3]
        mock_repo.update_competitor_prices.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_db_lock_used(self, mock_repo: MagicMock, calc: CompetitorPriceCalculator, config: CompetitorConfig) -> None:
        lock = asyncio.Lock()
        service = PcCompetitorService(mock_repo, calc, config, db_lock=lock)
        mock_repo.fetch_pcs_with_hardware.return_value = [
            PcBuildRecord(ad_id=1, gpu_detected="gtx_1060_3_gb", cpu_detected="i5_6400", price=10000),
        ]
        await service.run()
        mock_repo.update_competitor_prices.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_config_passed_to_fetch(self, service: PcCompetitorService, mock_repo: MagicMock) -> None:
        mock_repo.fetch_pcs_with_hardware.return_value = []
        await service.run()
        assert isinstance(mock_repo.fetch_pcs_with_hardware.await_args.args[0], CompetitorConfig)


# ===========================================================================
# 5. CompetitorConfig
# ===========================================================================
class TestCompetitorConfig:
    def test_frozen(self) -> None:
        config = CompetitorConfig()
        with pytest.raises(Exception):
            config.min_price = 500  # type: ignore[misc]

    def test_defaults(self) -> None:
        config = CompetitorConfig()
        assert config.min_price == 1000
        assert config.db_batch_size == 100
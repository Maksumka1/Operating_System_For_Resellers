"""
Unit-тести для hardware_evaluator_refactored.py

Запуск:
    pytest tests/test_hardware_evaluator.py -v
"""

import asyncio
from typing import Any
from unittest.mock import AsyncMock, MagicMock

import pytest

from core.hardware_evaluator import (
    DealCalculator,
    DealMetrics,
    DealMetricsUpdate,
    HardwareAdRecord,
    HardwareEvaluatorConfig,
    HardwareEvaluatorService,
)


# ===========================================================================
# 1. DealCalculator — чиста функція
# ===========================================================================
class TestDealCalculator:
    """Тести розрахунку метрик угоди."""

    @pytest.fixture
    def calc(self) -> DealCalculator:
        return DealCalculator(HardwareEvaluatorConfig())

    def test_super_deal(self, calc: DealCalculator) -> None:
        """Економія 25% → 🔥 SUPER DEAL."""
        result = calc.calculate(7500, 10000)
        assert result.deal_status == "🔥 SUPER DEAL"
        assert result.saving_uah == 2500
        assert result.saving_percent == 25

    def test_good_deal(self, calc: DealCalculator) -> None:
        """Економія 12% → ⭐ GOOD DEAL."""
        result = calc.calculate(8800, 10000)
        assert result.deal_status == "⭐ GOOD DEAL"
        assert result.saving_percent == 12

    def test_regular(self, calc: DealCalculator) -> None:
        """Економія 3% → regular."""
        result = calc.calculate(9700, 10000)
        assert result.deal_status == "regular"
        assert result.saving_percent == 3

    def test_overpriced(self, calc: DealCalculator) -> None:
        """Ціна вища на 10% → ❌ OVERPRICED."""
        result = calc.calculate(11000, 10000)
        assert result.deal_status == "❌ OVERPRICED"
        assert result.saving_uah == -1000
        assert result.saving_percent == -10

    def test_exact_threshold_super(self, calc: DealCalculator) -> None:
        """Рівно 20% → 🔥 SUPER DEAL."""
        result = calc.calculate(8000, 10000)
        assert result.deal_status == "🔥 SUPER DEAL"
        assert result.saving_percent == 20

    def test_exact_threshold_overpriced(self, calc: DealCalculator) -> None:
        """Рівно -5% → ❌ OVERPRICED."""
        result = calc.calculate(10500, 10000)
        assert result.deal_status == "❌ OVERPRICED"
        assert result.saving_percent == -5

    def test_clamp_min_percent(self, calc: DealCalculator) -> None:
        """Якщо ціна 0, fair 100 → seller_price стає 1, saving = 99%."""
        result = calc.calculate(0, 100)
        assert result.saving_percent == 99

    def test_clamp_max_percent(self, calc: DealCalculator) -> None:
        """Якщо ціна дуже висока → clamp до -100%."""
        result = calc.calculate(100000, 1)
        assert result.saving_percent == -100

    def test_zero_fair_price_defaults_to_one(self, calc: DealCalculator) -> None:
        """fair_price = 0 → стає 1, щоб уникнути ділення на нуль."""
        result = calc.calculate(0, 0)
        # seller=1, fair=1, saving=0, 0%
        assert result.saving_uah == 0
        assert result.saving_percent == 0
        assert result.deal_status == "regular"

    def test_negative_prices_clamped(self, calc: DealCalculator) -> None:
        """Від'ємні ціни → clamp до 1."""
        result = calc.calculate(-100, -50)
        # seller=1, fair=1
        assert result.saving_uah == 0
        assert result.saving_percent == 0


# ===========================================================================
# 2. HardwareAdRecord
# ===========================================================================
class TestHardwareAdRecord:
    def test_valid_record(self) -> None:
        rec = HardwareAdRecord(ad_id=1, component_name="gtx_1060", price=5000)
        assert rec.ad_id == 1
        assert rec.estimated_fair_price is None
        assert rec.deal_status is None

    def test_with_optional_fields(self) -> None:
        rec = HardwareAdRecord(
            ad_id=1,
            component_name="rtx_3060",
            price=10000,
            estimated_fair_price=12000,
            deal_status="⭐ GOOD DEAL",
        )
        assert rec.estimated_fair_price == 12000

    def test_ad_id_must_be_positive(self) -> None:
        with pytest.raises(Exception):
            HardwareAdRecord(ad_id=0, component_name="gpu", price=100)

    def test_price_must_be_positive(self) -> None:
        with pytest.raises(Exception):
            HardwareAdRecord(ad_id=1, component_name="gpu", price=0)

    def test_component_name_required(self) -> None:
        with pytest.raises(Exception):
            HardwareAdRecord(ad_id=1, component_name="", price=100)


# ===========================================================================
# 3. DealMetrics
# ===========================================================================
class TestDealMetrics:
    def test_valid_statuses(self) -> None:
        for status in ["🔥 SUPER DEAL", "⭐ GOOD DEAL", "❌ OVERPRICED", "regular"]:
            m = DealMetrics(saving_uah=100, saving_percent=10, deal_status=status)
            assert m.deal_status == status

    def test_invalid_status_rejected(self) -> None:
        with pytest.raises(Exception):
            DealMetrics(saving_uah=100, saving_percent=10, deal_status="INVALID")


# ===========================================================================
# 4. HardwareEvaluatorService — оркестратор з моками
# ===========================================================================
class TestHardwareEvaluatorService:
    @pytest.fixture
    def mock_fair_repo(self) -> MagicMock:
        repo = MagicMock()
        repo.fetch_latest_prices = AsyncMock(return_value={})
        return repo

    @pytest.fixture
    def mock_hw_repo(self) -> MagicMock:
        repo = MagicMock()
        repo.fetch_active_hardware = AsyncMock(return_value=[])
        repo.update_deal_metrics_batch = AsyncMock(return_value=0)
        return repo

    @pytest.fixture
    def calc(self) -> DealCalculator:
        return DealCalculator(HardwareEvaluatorConfig())

    @pytest.fixture
    def config(self) -> HardwareEvaluatorConfig:
        return HardwareEvaluatorConfig()

    @pytest.fixture
    def service(
        self,
        mock_fair_repo: MagicMock,
        mock_hw_repo: MagicMock,
        calc: DealCalculator,
        config: HardwareEvaluatorConfig,
    ) -> HardwareEvaluatorService:
        return HardwareEvaluatorService(
            fair_price_repo=mock_fair_repo,
            hardware_repo=mock_hw_repo,
            calculator=calc,
            config=config,
        )

    @pytest.mark.asyncio
    async def test_no_fair_prices_returns_empty(self, service: HardwareEvaluatorService, mock_fair_repo: MagicMock) -> None:
        mock_fair_repo.fetch_latest_prices.return_value = {}
        result = await service.run()
        assert result == []
        mock_hw_repo = service._hw_repo
        mock_hw_repo.fetch_active_hardware.assert_not_called()

    @pytest.mark.asyncio
    async def test_no_ads_returns_empty(self, service: HardwareEvaluatorService, mock_fair_repo: MagicMock, mock_hw_repo: MagicMock) -> None:
        mock_fair_repo.fetch_latest_prices.return_value = {"gtx_1060": 5000}
        mock_hw_repo.fetch_active_hardware.return_value = []
        result = await service.run()
        assert result == []
        mock_hw_repo.update_deal_metrics_batch.assert_not_called()

    @pytest.mark.asyncio
    async def test_updates_calculated_and_saved(self, service: HardwareEvaluatorService, mock_fair_repo: MagicMock, mock_hw_repo: MagicMock) -> None:
        mock_fair_repo.fetch_latest_prices.return_value = {"gtx_1060": 10000}
        mock_hw_repo.fetch_active_hardware.return_value = [
            HardwareAdRecord(ad_id=1, component_name="gtx_1060", price=8000),
        ]
        result = await service.run()
        assert result == [1]
        mock_hw_repo.update_deal_metrics_batch.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_skip_unchanged_records(self, service: HardwareEvaluatorService, mock_fair_repo: MagicMock, mock_hw_repo: MagicMock) -> None:
        """Якщо fair_price і status не змінились — не оновлюємо."""
        mock_fair_repo.fetch_latest_prices.return_value = {"gtx_1060": 10000}
        mock_hw_repo.fetch_active_hardware.return_value = [
            HardwareAdRecord(
                ad_id=1,
                component_name="gtx_1060",
                price=8000,
                estimated_fair_price=10000,
                deal_status="🔥 SUPER DEAL",
            ),
        ]
        result = await service.run()
        assert result == []  # нічого не оновлено
        mock_hw_repo.update_deal_metrics_batch.assert_not_called()

    @pytest.mark.asyncio
    async def test_skip_missing_component(self, service: HardwareEvaluatorService, mock_fair_repo: MagicMock, mock_hw_repo: MagicMock) -> None:
        """Якщо component_name немає в fair_prices — skip."""
        mock_fair_repo.fetch_latest_prices.return_value = {"gtx_1060": 10000}
        mock_hw_repo.fetch_active_hardware.return_value = [
            HardwareAdRecord(ad_id=1, component_name="rtx_4090", price=50000),
        ]
        result = await service.run()
        assert result == []

    @pytest.mark.asyncio
    async def test_multiple_ads(self, service: HardwareEvaluatorService, mock_fair_repo: MagicMock, mock_hw_repo: MagicMock) -> None:
        mock_fair_repo.fetch_latest_prices.return_value = {
            "gtx_1060": 10000,
            "rtx_3060": 20000,
        }
        mock_hw_repo.fetch_active_hardware.return_value = [
            HardwareAdRecord(ad_id=1, component_name="gtx_1060", price=8800),
            HardwareAdRecord(ad_id=2, component_name="rtx_3060", price=21000),
            HardwareAdRecord(ad_id=3, component_name="gtx_1060", price=10000),
        ]
        result = await service.run()
        assert sorted(result) == [1, 2, 3]
        mock_hw_repo.update_deal_metrics_batch.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_db_lock_used(self, mock_fair_repo: MagicMock, mock_hw_repo: MagicMock, calc: DealCalculator, config: HardwareEvaluatorConfig) -> None:
        lock = asyncio.Lock()
        service = HardwareEvaluatorService(mock_fair_repo, mock_hw_repo, calc, config, db_lock=lock)
        mock_fair_repo.fetch_latest_prices.return_value = {"gtx_1060": 10000}
        mock_hw_repo.fetch_active_hardware.return_value = [
            HardwareAdRecord(ad_id=1, component_name="gtx_1060", price=8000),
        ]
        await service.run()
        mock_hw_repo.update_deal_metrics_batch.assert_awaited_once()


# ===========================================================================
# 5. HardwareEvaluatorConfig
# ===========================================================================
class TestHardwareEvaluatorConfig:
    def test_frozen(self) -> None:
        config = HardwareEvaluatorConfig()
        with pytest.raises(Exception):
            config.min_price = 50  # type: ignore[misc]

    def test_defaults(self) -> None:
        config = HardwareEvaluatorConfig()
        assert config.min_price == 100
        assert config.db_batch_size == 100
        assert config.super_deal_threshold == 15.0
        assert "gpu" in config.item_types
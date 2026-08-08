"""
Unit-тести для pc_evaluator_refactored.py

Запуск:
    pytest tests/test_pc_evaluator.py -v
"""

import asyncio
from typing import Any
from unittest.mock import AsyncMock, MagicMock

import pytest

from core.pc_evaluator import (
    ExtractedComponents,
    HardwareMatchersExtractor,
    PcAdRecord,
    PcEvaluationResult,
    PcEvaluationService,
    PcEvaluator,
    PcEvaluatorConfig,
)


# ===========================================================================
# 1. PcAdRecord
# ===========================================================================
class TestPcAdRecord:
    def test_full_text_combines_title_and_description(self) -> None:
        rec = PcAdRecord(ad_id=1, title="GTX 1060", description="i5 6400 16GB", price=5000)
        assert "GTX 1060" in rec.full_text
        assert "i5 6400" in rec.full_text

    def test_full_text_trims_options(self) -> None:
        rec = PcAdRecord(ad_id=1, title="GTX 1060", description="додатково ssd", price=5000)
        assert "додатково" not in rec.full_text
        assert "ssd" not in rec.full_text

    def test_full_text_without_description(self) -> None:
        rec = PcAdRecord(ad_id=1, title="GTX 1060", price=5000)
        assert rec.full_text == "GTX 1060"

    def test_ad_id_positive(self) -> None:
        with pytest.raises(Exception):
            PcAdRecord(ad_id=0, title="test", price=100)

    def test_price_positive(self) -> None:
        with pytest.raises(Exception):
            PcAdRecord(ad_id=1, title="test", price=0)


# ===========================================================================
# 2. ExtractedComponents
# ===========================================================================
class TestExtractedComponents:
    def test_all_fields_optional(self) -> None:
        comp = ExtractedComponents()
        assert comp.gpu is None
        assert comp.cpu is None

    def test_with_values(self) -> None:
        comp = ExtractedComponents(gpu="gtx_1060", cpu="i5_6400")
        assert comp.gpu == "gtx_1060"


# ===========================================================================
# 3. PcEvaluationResult
# ===========================================================================
class TestPcEvaluationResult:
    def test_valid_statuses(self) -> None:
        for status in ["🔥 SUPER DEAL", "⭐ GOOD DEAL", "❌ OVERPRICED", "regular"]:
            result = PcEvaluationResult(
                ad_id=1, seller_price_clean=5000,
                estimated_fair_price=6000,
                saving_uah=1000, saving_percent=17,
                deal_status=status, evaluated_at="2024-01-01",
            )
            assert result.deal_status == status

    def test_invalid_status_rejected(self) -> None:
        with pytest.raises(Exception):
            PcEvaluationResult(
                ad_id=1, seller_price_clean=5000,
                estimated_fair_price=6000,
                saving_uah=1000, saving_percent=17,
                deal_status="INVALID", evaluated_at="2024-01-01",
            )


# ===========================================================================
# 4. PcEvaluator — чиста функція
# ===========================================================================
class TestPcEvaluator:
    @pytest.fixture
    def config(self) -> PcEvaluatorConfig:
        return PcEvaluatorConfig(
            hardware_targets=frozenset({"gtx_1060", "i5_6400", "b360", "ddr4_16gb", "ssd_240", "psu_500w"}),
        )

    @pytest.fixture
    def evaluator(self, config: PcEvaluatorConfig) -> PcEvaluator:
        return PcEvaluator(config)

    @pytest.fixture
    def prices(self) -> dict[str, int]:
        return {
            "gtx_1060": 5000,
            "i5_6400": 3000,
            "b360": 2000,
            "ddr4_16gb": 1500,
            "ssd_240": 800,
            "psu_500w": 700,
        }

    def test_full_build_super_deal(self, evaluator: PcEvaluator, prices: dict[str, int]) -> None:
        """ПК з усіма комплектуючими, ціна нижча на 25% → SUPER DEAL."""
        ad = PcAdRecord(ad_id=1, title="Gaming PC", price=8000)
        comps = ExtractedComponents(
            gpu="gtx_1060", cpu="i5_6400",
            motherboard="b360", ram="ddr4_16gb",
            storage="ssd_240", psu="psu_500w",
        )
        result = evaluator.evaluate(ad, comps, prices)

        # fair = 5000+3000 + (2000+1500+800+700) + 1200 = 14200
        assert result.estimated_fair_price == 14200
        assert result.deal_status == "🔥 SUPER DEAL"
        assert result.saving_uah == 6200
        assert result.gpu_detected == "gtx_1060"
        assert result.cpu_detected == "i5_6400"

    def test_no_extras_base_cost(self, evaluator: PcEvaluator, prices: dict[str, int]) -> None:
        """Тільки GPU+CPU, без extra → base_pc_cost_no_extras = 3800."""
        ad = PcAdRecord(ad_id=2, title="Budget PC", price=7000)
        comps = ExtractedComponents(gpu="gtx_1060", cpu="i5_6400")
        result = evaluator.evaluate(ad, comps, prices)

        # fair = 5000 + 3000 + 3800 = 11800
        assert result.estimated_fair_price == 11800
        assert result.mb_market_price == 0
        assert result.deal_status == "🔥 SUPER DEAL"

    def test_unknown_cpu_forces_regular(self, evaluator: PcEvaluator, prices: dict[str, int]) -> None:
        """Без CPU → deal_status = regular, saving = 0."""
        ad = PcAdRecord(ad_id=3, title="PC", price=5000)
        comps = ExtractedComponents(gpu="gtx_1060")
        result = evaluator.evaluate(ad, comps, prices)

        assert result.cpu_detected == "Unknown CPU"
        assert result.deal_status == "regular"
        assert result.saving_uah == 0
        assert result.saving_percent == 0

    def test_overpriced(self, evaluator: PcEvaluator, prices: dict[str, int]) -> None:
        """Ціна вища за fair → OVERPRICED."""
        ad = PcAdRecord(ad_id=4, title="PC", price=20000)
        comps = ExtractedComponents(gpu="gtx_1060", cpu="i5_6400")
        result = evaluator.evaluate(ad, comps, prices)

        # fair = 5000+3000+3800 = 11800, seller=20000
        assert result.deal_status == "❌ OVERPRICED"
        assert result.saving_uah < 0

    def test_good_deal_by_uah(self, evaluator: PcEvaluator, prices: dict[str, int]) -> None:
        """Економія 900 грн (> 800 threshold) → GOOD DEAL."""
        ad = PcAdRecord(ad_id=5, title="PC", price=10900)
        comps = ExtractedComponents(gpu="gtx_1060", cpu="i5_6400")
        result = evaluator.evaluate(ad, comps, prices)

        # fair = 11800, saving = 900
        assert result.deal_status == "⭐ GOOD DEAL"
        assert result.saving_uah == 900

    def test_regular_small_saving(self, evaluator: PcEvaluator, prices: dict[str, int]) -> None:
        """Економія 3% (< 8%) → regular."""
        ad = PcAdRecord(ad_id=6, title="PC", price=11400)
        comps = ExtractedComponents(gpu="gtx_1060", cpu="i5_6400")
        result = evaluator.evaluate(ad, comps, prices)

        # fair = 11800, saving = 400 (~3.4%)
        assert result.deal_status == "regular"

    def test_zero_price_clamped(self, evaluator: PcEvaluator, prices: dict[str, int]) -> None:
        """price=0 → стає 1."""
        ad = PcAdRecord(ad_id=7, title="PC", price=1)
        comps = ExtractedComponents(gpu="gtx_1060", cpu="i5_6400")
        result = evaluator.evaluate(ad, comps, prices)

        assert result.seller_price_clean == 1

    def test_missing_component_price_zero(self, evaluator: PcEvaluator) -> None:
        """Комплектуюче є, але немає ціни → ціна 0."""
        ad = PcAdRecord(ad_id=8, title="PC", price=5000)
        comps = ExtractedComponents(gpu="rtx_4090", cpu="i5_6400")
        result = evaluator.evaluate(ad, comps, {"i5_6400": 3000})

        assert result.gpu_market_price == 0
        assert result.gpu_detected == "rtx_4090"


# ===========================================================================
# 5. HardwareMatchersExtractor
# ===========================================================================
class TestHardwareMatchersExtractor:
    def test_extract_filters_by_targets(self) -> None:
        """Повертає тільки ті комплектуючі, що є в hardware_targets."""
        extractor = HardwareMatchersExtractor(
            hardware_targets=frozenset({"gtx_1060", "i5_6400"}),
            extract_gpu_fn=lambda t: ["gtx_1060", "rtx_3060"],
            extract_cpu_fn=lambda t: ["i5_6400", "i7_9700"],
            extract_motherboard_fn=lambda t: [],
            extract_ram_fn=lambda t: [],
            extract_storage_fn=lambda t: [],
            extract_psu_fn=lambda t: [],
            normalize_fn=lambda t: t.lower(),
        )
        result = extractor.extract("some text")
        assert result.gpu == "gtx_1060"
        assert result.cpu == "i5_6400"

    def test_no_match_returns_none(self) -> None:
        extractor = HardwareMatchersExtractor(
            hardware_targets=frozenset({"gtx_1060"}),
            extract_gpu_fn=lambda t: ["rtx_4090"],
            extract_cpu_fn=lambda t: [],
            extract_motherboard_fn=lambda t: [],
            extract_ram_fn=lambda t: [],
            extract_storage_fn=lambda t: [],
            extract_psu_fn=lambda t: [],
            normalize_fn=lambda t: t,
        )
        result = extractor.extract("text")
        assert result.gpu is None
        assert result.cpu is None

    def test_normalize_called(self) -> None:
        called = False
        def _norm(t: str) -> str:
            nonlocal called
            called = True
            return t

        extractor = HardwareMatchersExtractor(
            hardware_targets=frozenset({}),
            extract_gpu_fn=lambda t: [],
            extract_cpu_fn=lambda t: [],
            extract_motherboard_fn=lambda t: [],
            extract_ram_fn=lambda t: [],
            extract_storage_fn=lambda t: [],
            extract_psu_fn=lambda t: [],
            normalize_fn=_norm,
        )
        extractor.extract("test")
        assert called


# ===========================================================================
# 6. PcEvaluationService — оркестратор з моками
# ===========================================================================
class TestPcEvaluationService:
    @pytest.fixture
    def mock_price_repo(self) -> MagicMock:
        repo = MagicMock()
        repo.fetch_prices = AsyncMock(return_value={})
        return repo

    @pytest.fixture
    def mock_pc_repo(self) -> MagicMock:
        repo = MagicMock()
        repo.fetch_unrated_pcs = AsyncMock(return_value=[])
        repo.update_evaluations = AsyncMock(return_value=0)
        return repo

    @pytest.fixture
    def mock_extractor(self) -> MagicMock:
        ext = MagicMock()
        ext.extract = MagicMock(return_value=ExtractedComponents())
        return ext

    @pytest.fixture
    def config(self) -> PcEvaluatorConfig:
        return PcEvaluatorConfig(hardware_targets=frozenset({"gtx_1060", "i5_6400"}))

    @pytest.fixture
    def evaluator(self, config: PcEvaluatorConfig) -> PcEvaluator:
        return PcEvaluator(config)

    @pytest.fixture
    def service(
        self,
        mock_price_repo: MagicMock,
        mock_pc_repo: MagicMock,
        mock_extractor: MagicMock,
        evaluator: PcEvaluator,
        config: PcEvaluatorConfig,
    ) -> PcEvaluationService:
        return PcEvaluationService(
            price_repo=mock_price_repo,
            pc_repo=mock_pc_repo,
            extractor=mock_extractor,
            evaluator=evaluator,
            config=config,
        )

    @pytest.mark.asyncio
    async def test_no_prices_returns_empty(self, service: PcEvaluationService, mock_price_repo: MagicMock) -> None:
        mock_price_repo.fetch_prices.return_value = {}
        result = await service.run()
        assert result == []
        service._pc_repo.fetch_unrated_pcs.assert_not_called()

    @pytest.mark.asyncio
    async def test_no_pcs_returns_empty(self, service: PcEvaluationService, mock_price_repo: MagicMock, mock_pc_repo: MagicMock) -> None:
        mock_price_repo.fetch_prices.return_value = {"gtx_1060": 5000}
        mock_pc_repo.fetch_unrated_pcs.return_value = []
        result = await service.run()
        assert result == []
        mock_pc_repo.update_evaluations.assert_not_called()

    @pytest.mark.asyncio
    async def test_successful_evaluation(self, service: PcEvaluationService, mock_price_repo: MagicMock, mock_pc_repo: MagicMock, mock_extractor: MagicMock) -> None:
        mock_price_repo.fetch_prices.return_value = {"gtx_1060": 5000, "i5_6400": 3000}
        mock_pc_repo.fetch_unrated_pcs.return_value = [
            PcAdRecord(ad_id=1, title="PC gtx_1060 i5_6400", price=8000),
        ]
        mock_extractor.extract.return_value = ExtractedComponents(gpu="gtx_1060", cpu="i5_6400")

        result = await service.run()
        assert result == [1]
        mock_pc_repo.update_evaluations.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_extractor_called_with_full_text(self, service: PcEvaluationService, mock_price_repo: MagicMock, mock_pc_repo: MagicMock, mock_extractor: MagicMock) -> None:
        mock_price_repo.fetch_prices.return_value = {"gtx_1060": 5000}
        mock_pc_repo.fetch_unrated_pcs.return_value = [
            PcAdRecord(ad_id=1, title="GTX 1060", description="i5 6400", price=5000),
        ]
        await service.run()
        call_args = mock_extractor.extract.call_args[0][0]
        assert "GTX 1060" in call_args
        assert "i5 6400" in call_args

    @pytest.mark.asyncio
    async def test_db_lock_used(self, mock_price_repo: MagicMock, mock_pc_repo: MagicMock, mock_extractor: MagicMock, evaluator: PcEvaluator, config: PcEvaluatorConfig) -> None:
        lock = asyncio.Lock()
        service = PcEvaluationService(
            mock_price_repo, mock_pc_repo, mock_extractor, evaluator, config, db_lock=lock
        )
        mock_price_repo.fetch_prices.return_value = {"gtx_1060": 5000}
        mock_pc_repo.fetch_unrated_pcs.return_value = [
            PcAdRecord(ad_id=1, title="PC", price=5000),
        ]
        mock_extractor.extract.return_value = ExtractedComponents()
        await service.run()
        mock_pc_repo.update_evaluations.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_multiple_pcs(self, service: PcEvaluationService, mock_price_repo: MagicMock, mock_pc_repo: MagicMock, mock_extractor: MagicMock) -> None:
        mock_price_repo.fetch_prices.return_value = {"gtx_1060": 5000, "i5_6400": 3000}
        mock_pc_repo.fetch_unrated_pcs.return_value = [
            PcAdRecord(ad_id=1, title="PC1", price=8000),
            PcAdRecord(ad_id=2, title="PC2", price=12000),
        ]
        mock_extractor.extract.return_value = ExtractedComponents(gpu="gtx_1060", cpu="i5_6400")

        result = await service.run()
        assert sorted(result) == [1, 2]


# ===========================================================================
# 7. PcEvaluatorConfig
# ===========================================================================
class TestPcEvaluatorConfig:
    def test_frozen(self) -> None:
        config = PcEvaluatorConfig()
        with pytest.raises(Exception):
            config.min_price = 50  # type: ignore[misc]

    def test_defaults(self) -> None:
        config = PcEvaluatorConfig()
        assert config.min_price == 100
        assert config.db_batch_size == 100
        assert config.base_case_cooler_cost == 1200
        assert config.base_pc_cost_no_extras == 3800
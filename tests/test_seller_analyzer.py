"""
Unit-тести для seller_analyzer_refactored.py

Запуск:
    pytest tests/test_seller_analyzer.py -v
"""

import asyncio
from typing import Any
from unittest.mock import AsyncMock, MagicMock

import pytest

from core.seller_analyzer import (
    CurlCffiOlxApiClient,
    RatingParser,
    RiskClassifier,
    SellerAnalysisResult,
    SellerAnalysisService,
    SellerAnalyzerConfig,
    SellerAnalyzerWorker,
    SellerApiData,
    SellerRawData,
    SellerTypeClassifier,
    YearExtractor,
)


# ===========================================================================
# 1. RatingParser
# ===========================================================================
class TestRatingParser:
    def test_valid_rating(self) -> None:
        stars, has = RatingParser.parse("4.5/5.0 (120 оцінок)")
        assert stars == 4.5
        assert has is True

    def test_no_rating(self) -> None:
        stars, has = RatingParser.parse("немає оцінок")
        assert stars == 0.0
        assert has is False

    def test_empty_string(self) -> None:
        stars, has = RatingParser.parse("")
        assert stars == 0.0
        assert has is False

    def test_none(self) -> None:
        stars, has = RatingParser.parse(None)  # type: ignore[arg-type]
        assert stars == 0.0
        assert has is False

    def test_integer_rating(self) -> None:
        stars, has = RatingParser.parse("5/5.0 (1 оцінка)")
        assert stars == 5.0
        assert has is True


# ===========================================================================
# 2. YearExtractor
# ===========================================================================
class TestYearExtractor:
    def test_year_in_text(self) -> None:
        assert YearExtractor.extract("Зареєстрований у 2019 році") == 2019

    def test_no_year(self) -> None:
        assert YearExtractor.extract("Немає року") is None

    def test_none(self) -> None:
        assert YearExtractor.extract(None) is None

    def test_old_year(self) -> None:
        assert YearExtractor.extract("1999 рік") == 1999

    def test_multiple_years_first_taken(self) -> None:
        assert YearExtractor.extract("2015-2020") == 2015


# ===========================================================================
# 3. RiskClassifier
# ===========================================================================
class TestRiskClassifier:
    @pytest.fixture
    def classifier(self) -> RiskClassifier:
        return RiskClassifier(SellerAnalyzerConfig())

    def test_safe(self, classifier: RiskClassifier) -> None:
        assert classifier.classify(deals=25, stars=4.5, has_rating=True, age_years=3) == "safe"

    def test_safe_boundary_deals(self, classifier: RiskClassifier) -> None:
        # deals=20, stars=4.0, age=3 → safe
        assert classifier.classify(deals=20, stars=4.0, has_rating=True, age_years=3) == "safe"

    def test_safe_boundary_age_exact_2(self, classifier: RiskClassifier) -> None:
        # age=2, age > 2 is False → not safe
        # deals=20, stars=4.0, age=2 → neutral? deals>=20, stars>=4.0, age>=2 → neutral
        assert classifier.classify(deals=20, stars=4.0, has_rating=True, age_years=2) == "neutral"

    def test_neutral(self, classifier: RiskClassifier) -> None:
        # deals=15, stars=3.5, age=2 → neutral
        assert classifier.classify(deals=15, stars=3.5, has_rating=True, age_years=2) == "neutral"

    def test_neutral_boundary(self, classifier: RiskClassifier) -> None:
        # deals=10, stars=3.1, age=2 → neutral
        assert classifier.classify(deals=10, stars=3.1, has_rating=True, age_years=2) == "neutral"

    def test_suspicious_low_deals(self, classifier: RiskClassifier) -> None:
        assert classifier.classify(deals=5, stars=4.5, has_rating=True, age_years=3) == "suspicious"

    def test_suspicious_low_stars(self, classifier: RiskClassifier) -> None:
        assert classifier.classify(deals=25, stars=2.0, has_rating=True, age_years=3) == "suspicious"

    def test_suspicious_young_account(self, classifier: RiskClassifier) -> None:
        assert classifier.classify(deals=25, stars=4.5, has_rating=True, age_years=1) == "suspicious"

    def test_suspicious_no_rating(self, classifier: RiskClassifier) -> None:
        # has_rating=False → stars treated as 0.0
        assert classifier.classify(deals=25, stars=0.0, has_rating=False, age_years=3) == "suspicious"

    def test_suspicious_none_age(self, classifier: RiskClassifier) -> None:
        # age_years=None → treated as 0
        assert classifier.classify(deals=25, stars=4.5, has_rating=True, age_years=None) == "suspicious"


# ===========================================================================
# 4. SellerTypeClassifier
# ===========================================================================
class TestSellerTypeClassifier:
    @pytest.fixture
    def classifier(self) -> SellerTypeClassifier:
        return SellerTypeClassifier(SellerAnalyzerConfig())

    def test_shop_by_flag(self, classifier: SellerTypeClassifier) -> None:
        assert classifier.classify(is_shop_raw=True, deals=5, stars=3.0, has_rating=True) == "shop"

    def test_shop_by_deals_and_stars(self, classifier: SellerTypeClassifier) -> None:
        # deals > 50 AND stars >= 4.0
        assert classifier.classify(is_shop_raw=False, deals=55, stars=4.5, has_rating=True) == "shop"

    def test_reseller(self, classifier: SellerTypeClassifier) -> None:
        # NOT shop AND deals > 30
        assert classifier.classify(is_shop_raw=False, deals=35, stars=3.5, has_rating=True) == "reseller"

    def test_private_person(self, classifier: SellerTypeClassifier) -> None:
        assert classifier.classify(is_shop_raw=False, deals=5, stars=4.5, has_rating=True) == "private_person"

    def test_shop_deals_boundary(self, classifier: SellerTypeClassifier) -> None:
        # deals=50, not > 50 → not shop by deals
        assert classifier.classify(is_shop_raw=False, deals=50, stars=4.5, has_rating=True) == "reseller"

    def test_reseller_boundary(self, classifier: SellerTypeClassifier) -> None:
        # deals=30, not > 30 → private_person
        assert classifier.classify(is_shop_raw=False, deals=30, stars=4.5, has_rating=True) == "private_person"

    def test_no_rating_stars_zero(self, classifier: SellerTypeClassifier) -> None:
        # has_rating=False → stars=0, deals=55 → reseller (not shop because stars < 4.0)
        assert classifier.classify(is_shop_raw=False, deals=55, stars=0.0, has_rating=False) == "reseller"


# ===========================================================================
# 5. Pydantic Models
# ===========================================================================
class TestSellerRawData:
    def test_valid(self) -> None:
        s = SellerRawData(ad_id=1, seller_id="123", seller_uuid="abc")
        assert s.seller_id == "123"

    def test_optional_fields(self) -> None:
        s = SellerRawData(ad_id=1)
        assert s.seller_id is None
        assert s.seller_created_at is None

    def test_ad_id_positive(self) -> None:
        with pytest.raises(Exception):
            SellerRawData(ad_id=0)


class TestSellerApiData:
    def test_defaults(self) -> None:
        d = SellerApiData()
        assert d.successful_deals == 0
        assert d.rating_str == "немає оцінок"


class TestSellerAnalysisResult:
    def test_valid_risk(self) -> None:
        for risk in ["safe", "neutral", "suspicious"]:
            r = SellerAnalysisResult(
                ad_id=1, successful_deals=10,
                seller_rating="4/5.0", seller_type="shop", seller_risk=risk,
            )
            assert r.seller_risk == risk

    def test_valid_type(self) -> None:
        for t in ["shop", "reseller", "private_person"]:
            r = SellerAnalysisResult(
                ad_id=1, successful_deals=10,
                seller_rating="4/5.0", seller_type=t, seller_risk="safe",
            )
            assert r.seller_type == t

    def test_invalid_risk(self) -> None:
        with pytest.raises(Exception):
            SellerAnalysisResult(
                ad_id=1, successful_deals=10,
                seller_rating="4/5.0", seller_type="shop", seller_risk="unknown",
            )

    def test_invalid_type(self) -> None:
        with pytest.raises(Exception):
            SellerAnalysisResult(
                ad_id=1, successful_deals=10,
                seller_rating="4/5.0", seller_type="hacker", seller_risk="safe",
            )


# ===========================================================================
# 6. CurlCffiOlxApiClient — _is_valid_id
# ===========================================================================
class TestCurlCffiOlxApiClient:
    @pytest.fixture
    def client(self) -> CurlCffiOlxApiClient:
        mock_session = MagicMock()
        config = SellerAnalyzerConfig()
        return CurlCffiOlxApiClient(mock_session, config)

    def test_valid_id(self, client: CurlCffiOlxApiClient) -> None:
        assert client._is_valid_id("12345") is True
        assert client._is_valid_id("abc-def") is True

    def test_empty(self, client: CurlCffiOlxApiClient) -> None:
        assert client._is_valid_id("") is False
        assert client._is_valid_id(None) is False

    def test_failed(self, client: CurlCffiOlxApiClient) -> None:
        assert client._is_valid_id("failed") is False
        assert client._is_valid_id("None") is False
        assert client._is_valid_id("null") is False

    def test_whitespace(self, client: CurlCffiOlxApiClient) -> None:
        assert client._is_valid_id("   ") is False


# ===========================================================================
# 7. SellerAnalyzerWorker — з моканим API
# ===========================================================================
class TestSellerAnalyzerWorker:
    @pytest.fixture
    def config(self) -> SellerAnalyzerConfig:
        return SellerAnalyzerConfig()

    @pytest.fixture
    def worker(self, config: SellerAnalyzerConfig) -> SellerAnalyzerWorker:
        mock_api = MagicMock()
        mock_api.fetch_delivery_deals = AsyncMock(return_value=25)
        mock_api.fetch_seller_rating = AsyncMock(return_value="4.5/5.0 (100 оцінок)")

        risk = RiskClassifier(config)
        seller_type = SellerTypeClassifier(config)
        year = YearExtractor()
        parser = RatingParser()

        return SellerAnalyzerWorker(mock_api, risk, seller_type, year, parser, config)

    @pytest.mark.asyncio
    async def test_analyze_safe_shop(self, worker: SellerAnalyzerWorker) -> None:
        seller = SellerRawData(
            ad_id=1,
            seller_id="123",
            seller_uuid="abc",
            seller_created_at="2019-01-01",
            seller_type_raw="shop",
        )
        semaphore = asyncio.Semaphore(1)
        result = await worker.analyze(seller, semaphore)

        assert result is not None
        assert result.ad_id == 1
        assert result.successful_deals == 25
        assert result.seller_rating == "4.5/5.0 (100 оцінок)"
        assert result.seller_risk == "safe"
        assert result.seller_type == "shop"

    @pytest.mark.asyncio
    async def test_analyze_suspicious_private(self, worker: SellerAnalyzerWorker, config: SellerAnalyzerConfig) -> None:
        mock_api = MagicMock()
        mock_api.fetch_delivery_deals = AsyncMock(return_value=5)
        mock_api.fetch_seller_rating = AsyncMock(return_value="немає оцінок")

        risk = RiskClassifier(config)
        seller_type = SellerTypeClassifier(config)
        w = SellerAnalyzerWorker(mock_api, risk, seller_type, YearExtractor(), RatingParser(), config)

        seller = SellerRawData(
            ad_id=2,
            seller_id="456",
            seller_uuid="def",
            seller_created_at="2024-01-01",
            seller_type_raw="private",
        )
        result = await w.analyze(seller, asyncio.Semaphore(1))

        assert result is not None
        assert result.seller_risk == "suspicious"
        assert result.seller_type == "private_person"
        assert result.successful_deals == 5

    @pytest.mark.asyncio
    async def test_analyze_reseller(self, worker: SellerAnalyzerWorker, config: SellerAnalyzerConfig) -> None:
        mock_api = MagicMock()
        mock_api.fetch_delivery_deals = AsyncMock(return_value=35)
        mock_api.fetch_seller_rating = AsyncMock(return_value="3.5/5.0 (50 оцінок)")

        risk = RiskClassifier(config)
        seller_type = SellerTypeClassifier(config)
        w = SellerAnalyzerWorker(mock_api, risk, seller_type, YearExtractor(), RatingParser(), config)

        seller = SellerRawData(
            ad_id=3,
            seller_id="789",
            seller_uuid="ghi",
            seller_created_at="2020-01-01",
            seller_type_raw="private",
        )
        result = await w.analyze(seller, asyncio.Semaphore(1))

        assert result is not None
        assert result.seller_type == "reseller"
        assert result.seller_risk == "neutral"


# ===========================================================================
# 8. SellerAnalysisService — оркестратор з моками
# ===========================================================================
class TestSellerAnalysisService:
    @pytest.fixture
    def mock_repo(self) -> MagicMock:
        repo = MagicMock()
        repo.fetch_unchecked_sellers = AsyncMock(return_value=[])
        repo.update_seller_analysis_batch = AsyncMock(return_value=0)
        return repo

    @pytest.fixture
    def mock_worker(self) -> MagicMock:
        worker = MagicMock()
        worker.analyze = AsyncMock(return_value=None)
        return worker

    @pytest.fixture
    def config(self) -> SellerAnalyzerConfig:
        return SellerAnalyzerConfig()

    @pytest.fixture
    def service(self, mock_repo: MagicMock, mock_worker: MagicMock, config: SellerAnalyzerConfig) -> SellerAnalysisService:
        return SellerAnalysisService(
            repository=mock_repo,
            worker=mock_worker,
            config=config,
        )

    @pytest.mark.asyncio
    async def test_no_sellers_returns_empty(self, service: SellerAnalysisService, mock_repo: MagicMock) -> None:
        mock_repo.fetch_unchecked_sellers.return_value = []
        result = await service.run()
        assert result == []
        mock_repo.update_seller_analysis_batch.assert_not_called()

    @pytest.mark.asyncio
    async def test_successful_run(self, service: SellerAnalysisService, mock_repo: MagicMock, mock_worker: MagicMock) -> None:
        mock_repo.fetch_unchecked_sellers.return_value = [
            SellerRawData(ad_id=1, seller_id="123"),
        ]
        mock_worker.analyze.return_value = SellerAnalysisResult(
            ad_id=1, successful_deals=25,
            seller_rating="4.5/5.0", seller_type="shop", seller_risk="safe",
        )
        result = await service.run()
        assert result == [1]
        mock_repo.update_seller_analysis_batch.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_skip_failed_analyses(self, service: SellerAnalysisService, mock_repo: MagicMock, mock_worker: MagicMock) -> None:
        mock_repo.fetch_unchecked_sellers.return_value = [
            SellerRawData(ad_id=1, seller_id="123"),
            SellerRawData(ad_id=2, seller_id="456"),
        ]
        mock_worker.analyze.side_effect = [
            SellerAnalysisResult(
                ad_id=1, successful_deals=10,
                seller_rating="3/5.0", seller_type="private_person", seller_risk="neutral",
            ),
            None,  # другий провалився
        ]
        result = await service.run()
        assert result == [1]
        mock_repo.update_seller_analysis_batch.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_db_lock_used(self, mock_repo: MagicMock, mock_worker: MagicMock, config: SellerAnalyzerConfig) -> None:
        lock = asyncio.Lock()
        service = SellerAnalysisService(mock_repo, mock_worker, config, db_lock=lock)
        mock_repo.fetch_unchecked_sellers.return_value = [
            SellerRawData(ad_id=1, seller_id="123"),
        ]
        mock_worker.analyze.return_value = SellerAnalysisResult(
            ad_id=1, successful_deals=10,
            seller_rating="3/5.0", seller_type="private_person", seller_risk="neutral",
        )
        await service.run()
        mock_repo.update_seller_analysis_batch.assert_awaited_once()


# ===========================================================================
# 9. SellerAnalyzerConfig
# ===========================================================================
class TestSellerAnalyzerConfig:
    def test_frozen(self) -> None:
        config = SellerAnalyzerConfig()
        with pytest.raises(Exception):
            config.concurrent_requests = 10  # type: ignore[misc]

    def test_defaults(self) -> None:
        config = SellerAnalyzerConfig()
        assert config.concurrent_requests == 5
        assert config.request_timeout == 8.0
        assert config.safe_deals_threshold == 20
        assert config.shop_deals_threshold == 50
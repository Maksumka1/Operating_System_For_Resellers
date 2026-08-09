"""
Unit-тести для parser_hardware_production.py

Запуск:
    pytest tests/test_parser_hardware.py -v
"""

import asyncio
import time
from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from parsers.parser_hardware import (
    AdsRepository,
    EnvConfig,
    MetricsCollector,
    OlxGraphqlParser,
    ParsedAd,
    ParserConfig,
    SupabaseAdsRepository,
    TracingContext,
    _get_logger,
    clean_url,
    detect_socket,
    is_broken_ad,
    match_ad_to_hardware_target,
)


# ===========================================================================
# 1. EnvConfig
# ===========================================================================
class TestEnvConfig:
    def test_valid(self) -> None:
        cfg = EnvConfig(
            supabase_url="https://test.supabase.co",
            supabase_secret_key="sk_test_1234567890abcdef",
            olx_proxy_url="http://proxy:8080",
        )
        assert cfg.supabase_url == "https://test.supabase.co"
        assert cfg.request_timeout == 12
        assert cfg.pages_to_parse == 1

    def test_url_must_be_https(self) -> None:
        with pytest.raises(ValueError, match="https://"):
            EnvConfig(supabase_url="http://insecure.com", supabase_secret_key="key")

    def test_defaults(self) -> None:
        cfg = EnvConfig(supabase_url="https://x.co", supabase_secret_key="k")
        assert cfg.request_timeout == 12
        assert cfg.max_retries == 3
        assert cfg.pages_to_parse == 1

    def test_pages_to_parse_bounds(self) -> None:
        with pytest.raises(ValueError):
            EnvConfig(supabase_url="https://x.co", supabase_secret_key="k", pages_to_parse=0)
        with pytest.raises(ValueError):
            EnvConfig(supabase_url="https://x.co", supabase_secret_key="k", pages_to_parse=25)


# ===========================================================================
# 2. ParsedAd — Pydantic валідація
# ===========================================================================
class TestParsedAd:
    def test_valid_minimal(self) -> None:
        ad = ParsedAd(
            url="https://olx.ua/123",
            title="RTX 4090",
            price=50000,
            item_type="gpu",
            component_name="rtx_4090",
            parsed_date="2024-01-01",
        )
        assert ad.price == 50000
        assert ad.has_defects == 0

    def test_price_bounds(self) -> None:
        with pytest.raises(ValueError):
            ParsedAd(url="https://x", title="t", price=-1, item_type="gpu", component_name="g", parsed_date="2024-01-01")
        with pytest.raises(ValueError):
            ParsedAd(url="https://x", title="t", price=2_000_000_000, item_type="gpu", component_name="g", parsed_date="2024-01-01")

    def test_bundle_components_as_dict(self) -> None:
        ad = ParsedAd(
            url="https://olx.ua/456",
            title="Bundle",
            price=10000,
            item_type="bundle",
            component_name="bundle_i5_7500_h270",
            parsed_date="2024-01-01",
            bundle_components={"cpu": "i5_7500", "motherboard": "h270", "gpu": None},
        )
        assert ad.bundle_components["cpu"] == "i5_7500"
        assert ad.bundle_components["gpu"] is None

    def test_missing_required_fields(self) -> None:
        with pytest.raises(ValueError):
            ParsedAd(url="", title="t", price=100, item_type="gpu", component_name="g", parsed_date="2024-01-01")


# ===========================================================================
# 3. Pure Functions — is_broken_ad
# ===========================================================================
class TestIsBrokenAd:
    def test_broken_keywords(self) -> None:
        assert is_broken_ad("Відеокарта неробоча на запчастини") is True
        assert is_broken_ad("Продаю з дефектом, артефакти") is True
        assert is_broken_ad("Не працює, на ремонт") is True

    def test_clean_override(self) -> None:
        assert is_broken_ad("Без дефектів, без ремонту, ідеальний стан") is False
        assert is_broken_ad("Не був у ремонті, все ок") is False

    def test_empty_text(self) -> None:
        assert is_broken_ad("") is False
        assert is_broken_ad(None) is False  # type: ignore[arg-type]

    def test_false_positive_prevention(self) -> None:
        # "не був у ремонті" → clean_patterns має прибрати "ремонт"
        assert is_broken_ad("Відеокарта, не була у ремонті, стан ідеальний") is False


# ===========================================================================
# 4. Pure Functions — clean_url
# ===========================================================================
class TestCleanUrl:
    def test_removes_query_params(self) -> None:
        assert clean_url("https://olx.ua/d/uk/obyavlenie/123?utm_source=xxx") == "https://olx.ua/d/uk/obyavlenie/123"

    def test_keeps_path(self) -> None:
        assert clean_url("https://olx.ua/d/uk/obyavlenie/rtx-4090-abc123") == "https://olx.ua/d/uk/obyavlenie/rtx-4090-abc123"

    def test_no_params(self) -> None:
        assert clean_url("https://olx.ua/123") == "https://olx.ua/123"


# ===========================================================================
# 5. Pure Functions — detect_socket
# ===========================================================================
class TestDetectSocket:
    def test_socket_in_title(self) -> None:
        # DI: передаємо sockets напряму, без patch
        result = detect_socket(
            "Процесор Intel lga1151",
            "",
            "i5_9400f",
            sockets=["lga1151", "am4"],
            chipset_map={},
        )
        assert result == "lga1151"

    def test_chipset_fallback(self) -> None:
        with patch("parsers.parser_hardware.SOCKETS", []):
            with patch("parsers.parser_hardware.CHIPSET_TO_SOCKET", {"b360": "lga1151v2"}):
                result = detect_socket("Материнська плата", "", "b360")
                assert result == "lga1151v2"

    def test_no_match(self) -> None:
        with patch("parsers.parser_hardware.SOCKETS", []):
            with patch("parsers.parser_hardware.CHIPSET_TO_SOCKET", {}):
                assert detect_socket("Текст", "", "unknown") is None


# ===========================================================================
# 6. MetricsCollector
# ===========================================================================
class TestMetricsCollector:
    @pytest.fixture
    def metrics(self) -> MetricsCollector:
        return MetricsCollector()

    @pytest.mark.asyncio
    async def test_inc(self, metrics: MetricsCollector) -> None:
        await metrics.inc("test_counter", 5)
        await metrics.inc("test_counter", 3)
        snap = metrics.snapshot()
        assert snap["counters"]["test_counter"] == 8

    @pytest.mark.asyncio
    async def test_time(self, metrics: MetricsCollector) -> None:
        await metrics.time("test_timer", 0.5)
        await metrics.time("test_timer", 1.5)
        snap = metrics.snapshot()
        assert snap["timers"]["test_timer"]["count"] == 2
        assert snap["timers"]["test_timer"]["avg_ms"] == 1000.0

    @pytest.mark.asyncio
    async def test_concurrent_increments(self, metrics: MetricsCollector) -> None:
        async def worker() -> None:
            for _ in range(100):
                await metrics.inc("concurrent")

        await asyncio.gather(*[worker() for _ in range(5)])
        snap = metrics.snapshot()
        assert snap["counters"]["concurrent"] == 500


# ===========================================================================
# 7. SupabaseAdsRepository
# ===========================================================================
class TestSupabaseAdsRepository:
    @pytest.fixture
    def mock_client(self) -> MagicMock:
        return MagicMock()

    @pytest.fixture
    def repo(self, mock_client: MagicMock) -> SupabaseAdsRepository:
        return SupabaseAdsRepository(
            client=mock_client,
            metrics=MetricsCollector(),
            trace=TracingContext(),
        )

    @pytest.mark.asyncio
    async def test_fetch_seen_urls(self, repo: SupabaseAdsRepository, mock_client: MagicMock) -> None:
        mock_client.table.return_value.select.return_value.execute.return_value = MagicMock(
            data=[{"url": "https://a"}, {"url": "https://b"}]
        )
        result = await repo.fetch_seen_urls()
        assert result == {"https://a", "https://b"}

    @pytest.mark.asyncio
    async def test_fetch_seen_urls_error_returns_empty(self, repo: SupabaseAdsRepository, mock_client: MagicMock) -> None:
        mock_client.table.side_effect = RuntimeError("DB down")
        result = await repo.fetch_seen_urls()
        assert result == set()

    @pytest.mark.asyncio
    async def test_upsert_ads(self, repo: SupabaseAdsRepository, mock_client: MagicMock) -> None:
        ads = [
            ParsedAd(url="https://x", title="GPU", price=100, item_type="gpu", component_name="gtx_1060", parsed_date="2024-01-01"),
        ]
        mock_client.table.return_value.upsert.return_value.execute.return_value = MagicMock()
        count = await repo.upsert_ads(ads)
        assert count == 1
        mock_client.table.return_value.upsert.assert_called_once()

    @pytest.mark.asyncio
    async def test_upsert_empty_list(self, repo: SupabaseAdsRepository, mock_client: MagicMock) -> None:
        assert await repo.upsert_ads([]) == 0
        mock_client.table.assert_not_called()


# ===========================================================================
# 8. OlxGraphqlParser — з моками
# ===========================================================================
class TestOlxGraphqlParser:
    @pytest.fixture
    def mock_repo(self) -> MagicMock:
        repo = MagicMock(spec=AdsRepository)
        repo.fetch_seen_urls = AsyncMock(return_value=set())
        repo.upsert_ads = AsyncMock(return_value=0)
        return repo

    @pytest.fixture
    def parser(self, mock_repo: MagicMock) -> OlxGraphqlParser:
        env = EnvConfig(
            supabase_url="https://test.supabase.co",
            supabase_secret_key="test_key",
            pages_to_parse=1,
        )
        return OlxGraphqlParser(
            env=env,
            parser_config=ParserConfig(),
            metrics=MetricsCollector(),
            trace=TracingContext(),
            repo=mock_repo,
        )

    @pytest.mark.asyncio
    async def test_parse_all_with_shutdown(self, parser: OlxGraphqlParser, mock_repo: MagicMock) -> None:
        """Shutdown event має зупинити парсинг до мережевих запитів."""
        shutdown = asyncio.Event()
        shutdown.set()
        result = await parser.parse_all(shutdown_event=shutdown)
        assert result == []

    @pytest.mark.asyncio
    async def test_try_parse_item_valid(self, parser: OlxGraphqlParser) -> None:
        """_try_parse_item розпізнає відеокарту з типовим лістингом."""
        item = {
            "id": "123456789",
            "title": "Відеокарта MSI GeForce RTX 3060 12GB Gaming X",
            "url": "https://www.olx.ua/d/uk/obyavlenie/123",
            "description": "В ідеальному стані, не майнила",
            "params": [
                {"key": "price", "value": {"value": 8500, "currency": "UAH"}},
                {"key": "subcategory", "value": {"key": "videokarty"}},
            ],
            "location": {"city": {"name": "Київ"}},
            "created_time": "2024-01-15T10:00:00Z",
            "photos": [{"link": "https://img.olx.ua/1_{width}x{height}"}],
            "user": {"id": 999, "uuid": "abc", "name": "Seller", "created": "2020-05-01"},
            "business": False,
        }

        # Мокаємо HARDWARE_TARGETS для тесту
        with patch("parsers.parser_hardware.HARDWARE_TARGETS", {
            "rtx_3060": {"item_type": "gpu", "compiled_pattern": None},
        }):
            with patch("parsers.parser_hardware.extract_gpu", return_value=["rtx_3060"]):
                result = parser._try_parse_item(item, "videokarty", "gpu", {})

        assert result is not None
        assert result.component_name == "rtx_3060"
        assert result.price == 8500
        assert result.city == "Київ"
        assert result.has_defects == 0
        assert result.seller_type == "private_person"

    @pytest.mark.asyncio
    async def test_try_parse_item_duplicate_url_skipped(self, parser: OlxGraphqlParser) -> None:
        """URL вже в seen_urls → пропускаємо."""
        parser._seen_urls.add("https://www.olx.ua/d/uk/obyavlenie/duplicate")
        item = {
            "id": "1",
            "title": "RTX 4090",
            "url": "https://www.olx.ua/d/uk/obyavlenie/duplicate",
            "params": [{"key": "subcategory", "value": {"key": "videokarty"}}],
        }
        result = parser._try_parse_item(item, "videokarty", "gpu", {})
        assert result is None

    @pytest.mark.asyncio
    async def test_try_parse_item_no_match(self, parser: OlxGraphqlParser) -> None:
        """Невідома модель → None."""
        item = {
            "id": "1",
            "title": "Якийсь рандомний текст",
            "url": "https://olx.ua/1",
            "params": [{"key": "subcategory", "value": {"key": "videokarty"}}],
        }
        with patch("parsers.parser_hardware.extract_gpu", return_value=[]):
            result = parser._try_parse_item(item, "videokarty", "gpu", {})
        assert result is None

    @pytest.mark.asyncio
    async def test_try_parse_item_broken_ad(self, parser: OlxGraphqlParser) -> None:
        """Оголошення з дефектом → has_defects=1."""
        item = {
            "id": "1",
            "title": "Відеокарта неробоча на запчастини",
            "url": "https://olx.ua/1",
            "description": "Артефакти на екрані",
            "params": [
                {"key": "price", "value": {"value": 500}},
                {"key": "subcategory", "value": {"key": "videokarty"}},
            ],
            "location": {},
            "created_time": "",
            "photos": [],
            "user": {},
        }
        with patch("parsers.parser_hardware.extract_gpu", return_value=["gtx_1060"]):
            with patch("parsers.parser_hardware.HARDWARE_TARGETS", {"gtx_1060": {"item_type": "gpu"}}):
                result = parser._try_parse_item(item, "videokarty", "gpu", {})
        assert result is not None
        assert result.has_defects == 1

    @pytest.mark.asyncio
    async def test_try_parse_item_bundle(self, parser: OlxGraphqlParser) -> None:
        """Bundle-оголошення → bundle_components як dict."""
        item = {
            "id": "1",
            "title": "Комплект i5 7500 + H270 + 16GB RAM",
            "url": "https://olx.ua/1",
            "description": "",
            "params": [
                {"key": "price", "value": {"value": 4000}},
                {"key": "subcategory", "value": {"key": "materinskie-platy"}},
            ],
            "location": {"city": {"name": "Львів"}},
            "created_time": "2024-01-01T00:00:00Z",
            "photos": [],
            "user": {},
        }
        bundle_data = {
            "bundle_key": "bundle_i5_7500_h270",
            "components": {"cpu": "i5_7500", "motherboard": "h270", "gpu": None},
        }
        with patch("parsers.parser_hardware.detect_bundle_components", return_value=bundle_data):
            result = parser._try_parse_item(item, "materinskie-platy", "motherboard", {})

        assert result is not None
        assert result.item_type == "bundle"
        assert result.bundle_components == {"cpu": "i5_7500", "motherboard": "h270", "gpu": None}


# ===========================================================================
# 9. TracingContext
# ===========================================================================
class TestTracingContext:
    def test_trace_id_format(self) -> None:
        trace = TracingContext()
        assert len(trace.trace_id) == 16
        assert trace.trace_id.isalnum()

    def test_unique_per_instance(self) -> None:
        t1 = TracingContext()
        time.sleep(0.01)
        t2 = TracingContext()
        assert t1.trace_id != t2.trace_id


# ===========================================================================
# 10. Integration-style: parser flow with mocked session
# ===========================================================================
class TestParserIntegration:
    @pytest.mark.asyncio
    async def test_full_flow_mocked(self) -> None:
        """Інтеграційний тест: мокаємо весь HTTP-шар."""
        mock_repo = MagicMock(spec=AdsRepository)
        mock_repo.fetch_seen_urls = AsyncMock(return_value=set())
        mock_repo.upsert_ads = AsyncMock(return_value=0)

        env = EnvConfig(
            supabase_url="https://test.supabase.co",
            supabase_secret_key="test",
            pages_to_parse=1,
        )
        parser = OlxGraphqlParser(
            env=env,
            parser_config=ParserConfig(),
            metrics=MetricsCollector(),
            trace=TracingContext(),
            repo=mock_repo,
        )

        # Мокаємо AsyncSession контекстний менеджер
        mock_session = AsyncMock()
        mock_session.get = AsyncMock(return_value=AsyncMock(status_code=200))


        # resp.json() — синхронний метод у curl_cffi, тому MagicMock
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json = MagicMock(return_value={
            "data": {
                "clientCompatibleListings": {
                    "data": [
                        {
                            "id": "111",
                            "title": "RTX 3060 12GB",
                            "url": "https://olx.ua/111",
                            "description": "Нова",
                            "params": [
                                {"key": "price", "value": {"value": 9000}},
                                {"key": "subcategory", "value": {"key": "videokarty"}},
                            ],
                            "location": {"city": {"name": "Одеса"}},
                            "created_time": "2024-01-01T00:00:00Z",
                            "photos": [],
                            "user": {},
                        }
                    ]
                }
            }
        })
        mock_session.post = AsyncMock(return_value=mock_resp)
        mock_session.__aenter__ = AsyncMock(return_value=mock_session)
        mock_session.__aexit__ = AsyncMock(return_value=False)

        with patch("parsers.parser_hardware.AsyncSession", return_value=mock_session):
            with patch("parsers.parser_hardware.HARDWARE_TARGETS", {
                "rtx_3060": {"item_type": "gpu"},
            }):
                with patch("parsers.parser_hardware.extract_gpu", return_value=["rtx_3060"]):
                    result = await parser.parse_all()

        # Має бути 1 розпізнане оголошення
        assert len(result) == 1
        assert result[0].component_name == "rtx_3060"
        assert result[0].price == 9000
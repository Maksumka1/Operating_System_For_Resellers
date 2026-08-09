"""
Unit-тести для parser_pc_production.py (Основний функціонал)

Запуск:
    pytest tests/test_parser_pc.py -v
"""

import asyncio
from datetime import datetime
from pathlib import Path
from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from parsers.parser import (
    EnvConfig,
    JsonStatsRepository,
    MetricsCollector,
    OlxPcParser,
    ParsedPc,
    PcAdsRepository,
    PcParserConfig,
    SupabasePcAdsRepository,
    TracingContext,
    _get_logger,
    clean_url,
    extract_price,
    is_real_pc,
)


# ===========================================================================
# 1. EnvConfig
# ===========================================================================
class TestEnvConfig:
    def test_valid(self) -> None:
        cfg = EnvConfig(
            supabase_url="https://test.supabase.co",
            supabase_secret_key="sk_test_1234567890abcdef",
        )
        assert cfg.request_timeout == 15
        assert cfg.pages_to_parse == 1

    def test_url_must_be_https(self) -> None:
        with pytest.raises(ValueError, match="https://"):
            EnvConfig(supabase_url="http://insecure.com", supabase_secret_key="key")

    def test_pages_bounds(self) -> None:
        with pytest.raises(ValueError):
            EnvConfig(supabase_url="https://x.co", supabase_secret_key="k", pages_to_parse=0)
        with pytest.raises(ValueError):
            EnvConfig(supabase_url="https://x.co", supabase_secret_key="k", pages_to_parse=25)


# ===========================================================================
# 2. ParsedPc — Pydantic
# ===========================================================================
class TestParsedPc:
    def test_valid(self) -> None:
        pc = ParsedPc(
            url="https://olx.ua/123",
            title="Ігровий ПК",
            parsed_date="2024-01-01",
            price=15000,
        )
        assert pc.item_type == "pc"
        assert pc.price == 15000

    def test_price_bounds(self) -> None:
        with pytest.raises(ValueError):
            ParsedPc(url="https://x", title="t", parsed_date="2024-01-01", price=-1)
        with pytest.raises(ValueError):
            ParsedPc(url="https://x", title="t", parsed_date="2024-01-01", price=2_000_000_000)

    def test_defaults(self) -> None:
        pc = ParsedPc(url="https://x", title="t", parsed_date="2024-01-01")
        assert pc.status == "active"
        assert pc.seller_type == "private_person"
        assert pc.component_name is None


# ===========================================================================
# 3. Pure Functions — is_real_pc (CORE LOGIC)
# ===========================================================================
class TestIsRealPc:
    @pytest.fixture
    def cfg(self) -> PcParserConfig:
        return PcParserConfig()

    def test_valid_pc(self, cfg: PcParserConfig) -> None:
        assert is_real_pc("Ігровий ПК Ryzen 5", cfg) == (True, "valid_pc")
        assert is_real_pc("Системний блок Intel i5", cfg) == (True, "valid_pc")
        assert is_real_pc("Комп'ютер для роботи", cfg) == (True, "valid_pc")
        assert is_real_pc("Ноутбук Dell", cfg) == (True, "valid_pc")

    def test_banned_word_without_indicator(self, cfg: PcParserConfig) -> None:
        # "материнська плата" без слова "комп'ютер/ПК/системний блок"
        result = is_real_pc("Материнська плата ASUS", cfg)
        assert result[0] is False
        assert "banned_word" in result[1]

    def test_banned_word_with_pc_indicator(self, cfg: PcParserConfig) -> None:
        # "материнська плата" АЛЕ є "комп'ютер" — це ПК з материнкою
        result = is_real_pc("Комп'ютер + материнська плата ASUS", cfg)
        assert result[0] is True

    def test_starts_with_banned_word(self, cfg: PcParserConfig) -> None:
        result = is_real_pc("Материнська плата для ПК", cfg)
        assert result[0] is False
        assert "starts_with" in result[1]

    def test_empty_title(self, cfg: PcParserConfig) -> None:
        assert is_real_pc("", cfg) == (False, "empty_title")

    def test_ssd_alone_filtered(self, cfg: PcParserConfig) -> None:
        result = is_real_pc("SSD Kingston 500GB", cfg)
        assert result[0] is False

    def test_pc_with_ssd_allowed(self, cfg: PcParserConfig) -> None:
        result = is_real_pc("Ігровий ПК з SSD Kingston", cfg)
        assert result[0] is True


# ===========================================================================
# 4. Pure Functions — extract_price & clean_url
# ===========================================================================
class TestExtractPrice:
    def test_int(self) -> None:
        assert extract_price(15000) == 15000

    def test_string_with_currency(self) -> None:
        assert extract_price("15 000 грн") == 15000

    def test_string_with_dots(self) -> None:
        assert extract_price("15.000") == 15000

    def test_empty(self) -> None:
        assert extract_price("") == 0

    def test_none(self) -> None:
        assert extract_price(None) == 0  # type: ignore[arg-type]


class TestCleanUrl:
    def test_removes_query(self) -> None:
        assert clean_url("https://olx.ua/123?utm=xxx") == "https://olx.ua/123"

    def test_no_change(self) -> None:
        assert clean_url("https://olx.ua/123") == "https://olx.ua/123"


# ===========================================================================
# 5. MetricsCollector
# ===========================================================================
class TestMetricsCollector:
    @pytest.fixture
    def metrics(self) -> MetricsCollector:
        return MetricsCollector()

    @pytest.mark.asyncio
    async def test_inc_and_time(self, metrics: MetricsCollector) -> None:
        await metrics.inc("test", 5)
        await metrics.time("timer", 0.5)
        snap = metrics.snapshot()
        assert snap["counters"]["test"] == 5
        assert snap["timers"]["timer"]["count"] == 1

    @pytest.mark.asyncio
    async def test_concurrent(self, metrics: MetricsCollector) -> None:
        async def worker() -> None:
            for _ in range(50):
                await metrics.inc("counter")
        await asyncio.gather(*[worker() for _ in range(4)])
        assert metrics.snapshot()["counters"]["counter"] == 200


# ===========================================================================
# 6. Repository — SupabasePcAdsRepository
# ===========================================================================
class TestSupabasePcAdsRepository:
    @pytest.fixture
    def mock_client(self) -> MagicMock:
        return MagicMock()

    @pytest.fixture
    def repo(self, mock_client: MagicMock) -> SupabasePcAdsRepository:
        return SupabasePcAdsRepository(
            client=mock_client,
            metrics=MetricsCollector(),
            trace=TracingContext(),
        )

    @pytest.mark.asyncio
    async def test_fetch_urls(self, repo: SupabasePcAdsRepository, mock_client: MagicMock) -> None:
        mock_client.table.return_value.select.return_value.execute.return_value = MagicMock(
            data=[{"url": "https://a"}, {"url": "https://b"}]
        )
        result = await repo.fetch_seen_urls()
        assert result == {"https://a", "https://b"}

    @pytest.mark.asyncio
    async def test_fetch_error_returns_empty(self, repo: SupabasePcAdsRepository, mock_client: MagicMock) -> None:
        mock_client.table.side_effect = RuntimeError("DB down")
        result = await repo.fetch_seen_urls()
        assert result == set()

    @pytest.mark.asyncio
    async def test_upsert(self, repo: SupabasePcAdsRepository, mock_client: MagicMock) -> None:
        pcs = [ParsedPc(url="https://x", title="PC", parsed_date="2024-01-01", price=100)]
        mock_client.table.return_value.upsert.return_value.execute.return_value = MagicMock()
        assert await repo.upsert_pcs(pcs) == 1

    @pytest.mark.asyncio
    async def test_upsert_empty(self, repo: SupabasePcAdsRepository) -> None:
        assert await repo.upsert_pcs([]) == 0


# ===========================================================================
# 7. JsonStatsRepository
# ===========================================================================
class TestJsonStatsRepository:
    @pytest.mark.asyncio
    async def test_update_creates_file(self, tmp_path: Path) -> None:
        stats_file = tmp_path / "stats.json"
        repo = JsonStatsRepository(stats_file, TracingContext())
        await repo.update("parsing", {"parsed_total_new": 42})
        assert stats_file.exists()
        import json
        data = json.loads(stats_file.read_text())
        today = datetime.now().strftime("%d-%m-%Y")
        assert data[today]["parsing"]["parsed_total_new"] == 42


# ===========================================================================
# 8. OlxPcParser — Core Orchestrator
# ===========================================================================
class TestOlxPcParser:
    @pytest.fixture
    def mock_repo(self) -> MagicMock:
        repo = MagicMock(spec=PcAdsRepository)
        repo.fetch_seen_urls = AsyncMock(return_value=set())
        repo.upsert_pcs = AsyncMock(return_value=0)
        return repo

    @pytest.fixture
    def parser(self, mock_repo: MagicMock) -> OlxPcParser:
        env = EnvConfig(
            supabase_url="https://test.supabase.co",
            supabase_secret_key="test",
            pages_to_parse=1,
        )
        return OlxPcParser(
            env=env,
            cfg=PcParserConfig(),
            metrics=MetricsCollector(),
            trace=TracingContext(),
            repo=mock_repo,
            stats_repo=MagicMock(spec=JsonStatsRepository),
        )

    @pytest.mark.asyncio
    async def test_shutdown_stops_parsing(self, parser: OlxPcParser) -> None:
        shutdown = asyncio.Event()
        shutdown.set()
        result = await parser.parse_all(shutdown_event=shutdown)
        assert result == []

    def test_try_parse_item_valid(self, parser: OlxPcParser) -> None:
        item = {
            "id": "123",
            "title": "Ігровий ПК RTX 3060",
            "url": "https://olx.ua/123",
            "description": "Новий комп'ютер",
            "params": [{"key": "price", "value": {"value": 15000}}],
            "location": {"city": {"name": "Київ"}},
            "created_time": "2024-01-01T10:00:00Z",
            "photos": [{"link": "https://img.olx.ua/1_{width}x{height}"}],
            "user": {"id": 1, "uuid": "abc", "name": "Seller", "created": "2020-01-01"},
            "business": False,
        }
        result = parser._try_parse_item(item)
        assert result is not None
        assert result.title == "Ігровий ПК RTX 3060"
        assert result.price == 15000
        assert result.city == "Київ"
        assert result.seller_type == "private_person"
        assert result.item_type == "pc"

    def test_try_parse_item_duplicate_skipped(self, parser: OlxPcParser) -> None:
        parser._seen_urls.add("https://olx.ua/duplicate")
        item = {
            "id": "1",
            "title": "ПК",
            "url": "https://olx.ua/duplicate",
            "params": [],
            "location": {},
            "user": {},
        }
        assert parser._try_parse_item(item) is None

    def test_try_parse_item_not_a_pc_filtered(self, parser: OlxPcParser) -> None:
        item = {
            "id": "1",
            "title": "SSD Kingston 500GB",  # banned word, no PC indicator
            "url": "https://olx.ua/1",
            "params": [],
            "location": {},
            "user": {},
        }
        assert parser._try_parse_item(item) is None

    def test_try_parse_item_bundle_word_but_pc_allowed(self, parser: OlxPcParser) -> None:
        # "материнська плата" АЛЕ з "системний блок" — це ПК
        item = {
            "id": "1",
            "title": "Системний блок + материнська плата ASUS",
            "url": "https://olx.ua/1",
            "params": [{"key": "price", "value": {"value": 5000}}],
            "location": {"city": {"name": "Львів"}},
            "created_time": "2024-01-01T00:00:00Z",
            "photos": [],
            "user": {},
        }
        result = parser._try_parse_item(item)
        assert result is not None
        assert result.price == 5000

    def test_try_parse_item_business_seller(self, parser: OlxPcParser) -> None:
        item = {
            "id": "1",
            "title": "ПК для офісу",
            "url": "https://olx.ua/1",
            "params": [{"key": "price", "value": {"value": 8000}}],
            "location": {},
            "created_time": "",
            "photos": [],
            "user": {},
            "business": True,
        }
        result = parser._try_parse_item(item)
        assert result is not None
        assert result.seller_type == "shop"

    def test_try_parse_item_no_url(self, parser: OlxPcParser) -> None:
        item = {"id": "1", "title": "ПК", "url": "", "params": [], "location": {}, "user": {}}
        assert parser._try_parse_item(item) is None

    def test_try_parse_item_relative_url(self, parser: OlxPcParser) -> None:
        item = {
            "id": "1",
            "title": "ПК",
            "url": "/d/uk/obyavlenie/123",
            "params": [{"key": "price", "value": {"value": 1000}}],
            "location": {},
            "created_time": "",
            "photos": [],
            "user": {},
        }
        result = parser._try_parse_item(item)
        assert result is not None
        assert result.url == "https://www.olx.ua/d/uk/obyavlenie/123"


# ===========================================================================
# 9. TracingContext
# ===========================================================================
class TestTracingContext:
    def test_format(self) -> None:
        trace = TracingContext()
        assert len(trace.trace_id) == 16
        assert trace.trace_id.isalnum()

    def test_unique(self) -> None:
        t1 = TracingContext()
        import time
        time.sleep(0.01)
        t2 = TracingContext()
        assert t1.trace_id != t2.trace_id
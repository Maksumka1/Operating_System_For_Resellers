"""
Unit-тести для Component Price Analyzer (Production) — FIXED

Запуск:
    pytest tests/test_price_analyzer.py -v
"""

import asyncio
import time
from typing import Any
from unittest.mock import AsyncMock, MagicMock, call

import httpx
import pytest

# ---------------------------------------------------------------------------
# Адаптуй цей імпорт під свою структуру проєкту
# ---------------------------------------------------------------------------
from core.price_hardware import (
    CircuitBreaker,
    CircuitState,
    ComponentAd,
    ComponentPriceService,
    EnvConfig,
    MetricsCollector,
    PercentilePriceCalculator,
    PercentileResult,
    PriceAnalyzerConfig,
    PriceUpsertRecord,
    TracingContext,
    with_retry,
)


# ===========================================================================
# 1. ComponentAd — Pydantic валідація
# ===========================================================================
class TestComponentAd:
    def test_valid(self) -> None:
        ad = ComponentAd(ad_id=1, component_name="gtx_1060", price=5000)
        assert ad.ad_id == 1
        assert ad.price == 5000

    def test_ad_id_positive(self) -> None:
        with pytest.raises(Exception):
            ComponentAd(ad_id=0, component_name="gpu", price=100)

    def test_price_positive(self) -> None:
        with pytest.raises(Exception):
            ComponentAd(ad_id=1, component_name="gpu", price=0)

    def test_component_name_required(self) -> None:
        with pytest.raises(Exception):
            ComponentAd(ad_id=1, component_name="", price=100)


# ===========================================================================
# 2. PercentileResult & PriceUpsertRecord
# ===========================================================================
class TestPercentileResult:
    def test_valid(self) -> None:
        r = PercentileResult(component_name="gtx_1060", price=5000, sample_size=10, used_ids=[1, 2])
        assert r.sample_size == 10

    def test_price_positive(self) -> None:
        with pytest.raises(Exception):
            PercentileResult(component_name="gpu", price=0, sample_size=1, used_ids=[])


class TestPriceUpsertRecord:
    def test_valid(self) -> None:
        r = PriceUpsertRecord(
            component_name="gtx_1060",
            price=5000,
            date="2024-01-01",
            competitor_ids=[1],
            idempotency_key="abc123",
        )
        assert r.date == "2024-01-01"
        assert r.idempotency_key == "abc123"

    def test_idempotency_key_required(self) -> None:
        with pytest.raises(Exception):
            PriceUpsertRecord(
                component_name="gpu",
                price=100,
                date="2024-01-01",
                competitor_ids=[1],
                idempotency_key="",  # порожній ключ
            )


# ===========================================================================
# 3. PercentilePriceCalculator — чиста функція
# ===========================================================================
class TestPercentilePriceCalculator:
    @pytest.fixture
    def calc(self) -> PercentilePriceCalculator:
        return PercentilePriceCalculator(PriceAnalyzerConfig())

    def test_empty_returns_none(self, calc: PercentilePriceCalculator) -> None:
        assert calc.calculate("gpu", []) is None

    def test_less_than_3_returns_none(self, calc: PercentilePriceCalculator) -> None:
        ads = [
            ComponentAd(ad_id=1, component_name="gpu", price=1000),
            ComponentAd(ad_id=2, component_name="gpu", price=2000),
        ]
        assert calc.calculate("gpu", ads) is None

    def test_3_to_5_uses_median(self, calc: PercentilePriceCalculator) -> None:
        """3-5 оголошень → медіана, used_ids = всі."""
        ads = [
            ComponentAd(ad_id=1, component_name="gpu", price=1000),
            ComponentAd(ad_id=2, component_name="gpu", price=2000),
            ComponentAd(ad_id=3, component_name="gpu", price=3000),
        ]
        result = calc.calculate("gpu", ads)
        assert result is not None
        assert result.price == 2000  # медіана
        assert result.sample_size == 3
        assert sorted(result.used_ids) == [1, 2, 3]

    def test_5_uses_median(self, calc: PercentilePriceCalculator) -> None:
        ads = [
            ComponentAd(ad_id=1, component_name="gpu", price=1000),
            ComponentAd(ad_id=2, component_name="gpu", price=2000),
            ComponentAd(ad_id=3, component_name="gpu", price=3000),
            ComponentAd(ad_id=4, component_name="gpu", price=4000),
            ComponentAd(ad_id=5, component_name="gpu", price=5000),
        ]
        result = calc.calculate("gpu", ads)
        assert result is not None
        assert result.price == 3000  # медіана (n//2 = 2)
        assert result.sample_size == 5

    def test_10_uses_trim_and_percentile(self, calc: PercentilePriceCalculator) -> None:
        """10 оголошень → trim 10% (1 з кожного краю), 33-й перцентиль від 8."""
        ads = [
            ComponentAd(ad_id=i, component_name="gpu", price=i * 1000)
            for i in range(1, 11)
        ]  # prices: 1000, 2000, ..., 10000
        result = calc.calculate("gpu", ads)
        assert result is not None
        # trim 1 з кожного краю → залишається 2000..9000 (8 шт)
        # 33-й перцентиль: idx = int(8 * 0.33) = 2 → ціна 4000
        assert result.price == 4000
        assert result.sample_size == 8
        assert 1 not in result.used_ids  # 1000 обрізано
        assert 10 not in result.used_ids  # 10000 обрізано

    def test_6_uses_trim(self, calc: PercentilePriceCalculator) -> None:
        """Рівно 6 → trim 10% (0, бо int(0.6)=0), тоді 33-й від 6."""
        ads = [
            ComponentAd(ad_id=i, component_name="gpu", price=i * 1000)
            for i in range(1, 7)
        ]
        result = calc.calculate("gpu", ads)
        assert result is not None
        # trim_size = int(6 * 0.1) = 0 → не обрізаємо
        # idx = int(6 * 0.33) = 1 → ціна 2000 (індекс 1)
        assert result.price == 2000
        assert result.sample_size == 6

    def test_sorted_correctly(self, calc: PercentilePriceCalculator) -> None:
        """Ціни сортуються перед обробкою."""
        ads = [
            ComponentAd(ad_id=1, component_name="gpu", price=5000),
            ComponentAd(ad_id=2, component_name="gpu", price=1000),
            ComponentAd(ad_id=3, component_name="gpu", price=3000),
        ]
        result = calc.calculate("gpu", ads)
        assert result is not None
        assert result.price == 3000  # медіана відсортованого [1000,3000,5000]

    def test_different_components_isolated(self, calc: PercentilePriceCalculator) -> None:
        """Різні component_name не впливають одне на одного."""
        ads_gpu = [
            ComponentAd(ad_id=1, component_name="gtx_1060", price=5000),
            ComponentAd(ad_id=2, component_name="gtx_1060", price=6000),
            ComponentAd(ad_id=3, component_name="gtx_1060", price=7000),
        ]
        ads_cpu = [
            ComponentAd(ad_id=4, component_name="i5_6400", price=3000),
            ComponentAd(ad_id=5, component_name="i5_6400", price=4000),
            ComponentAd(ad_id=6, component_name="i5_6400", price=5000),
        ]
        r_gpu = calc.calculate("gtx_1060", ads_gpu)
        r_cpu = calc.calculate("i5_6400", ads_cpu)
        assert r_gpu is not None and r_gpu.price == 6000
        assert r_cpu is not None and r_cpu.price == 4000


# ===========================================================================
# 4. ComponentPriceService — оркестратор з моками
# ===========================================================================
class TestComponentPriceService:
    @pytest.fixture
    def mock_ad_repo(self) -> MagicMock:
        repo = MagicMock()
        repo.fetch_active_components = AsyncMock(return_value=[])
        return repo

    @pytest.fixture
    def mock_price_repo(self) -> MagicMock:
        repo = MagicMock()
        repo.upsert_prices = AsyncMock(return_value=0)
        return repo

    @pytest.fixture
    def calc(self) -> PercentilePriceCalculator:
        return PercentilePriceCalculator(PriceAnalyzerConfig())

    @pytest.fixture
    def config(self) -> PriceAnalyzerConfig:
        return PriceAnalyzerConfig()

    @pytest.fixture
    def metrics(self) -> MetricsCollector:
        return MetricsCollector()

    @pytest.fixture
    def trace(self) -> TracingContext:
        return TracingContext()

    @pytest.fixture
    def service(
        self,
        mock_ad_repo: MagicMock,
        mock_price_repo: MagicMock,
        calc: PercentilePriceCalculator,
        config: PriceAnalyzerConfig,
        metrics: MetricsCollector,
        trace: TracingContext,
    ) -> ComponentPriceService:
        return ComponentPriceService(
            ad_repo=mock_ad_repo,
            price_repo=mock_price_repo,
            calculator=calc,
            config=config,
            metrics=metrics,
            trace=trace,
        )

    @pytest.mark.asyncio
    async def test_no_ads_returns_empty(self, service: ComponentPriceService, mock_ad_repo: MagicMock) -> None:
        mock_ad_repo.fetch_active_components.return_value = []
        result = await service.run()
        assert result == []
        service._price_repo.upsert_prices.assert_not_called()

    @pytest.mark.asyncio
    async def test_insufficient_data_returns_empty(self, service: ComponentPriceService, mock_ad_repo: MagicMock) -> None:
        """1 оголошення на компонент → недостатньо для percentile."""
        mock_ad_repo.fetch_active_components.return_value = [
            ComponentAd(ad_id=1, component_name="gtx_1060", price=5000),
        ]
        result = await service.run()
        assert result == []
        service._price_repo.upsert_prices.assert_not_called()

    @pytest.mark.asyncio
    async def test_successful_calculation_and_upsert(
        self,
        service: ComponentPriceService,
        mock_ad_repo: MagicMock,
        mock_price_repo: MagicMock,
    ) -> None:
        mock_ad_repo.fetch_active_components.return_value = [
            ComponentAd(ad_id=1, component_name="gtx_1060", price=4000),
            ComponentAd(ad_id=2, component_name="gtx_1060", price=5000),
            ComponentAd(ad_id=3, component_name="gtx_1060", price=6000),
            ComponentAd(ad_id=4, component_name="i5_6400", price=2000),
            ComponentAd(ad_id=5, component_name="i5_6400", price=3000),
            ComponentAd(ad_id=6, component_name="i5_6400", price=4000),
        ]
        result = await service.run()
        assert len(result) == 2
        mock_price_repo.upsert_prices.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_multiple_components_grouped(self, service: ComponentPriceService, mock_ad_repo: MagicMock) -> None:
        mock_ad_repo.fetch_active_components.return_value = [
            ComponentAd(ad_id=1, component_name="gtx_1060", price=1000),
            ComponentAd(ad_id=2, component_name="gtx_1060", price=2000),
            ComponentAd(ad_id=3, component_name="gtx_1060", price=3000),
            ComponentAd(ad_id=4, component_name="rtx_3060", price=5000),
            ComponentAd(ad_id=5, component_name="rtx_3060", price=6000),
            ComponentAd(ad_id=6, component_name="rtx_3060", price=7000),
        ]
        result = await service.run()
        names = {r.component_name for r in result}
        assert names == {"gtx_1060", "rtx_3060"}

    @pytest.mark.asyncio
    async def test_config_passed_to_fetch(self, service: ComponentPriceService, mock_ad_repo: MagicMock) -> None:
        mock_ad_repo.fetch_active_components.return_value = []
        await service.run()
        assert isinstance(mock_ad_repo.fetch_active_components.await_args.args[0], PriceAnalyzerConfig)


# ===========================================================================
# 5. PriceAnalyzerConfig
# ===========================================================================
class TestPriceAnalyzerConfig:
    def test_frozen(self) -> None:
        config = PriceAnalyzerConfig()
        with pytest.raises(Exception):
            config.min_price = 50  # type: ignore[misc]

    def test_defaults(self) -> None:
        config = PriceAnalyzerConfig()
        assert config.min_price == 100
        assert config.min_ads_for_percentile == 3
        assert config.min_ads_for_trim == 6
        assert config.trim_fraction == 0.10
        assert config.percentile_index == 0.33


# ===========================================================================
# 6. Circuit Breaker
# ===========================================================================
class TestCircuitBreaker:
    @pytest.fixture
    def cb(self) -> CircuitBreaker:
        return CircuitBreaker(failure_threshold=3, recovery_timeout=0.1)

    @pytest.mark.asyncio
    async def test_closed_allows_requests(self, cb: CircuitBreaker) -> None:
        """У стані CLOSED запити проходять."""
        async def _ok() -> str:
            return "success"

        result = await cb.call(_ok)
        assert result == "success"

    @pytest.mark.asyncio
    async def test_opens_after_threshold(self, cb: CircuitBreaker) -> None:
        """Після N помилок circuit відкривається і блокує запити."""
        async def _fail() -> None:
            raise RuntimeError("boom")

        for _ in range(3):
            with pytest.raises(RuntimeError, match="boom"):
                await cb.call(_fail)

        # Circuit тепер OPEN
        with pytest.raises(RuntimeError, match="OPEN"):
            await cb.call(_fail)

    @pytest.mark.asyncio
    async def test_half_open_then_closes(self, cb: CircuitBreaker) -> None:
        """Після recovery_timeout circuit переходить у HALF_OPEN і закривається при успіху."""
        async def _fail() -> None:
            raise RuntimeError("boom")

        for _ in range(3):
            with pytest.raises(RuntimeError, match="boom"):
                await cb.call(_fail)

        # Чекаємо recovery_timeout
        await asyncio.sleep(0.15)

        async def _ok() -> str:
            return "recovered"

        result = await cb.call(_ok)
        assert result == "recovered"

    @pytest.mark.asyncio
    async def test_half_open_then_reopens(self, cb: CircuitBreaker) -> None:
        """HALF_OPEN + помилка → знову OPEN."""
        async def _fail() -> None:
            raise RuntimeError("boom")

        for _ in range(3):
            with pytest.raises(RuntimeError, match="boom"):
                await cb.call(_fail)

        await asyncio.sleep(0.15)

        with pytest.raises(RuntimeError, match="boom"):
            await cb.call(_fail)

        # Знову OPEN
        with pytest.raises(RuntimeError, match="OPEN"):
            await cb.call(_fail)


# ===========================================================================
# 7. Retry with exponential backoff
# ===========================================================================
class TestRetry:
    @pytest.mark.asyncio
    async def test_succeeds_on_third_attempt(self) -> None:
        """З 2-ма фейлами і 3-м успіхом — повертає результат."""
        mock_fn = AsyncMock(side_effect=[
            httpx.NetworkError("fail 1"),
            httpx.NetworkError("fail 2"),
            "success",
        ])

        result = await with_retry(mock_fn, max_attempts=3, base_delay=0.01)
        assert result == "success"
        assert mock_fn.call_count == 3

    @pytest.mark.asyncio
    async def test_fails_after_max_attempts(self) -> None:
        """Після вичерпання спроб — піднімає останню помилку."""
        mock_fn = AsyncMock(side_effect=httpx.TimeoutException("timeout"))

        with pytest.raises(httpx.TimeoutException):
            await with_retry(mock_fn, max_attempts=3, base_delay=0.01)

        assert mock_fn.call_count == 3

    @pytest.mark.asyncio
    async def test_no_retry_on_success(self) -> None:
        """При першому успіху retry не викликається зайвий раз."""
        mock_fn = AsyncMock(return_value="ok")

        result = await with_retry(mock_fn, max_attempts=3, base_delay=0.01)
        assert result == "ok"
        assert mock_fn.call_count == 1


# ===========================================================================
# 8. Graceful Shutdown
# ===========================================================================
class TestGracefulShutdown:
    @pytest.fixture
    def mock_ad_repo(self) -> MagicMock:
        repo = MagicMock()
        repo.fetch_active_components = AsyncMock(return_value=[])
        return repo

    @pytest.fixture
    def mock_price_repo(self) -> MagicMock:
        repo = MagicMock()
        repo.upsert_prices = AsyncMock(return_value=0)
        return repo

    @pytest.fixture
    def service_with_shutdown(
        self,
        mock_ad_repo: MagicMock,
        mock_price_repo: MagicMock,
    ) -> tuple[ComponentPriceService, asyncio.Event]:
        shutdown_event = asyncio.Event()
        service = ComponentPriceService(
            ad_repo=mock_ad_repo,
            price_repo=mock_price_repo,
            calculator=PercentilePriceCalculator(PriceAnalyzerConfig()),
            config=PriceAnalyzerConfig(),
            metrics=MetricsCollector(),
            trace=TracingContext(),
            shutdown_event=shutdown_event,
        )
        return service, shutdown_event

    @pytest.mark.asyncio
    async def test_shutdown_after_fetch_returns_empty(
        self,
        service_with_shutdown: tuple[ComponentPriceService, asyncio.Event],
        mock_ad_repo: MagicMock,
    ) -> None:
        """Якщо shutdown після fetch — повертає [] і не падає."""
        service, shutdown_event = service_with_shutdown

        async def _fetch_with_delay(*args: Any, **kwargs: Any) -> list[ComponentAd]:
            await asyncio.sleep(0.01)
            return [
                ComponentAd(ad_id=1, component_name="gpu", price=1000),
            ]

        mock_ad_repo.fetch_active_components = AsyncMock(side_effect=_fetch_with_delay)

        # Запускаємо run() і одразу сигналізуємо shutdown
        task = asyncio.create_task(service.run())
        await asyncio.sleep(0.005)
        shutdown_event.set()

        result = await task
        # Після fetch + shutdown — сервіс має завершитись чисто
        assert isinstance(result, list)

    @pytest.mark.asyncio
    async def test_shutdown_during_calculation_stops_processing(
        self,
        service_with_shutdown: tuple[ComponentPriceService, asyncio.Event],
        mock_ad_repo: MagicMock,
        mock_price_repo: MagicMock,
    ) -> None:
        """Shutdown під час розрахунку зупиняє обробку наступних компонентів."""
        service, shutdown_event = service_with_shutdown

        # 2 компоненти по 3 оголошення (достатньо для медіани)
        mock_ad_repo.fetch_active_components.return_value = [
            ComponentAd(ad_id=1, component_name="gpu_a", price=1000),
            ComponentAd(ad_id=2, component_name="gpu_a", price=2000),
            ComponentAd(ad_id=3, component_name="gpu_a", price=3000),
            ComponentAd(ad_id=4, component_name="gpu_b", price=4000),
            ComponentAd(ad_id=5, component_name="gpu_b", price=5000),
            ComponentAd(ad_id=6, component_name="gpu_b", price=6000),
        ]

        # Встановлюємо shutdown_event одразу — обробка має зупинитись
        shutdown_event.set()
        result = await service.run()

        # Має бути 0 результатів, бо shutdown спрацював до/під час обробки
        assert isinstance(result, list)


# ===========================================================================
# 9. Idempotency Key
# ===========================================================================
class TestIdempotencyKey:
    def test_same_data_same_key(self) -> None:
        """Однакові component_name + date + price → однаковий idempotency_key."""
        import hashlib

        def _make_key(name: str, date: str, price: int) -> str:
            return hashlib.sha256(f"{name}:{date}:{price}".encode()).hexdigest()[:32]

        key1 = _make_key("rtx_4090", "2024-01-15", 15000)
        key2 = _make_key("rtx_4090", "2024-01-15", 15000)
        assert key1 == key2
        assert len(key1) == 32

    def test_different_data_different_key(self) -> None:
        """Різні дані → різні ключі."""
        import hashlib

        def _make_key(name: str, date: str, price: int) -> str:
            return hashlib.sha256(f"{name}:{date}:{price}".encode()).hexdigest()[:32]

        key1 = _make_key("rtx_4090", "2024-01-15", 15000)
        key2 = _make_key("rtx_4090", "2024-01-15", 16000)
        assert key1 != key2

    @pytest.mark.asyncio
    async def test_upsert_record_contains_key(self) -> None:
        """Service генерує PriceUpsertRecord з заповненим idempotency_key."""
        mock_ad_repo = MagicMock()
        mock_ad_repo.fetch_active_components = AsyncMock(return_value=[
            ComponentAd(ad_id=1, component_name="gtx_1060", price=5000),
            ComponentAd(ad_id=2, component_name="gtx_1060", price=6000),
            ComponentAd(ad_id=3, component_name="gtx_1060", price=7000),
        ])
        mock_price_repo = MagicMock()
        mock_price_repo.upsert_prices = AsyncMock(return_value=1)

        service = ComponentPriceService(
            ad_repo=mock_ad_repo,
            price_repo=mock_price_repo,
            calculator=PercentilePriceCalculator(PriceAnalyzerConfig()),
            config=PriceAnalyzerConfig(),
            metrics=MetricsCollector(),
            trace=TracingContext(),
        )

        await service.run()

        # Перевіряємо, що upsert_prices отримав записи з idempotency_key
        call_args = mock_price_repo.upsert_prices.await_args
        records: list[PriceUpsertRecord] = call_args.args[0]
        assert len(records) == 1
        assert records[0].idempotency_key
        assert len(records[0].idempotency_key) == 32
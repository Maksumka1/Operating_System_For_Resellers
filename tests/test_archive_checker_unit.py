"""
Unit-тести ArchiveChecker з фейковими залежностями.

Запуск:
    pytest tests/test_archive_checker_unit.py -v
"""
import pytest
from datetime import datetime, timezone
from unittest.mock import AsyncMock

from scripts.clean_archive import (
    ArchiveChecker,
    ArchiveCheckerConfig,
    AdRecord,
    AdRepository,
    OlxHttpClient,
)


class FakeAdRepository(AdRepository):
    """In-memory сховище без Supabase."""

    def __init__(self, ads: list[AdRecord]):
        self._ads = ads
        self.deactivated_ids: list[int] = []
        self.deactivated_at: datetime | None = None

    async def get_active_ads(self, limit: int, offset: int = 0):
        return self._ads[offset : offset + limit]

    async def deactivate_batch(self, ad_ids: list[int], deactivated_at: datetime):
        self.deactivated_ids.extend(ad_ids)
        self.deactivated_at = deactivated_at
        return len(ad_ids)


class TestArchiveChecker:
    """Тести оркестратора."""

    @pytest.mark.asyncio
    async def test_all_active_ads_stay_active(self):
        """Всі 200 → 0 деактивованих."""
        ads = [
            AdRecord(ad_id=1, url="/d/uk/obyavlenie/1"),
            AdRecord(ad_id=2, url="/d/uk/obyavlenie/2"),
        ]
        repo = FakeAdRepository(ads)

        http_mock = AsyncMock(spec=OlxHttpClient)
        http_mock.check_url = AsyncMock(return_value=(200, "https://olx.ua/d/uk/obyavlenie/x"))
        http_mock.warmup = AsyncMock()

        config = ArchiveCheckerConfig(max_ads_per_check=100, db_batch_size=10)
        checker = ArchiveChecker(repo, http_mock, config)

        stats = await checker.run()

        assert stats["checked"] == 2
        assert stats["deactivated"] == 0
        assert len(repo.deactivated_ids) == 0

    @pytest.mark.asyncio
    async def test_mixed_ads_partially_deactivated(self):
        """Один 404, один 200 → 1 деактивований."""
        ads = [
            AdRecord(ad_id=1, url="/d/uk/obyavlenie/1"),
            AdRecord(ad_id=2, url="/d/uk/obyavlenie/2"),
        ]
        repo = FakeAdRepository(ads)

        http_mock = AsyncMock(spec=OlxHttpClient)
        # side_effect: перший виклик → 404, другий → 200
        http_mock.check_url = AsyncMock(side_effect=[
            (404, "https://olx.ua/d/uk/obyavlenie/1"),
            (200, "https://olx.ua/d/uk/obyavlenie/2"),
        ])
        http_mock.warmup = AsyncMock()

        config = ArchiveCheckerConfig(max_ads_per_check=100, db_batch_size=10)
        checker = ArchiveChecker(repo, http_mock, config)

        stats = await checker.run()

        assert stats["checked"] == 2
        assert stats["deactivated"] == 1
        assert repo.deactivated_ids == [1]

    @pytest.mark.asyncio
    async def test_empty_db_returns_zero(self):
        """Порожня БД → нулі."""
        repo = FakeAdRepository([])

        http_mock = AsyncMock(spec=OlxHttpClient)
        http_mock.warmup = AsyncMock()

        config = ArchiveCheckerConfig()
        checker = ArchiveChecker(repo, http_mock, config)

        stats = await checker.run()

        assert stats["checked"] == 0
        assert stats["deactivated"] == 0
        
        http_mock.warmup.assert_not_called()

    @pytest.mark.asyncio
    async def test_timeout_keeps_active(self):
        """Таймаут (status_code=0) → залишаємо active."""
        ads = [AdRecord(ad_id=1, url="/d/uk/obyavlenie/1")]
        repo = FakeAdRepository(ads)

        http_mock = AsyncMock(spec=OlxHttpClient)
        http_mock.check_url = AsyncMock(return_value=(0, "https://olx.ua/d/uk/obyavlenie/1"))
        http_mock.warmup = AsyncMock()

        config = ArchiveCheckerConfig(max_ads_per_check=100, db_batch_size=10)
        checker = ArchiveChecker(repo, http_mock, config)

        stats = await checker.run()

        assert stats["deactivated"] == 0
        assert len(repo.deactivated_ids) == 0

    @pytest.mark.asyncio
    async def test_large_batch_respects_db_batch_size(self):
        """Багато оголошень → деактивація пачками."""
        ads = [AdRecord(ad_id=i, url=f"/d/uk/obyavlenie/{i}") for i in range(1, 251)]
        repo = FakeAdRepository(ads)

        http_mock = AsyncMock(spec=OlxHttpClient)
        http_mock.check_url = AsyncMock(return_value=(404, "https://olx.ua/d/uk/obyavlenie/x"))
        http_mock.warmup = AsyncMock()

        config = ArchiveCheckerConfig(max_ads_per_check=1000, db_batch_size=100)
        checker = ArchiveChecker(repo, http_mock, config)

        stats = await checker.run()

        assert stats["checked"] == 250
        assert stats["deactivated"] == 250
        assert len(repo.deactivated_ids) == 250
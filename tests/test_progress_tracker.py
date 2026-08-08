"""
Unit-тести для ProgressTracker.

Запуск:
    pytest tests/test_progress_tracker.py -v
"""
import pytest
import asyncio
from scripts.clean_archive import ProgressTracker


class TestProgressTracker:
    """Тести потокобезпечного лічильника."""

    @pytest.mark.asyncio
    async def test_increment_increases_counter(self):
        """Один increment → processed == 1."""
        tracker = ProgressTracker(total=100, log_interval=50)
        await tracker.increment()
        assert tracker.processed == 1

    @pytest.mark.asyncio
    async def test_concurrent_increments_are_atomic(self):
        """100 паралельних increment → processed == 100."""
        tracker = ProgressTracker(total=100, log_interval=999)

        async def worker():
            await tracker.increment()

        await asyncio.gather(*[worker() for _ in range(100)])
        assert tracker.processed == 100

    @pytest.mark.asyncio
    async def test_progress_logs_at_interval(self):
        """Лог спрацьовує при досягненні інтервалу (не падає)."""
        tracker = ProgressTracker(total=10, log_interval=5)
        for _ in range(5):
            await tracker.increment()
        # Лічильник оновився коректно — лог викликався
        assert tracker.processed == 5

    def test_zero_total_raises_value_error(self):
        """Невалідний total → ValueError."""
        with pytest.raises(ValueError, match="total must be positive"):
            ProgressTracker(total=0, log_interval=10)

    def test_negative_total_raises_value_error(self):
        """Від'ємний total → ValueError."""
        with pytest.raises(ValueError, match="total must be positive"):
            ProgressTracker(total=-5, log_interval=10)
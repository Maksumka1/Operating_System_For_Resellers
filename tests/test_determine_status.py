"""
Unit-тести для determine_status() — FIXED.

Запуск:
    pytest tests/test_determine_status.py -v
"""
import pytest
from scripts.clean_archive import determine_status


class TestDetermineStatus:
    """Тести логіки визначення статусу оголошення."""

    @pytest.mark.parametrize("status_code", [404, 410])
    def test_4xx_returns_deactivated(self, status_code):
        """404 та 410 → завжди deactivated, незалежно від URL."""
        result = determine_status(status_code, "https://olx.ua/d/uk/obyavlenie/123")
        assert result == "deactivated"

    def test_200_with_obyavlenie_returns_active(self):
        """200 + фінальний URL містить /obyavlenie/ → active."""
        result = determine_status(200, "https://www.olx.ua/d/uk/obyavlenie/test-ID123.html")
        assert result == "active"

    @pytest.mark.parametrize("status_code", [301, 302, 500, 502, 503])
    def test_other_statuses_return_active(self, status_code):
        """Всі статуси, крім 404/410, без редиректу на головну → active."""
        result = determine_status(status_code, "https://www.olx.ua/d/uk/obyavlenie/test-ID123.html")
        assert result == "active"

    def test_200_on_homepage_returns_deactivated(self):
        """200, але фінальний URL — головна (немає /obyavlenie/) → deactivated."""
        result = determine_status(200, "https://www.olx.ua/")
        assert result == "deactivated"

    def test_200_on_category_page_returns_deactivated(self):
        """200, але фінальний URL — категорія (немає /obyavlenie/) → deactivated."""
        result = determine_status(200, "https://www.olx.ua/uk/elektronika/")
        assert result == "deactivated"

    def test_200_on_search_page_returns_deactivated(self):
        """200, але фінальний URL — пошук (немає /obyavlenie/) → deactivated."""
        result = determine_status(200, "https://www.olx.ua/uk/list/q-iphone/")
        assert result == "deactivated"
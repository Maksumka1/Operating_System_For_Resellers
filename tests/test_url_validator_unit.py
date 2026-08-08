"""
Unit-тести UrlSafetyValidator (без реальних запитів).

Запуск:
    pytest tests/test_url_validator_unit.py -v
"""
import pytest
from scripts.clean_archive import UrlSafetyValidator, ArchiveCheckerConfig


@pytest.fixture
def validator():
    return UrlSafetyValidator(ArchiveCheckerConfig())


class TestUrlSafetyValidator:
    """Тести SSRF-захисту."""

    @pytest.mark.parametrize("url", [
        "https://www.olx.ua/d/uk/obyavlenie/123",
        "http://www.olx.ua/d/uk/obyavlenie/123",
    ])
    def test_olx_domains_allowed(self, validator, url):
        assert validator.is_safe(url) is True

    @pytest.mark.parametrize("url", [
        "http://169.254.169.254/latest/meta-data/",
        "http://127.0.0.1:8000/admin",
        "http://0.0.0.0:22",
        "http://192.168.1.1",
        "http://10.0.0.1",
    ])
    def test_internal_ips_blocked(self, validator, url):
        assert validator.is_safe(url) is False

    @pytest.mark.parametrize("url", [
        "https://evil.com/steal",
        "https://google.com/",
        "https://fake-olx.ua/",
        "https://olx.ua.attacker.com/",
    ])
    def test_non_olx_domains_blocked(self, validator, url):
        assert validator.is_safe(url) is False

    @pytest.mark.parametrize("url", [
        "file:///etc/passwd",
        "ftp://server.com/data",
        "dict://localhost:11211/",
        "data:text/html,<script>alert(1)</script>",
    ])
    def test_dangerous_schemes_blocked(self, validator, url):
        assert validator.is_safe(url) is False

    def test_url_with_credentials_blocked(self, validator):
        url = "https://user:pass@olx.ua/d/uk/obyavlenie/123"
        assert validator.is_safe(url) is False

    def test_empty_hostname_blocked(self, validator):
        assert validator.is_safe("http:///path") is False
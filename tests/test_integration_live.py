"""
Реальні запити до OLX.
Запуск: pytest tests/test_integration_live.py -v -m slow
"""
import pytest
import asyncio
from curl_cffi.requests import AsyncSession

pytestmark = pytest.mark.slow


class TestLiveOlxRequests:
    """Реальні запити до OLX."""

    @pytest.mark.asyncio
    async def test_active_urls(self, active_urls):
        from scripts.clean_archive import ArchiveCheckerConfig, UrlSafetyValidator, OlxHttpClient
        
        config = ArchiveCheckerConfig()
        validator = UrlSafetyValidator(config)
        
        async with AsyncSession(headers=config.headers, impersonate="chrome120") as session:
            client = OlxHttpClient(session, validator, config)
            
            for url in active_urls:
                status_code, final_url = await client.check_url(url)
                assert status_code == 200, f"{url} → {status_code}"
                assert "/obyavlenie/" in final_url, f"{url} редіректнув на {final_url}"

    @pytest.mark.asyncio
    async def test_deactivated_urls(self, deactivated_urls):
        from scripts.clean_archive import ArchiveCheckerConfig, UrlSafetyValidator, OlxHttpClient
        
        config = ArchiveCheckerConfig()
        validator = UrlSafetyValidator(config)
        
        async with AsyncSession(headers=config.headers, impersonate="chrome120") as session:
            client = OlxHttpClient(session, validator, config)
            
            for url in deactivated_urls:
                status_code, final_url = await client.check_url(url)
                is_404 = status_code in (404, 410)
                assert is_404, f"{url}: {status_code} → {final_url}"

    @pytest.mark.asyncio
    async def test_ssrf_blocks_internal_ip(self):
        from scripts.clean_archive import ArchiveCheckerConfig, UrlSafetyValidator, OlxHttpClient, SecurityError
        
        config = ArchiveCheckerConfig()
        validator = UrlSafetyValidator(config)
        
        async with AsyncSession(headers=config.headers, impersonate="chrome120") as session:
            client = OlxHttpClient(session, validator, config)
            
            with pytest.raises(SecurityError):
                await client.check_url("http://169.254.169.254/latest/meta-data/")
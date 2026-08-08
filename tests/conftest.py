import sys
from pathlib import Path

TESTS_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = TESTS_DIR.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import pytest

@pytest.fixture(scope="session")
def deactivated_urls() -> list[str]:
    return [
        "https://www.olx.ua/d/uk/obyavlenie/vazhlivo-shanovn-ID1111lY.html",
        "https://www.olx.ua/d/uk/obyavlenie/vdeokarta-xfx-rx-6600xt-quick-308-black-ID1111SG.html",
    ]

@pytest.fixture(scope="session")
def active_urls() -> list[str]:
    return [
        "https://www.olx.ua/d/uk/obyavlenie/zhorstkiy-disk-western-digital-wd-purple-500gb-1tb-2tb-3tb-4tb-8tv-IDTMqiX.html",
        "https://www.olx.ua/d/uk/obyavlenie/ssd-bestoss-2-5-sata-120-256-512gb-IDU1Wsi.html",
    ]
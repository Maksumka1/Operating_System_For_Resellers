"""
test_hardware_matchers.py

Простий pytest: по 10 прикладів на кожну категорію.
Запуск: pytest test_hardware_matchers.py -v
"""

import pytest
from hardware_matchers import HardwareMatcher, InputValidationError


@pytest.fixture(scope="module")
def matcher():
    return HardwareMatcher()


# ---------------------------------------------------------------------------
# GPU (10 прикладів)
# ---------------------------------------------------------------------------
GPU_CASES = [
    ("Відеокарта ASUS GeForce RTX 3060 Ti 8GB", ["rtx_3060_ti", "rtx_3060_ti_8gb", "rtx_3060_ti_8_gb"]),
    ("MSI GTX 1050 Ti 4Gb Gaming", ["gtx_1050_ti", "gtx_1050_ti_4gb", "gtx_1050_ti_4_gb"]),
    ("Zotac 1080 8gb AMP Edition", ["gtx_1080", "gtx_1080_8gb", "gtx_1080_8_gb"]),
    ("Sapphire RX 6700 XT 12GB", ["rx_6700_xt", "rx_6700_xt_12gb", "rx_6700_xt_12_gb", "rx_6700"]),
    ("Intel Arc A750 8 GB", ["arc_a750", "arc_a750_8gb", "arc_a750_8_gb"]),
    ("Radeon HD 7850 2Gb", ["hd_7850", "hd_7850_2gb", "hd_7850_2_gb"]),
    ("AMD R9 390X 8GB", ["r9_390_x"]),
    ("Відеокарта 1660 Super 6гб", ["gtx_1660_super", "gtx_1660_super_6gb", "gtx_1660_super_6_gb"]),
    ("NVIDIA CMP 90HX майнінг", ["cmp_90hx"]),
    ("Palit RTX 4070 Ti Super 16GB", ["rtx_4070_ti_super", "rtx_4070_ti_super_16gb", "rtx_4070_ti_super_16_gb"]),
]


@pytest.mark.parametrize("title,expected_subkeys", GPU_CASES)
def test_gpu_extraction(matcher, title, expected_subkeys):
    profile = matcher.match(title)
    assert profile.gpu, f"GPU not found in: {title}"
    for sub in expected_subkeys:
        assert sub in profile.gpu, f"Expected {sub} in {profile.gpu}"


# ---------------------------------------------------------------------------
# CPU (10 прикладів)
# ---------------------------------------------------------------------------
CPU_CASES = [
    ("Процесор Intel Core i5-10400F", ["i5_10400f"]),
    ("AMD Ryzen 5 5600X BOX", ["ryzen_5_5600x"]),
    ("Intel Core Ultra 7 155H", ["core_ultra_7_155h"]),
    ("Процесор Xeon E5-2680 v2", ["xeon_e5_2680_v2"]),
    ("AMD FX-8350 AM3+", ["fx_8350"]),
    ("Pentium Gold G6400", ["pentium_g6400", "celeron_g6400"]),
    ("Athlon 64 X2 6000+", ["athlon_x4_6000", "athlon_ii_x2_6000", "athlon_64_x2_6000", "athlon_6000"]),
    ("Core 2 Quad Q9550", ["core_2_quad_q9550"]),
    ("Ryzen 9 7950X3D", ["ryzen_9_7950x3d"]),
    ("Intel i3-12100", ["i3_12100"]),
]


@pytest.mark.parametrize("title,expected_subkeys", CPU_CASES)
def test_cpu_extraction(matcher, title, expected_subkeys):
    profile = matcher.match(title)
    assert profile.cpu, f"CPU not found in: {title}"
    for sub in expected_subkeys:
        assert sub in profile.cpu, f"Expected {sub} in {profile.cpu}"


# ---------------------------------------------------------------------------
# Motherboard (10 прикладів)
# ---------------------------------------------------------------------------
MB_CASES = [
    ("Материнка ASUS ROG STRIX Z790-E", ["z790"]),
    ("MSI B450 Tomahawk Max", ["b450"]),
    ("Gigabyte X670 AORUS Elite", ["x670"]),
    ("ASRock B550M Pro4", ["b550"]),
    ("Плата H610M-K", ["h610"]),
    ("Материнська плата 970 AM3+", ["970"]),
    ("ASUS M5A78L-M LX3", ["760g", "780g"]),
    ("Gigabyte GA-H110M-S2", ["h110"]),
    ("MSI X870E Carbon WIFI", ["x870e"]),
    ("Biostar A320MH", ["a320"]),
]


@pytest.mark.parametrize("title,expected_subkeys", MB_CASES)
def test_motherboard_extraction(matcher, title, expected_subkeys):
    profile = matcher.match(title)
    assert profile.motherboard, f"MB not found in: {title}"
    for sub in expected_subkeys:
        assert sub in profile.motherboard, f"Expected {sub} in {profile.motherboard}"


# ---------------------------------------------------------------------------
# PSU (10 прикладів)
# ---------------------------------------------------------------------------
PSU_CASES = [
    ("Блок живлення 600W", ["600w"]),
    ("Corsair RM750 80+ Gold", ["750w"]),
    ("БЖ Chieftec 500W", ["500w"]),
    ("Deepcool 650W", ["650w"]),
    ("Блок питания 850 ватт", ["850w"]),
    ("Seasonic GX-1000", ["1000w"]),
    ("БП 400W", ["400w"]),
    ("Zalman 700W", ["700w"]),
    ("Be Quiet 550W", ["550w"]),
    ("Aerocool 1200W", ["1200w"]),
]


@pytest.mark.parametrize("title,expected_subkeys", PSU_CASES)
def test_psu_extraction(matcher, title, expected_subkeys):
    profile = matcher.match(title)
    assert profile.psu, f"PSU not found in: {title}"
    for sub in expected_subkeys:
        assert sub in profile.psu, f"Expected {sub} in {profile.psu}"


# ---------------------------------------------------------------------------
# Storage (10 прикладів)
# ---------------------------------------------------------------------------
STORAGE_CASES = [
    ("SSD Kingston 240GB", ["ssd_240gb"]),
    ("HDD Seagate 1TB Barracuda", ["hdd_1tb"]),
    ("NVMe M.2 500GB Samsung", ["ssd_500gb"]),
    ("Жорсткий диск 2TB WD Blue", ["hdd_2tb"]),
    ("SSD Apacer 120GB", ["ssd_120gb"]),
    ("HDD Toshiba 4TB", ["hdd_4tb"]),
    ("SSD Netac 256GB", ["ssd_256gb"]),
    ("Вінчестер 500GB", ["hdd_500gb", "ssd_500gb"]),
    ("SSD Patriot 512GB", ["ssd_512gb"]),
    ("HDD 8TB IronWolf", ["hdd_8tb"]),
]


@pytest.mark.parametrize("title,expected_subkeys", STORAGE_CASES)
def test_storage_extraction(matcher, title, expected_subkeys):
    profile = matcher.match(title)
    assert profile.storage, f"Storage not found in: {title}"
    for sub in expected_subkeys:
        assert sub in profile.storage, f"Expected {sub} in {profile.storage}"


# ---------------------------------------------------------------------------
# RAM (10 прикладів)
# ---------------------------------------------------------------------------
RAM_CASES = [
    ("RAM DDR4 8GB", ["ram_ddr4_8gb"]),
    ("DDR3 2x8GB Kingston", ["ram_ddr3_16gb"]),
    ("Оператива DDR5 32GB", ["ram_ddr5_32gb"]),
    ("DDR4 4x16GB RGB", ["ram_ddr4_64gb"]),
    ("Модуль пам'яті DDR3 4GB", ["ram_ddr3_4gb"]),
    ("DDR5 2x32GB 6000MHz", ["ram_ddr5_64gb"]),
    ("DDR4 8x8GB Server", ["ram_ddr4_64gb"]),
    ("DDR4 1x16GB", ["ram_ddr4_16gb"]),
    ("ОЗУ DDR3 2x4GB", ["ram_ddr3_8gb"]),
    ("DDR5 48GB Kit", ["ram_ddr5_48gb"]),
]


@pytest.mark.parametrize("title,expected_subkeys", RAM_CASES)
def test_ram_extraction(matcher, title, expected_subkeys):
    profile = matcher.match(title)
    assert profile.ram, f"RAM not found in: {title}"
    for sub in expected_subkeys:
        assert sub in profile.ram, f"Expected {sub} in {profile.ram}"


# ---------------------------------------------------------------------------
# Безпека / валідація
# ---------------------------------------------------------------------------

def test_none_title_raises(matcher):
    with pytest.raises(InputValidationError):
        matcher.match(None)


def test_non_string_title_raises(matcher):
    with pytest.raises(InputValidationError):
        matcher.match(12345)


def test_too_long_title_raises(matcher):
    with pytest.raises(InputValidationError):
        matcher.match("x" * 2000)
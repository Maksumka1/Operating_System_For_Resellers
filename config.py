from pathlib import Path

# Базові шляхи та глобальні налаштування
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

DB_FILE = DATA_DIR / "hardware.db"
STATS_FILE = DATA_DIR / "stats.json"
CLEANED_STATE_FILE = DATA_DIR / "cleaned_state.json"
HTML_FILE = DATA_DIR / "olx_page_source.html"

PARSER_SETTINGS = {
    "request_delay": 2.0,
    "analyzer_delay": 0.5,
    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

BANNED_KEYWORDS = [
    "куплю", "обмін", "оренда", "шукаю", "несправна", "на запчастини", 
    "прогріта", "після майнінгу", "відвал", "артефакти", "копія"
]

VIDEOCARDS = [
    "gt_610", "gt_710", "gt_720", "gt_730", "gt_740","gt_1030", "gtx_745", "gtx_770", "gtx_750_ti", "gtx_750", "gtx_760","gtx_780_ti","gtx_780", "gtx_950", "gtx_960", "gtx_970",
    "gtx_980_ti", "gtx_980", "gtx_1050_ti", "gtx_1050", "gtx_1060", "gtx_1060_3gb", "gtx_1070_ti", "gtx_1070", "gtx_1080_ti", "gtx_1080",
    "gtx_1630", "gtx_1650_super", "gtx_1650", "gtx_1660_super", "gtx_1660_ti", "gtx_1660", "rtx_2060_super", "rtx_2060", "rtx_2070_super",
    "rtx_2070", "rtx_2080_ti", "rtx_2080_super", "rtx_2080", "rtx_3050_6gb", "rtx_3080_12gb", "rtx_3050", "rtx_3060_ti", "rtx_3060", "rtx_3070_ti",
    "rtx_3070", "rtx_3080_ti", "rtx_3080", "rtx_3090_ti", "rtx_3090", "rtx_4060_ti", "rtx_4060", "rtx_4070_ti_super",
    "rtx_4070_ti", "rtx_4070_super", "rtx_4070", "rtx_4080_super", "rtx_4080", "rtx_4090", "rtx_5090", "rtx_5080", "rtx_5070_ti", "rtx_5070", 
    "rtx_5060_ti", "rtx_5060", "rtx_5050", "rx_460", "rx_470", "rx_480", "rx_550", "rx_560", "rx_570", "rx_580", "rx_590", "rx_5500_xt", "rx_5500", 
    "rx_5600_xt", "rx_5300", "rx_5600", "rx_5700_xt", "rx_5700", "rx_6400", "rx_6500_xt", "rx_6650_xt", "rx_6600_xt", "rx_6600", "rx_6750_xt", "rx_6700_xt",
    "rx_6700", "rx_6800_xt", "rx_6800", "rx_6950_xt", "rx_6900_xt", "rx_7600_xt", "rx_7600", "rx_7700_xt", "rx_7800_xt",
    "rx_7900_gre", "rx_7900_xtx", "rx_7900_xt", "rx_9060_xt", "rx_9070_xt", "rx_9070",
    "quadro_k620", "quadro_k2000", "quadro_k2200", "quadro_k4000", "quadro_k4200", "quadro_k5000", "quadro_k6000",
    "quadro_m2000", "quadro_m4000", "quadro_m5000", "quadro_m6000",
    "quadro_p620", "quadro_p1000", "quadro_p2000", "quadro_p2200", "quadro_p4000", "quadro_p5000", "quadro_p6000",
    "quadro_rtx_3000", "quadro_rtx_4000", "quadro_rtx_5000", "quadro_rtx_6000",
]

INTEL_CPUS = [
    "i3_6098p", "i3_6100t", "i3_6100", "i3_6300t", "i3_6300", "i3_6320", "i3_7100t", "i3_7100", "i3_7300t", 
    "i3_7300", "i3_7320", "i3_8100t", "i3_8100", "i3_8350k", "i3_8300t", "i3_8300", "i3_9100f", "i3_9100t", 
    "i3_9100", "i3_9350k", "i3_10105f", "i3_10105t", "i3_10105", "i3_10100t", "i3_10100f", "i3_10100", 
    "i3_10300t", "i3_10300", "i3_10320", "i3_12100f", "i3_12100t", "i3_12100", "i3_12300f", "i3_12300t", 
    "i3_12300", "i3_13100f", "i3_13100t", "i3_13100", "i3_14100f", "i3_14100t", "i3_14100", "i5_2300", 
    "i5_2310", "i5_2320", "i5_2400", "i5_2500", "i5_2500k", "i5_3330", "i5_3340", "i5_3450", "i5_3470", 
    "i5_3550", "i5_3570", "i5_3570k", "i5_4430", "i5_4440", "i5_4460", "i5_4570", "i5_4590", "i5_4670", 
    "i5_4670k", "i5_4690", "i5_4690k", "i5_6400t", "i5_6400", "i5_6500t", "i5_6500", "i5_6600t", "i5_6600k", "i5_6600", 
    "i5_7400t", "i5_7400", "i5_7500t", "i5_7500", "i5_7600t", "i5_7600k", "i5_7600", "i5_8400t", "i5_8500t", 
    "i5_8500", "i5_8600t", "i5_8600k", "i5_8600", "i5_8400", "i5_9400t", "i5_9500f", "i5_9500t", "i5_9500", 
    "i5_9600kf", "i5_9600t", "i5_9400f", "i5_9400", "i5_9600k", "i5_9600", "i5_10400f", "i5_10400t", 
    "i5_10400", "i5_10500t", "i5_10500", "i5_10600kf", "i5_10600k", "i5_10600t", "i5_10600", "i5_11400f", 
    "i5_11400t", "i5_11400", "i5_11500t", "i5_11500", "i5_11600kf", "i5_11600k", "i5_11600f", "i5_11600t", 
    "i5_11600", "i5_12400f", "i5_12400t", "i5_12400", "i5_12500t", "i5_12500", "i5_12600kf", "i5_12600k", 
    "i5_12600t", "i5_12600", "i5_13400f", "i5_13400t", "i5_13400", "i5_13500t", "i5_13500", "i5_13600kf", 
    "i5_13600k", "i5_13600f", "i5_13600t", "i5_13600", "i5_14400f", "i5_14400t", "i5_14400", "i5_14500t", 
    "i5_14500", "i5_14600kf", "i5_14600k", "i5_14600f", "i5_14600t", "i5_14600", "i7_2600", "i7_2600k", "i7_2700k",
    "i7_3770", "i7_3770k", "i7_4770", "i7_4770k", "i7_4790", "i7_4790k", "i7_6700k", "i7_6700t", 
    "i7_6700", "i7_7700k", "i7_7700t", "i7_7700", "i7_8086k", "i7_8700k", "i7_8700t", "i7_8700", "i7_9700kf", 
    "i7_9700k", "i7_9700f", "i7_9700t", "i7_9700", "i7_10700kf", "i7_10700k", "i7_10700f", "i7_10700t", 
    "i7_10700", "i7_11700kf", "i7_11700k", "i7_11700f", "i7_11700t", "i7_11700", "i7_12700kf", "i7_12700k", 
    "i7_12700f", "i7_12700t", "i7_12700", "i7_13700kf", "i7_13700k", "i7_13700f", "i7_13700t", "i7_13700", 
    "i7_14700kf", "i7_14700k", "i7_14700f", "i7_14700t", "i7_14700", "i9_9900kf", "i9_9900f", "i9_9900t",
    "i9_10900kf", "i9_10900f", "i9_10900t", "i9_11900kf", "i9_11900f", "i9_11900t", "i9_12900kf", "i9_12900f", 
    "i9_12900t", "i9_13900kf", "i9_13900f", "i9_13900t", "i9_14900kf", "i9_14900f", "i9_14900t", "i9_9900k", 
    "i9_9900", "i9_10900k", "i9_10900", "i9_11900k", "i9_11900", "i9_12900k", "i9_12900", "i9_13900k", 
    "i9_13900", "i9_14900k", "i9_14900"
]

AMD_CPUS = [
    "ryzen_3_1200", "ryzen_3_1300x", "ryzen_3_2200ge", "ryzen_3_2200g", "ryzen_3_2300x", "ryzen_3_3100", 
    "ryzen_3_3300x", "ryzen_3_4300ge", "ryzen_3_4300g", "ryzen_3_5300ge", "ryzen_3_5300g", "ryzen_3_7300x", 
    "ryzen_3_7300", "ryzen_3_8300ge", "ryzen_3_8300g", "ryzen_5_1400", "ryzen_5_1500x", "ryzen_5_1600af", 
    "ryzen_5_1600x", "ryzen_5_1600", "ryzen_5_2400ge", "ryzen_5_2400g", "ryzen_5_2500x", "ryzen_5_2600x", 
    "ryzen_5_2600", "ryzen_5_3400ge", "ryzen_5_3400g", "ryzen_5_3500x", "ryzen_5_3500", "ryzen_5_3600xt", 
    "ryzen_5_3600x", "ryzen_5_3600", "ryzen_5_4500", "ryzen_5_4600g", "ryzen_5_5500", "ryzen_5_5500gt", 
    "ryzen_5_5600g", "ryzen_5_5600gt", "ryzen_5_5600", "ryzen_5_5600x", "ryzen_5_5600xt", "ryzen_5_5700g", 
    "ryzen_5_7500f", "ryzen_5_7600", "ryzen_5_7600x", "ryzen_7_1700", "ryzen_7_1700x", "ryzen_7_1800x", 
    "ryzen_7_2700", "ryzen_7_2700x", "ryzen_7_3700x", "ryzen_7_3800x", "ryzen_7_3800xt", "ryzen_7_4700g", 
    "ryzen_7_5700", "ryzen_7_5700g", "ryzen_7_5700x", "ryzen_7_5800", "ryzen_7_5800x", "ryzen_7_5800x3d", 
    "ryzen_7_7700", "ryzen_7_7700x", "ryzen_7_7800x3d", "ryzen_9_3900", "ryzen_9_3900x", "ryzen_9_3950x",
    "ryzen_9_5900", "ryzen_9_5900x", "ryzen_9_5950x", "ryzen_9_7900", "ryzen_9_7900x", "ryzen_9_7900x3d",
    "ryzen_9_7950x", "ryzen_9_7950x3d","ryzen_9_9900x", "ryzen_9_9900x3d", "ryzen_9_9950x", "ryzen_9_9950x3d"
]

XEON_CPUS = [
    "xeon_e3_1220", "xeon_e3_1230", "xeon_e3_1240", "xeon_e3_1270", "xeon_e3_1280", "xeon_e3_1290",
    "xeon_e3_1220_v2", "xeon_e3_1230_v2", "xeon_e3_1240_v2", "xeon_e3_1270_v2", "xeon_e3_1280_v2", "xeon_e3_1290_v2",
    "xeon_e3_1220_v3", "xeon_e3_1230_v3", "xeon_e3_1240_v3", "xeon_e3_1270_v3", "xeon_e3_1280_v3",
    "xeon_e3_1220_v5", "xeon_e3_1230_v5", "xeon_e3_1240_v5", "xeon_e3_1270_v5",
    "xeon_e3_1220_v6", "xeon_e3_1230_v6", "xeon_e3_1240_v6", "xeon_e3_1270_v6",

    "xeon_e5_2620", "xeon_e5_2630", "xeon_e5_2640", "xeon_e5_2650",
    "xeon_e5_2660", "xeon_e5_2670", "xeon_e5_2680", "xeon_e5_2690",
    "xeon_e5_2620_v2", "xeon_e5_2630_v2", "xeon_e5_2640_v2", "xeon_e5_2650_v2",
    "xeon_e5_2660_v2", "xeon_e5_2670_v2", "xeon_e5_2680_v2", "xeon_e5_2690_v2",
    "xeon_e5_2620_v3", "xeon_e5_2630_v3", "xeon_e5_2640_v3", "xeon_e5_2650_v3",
    "xeon_e5_2660_v3", "xeon_e5_2670_v3", "xeon_e5_2680_v3", "xeon_e5_2690_v3",
    "xeon_e5_2620_v4", "xeon_e5_2630_v4", "xeon_e5_2640_v4", "xeon_e5_2650_v4",
    "xeon_e5_2660_v4", "xeon_e5_2670_v4", "xeon_e5_2680_v4", "xeon_e5_2690_v4",
]

MOTHERBOARDS = [
    "h61", "b65", "q65", "q67", "h67", "p67", "z68", "b75", "q75", "q77", "h77", "z75", "z77",
    "h81", "b85", "q85", "q87", "h87", "z87", "h97", "z97",
    "h110", "b150", "q150", "h170", "q170", "z170",
    "b250", "h270", "z270", "h310", "b360", "b365", "h370", "q370", "z370", "z390",
    "h410", "b460", "h470", "q470", "z490", "h510", "b560", "h570", "q570", "z590",
    "h610", "b660", "h670", "q670", "z690", "b760", "h770", "z790",
    "x58", "x79", "x99", "x299",
    "c202", "c204", "c206", "c222", "c224", "c226", "c232", "c236", "c242", "c246", "c621", "c622", "c741", "c742",
    "w480", "w580", "w680",
    "760g", "770", "780g", "785g", "790x", "790fx", "870", "880g", "890gx", "890fx", "970", "990x", "990fx",
    "a55", "a58", "a68h", "a75", "a78", "a85x", "a88x",
    "a320", "b350", "x370", "b450", "x470", "a520", "b550", "x570",
    "a620", "b650", "b650e", "x670", "x670e", "b840", "b850", "x870", "x870e"
]

SOCKETS = [
    "lga775", "lga1150", "lga1151", "lga1151v2", "lga1155", "lga1156", "lga1200", "lga1700",
    "lga1356", "lga1366", "lga1567", "lga2011", "lga2011-3", "lga2066", "lga3647", "lga4189", "lga4677",
    "socket775", "socket1150", "socket1151", "socket1155", "socket1156", "socket1200", "socket1700",
    "socket1366", "socket2011", "socket2011-3", "socket2066",
    "am2", "am2+", "am3", "am3+", "am4", "am5",
    "fm1", "fm2", "fm2+",
    "swrx8", "str4", "trx4", "strx4"
]

CHIPSET_TO_SOCKET = {
    # LGA 775
    "p45": "lga775", "g41": "lga775", "p35": "lga775",
    # LGA 1155
    "h61": "lga1155", "b75": "lga1155", "z77": "lga1155", "h77": "lga1155", "z68": "lga1155", "p67": "lga1155",
    # LGA 1150
    "h81": "lga1150", "b85": "lga1150", "z87": "lga1150", "z97": "lga1150", "h97": "lga1150",
    # LGA 1151 (100/200 series) & LGA 1151v2 (300 series)
    "h110": "lga1151", "b150": "lga1151", "b250": "lga1151", "z170": "lga1151", "z270": "lga1151",
    "h310": "lga1151v2", "b360": "lga1151v2", "b365": "lga1151v2", "z370": "lga1151v2", "z390": "lga1151v2",
    # LGA 1200
    "h410": "lga1200", "b460": "lga1200", "z490": "lga1200", "h510": "lga1200", "b560": "lga1200", "z590": "lga1200",
    # LGA 1700
    "h610": "lga1700", "b660": "lga1700", "h670": "lga1700", "z690": "lga1700", "b760": "lga1700", "z790": "lga1700",
    # X-Series / Servers
    "x79": "lga2011", "x99": "lga2011-3", "x299": "lga2066", "x58": "lga1366",
    # AM3 / AM3+
    "760g": "am3+", "970": "am3+", "990fx": "am3+",
    # FM2 / FM2+
    "a55": "fm2", "a58": "fm2", "a68h": "fm2+", "a88x": "fm2+",
    # AM4
    "a320": "am4", "b350": "am4", "x370": "am4", "b450": "am4", "x470": "am4", "a520": "am4", "b550": "am4", "x570": "am4",
    # AM5
    "a620": "am5", "b650": "am5", "b650e": "am5", "x670": "am5", "x670e": "am5", "b840": "am5", "b850": "am5", "x870": "am5", "x870e": "am5"
}

PSUS = [
    "400w", "450w", "500w", "550w", "600w", "650w", "700w", "750w", "800w", "850w", "1000w", "1050w", "1100w", "1150w", "1200w", "1250w", "1300w", "1350w", "1400w"
    ]

STORAGES = [
    "ssd_120gb", "ssd_128gb", "ssd_240gb", "ssd_256gb", "ssd_480gb", "ssd_500gb", "ssd_512gb", "ssd_1tb", "ssd_2tb",
    "hdd_500gb", "hdd_1tb", "hdd_2tb"
]

HARDWARE_TARGETS = {}

def make_variants(name: str, replaces: list) -> list:
    """Генерує валідаційні ключові слова з урахуванням розкладки клавіатури"""
    raw = name.replace("_", " ")
    dash = name.replace("_", "-")
    joined = name.replace("_", "")
    
    variants = [raw, dash, joined]
    for eng, ukr in replaces:
        variants.extend([v.replace(eng, ukr) for v in variants.copy()])
    return list(set(variants))

# 1. Генерація для відеокарт (videokarty / gpu)
for card in VIDEOCARDS:
    card_clean = card.replace("sурер", "super")
    keywords = make_variants(card_clean, [("gtx", "гтх"), ("rtx", "ртх"), ("rx", "рх"), ("ti", "ті"), ("super", "sурер")])
    HARDWARE_TARGETS[card] = {
        "item_type": "gpu",
        "subcategory": "videokarty",
        "required_keywords": keywords
    }

# 2. Генерація для Intel проців (protsessory / cpu)
for cpu in INTEL_CPUS:
    keywords = make_variants(cpu, [("i3", "і3"), ("i5", "і5"), ("i7", "і7"), ("i9", "і9"), ("k", "к"), ("t", "т"), ("f", "ф")])
    HARDWARE_TARGETS[cpu] = {
        "item_type": "cpu",
        "subcategory": "protsessory",
        "required_keywords": keywords
    }

# 3. Генерація для AMD проців (protsessory / cpu)
for cpu in AMD_CPUS:
    keywords = make_variants(cpu, [("ryzen", "руzen"), ("x", "х")])
    HARDWARE_TARGETS[cpu] = {
        "item_type": "cpu",
        "subcategory": "protsessory",
        "required_keywords": keywords
    }

# 4. Генерація для Xeon проців (protsessory / cpu)
for cpu in XEON_CPUS:
    keywords = make_variants(cpu, [("xeon", "ксеон"), ("xeon", "зеон"), ("v", "в"), ("e", "е")])
    HARDWARE_TARGETS[cpu] = {
        "item_type": "cpu",
        "subcategory": "protsessory",
        "required_keywords": keywords
    }

for mb in MOTHERBOARDS:
    keywords = make_variants(mb, [("b", "б"), ("h", "х"), ("z", "з"), ("a", "а"), ("x", "х")])
    HARDWARE_TARGETS[mb] = {
        "item_type": "motherboard",
        "subcategory": "materinskie-platy",
        "required_keywords": keywords
    }

# 5. Блоки живлення
for psu in PSUS:
    keywords = make_variants(psu, [("w", "вт"), ("w", "ват"), ("w", "в")])
    HARDWARE_TARGETS[psu] = {
        "item_type": "psu",
        "subcategory": "bloki-pitaniya",
        "required_keywords": keywords
    }

# 6. Накопичувачі
for st in STORAGES:
    keywords = make_variants(st, [("gb", "гб"), ("tb", "тб"), ("ssd", "ссд"), ("hdd", "хдд")])
    HARDWARE_TARGETS[st] = {
        "item_type": "storage",
        "subcategory": "zhestkie-diski",
        "required_keywords": keywords
    }
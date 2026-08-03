import re
import os
from dotenv import load_dotenv
from supabase import create_client
from pathlib import Path
from hardware_matchers import normalize_title

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

DB_FILE = DATA_DIR / "hardware.db"
STATS_FILE = DATA_DIR / "stats.json"
CLEANED_STATE_FILE = DATA_DIR / "cleaned_state.json"
HTML_FILE = DATA_DIR / "olx_page_source.html"

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SECRET_KEY") or os.getenv("SUPABASE_PUBLISHABLE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY or "")

PARSER_SETTINGS = {
    "request_delay": 2.0,
    "analyzer_delay": 0.5,
    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

BANNED_KEYWORDS = [
    "куплю", "обмін", "оренда", "шукаю", "несправна", "на запчастини", 
    "прогріта", "після майнінгу", "відвал", "артефакти", "копія"
]

def load_all_gpus_from_db():
    """Завантажує всі розпізнані відеокарти з таблиці gpu_specs."""
    try:
        res = supabase.table("gpu_specs").select("slug").execute()
        rows = res.data or []
        return [row["slug"] for row in rows if row.get("slug")]
    except Exception as e:
        print(f"⚠️ [CONFIG WARN] Не вдалося завантажити відеокарти з DB: {e}")
        return []

# Динамічно завантажуємо відеокарти з бази замість великого масиву VIDEOCARDS
DB_VIDEOCARDS = load_all_gpus_from_db()
if DB_VIDEOCARDS:
    VIDEOCARDS = DB_VIDEOCARDS


def load_all_cpus_from_db():
    """Завантажує всі 3200+ десктопних процесорів з таблиці cpu_specs."""
    try:
        # Витягуємо лише slugs та бренди
        res = supabase.table("cpu_specs").select("slug, brand, raw_name").execute()
        rows = res.data or []
        
        intel_list = []
        amd_list = []
        xeon_list = []

        for row in rows:
            slug = row["slug"]
            raw_name = row["raw_name"].lower()

            if "xeon" in raw_name:
                xeon_list.append(slug)
            elif row["brand"] == "AMD":
                amd_list.append(slug)
            else:
                intel_list.append(slug)

        return intel_list, amd_list, xeon_list
    except Exception as e:
        print(f"⚠️ [CONFIG WARN] Не вдалося завантажити процесори з DB: {e}")
        # Резервні дефолтні значення, якщо немає інету
        return [], [], []

# Динамічно завантажуємо списки при запуску проєкту
INTEL_CPUS, AMD_CPUS, XEON_CPUS = load_all_cpus_from_db()

MOTHERBOARDS = [
    "p55", "p45", "p35", "p965", "g41", "g31", "n68", "tb360",
    "h81_btc", "g6100", "k9ngm3", "m5a78l", "k10n78", "a99", "x99_bd3",
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
    "lga775", "lga1150", "lga1151", "lga1151v2", "lga1155", "lga1156", "lga1200", "lga1700", "lga1851",
    "lga1356", "lga1366", "lga1567", "lga2011", "lga2011-3", "lga2066", "lga3647", "lga4189", "lga4677",
    "socket775", "socket1150", "socket1151", "socket1155", "socket1156", "socket1200", "socket1700", "socket1851",
    "socket1366", "socket2011", "socket2011-3", "socket2066",
    "am2", "am2+", "am3", "am3+", "am4", "am5", "fm1", "fm2", "fm2+",
    "swrx8", "str4", "trx4", "strx4"
]

CHIPSET_TO_SOCKET = {
    "p45": "lga775", "g41": "lga775", "p35": "lga775",
    "h61": "lga1155", "b75": "lga1155", "z77": "lga1155", "h77": "lga1155", "z68": "lga1155", "p67": "lga1155",
    "h81": "lga1150", "b85": "lga1150", "z87": "lga1150", "z97": "lga1150", "h97": "lga1150",
    "h110": "lga1151", "b150": "lga1151", "b250": "lga1151", "z170": "lga1151", "z270": "lga1151",
    "h310": "lga1151v2", "b360": "lga1151v2", "b365": "lga1151v2", "z370": "lga1151v2", "z390": "lga1151v2",
    "h410": "lga1200", "b460": "lga1200", "z490": "lga1200", "h510": "lga1200", "b560": "lga1200", "z590": "lga1200",
    "h610": "lga1700", "b660": "lga1700", "h670": "lga1700", "z690": "lga1700", "b760": "lga1700", "z790": "lga1700",
    "x79": "lga2011", "x99": "lga2011-3", "x299": "lga2066", "x58": "lga1366",
    "760g": "am3+", "970": "am3+", "990fx": "am3+",
    "a55": "fm2", "a58": "fm2", "a68h": "fm2+", "a88x": "fm2+",
    "a320": "am4", "b350": "am4", "x370": "am4", "b450": "am4", "x470": "am4", "a520": "am4", "b550": "am4", "x570": "am4",
    "a620": "am5", "b650": "am5", "b650e": "am5", "x670": "am5", "x670e": "am5", "b840": "am5", "b850": "am5", "x870": "am5", "x870e": "am5"
}

PSUS = [
    "200w", "240w", "250w", "300w", "350w", "380w", "385w", "400w", "420w", "430w", 
    "450w", "460w", "500w", "520w", "530w", "550w", "600w", "620w", "650w", "700w", 
    "750w", "800w", "850w", "1000w", "1050w", "1100w", "1150w", "1200w", "1250w", 
    "1300w", "1350w", "1400w", "1500w", "1600w", "1650w", "2000w"
]

STORAGES = [
    "ssd_60gb", "ssd_64gb", "ssd_120gb", "ssd_128gb", "ssd_160gb", "ssd_200gb", "ssd_240gb", "ssd_250gb", "ssd_256gb", 
    "ssd_300gb", "ssd_320gb", "ssd_400gb", "ssd_480gb", "ssd_500gb", "ssd_512gb", "ssd_960gb", "ssd_1tb", "ssd_2tb", 
    "ssd_4tb", "ssd_8tb",
    "hdd_80gb", "hdd_120gb", "hdd_160gb", "hdd_200gb", "hdd_250gb", "hdd_300gb", "hdd_320gb", "hdd_400gb", "hdd_500gb", 
    "hdd_1tb", "hdd_2tb", "hdd_3tb", "hdd_4tb", "hdd_6tb", "hdd_8tb", "hdd_10tb", "hdd_12tb", "hdd_14tb", "hdd_16tb", 
    "hdd_18tb", "hdd_20tb"
]


RAMS = [
    # DDR3
    "ram_ddr3_4gb", "ram_ddr3_8gb", "ram_ddr3_16gb",
    # DDR4
    "ram_ddr4_4gb", "ram_ddr4_8gb", "ram_ddr4_16gb", "ram_ddr4_32gb", "ram_ddr4_64gb",
    # DDR5
    "ram_ddr5_8gb", "ram_ddr5_16gb", "ram_ddr5_32gb", "ram_ddr5_48gb", "ram_ddr5_64gb", "ram_ddr5_96gb"
]

# Генератори ключів для підтримуваних стародрукованих типів
def generate_mb_keywords(mb_code: str) -> list[str]:
    variants = set()
    raw = mb_code.replace("_", " ")
    dash = mb_code.replace("_", "-")
    joined = mb_code.replace("_", "")
    for base in [raw, dash, joined]:
        variants.add(base)
        match = re.match(r"^([a-z]+)(\d+)(.*)$", base, re.IGNORECASE)
        if match:
            letter, num, rest = match.groups()
            variants.update([
                f"{letter} {num}{rest}", f"{letter} {num} {rest}", f"{letter}{num} {rest}",
                f"{letter}{num}m", f"{letter} {num}m", f"{letter}{num} m",
            ])
    return list(variants)

def generate_psu_keywords(psu_code: str) -> list[str]:
    variants = set()
    num = re.sub(r"\D", "", psu_code)
    for unit in ["w", "вт", "ват", "watt", "wt", "в"]:
        variants.add(f"{num}{unit}")
        variants.add(f"{num} {unit}")
        variants.add(f"{num}{unit}.")
        variants.add(f"{num} {unit}.")
    return list(variants)

def generate_storage_keywords(st_code: str) -> list[str]:
    variants = set()
    st_type, cap = st_code.split("_")
    cap_num = re.sub(r"\D", "", cap)
    unit = "tb" if "tb" in cap else "gb"
    unit_ukr = "тб" if unit == "tb" else "гб"
    type_variants = ["ssd", "ссд", "nvme"] if st_type == "ssd" else ["hdd", "хдд", "жорсткий диск", "жесткий диск", "винчестер"]
    for t in type_variants:
        variants.add(f"{t} {cap_num}{unit}")
        variants.add(f"{t} {cap_num} {unit}")
        variants.add(f"{t} {cap_num}{unit_ukr}")
        variants.add(f"{t} {cap_num} {unit_ukr}")
        variants.add(f"{cap_num}{unit} {t}")
        variants.add(f"{cap_num} {unit} {t}")
    return list(variants)

# --- СЛОВНИК СІТКИ ТОВАРІВ ---
HARDWARE_TARGETS = {}

def _register_simple(items_list: list[str], item_type: str, subcategory: str):
    """Швидка реєстрація моделей GPU / CPU для Direct Lookup (O(1))."""
    for item in items_list:
        HARDWARE_TARGETS[item] = {
            "item_type": item_type,
            "subcategory": subcategory,
        }

def _register_legacy_targets(items_list: list[str], item_type: str, subcategory: str, kw_generator):
    """Реєстрація категорій, де поки використовується створювана картотека регулярних виразів."""
    for item in items_list:
        keywords = kw_generator(item)
        keywords_sorted = sorted(set(keywords), key=len, reverse=True)
        escaped_kws = [re.escape(kw.strip().lower()) for kw in keywords_sorted if kw.strip()]
        pattern_str = r"(?<![a-zA-Z0-9а-яА-ЯіІїЇєЄґҐ])(?:" + "|".join(escaped_kws) + r")(?![a-zA-Z0-9а-яА-ЯіІїЇєЄґҐ])"
        HARDWARE_TARGETS[item] = {
            "item_type": item_type,
            "subcategory": subcategory,
            "compiled_pattern": re.compile(pattern_str, re.IGNORECASE)
        }

# Реєстрація нових компонентів (O(1))
_register_simple(VIDEOCARDS, "gpu", "videokarty")
_register_simple(INTEL_CPUS, "cpu", "protsessory")
_register_simple(AMD_CPUS, "cpu", "protsessory")
_register_simple(XEON_CPUS, "cpu", "protsessory")
_register_simple(RAMS, "ram", "operativnaya-pamyat")

# Реєстрація старого механізму для Motherboards, PSU, Storage
_register_legacy_targets(MOTHERBOARDS, "motherboard", "materinskie-platy", generate_mb_keywords)
_register_legacy_targets(PSUS, "psu", "bloki-pitaniya", generate_psu_keywords)
_register_legacy_targets(STORAGES, "storage", "zhestkie-diski", generate_storage_keywords)

# Для відкатних категорій (Motherboards, Storage, PSU)
LEGACY_PRE_SORTED_TARGETS = [
    (k, v) for k, v in HARDWARE_TARGETS.items() if "compiled_pattern" in v
]
LEGACY_PRE_SORTED_TARGETS.sort(key=lambda x: (len(x[0]), "_" in x[0]), reverse=True)
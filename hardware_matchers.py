import re

# ---------------------------------------------------------
# 1. СИСТЕМА НОРМАЛІЗАЦІЇ
# ---------------------------------------------------------

CYRILLIC_TO_LATIN = str.maketrans({
    'х': 'x', 'Х': 'x',
    'с': 'c', 'С': 'c',
    'а': 'a', 'А': 'a',
    'е': 'e', 'Е': 'e',
    'о': 'o', 'О': 'o',
    'р': 'p', 'Р': 'p',
    'і': 'i', 'І': 'i',
    'в': 'b', 'В': 'b',
    'м': 'm', 'М': 'm',
    'т': 't', 'Т': 't',
    'у': 'y', 'У': 'y',
    'к': 'k', 'К': 'k',
    'н': 'h', 'Н': 'h'
})

NOISE_CHARS_PATTERN = re.compile(r"[®™©]", re.IGNORECASE)
SEPARATORS_PATTERN = re.compile(r"[-/\\(),.;:+_]")
MULTI_SPACE_PATTERN = re.compile(r"\s+")

BUNDLE_KEYWORDS_PATTERN = re.compile(
    r"\b(?:комплект|сет|set|збірка|сборка|мать\s*\+\s*проц|плата\s*\+\s*проц|проц\s*\+\s*мать|комплектом)\b"
    r"|"
    r"\b(?:\+\s*(?:озу|ram|кулер|охлад|водянка|память|памяттю|оператива|бж|видеокарта|відеокарта))\b",
    re.IGNORECASE
)

def replace_cyrillic_homoglyphs(text: str) -> str:
    return text.translate(CYRILLIC_TO_LATIN)

def normalize_title(text: str) -> str:
    if not text:
        return ""
    text = text.lower()

    # 1. Заміна одиниць виміру та префіксів ДО заміни омогліфів
    text = re.sub(r"(\d+)\s*(?:вт|ват|ватт|wt)\b", r"\1w", text)
    text = re.sub(r"\bна\s*(\d+)\s*w\b", r"\1w", text)
    text = re.sub(r"\bрх\b|\bрх(?=\d)", "rx ", text)
    text = re.sub(r"\bгтх\b|\bгтх(?=\d)", "gtx ", text)
    text = re.sub(r"\bртх\b|\bртх(?=\d)", "rtx ", text)
    text = re.sub(r"(\d+)\s*(гб|г)\b", r"\1gb", text)

    # 2. Виправлення описок та відсутніх префіксів серій
    text = re.sub(r"\bgt\s*(10[5-8]0|16[56]0|20[6-8]0|30[5-9]0|40[5-9]0|50[5-9]0)\b", r"gtx \1", text)
    text = re.sub(r"\br([79])(\d{3}\w*)\b", r"r\1 \2", text)

    # 3. Нормалізація омогліфів та розділювачів
    text = replace_cyrillic_homoglyphs(text)
    text = NOISE_CHARS_PATTERN.sub("", text)
    text = SEPARATORS_PATTERN.sub(" ", text)
    text = MULTI_SPACE_PATTERN.sub(" ", text).strip()
    return text


# ---------------------------------------------------------
# 2. УНІВЕРСАЛЬНІ REGEX ДЛЯ GPU
# ---------------------------------------------------------

VRAM_PATTERN = re.compile(r"\b(?P<vram_num>\d{1,2})\s*(?:gb|гб|г|g)\b", re.IGNORECASE)

NVIDIA_GPU_PATTERN = re.compile(
    r"\b(?:geforce\s+)?(?:nx)?(?P<family>rtx|gtx|gts|gt|fx)\s*(?P<number>\d{3,4})\s*(?P<suffix>ti\s*super|ti|super)?\b"
    r"|"
    r"\b(?P<number_alt>\d{3,4})\s*(?P<suffix_alt>ti\s*super|ti|super)?\s*(?P<family_alt>rtx|gtx|gts|gt)\b"
    r"|"
    r"\b(?P<number_direct>\d{3,4})\s*(?P<suffix_direct>ti\s*super|ti|super)\b"
    r"|"
    # Для голих точних моделей без GTX/RTX (наприклад, Zotac 1080 8gb, 4060 8gb)
    r"\b(?P<bare_num>1030|1050|1060|1070|1080|1630|1650|1660|2060|2070|2080|3050|3060|3070|3080|3090|4060|4070|4080|4090|5060|5070|5080|5090)\s*(?P<bare_suf>ti\s*super|ti|super)?\b",
    re.IGNORECASE
)

AMD_RX_PATTERN = re.compile(
    r"\b(?:radeon\s+)?(?:rx|rt)\s*(?P<number>\d{3,4})\s*(?P<suffix>xtx|xt|gre)?(?:\s*2048sp)?\b"
    r"|"
    r"\b(?P<number_alt>\d{3,4})\s*(?P<suffix_alt>xtx|xt|gre)?\s*(?:rx|rt)\b"
    r"|"
    r"\b(?:radeon\s+pro\s+)?w(?P<pro_num>\d{4})\b",
    re.IGNORECASE
)

MINING_GPU_PATTERN = re.compile(
    r"\b(?P<p_series>p10\d)\s*(?P<p_num>090|100)\b|\b(?P<cmp_fam>cmp)\s*(?P<cmp_num>\d{2,3}hx)\b",
    re.IGNORECASE
)

AMD_LEGACY_PATTERN = re.compile(
    r"\b(?:radeon\s+)?hd\s*(?P<hd_num>\d{4})\s*(?P<hd_suf>xtx|xt|pro)?\b"
    r"|"
    r"\b(?P<r_fam>r[579])\s*(?P<r_num>\d{3}|fury)\s*(?P<r_suf>x)?\b"
    r"|"
    r"\b(?:rx\s+)?vega\s*(?P<vega_num>56|64)\b",
    re.IGNORECASE
)

INTEL_ARC_PATTERN = re.compile(
    r"\b(?:intel\s+)?arc\s*(?P<model>a\d{3})\b|\b(?P<model_alt>a\d{3})\s*arc\b",
    re.IGNORECASE
)

def extract_gpu(normalized_title: str) -> list[str]:
    raw_candidates = []

    for match in NVIDIA_GPU_PATTERN.finditer(normalized_title):
        m = match.groupdict()
        if m.get('bare_num'):
            num = m['bare_num']
            suf = f"_{m['bare_suf']}" if m.get('bare_suf') else ""
            prefix = "gtx" if num.startswith(('10', '16', '9', '7')) else "rtx"
            raw_candidates.append(f"{prefix}_{num}{suf}")
        elif m.get('legacy_num'):
            raw_candidates.append(f"{m['legacy_fam']}_{m['legacy_num']}")
            raw_candidates.append(f"{m['legacy_num']}_{m['legacy_fam']}")
        elif m.get('number_direct'):
            raw_candidates.append(f"rtx_{m['number_direct']}_{m['suffix_direct']}")
            raw_candidates.append(f"gtx_{m['number_direct']}_{m['suffix_direct']}")
        else:
            family = m['family'] or m['family_alt']
            number = m['number'] or m['number_alt']
            suffix = m['suffix'] or m['suffix_alt']
            if family and number:
                key = f"{family}_{number}"
                if suffix:
                    key += f"_{suffix.replace(' ', '_')}"
                raw_candidates.append(key)

    for match in AMD_RX_PATTERN.finditer(normalized_title):
        m = match.groupdict()
        if m.get('pro_num'):
            raw_candidates.append(f"w{m['pro_num']}")
            raw_candidates.append(f"rx_w{m['pro_num']}")
        else:
            number = m['number'] or m['number_alt']
            suffix = m['suffix'] or m['suffix_alt']
            if number:
                key = f"rx_{number}"
                if suffix:
                    raw_candidates.append(f"{key}_{suffix}")
                raw_candidates.append(key)

    for match in MINING_GPU_PATTERN.finditer(normalized_title):
        m = match.groupdict()
        if m.get('p_series'):
            raw_candidates.append(f"{m['p_series']}_{m['p_num']}")
        elif m.get('cmp_fam'):
            raw_candidates.append(f"{m['cmp_fam']}_{m['cmp_num']}")

    for match in AMD_LEGACY_PATTERN.finditer(normalized_title):
        m = match.groupdict()
        if m.get('hd_num'):
            key = f"hd_{m['hd_num']}"
            if m['hd_suf']:
                raw_candidates.append(f"{key}_{m['hd_suf']}")
            raw_candidates.append(key)
        elif m.get('r_fam') and m.get('r_num'):
            key = f"{m['r_fam']}_{m['r_num']}"
            if m.get('r_suf'):
                key += f"_{m['r_suf']}"
            raw_candidates.append(key)
        elif m.get('vega_num'):
            raw_candidates.append(f"rx_vega_{m['vega_num']}")

    for match in INTEL_ARC_PATTERN.finditer(normalized_title):
        m = match.groupdict()
        model = m['model'] or m['model_alt']
        if model:
            raw_candidates.append(f"arc_{model}")

    vram_match = VRAM_PATTERN.search(normalized_title)
    vram_val = vram_match.group('vram_num') if vram_match else None

    final_keys = []
    for key in raw_candidates:
        if vram_val:
            final_keys.append(f"{key}_{vram_val}gb")
            final_keys.append(f"{key}_{vram_val}_gb")
        final_keys.append(key)

    return list(dict.fromkeys(final_keys))


# ---------------------------------------------------------
# 3. УНІВЕРСАЛЬНІ REGEX ДЛЯ CPU
# ---------------------------------------------------------

INTEL_CORE_PATTERN = re.compile(
    r"\b(?:intel\s+)?(?:core\s+)?(?:i+)?(?P<brand>i[3579])\s*(?P<number>\d{3,5})\s*(?P<suffix>xe|x|kf|k|f|t|qm|hq|mq|c|s)?\b"
    r"|"
    r"\b(?P<number_alt>\d{3,5})\s*(?P<suffix_alt>xe|x|kf|k|f|t|s)?\s*(?:core\s+)?(?P<brand_alt>i[3579])\b"
    r"|"
    r"\b(?:core\s+)?ultra\s*(?P<u_brand>[579])\s*(?P<u_num>\d{3})\s*(?P<u_suf>kf|k|f|t)?\b"
    r"|"
    r"\b(?:core\s+2\s+quad|q)\s*(?:0|o)?(?P<q_num>\d{4})\b"
    r"|"
    r"\b(?:core\s+2\s+duo)\s*(?P<c2d_num>\d{4})\b",
    re.IGNORECASE
)

INTEL_LOW_PATTERN = re.compile(
    r"\b(?:pentium|celeron)\s*(?:gold\s+)?(?P<p_code>[g|e]?\d{3,4}[a-z]?)\b"
    r"|"
    r"\b(?P<p_num>5300)\s*dual\s*core\b",
    re.IGNORECASE
)

AMD_RYZEN_PATTERN = re.compile(
    r"\b(?:amd\s+)?(?:ryzen|razen|rayzen|r)\s*(?P<series>[3579])?\s*(?P<number>[1-9]\d{3})\s*(?P<suffix>x3d|xt|af|gt|ge|g|x|f)?\b"
    r"|"
    r"\b(?P<number_alt>[1-9]\d{3})\s*(?P<suffix_alt>x3d|xt|af|gt|ge|g|x|f)?\s*(?:ryzen|r)\s*(?P<series_alt>[3579])?\b",
    re.IGNORECASE
)

AMD_OTHER_PATTERN = re.compile(
    r"\b(?:amd\s+)?fx\s*(?P<fx_num>\d{4})\b"
    r"|"
    r"\b(?:athlon\s+(?:64\s+)?(?:ii\s+)?(?:x[24]\s+)?)(?P<ath_num>\d{3,4}[a-z]?|\d{3}ge)\b"
    r"|"
    r"\b(?:amd\s+)?(?P<a_series>a\d{1,2})\s*(?P<a_num>\d{4})\b",
    re.IGNORECASE
)

INTEL_XEON_PATTERN = re.compile(
    r"\b(?:intel\s+)?(?:xeon|zeon|ксеон|зеон)\s*(?:e\s*)?(?P<series>[357])?\s*(?P<number>\d{4}[a-z]?)\s*(?:v(?P<version>\d))?\b"
    r"|"
    r"\b(?P<number_alt>\d{4}[a-z]?)\s*(?:v(?P<version_alt>\d))\s*(?:xeon|zeon|ксеон|зеон)?\b",
    re.IGNORECASE
)

def extract_intel_cpu(normalized_title: str) -> list[str]:
    candidates = []
    for match in INTEL_CORE_PATTERN.finditer(normalized_title):
        m = match.groupdict()
        if m.get('u_brand'):
            key = f"core_ultra_{m['u_brand']}_{m['u_num']}"
            if m['u_suf']: key += f"{m['u_suf']}"
            candidates.append(key)
        elif m.get('q_num'):
            candidates.append(f"core_2_quad_q{m['q_num']}")
        elif m.get('c2d_num'):
            candidates.append(f"core_2_duo_e{m['c2d_num']}")
        else:
            brand = m['brand'] or m['brand_alt']
            number = m['number'] or m['number_alt']
            suffix = m['suffix'] or m['suffix_alt'] or ""
            if brand and number:
                candidates.append(f"{brand}_{number}{suffix}")
                
    for match in INTEL_LOW_PATTERN.finditer(normalized_title):
        m = match.groupdict()
        if m.get('p_code'):
            code = m['p_code']
            if code.startswith(('g', 'e')):
                candidates.append(f"pentium_{code}")
                candidates.append(f"celeron_{code}")
            else:
                candidates.append(f"pentium_g{code}")
        elif m.get('p_num'):
            candidates.append(f"pentium_e{m['p_num']}")

    return candidates

def _infer_ryzen_series(number_str: str) -> str:
    """Визначає серію Ryzen (3/5/7/9) за першою цифрою моделі, якщо вона пропущена."""
    num = int(number_str)
    if num in (1200, 1300, 2200, 3100, 3200, 4100, 5300):
        return "3"
    elif num in (1400, 1500, 1600, 2600, 3500, 3600, 4500, 5500, 5600, 7500, 7600):
        return "5"
    elif num in (1700, 1800, 2700, 3700, 3800, 5700, 5800, 7700, 7800, 9700):
        return "7"
    elif num >= 3900:
        return "9"
    return "5"

def extract_ryzen_cpu(normalized_title: str) -> list[str]:
    candidates = []
    for match in AMD_RYZEN_PATTERN.finditer(normalized_title):
        m = match.groupdict()
        number = m['number'] or m['number_alt']
        series = m['series'] or m['series_alt'] or _infer_ryzen_series(number)
        suffix = m['suffix'] or m['suffix_alt'] or ""
        if number:
            candidates.append(f"ryzen_{series}_{number}{suffix}")
    return candidates

def extract_amd_other_cpu(normalized_title: str) -> list[str]:
    candidates = []
    for match in AMD_OTHER_PATTERN.finditer(normalized_title):
        m = match.groupdict()
        if m.get('fx_num'):
            candidates.append(f"fx_{m['fx_num']}")
        elif m.get('ath_num'):
            num = m['ath_num']
            candidates.append(f"athlon_x4_{num}")
            candidates.append(f"athlon_ii_x2_{num}")
            candidates.append(f"athlon_64_x2_{num}")
            candidates.append(f"athlon_{num}")
        elif m.get('a_series') and m.get('a_num'):
            candidates.append(f"{m['a_series']}_{m['a_num']}")
    return candidates

def extract_xeon_cpu(normalized_title: str) -> list[str]:
    candidates = []
    for match in INTEL_XEON_PATTERN.finditer(normalized_title):
        m = match.groupdict()
        series = m.get('series')
        number = m.get('number') or m.get('number_alt')
        version = m.get('version') or m.get('version_alt')

        if number:
            parts = ["xeon"]
            if series: parts.append(f"e{series}")
            parts.append(number)
            if version: parts.append(f"v{version}")
            candidates.append("_".join(parts))
            
            if not series and len(number) == 4 and number.startswith(('2', '1')):
                candidates.append(f"xeon_e5_{number}" + (f"_v{version}" if version else ""))
                candidates.append(f"xeon_e3_{number}" + (f"_v{version}" if version else ""))
    return candidates

def extract_cpu(normalized_title: str) -> list[str]:
    res = []
    res.extend(extract_intel_cpu(normalized_title))
    res.extend(extract_ryzen_cpu(normalized_title))
    res.extend(extract_amd_other_cpu(normalized_title))
    res.extend(extract_xeon_cpu(normalized_title))
    return list(dict.fromkeys(res))


# ---------------------------------------------------------
# 4. УНІВЕРСАЛЬНІ REGEX ДЛЯ MOTHERBOARDS
# ---------------------------------------------------------

MOTHERBOARD_PATTERN = re.compile(
    r"\b(?P<intel_chip>z790|z690|z590|z490|z390|z370|z270|z170|z97|z87|z77|z75|z68|"
    r"b760|b660|b560|b460|b365|b360|b250|b150|b85|b75|"
    r"h770|h670|h610|h570|h510|h470|h410|h370|h310|h270|h170|h110|h97|h87|h81|h77|h67|h61|"
    r"x299|x99|x79|x58|p67|p55|p45|p35|p965|g41|g31)(?:[a-z0-9_]*\b)?"
    r"|"
    r"\b(?P<amd_chip>x870e|x870|x670e|x670|x570|x470|x370|"
    r"b850|b840|b650e|b650|b550|b450|b350|"
    r"a620|a520|a320|a88x|a78|a75|a68h|a58|a55|"
    r"990fx|990x|890fx|890gx|880g|870|790fx|790gx|790x|785g|780g|770|760g)(?:[a-z0-9_]*\b)?"
    r"|"
    r"\b(?P<amd_legacy_970>970)\s*(?:am3|am3\+|плата|материнка|motherboard|mb)\b"
    r"|"
    r"\b(?P<custom_chip>n68c|n68|g6100|m68mt|m5a78l|m4a78lt|m4n68t|m2npv|p5kpl|p5qc|tb360)\b",
    re.IGNORECASE
)

def extract_motherboard(normalized_title: str) -> list[str]:
    candidates = []
    for match in MOTHERBOARD_PATTERN.finditer(normalized_title):
        m = match.groupdict()
        chip = m['intel_chip'] or m['amd_chip'] or m.get('amd_legacy_970') or m['custom_chip']
        if chip:
            chip_clean = chip.lower()
            
            if chip_clean.startswith("n68") or chip_clean in ["m68mt", "m4n68t"]:
                candidates.append("760g")
                candidates.append("n68")
            elif chip_clean in ["m5a78l", "m4a78lt"]:
                candidates.append("760g")
                candidates.append("780g")
            elif chip_clean == "p5kpl":
                candidates.append("g31")
            elif chip_clean == "p5qc":
                candidates.append("p45")
            elif chip_clean in ["g6100", "m2npv"]:
                candidates.append("g6100")
            else:
                candidates.append(chip_clean)

    return list(dict.fromkeys(candidates))


# ---------------------------------------------------------
# 5. УНІВЕРСАЛЬНІ REGEX ДЛЯ BLOKIV ZHYVLENNYA (PSU)
# ---------------------------------------------------------

PSU_PATTERN = re.compile(
    r"\b(?P<watt>\d{3,4})\s*(?:w|вт|ват|watt|wt|в)\b"
    r"|"
    r"\b(?:ctg|gpa|gpc|gps|gpx|iarena|task|element|proton|smart|core|vx|ud|bqt|aps|bdf|gpe|rs|kf|tx|hx|rm|cx|cv|sf|ssr|sp|gx|gm|gd|dq|pq|pn|fm|atx|mwe)\s*[-_]?\s*(?P<model_watt>\d{3,4})\b"
    r"|"
    r"\b(?P<prefix_watt>\d{3,4})\s*(?:w|вт|ват)?\s*(?:chieftec|zalman|seasonic|corsair|be\s+quiet|aerocool|cougar|deepcool|msi|asus|gigabyte|vinga|emerson)\b",
    re.IGNORECASE
)

NON_PC_PSU_PATTERN = re.compile(
    r"\b(?:ноутбук|ноутбука|камери|видеонаблюдения|відеонагляду|роутер|роутера|poe|инжектор|інжектор|кабель|шнур|перехідник|переходник|mikrotik|canon|lenovo|19v|12v|24v)\b",
    re.IGNORECASE
)

def extract_psu(normalized_title: str) -> list[str]:
    if NON_PC_PSU_PATTERN.search(normalized_title):
        return []

    candidates = []
    for match in PSU_PATTERN.finditer(normalized_title):
        m = match.groupdict()
        watt = m['watt'] or m['model_watt'] or m['prefix_watt']
        if watt:
            candidates.append(f"{watt}w")

    return list(dict.fromkeys(candidates))


# ---------------------------------------------------------
# 6. УНІВЕРСАЛЬНІ REGEX ДЛЯ STORAGE (SSD / HDD)
# ---------------------------------------------------------

STORAGE_CAPACITY_PATTERN = re.compile(
    r"\b(?P<gb_num>60|64|80|120|128|160|200|240|250|256|300|320|400|480|500|512|960|1000|1024)\s*(?:gb|гб|гігабайт|гигабайт)\b"
    r"|"
    r"\b(?P<tb_num>1|2|3|4|6|8|10|12|14|16|18|20)\s*(?:tb|тб|терабайт|тв)\b"
    r"|"
    r"\b2000\s*(?:gb|гб)\b",
    re.IGNORECASE
)

SSD_TYPE_PATTERN = re.compile(r"\b(?:ssd|ссд|nvme|m\.2|m2|evo|pro|patriot|kingston|apacer|goodram|netac)\b", re.IGNORECASE)
HDD_TYPE_PATTERN = re.compile(r"\b(?:hdd|хдд|жорстк|жестк|винчестер|seagate|barracuda|ironwolf|toshiba|hitachi|fujitsu|wd|western\s+digital)\b", re.IGNORECASE)

NON_STORAGE_PATTERN = re.compile(
    r"\b(?:карман|кишеня|салазки|caddy|контроллер|контролер|expander|плата|dvd|дискета|кабель|адаптер)\b",
    re.IGNORECASE
)

def extract_storage(normalized_title: str) -> list[str]:
    if NON_STORAGE_PATTERN.search(normalized_title):
        return []

    candidates = []
    is_ssd = bool(SSD_TYPE_PATTERN.search(normalized_title))
    is_hdd = bool(HDD_TYPE_PATTERN.search(normalized_title))

    pref_types = []
    if is_ssd: pref_types.append("ssd")
    if is_hdd: pref_types.append("hdd")
    if not pref_types: pref_types = ["ssd", "hdd"]

    for match in STORAGE_CAPACITY_PATTERN.finditer(normalized_title):
        m = match.groupdict()
        if m.get('gb_num'):
            cap = f"{m['gb_num']}gb"
        elif m.get('tb_num'):
            cap = f"{m['tb_num']}tb"
        else:
            cap = "2tb"

        for st_type in pref_types:
            candidates.append(f"{st_type}_{cap}")

    return list(dict.fromkeys(candidates))


# ---------------------------------------------------------
# 7. УНІВЕРСАЛЬНІ REGEX ДЛЯ RAM (ОПЕРАТИВНА ПАМ'ЯТЬ)
# ---------------------------------------------------------

RAM_TYPE_PATTERN = re.compile(r"\b(?P<type>ddr[345])\b", re.IGNORECASE)

RAM_KIT_PATTERN = re.compile(
    r"\b(?P<count>[248])\s*[*xхx]\s*(?P<single_cap>4|8|16|32|64)\s*(?:gb|гб)?\b",
    re.IGNORECASE
)

RAM_SINGLE_PATTERN = re.compile(
    r"\b(?P<cap>4|8|16|32|48|64|96)\s*(?:gb|гб|гігабайт|гигабайт)\b",
    re.IGNORECASE
)

NON_RAM_PATTERN = re.compile(
    r"\b(?:кулер|радіαтор|радиатор|тримач|держатель|планка\s+кріплення)\b",
    re.IGNORECASE
)

def extract_ram(normalized_title: str) -> list[str]:
    if NON_RAM_PATTERN.search(normalized_title):
        return []

    type_match = RAM_TYPE_PATTERN.search(normalized_title)
    if not type_match:
        return []
    
    ddr_type = type_match.group("type").lower()

    kit_match = RAM_KIT_PATTERN.search(normalized_title)
    if kit_match:
        count = int(kit_match.group("count"))
        single_cap = int(kit_match.group("single_cap"))
        total_cap = count * single_cap
        return [f"ram_{ddr_type}_{total_cap}gb"]

    single_match = RAM_SINGLE_PATTERN.search(normalized_title)
    if single_match:
        cap = single_match.group("cap")
        return [f"ram_{ddr_type}_{cap}gb"]

    return []


# ---------------------------------------------------------
# 8. ДЕТЕКТОР СУТНОСТІ BUNDLE (КОМПЛЕКТІВ)
# ---------------------------------------------------------

def detect_bundle_components(title_clean: str, hardware_targets: dict) -> dict | None:
    gpus = [c for c in extract_gpu(title_clean) if c in hardware_targets]
    cpus = [c for c in extract_cpu(title_clean) if c in hardware_targets]
    mbs = [c for c in extract_motherboard(title_clean) if c in hardware_targets]

    categories_present = 0
    if gpus: categories_present += 1
    if cpus: categories_present += 1
    if mbs: categories_present += 1

    has_bundle_keyword = bool(BUNDLE_KEYWORDS_PATTERN.search(title_clean))

    if categories_present >= 2 or (has_bundle_keyword and categories_present >= 1):
        primary_cpu = cpus[0] if cpus else None
        primary_mb = mbs[0] if mbs else None
        primary_gpu = gpus[0] if gpus else None

        parts = []
        if primary_cpu: parts.append(primary_cpu)
        if primary_mb: parts.append(primary_mb)
        if primary_gpu: parts.append(primary_gpu)

        bundle_key = "bundle_" + "_".join(parts) if parts else "bundle_generic"

        return {
            "bundle_key": bundle_key,
            "components": {
                "cpu": primary_cpu,
                "motherboard": primary_mb,
                "gpu": primary_gpu
            }
        }

    return None
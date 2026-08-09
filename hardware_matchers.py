"""
hardware_matchers.py

Модуль для витягування апаратних ключів із назв товарів.
Рефакторинг із фокусом на: читабельність, типізацію, масштабованість,
базову безпеку (валідація вхідних даних, захист від ReDoS через обмеження довжини).
"""

from __future__ import annotations

import re
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Pattern, Set

# ---------------------------------------------------------------------------
# Безпека та валідація
# ---------------------------------------------------------------------------

class InputValidationError(ValueError):
    """Некоректні вхідні дані."""
    pass


class SecurityLimits:
    """Обмеження для запобігання зловживанням (ReDoS, memory bloat)."""
    MAX_TITLE_LENGTH: int = 10_000
    MAX_RESULTS_PER_CATEGORY: int = 50


def _validate_title(title: Optional[str]) -> str:
    """Перевіряє, обрізає та нормалізує вхідний рядок."""
    if title is None:
        return ""
    if not isinstance(title, str):
        title = str(title)
    
    # Автоматично обрізаємо занадто довгий текст замість падіння помилкою
    if len(title) > SecurityLimits.MAX_TITLE_LENGTH:
        return title[:SecurityLimits.MAX_TITLE_LENGTH]
        
    return title


# ---------------------------------------------------------------------------
# Нормалізація
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class NormalizationConfig:
    """Конфігурація нормалізації тексту."""
    cyrillic_map: Dict[str, str] = field(default_factory=lambda: {
        'х': 'x', 'Х': 'x', 'с': 'c', 'С': 'c', 'а': 'a', 'А': 'a',
        'е': 'e', 'Е': 'e', 'о': 'o', 'О': 'o', 'р': 'p', 'Р': 'p',
        'і': 'i', 'І': 'i', 'в': 'b', 'В': 'b', 'м': 'm', 'М': 'm',
        'т': 't', 'Т': 't', 'у': 'y', 'У': 'y', 'к': 'k', 'К': 'k',
        'н': 'h', 'Н': 'h',
    })
    noise_chars: Pattern[str] = field(
        default_factory=lambda: re.compile(r"[®™©]", re.IGNORECASE)
    )
    separators: Pattern[str] = field(
        default_factory=lambda: re.compile(r"[-/\\(),.;:+_]")
    )
    multi_space: Pattern[str] = field(
        default_factory=lambda: re.compile(r"\s+")
    )


class TextNormalizer:
    """Нормалізує назви товарів для подальшого парсингу."""

    def __init__(self, config: Optional[NormalizationConfig] = None) -> None:
        self.cfg = config or NormalizationConfig()
        self._trans_table = str.maketrans(self.cfg.cyrillic_map)

    def normalize(self, raw_title: str) -> str:
        """Повертає очищену нижньорегістрову строку."""
        text = raw_title.lower()

        # 1. Одиниці виміру та префікси (ДО омогліфів)
        text = re.sub(r"(\d+)\s*(?:вт|ват|ватт|wt)\b", r"\1w", text)
        text = re.sub(r"\bна\s*(\d+)\s*w\b", r"\1w", text)
        text = re.sub(r"\bрх\b|\bрх(?=\d)", "rx ", text)
        text = re.sub(r"\bгтх\b|\bгтх(?=\d)", "gtx ", text)
        text = re.sub(r"\bртх\b|\bртх(?=\d)", "rtx ", text)
        text = re.sub(r"(\d+)\s*(гб|г)\b", r"\1gb", text)

        # 2. Виправлення типових описок
        text = re.sub(
            r"\bgt\s*(10[5-8]0|16[56]0|20[6-8]0|30[5-9]0|40[5-9]0|50[5-9]0)\b",
            r"gtx \1", text
        )
        text = re.sub(r"\br([79])(\d{3}\w*)\b", r"r\1 \2", text)

        # 3. Омогліфи, шум, роздільники
        text = text.translate(self._trans_table)
        text = self.cfg.noise_chars.sub("", text)
        text = self.cfg.separators.sub(" ", text)
        text = self.cfg.multi_space.sub(" ", text).strip()

        return text


# ---------------------------------------------------------------------------
# Базовий екстрактор
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class ExtractionResult:
    """Результат роботи екстрактора."""
    category: str
    keys: List[str]


class BaseExtractor(ABC):
    """Базовий клас для всіх апаратних екстракторів."""

    CATEGORY: str = "base"

    @abstractmethod
    def extract(self, normalized_title: str) -> List[str]:
        """Повертає список унікальних ключів."""
        ...

    def _limit(self, items: List[str]) -> List[str]:
        """Обмежує кількість результатів та дедублікує."""
        seen: Set[str] = set()
        out: List[str] = []
        for item in items:
            if item not in seen and len(out) < SecurityLimits.MAX_RESULTS_PER_CATEGORY:
                seen.add(item)
                out.append(item)
        return out


# ---------------------------------------------------------------------------
# GPU Extractor
# ---------------------------------------------------------------------------

class GpuExtractor(BaseExtractor):
    CATEGORY = "gpu"

    # --- patterns ---
    _VRAM = re.compile(r"\b(?P<vram_num>\d{1,2})\s*(?:gb|гб|г|g)\b", re.IGNORECASE)

    _NVIDIA = re.compile(
        r"\b(?:geforce\s+)?(?:nx)?(?P<family>rtx|gtx|gts|gt|fx)\s*(?P<number>\d{3,4})\s*(?P<suffix>ti\s*super|ti|super)?\b"
        r"|"
        r"\b(?P<number_alt>\d{3,4})\s*(?P<suffix_alt>ti\s*super|ti|super)?\s*(?P<family_alt>rtx|gtx|gts|gt)\b"
        r"|"
        r"\b(?P<number_direct>\d{3,4})\s*(?P<suffix_direct>ti\s*super|ti|super)\b"
        r"|"
        r"\b(?P<bare_num>1030|1050|1060|1070|1080|1630|1650|1660|2060|2070|2080|3050|3060|3070|3080|3090|4060|4070|4080|4090|5060|5070|5080|5090)\s*(?P<bare_suf>ti\s*super|ti|super)?\b",
        re.IGNORECASE,
    )

    _AMD_RX = re.compile(
        r"\b(?:radeon\s+)?(?:rx|rt)\s*(?P<number>\d{3,4})\s*(?P<suffix>xtx|xt|gre)?(?:\s*2048sp)?\b"
        r"|"
        r"\b(?P<number_alt>\d{3,4})\s*(?P<suffix_alt>xtx|xt|gre)?\s*(?:rx|rt)\b"
        r"|"
        r"\b(?:radeon\s+pro\s+)?w(?P<pro_num>\d{4})\b",
        re.IGNORECASE,
    )

    _MINING = re.compile(
        r"\b(?P<p_series>p10\d)\s*(?P<p_num>090|100)\b|\b(?P<cmp_fam>cmp)\s*(?P<cmp_num>\d{2,3}hx)\b",
        re.IGNORECASE,
    )

    _AMD_LEGACY = re.compile(
        r"\b(?:radeon\s+)?hd\s*(?P<hd_num>\d{4})\s*(?P<hd_suf>xtx|xt|pro)?\b"
        r"|"
        r"\b(?P<r_fam>r[579])\s*(?P<r_num>\d{3}|fury)\s*(?P<r_suf>x)?\b"
        r"|"
        r"\b(?:rx\s+)?vega\s*(?P<vega_num>56|64)\b",
        re.IGNORECASE,
    )

    _INTEL_ARC = re.compile(
        r"\b(?:intel\s+)?arc\s*(?P<model>a\d{3})\b|\b(?P<model_alt>a\d{3})\s*arc\b",
        re.IGNORECASE,
    )

    def extract(self, normalized_title: str) -> List[str]:
        raw: List[str] = []

        # NVIDIA
        for m in self._NVIDIA.finditer(normalized_title):
            g = m.groupdict()
            if g.get("bare_num"):
                num = g["bare_num"]
                suf = f"_{g['bare_suf']}" if g.get("bare_suf") else ""
                prefix = "gtx" if num.startswith(("10", "16", "9", "7")) else "rtx"
                raw.append(f"{prefix}_{num}{suf}")
            elif g.get("number_direct"):
                raw.append(f"rtx_{g['number_direct']}_{g['suffix_direct']}")
                raw.append(f"gtx_{g['number_direct']}_{g['suffix_direct']}")
            else:
                family = g.get("family") or g.get("family_alt")
                number = g.get("number") or g.get("number_alt")
                suffix = g.get("suffix") or g.get("suffix_alt")
                if family and number:
                    key = f"{family}_{number}"
                    if suffix:
                        key += f"_{suffix.replace(' ', '_')}"
                    raw.append(key)

        # AMD RX
        for m in self._AMD_RX.finditer(normalized_title):
            g = m.groupdict()
            if g.get("pro_num"):
                raw.append(f"w{g['pro_num']}")
                raw.append(f"rx_w{g['pro_num']}")
            else:
                number = g.get("number") or g.get("number_alt")
                suffix = g.get("suffix") or g.get("suffix_alt")
                if number:
                    key = f"rx_{number}"
                    if suffix:
                        raw.append(f"{key}_{suffix}")
                    raw.append(key)

        # Mining
        for m in self._MINING.finditer(normalized_title):
            g = m.groupdict()
            if g.get("p_series"):
                raw.append(f"{g['p_series']}_{g['p_num']}")
            elif g.get("cmp_fam"):
                raw.append(f"{g['cmp_fam']}_{g['cmp_num']}")

        # AMD Legacy
        for m in self._AMD_LEGACY.finditer(normalized_title):
            g = m.groupdict()
            if g.get("hd_num"):
                key = f"hd_{g['hd_num']}"
                if g.get("hd_suf"):
                    raw.append(f"{key}_{g['hd_suf']}")
                raw.append(key)
            elif g.get("r_fam") and g.get("r_num"):
                key = f"{g['r_fam']}_{g['r_num']}"
                if g.get("r_suf"):
                    key += f"_{g['r_suf']}"
                raw.append(key)
            elif g.get("vega_num"):
                raw.append(f"rx_vega_{g['vega_num']}")

        # Intel Arc
        for m in self._INTEL_ARC.finditer(normalized_title):
            g = m.groupdict()
            model = g.get("model") or g.get("model_alt")
            if model:
                raw.append(f"arc_{model}")

        # VRAM
        vram_match = self._VRAM.search(normalized_title)
        vram_val = vram_match.group("vram_num") if vram_match else None

        final: List[str] = []
        for key in raw:
            if vram_val:
                final.append(f"{key}_{vram_val}gb")
                final.append(f"{key}_{vram_val}_gb")
            final.append(key)

        return self._limit(final)


# ---------------------------------------------------------------------------
# CPU Extractor
# ---------------------------------------------------------------------------

class CpuExtractor(BaseExtractor):
    CATEGORY = "cpu"

    _INTEL_CORE = re.compile(
        r"\b(?:intel\s+)?(?:core\s+)?(?:i+)?(?P<brand>i[3579])\s*(?P<number>\d{3,5})\s*(?P<suffix>xe|x|kf|k|f|t|qm|hq|mq|c|s)?\b"
        r"|"
        r"\b(?P<number_alt>\d{3,5})\s*(?P<suffix_alt>xe|x|kf|k|f|t|s)?\s*(?:core\s+)?(?P<brand_alt>i[3579])\b"
        r"|"
        r"\b(?:core\s+)?ultra\s*(?P<u_brand>[579])\s*(?P<u_num>\d{3})\s*(?P<u_suf>kf|k|f|t|h)?\b"
        r"|"
        r"\b(?:core\s+2\s+quad|q)\s*(?:0|o)?(?P<q_num>\d{4})\b"
        r"|"
        r"\b(?:core\s+2\s+duo)\s*(?P<c2d_num>\d{4})\b",
        re.IGNORECASE,
    )

    _INTEL_LOW = re.compile(
        r"\b(?:pentium|celeron)\s*(?:gold\s+)?(?P<p_code>[g|e]?\d{3,4}[a-z]?)\b"
        r"|"
        r"\b(?P<p_num>5300)\s*dual\s*core\b",
        re.IGNORECASE,
    )

    _AMD_RYZEN = re.compile(
        r"\b(?:amd\s+)?(?:ryzen|razen|rayzen|r)\s*(?P<series>[3579])?\s*(?P<number>[1-9]\d{3})\s*(?P<suffix>x3d|xt|af|gt|ge|g|x|f)?\b"
        r"|"
        r"\b(?P<number_alt>[1-9]\d{3})\s*(?P<suffix_alt>x3d|xt|af|gt|ge|g|x|f)?\s*(?:ryzen|r)\s*(?P<series_alt>[3579])?\b",
        re.IGNORECASE,
    )

    _AMD_OTHER = re.compile(
        r"\b(?:amd\s+)?fx\s*(?P<fx_num>\d{4})\b"
        r"|"
        r"\b(?:athlon\s+(?:64\s+)?(?:ii\s+)?(?:x[24]\s+)?)(?P<ath_num>\d{3,4}[a-z]?|\d{3}ge)\b"
        r"|"
        r"\b(?:amd\s+)?(?P<a_series>a\d{1,2})\s*(?P<a_num>\d{4})\b",
        re.IGNORECASE,
    )

    _INTEL_XEON = re.compile(
        r"\b(?:intel\s+)?(?:xeon|zeon|ксеон|зеон)\s*(?:e\s*)?(?P<series>[357])?\s*(?P<number>\d{4}[a-z]?)\s*(?:v(?P<version>\d))?\b"
        r"|"
        r"\b(?P<number_alt>\d{4}[a-z]?)\s*(?:v(?P<version_alt>\d))\s*(?:xeon|zeon|ксеон|зеон)?\b",
        re.IGNORECASE,
    )

    @staticmethod
    def _infer_ryzen_series(number_str: str) -> str:
        num = int(number_str)
        if num in (1200, 1300, 2200, 3100, 3200, 4100, 5300):
            return "3"
        if num in (1400, 1500, 1600, 2600, 3500, 3600, 4500, 5500, 5600, 7500, 7600):
            return "5"
        if num in (1700, 1800, 2700, 3700, 3800, 5700, 5800, 7700, 7800, 9700):
            return "7"
        if num >= 3900:
            return "9"
        return "5"

    def extract(self, normalized_title: str) -> List[str]:
        raw: List[str] = []

        for m in self._INTEL_CORE.finditer(normalized_title):
            g = m.groupdict()
            if g.get("u_brand"):
                key = f"core_ultra_{g['u_brand']}_{g['u_num']}"
                if g.get("u_suf"):
                    key += f"{g['u_suf']}"
                raw.append(key)
            elif g.get("q_num"):
                raw.append(f"core_2_quad_q{g['q_num']}")
            elif g.get("c2d_num"):
                raw.append(f"core_2_duo_e{g['c2d_num']}")
            else:
                brand = g.get("brand") or g.get("brand_alt")
                number = g.get("number") or g.get("number_alt")
                suffix = g.get("suffix") or g.get("suffix_alt") or ""
                if brand and number:
                    raw.append(f"{brand}_{number}{suffix}")

        for m in self._INTEL_LOW.finditer(normalized_title):
            g = m.groupdict()
            if g.get("p_code"):
                code = g["p_code"]
                if code.startswith(("g", "e")):
                    raw.append(f"pentium_{code}")
                    raw.append(f"celeron_{code}")
                else:
                    raw.append(f"pentium_g{code}")
            elif g.get("p_num"):
                raw.append(f"pentium_e{g['p_num']}")

        for m in self._AMD_RYZEN.finditer(normalized_title):
            g = m.groupdict()
            number = g.get("number") or g.get("number_alt")
            series = g.get("series") or g.get("series_alt") or self._infer_ryzen_series(number)
            suffix = g.get("suffix") or g.get("suffix_alt") or ""
            if number:
                raw.append(f"ryzen_{series}_{number}{suffix}")

        for m in self._AMD_OTHER.finditer(normalized_title):
            g = m.groupdict()
            if g.get("fx_num"):
                raw.append(f"fx_{g['fx_num']}")
            elif g.get("ath_num"):
                num = g["ath_num"]
                raw.extend([
                    f"athlon_x4_{num}",
                    f"athlon_ii_x2_{num}",
                    f"athlon_64_x2_{num}",
                    f"athlon_{num}",
                ])
            elif g.get("a_series") and g.get("a_num"):
                raw.append(f"{g['a_series']}_{g['a_num']}")

        for m in self._INTEL_XEON.finditer(normalized_title):
            g = m.groupdict()
            series = g.get("series")
            number = g.get("number") or g.get("number_alt")
            version = g.get("version") or g.get("version_alt")
            if number:
                parts = ["xeon"]
                if series:
                    parts.append(f"e{series}")
                parts.append(number)
                if version:
                    parts.append(f"v{version}")
                raw.append("_".join(parts))
                if not series and len(number) == 4 and number.startswith(("2", "1")):
                    for fam in ("e5", "e3"):
                        raw.append(f"xeon_{fam}_{number}" + (f"_v{version}" if version else ""))

        return self._limit(raw)


# ---------------------------------------------------------------------------
# Motherboard Extractor
# ---------------------------------------------------------------------------

class MotherboardExtractor(BaseExtractor):
    CATEGORY = "motherboard"

    _CHIPSET = re.compile(
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
        re.IGNORECASE,
    )

    _CUSTOM_MAP: Dict[str, List[str]] = {
        "n68": ["760g", "n68"],
        "n68c": ["760g", "n68"],
        "m68mt": ["760g", "n68"],
        "m4n68t": ["760g", "n68"],
        "m5a78l": ["760g", "780g"],
        "m4a78lt": ["760g", "780g"],
        "p5kpl": ["g31"],
        "p5qc": ["p45"],
        "g6100": ["g6100"],
        "m2npv": ["g6100"],
    }

    def extract(self, normalized_title: str) -> List[str]:
        raw: List[str] = []
        for m in self._CHIPSET.finditer(normalized_title):
            g = m.groupdict()
            chip = (
                g.get("intel_chip")
                or g.get("amd_chip")
                or g.get("amd_legacy_970")
                or g.get("custom_chip")
            )
            if not chip:
                continue
            chip_clean = chip.lower()
            if chip_clean in self._CUSTOM_MAP:
                raw.extend(self._CUSTOM_MAP[chip_clean])
            else:
                raw.append(chip_clean)
        return self._limit(raw)


# ---------------------------------------------------------------------------
# PSU Extractor
# ---------------------------------------------------------------------------

class PsuExtractor(BaseExtractor):
    CATEGORY = "psu"

    _PSU = re.compile(
        r"\b(?P<watt>\d{3,4})\s*(?:w|вт|ват|watt|wt|в)\b"
        r"|"
        r"\b(?:ctg|gpa|gpc|gps|gpx|iarena|task|element|proton|smart|core|vx|ud|bqt|aps|bdf|gpe|rs|kf|tx|hx|rm|cx|cv|sf|ssr|sp|gx|gm|gd|dq|pq|pn|fm|atx|mwe)\s*[-_]?\s*(?P<model_watt>\d{3,4})\b"
        r"|"
        r"\b(?P<prefix_watt>\d{3,4})\s*(?:w|вт|ват)?\s*(?:chieftec|zalman|seasonic|corsair|be\s+quiet|aerocool|cougar|deepcool|msi|asus|gigabyte|vinga|emerson)\b",
        re.IGNORECASE,
    )

    _NON_PC = re.compile(
        r"\b(?:ноутбук|ноутбука|камери|видеонаблюдения|відеонагляду|роутер|роутера|poe|инжектор|інжектор|кабель|шнур|перехідник|переходник|mikrotik|canon|lenovo|19v|12v|24v)\b",
        re.IGNORECASE,
    )

    def extract(self, normalized_title: str) -> List[str]:
        if self._NON_PC.search(normalized_title):
            return []
        raw: List[str] = []
        for m in self._PSU.finditer(normalized_title):
            g = m.groupdict()
            watt = g.get("watt") or g.get("model_watt") or g.get("prefix_watt")
            if watt:
                raw.append(f"{watt}w")
        return self._limit(raw)


# ---------------------------------------------------------------------------
# Storage Extractor
# ---------------------------------------------------------------------------

class StorageExtractor(BaseExtractor):
    CATEGORY = "storage"

    _CAPACITY = re.compile(
        r"\b(?P<gb_num>60|64|80|120|128|160|200|240|250|256|300|320|400|480|500|512|960|1000|1024)\s*(?:gb|гб|гігабайт|гигабайт)\b"
        r"|"
        r"\b(?P<tb_num>1|2|3|4|6|8|10|12|14|16|18|20)\s*(?:tb|тб|терабайт|тв)\b"
        r"|"
        r"\b2000\s*(?:gb|гб)\b",
        re.IGNORECASE,
    )

    _SSD = re.compile(
        r"\b(?:ssd|ссд|nvme|m\.2|m2|evo|pro|patriot|kingston|apacer|goodram|netac)\b",
        re.IGNORECASE,
    )
    _HDD = re.compile(
        r"\b(?:hdd|хдд|жорстк|жестк|винчестер|seagate|barracuda|ironwolf|toshiba|hitachi|fujitsu|wd|western\s+digital)\b",
        re.IGNORECASE,
    )
    _NON_STORAGE = re.compile(
        r"\b(?:карман|кишеня|салазки|caddy|контроллер|контролер|expander|плата|dvd|дискета|кабель|адаптер)\b",
        re.IGNORECASE,
    )

    def extract(self, normalized_title: str) -> List[str]:
        if self._NON_STORAGE.search(normalized_title):
            return []

        raw: List[str] = []
        is_ssd = bool(self._SSD.search(normalized_title))
        is_hdd = bool(self._HDD.search(normalized_title))
        types = []
        if is_ssd:
            types.append("ssd")
        if is_hdd:
            types.append("hdd")
        if not types:
            types = ["ssd", "hdd"]

        for m in self._CAPACITY.finditer(normalized_title):
            g = m.groupdict()
            if g.get("gb_num"):
                cap = f"{g['gb_num']}gb"
            elif g.get("tb_num"):
                cap = f"{g['tb_num']}tb"
            else:
                cap = "2tb"
            for st_type in types:
                raw.append(f"{st_type}_{cap}")

        return self._limit(raw)


# ---------------------------------------------------------------------------
# RAM Extractor
# ---------------------------------------------------------------------------

class RamExtractor(BaseExtractor):
    CATEGORY = "ram"

    _DDR = re.compile(r"\b(?P<type>ddr[345])\b", re.IGNORECASE)
    _KIT = re.compile(
        r"\b(?P<count>[1248])\s*[*xхx]\s*(?P<single_cap>4|8|16|32|64)\s*(?:gb|гб)?\b",
        re.IGNORECASE,
    )
    _SINGLE = re.compile(
        r"\b(?P<cap>4|8|16|32|48|64|96)\s*(?:gb|гб|гігабайт|гигабайт)\b",
        re.IGNORECASE,
    )
    _NON_RAM = re.compile(
        r"\b(?:кулер|радіαтор|радиатор|тримач|держатель|планка\s+кріплення)\b",
        re.IGNORECASE,
    )

    def extract(self, normalized_title: str) -> List[str]:
        if self._NON_RAM.search(normalized_title):
            return []

        type_match = self._DDR.search(normalized_title)
        if not type_match:
            return []
        ddr_type = type_match.group("type").lower()

        kit_match = self._KIT.search(normalized_title)
        if kit_match:
            count = int(kit_match.group("count"))
            single_cap = int(kit_match.group("single_cap"))
            total = count * single_cap
            return [f"ram_{ddr_type}_{total}gb"]

        single_match = self._SINGLE.search(normalized_title)
        if single_match:
            cap = single_match.group("cap")
            return [f"ram_{ddr_type}_{cap}gb"]

        return []


# ---------------------------------------------------------------------------
# Bundle Detector
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class BundleResult:
    bundle_key: str
    components: Dict[str, Optional[str]]


class BundleDetector:
    """Визначає, чи є товар комплектом (bundle) кількох компонентів."""

    _BUNDLE_KEYWORDS = re.compile(
        r"\b(?:комплект|сет|set|збірка|сборка|мать\s*\+\s*проц|плата\s*\+\s*проц|проц\s*\+\s*мать|комплектом)\b"
        r"|"
        r"\b(?:\+\s*(?:озу|ram|кулер|охлад|водянка|память|памяттю|оператива|бж|видеокарта|відеокарта))\b",
        re.IGNORECASE,
    )

    def __init__(
        self,
        gpu_extractor: Optional[GpuExtractor] = None,
        cpu_extractor: Optional[CpuExtractor] = None,
        mb_extractor: Optional[MotherboardExtractor] = None,
    ) -> None:
        self.gpu_ex = gpu_extractor or GpuExtractor()
        self.cpu_ex = cpu_extractor or CpuExtractor()
        self.mb_ex = mb_extractor or MotherboardExtractor()

    def detect(
        self, normalized_title: str, hardware_targets: Optional[Dict[str, Set[str]]] = None
    ) -> Optional[BundleResult]:
        """
        Якщо hardware_targets передано — фільтрує результати за дозволеними ключами.
        """
        gpus = self.gpu_ex.extract(normalized_title)
        cpus = self.cpu_ex.extract(normalized_title)
        mbs = self.mb_ex.extract(normalized_title)

        if hardware_targets:
            gpus = [c for c in gpus if c in hardware_targets.get("gpu", set())]
            cpus = [c for c in cpus if c in hardware_targets.get("cpu", set())]
            mbs = [c for c in mbs if c in hardware_targets.get("motherboard", set())]

        categories = sum(bool(x) for x in (gpus, cpus, mbs))
        has_keyword = bool(self._BUNDLE_KEYWORDS.search(normalized_title))

        if categories >= 2 or (has_keyword and categories >= 1):
            primary_cpu = cpus[0] if cpus else None
            primary_mb = mbs[0] if mbs else None
            primary_gpu = gpus[0] if gpus else None

            parts = [p for p in (primary_cpu, primary_mb, primary_gpu) if p]
            bundle_key = "bundle_" + "_".join(parts) if parts else "bundle_generic"

            return BundleResult(
                bundle_key=bundle_key,
                components={
                    "cpu": primary_cpu,
                    "motherboard": primary_mb,
                    "gpu": primary_gpu,
                },
            )
        return None


# ---------------------------------------------------------------------------
# Фасад — єдиний точний вход
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class HardwareProfile:
    """Повний профіль товару."""
    gpu: List[str] = field(default_factory=list)
    cpu: List[str] = field(default_factory=list)
    motherboard: List[str] = field(default_factory=list)
    psu: List[str] = field(default_factory=list)
    storage: List[str] = field(default_factory=list)
    ram: List[str] = field(default_factory=list)
    bundle: Optional[BundleResult] = None


class HardwareMatcher:
    """Головний клас: нормалізує заголовок і делегує витягування екстракторам."""

    def __init__(self) -> None:
        self.normalizer = TextNormalizer()
        self.gpu_ex = GpuExtractor()
        self.cpu_ex = CpuExtractor()
        self.mb_ex = MotherboardExtractor()
        self.psu_ex = PsuExtractor()
        self.storage_ex = StorageExtractor()
        self.ram_ex = RamExtractor()
        self.bundle_detector = BundleDetector(
            self.gpu_ex, self.cpu_ex, self.mb_ex
        )

    def match(self, title: str) -> HardwareProfile:
        """Публічний API."""
        validated = _validate_title(title)
        clean = self.normalizer.normalize(validated)

        return HardwareProfile(
            gpu=self.gpu_ex.extract(clean),
            cpu=self.cpu_ex.extract(clean),
            motherboard=self.mb_ex.extract(clean),
            psu=self.psu_ex.extract(clean),
            storage=self.storage_ex.extract(clean),
            ram=self.ram_ex.extract(clean),
            bundle=self.bundle_detector.detect(clean),
        )


# ---------------------------------------------------------------------------
# Глобальні функції для зворотної сумісності (Backward Compatibility API)
# ---------------------------------------------------------------------------

_default_normalizer = TextNormalizer()
_default_gpu_ex = GpuExtractor()
_default_cpu_ex = CpuExtractor()
_default_mb_ex = MotherboardExtractor()
_default_psu_ex = PsuExtractor()
_default_storage_ex = StorageExtractor()
_default_ram_ex = RamExtractor()


def normalize_title(title: str) -> str:
    """Нормалізує назву товару."""
    if not title:
        return ""
    validated = _validate_title(title)
    return _default_normalizer.normalize(validated)


def _safe_normalize(title: str) -> str:
    if not title:
        return ""
    try:
        return normalize_title(title)
    except InputValidationError:
        return ""


def extract_cpu(title: str) -> List[str]:
    """Витягує CPU з назви."""
    clean = _safe_normalize(title)
    return _default_cpu_ex.extract(clean) if clean else []


def extract_gpu(title: str) -> List[str]:
    """Витягує GPU з назви."""
    clean = _safe_normalize(title)
    return _default_gpu_ex.extract(clean) if clean else []


def extract_motherboard(title: str) -> List[str]:
    """Витягує материнську плату з назви."""
    clean = _safe_normalize(title)
    return _default_mb_ex.extract(clean) if clean else []


def extract_mb(title: str) -> List[str]:
    """Аліас для extract_motherboard."""
    return extract_motherboard(title)


def extract_psu(title: str) -> List[str]:
    """Витягує БЖ з назви."""
    clean = _safe_normalize(title)
    return _default_psu_ex.extract(clean) if clean else []


def extract_storage(title: str) -> List[str]:
    """Витягує накопичувачі (SSD/HDD) з назви."""
    clean = _safe_normalize(title)
    return _default_storage_ex.extract(clean) if clean else []


def extract_ram(title: str) -> List[str]:
    """Витягує ОЗП з назви."""
    clean = _safe_normalize(title)
    return _default_ram_ex.extract(clean) if clean else []
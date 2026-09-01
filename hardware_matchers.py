"""
hardware_matchers.py

Модуль для витягування апаратних ключів із назв товарів.
Рефакторинг із фокусом на: точність екстракції, відсутність хибних спрацювань,
правильну детекцію бандлів та розділення типів накопичувачів/ОЗП.
"""

from __future__ import annotations

import re
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Pattern, Set


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
    if len(title) > SecurityLimits.MAX_TITLE_LENGTH:
        return title[:SecurityLimits.MAX_TITLE_LENGTH]
    return title


# ---------------------------------------------------------------------------
# Нормалізація
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class NormalizationConfig:
    cyrillic_map: Dict[str, str] = field(default_factory=lambda: {
        'а': 'a', 'е': 'e', 'о': 'o', 'р': 'p', 'с': 'c', 
        'х': 'x', 'і': 'i', 'у': 'y', 'к': 'k',
    })
    noise_chars: Pattern[str] = field(
        default_factory=lambda: re.compile(r"[®™©]", re.IGNORECASE)
    )
    separators: Pattern[str] = field(
        default_factory=lambda: re.compile(r"[-/\\(),.;:_]")
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
        text = raw_title.lower()
        text = re.sub(r"[`'’ʼ]", "'", text)
        text = text.translate(self._trans_table)

        text = re.sub(r"(\d+)\s*(?:вт|ват|ватт|wt)\b", r"\1w", text)
        text = re.sub(r"\bна\s*(\d+)\s*w\b", r"\1w", text)
        text = re.sub(r"\b(rx|gtx|rtx)(?=\d)", r"\1 ", text)
        text = re.sub(r"(\d+)\s*(гб|г|gb)\b", r"\1gb", text)

        text = re.sub(
            r"\bgt\s*(10[5-8]0|16[56]0|20[6-8]0|30[5-9]0|40[5-9]0|50[5-9]0)\b",
            r"gtx \1", text
        )
        text = re.sub(r"\br([3579])\s*(\d{4}\w*)\b", r"ryzen \1 \2", text)

        text = self.cfg.noise_chars.sub("", text)
        text = self.cfg.separators.sub(" ", text)
        return self.cfg.multi_space.sub(" ", text).strip()


# ---------------------------------------------------------------------------
# Базовий екстрактор
# ---------------------------------------------------------------------------

class BaseExtractor(ABC):
    CATEGORY: str = "base"

    @abstractmethod
    def extract(self, normalized_title: str) -> List[str]:
        ...

    def _limit(self, items: List[str]) -> List[str]:
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

        for m in self._NVIDIA.finditer(normalized_title):
            g = m.groupdict()
            if g.get("bare_num"):
                num = g["bare_num"]
                suf = f"_{g['bare_suf']}" if g.get("bare_suf") else ""
                prefix = "gtx" if num.startswith(("10", "16", "9", "7")) else "rtx"
                raw.append(f"{prefix}_{num}{suf}".replace(" ", "_"))
            elif g.get("number_direct"):
                raw.append(f"rtx_{g['number_direct']}_{g['suffix_direct']}".replace(" ", "_"))
                raw.append(f"gtx_{g['number_direct']}_{g['suffix_direct']}".replace(" ", "_"))
            else:
                family = g.get("family") or g.get("family_alt")
                number = g.get("number") or g.get("number_alt")
                suffix = g.get("suffix") or g.get("suffix_alt")
                if family and number:
                    suf_clean = f"_{suffix.strip().replace(' ', '_').lower()}" if suffix else ""
                    raw.append(f"{family}_{number}{suf_clean}")


        for m in self._AMD_RX.finditer(normalized_title):
            g = m.groupdict()
            if g.get("pro_num"):
                raw.append(f"w{g['pro_num']}")
            else:
                number = g.get("number") or g.get("number_alt")
                suffix = g.get("suffix") or g.get("suffix_alt")
                if number:
                    key = f"rx_{number}"
                    if suffix:
                        raw.append(f"{key}_{suffix.lower()}")
                    else:
                        raw.append(key)

        for m in self._MINING.finditer(normalized_title):
            g = m.groupdict()
            if g.get("p_series"):
                raw.append(f"{g['p_series']}_{g['p_num']}")
            elif g.get("cmp_fam"):
                raw.append(f"{g['cmp_fam']}_{g['cmp_num']}")

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

        for m in self._INTEL_ARC.finditer(normalized_title):
            g = m.groupdict()
            model = g.get("model") or g.get("model_alt")
            if model:
                raw.append(f"arc_{model}")

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
        r"\b(?:pentium|celeron)\s*(?:gold\s+)?(?P<p_code>[ge]?\d{3,4}[a-z]?)\b"
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
                    suf_clean = suffix.strip().lower()
                    raw.append(f"{brand}_{number}{suf_clean}")

        for m in self._INTEL_LOW.finditer(normalized_title):
            g = m.groupdict()
            if g.get("p_code"):
                code = g["p_code"]
                if code.startswith(("g", "e")):
                    raw.append(f"pentium_{code}")
                    raw.append(f"celeron_{code}")
                else:
                    raw.append(f"pentium_g{code}")
                    raw.append(f"celeron_g{code}")
            elif g.get("p_num"):
                raw.append(f"pentium_e{g['p_num']}")

        for m in self._AMD_RYZEN.finditer(normalized_title):
            g = m.groupdict()
            number = g.get("number") or g.get("number_alt")
            series = g.get("series") or g.get("series_alt") or (self._infer_ryzen_series(number) if number else "5")
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
# Motherboard Extractor (Точні межі \b, сортування за спаданням довжини)
# ---------------------------------------------------------------------------

class MotherboardExtractor(BaseExtractor):
    CATEGORY = "motherboard"

    # Сортований перелік чипсетів (довші йдуть першими, щоб b850 не матчило як b85)
    _CHIPSET_LIST = [
        "x870e", "x670e", "b650e", "x870", "x670", "b850", "b840", "b650", "a620", "b550", "a520", "x570",
        "x470", "b450", "x370", "b350", "a320", "990fx", "890fx", "890gx", "790fx", "790gx",
        "z790", "h770", "b760", "z690", "h670", "b660", "h610", "z590", "h570", "b560", "h510",
        "z490", "h470", "b460", "h410", "z390", "z370", "h370", "b365", "b360", "h310",
        "z270", "h270", "b250", "z170", "h170", "b150", "h110", "z97", "h97", "z87", "h87", "b85", "h81",
        "z77", "z75", "h77", "z68", "p67", "h67", "b75", "h61", "x299", "x99", "x79", "x58",
        "p55", "p45", "p35", "p965", "g41", "g31", "tb360", "760g", "880g", "870", "770", "a88x", "a78", "a75", "a68h", "a58", "a55"
    ]
    
    _CHIPSET = re.compile(
        r"\b(?P<chip>" + "|".join(sorted(_CHIPSET_LIST, key=len, reverse=True)) + r")\b"
        r"|"
        r"\b(?P<amd_legacy_970>970)\s*(?:am3|am3\+|плата|материнка|motherboard|mb)\b"
        r"|"
        r"\b(?P<custom_chip>n68c|n68|g6100|m68mt|m5a78l|m4a78lt|m4n68t|m2npv|p5kpl|p5qc)\b",
        re.IGNORECASE,
    )

    _CUSTOM_MAP: Dict[str, List[str]] = {
        "n68": ["760g", "n68"],
        "n68c": ["760g", "n68"],
        "m68mt": ["760g", "n68"],
        "m4n68t": ["760g", "n68"],
        "m5a78l": ["760g", "m5a78l"],
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
            chip = g.get("chip") or g.get("amd_legacy_970") or g.get("custom_chip")
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
        r"\b(?P<watt>\d{3,4})\s*(?:w|вт|ват|watt|wt)\b"
        r"|"
        r"\b(?:ctg|gpa|gpc|gps|gpx|iarena|task|element|proton|smart|core|vx|ud|bqt|aps|bdf|gpe|rs|kf|tx|hx|rm|cx|cv|sf|ssr|sp|gx|gm|gd|dq|pq|pn|fm|atx|mwe)\s*[-_]?\s*(?P<model_watt>\d{3,4})\b"
        r"|"
        r"\b(?P<prefix_watt>\d{3,4})\s*(?:w|вт|ват)?\s*(?:chieftec|zalman|seasonic|corsair|be\s+quiet|aerocool|cougar|deepcool|msi|asus|gigabyte|vinga|emerson|superflower)\b",
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
# Storage Extractor (Ізоляція HDD від SSD та RAM)
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
        r"\b(?:ssd|ссд|nvme|m\.2|m2|evo|pro|patriot|kingston|apacer|goodram|netac|sxs1000|sn\d{3})\b",
        re.IGNORECASE,
    )
    _HDD = re.compile(
        r"\b(?:hdd|хдд|жорстк|жестк|винчестер|seagate|barracuda|ironwolf|skyhawk|toshiba|hitachi|fujitsu|wd|western\s+digital|3\.5)\b",
        re.IGNORECASE,
    )
    _RAM_EXCLUDE = re.compile(
        r"\b(?:ddr\d?|ram|озу|пам'ять|память|оперативн\w*|dimm|sodimm)\b",
        re.IGNORECASE,
    )
    _NON_STORAGE = re.compile(
        r"\b(?:карман|кишеня|салазки|caddy|контроллер|контролер|expander|плата\s+hdd|плата\s+жорсткого|плата\s+жесткого|dvd|дискета|кабель|адаптер)\b",
        re.IGNORECASE,
    )

    def extract(self, normalized_title: str) -> List[str]:
        # Якщо в описі явно вказано ОЗП або аксесуари — ігноруємо
        if self._NON_STORAGE.search(normalized_title) or self._RAM_EXCLUDE.search(normalized_title):
            return []

        raw: List[str] = []
        is_ssd = bool(self._SSD.search(normalized_title))
        is_hdd = bool(self._HDD.search(normalized_title))

        # Визначаємо типи: пріоритет за чіткими маркерами
        if is_hdd and not is_ssd:
            types = ["hdd"]
        elif is_ssd and not is_hdd:
            types = ["ssd"]
        elif is_hdd and is_ssd:
            # Наприклад "Вінчестер SSD"
            types = ["ssd"] if "ssd" in normalized_title or "ссд" in normalized_title else ["hdd"]
        else:
            types = ["hdd", "ssd"]

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
        r"\b(?:кулер|радіатор|радиатор|тримач|держатель|планка\s+кріплення)\b",
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
# Bundle Detector (Виправлено перевірку target_items)
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
        r"(?:\+\s*(?:озу|ram|кулер|охлад|водянка|память|пам'ять|памяттю|оператива|бж|видеокарта|відеокарта))\b"
        r"|"
        r"\+",
        re.IGNORECASE,
    )

    def __init__(
        self,
        gpu_extractor: Optional[GpuExtractor] = None,
        cpu_extractor: Optional[CpuExtractor] = None,
        mb_extractor: Optional[MotherboardExtractor] = None,
        ram_extractor: Optional[RamExtractor] = None,
    ) -> None:
        self.gpu_ex = gpu_extractor or GpuExtractor()
        self.cpu_ex = cpu_extractor or CpuExtractor()
        self.mb_ex = mb_extractor or MotherboardExtractor()
        self.ram_ex = ram_extractor or RamExtractor()

    def detect_from_extracted(
        self,
        normalized_title: str,
        gpus: List[str],
        cpus: List[str],
        mbs: List[str],
        rams: Optional[List[str]] = None,
        hardware_targets: Optional[Dict[str, Any]] = None,
    ) -> Optional[BundleResult]:
        rams = rams or []

        # Якщо передано таргет-словник, перевіряємо валідність ключів
        if hardware_targets:
            if isinstance(next(iter(hardware_targets.values()), None), dict):
                # Плаский словник: {target_name: {"item_type": ...}}
                valid_gpus = {k for k, v in hardware_targets.items() if v.get("item_type") == "gpu"}
                valid_cpus = {k for k, v in hardware_targets.items() if v.get("item_type") == "cpu"}
                valid_mbs = {k for k, v in hardware_targets.items() if v.get("item_type") == "motherboard"}
            else:
                # Вкладений словник: {"gpu": {...}}
                valid_gpus = set(hardware_targets.get("gpu", []))
                valid_cpus = set(hardware_targets.get("cpu", []))
                valid_mbs = set(hardware_targets.get("motherboard", []))

            gpus = [c for c in gpus if c in valid_gpus]
            cpus = [c for c in cpus if c in valid_cpus]
            mbs = [c for c in mbs if c in valid_mbs]

        categories = sum(bool(x) for x in (gpus, cpus, mbs))
        has_keyword = bool(self._BUNDLE_KEYWORDS.search(normalized_title))

        # Комплект якщо: >= 2 основних компонентів АБО 1 основний + RAM + ключове слово (+)
        if has_keyword and (categories >= 1):
            primary_cpu = cpus[0] if cpus else None
            primary_mb = mbs[0] if mbs else None
            primary_gpu = gpus[0] if gpus else None
            primary_ram = rams[0] if rams else None

            # Формуємо стандартизований ключ бандла
            parts = []
            if primary_mb:
                parts.append(primary_mb)
            if primary_cpu:
                parts.append(primary_cpu)
            if primary_gpu:
                parts.append(primary_gpu)
            if primary_ram:
                parts.append(primary_ram)

            bundle_key = "_".join(parts) if parts else "bundle_generic"

            return BundleResult(
                bundle_key=bundle_key,
                components={
                    "cpu": primary_cpu,
                    "motherboard": primary_mb,
                    "gpu": primary_gpu,
                    "ram": primary_ram,
                },
            )
        return None

    def detect(
        self, normalized_title: str, hardware_targets: Optional[Dict[str, Any]] = None
    ) -> Optional[BundleResult]:
        gpus = self.gpu_ex.extract(normalized_title)
        cpus = self.cpu_ex.extract(normalized_title)
        mbs = self.mb_ex.extract(normalized_title)
        rams = self.ram_ex.extract(normalized_title)
        return self.detect_from_extracted(
            normalized_title, gpus, cpus, mbs, rams, hardware_targets
        )


# ---------------------------------------------------------------------------
# Backward Compatibility API
# ---------------------------------------------------------------------------

_default_normalizer = TextNormalizer()
_default_gpu_ex = GpuExtractor()
_default_cpu_ex = CpuExtractor()
_default_mb_ex = MotherboardExtractor()
_default_psu_ex = PsuExtractor()
_default_storage_ex = StorageExtractor()
_default_ram_ex = RamExtractor()
_default_bundle_detector = BundleDetector()


def normalize_title(title: str) -> str:
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
    clean = _safe_normalize(title)
    return _default_cpu_ex.extract(clean) if clean else []


def extract_gpu(title: str) -> List[str]:
    clean = _safe_normalize(title)
    return _default_gpu_ex.extract(clean) if clean else []


def extract_motherboard(title: str) -> List[str]:
    clean = _safe_normalize(title)
    return _default_mb_ex.extract(clean) if clean else []


def extract_mb(title: str) -> List[str]:
    return extract_motherboard(title)


def extract_psu(title: str) -> List[str]:
    clean = _safe_normalize(title)
    return _default_psu_ex.extract(clean) if clean else []


def extract_storage(title: str) -> List[str]:
    clean = _safe_normalize(title)
    return _default_storage_ex.extract(clean) if clean else []


def extract_ram(title: str) -> List[str]:
    clean = _safe_normalize(title)
    return _default_ram_ex.extract(clean) if clean else []


def detect_bundle_components(title: str, hardware_targets: dict | None = None) -> dict | None:
    clean = _safe_normalize(title)
    if not clean:
        return None
    res = _default_bundle_detector.detect(clean, hardware_targets)
    if res:
        return {
            "bundle_key": res.bundle_key,
            "components": res.components
        }
    return None
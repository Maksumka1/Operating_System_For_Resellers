"""
hardware_matchers.py — Виправлена та стабільна виробнича версія
"""

from __future__ import annotations

import re
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Pattern, Set


class InputValidationError(ValueError):
    pass


class SecurityLimits:
    MAX_TITLE_LENGTH: int = 10_000
    MAX_RESULTS_PER_CATEGORY: int = 50


def _validate_title(title: Optional[str]) -> str:
    if title is None:
        return ""
    if not isinstance(title, str):
        title = str(title)
    if len(title) > SecurityLimits.MAX_TITLE_LENGTH:
        return title[:SecurityLimits.MAX_TITLE_LENGTH]
    return title


@dataclass(frozen=True)
class NormalizationConfig:
    # ТІЛЬКИ справжні візуальні омогліфи!
    # Заборонено додавати 'в'->'b', 'г'->'g', 'д'->'d', бо це ламає кириличні одиниці вимірювання (вт, гб, ссд).
    cyrillic_map: Dict[str, str] = field(default_factory=lambda: {
        'а': 'a', 'е': 'e', 'о': 'o', 'р': 'p', 'с': 'c', 
        'х': 'x', 'і': 'i', 'у': 'y', 'к': 'k',
    })
    noise_chars: Pattern[str] = field(
        default_factory=lambda: re.compile(r"[®™©]", re.IGNORECASE)
    )
    separators: Pattern[str] = field(
        default_factory=lambda: re.compile(r"[-/\\(),.;:_+]")
    )
    multi_space: Pattern[str] = field(
        default_factory=lambda: re.compile(r"\s+")
    )


class TextNormalizer:
    def __init__(self, config: Optional[NormalizationConfig] = None) -> None:
        self.cfg = config or NormalizationConfig()
        self._trans_table = str.maketrans(self.cfg.cyrillic_map)

    def normalize(self, raw_title: str) -> str:
        text = raw_title.lower()
        text = re.sub(r"[`'’ʼ]", "'", text)

        # 1. Специфічні скорочення до будь-якої обробки
        text = re.sub(r"\bm[\s\._-]*2\b", "m2", text)
        text = re.sub(r"\b(\d+)\s*по\s*(\d+)\s*(?:gb|гб)?\b", r"\1x\2gb", text)  # "2 по 8" / "2 по 8гб" -> "2x8gb"

        # 2. Нормалізація одиниць вимірювання ДО заміни літер
        # Блоки живлення (вт, ват -> w)
        text = re.sub(r"(\d+)\s*(?:вт|ват|ватт|wt|w)\b", r"\1w", text)
        text = re.sub(r"\bна\s*(\d+)\s*w\b", r"\1w", text)

        # Пам'ять (гб, gb -> gb; тб, tb -> tb)
        text = re.sub(r"(\d+)\s*(?:гб|г|gb)\b", r"\1gb", text)
        text = re.sub(r"(\d+)\s*(?:тб|т|tb)\b", r"\1tb", text)

        # Типи накопичувачів
        text = re.sub(r"\b(?:ссд|ssd)\b", "ssd", text)
        text = re.sub(r"\b(?:хдд|hdd)\b", "hdd", text)

        # Префікси лінійок
        text = re.sub(r"\b(rx|gtx|rtx)(?=\d)", r"\1 ", text)
        text = re.sub(
            r"\bgt\s*(10[5-8]0|16[56]0|20[6-8]0|30[5-9]0|40[5-9]0|50[5-9]0)\b",
            r"gtx \1", text
        )
        text = re.sub(r"\br([3579])\s*(\d{4}\w*)\b", r"ryzen \1 \2", text)

        # 3. Заміна лише візуальних омогліфів
        text = text.translate(self._trans_table)

        # 4. Видалення шуму та роздільників
        text = self.cfg.noise_chars.sub("", text)
        text = self.cfg.separators.sub(" ", text)
        return self.cfg.multi_space.sub(" ", text).strip()


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


class GpuExtractor(BaseExtractor):
    CATEGORY = "gpu"

    _NVIDIA = re.compile(
        r"\b(?:geforce\s+)?(?P<family>rtx|gtx|gts|gt)\s*(?P<number>10[3-8]0|16[3-6]0|20[6-8]0|30[5-9]0|40[5-9]0|50[5-9]0|[79]\d0)\s*(?P<suffix>ti\s*super|ti|super)?\b",
        re.IGNORECASE,
    )

    _AMD_RX = re.compile(
        r"\b(?:radeon\s+)?rx\s*(?P<number>[4567]\d{2,3})\s*(?P<suffix>xtx|xt|gre)?(?:\s*2048sp)?\b",
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
            fam = g["family"].lower()
            num = g["number"]
            suf = f"_{g['suffix'].strip().replace(' ', '_').lower()}" if g.get("suffix") else ""
            key = f"{fam}_{num}{suf}"

            tail = normalized_title[m.end():m.end() + 15]
            vram_m = re.search(r"^\s*(?P<v>\d{1,2})\s*gb\b", tail)
            if vram_m:
                v = vram_m.group('v')
                raw.append(f"{key}_{v}_gb")
                raw.append(f"{key}_{v}gb")
            raw.append(key)

        # AMD RX
        for m in self._AMD_RX.finditer(normalized_title):
            g = m.groupdict()
            num = g["number"]
            suf = f"_{g['suffix'].strip().lower()}" if g.get("suffix") else ""
            key = f"rx_{num}{suf}"

            tail = normalized_title[m.end():m.end() + 15]
            vram_m = re.search(r"^\s*(?P<v>\d{1,2})\s*gb\b", tail)
            if vram_m:
                v = vram_m.group('v')
                raw.append(f"{key}_{v}_gb")
                raw.append(f"{key}_{v}gb")
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
                    raw.append(f"{key}_{g['hd_suf'].lower()}")
                else:
                    raw.append(key)
            elif g.get("r_fam") and g.get("r_num"):
                key = f"{g['r_fam'].lower()}_{g['r_num']}"
                if g.get("r_suf"):
                    key += f"_{g['r_suf'].lower()}"
                raw.append(key)
            elif g.get("vega_num"):
                raw.append(f"rx_vega_{g['vega_num']}")

        # Intel Arc
        for m in self._INTEL_ARC.finditer(normalized_title):
            g = m.groupdict()
            model = g.get("model") or g.get("model_alt")
            if model:
                raw.append(f"arc_{model.lower()}")

        return self._limit(raw)


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


class MotherboardExtractor(BaseExtractor):
    CATEGORY = "motherboard"

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
        r"\b(?P<chip>" + "|".join(sorted(_CHIPSET_LIST, key=len, reverse=True)) + r")(?:[-_\s]?[mak]|[-_\s]?(?:pro|plus|gaming|wifi|ds3h|hdv|k|e))?\b"
        r"|"
        r"\b(?:плата|материнка|mb|gigabyte|asus|msi|asrock)?\s*(?P<amd_legacy_970>970)[a-z]?\b"
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


class PsuExtractor(BaseExtractor):
    CATEGORY = "psu"

    _PSU = re.compile(
        r"\b(?P<watt>\d{3,4})\s*w\b"
        r"|"
        r"\b(?:ctg|gpa|gpc|gps|gpx|iarena|task|element|proton|smart|core|vx|ud|bqt|aps|bdf|gpe|rs|kf|tx|hx|rm|cx|cv|sf|ssr|sp|gx|gm|gd|dq|pq|pn|fm|atx|mwe)\s*[-_]?\s*(?P<model_watt>\d{3,4})\b"
        r"|"
        r"\b(?P<prefix_watt>\d{3,4})\s*(?:w)?\s*(?:chieftec|zalman|seasonic|corsair|be\s+quiet|aerocool|cougar|deepcool|msi|asus|gigabyte|vinga|emerson|superflower)\b",
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


class StorageExtractor(BaseExtractor):
    CATEGORY = "storage"

    _DIRECT_STORAGE = re.compile(
        r"\b(?P<type>ssd|nvme|m2|hdd)\s*(?P<cap>\d{2,4}gb|[124]tb)\b"
        r"|"
        r"\b(?P<cap_alt>\d{2,4}gb|[124]tb)\s*(?P<type_alt>ssd|nvme|m2|hdd)\b",
        re.IGNORECASE,
    )

    _ISOLATED_CAP = re.compile(
        r"\b(?P<cap>120gb|128gb|240gb|250gb|256gb|480gb|500gb|512gb|960gb|1000gb|1tb|2tb)\b",
        re.IGNORECASE,
    )

    _NON_STORAGE = re.compile(
        r"\b(?:карман|кишеня|салазки|caddy|контроллер|контролер|expander|плата\s+hdd|плата\s+жорсткого|dvd|дискета|кабель|адаптер)\b",
        re.IGNORECASE,
    )

    def extract(self, normalized_title: str) -> List[str]:
        if self._NON_STORAGE.search(normalized_title):
            return []

        # БЕЗПЕЧНЕ МАСКУВАННЯ: Знаходимо точні координати відеокарт
        vram_spans = []
        for gpu_m in re.finditer(r"\b(?:rtx|gtx|rx|geforce)\s+\d{3,4}(?:\s*(?:ti\s*super|ti|super|xtx|xt))?\s+(\d{1,2}gb)\b", normalized_title):
            vram_spans.append(gpu_m.span(1))

        # Перевіряємо, чи позиція збігу не перетинається з VRAM
        def is_vram(start: int, end: int) -> bool:
            return any(vs <= start and end <= ve for vs, ve in vram_spans)

        raw: List[str] = []

        # 1. Прямий пошук пар: [тип + обсяг]
        for m in self._DIRECT_STORAGE.finditer(normalized_title):
            if is_vram(m.start(), m.end()):
                continue
            g = m.groupdict()
            st_type = (g.get("type") or g.get("type_alt") or "").lower()
            cap = (g.get("cap") or g.get("cap_alt") or "").lower().replace(" ", "")

            if "gb" in cap:
                val = int(cap.replace("gb", ""))
                if val < 60:  # Менше 60 ГБ — це не системний накопичувач
                    continue

            prefix = "hdd" if "hdd" in st_type else "ssd"
            raw.append(f"{prefix}_{cap}")

        # 2. Непрямі згадки
        if not raw and re.search(r"\b(?:ssd|nvme|m2|hdd)\b", normalized_title):
            is_hdd = bool(re.search(r"\b(?:hdd)\b", normalized_title))
            st_prefix = "hdd" if is_hdd else "ssd"
            for m in self._ISOLATED_CAP.finditer(normalized_title):
                if not is_vram(m.start(), m.end()):
                    raw.append(f"{st_prefix}_{m.group('cap').lower()}")

        # Системні SSD завжди мають пріоритет
        raw.sort(key=lambda x: 0 if x.startswith("ssd") else 1)
        return self._limit(raw)


class RamExtractor(BaseExtractor):
    CATEGORY = "ram"

    _DDR = re.compile(r"\b(?P<type>ddr[345])\b", re.IGNORECASE)
    _KIT = re.compile(
        r"\b(?P<count>[1248])\s*[*x]\s*(?P<single_cap>4|8|16|32|64)\s*(?:gb)?\b",
        re.IGNORECASE,
    )
    _SINGLE_CAP = re.compile(r"\b(?P<cap>4|8|16|32|48|64|96)\s*gb\b", re.IGNORECASE)

    def extract(self, normalized_title: str) -> List[str]:
        # 1. Знаходимо точні координати VRAM, щоб не переплутати з ОЗП
        vram_spans = []
        for gpu_m in re.finditer(
            r"\b(?:rtx|gtx|rx|geforce)\s+\d{3,4}(?:\s*(?:ti\s*super|ti|super|xtx|xt))?\s+(\d{1,2}gb)\b",
            normalized_title,
        ):
            vram_spans.append(gpu_m.span(1))

        def is_vram(start: int, end: int) -> bool:
            return any(vs <= start and end <= ve for vs, ve in vram_spans)

        # Визначаємо тип DDR (ddr3 / ddr4 / ddr5)
        type_match = self._DDR.search(normalized_title)
        ddr_type = type_match.group("type").lower() if type_match else None

        # 2. Перевірка конфігурацій KIT (наприклад, 2x8gb, 4x16gb)
        kit_match = self._KIT.search(normalized_title)
        if kit_match:
            count = int(kit_match.group("count"))
            single = int(kit_match.group("single_cap"))
            total = count * single
            actual_ddr = ddr_type or "ddr4"
            return [f"ram_{actual_ddr}_{total}gb", f"ram_{total}gb"]

        # 3. Пошук окремих планок ОЗП
        candidates = []
        for m in self._SINGLE_CAP.finditer(normalized_title):
            if is_vram(m.start(), m.end()):
                continue

            cap_val = int(m.group("cap"))

            # Вузький контекст безпосередньо біля числа
            prefix = normalized_title[max(0, m.start() - 10):m.start()]
            suffix = normalized_title[m.end():min(len(normalized_title), m.end() + 10)]
            surrounding_wide = normalized_title[max(0, m.start() - 15):min(len(normalized_title), m.end() + 15)]

            # Число є накопичувачем, ТІЛЬКИ якщо тип диска приклеєний безпосередньо до нього
            # (наприклад: "ssd 16gb", "16gb ssd", "m2 16gb")
            is_direct_storage = bool(
                re.search(r"(?:ssd|hdd|nvme|m2)\s*$", prefix) or 
                re.search(r"^\s*(?:ssd|hdd|nvme|m2)", suffix)
            )
            if is_direct_storage:
                continue

            # Маркери ОЗП
            has_direct_ram = bool(
                re.search(r"(?:ram|озу|пам|память|ddr[345])\s*$", prefix) or 
                re.search(r"^\s*(?:ram|озу|пам|память|ddr[345])", suffix)
            )
            has_wide_ram = bool(
                re.search(r"\b(?:ram|озу|пам|память|ddr[345]|fury|kingston|corsair|3200mhz|6000mhz)\b", surrounding_wide)
            )

            # Пріоритет: 2 = пряме сусідство з RAM/DDR, 1 = маркер поруч у тексті, 0 = нейтральне число
            score = 2 if has_direct_ram else (1 if has_wide_ram else 0)
            candidates.append((cap_val, score))

        if candidates:
            # Сортуємо: спочатку за наявністю маркера RAM, потім за спаданням обсягу
            candidates.sort(key=lambda x: (x[1], x[0]), reverse=True)
            chosen_cap = candidates[0][0]
            actual_ddr = ddr_type or "ddr4"
            return [f"ram_{actual_ddr}_{chosen_cap}gb", f"ram_{chosen_cap}gb"]

        return []


# ---------------------------------------------------------------------------
# Bundle Detector
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class BundleResult:
    bundle_key: str
    components: Dict[str, Optional[str]]


class BundleDetector:
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

        if hardware_targets:
            if isinstance(next(iter(hardware_targets.values()), None), dict):
                valid_gpus = {k for k, v in hardware_targets.items() if v.get("item_type") == "gpu"}
                valid_cpus = {k for k, v in hardware_targets.items() if v.get("item_type") == "cpu"}
                valid_mbs = {k for k, v in hardware_targets.items() if v.get("item_type") == "motherboard"}
            else:
                valid_gpus = set(hardware_targets.get("gpu", []))
                valid_cpus = set(hardware_targets.get("cpu", []))
                valid_mbs = set(hardware_targets.get("motherboard", []))

            gpus = [c for c in gpus if c in valid_gpus]
            cpus = [c for c in cpus if c in valid_cpus]
            mbs = [c for c in mbs if c in valid_mbs]

        categories = sum(bool(x) for x in (gpus, cpus, mbs))
        has_keyword = bool(self._BUNDLE_KEYWORDS.search(normalized_title))

        if has_keyword and (categories >= 1):
            primary_cpu = cpus[0] if cpus else None
            primary_mb = mbs[0] if mbs else None
            primary_gpu = gpus[0] if gpus else None
            primary_ram = rams[0] if rams else None

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
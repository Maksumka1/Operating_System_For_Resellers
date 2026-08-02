from __future__ import annotations

import asyncio
import re
import sys
import os
import time
import json
from datetime import datetime, timezone
from pathlib import Path
from collections import defaultdict
from urllib.parse import urlparse
from curl_cffi.requests import AsyncSession
from supabase import create_client, Client
from dotenv import load_dotenv

from config import HARDWARE_TARGETS, LEGACY_PRE_SORTED_TARGETS, SOCKETS, CHIPSET_TO_SOCKET
from hardware_matchers import detect_bundle_components, extract_motherboard, extract_psu, extract_ram, extract_storage, normalize_title, extract_gpu, extract_cpu


PROJECT_ROOT = Path(__file__).resolve().parent
if not (PROJECT_ROOT / "config.py").exists():
    PROJECT_ROOT = PROJECT_ROOT.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from config import HARDWARE_TARGETS, SOCKETS, CHIPSET_TO_SOCKET
load_dotenv(PROJECT_ROOT / ".env")
SUPABASE_URL = os.getenv("SUPABASE_URL", "https://nfhtmfhckctuyhfolhou.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_SECRET_KEY") or os.getenv("SUPABASE_PUBLISHABLE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY or "")


# ------------------------------------------------------------------------------
# КЛАС АСИНХРОННОГО ДЕБАГЕРА (ЗБЕРІГАЄ У debug/debug_report_parse_hardware.md)
# ------------------------------------------------------------------------------
class PipelineDebugger:
    """Дебаггер для аналізу результатів парсингу комплектуючих OLX."""
    def __init__(self, filename="debug_report_parse_hardware.md"):
        self.debug_dir = PROJECT_ROOT / "debug"
        self.debug_dir.mkdir(parents=True, exist_ok=True)
        self.filepath = self.debug_dir / filename
        
        self.start_time = datetime.now()
        self.stats = defaultdict(lambda: defaultdict(int))
        self.samples = defaultdict(list)
        self.lock = asyncio.Lock()

    async def record_stat(self, category: str, metric: str, count: int = 1):
        async with self.lock:
            self.stats[category][metric] += count

    async def add_sample(self, category: str, item: dict, max_samples: int = 100):
        async with self.lock:
            if len(self.samples[category]) < max_samples:
                self.samples[category].append(item)

    def save_report(self):
        duration = (datetime.now() - self.start_time).total_seconds()
        
        report = []
        report.append("# 🐛 ДЕБАГ-ЗВІТ ПАРСИНГУ КОМПЛЕКТУЮЧИХ OLX (GraphQL)")
        report.append(f"**Дата та час запуску:** {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"**Тривалість виконання:** {duration:.2f} сек")
        report.append(f"**Шлях до звіту:** `{self.filepath}`\n")
        
        report.append("## 📌 1. Задача та мета коду")
        report.append(
            "Основна мета: асинхронний збір свіжих оголошень комплектуючих з OLX (GraphQL API).\n"
            "1. Отримання оголошень по підкатегоріях (відеокарти, процесори, материнські плати, БЖ, накопичувачі).\n"
            "2. Фільтрація дублікатів за URL та перевірка приналежності до підкатегорії.\n"
            "3. Сувора ідентифікація моделі заліза (`match_ad_to_hardware_target`) з очищенням порівняльних фраз.\n"
            "4. Детекція сокетів, перевірка на дефекти/неробочий стан (`is_broken_ad`) та розпарсинг фото/продавця.\n"
            "5. Відправка готових записів у Supabase (`ads`) та тригер WebSocket стріму.\n"
        )

        report.append("## 📊 2. Загальна статистика вхідних даних та відсіювання")
        for cat, metrics in self.stats.items():
            report.append(f"### ⚙️ Секція: {cat}")
            for metric, val in metrics.items():
                report.append(f"- **{metric}:** {val}")
            report.append("")

        report.append("## 🔄 3. Детальні приклади даних")
        
        category_mapping = [
            ("gpu", "🎮 Відеокарти (GPU)"),
            ("cpu", "🧠 Процесори (CPU)"),
            ("motherboard", "🔌 Материнські плати (Motherboard)"),
            ("psu", "⚡ Блоки живлення (PSU)"),
            ("storage", "💾 Накопичувачі (SSD / HDD)"),
            ("ram", "📟 Оперативна пам'ять (RAM)"),
            ("bundle", "📦 Комплекти (Bundles)")
        ]

        # 1. Секція відсіяних оголошень ДЛЯ КОЖНОЇ КАТЕГОРІЇ (по 100 прикладів)
        report.append("### 🚫 Відсіяні оголошення (по 100 прикладів для кожної категорії):")
        for type_key, title in category_mapping:
            filter_key = f"Filtered_{type_key}"
            filtered_samples = self.samples.get(filter_key, [])
            report.append(f"#### {title} — Відсіяно (Показано {len(filtered_samples)} з max 100):")
            if not filtered_samples:
                report.append("_Жодного відсіяного оголошення в цій категорії._\n")
                continue
            
            for idx, sample in enumerate(filtered_samples, 1):
                report.append(f"**Семпл #{idx}:**")
                report.append("```json\n" + json.dumps(sample, indent=2, ensure_ascii=False) + "\n```")
            report.append("")

        # 2. Секція розпізнаних моделей ДЛЯ КОЖНОЇ КАТЕГОРІЇ (по 40 прикладів)
        report.append("### 🎯 Успішно розпізнані моделі заліза (по 40 прикладів для кожної категорії):")
        for type_key, title in category_mapping:
            recognized_key = f"Recognized_{type_key}"
            cat_samples = self.samples.get(recognized_key, [])
            report.append(f"#### {title} — Розпізнано (Показано {len(cat_samples)} з max 40):")
            if not cat_samples:
                report.append("_Жодного оголошення з цієї категорії не розпізнано під час запуску._\n")
                continue
            
            for idx, sample in enumerate(cat_samples, 1):
                report.append(f"**Зразок #{idx}:**")
                report.append("```json\n" + json.dumps(sample, indent=2, ensure_ascii=False) + "\n```")
            report.append("")

        report.append("=" * 60 + "\n")
        
        with open(self.filepath, "w", encoding="utf-8") as f:
            f.write("\n".join(report))
        
        print(f"📝 [DEBUG] Повний дебаг-звіт збережено у `{self.filepath}`")


# Глобальний екземпляр дебаггера
debugger = PipelineDebugger()


BROKEN_PATTERN = re.compile(
    r"неробоч|не робоч|запчастин|запчасть|запчасти|дефект|відновлен|восстановлен|"
    r"артефакт|поломан|неисправн|не справн|на детал|запчасті|прогрів|не стартует|"
    r"не включа|не включається|не включается|не працює|не работает|не робочий|"
    r"на\s+запчаст\w*|под\s+восстановление|під\s+відновлення|под\s+ремонт|під\s+ремонт|"
    r"непрацю\w*|\bремонт\w*",
    re.IGNORECASE,
)

CLEAN_PATTERNS = re.compile(
    r"(?:"
    r"без\s+(?:будь-яких\s+|будь\s+яких\s+)?(?:проблем|дефект\w*|артефакт\w*|ремонт\w*|нюанс\w*)|"
    r"без\s+майнинга\s+и\s+ремонтов|"
    r"не\s+(?:був|были?|было)\s+в\s+ремонт\w*|"
    r"в\s+ремонт\w*\s+не\s+(?:був|был)|"
    r"не\s+ремонтував\w*|не\s+ремонтировал\w*|не\s+вскрывался\w*|не\s+розбирався|"
    r"дефект\w*\s+(?:не|нет)\s+\w*|"
    r"без\s+физических\s+повреждений"
    r")",
    re.IGNORECASE,
)

COMPARISON_PATTERN = re.compile(
    r"(?:сильніше\s+за|мощнее\s+чем|быстрее\s+чем|аналог|замість|вмісто|вместо|похожа\s+на|як|как|рівень|уровень|мощнее|быстрее|сильнее)\s+[a-z0-9\s_-]+|\(.*?\)",
    re.IGNORECASE
)

MULTILOT_PATTERN = re.compile(
    r"\d+\s*(?:gb|гб)\s*,\s*\d+\s*(?:gb|гб)",
    re.IGNORECASE
)

HEADERS = {
    "accept": "application/json",
    "accept-language": "uk",
    "content-type": "application/json",
    "origin": "https://www.olx.ua",
    "referer": "https://www.olx.ua/",
    "sec-ch-ua": '"Not;A=Brand";v="8", "Chromium";v="124", "Google Chrome";v="124"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "x-client": "DESKTOP",
}

TIMEOUT = 12

SUBCATEGORIES_TO_PARSE = [
    {"item_type": "gpu", "subcategory": "videokarty", "name": "Відеокарти"},
    {"item_type": "cpu", "subcategory": "protsessory", "name": "Процесори"},
    {"item_type": "motherboard", "subcategory": "materinskie-platy", "name": "Материнські плати"},
    {"item_type": "psu", "subcategory": "bloki-pitaniya", "name": "Блоки живлення"},
    {"item_type": "storage", "subcategory": "zhestkie-diski", "name": "Накопичувачі"},
    {"item_type": "ram", "subcategory": "moduli-pamyati", "name": "Оперативна пам'ять"}
]

GRAPHQL_QUERY = """query ListingSearchQuery($searchParameters: [SearchParameter!] = []) {
  clientCompatibleListings(searchParameters: $searchParameters) {
    ... on ListingSuccess {
      data {
        id title url status created_time last_refresh_time description
        location { city { name } }
        photos { link }
        user { id uuid name created }
        params {
          key name
          value {
            ... on PriceParam { value currency label }
            ... on GenericParam { key label }
          }
        }
      }
    }
  }
}"""


def validate_title_strict(title_lower: str, compiled_pattern: re.Pattern) -> bool:
    return bool(compiled_pattern.search(title_lower))

def is_broken_ad(text: str) -> bool:
    if not text:
        return False
    clean_text = CLEAN_PATTERNS.sub("", text)
    return bool(BROKEN_PATTERN.search(clean_text))

def clean_url(url: str) -> str:
    parsed = urlparse(url)
    return f"{parsed.scheme}://{parsed.netloc}{parsed.path}"

def detect_socket(title: str, description: str, component_name: str) -> str | None:
    full_text = f"{title} {description}".lower()

    for sock in SOCKETS:
        pattern = r"\b" + re.escape(sock.replace("-", " ")) + r"\b"
        if re.search(pattern, full_text.replace("-", " ")):
            clean_sock = sock.replace("socket", "lga")
            return clean_sock

    mb_key = component_name.lower().replace("_", "")
    if mb_key in CHIPSET_TO_SOCKET:
        return CHIPSET_TO_SOCKET[mb_key]

    return None


def match_ad_to_hardware_target(title: str, target_items_for_type: dict = None) -> tuple[str, dict] | None:
    if not title:
        return None

    # 1. Повна нормалізація
    title_clean = normalize_title(title)

    if MULTILOT_PATTERN.search(title_clean):
        return None

    title_for_match = COMPARISON_PATTERN.sub("", title_clean)

    # --- ПЕРЕВІРКА НА СУТНІСТЬ BUNDLE (КОМПЛЕКТ) ---
    bundle_data = detect_bundle_components(title_for_match, HARDWARE_TARGETS)
    if bundle_data:
        bundle_key = bundle_data["bundle_key"]
        bundle_cfg = {
            "item_type": "bundle",
            "subcategory": "komplektuyushchie-set",
            "components": bundle_data["components"]
        }
        return bundle_key, bundle_cfg

    # --- СТЕК ПООДИНОКИХ СУТНОСТЕЙ (Окремі товари) ---

    # 1. Спеціальний перевірочний виняток для китайських X99
    if "x99" in title_for_match and "x99" in HARDWARE_TARGETS:
        return "x99", HARDWARE_TARGETS["x99"]

    # 2. GPU Matching (O(1))
    gpu_candidates = extract_gpu(title_for_match)
    for cand in gpu_candidates:
        if cand in HARDWARE_TARGETS:
            return cand, HARDWARE_TARGETS[cand]

    # 3. CPU Matching (O(1))
    cpu_candidates = extract_cpu(title_for_match)
    for cand in cpu_candidates:
        if cand in HARDWARE_TARGETS:
            return cand, HARDWARE_TARGETS[cand]

    # 4. Motherboard Matching (O(1))
    mb_candidates = extract_motherboard(title_for_match)
    for cand in mb_candidates:
        if cand in HARDWARE_TARGETS:
            return cand, HARDWARE_TARGETS[cand]

    psu_candidates = extract_psu(title_for_match)
    for cand in psu_candidates:
        if cand in HARDWARE_TARGETS:
            return cand, HARDWARE_TARGETS[cand]

    # 6. Storage Matching (O(1))
    storage_candidates = extract_storage(title_for_match)
    for cand in storage_candidates:
        if cand in HARDWARE_TARGETS:
            return cand, HARDWARE_TARGETS[cand]

    # 7. RAM Matching (O(1))
    ram_candidates = extract_ram(title_for_match)
    for cand in ram_candidates:
        if cand in HARDWARE_TARGETS:
            return cand, HARDWARE_TARGETS[cand]


    # 5. Fallback / Storage & PSU
    targets_to_check = LEGACY_PRE_SORTED_TARGETS if target_items_for_type is None else sorted(
        target_items_for_type.items(), key=lambda x: len(x[0]), reverse=True
    )

    for target_name, cfg in targets_to_check:
        compiled_patt = cfg.get("compiled_pattern")

        if cfg.get("item_type") == "storage":
            parts = target_name.split("_")
            if len(parts) < 2: continue
            st_type, capacity_raw = parts[0], parts[1]
            cap_num = re.sub(r"\D", "", capacity_raw)
            cap_unit = "tb" if "tb" in capacity_raw else "gb"

            has_type = False
            if st_type == "ssd":
                has_type = any(w in title_for_match for w in ["ssd", "ссд", "nvme", "m.2", "m2"])
            elif st_type == "hdd":
                has_type = any(w in title_for_match for w in [
                    "hdd", "хдд", "жорстк", "жестк", "винчестер", "toshiba",
                    "wd blue", "wd red", "wd black", "wd green", "barracuda", "wd", "hitachi", "seagate", "ironwolf"
                ])

            if not has_type: continue

            if capacity_raw == "1tb":
                pattern = r"(?<![a-z0-9])(1\s*(tb|тб|терабайт)|(1000|1024)\s*(gb|гб|гігабайт|гигабайт))(?![a-z0-9])"
            elif cap_unit == "tb":
                pattern = r"(?<![a-z0-9])" + cap_num + r"\s*(tb|тб|терабайт)(?![a-z0-9])"
            else:
                pattern = r"(?<![a-z0-9])" + cap_num + r"\s*(gb|гб|гігабайт|гигабайт)(?![a-z0-9])"

            if re.search(pattern, title_for_match):
                return target_name, cfg
        else:
            if compiled_patt and bool(compiled_patt.search(title_for_match)):
                return target_name, cfg

    return None


async def fetch_subcategory_page(
    session: AsyncSession,
    subcat_info: dict,
    hardware_targets: dict,
    seen_urls: set[str],
    today_sql: str,
    offset: int = 0,
    limit: int = 40,
    max_retries: int = 3,
) -> list[dict]:
    subcat_key = subcat_info["subcategory"]
    item_type = subcat_info["item_type"]

    targets_for_this_type = {
        k: v for k, v in hardware_targets.items() if v.get("item_type") == item_type
    }

    search_params = [
        {"key": "category_id", "value": "458"},
        {"key": "filter_enum_subcategory[0]", "value": subcat_key},
        {"key": "currency", "value": "UAH"},
        {"key": "sort_by", "value": "created_at:desc"},
        {"key": "limit", "value": str(limit)},
        {"key": "offset", "value": str(offset)},
    ]

    json_payload = {
        "query": GRAPHQL_QUERY,
        "variables": {"searchParameters": search_params},
    }

    parsed_for_subcat = []

    for attempt in range(1, max_retries + 1):
        try:
            await asyncio.sleep(0.3)
            resp = await session.post(
                "https://www.olx.ua/apigateway/graphql",
                json=json_payload,
                timeout=TIMEOUT,
            )

            if resp.status_code in (401, 403):
                await debugger.record_stat("Network", f"HTTP 403 (Блокування {subcat_key})")
                print(f"[WARN 403] Блокування на '{subcat_key}'. Спроба {attempt}/{max_retries}. Чекаємо 10с...")
                await asyncio.sleep(10)
                continue

            if resp.status_code != 200:
                await debugger.record_stat("Network", f"HTTP Status {resp.status_code}")
                print(f"[ERR] HTTP Status {resp.status_code} для '{subcat_key}'")
                await asyncio.sleep(2)
                continue

            res_json = resp.json()
            break
        except Exception as e:
            await debugger.record_stat("Network", "Мережева помилка (Exception)")
            print(f"[EXC] Помилка мережі для '{subcat_key}': {e}")
            await asyncio.sleep(2)
            if attempt == max_retries:
                return []
    else:
        return []

    listings = (
        res_json.get("data", {})
        .get("clientCompatibleListings", {})
        .get("data", [])
    )

    await debugger.record_stat("OLX_GraphQL", f"Отримано оголошень [{subcat_key}]", len(listings))

    if not listings:
        await debugger.record_stat("OLX_GraphQL", f"Відсіяно if (Порожній список [{subcat_key}])")
        return []

    for item in listings:
        try:
            ad_subcat = None
            for param in item.get("params", []):
                if param.get("key") == "subcategory":
                    val_obj = param.get("value") or {}
                    ad_subcat = val_obj.get("key")
                    break

            if ad_subcat and ad_subcat != subcat_key:
                await debugger.record_stat("Filtering_Rules", "Відсіяно if (Невідповідність підкатегорії)")
                # Зберігаємо відсіяні оголошення ОКРЕМО по категорії
                await debugger.add_sample(f"Filtered_{item_type}", {
                    "reason": "mismatched_subcategory",
                    "expected": subcat_key,
                    "actual": ad_subcat,
                    "title": item.get("title")
                }, max_samples=100)
                continue

            title = item.get("title", "Без назви").replace("'", "").strip()

            raw_url = item.get("url", "")
            if not raw_url:
                await debugger.record_stat("Filtering_Rules", "Відсіяно if (Порожній URL)")
                continue

            if not raw_url.startswith("http"):
                raw_url = "https://www.olx.ua" + raw_url

            advert_url = clean_url(raw_url)

            if advert_url in seen_urls:
                # await debugger.record_stat("Filtering_Rules", "Відсіяно if (Дублікат URL в DB)")
                # Зберігаємо відсіяні оголошення ОКРЕМО по категорії
                await debugger.add_sample(f"Filtered_{item_type}", {
                    "reason": "duplicate_url_already_in_db",
                    "url": advert_url,
                    "title": title
                }, max_samples=100)
                continue

            user_data = item.get("user") or {}
            seller_id = str(user_data.get("id")) if user_data.get("id") else None
            seller_uuid = str(user_data.get("uuid")) if user_data.get("uuid") else None
            seller_name = user_data.get("name") or "Невідомо"

            matched = match_ad_to_hardware_target(title, targets_for_this_type)
            if not matched:
                await debugger.record_stat("Filtering_Rules", "Відсіяно if (Не розпізнано модель заліза)")
                # Зберігаємо відсіяні оголошення ОКРЕМО по категорії
                await debugger.add_sample(f"Filtered_{item_type}", {
                    "reason": "no_hardware_target_matched",
                    "title": title,
                    "item_type": item_type
                }, max_samples=100)
                continue

            raw_ad_id = item.get("id")
            ad_id = int(raw_ad_id) if raw_ad_id and str(raw_ad_id).isdigit() else None

            target_name, cfg = matched
            description = (item.get("description") or "").replace("<br />", "")

            full_text = f"{title} {description}"
            has_defects = 1 if is_broken_ad(full_text) else 0

            if has_defects:
                await debugger.record_stat("Parsing_Metrics", "Виявлено товарів з дефектами")

            price = 0
            for param in item.get("params", []):
                if param.get("key") == "price":
                    price_val = param.get("value", {}).get("value", 0)
                    if isinstance(price_val, (int, float)) and price_val <= 1_000_000_000:
                        price = int(price_val)
                    break

            loc_data = item.get("location", {}) or {}
            city = loc_data.get("city", {}).get("name", "Невідомо") if loc_data.get("city") else "Невідомо"

            created_time_raw = item.get("created_time", "")
            ad_date = created_time_raw.split("T")[0] if created_time_raw else "Невідомо"

            raw_photos = item.get("photos", [])
            photo_urls_list = []
            for p in raw_photos:
                link = p.get("link", "")
                if link:
                    formatted_link = link.replace("{width}", "1000").replace("{height}", "750")
                    photo_urls_list.append(formatted_link)

            first_photo = photo_urls_list[0] if photo_urls_list else "Невідомо"
            all_photos_str = ",".join(photo_urls_list) if photo_urls_list else None

            user_created_raw = str(user_data.get("created") or "")
            seller_created_at = user_created_raw.split("-")[0] if "-" in user_created_raw else None

            is_business = item.get("business", False)
            seller_type = "shop" if is_business else "private_person"

            detected_socket = None
            if item_type in ("motherboard", "cpu"):
                detected_socket = detect_socket(title, description, target_name)

            bundle_components = cfg.get("components") if item_type == "bundle" or target_name.startswith("bundle_") else None

            ad_payload = {
                "ad_id": ad_id,
                "url": advert_url,
                "title": title,
                "description": description,
                "price": price,
                "item_type": cfg.get("item_type", item_type),
                "component_name": target_name,
                "socket": detected_socket,
                "has_defects": has_defects,
                "city": city,
                "created_at_olx": ad_date,
                "photo_url": first_photo,
                "all_photos": all_photos_str,
                "parsed_date": today_sql,
                "status": "active",
                "seller_id": seller_id,
                "seller_uuid": seller_uuid,
                "seller_name": seller_name,
                "seller_created_at": seller_created_at,
                "seller_type": seller_type,
                "seller_price_clean": price,
                "bundle_components": bundle_components
            }

            parsed_for_subcat.append(ad_payload)
            seen_urls.add(advert_url)

            await debugger.record_stat("Parsing_Metrics", f"Успішно розпізнано [{item_type}]")
            
            # Додаємо розпізнані семпли ОКРЕМО по категорії (до 40)
            await debugger.add_sample(f"Recognized_{item_type}", {
                "raw_title": title,
                "matched_target": target_name,
                "item_type": item_type,
                "detected_socket": detected_socket,
                "has_defects": bool(has_defects),
                "price_uah": price
            }, max_samples=40)

            defect_tag = " [⚠️ ДЕФЕКТ]" if has_defects else ""
            print(f"   🎯 [РОЗПІЗНАНО: {target_name}]{defect_tag}: {title[:40]}... ({price} грн)")

        except Exception as ex:
            await debugger.record_stat("Errors", f"Помилка елемента: {str(ex)[:40]}")
            print(f"   [!] Помилка обробки елемента: {ex}")
            continue

    return parsed_for_subcat


async def run_parser(
    hardware_items: dict, seen_urls: set[str], today_sql: str, pages_to_parse: int = 1
) -> list[dict]:
    async with AsyncSession(headers=HEADERS, impersonate="chrome124") as session:
        print("🔥 Прогріваємо сесію...")
        try:
            await session.get("https://www.olx.ua/uk/elektronika/", timeout=10)
        except Exception:
            pass

        all_results = []
        for subcat_info in SUBCATEGORIES_TO_PARSE:
            subcat_key = subcat_info["subcategory"]
            cat_name = subcat_info["name"]
            print(f"\n📡 Завантажуємо свіжі {cat_name} (підкатегорія: {subcat_key}, сторінок: {pages_to_parse})...")

            for page in range(pages_to_parse):
                offset = page * 40
                if pages_to_parse > 1:
                    print(f"   📂 Сторінка {page + 1}/{pages_to_parse} (offset={offset})...")

                res = await fetch_subcategory_page(
                    session, subcat_info, hardware_items, seen_urls, today_sql, offset=offset, limit=40
                )
                all_results.extend(res)

                if pages_to_parse > 1 and page < pages_to_parse - 1:
                    await asyncio.sleep(1.0)

    return all_results


def main(pages_to_parse: int = 1) -> None:
    today_sql = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    # 1. Завантажуємо існуючі URL з лімітом 50000 записів для стабільної дедуплікації
    try:
        response = supabase.table("ads").select("url").limit(50000).execute()
        seen_urls = set(row["url"] for row in (response.data or []))
        asyncio.run(debugger.record_stat("Supabase_Input", "Завантажено URLs для дедуплікації", len(seen_urls)))
        print(f"[БАЗА SUPABASE] Завантажено {len(seen_urls)} комплектуючих для дедуплікації.")
    except Exception as e:
        asyncio.run(debugger.record_stat("Supabase_Input", "Помилка читання Supabase URLs"))
        print(f"[ПОМИЛКА ЧИТАННЯ SUPABASE]: {e}")
        seen_urls = set()

    hardware_items = {
        k: v for k, v in HARDWARE_TARGETS.items() if not k.startswith("pc_")
    }

    asyncio.run(debugger.record_stat("Parser_Config", "Цільових моделей комплектуючих", len(hardware_items)))
    print(f"🚀 Стартуємо збір по підкатегоріях для {len(hardware_items)} моделей (сторінок на категорію: {pages_to_parse})...")
    start_time = time.time()

    new_ads_to_insert = asyncio.run(
        run_parser(hardware_items, seen_urls, today_sql, pages_to_parse=pages_to_parse)
    )

    elapsed = time.time() - start_time
    asyncio.run(debugger.record_stat("Summary", "Знайдено нових унікальних оголошень", len(new_ads_to_insert)))
    print(f"\n⏱️ Мережевий збір завершено за {elapsed:.2f} сек. (Знайдено нових комплектуючих: {len(new_ads_to_insert)})")

    # 2. Збереження у хмарний PostgreSQL Supabase та тригер WebSockets
    if new_ads_to_insert:
        try:
            supabase.table("ads").upsert(new_ads_to_insert, on_conflict="ad_id").execute()
            asyncio.run(debugger.record_stat("Supabase_Output", "Успішно збережено нових оголошень", len(new_ads_to_insert)))
            print(f"[УСПІХ SUPABASE] Збережено {len(new_ads_to_insert)} нових комплектуючих у хмару!")

            # 3. Тригеримо WebSocket на сервері для оновлення живого стріму
            try:
                import requests
                requests.post("http://localhost:8000/api/trigger-new-ad", json=new_ads_to_insert, timeout=2)
                asyncio.run(debugger.record_stat("WebSocket", "Успішно надіслано тригер стріму"))
                print("📢 [WEBSOCKET] Живий стрим оновлено!")
            except Exception:
                asyncio.run(debugger.record_stat("WebSocket", "Помилка з'єднання з локальним сервером"))
                pass

        except Exception as ex:
            asyncio.run(debugger.record_stat("Supabase_Output", f"Помилка Upsert: {str(ex)[:40]}"))
            print(f"❌ [ПОМИЛКА SUPABASE]: {ex}")
    else:
        asyncio.run(debugger.record_stat("Summary", "Немає нових оголошень для відправки в DB"))
        print("[INFO] Нових оголошень для запису не знайдено.")

    # Зберігаємо підсумковий дебаг-звіт у debug/debug_report_parse_hardware.md
    debugger.save_report()


if __name__ == "__main__":
    main()
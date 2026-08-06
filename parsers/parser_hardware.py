from __future__ import annotations

import os
import asyncio
import json
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from collections import defaultdict
from urllib.parse import urlparse
import aiohttp

from curl_cffi.requests import AsyncSession
from supabase import create_client, Client
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent
if not (PROJECT_ROOT / "config.py").exists():
    PROJECT_ROOT = PROJECT_ROOT.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from config import HARDWARE_TARGETS, LEGACY_PRE_SORTED_TARGETS, SOCKETS, CHIPSET_TO_SOCKET
from hardware_matchers import (
    detect_bundle_components, extract_motherboard, extract_psu, 
    extract_ram, extract_storage, normalize_title, extract_gpu, extract_cpu
)

load_dotenv(PROJECT_ROOT / ".env")

SUPABASE_URL = os.getenv("SUPABASE_URL", "https://nfhtmfhckctuyhfolhou.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_SECRET_KEY") or os.getenv("SUPABASE_PUBLISHABLE_KEY")
OLX_PROXY_URL = os.getenv("OLX_PROXY_URL") or None

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY or "")


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

    async def save_report_async(self):
        duration = (datetime.now() - self.start_time).total_seconds()
        report = [
            "# 🐛 ДЕБАГ-ЗВІТ ПАРСИНГУ КОМПЛЕКТУЮЧИХ OLX (GraphQL)",
            f"**Дата та час запуску:** {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}",
            f"**Тривалість виконання:** {duration:.2f} сек",
            f"**Шлях до звіту:** `{self.filepath}`\n",
            "## 📌 1. Задача та мета коду",
            "Основна мета: асинхронний збір свіжих оголошень комплектуючих з OLX (GraphQL API).\n",
            "## 📊 2. Загальна статистика вхідних даних та відсіювання"
        ]
        for cat, metrics in self.stats.items():
            report.append(f"### ⚙️ Секція: {cat}")
            for metric, val in metrics.items():
                report.append(f"- **{metric}:** {val}")
            report.append("")

        report.append("## 🔄 3. Детальні приклади даних")
        category_mapping = [
            ("gpu", "🎮 Відеокарти (GPU)"), ("cpu", "🧠 Процесори (CPU)"),
            ("motherboard", "🔌 Материнські плати"), ("psu", "⚡ Блоки живлення"),
            ("storage", "💾 Накопичувачі"), ("ram", "📟 Оперативна пам'ять"),
            ("bundle", "📦 Комплекти")
        ]

        report.append("### 🚫 Відсіяні оголошення:")
        for type_key, title in category_mapping:
            filter_key = f"Filtered_{type_key}"
            filtered_samples = self.samples.get(filter_key, [])
            report.append(f"#### {title} — Відсіяно ({len(filtered_samples)}):")
            for idx, sample in enumerate(filtered_samples, 1):
                report.append(f"**Семпл #{idx}:**\n```json\n" + json.dumps(sample, indent=2, ensure_ascii=False) + "\n```")
            report.append("")

        report.append("### 🎯 Успішно розпізнані моделі:")
        for type_key, title in category_mapping:
            cat_samples = self.samples.get(f"Recognized_{type_key}", [])
            report.append(f"#### {title} — Розпізнано ({len(cat_samples)}):")
            for idx, sample in enumerate(cat_samples, 1):
                report.append(f"**Зразок #{idx}:**\n```json\n" + json.dumps(sample, indent=2, ensure_ascii=False) + "\n```")
            report.append("")

        def _write():
            with open(self.filepath, "w", encoding="utf-8") as f:
                f.write("\n".join(report))

        await asyncio.to_thread(_write)
        print(f"📝 [DEBUG] Повний дебаг-звіт збережено у `{self.filepath}`")


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

MULTILOT_PATTERN = re.compile(r"\d+\s*(?:gb|гб)\s*,\s*\d+\s*(?:gb|гб)", re.IGNORECASE)

HEADERS = {
    "accept": "application/json",
    "accept-language": "uk",
    "content-type": "application/json",
    "origin": "https://www.olx.ua",
    "referer": "https://www.olx.ua/",
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
            return sock.replace("socket", "lga")

    mb_key = component_name.lower().replace("_", "")
    return CHIPSET_TO_SOCKET.get(mb_key)


def match_ad_to_hardware_target(title: str, target_items_for_type: dict = None) -> tuple[str, dict] | None:
    if not title:
        return None

    title_clean = normalize_title(title)
    if MULTILOT_PATTERN.search(title_clean):
        return None

    title_for_match = COMPARISON_PATTERN.sub("", title_clean)

    bundle_data = detect_bundle_components(title_for_match, HARDWARE_TARGETS)
    if bundle_data:
        return bundle_data["bundle_key"], {
            "item_type": "bundle",
            "subcategory": "komplektuyushchie-set",
            "components": bundle_data["components"]
        }

    if "x99" in title_for_match and "x99" in HARDWARE_TARGETS:
        return "x99", HARDWARE_TARGETS["x99"]

    for cand in extract_gpu(title_for_match):
        if cand in HARDWARE_TARGETS: return cand, HARDWARE_TARGETS[cand]
    for cand in extract_cpu(title_for_match):
        if cand in HARDWARE_TARGETS: return cand, HARDWARE_TARGETS[cand]
    for cand in extract_motherboard(title_for_match):
        if cand in HARDWARE_TARGETS: return cand, HARDWARE_TARGETS[cand]
    for cand in extract_psu(title_for_match):
        if cand in HARDWARE_TARGETS: return cand, HARDWARE_TARGETS[cand]
    for cand in extract_storage(title_for_match):
        if cand in HARDWARE_TARGETS: return cand, HARDWARE_TARGETS[cand]
    for cand in extract_ram(title_for_match):
        if cand in HARDWARE_TARGETS: return cand, HARDWARE_TARGETS[cand]

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
                    "barracuda", "hitachi", "seagate", "ironwolf"
                ])
            if not has_type: continue

            pattern = (r"(?<![a-z0-9])(1\s*(tb|тб|терабайт)|(1000|1024)\s*(gb|гб|гігабайт|гигабайт))(?![a-z0-9])"
                       if capacity_raw == "1tb" else
                       r"(?<![a-z0-9])" + cap_num + r"\s*(" + cap_unit + r"|тб|терабайт|гб|гігабайт)(?![a-z0-9])")

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
    rate_limiter = None
) -> list[dict]:
    subcat_key = subcat_info["subcategory"]
    item_type = subcat_info["item_type"]
    targets_for_this_type = {k: v for k, v in hardware_targets.items() if v.get("item_type") == item_type}

    search_params = [
        {"key": "category_id", "value": "458"},
        {"key": "filter_enum_subcategory[0]", "value": subcat_key},
        {"key": "currency", "value": "UAH"},
        {"key": "sort_by", "value": "created_at:desc"},
        {"key": "limit", "value": str(limit)},
        {"key": "offset", "value": str(offset)},
    ]

    json_payload = {"query": GRAPHQL_QUERY, "variables": {"searchParameters": search_params}}
    parsed_for_subcat = []

    for attempt in range(1, max_retries + 1):
        try:
            if rate_limiter:
                await rate_limiter.acquire()

            resp = await session.post("https://www.olx.ua/apigateway/graphql", json=json_payload, timeout=TIMEOUT)

            if rate_limiter:
                await rate_limiter.report_result(resp.status_code)

            if resp.status_code in (401, 403):
                await debugger.record_stat("Network", f"HTTP 403 ({subcat_key})")
                await asyncio.sleep(10)
                continue

            if resp.status_code != 200:
                await debugger.record_stat("Network", f"HTTP Status {resp.status_code}")
                await asyncio.sleep(2)
                continue

            res_json = resp.json()
            break
        except Exception as e:
            await debugger.record_stat("Network", "Мережева помилка")
            await asyncio.sleep(2)
            if attempt == max_retries:
                return []
    else:
        return []

    listings = res_json.get("data", {}).get("clientCompatibleListings", {}).get("data", [])
    await debugger.record_stat("OLX_GraphQL", f"Отримано [{subcat_key}]", len(listings))

    for item in listings:
        try:
            ad_subcat = None
            for param in item.get("params", []):
                if param.get("key") == "subcategory":
                    ad_subcat = (param.get("value") or {}).get("key")
                    break

            if ad_subcat and ad_subcat != subcat_key:
                await debugger.record_stat("Filtering_Rules", "Відсіяно (Невідповідність підкатегорії)")
                await debugger.add_sample(f"Filtered_{item_type}", {"reason": "mismatched_subcategory", "title": item.get("title")})
                continue

            title = str(item.get("title") or "Без назви").replace("'", "").strip()
            raw_url = item.get("url", "")
            if not raw_url:
                continue

            if not raw_url.startswith("http"):
                raw_url = "https://www.olx.ua" + raw_url
            advert_url = clean_url(raw_url)

            if advert_url in seen_urls:
                await debugger.add_sample(f"Filtered_{item_type}", {"reason": "duplicate_url_already_in_db", "url": advert_url, "title": title})
                continue

            matched = match_ad_to_hardware_target(title, targets_for_this_type)
            if not matched:
                await debugger.record_stat("Filtering_Rules", "Відсіяно (Не розпізнано модель)")
                await debugger.add_sample(f"Filtered_{item_type}", {"reason": "no_hardware_target_matched", "title": title})
                continue

            target_name, cfg = matched
            raw_ad_id = item.get("id")
            ad_id = int(raw_ad_id) if raw_ad_id and str(raw_ad_id).isdigit() else None
            description = str(item.get("description") or "").replace("<br />", "")
            full_text = f"{title} {description}"
            has_defects = 1 if is_broken_ad(full_text) else 0

            price = 0
            for param in item.get("params", []):
                if param.get("key") == "price":
                    price_val = param.get("value", {}).get("value", 0)
                    if isinstance(price_val, (int, float)) and price_val <= 1_000_000_000:
                        price = int(price_val)
                    break

            loc_data = item.get("location", {}) or {}
            city = loc_data.get("city", {}).get("name", "Невідомо") if loc_data.get("city") else "Невідомо"
            created_time_raw = str(item.get("created_time") or "")
            ad_date = created_time_raw.split("T")[0] if "T" in created_time_raw else "Невідомо"

            raw_photos = item.get("photos", []) or []
            photo_urls_list = [p.get("link", "").replace("{width}", "1000").replace("{height}", "750") for p in raw_photos if p and p.get("link")]

            user_data = item.get("user") or {}
            seller_id = str(user_data.get("id")) if user_data.get("id") else None
            seller_uuid = str(user_data.get("uuid")) if user_data.get("uuid") else None
            user_created_raw = str(user_data.get("created") or "")
            seller_created_at = user_created_raw.split("-")[0] if "-" in user_created_raw else None

            detected_socket = detect_socket(title, description, target_name) if item_type in ("motherboard", "cpu") else None
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
                "photo_url": photo_urls_list[0] if photo_urls_list else "Невідомо",
                "all_photos": ",".join(photo_urls_list) if photo_urls_list else None,
                "parsed_date": today_sql,
                "status": "active",
                "seller_id": seller_id,
                "seller_uuid": seller_uuid,
                "seller_name": user_data.get("name") or "Невідомо",
                "seller_created_at": seller_created_at,
                "seller_type": "shop" if item.get("business", False) else "private_person",
                "seller_price_clean": price,
                "bundle_components": bundle_components
            }

            parsed_for_subcat.append(ad_payload)
            seen_urls.add(advert_url)

            await debugger.record_stat("Parsing_Metrics", f"Успішно розпізнано [{item_type}]")
            await debugger.add_sample(f"Recognized_{item_type}", {"raw_title": title, "matched_target": target_name, "price_uah": price})
            print(f"   🎯 [РОЗПІЗНАНО: {target_name}]: {title[:40]}... ({price} грн)")

        except Exception as ex:
            await debugger.record_stat("Errors", f"Помилка елемента: {str(ex)[:40]}")
            continue

    return parsed_for_subcat


async def main_async(
    pages_to_parse: int = 1, 
    db_lock: asyncio.Lock | None = None,
    rate_limiter = None
) -> None:
    start_time = time.time()
    today_sql = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    def _fetch_seen_urls():
        try:
            res = supabase.table("ads").select("url").execute()
            return set(row["url"] for row in (res.data or []))
        except Exception as e:
            print(f"[ПОМИЛКА ЧИТАННЯ SUPABASE]: {e}")
            return set()

    if db_lock:
        async with db_lock:
            seen_urls = await asyncio.to_thread(_fetch_seen_urls)
    else:
        seen_urls = await asyncio.to_thread(_fetch_seen_urls)

    await debugger.record_stat("Supabase_Input", "Завантажено URLs для дедуплікації", len(seen_urls))
    print(f"[БАЗА SUPABASE] Завантажено {len(seen_urls)} комплектуючих для дедуплікації.")

    hardware_items = {k: v for k, v in HARDWARE_TARGETS.items() if not k.startswith("pc_")}
    await debugger.record_stat("Parser_Config", "Цільових моделей комплектуючих", len(hardware_items))

    proxy_kwargs = {"proxies": {"http": OLX_PROXY_URL, "https": OLX_PROXY_URL}} if OLX_PROXY_URL else {}

    async with AsyncSession(headers=HEADERS, impersonate="chrome124", **proxy_kwargs) as session:
        print("🔥 Прогріваємо сесію...")
        try:
            await session.get("https://www.olx.ua/uk/elektronika/", timeout=10)
        except Exception:
            pass

        all_results = []
        for subcat_info in SUBCATEGORIES_TO_PARSE:
            subcat_key = subcat_info["subcategory"]
            cat_name = subcat_info["name"]
            print(f"\n📡 Завантажуємо {cat_name} ({subcat_key}, сторінок: {pages_to_parse})...")

            for page in range(pages_to_parse):
                res = await fetch_subcategory_page(
                    session, subcat_info, hardware_items, seen_urls, today_sql,
                    offset=page * 40, limit=40, rate_limiter=rate_limiter
                )
                all_results.extend(res)
                if pages_to_parse > 1 and page < pages_to_parse - 1:
                    await asyncio.sleep(1.0)

    elapsed = time.time() - start_time
    await debugger.record_stat("Summary", "Знайдено нових унікальних оголошень", len(all_results))
    print(f"\n⏱️ Мережевий збір завершено за {elapsed:.2f} сек. (Нових: {len(all_results)})")

    if all_results:
        def _upsert():
            supabase.table("ads").upsert(all_results, on_conflict="ad_id").execute()

        try:
            if db_lock:
                async with db_lock:
                    await asyncio.to_thread(_upsert)
            else:
                await asyncio.to_thread(_upsert)

            await debugger.record_stat("Supabase_Output", "Успішно збережено в DB", len(all_results))
            print(f"[УСПІХ SUPABASE] Збережено {len(all_results)} нових комплектуючих у хмару!")

            try:
                async with aiohttp.ClientSession() as trigger_session:
                    await trigger_session.post("http://localhost:8000/api/trigger-new-ad", json=all_results, timeout=5)
                await debugger.record_stat("WebSocket", "Успішно надіслано тригер стріму")
                print("[WEBSOCKET] Живий стрим оновлено!")
            except Exception:
                await debugger.record_stat("WebSocket", "Помилка відправки тригеру")
        except Exception as ex:
            await debugger.record_stat("Supabase_Output", f"Помилка Upsert: {str(ex)[:40]}")
            print(f"❌ [ПОМИЛКА SUPABASE]: {ex}")
    else:
        await debugger.record_stat("Summary", "Немає нових оголошень для відправки в DB")

    await debugger.save_report_async()


def main(pages_to_parse: int = 1) -> None:
    """Точка входу для ручного запуска з консолі."""
    asyncio.run(main_async(pages_to_parse=pages_to_parse))


if __name__ == "__main__":
    main()
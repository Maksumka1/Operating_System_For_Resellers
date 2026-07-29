from __future__ import annotations

import asyncio
import re
import sys
import os
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse
from curl_cffi.requests import AsyncSession
from supabase import create_client, Client
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent
if not (PROJECT_ROOT / "config.py").exists():
    PROJECT_ROOT = PROJECT_ROOT.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from config import DB_FILE, HARDWARE_TARGETS, SOCKETS, CHIPSET_TO_SOCKET
load_dotenv(PROJECT_ROOT / ".env")
SUPABASE_URL = os.getenv("SUPABASE_URL", "https://nfhtmfhckctuyhfolhou.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_SECRET_KEY") or os.getenv("SUPABASE_PUBLISHABLE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY or "")


BROKEN_PATTERN = re.compile(
    r"неробоч|не робоч|запчастин|запчасть|ремонт|дефект|відновлен|восстановлен|"
    r"артефакт|поломан|неисправн|не справн|на детал|запчасті|прогрів|не стартует|"
    r"не включа|не включається|не включается|не працює|не работает|не робочий",
    re.IGNORECASE,
)

CLEAN_PATTERNS = re.compile(
    r"не\s*ремонтувал\w*|без\s*дефект\w*|без\s*артефакт\w*|не\s*прогрівав\w*|без\s*ремонт\w*",
    re.IGNORECASE
)

# 🎯 Патерн для очищення порівняльних слів ("сильніше за gtx 1650", "аналог rx 580" тощо)
COMPARISON_PATTERN = re.compile(
    r"(сильніше\s+за|мощнее\s+чем|быстрее\s+чем|аналог|замість|вмісто|вместо|похожа\s+на)\s+[a-z0-9\s_]+",
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


def validate_title_strict(title: str, required_keywords: list[str]) -> bool:
    """Сувора перевірка ключових слів з урахуванням меж слів."""
    title_lower = title.lower()
    for kw in required_keywords:
        kw_clean = kw.lower().strip()
        pattern = r"(?<![a-z0-9])" + re.escape(kw_clean) + r"(?![a-z0-9])"
        if re.search(pattern, title_lower):
            return True
    return False


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


def match_ad_to_hardware_target(title: str, target_items_for_type: dict) -> tuple[str, dict] | None:
    title_clean = title.lower()

    # 🎯 1. Прибираємо порівняльні фрази на кшталт "сильніше за gtx 1650"
    title_for_match = COMPARISON_PATTERN.sub("", title_clean)

    # 🎯 2. Сортуємо моделі за довжиною назви від найдовших до найкоротших
    sorted_targets = sorted(
        target_items_for_type.items(),
        key=lambda x: len(x[0]),
        reverse=True
    )

    for target_name, cfg in sorted_targets:
        req_keywords = cfg.get("required_keywords", [])

        if cfg.get("item_type") == "storage":
            parts = target_name.split("_")
            if len(parts) < 2:
                continue

            st_type = parts[0]
            capacity_raw = parts[1]
            cap_num = re.sub(r"\D", "", capacity_raw)
            cap_unit = "tb" if "tb" in capacity_raw else "gb"

            has_type = False
            if st_type == "ssd":
                has_type = "ssd" in title_for_match or "ссд" in title_for_match or "nvme" in title_for_match
            elif st_type == "hdd":
                has_type = any(w in title_for_match for w in [
                    "hdd", "хдд", "жорстк", "жестк", "винчестер", "жерстк", "toshiba",
                    "wd blue", "wd red", "wd black", "wd green", "barracuda", "wd"
                ])

            if not has_type:
                continue

            if cap_unit == "tb":
                pattern = r"(?<![a-z0-9])" + cap_num + r"\s*(tb|тб|терабайт|1000\s*gb|1000\s*гб)(?![a-z0-9])"
            else:
                pattern = r"(?<![a-z0-9])" + cap_num + r"\s*(gb|гб|гігабайт|гигабайт)?(?![a-z0-9])"

            if re.search(pattern, title_for_match):
                return target_name, cfg

        else:
            if validate_title_strict(title_for_match, req_keywords):
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
                print(f"[WARN 403] Блокування на '{subcat_key}'. Спроба {attempt}/{max_retries}. Чекаємо 10с...")
                await asyncio.sleep(10)
                continue

            if resp.status_code != 200:
                print(f"[ERR] HTTP Status {resp.status_code} для '{subcat_key}'")
                await asyncio.sleep(2)
                continue

            res_json = resp.json()
            break
        except Exception as e:
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

    if not listings:
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
                continue

            title = item.get("title", "Без назви").replace("'", "").strip()

            raw_url = item.get("url", "")
            if not raw_url:
                continue

            if not raw_url.startswith("http"):
                raw_url = "https://www.olx.ua" + raw_url

            advert_url = clean_url(raw_url)

            if advert_url in seen_urls:
                continue

            user_data = item.get("user") or {}
            seller_id = str(user_data.get("id")) if user_data.get("id") else None
            seller_uuid = str(user_data.get("uuid")) if user_data.get("uuid") else None
            seller_name = user_data.get("name") or "Невідомо"

            matched = match_ad_to_hardware_target(title, targets_for_this_type)
            if not matched:
                continue

            raw_ad_id = item.get("id")
            ad_id = int(raw_ad_id) if raw_ad_id and str(raw_ad_id).isdigit() else None

            target_name, cfg = matched
            description = (item.get("description") or "").replace("<br />", "")

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

            parsed_for_subcat.append({
                "ad_id": ad_id,
                "url": advert_url,
                "title": title,
                "description": description,
                "price": price,
                "item_type": item_type,
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
                "seller_price_clean": price
            })

            seen_urls.add(advert_url)

            defect_tag = " [⚠️ ДЕФЕКТ]" if has_defects else ""
            print(f"   🎯 [РОЗПІЗНАНО: {target_name}]{defect_tag}: {title[:40]}... ({price} грн)")

        except Exception as ex:
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
        print(f"[БАЗА SUPABASE] Завантажено {len(seen_urls)} комплектуючих для дедуплікації.")
    except Exception as e:
        print(f"[ПОМИЛКА ЧИТАННЯ SUPABASE]: {e}")
        seen_urls = set()

    hardware_items = {
        k: v for k, v in HARDWARE_TARGETS.items() if not k.startswith("pc_")
    }

    print(f"🚀 Стартуємо збір по підкатегоріях для {len(hardware_items)} моделей (сторінок на категорію: {pages_to_parse})...")
    start_time = time.time()

    new_ads_to_insert = asyncio.run(
        run_parser(hardware_items, seen_urls, today_sql, pages_to_parse=pages_to_parse)
    )

    elapsed = time.time() - start_time
    print(f"\n⏱️ Мережевий збір завершено за {elapsed:.2f} сек. (Знайдено нових комплектуючих: {len(new_ads_to_insert)})")

    # 2. Збереження у хмарний PostgreSQL Supabase та тригер WebSockets
    if new_ads_to_insert:
        try:
            supabase.table("ads").upsert(new_ads_to_insert, on_conflict="ad_id").execute()
            print(f"[УСПІХ SUPABASE] Збережено {len(new_ads_to_insert)} нових комплектуючих у хмару!")

            # 3. Тригеримо WebSocket на сервері для оновлення живого стріму
            try:
                import requests
                requests.post("http://localhost:8000/api/trigger-new-ad", json=new_ads_to_insert, timeout=2)
                print("📢 [WEBSOCKET] Живий стрим оновлено!")
            except Exception:
                pass

        except Exception as ex:
            print(f"❌ [ПОМИЛКА SUPABASE]: {ex}")
    else:
        print("[INFO] Нових оголошень для запису не знайдено.")


if __name__ == "__main__":
    main()
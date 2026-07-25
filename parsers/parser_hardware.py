from __future__ import annotations

import asyncio
import re
import sqlite3
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse
from curl_cffi.requests import AsyncSession

PROJECT_ROOT = Path(__file__).resolve().parent
if not (PROJECT_ROOT / "config.py").exists():
    PROJECT_ROOT = PROJECT_ROOT.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from config import DB_FILE, HARDWARE_TARGETS, SOCKETS, CHIPSET_TO_SOCKET

BROKEN_PATTERN = re.compile(
    r"неробоч|не робоч|запчастин|запчасть|ремонт|дефект|відновлен|восстановлен|"
    r"артефакт|поломан|неисправн|не справн|на детал|запчасті|прогрів|не стартует|"
    r"не включа|не включається|не включается|не працює|не работает|не робочий",
    re.IGNORECASE,
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


def get_db_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_FILE)
    conn.execute("PRAGMA journal_mode=WAL;")
    return conn


def validate_title(title: str, required_keywords: list[str]) -> bool:
    title_lower = title.lower()
    return any(word.lower() in title_lower for word in required_keywords)


def is_broken_ad(text: str) -> bool:
    return bool(BROKEN_PATTERN.search(text))


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

    for target_name, cfg in target_items_for_type.items():
        req_keywords = cfg.get("required_keywords", [])

        # 🎯 Гнучка логіка розпізнавання для накопичувачів (SSD / HDD)
        if cfg.get("item_type") == "storage":
            parts = target_name.split("_")  # Наприклад: ["ssd", "120gb"] або ["hdd", "1tb"]
            if len(parts) < 2:
                continue

            st_type = parts[0]  # ssd / hdd
            capacity_raw = parts[1]  # 120gb / 1tb
            cap_num = re.sub(r"\D", "", capacity_raw)  # 120 / 1
            cap_unit = "tb" if "tb" in capacity_raw else "gb"

            # 1. Перевіряємо тип накопичувача
            has_type = False
            if st_type == "ssd":
                has_type = "ssd" in title_clean or "ссд" in title_clean or "nvme" in title_clean
            elif st_type == "hdd":
                has_type = any(w in title_clean for w in [
                "hdd", "хдд", "жорстк", "жестк", "винчестер", "жерстк", "toshiba",
                "wd blue", "wd red", "wd black", "wd green", "barracuda", "wd"
            ])

            if not has_type:
                continue

            # 2. Перевіряємо наявність числа об'єму (з урахуванням пробілів та варіантів одиниць)
            if cap_unit == "tb":
                pattern = r"\b" + cap_num + r"\s*(tb|тб|терабайт|1000\s*gb|1000\s*гб)\b"
            else:
                pattern = r"(?<!\w)" + cap_num + r"\s*(gb|гб|гігабайт|гигабайт)?\b"

            if re.search(pattern, title_clean):
                return target_name, cfg

        # 🎯 Стандартна логіка для відеокарт, процесорів, материнок і БЖ
        else:
            if validate_title(title_clean, req_keywords):
                return target_name, cfg

    return None


async def fetch_subcategory_feed(
    session: AsyncSession,
    subcat_info: dict,
    hardware_targets: dict,
    seen_urls: set[str],
    today_sql: str,
    max_retries: int = 3,
) -> list[tuple]:
    subcat_key = subcat_info["subcategory"]
    item_type = subcat_info["item_type"]
    cat_name = subcat_info["name"]

    print(f"\n📡 Завантажуємо свіжі {cat_name} (підкатегорія: {subcat_key})...")

    targets_for_this_type = {
        k: v for k, v in hardware_targets.items() if v.get("item_type") == item_type
    }

    search_params = [
        {"key": "category_id", "value": "458"},
        {"key": "filter_enum_subcategory[0]", "value": subcat_key},
        {"key": "currency", "value": "UAH"},
        {"key": "sort_by", "value": "created_at:desc"},
        {"key": "limit", "value": "50"},
    ]

    json_payload = {
        "query": GRAPHQL_QUERY,
        "variables": {"searchParameters": search_params},
    }

    parsed_for_subcat = []

    for attempt in range(1, max_retries + 1):
        try:
            await asyncio.sleep(0.5)
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
        print(f"  [i] Порожній потік для підкатегорії {subcat_key}")
        return []

    print(f"  [+] Отримано {len(listings)} лотів з OLX. Починаємо обробку оголошень...")

    for item in listings:
        try:
            # 🎯 ФІЛЬТР 1: Перевірка підкатегорії у структурі JSON
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

            # 🎯 ФІЛЬТР 2: Дублікати
            if advert_url in seen_urls:
                print(f"   [🔄 ДУБЛІКАТ]: {title[:45]}...")
                continue

            # 🎯 ФІЛЬТР 3: Розпізнавання моделі
            matched = match_ad_to_hardware_target(title, targets_for_this_type)
            if not matched:
                print(f"   [⏭️ НЕ ВІДСТЕЖУЄТЬСЯ МОДЕЛЬ]: {title[:45]}...")
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

            detected_socket = None
            if item_type in ("motherboard", "cpu"):
                detected_socket = detect_socket(title, description, target_name)

            parsed_for_subcat.append(
                (
                    ad_id,
                    advert_url,
                    title,
                    description,
                    price,
                    item_type,
                    target_name,
                    detected_socket,
                    has_defects,
                    city,
                    ad_date,
                    first_photo,
                    all_photos_str,
                    today_sql,
                    "active",
                )
            )

            seen_urls.add(advert_url)

            defect_tag = " [⚠️ ДЕФЕКТ]" if has_defects else ""
            print(f"   🎯 [РОЗПІЗНАНО: {target_name}]{defect_tag}: {title[:40]}... ({price} грн)")

        except Exception as ex:
            print(f"   [!] Помилка обробки елемента: {ex}")
            continue

    return parsed_for_subcat


async def run_parser(
    hardware_items: dict, seen_urls: set[str], today_sql: str
) -> list[tuple]:
    async with AsyncSession(headers=HEADERS, impersonate="chrome124") as session:
        print("🔥 Прогріваємо сесію...")
        try:
            await session.get("https://www.olx.ua/uk/elektronika/", timeout=10)
        except Exception:
            pass

        all_results = []
        for subcat_info in SUBCATEGORIES_TO_PARSE:
            res = await fetch_subcategory_feed(
                session, subcat_info, hardware_items, seen_urls, today_sql
            )
            all_results.extend(res)

    return all_results


def main() -> None:
    today_sql = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    if not DB_FILE.exists():
        print("[ПОМИЛКА] Базу даних не знайдено!")
        return

    conn = get_db_connection()
    cursor = conn.cursor()

    for col_def in ["all_photos TEXT", "ad_id INTEGER", "socket TEXT", "has_defects INTEGER DEFAULT 0"]:
        try:
            cursor.execute(f"ALTER TABLE ads ADD COLUMN {col_def};")
        except sqlite3.OperationalError:
            pass

    cursor.execute("SELECT url FROM ads")
    seen_urls = set(row[0] for row in cursor.fetchall())

    hardware_items = {
        k: v for k, v in HARDWARE_TARGETS.items() if not k.startswith("pc_")
    }

    print(f"🚀 Стартуємо швидкісний збір по підкатегоріях для {len(hardware_items)} відстежуваних моделей...")
    start_time = time.time()

    new_ads_to_insert = asyncio.run(
        run_parser(hardware_items, seen_urls, today_sql)
    )

    elapsed = time.time() - start_time
    print(f"\n⏱️ Мережевий збір завершено за {elapsed:.2f} сек. (Знайдено нових комплектуючих: {len(new_ads_to_insert)})")

    if new_ads_to_insert:
        cursor.executemany(
            """
        INSERT OR IGNORE INTO ads (
            ad_id, url, title, description, price, item_type, component_name, 
            socket, has_defects, city, created_at_olx, photo_url, all_photos, parsed_date, status
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
            new_ads_to_insert,
        )
        conn.commit()
        print(f"[УСПІХ] Збережено {len(new_ads_to_insert)} нових унікальних комплектуючих у 'ads'.")
    else:
        print("[INFO] Нових оголошень для запису не знайдено.")

    conn.close()


if __name__ == "__main__":
    main()
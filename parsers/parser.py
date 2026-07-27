from __future__ import annotations

import os
import asyncio
import json
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

from curl_cffi.requests import AsyncSession
from supabase import create_client, Client

PROJECT_ROOT = Path(__file__).resolve().parent
if not (PROJECT_ROOT / "config.py").exists():
    PROJECT_ROOT = PROJECT_ROOT.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from config import STATS_FILE

# --- ПІДКТЮЧЕННЯ ДО SUPABASE ---
SUPABASE_URL = os.getenv("SUPABASE_URL", "https://nfhtmfhckctuyhfolhou.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_SECRET_KEY") or os.getenv("SUPABASE_PUBLISHABLE_KEY")

if not SUPABASE_KEY:
    print("⚠️ [УВАГА] Не вказано SUPABASE_SECRET_KEY / SUPABASE_PUBLISHABLE_KEY у змінних середовища!")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY or "")

TIMEOUT = 15

NOT_A_PC_WORDS = [
    "материнська плата", "материнская плата", "материнка", "мать", 
    "блок питания", "блок живлення", "дбж", "ups", "бесперебойник",
    "оперативна память", "оперативная память", "озу", "ram",
    "кулер", "вентилятор", "корпус без", "видеокарта", "відеокарта", 
    "процессор", "процесор", "ssd", "hdd", "жесткий диск", "жорсткий диск"
]

HEADERS = {
    "accept": "application/json",
    "accept-language": "uk",
    "content-type": "application/json",
    "origin": "https://www.olx.ua",
    "priority": "u=1, i",
    "referer": "https://www.olx.ua/",
    "sec-ch-ua": '"Not;A=Brand";v="8", "Chromium";v="124", "Google Chrome";v="124"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "x-client": "DESKTOP",
}

GRAPHQL_QUERY = """query ListingSearchQuery($searchParameters: [SearchParameter!] = []) {
  clientCompatibleListings(searchParameters: $searchParameters) {
    ... on ListingSuccess {
      data {
        id title status url created_time last_refresh_time description business
        location { city { name } }
        photos { link }
        user { id uuid name created }
        params {
          key name
          value {
            ... on PriceParam { value currency label }
          }
        }
      }
    }
  }
}"""


def clean_url(url: str) -> str:
    parsed = urlparse(url)
    return f"{parsed.scheme}://{parsed.netloc}{parsed.path}"


def extract_price(price_val: str | int | float) -> int:
    if isinstance(price_val, (int, float)):
        return int(price_val)
    digits = re.sub(r"\D", "", str(price_val))
    return int(digits) if digits else 0


def is_real_pc(title: str) -> bool:
    if not title:
        return False
        
    title_lower = title.lower()
    pc_indicators = ["пк", "комп", "системний блок", "системный блок", "компьютер", "комп’ютер", "системник", "pc", "mac", "блок"]

    for bad_word in NOT_A_PC_WORDS:
        if bad_word in title_lower:
            if title_lower.startswith(bad_word):
                return False
            if not any(indicator in title_lower for indicator in pc_indicators):
                return False

    return True


def update_statistics(section: str, metrics: dict) -> None:
    today_str = datetime.now(timezone.utc).strftime("%d-%m-%Y")
    stats = {}

    if STATS_FILE.exists():
        try:
            stats = json.loads(STATS_FILE.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            stats = {}

    if today_str not in stats:
        stats[today_str] = {
            "parsing": {
                "parsed_total_new": 0,
                "duplicates_skipped": 0,
                "avg_parsing_time_ms": 0.0,
                "total_time_seconds": 0.0,
            },
            "filtering": {
                "banned_words_triggered": 0,
                "filtered_total_active": 0,
            },
            "market_analysis": {
                "avg_ad_price_uah": 0,
                "min_price_today": 0,
                "max_price_today": 0,
            },
            "system_health": {"network_errors": 0, "parsing_errors": 0},
        }

    if section in stats[today_str]:
        stats[today_str][section].update(metrics)

    STATS_FILE.write_text(
        json.dumps(stats, ensure_ascii=False, indent=2), encoding="utf-8"
    )


async def fetch_pcs_page(
    session: AsyncSession,
    seen_urls: set[str],
    offset: int = 0,
    limit: int = 40,
    max_retries: int = 5,
) -> tuple[list[dict], int, int, int]:
    json_payload = {
        "query": GRAPHQL_QUERY,
        "variables": {
            "searchParameters": [
                {"key": "category_id", "value": "78"},
                {"key": "limit", "value": str(limit)},
                {"key": "sort_by", "value": "created_at:desc"},
                {"key": "offset", "value": str(offset)},
            ]
        },
    }

    new_items = []
    duplicates_count = 0
    network_errors = 0
    parsing_errors = 0

    today_sql = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    for attempt in range(1, max_retries + 1):
        try:
            resp = await session.post(
                "https://www.olx.ua/apigateway/graphql",
                json=json_payload,
                timeout=TIMEOUT,
            )

            if resp.status_code in (401, 403):
                print(f"[WARN GraphQL] 403 Forbidden. Спроба {attempt}/{max_retries}. Прогрів та чекаємо 10s...")
                network_errors += 1
                try:
                    await session.get("https://www.olx.ua/uk/elektronika/", timeout=10)
                except Exception:
                    pass
                await asyncio.sleep(10)
                continue

            if resp.status_code != 200:
                print(f"[ERR GraphQL] HTTP status {resp.status_code}. Спроба {attempt}/{max_retries}...")
                network_errors += 1
                await asyncio.sleep(attempt * 3)
                continue

            data = resp.json()
            listings = (
                data.get("data", {})
                .get("clientCompatibleListings", {})
                .get("data", [])
            )

            for item in listings:
                try:
                    raw_id = item.get("id")
                    ad_id = int(raw_id) if raw_id and str(raw_id).isdigit() else None

                    raw_url = item.get("url", "")
                    if not raw_url:
                        continue

                    if not raw_url.startswith("http"):
                        raw_url = "https://www.olx.ua" + raw_url

                    advert_url = clean_url(raw_url)

                    if advert_url in seen_urls:
                        duplicates_count += 1
                        continue

                    title = item.get("title", "").replace("'", "").strip()

                    if not is_real_pc(title):
                        print(f"   [🚫 ВІДСІЯНО ЗАПЧАСТИНУ]: {title[:50]}...")
                        continue

                    description = item.get("description", "").strip().replace("<br />", "\n").replace("<br>", "\n")

                    price = 0
                    for param in item.get("params", []):
                        if param.get("key") == "price":
                            val_data = param.get("value", {})
                            price = extract_price(val_data.get("value", 0))
                            break

                    loc_data = item.get("location", {}) or {}
                    city = loc_data.get("city", {}).get("name", "Невідомо") if loc_data.get("city") else "Невідомо"

                    created_time_raw = item.get("created_time", "")
                    created_at_olx = created_time_raw.split("T")[0] if "T" in created_time_raw else "Невідомо"
                    last_refresh_time = item.get("last_refresh_time") or "Невідомо"

                    raw_photos = item.get("photos", []) or []
                    formatted_photos = [
                        p.get("link", "").replace("{width}", "1000").replace("{height}", "750")
                        for p in raw_photos if p.get("link")
                    ]

                    photo_url = formatted_photos[0] if formatted_photos else "Невідомо"
                    additional_photos_str = ",".join(formatted_photos[1:]) if len(formatted_photos) > 1 else None
                    all_photos_str = ",".join(formatted_photos) if formatted_photos else None

                    user_data = item.get("user") or {}
                    seller_id = str(user_data.get("id")) if user_data.get("id") else None
                    seller_uuid = str(user_data.get("uuid")) if user_data.get("uuid") else None
                    seller_name = user_data.get("name") or "Невідомо"
                    
                    user_created_raw = user_data.get("created") or ""
                    seller_created_at = user_created_raw.split("-")[0] if user_created_raw else None
                    
                    is_business = item.get("business", False)
                    seller_type = "shop" if is_business else "private_person"

                    # Замість tuple створюємо дикт для Supabase
                    ad_dict = {
                        "ad_id": ad_id,
                        "url": advert_url,
                        "parsed_date": today_sql,
                        "status": "active",
                        "title": title,
                        "description": description,
                        "price": price,
                        "item_type": "pc",
                        "component_name": None,
                        "city": city,
                        "created_at_olx": created_at_olx,
                        "last_refresh_time": last_refresh_time,
                        "photo_url": photo_url,
                        "photos": additional_photos_str,
                        "all_photos": all_photos_str,
                        "seller_id": seller_id,
                        "seller_uuid": seller_uuid,
                        "seller_name": seller_name,
                        "seller_created_at": seller_created_at,
                        "seller_type": seller_type,
                        "seller_price_clean": price
                    }

                    new_items.append(ad_dict)
                    seen_urls.add(advert_url)
                    print(f"   [+] Новий ПК [ID: {ad_id}]: {title[:45]}... ({price} грн)")

                except Exception as ex:
                    parsing_errors += 1
                    print(f"[ПОМИЛКА ПАРСИНГУ] Елемент оголошення: {ex}")

            return new_items, duplicates_count, network_errors, parsing_errors

        except Exception as ex:
            network_errors += 1
            print(f"[ПОМИЛКА МЕРЕЖІ] Спроба {attempt}/{max_retries}: {ex}")
            await asyncio.sleep(attempt * 2)

    print(f"❌ [КРИТИЧНО] Не вдалося завантажити ПК після {max_retries} спроб.")
    return new_items, duplicates_count, network_errors, parsing_errors


async def main_async(pages_to_parse: int = 1) -> None:
    start_time = time.time()

    # Завантажуємо існуючі URL з Supabase для дедуплікації
    try:
        response = supabase.table("ads").select("url").execute()
        seen_urls = set(row["url"] for row in (response.data or []))
        print(f"[БАЗА SUPABASE] Завантажено {len(seen_urls)} оголошень для дедуплікації.")
    except Exception as e:
        print(f"[ПОМИЛКА ЧИТАННЯ SUPABASE]: {e}")
        seen_urls = set()

    async with AsyncSession(headers=HEADERS, impersonate="chrome124") as session:
        print("🔥 Прогріваємо сесію OLX...")
        try:
            await session.get("https://www.olx.ua/", timeout=15)
            await asyncio.sleep(0.5)
        except Exception as e:
            print(f"[WARN Warmup] Помилка прогріву: {e}")

        all_new_pcs = []
        total_duplicates = 0
        total_net_errors = 0
        total_parse_errors = 0

        print(f"\n🎯 [ПАРСИНГ] Починаємо збір (кількість сторінок: {pages_to_parse})...")
        for page in range(pages_to_parse):
            offset = page * 40
            print(f"   📂 Сторінка {page + 1}/{pages_to_parse} (offset={offset})...")
            
            items, dups, net_err, parse_err = await fetch_pcs_page(
                session, seen_urls, offset=offset, limit=40
            )
            all_new_pcs.extend(items)
            total_duplicates += dups
            total_net_errors += net_err
            total_parse_errors += parse_err
            
            if pages_to_parse > 1 and page < pages_to_parse - 1:
                await asyncio.sleep(1.5)

    new_parsed_count = len(all_new_pcs)

    # Збереження в Supabase та трансляція через WebSocket
    if all_new_pcs:
        try:
            # Upsert у хмарний PostgreSQL
            supabase.table("ads").upsert(all_new_pcs, on_conflict="url").execute()
            print(f"\n[УСПІХ SUPABASE] Збережено {new_parsed_count} нових ПК у хмару!")

            # Надсилаємо нові лоти на наш FastAPI server.py, щоб спрацювала WebSocket-анімація на сайті
            try:
                await session.post("http://localhost:8000/api/trigger-new-ad", json=all_new_pcs)
                print("📢 [WEBSOCKET] Трансляцію нових лотів на фронтенд успішно відправлено!")
            except Exception as ws_err:
                print(f"⚠️ [WEBSOCKET WARN] Не вдалося тригернути WebSocket на сервері: {ws_err}")

        except Exception as e:
            print(f"\n❌ [ПОМИЛКА ЗБЕРЕЖЕННЯ В SUPABASE]: {e}")
    else:
        print("\n[INFO] Нових комп'ютерів у цій ітерації немає.")

    end_time = time.time()
    total_time_seconds = end_time - start_time
    total_time_ms = total_time_seconds * 1000
    avg_time = (
        round(total_time_ms / new_parsed_count, 2)
        if new_parsed_count > 0
        else 0
    )

    print(f"⏱️ Час парсингу: {total_time_seconds:.2f} сек")

    update_statistics(
        "parsing",
        {
            "parsed_total_new": new_parsed_count,
            "duplicates_skipped": total_duplicates,
            "avg_parsing_time_ms": avg_time,
            "total_time_seconds": round(total_time_seconds, 2),
        },
    )

    update_statistics(
        "system_health",
        {
            "network_errors": total_net_errors,
            "parsing_errors": total_parse_errors,
        },
    )


def main(pages_to_parse: int = 1) -> None:
    asyncio.run(main_async(pages_to_parse=pages_to_parse))


if __name__ == "__main__":
    main()
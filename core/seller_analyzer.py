from __future__ import annotations

import asyncio
import json
import random
import re
import sqlite3
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

from curl_cffi.requests import AsyncSession

PROJECT_ROOT = Path(__file__).resolve().parent
if not (PROJECT_ROOT / "config.py").exists():
    PROJECT_ROOT = PROJECT_ROOT.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

try:
    from config import DB_FILE
except ImportError:
    DB_FILE = "ads.db"

CONCURRENT_REQUESTS = 3  # Оптимально для високої швидкості
PROCESSED_COUNT = 0
COUNT_LOCK = asyncio.Lock()
TIMEOUT = 12

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
    "x-client": "DESKTOP",  # 🎯 КРИТИЧНИЙ ЗОЛОТИЙ ХЕДЕР
}

GRAPHQL_QUERY = """query ListingSearchQuery($searchParameters: [SearchParameter!] = []) {
  clientCompatibleListings(searchParameters: $searchParameters) {
    ... on ListingSuccess {
      data {
        id title status url created_time valid_to_time last_refresh_time description business
        location { city { name } }
        contact { name phone chat }
        photos { link }
        user { id uuid name created is_online last_seen company_name }
        params {
          key name
          value {
            ... on PriceParam { value currency label }
            ... on GenericParam { label }
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


def clean_search_query(text: str) -> str:
    if not text:
        return ""
    cleaned = re.sub(r"[^\w\s]", " ", text, flags=re.UNICODE)
    words = cleaned.split()
    short_query = " ".join(words[:4])
    return short_query[:35].strip()


async def warmup_session(session: AsyncSession) -> bool:
    """Отримує початкові DataDome та OLX cookies."""
    print("🔥 Ініціалізація та прогрів DataDome сесії...")
    try:
        resp = await session.get("https://www.olx.ua/uk/elektronika/", timeout=TIMEOUT)
        if resp.status_code == 200:
            print("[Warmup] Сесію успішно ініціалізовано!")
            return True
    except Exception as e:
        print(f"[WARN Warmup] Помилка прогріву: {e}")
    return False


async def fetch_delivery_deals(session: AsyncSession, seller_id: str) -> int:
    if not seller_id or seller_id == "failed":
        return 0
    url = f"https://khonor.eu-sharedservices.olxcdn.com/api/olx/ua/user/{seller_id}/badge/delivery"
    try:
        resp = await session.get(url, timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            for badge in data.get("body", []):
                if badge.get("name") == "delivery":
                    return int(badge.get("data", {}).get("amount", 0))
    except Exception:
        pass
    return 0


async def fetch_seller_rating(session: AsyncSession, seller_uuid: str) -> str:
    if not seller_uuid:
        return "немає оцінок"
    url = f"https://rating-cdn.css.olx.io/ratings/v1/public/olxua/user/{seller_uuid}/eligibleClusters?includeScores=true"
    try:
        resp = await session.get(url, timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            clusters = data.get("clusters", [])
            if clusters:
                cluster = clusters[0]
                score = cluster.get("scoreDetails", {}).get("value", None)
                total_ratings = cluster.get("scoreDetails", {}).get("ratings", {}).get("totalCount", 0)
                if score is not None and total_ratings > 0:
                    return f"{score}/5.0 ({total_ratings} оцінок)"
    except Exception:
        pass
    return "немає оцінок"


async def fetch_ad_graphql(session: AsyncSession, ad_id: int | str, url: str, title: str) -> dict | None:
    search_params = []
    if ad_id and str(ad_id).isdigit():
        search_params = [{"key": "id", "value": str(ad_id)}]
    else:
        search_phrase = clean_search_query(title)
        if not search_phrase:
            match = re.search(r"/obyavlenie/(.*?)(?:-ID|\.html)", url)
            if match:
                search_phrase = clean_search_query(match.group(1).replace("-", " "))
        search_params = [
            {"key": "query", "value": search_phrase},
            {"key": "limit", "value": "10"},
        ]

    json_payload = {
        "query": GRAPHQL_QUERY,
        "variables": {"searchParameters": search_params},
    }

    for attempt in range(2):
        try:
            # Мінімальна затримка для збереження швидкості
            await asyncio.sleep(random.uniform(0.1, 0.2))

            resp = await session.post(
                "https://www.olx.ua/apigateway/graphql",
                json=json_payload,
                timeout=TIMEOUT,
            )

            if resp.status_code in (401, 403):
                print(f"[WARN GraphQL] {resp.status_code} Заблоковано (ad_id={ad_id}). Оновлюємо сесію...")
                await warmup_session(session)
                await asyncio.sleep(0.5)
                continue

            if resp.status_code != 200:
                print(f"[ERR GraphQL] HTTP status {resp.status_code} (ad_id={ad_id})")
                return None

            data = resp.json()
            listings = (
                data.get("data", {})
                .get("clientCompatibleListings", {})
                .get("data", [])
            )

            if not listings:
                print(f"[ERR GraphQL] Порожній результат для ad_id={ad_id}")
                return None

            target_ad = listings[0]
            str_ad_id = str(ad_id)

            for item in listings:
                item_id = str(item.get("id", ""))
                if item_id and (item_id == str_ad_id or item_id in url):
                    target_ad = item
                    break

            raw_photos = target_ad.get("photos", [])
            photo_urls_list = []
            for p in raw_photos:
                link = p.get("link", "") if isinstance(p, dict) else ""
                if link:
                    formatted_link = link.replace("{width}", "1000").replace("{height}", "750")
                    photo_urls_list.append(formatted_link)

            all_photos_str = ",".join(photo_urls_list) if photo_urls_list else None
            first_photo = photo_urls_list[0] if photo_urls_list else None

            user_data = target_ad.get("user", {}) or {}
            loc_data = target_ad.get("location", {}) or {}

            seller_id = str(user_data.get("id", ""))
            seller_uuid = str(user_data.get("uuid", ""))
            created_raw = user_data.get("created", "")
            created_year = created_raw.split("-")[0] if created_raw else "Невідомо"

            successful_deals = await fetch_delivery_deals(session, seller_id)
            seller_rating = await fetch_seller_rating(session, seller_uuid)

            return {
                "seller_id": seller_id,
                "seller_name": user_data.get("name", "Невідомо"),
                "seller_created_at": created_year,
                "seller_successful_deals": successful_deals,
                "seller_rating": seller_rating,
                "is_company": target_ad.get("business", False),
                "olx_created_time": target_ad.get("created_time"),
                "olx_refresh_time": target_ad.get("last_refresh_time"),
                "olx_city_name": loc_data.get("city", {}).get("name") if loc_data.get("city") else None,
                "olx_photo_url": first_photo,
                "all_photos": all_photos_str,
                "description": target_ad.get("description"),
            }

        except Exception as e:
            print(f"[EXC GraphQL] Помилка обробки ad_id={ad_id}: {e}")
            return None

    return None


async def process_single_ad_worker(
    session: AsyncSession,
    ad_data: tuple,
    semaphore: asyncio.Semaphore,
) -> dict:
    global PROCESSED_COUNT
    db_id, ad_id, url, price, item_type, title = ad_data

    async with semaphore:
        # 🎯 Автоматична перерва на 15 секунд кожні 100 запитів для скидання DataDome Rate Limit
        async with COUNT_LOCK:
            PROCESSED_COUNT += 1
            if PROCESSED_COUNT % 100 == 0:
                print(f"\n⏳ [{PROCESSED_COUNT} лотів оброблено] Пауза 25 сек для скидання ліміту DataDome...\n")
                await asyncio.sleep(25)

        seller_info = await fetch_ad_graphql(session, ad_id, url, title)

    if seller_info:
        print(f"[{db_id}] Оголошення (OLX ID: {ad_id}) успішно пройшло перевірку")
    else:
        print(f"[{db_id}] Оголошення (OLX ID: {ad_id}) — помилка обробки")

    if not seller_info:
        return {"db_id": db_id, "status": "failed"}

    real_olx_ads_count = seller_info["seller_successful_deals"]
    rating_str = seller_info["seller_rating"]

    seller_stars = 0.0
    if rating_str and rating_str != "немає оцінок":
        try:
            match = re.match(r"([0-9.]+)/5\.0", rating_str)
            if match:
                seller_stars = float(match.group(1))
        except Exception:
            pass

    today_year = datetime.now(timezone.utc).year
    try:
        reg_year = int(seller_info["seller_created_at"])
        acc_age_years = today_year - reg_year
    except ValueError:
        acc_age_years = 0

    is_low_deals = real_olx_ads_count < 20
    is_bad_rating = seller_stars < 4.0
    is_new_account = acc_age_years <= 1

    if is_low_deals or is_bad_rating or is_new_account:
        seller_risk = "suspicious"
    elif acc_age_years >= 2 or real_olx_ads_count >= 50:
        seller_risk = "safe"
    else:
        seller_risk = "neutral"

    is_company = seller_info["is_company"]
    if is_company or (real_olx_ads_count > 50 and seller_stars >= 4.0):
        seller_type = "shop"
    elif not is_company and real_olx_ads_count > 50:
        seller_type = "reseller"
    else:
        seller_type = "private_person"

    return {
        "status": "success",
        "db_id": db_id,
        "ad_id": ad_id,
        "url": url,
        "price": price,
        "title": title,
        "item_type": item_type,
        "seller_info": seller_info,
        "real_olx_ads_count": real_olx_ads_count,
        "seller_type": seller_type,
        "seller_risk": seller_risk,
    }


async def run_seller_analysis_async(ads_to_check: list[tuple]) -> list[dict]:
    semaphore = asyncio.Semaphore(CONCURRENT_REQUESTS)

    async with AsyncSession(headers=HEADERS, impersonate="chrome124") as session:
        await warmup_session(session)

        tasks = [
            process_single_ad_worker(session, ad_data, semaphore)
            for ad_data in ads_to_check
        ]
        results = await asyncio.gather(*tasks)

    return results


def run_seller_analysis() -> list[int]:
    global PROCESSED_COUNT
    PROCESSED_COUNT = 0  # Скидаємо лічильник перед запуском нового аналізу

    print("\n" + "=" * 60)
    print("🕵️‍♂️ ЗАПУСК GRAPHQL API АНАЛІЗУ (З ТОЧНИМ ПОШУКОМ ЗА AD_ID)")
    print("=" * 60)

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, ad_id, url, price, item_type, title 
        FROM ads 
        WHERE (seller_id IS NULL OR seller_id = 'failed') 
          AND status = 'active' 
          AND (has_defects = 0 OR has_defects IS NULL)
    """)
    ads_to_check = cursor.fetchall()
    conn.close()

    if not ads_to_check:
        print("[ANALYZER] Немає нових або 'failed' оголошень для аналізу.")
        return []

    print(f"[ANALYZER] Знайдено {len(ads_to_check)} лотів. Запускаємо асинхронну обробку...")
    start_time = time.time()

    results = asyncio.run(run_seller_analysis_async(ads_to_check))

    conn = get_db_connection()
    cursor = conn.cursor()

    for col in ["photos", "all_photos"]:
        try:
            cursor.execute(f"ALTER TABLE ads ADD COLUMN {col} TEXT;")
        except sqlite3.OperationalError:
            pass

    success_ids = []
    failed_count = 0

    print("\n💾 Запис результатів у базу даних...")
    for res in results:
        if not res:
            continue

        db_id = res["db_id"]

        if res["status"] == "failed":
            cursor.execute("UPDATE ads SET seller_id = 'failed' WHERE id = ?", (db_id,))
            failed_count += 1
            continue

        info = res["seller_info"]

        cursor.execute(
            """
            UPDATE ads 
            SET 
                seller_id = ?,
                seller_name = ?,
                seller_created_at = ?,
                seller_successful_deals = ?,
                seller_rating = ?,
                seller_type = ?,
                seller_risk_score = ?,
                photo_url = COALESCE(?, photo_url),
                photos = COALESCE(?, photos),
                all_photos = COALESCE(?, all_photos),
                description = COALESCE(?, description)
            WHERE id = ?
        """,
            (
                info["seller_id"],
                info["seller_name"],
                info["seller_created_at"],
                res["real_olx_ads_count"],
                info["seller_rating"],
                res["seller_type"],
                res["seller_risk"],
                info.get("olx_photo_url"),
                info.get("all_photos"),
                info.get("all_photos"),
                info.get("description"),
                db_id,
            ),
        )

        update_fields = {}
        if info.get("olx_city_name"):
            update_fields["city"] = info["olx_city_name"]

        if info.get("olx_created_time"):
            try:
                update_fields["created_at_olx"] = info["olx_created_time"].split("T")[0]
            except Exception:
                update_fields["created_at_olx"] = info["olx_created_time"]

        if info.get("olx_refresh_time"):
            update_fields["last_refresh_time"] = info["olx_refresh_time"]

        if update_fields:
            sql_set_parts = [f"{key} = ?" for key in update_fields.keys()]
            sql_query = f"UPDATE ads SET {', '.join(sql_set_parts)} WHERE id = ?"
            sql_params = list(update_fields.values()) + [db_id]
            cursor.execute(sql_query, sql_params)

        success_ids.append(db_id)

    conn.commit()
    conn.close()

    elapsed = time.time() - start_time
    print(f"\n[УСПІХ] Обробку завершено за {elapsed:.2f} сек!")
    print(f"Успішно проаналізовано: {len(success_ids)}, Помилок: {failed_count}")
    return success_ids


if __name__ == "__main__":
    run_seller_analysis()
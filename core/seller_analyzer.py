import os
import asyncio
import re
import sys
import time
from dotenv import load_dotenv
from datetime import datetime, timezone
from pathlib import Path
from collections import defaultdict

from curl_cffi.requests import AsyncSession
from supabase import create_client, Client

PROJECT_ROOT = Path(__file__).resolve().parent
if not (PROJECT_ROOT / "config.py").exists():
    PROJECT_ROOT = PROJECT_ROOT.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
load_dotenv(PROJECT_ROOT / ".env")

SUPABASE_URL = os.getenv("SUPABASE_URL", "https://nfhtmfhckctuyhfolhou.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_SECRET_KEY") or os.getenv("SUPABASE_PUBLISHABLE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY or "")

CONCURRENT_REQUESTS = 5
PROCESSED_COUNT = 0
COUNT_LOCK = asyncio.Lock()
TIMEOUT = 8

HEADERS = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "uk-UA,uk;q=0.9,en-US;q=0.8,en;q=0.7",
    "origin": "https://www.olx.ua",
    "referer": "https://www.olx.ua/",
    "sec-ch-ua": '"Not;A=Brand";v="8", "Chromium";v="124", "Google Chrome";v="124"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "cross-site",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "x-client": "DESKTOP",
}


async def fetch_delivery_deals(session: AsyncSession, seller_id: str) -> int:
    if not seller_id or str(seller_id).strip() in ("", "failed", "None"):
        return 0

    url = f"https://khonor.eu-sharedservices.olxcdn.com/api/olx/ua/user/{seller_id}/badge/delivery"
    try:
        resp = await session.get(url, timeout=TIMEOUT)
        if resp.status_code == 200:
            data = resp.json()
            for badge in data.get("body", []):
                if badge.get("name") == "delivery":
                    return int(badge.get("data", {}).get("amount", 0))
    except Exception:
        pass
    return 0


async def fetch_seller_rating(session: AsyncSession, seller_uuid: str) -> str:
    if not seller_uuid or str(seller_uuid).strip() in ("", "failed", "None"):
        return "немає оцінок"

    url = f"https://rating-cdn.css.olx.io/ratings/v1/public/olxua/user/{seller_uuid}/eligibleClusters?includeScores=true"
    try:
        resp = await session.get(url, timeout=TIMEOUT)
        if resp.status_code == 200:
            data = resp.json()
            clusters = data.get("clusters", [])
            if clusters:
                cluster = clusters[0]
                score_details = cluster.get("scoreDetails", {})
                score = score_details.get("value")
                total_ratings = score_details.get("ratings", {}).get("totalCount", 0)

                if score is not None and total_ratings > 0:
                    return f"{score}/5.0 ({total_ratings} оцінок)"
    except Exception:
        pass
    return "немає оцінок"


async def process_single_seller_worker(
    session: AsyncSession,
    ad_data: tuple,
    semaphore: asyncio.Semaphore,
) -> dict:
    global PROCESSED_COUNT
    db_id, seller_id, seller_uuid, seller_created_at, seller_type_raw = ad_data

    async with semaphore:
        async with COUNT_LOCK:
            PROCESSED_COUNT += 1

        successful_deals, rating_str = await asyncio.gather(
            fetch_delivery_deals(session, seller_id),
            fetch_seller_rating(session, seller_uuid),
        )

    seller_stars = 0.0
    has_rating = False
    if rating_str and rating_str != "немає оцінок":
        try:
            match = re.match(r"([0-9.]+)/5\.0", rating_str)
            if match:
                seller_stars = float(match.group(1))
                has_rating = True
        except Exception:
            pass

    today_year = datetime.now(timezone.utc).year
    acc_age_years = 0

    if seller_created_at:
        match = re.search(r"\b(19|20)\d{2}\b", str(seller_created_at))
        if match:
            reg_year = int(match.group(0))
            acc_age_years = max(0, today_year - reg_year)

    stars = seller_stars if has_rating else 0.0

    is_safe = (successful_deals >= 20) and (stars >= 4.0) and (acc_age_years > 2)
    is_neutral = (successful_deals >= 10) and (stars > 3.0) and (acc_age_years >= 2)

    if is_safe:
        seller_risk = "safe"
    elif is_neutral:
        seller_risk = "neutral"
    else:
        seller_risk = "suspicious"

    is_shop = seller_type_raw == "shop"
    if is_shop or (successful_deals > 50 and seller_stars >= 4.0):
        final_seller_type = "shop"
    elif not is_shop and successful_deals > 30:
        final_seller_type = "reseller"
    else:
        final_seller_type = "private_person"

    print(f"  [+] [ID: {db_id}] Продавець: {seller_id} | Угод: {successful_deals} | Рейтинг: {rating_str} | Ризик: {seller_risk}")

    return {
        "status": "success",
        "db_id": db_id,
        "seller_successful_deals": successful_deals,
        "seller_rating": rating_str,
        "seller_type": final_seller_type,
        "seller_risk": seller_risk,
    }


async def run_seller_analysis_async(ads_to_check: list[tuple]) -> list[dict]:
    semaphore = asyncio.Semaphore(CONCURRENT_REQUESTS)

    async with AsyncSession(headers=HEADERS, impersonate="chrome124") as session:
        tasks = [
            process_single_seller_worker(session, ad_data, semaphore)
            for ad_data in ads_to_check
        ]
        results = await asyncio.gather(*tasks)

    return results


def run_seller_analysis() -> list[int]:
    global PROCESSED_COUNT
    PROCESSED_COUNT = 0

    print("\n" + "=" * 60)
    print("🕵️‍♂️ ЗАПУСК АНАЛІЗУ ПРОДАВЦІВ (УГОДИ ТА РЕЙТИНГ)")
    print("=" * 60)

    try:
        response = supabase.table("ads") \
            .select("id, seller_id, seller_uuid, seller_created_at, seller_type") \
            .not_.is_("seller_id", "null") \
            .neq("seller_id", "failed") \
            .eq("status", "active") \
            .eq("seller_checked", 0) \
            .execute()
        
        raw_ads = response.data or []
    except Exception as e:
        print(f"❌ [SUPABASE ERROR]: {e}")
        return []

    if not raw_ads:
        print("[ANALYZER] Усі нові продавці вже перевірені (seller_checked = 1).")
        return []

    ads_to_check = [
        (
            ad["id"], 
            ad.get("seller_id"), 
            ad.get("seller_uuid"), 
            ad.get("seller_created_at"), 
            ad.get("seller_type")
        )
        for ad in raw_ads
    ]

    print(f"[ANALYZER] Знайдено {len(ads_to_check)} неперевірених продавців. Аналізуємо...")
    start_time = time.time()

    results = asyncio.run(run_seller_analysis_async(ads_to_check))

    success_ids = []
    
    # 🔥 ГРУПУВАННЯ ДЛЯ ПАКЕТНОГО ОНОВЛЕННЯ БЕЗ СОКЕТНИХ ПОМИЛОК
    grouped_updates = defaultdict(list)

    for res in results:
        if not res or res.get("status") != "success":
            continue

        db_id = res["db_id"]
        # Складаємо ключ із характеристик
        key = (
            res["seller_successful_deals"],
            res["seller_rating"],
            res["seller_type"],
            res["seller_risk"]
        )
        grouped_updates[key].append(db_id)
        success_ids.append(db_id)

    print("\n💾 Оновлення даних про продавців у хмарі Supabase...")
    if grouped_updates:
        try:
            total_updated = 0
            for (deals, rating, s_type, risk), ids in grouped_updates.items():
                payload = {
                    "seller_successful_deals": deals,
                    "seller_rating": rating,
                    "seller_type": s_type,
                    "seller_risk_score": risk,
                    "seller_checked": 1
                }
                
                # Оновлюємо пачками по 100 елементів за 1 мережевий запит
                chunk_size = 100
                for i in range(0, len(ids), chunk_size):
                    batch = ids[i : i + chunk_size]
                    supabase.table("ads").update(payload).in_("id", batch).execute()
                    total_updated += len(batch)

            print(f"✅ [УСПІХ] Пакетно оновлено та позначено seller_checked=1 для {total_updated} продавців!")
        except Exception as e:
            print(f"❌ [ПОМИЛКА ЗБЕРЕЖЕННЯ В SUPABASE]: {e}")

    elapsed = time.time() - start_time
    print(f"\n[УСПІХ] Аналіз продавців завершено за {elapsed:.2f} сек!")
    print(f"Оновлено записів: {len(success_ids)}")
    return success_ids


if __name__ == "__main__":
    run_seller_analysis()
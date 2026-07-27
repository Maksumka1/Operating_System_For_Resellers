import os
import asyncio
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

from curl_cffi.requests import AsyncSession
from supabase import create_client, Client

PROJECT_ROOT = Path(__file__).resolve().parent
if not (PROJECT_ROOT / "config.py").exists():
    PROJECT_ROOT = PROJECT_ROOT.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

SUPABASE_URL = os.getenv("SUPABASE_URL", "https://nfhtmfhckctuyhfolhou.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_SECRET_KEY") or os.getenv("SUPABASE_PUBLISHABLE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY or "")

CONCURRENT_REQUESTS = 5
PROCESSED_COUNT = 0
COUNT_LOCK = asyncio.Lock()
TIMEOUT = 8

# 🎯 Повний набір необхідних заголовків для запитів до microservices OLX
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
    """Отримує кількість успішних угод OLX Доставки (числовий seller_id)."""
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
    """Отримує рейтинг та кількість оцінок (UUID seller_uuid)."""
    if not seller_uuid or str(seller_uuid).strip() in ("", "failed", "None"):
        return "немає оцінок"

    # Виправлено: видалено зайвий слеш на кінці URL
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

        # Одночасний виклик обох ендпоінтів для прискорення
        successful_deals, rating_str = await asyncio.gather(
            fetch_delivery_deals(session, seller_id),
            fetch_seller_rating(session, seller_uuid),
        )

    # 🎯 РОЗРАХУНОК ЗІРОК
    seller_stars = 0.0
    if rating_str and rating_str != "немає оцінок":
        try:
            match = re.match(r"([0-9.]+)/5\.0", rating_str)
            if match:
                seller_stars = float(match.group(1))
        except Exception:
            pass

    # 🎯 РОЗРАХУНОК ВІКУ АКАУНТУ
    today_year = datetime.now(timezone.utc).year
    acc_age_years = 0

    if seller_created_at:
        match = re.search(r"\b(19|20)\d{2}\b", str(seller_created_at))
        if match:
            reg_year = int(match.group(0))
            acc_age_years = max(0, today_year - reg_year)

    # 🎯 СКОРИНГ РИЗИКУ
    is_low_deals = successful_deals < 10
    is_bad_rating = 0.0 < seller_stars < 4.0
    is_new_account = acc_age_years <= 1

    if is_low_deals or is_bad_rating or is_new_account:
        seller_risk = "suspicious"
    elif acc_age_years >= 2 or successful_deals >= 30:
        seller_risk = "safe"
    else:
        seller_risk = "neutral"

    # 🎯 КЛАСИФІКАЦІЯ ПРОДАВЦЯ
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

    # 1. Завантажуємо з Supabase оголошення з неперевіреними продавцями
    try:
        response = supabase.table("ads") \
            .select("id, seller_id, seller_uuid, seller_created_at, seller_type") \
            .not_.is_("seller_id", "null") \
            .neq("seller_id", "failed") \
            .eq("status", "active") \
            .or_("seller_successful_deals.is.null,seller_rating.is.null") \
            .execute()
        
        raw_ads = response.data or []
    except Exception as e:
        print(f"❌ [SUPABASE ERROR]: {e}")
        return []

    if not raw_ads:
        print("[ANALYZER] Усі активні продавці вже проаналізовані.")
        return []

    # Перетворюємо дикти з Supabase у кортежі, які чекає асинхронний воркер
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

    print(f"[ANALYZER] Знайдено {len(ads_to_check)} продавців для перевірки. Аналізуємо...")
    start_time = time.time()

    # Запускаємо асинхронні запити
    results = asyncio.run(run_seller_analysis_async(ads_to_check))

    # 2. Формуємо масив результатів для пакетного upsert у Supabase
    updates_pool = []
    success_ids = []

    for res in results:
        if not res or res.get("status") != "success":
            continue

        db_id = res["db_id"]
        updates_pool.append({
            "id": db_id,
            "seller_successful_deals": res["seller_successful_deals"],
            "seller_rating": res["seller_rating"],
            "seller_type": res["seller_type"],
            "seller_risk_score": res["seller_risk"],
        })
        success_ids.append(db_id)

    print("\n💾 Оновлення даних про продавців у хмарі Supabase...")
    if updates_pool:
        try:
            supabase.table("ads").upsert(updates_pool, on_conflict="id").execute()
            print(f"✅ [УСПІХ] Оновлено інформацію для {len(updates_pool)} продавців!")
        except Exception as e:
            print(f"❌ [ПОМИЛКА ЗБЕРЕЖЕННЯ В SUPABASE]: {e}")

    elapsed = time.time() - start_time
    print(f"\n[УСПІХ] Аналіз продавців завершено за {elapsed:.2f} сек!")
    print(f"Оновлено записів: {len(success_ids)}")
    return success_ids


if __name__ == "__main__":
    run_seller_analysis()
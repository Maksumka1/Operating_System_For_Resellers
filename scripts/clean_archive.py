import os
import asyncio
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

BATCH_SIZE = 50        # OLX приймає по 50 ID в один GraphQL-запит
CONCURRENT_BATCHES = 5  # 5 паралельних пакунків одночасно
TIMEOUT = 10

HEADERS = {
    "accept": "*/*",
    "accept-language": "uk-UA,uk;q=0.9,en-US;q=0.8,en;q=0.7",
    "content-type": "application/json",
    "origin": "https://www.olx.ua",
    "referer": "https://www.olx.ua/",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
}

# Легкий GraphQL запит
BATCH_CHECK_QUERY = """query GetListingsByIds($ids: [Int!]!) {
  clientCompatibleListings(searchParameters: [{key: "id", value: $ids}]) {
    ... on ListingSuccess {
      data {
        id
        status
      }
    }
  }
}"""


async def process_batch(
    session: AsyncSession,
    batch: list[tuple[int, int]],  # [(db_id, ad_id), ...]
    semaphore: asyncio.Semaphore,
) -> list[tuple[int, str]]:
    results = []
    # Карта: olx_ad_id -> sqlite_db_id
    id_map = {ad_id: db_id for db_id, ad_id in batch if ad_id is not None}
    olx_ids = list(id_map.keys())

    if not olx_ids:
        for db_id, _ in batch:
            results.append((db_id, "active"))
        return results

    json_payload = {
        "query": BATCH_CHECK_QUERY,
        "variables": {"ids": olx_ids},
    }

    async with semaphore:
        try:
            resp = await session.post(
                "https://www.olx.ua/apigateway/graphql",
                json=json_payload,
                timeout=TIMEOUT,
            )

            if resp.status_code == 200:
                data = resp.json()
                listings = (
                    data.get("data", {})
                    .get("clientCompatibleListings", {})
                    .get("data", [])
                )

                # ЗАХИСТ ВІД СБОЮ API: Якщо відповідь порожня при HTTP 200, не маркуємо як видалені
                if not listings and len(olx_ids) > 0:
                    for db_id, _ in batch:
                        results.append((db_id, "active"))
                    return results

                found_olx_ids = set()
                for item in listings:
                    real_id = int(item.get("id", 0))
                    status = item.get("status", "active")

                    if real_id in id_map:
                        found_olx_ids.add(real_id)
                        target_db_id = id_map[real_id]
                        
                        if status != "active":
                            results.append((target_db_id, "deactivated"))
                        else:
                            results.append((target_db_id, "active"))

                # Усі ID, які OLX ВЗАГАЛІ НЕ ПОВЕРНУВ — видалені з майданчика!
                for ad_id, db_id in id_map.items():
                    if ad_id not in found_olx_ids:
                        results.append((db_id, "deactivated"))

            else:
                for db_id, _ in batch:
                    results.append((db_id, "active"))

        except Exception:
            for db_id, _ in batch:
                results.append((db_id, "active"))

    return results


async def run_fast_verifier(active_ads: list[tuple[int, int]]) -> list[tuple[int, str]]:
    # Розбиваємо список (db_id, ad_id) на батчі по 50 шт
    batches = [
        active_ads[i : i + BATCH_SIZE]
        for i in range(0, len(active_ads), BATCH_SIZE)
    ]

    semaphore = asyncio.Semaphore(CONCURRENT_BATCHES)

    async with AsyncSession(headers=HEADERS, impersonate="chrome120") as session:
        print("🔥 Прогріваємо сесію...")
        try:
            await session.get("https://www.olx.ua/", timeout=10)
            await asyncio.sleep(0.5)
        except Exception:
            pass

        tasks = [process_batch(session, b, semaphore) for b in batches]
        nested_results = await asyncio.gather(*tasks)

    flat_results = [item for sublist in nested_results for item in sublist]
    return flat_results


def main() -> None:
    print("⚡ СТАРТ УЛЬТРА-ШВИДКОЇ ПАКЕТНОЇ ПЕРЕВІРКИ СТАТУСІВ")

    # 1. Завантажуємо активні ad_id та id прямо з Supabase
    try:
        response = supabase.table("ads") \
            .select("id, ad_id") \
            .eq("status", "active") \
            .not_.is_("ad_id", "null") \
            .execute()
        raw_ads = response.data or []
    except Exception as e:
        print(f"❌ [SUPABASE ERROR]: {e}")
        return

    if not raw_ads:
        print("[INFO] Немає активних оголошень з ad_id для перевірки.")
        return

    # Перетворюємо у кортежі (db_id, ad_id), які чекає асинхронний воркер
    active_ads = [(ad["id"], ad["ad_id"]) for ad in raw_ads]

    print(f"[VERIFIER] Завантажено {len(active_ads)} лотів із Supabase.")
    start_time = time.time()

    # 2. Запускаємо перевірку через GraphQL API OLX
    results = asyncio.run(run_fast_verifier(active_ads))

    now_str = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M")
    
    deactivated_pool = [
        {
            "id": db_id,
            "status": "deactivated",
            "deactivated_at": now_str
        }
        for db_id, status in results
        if status == "deactivated"
    ]

    # 3. Маркуємо закриті лоти у хмарі через upsert
    if deactivated_pool:
        try:
            supabase.table("ads").upsert(deactivated_pool, on_conflict="id").execute()
            print(f"[УСПІХ SUPABASE] Знайдено та деактивовано: {len(deactivated_pool)} шт.")
        except Exception as e:
            print(f"❌ [ПОМИЛКА ЗБЕРЕЖЕННЯ СТАТУСІВ В SUPABASE]: {e}")
    else:
        print("[INFO] Усі оголошення досі активні.")

    elapsed = time.time() - start_time
    print(f"--- 🚀 {len(active_ads)} оголошень перевірено за {elapsed:.2f} сек ---")


if __name__ == "__main__":
    main()


if __name__ == "__main__":
    main()
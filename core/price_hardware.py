import os
import sys
import asyncio
from datetime import datetime, timezone
from pathlib import Path
from dotenv import load_dotenv
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


def calculate_percentile_price(ads_list: list[dict]) -> tuple[int, list[int]]:
    if not ads_list:
        return 0, []

    sorted_ads = sorted(ads_list, key=lambda x: x["price"])
    n = len(sorted_ads)

    if n < 3:
        return 0, []

    if n < 6:
        mid = n // 2
        selected_price = sorted_ads[mid]["price"]
        used_ids = [ad["ad_id"] for ad in sorted_ads]
        return selected_price, used_ids

    trim_size = int(n * 0.1)
    if trim_size > 0:
        trimmed_ads = sorted_ads[trim_size : n - trim_size]
    else:
        trimmed_ads = sorted_ads

    n_trimmed = len(trimmed_ads)
    index = int(n_trimmed * 0.33)
    index = min(index, n_trimmed - 1)

    selected_price = trimmed_ads[index]["price"]
    used_ids = [ad["ad_id"] for ad in trimmed_ads]

    return selected_price, used_ids


async def main_async(db_lock: asyncio.Lock | None = None) -> None:
    """Головний асинхронний метод розрахунку прайсів для оркестратора."""
    today_sql = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    print(f"--- ПОЧАТОК АНАЛІЗУ ЦІН КОМПЛЕКТУЮЧИХ ZA {today_sql} ---")

    def _fetch_active_ads():
        try:
            response = (
                supabase.table("ads")
                .select("ad_id, component_name, price")
                .in_("item_type", ["gpu", "cpu", "motherboard", "psu", "storage", "ram", "bundle"])
                .eq("status", "active")
                .eq("has_defects", 0)
                .gt("price", 100)
                .not_.is_("component_name", "null")
                .neq("seller_risk_score", "suspicious")
                .execute()
            )
            return response.data or []
        except Exception as e:
            print(f"❌ [SUPABASE ERROR]: {e}")
            return []

    all_ads = await asyncio.to_thread(_fetch_active_ads)

    if not all_ads:
        print("[INFO] Немає достатніх даних для розрахунку ринкових цін.")
        return

    ads_by_component: dict[str, list[dict]] = {}
    for ad in all_ads:
        comp_name = ad.get("component_name")
        if comp_name:
            ads_by_component.setdefault(comp_name, []).append(ad)

    records_to_upsert = []

    for target_name, ads_list in ads_by_component.items():
        real_price, competitor_ids = calculate_percentile_price(ads_list)
        
        if real_price > 0:
            records_to_upsert.append({
                "component_name": target_name,
                "price": real_price,
                "date": today_sql,
                "competitor_ids": competitor_ids
            })
            print(f"  [RESULT] -> {target_name}: {real_price} UAH (вибірка: {len(competitor_ids)} лотів)")
        else:
            print(f"  [SKIP] -> {target_name}: недостатньо оголошень для оцінки ({len(ads_list)} шт)")

    if records_to_upsert:
        def _upsert_prices():
            supabase.table("component_prices").upsert(
                records_to_upsert, 
                on_conflict="component_name,date"
            ).execute()

        try:
            if db_lock:
                async with db_lock:
                    await asyncio.to_thread(_upsert_prices)
            else:
                await asyncio.to_thread(_upsert_prices)

            print(f"\n✅ [УСПІХ] Оновлено ціни та competitor_ids для {len(records_to_upsert)} моделей!")
        except Exception as e:
            print(f"\n❌ [ПОМИЛКА ЗБЕРЕЖЕННЯ ЦІН В SUPABASE]: {e}")
    else:
        print("[INFO] Немає достатніх даних для розрахунку ринкових цін.")


def main() -> None:
    """Точка входу для ручного запуску з консолі."""
    asyncio.run(main_async())


if __name__ == "__main__":
    main()
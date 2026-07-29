import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from dotenv import load_dotenv
from supabase import create_client, Client

PROJECT_ROOT = Path(__file__).resolve().parent
if not (PROJECT_ROOT / "config.py").exists():
    PROJECT_ROOT = PROJECT_ROOT.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from config import HARDWARE_TARGETS
load_dotenv(PROJECT_ROOT / ".env")
SUPABASE_URL = os.getenv("SUPABASE_URL", "https://nfhtmfhckctuyhfolhou.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_SECRET_KEY") or os.getenv("SUPABASE_PUBLISHABLE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY or "")

hardware_items = {k: v for k, v in HARDWARE_TARGETS.items() if not k.startswith("pc_")}


def calculate_percentile_price(prices: list[int]) -> int:
    if not prices:
        return 0

    sorted_prices = sorted(prices)
    n = len(sorted_prices)

    # 1. Якщо менше 3 оголошень — вибірка нерелевантна для ринкової оцінки
    if n < 3:
        return 0

    # 2. Для малих вибірок (3-5 шт) беремо медіану, щоб не схопити найнижчий аномальний скам
    if n < 6:
        mid = n // 2
        return sorted_prices[mid]

    # 3. Для великих вибірок (>= 6) відсікаємо 10% аномалій з країв і беремо 33-й перцентиль
    trim_size = int(n * 0.1)
    if trim_size > 0:
        sorted_prices = sorted_prices[trim_size : n - trim_size]
        n = len(sorted_prices)

    index = int(n * 0.33)
    index = min(index, n - 1)

    return sorted_prices[index]


def main() -> None:
    today_sql = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    print(f"--- ПОЧАТОК АНАЛІЗУ ЦІН КОМПЛЕКТУЮЧИХ ЗА {today_sql} ---")

    try:
        response = supabase.table("ads") \
            .select("component_name, price") \
            .in_("item_type", ["gpu", "cpu", "motherboard", "psu", "storage"]) \
            .eq("status", "active") \
            .eq("has_defects", 0) \
            .gt("price", 100) \
            .not_.is_("component_name", "null") \
            .neq("seller_risk_score", "suspicious") \
            .execute()
        all_ads = response.data or []
    except Exception as e:
        print(f"❌ [SUPABASE ERROR]: {e}")
        return

    prices_by_component: dict[str, list[int]] = {}
    for ad in all_ads:
        comp_name = ad["component_name"]
        if comp_name in hardware_items:
            prices_by_component.setdefault(comp_name, []).append(ad["price"])

    records_to_upsert = []

    for target_name, prices_list in prices_by_component.items():
        real_price = calculate_percentile_price(prices_list)
        
        # Записуємо тільки якщо вибірка була достатньою (> 0)
        if real_price > 0:
            records_to_upsert.append({
                "component_name": target_name,
                "price": real_price,
                "date": today_sql
            })
            print(f"  [RESULT] -> {target_name}: {real_price} UAH (вибірка: {len(prices_list)} оголошень)")
        else:
            print(f"  [SKIP] -> {target_name}: недостатньо оголошень для оцінки ({len(prices_list)} шт)")

    if records_to_upsert:
        try:
            supabase.table("component_prices").upsert(
                records_to_upsert, 
                on_conflict="component_name,date"
            ).execute()
            print(f"\n✅ [УСПІХ] Розраховано та збережено в хмару ринкові ціни для {len(records_to_upsert)} моделей!")
        except Exception as e:
            print(f"\n❌ [ПОМИЛКА ЗБЕРЕЖЕННЯ ЦІН В SUPABASE]: {e}")
    else:
        print("[INFO] Немає достатніх даних для розрахунку ринкових цін.")


if __name__ == "__main__":
    main()
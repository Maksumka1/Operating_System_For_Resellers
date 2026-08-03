import os
import sys
from pathlib import Path
from collections import defaultdict
from dotenv import load_dotenv
from supabase import create_client, Client

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

load_dotenv(PROJECT_ROOT / ".env")

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SECRET_KEY") or os.getenv("SUPABASE_PUBLISHABLE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY or "")


def calculate_deal_metrics(seller_price: int, fair_price: int) -> tuple[int, float, str]:
    """Розраховує економію в UAH, відсоток вигоди та статус угоди для комплектуючих."""
    safe_seller_price = max(int(seller_price), 1)
    safe_fair_price = max(int(fair_price), 1)

    saving = safe_fair_price - safe_seller_price
    saving_percent = (saving / safe_fair_price) * 100.0

    if saving_percent < -100:
        saving_percent = -100.0
    elif saving_percent > 100:
        saving_percent = 100.0

    if saving_percent >= 20:
        deal_status = "🔥 SUPER DEAL"
    elif saving_percent >= 10:
        deal_status = "⭐ GOOD DEAL"
    elif saving_percent <= -5:
        deal_status = "❌ OVERPRICED"
    else:
        deal_status = "regular"

    return saving, round(saving_percent, 1), deal_status


def evaluate_hardware_ads() -> list[int]:
    """Оцінює вигідність окремих комплектуючих за останніми цінами з component_prices."""
    updated_ad_ids = set()

    # 1. Завантажуємо найсвіжіші орієнтири цін із component_prices
    component_fair_prices = {}
    try:
        res = (
            supabase.table("component_prices")
            .select("component_name, price")
            .order("date", desc=True)
            .execute()
        )
        if res.data:
            for row in res.data:
                comp_name = row.get("component_name")
                if comp_name and comp_name not in component_fair_prices:
                    component_fair_prices[comp_name] = row["price"]
    except Exception as e:
        print(f" [HARDWARE EVALUATOR] Помилка завантаження component_prices: {e}")

    if not component_fair_prices:
        print(" [HARDWARE EVALUATOR] База component_prices порожня. Спочатку запусти price_hardware.py.")
        return []

    # 2. Витягуємо ВСІ активні комплектуючі (разом із поточними оцінками для порівняння)
    all_hardware_ads = []
    page_size = 1000
    start = 0

    try:
        while True:
            response = (
                supabase.table("ads")
                .select("ad_id, component_name, price, estimated_fair_price, deal_status")
                .in_("item_type", ["gpu", "cpu", "motherboard", "psu", "storage", "ram", "bundle"])
                .eq("status", "active")
                .gt("price", 100)
                .not_.is_("component_name", "null")
                .range(start, start + page_size - 1)
                .execute()
            )
            batch = response.data or []
            all_hardware_ads.extend(batch)

            if len(batch) < page_size:
                break
            start += page_size

    except Exception as e:
        print(f" [SUPABASE ERROR]: {e}")
        return []

    if not all_hardware_ads:
        print("[HARDWARE EVALUATOR] Немає активних комплектуючих для оцінки.")
        return []

    print(f" [HARDWARE EVALUATOR] Аналізуємо {len(all_hardware_ads)} лотів заліза...")

    updates_by_payload = defaultdict(list)

    for ad in all_hardware_ads:
        ad_id = ad.get("ad_id")
        comp_name = ad.get("component_name")
        seller_price = ad.get("price", 0)

        if not ad_id or not comp_name:
            continue

        fair_price = component_fair_prices.get(comp_name)
        if not fair_price or fair_price <= 0:
            continue

        saving, saving_percent, deal_status = calculate_deal_metrics(seller_price, fair_price)
        
        curr_fair_p = ad.get("estimated_fair_price")
        curr_status = ad.get("deal_status")

        #  Оптимізація: Оновлюємо ТІЛЬКИ ТІ лоти, де оцінка реально ЗМІНИЛАСЯ або її ще не було
        if curr_fair_p == int(fair_price) and curr_status == deal_status:
            continue

        payload_key = (
            int(fair_price),
            int(round(saving)),
            int(round(saving_percent)),
            deal_status
        )

        updates_by_payload[payload_key].append(ad_id)
        updated_ad_ids.add(ad_id)

    # 3. Пакетне оновлення таблиці ads у Supabase по ad_id
    if updates_by_payload:
        print(f" [HARDWARE EVALUATOR] Записуємо зміни для {len(updated_ad_ids)} лотів у Supabase...")
        try:
            for (fair_p, sav_uah, sav_pct, d_status), ad_ids in updates_by_payload.items():
                update_data = {
                    "estimated_fair_price": fair_p,
                    "saving_uah": sav_uah,
                    "saving_percent": sav_pct,
                    "deal_status": d_status
                }
                chunk_size = 100
                for i in range(0, len(ad_ids), chunk_size):
                    batch = ad_ids[i : i + chunk_size]
                    supabase.table("ads").update(update_data).in_("ad_id", batch).execute()

            print(f" [HARDWARE EVALUATOR] Успішно оцінено та оновлено {len(updated_ad_ids)} лотів комплектуючих!")
        except Exception as e:
            print(f" [ПОМИЛКА ЗБЕРЕЖЕННЯ ОЦІНКИ ЗАЛІЗА]: {e}")
    else:
        print("ℹ [HARDWARE EVALUATOR] Усі комплектуючі вже мають актуальні ціни та статуси.")

    return list(updated_ad_ids)


def main() -> list[int]:
    print("\n" + "=" * 50)
    print(" ЗАПУСК ОЦІНКИ ВИГОДИ КОМПЛЕКТУЮЧИХ (HARDWARE EVALUATOR)")
    print("=" * 50)

    updated_ids = evaluate_hardware_ads()
    return updated_ids


if __name__ == "__main__":
    main()
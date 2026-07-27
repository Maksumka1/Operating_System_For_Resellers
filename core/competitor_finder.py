import os
import sys
from pathlib import Path
from collections import defaultdict
from supabase import create_client, Client

PROJECT_ROOT = Path(__file__).resolve().parent
if not (PROJECT_ROOT / "config.py").exists():
    PROJECT_ROOT = PROJECT_ROOT.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

SUPABASE_URL = os.getenv("SUPABASE_URL", "https://nfhtmfhckctuyhfolhou.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_SECRET_KEY") or os.getenv("SUPABASE_PUBLISHABLE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY or "")



def calculate_real_market_price(prices: list[int]) -> int:
    """Вираховує справедливу ринкову ціну на основі медіани після відсікання аномалій."""
    valid_prices = [p for p in prices if p > 100]
    if not valid_prices:
        return 0

    sorted_p = sorted(valid_prices)
    n = len(sorted_p)

    # Відсікаємо 10% найдешевших і 10% найдорожчих (аномалії/скам)
    if n >= 6:
        trim = int(n * 0.1)
        sorted_p = sorted_p[trim : n - trim]

    mid = len(sorted_p) // 2
    if len(sorted_p) % 2 == 0:
        return int((sorted_p[mid - 1] + sorted_p[mid]) / 2)
    return int(sorted_p[mid])


def calculate_deal_metrics(seller_price: int, fair_price: int) -> tuple[int, float, str]:
    """Універсальний розрахунок вигоди для комплектуючих без нулів і зсувів."""
    safe_seller_price = max(int(seller_price), 1)
    safe_fair_price = max(int(fair_price), 1)

    saving = safe_fair_price - safe_seller_price
    saving_percent = (saving / safe_fair_price) * 100.0

    # Обмеження відсоткових аномалій для чистоти інтерфейсу
    if saving_percent < -100:
        saving_percent = -100.0
    elif saving_percent > 100:
        saving_percent = 100.0

    if saving_percent >= 20:
        deal_status = "🔥 SUPER DEAL"
    elif saving_percent >= 10:
        deal_status = "⭐ GOOD DEAL"
    elif saving_percent <= -15:
        deal_status = "❌ OVERPRICED"
    else:
        deal_status = "regular"

    return saving, round(saving_percent, 1), deal_status


def update_hardware_competitor_prices() -> None:
    # 1. Завантажуємо орієнтири цін із component_prices у Supabase
    component_fair_prices = {}
    try:
        res = supabase.table("component_prices").select("component_name, price").order("date", desc=True).execute()
        if res.data:
            component_fair_prices = {row["component_name"]: row["price"] for row in res.data}
    except Exception as e:
        print(f"[COMPETITORS WARN] Помилка завантаження component_prices: {e}")

    # 2. Отримуємо всі активні комплектуючі
    try:
        response = supabase.table("ads") \
            .select("id, component_name, price") \
            .in_("item_type", ["gpu", "cpu", "motherboard", "psu", "storage"]) \
            .eq("status", "active") \
            .eq("has_defects", 0) \
            .gt("price", 100) \
            .not_.is_("component_name", "null") \
            .execute()
        rows = response.data or []
    except Exception as e:
        print(f"❌ [SUPABASE ERROR]: {e}")
        return

    if not rows:
        print("[COMPETITORS] Активних комплектуючих для аналізу не знайдено.")
        return

    comp_items = defaultdict(list)
    for row in rows:
        comp_items[row["component_name"]].append({"id": row["id"], "price": row["price"]})

    print(f"[COMPETITORS] Аналізуємо ринкові ціни та вигоду для {len(comp_items)} моделей заліза...")

    updates = []
    for comp_name, items in comp_items.items():
        all_prices = [it["price"] for it in items]
        market_price = calculate_real_market_price(all_prices)

        if market_price > 0:
            # Якщо є в таблиці component_prices — беремо звідти, якщо ні — беремо медіану ринку
            fair_price = component_fair_prices.get(comp_name, market_price)

            for item in items:
                ad_id = item["id"]
                seller_price = item["price"]

                saving, saving_percent, deal_status = calculate_deal_metrics(seller_price, fair_price)
                updates.append({"id": ad_id, "market_price": market_price, "fair_price": fair_price, "saving": saving, "saving_percent": saving_percent, "deal_status": deal_status})

    if updates:
        # Формуємо список об'єктів із первинним ключем (id)
        records_to_upsert = [
            {
                "id": item["id"],
                "competitor_price": item["market_price"],
                "estimated_fair_price": item["fair_price"],
                "saving_uah": item["saving"],
                "saving_percent": item["saving_percent"],
                "deal_status": item["deal_status"]
            }
            for item in updates
        ]

        # Один мережевий запит замість сотні циклів!
        supabase.table("ads").upsert(records_to_upsert, on_conflict="id").execute()

        print(f"✅ Комплектуючі оновлено! Розраховано ціни та вигоду для {len(updates)} оголошень.")


def update_pcs_competitor_prices() -> None:
    """Прораховує середню ціну конкурентів для всіх ПК зі схожою конфігурацією (CPU + GPU) (БЕЗ ЗМІН)."""
    try:
        response = supabase.table("ads") \
            .select("id, gpu_detected, cpu_detected, price") \
            .eq("item_type", "pc") \
            .eq("status", "active") \
            .eq("has_defects", 0) \
            .not_.is_("gpu_detected", "null") \
            .not_.is_("cpu_detected", "null") \
            .gt("price", 1000) \
            .execute()
        all_pcs = response.data or []
    except Exception as e:
        print(f"❌ [SUPABASE ERROR]: {e}")
        return

    if not all_pcs:
        print("[COMPETITORS] Активних ПК з розпізнаним залізом немає.")
        return

    build_items = defaultdict(list)
    for pc in all_pcs:
        gpu = pc.get("gpu_detected") or ""
        cpu = pc.get("cpu_detected") or ""
        if "unknown" in gpu.lower() or "unknown" in cpu.lower():
            continue
        build_key = f"{gpu.lower()}_{cpu.lower()}"
        build_items[build_key].append({"id": pc["id"], "price": pc["price"]})

    print(f"[COMPETITORS] Перераховуємо ціни конкурентів для {len(all_pcs)} ПК...")

    for build_key, items in build_items.items():
        for current_item in items:
            cur_id = current_item["id"]
            other_prices = [it["price"] for it in items if it["id"] != cur_id]

            avg_competitor_price = current_item["price"] if not other_prices else int(sum(other_prices) / len(other_prices))

            supabase.table("ads").update({"competitor_price": avg_competitor_price}).eq("id", cur_id).execute()

    print(f"✅ Комп'ютери оновлено! Розраховано ціни конкурентів.")


def main():
    print("\n" + "="*50)
    print("📊 ЗАПУСК АНАЛІЗУ КОНКУРЕНТНОГО СЕРЕДОВИЩА")
    print("="*50)

    update_hardware_competitor_prices()
    update_pcs_competitor_prices()

    print("[УСПІХ] Повний аналіз ринку конкурентів завершено успішно!")


if __name__ == "__main__":
    main()
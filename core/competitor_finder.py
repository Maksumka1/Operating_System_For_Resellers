import os
import sys
from pathlib import Path
from collections import defaultdict
from dotenv import load_dotenv
from supabase import create_client, Client
from concurrent.futures import ThreadPoolExecutor

PROJECT_ROOT = Path(__file__).resolve().parent
if not (PROJECT_ROOT / "config.py").exists():
    PROJECT_ROOT = PROJECT_ROOT.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
load_dotenv(PROJECT_ROOT / ".env")

SUPABASE_URL = os.getenv("SUPABASE_URL", "https://nfhtmfhckctuyhfolhou.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_SECRET_KEY") or os.getenv("SUPABASE_PUBLISHABLE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY or "")


def calculate_real_market_price(prices: list[int]) -> int:
    """Вираховує справедливу ринкову ціну на основі медіани після відсікання аномалій."""
    valid_prices = [p for p in prices if p > 100]
    
    if len(valid_prices) < 3:
        return 0

    sorted_p = sorted(valid_prices)
    n = len(sorted_p)

    if n >= 6:
        trim = int(n * 0.1)
        sorted_p = sorted_p[trim : n - trim]

    mid = len(sorted_p) // 2
    if len(sorted_p) % 2 == 0:
        return int((sorted_p[mid - 1] + sorted_p[mid]) / 2)
    return int(sorted_p[mid])


def calculate_deal_metrics(seller_price: int, fair_price: int) -> tuple[int, float, str]:
    """Універсальний розрахунок вигоди для комплектуючих."""
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
    elif saving_percent <= -15:
        deal_status = "❌ OVERPRICED"
    else:
        deal_status = "regular"

    return saving, round(saving_percent, 1), deal_status


def _safe_update_ad(item: dict) -> bool:
    """Безпечне оновлення одного запису з ізоляцією сокет-помилок."""
    try:
        ad_id = item.pop("id")
        supabase.table("ads").update(item).eq("id", ad_id).execute()
        return True
    except Exception:
        return False


def update_hardware_competitor_prices() -> set[int]:
    updated_ids = set()

    # 1. Завантажуємо орієнтири цін із component_prices
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
            .neq("seller_risk_score", "suspicious") \
            .execute()
        rows = response.data or []
    except Exception as e:
        print(f"❌ [SUPABASE ERROR]: {e}")
        return updated_ids

    if not rows:
        print("[COMPETITORS] Активних комплектуючих для аналізу не знайдено.")
        return updated_ids

    comp_items = defaultdict(list)
    for row in rows:
        comp_items[row["component_name"]].append({"id": row["id"], "price": row["price"]})

    print(f"[COMPETITORS] Аналізуємо ринкові ціни та вигоду для {len(comp_items)} моделей заліза...")

    updates = []
    for comp_name, items in comp_items.items():
        all_prices = [it["price"] for it in items]
        market_price = calculate_real_market_price(all_prices)

        fair_price = component_fair_prices.get(comp_name) or market_price

        if fair_price > 0:
            for item in items:
                ad_id = item["id"]
                seller_price = item["price"]

                saving, saving_percent, deal_status = calculate_deal_metrics(seller_price, fair_price)
                
                updates.append({
                    "id": ad_id,
                    "competitor_price": int(market_price if market_price > 0 else fair_price),
                    "estimated_fair_price": int(fair_price),
                    "saving_uah": int(round(saving)),
                    "saving_percent": int(round(saving_percent)),
                    "deal_status": deal_status
                })
                updated_ids.add(ad_id)

    if updates:
        try:
            with ThreadPoolExecutor(max_workers=4) as executor:
                list(executor.map(_safe_update_ad, updates))
            print(f"✅ Комплектуючі оновлено! Розраховано ціни для {len(updates)} оголошень.")
        except Exception as e:
            print(f"❌ [ПОМИЛКА ЗБЕРЕЖЕННЯ КОНКУРЕНТІВ ЗАЛІЗА]: {e}")

    return updated_ids


def update_pcs_competitor_prices() -> set[int]:
    """Прораховує середню ціну конкурентів для всіх ПК зі схожою конфігурацією (CPU + GPU)."""
    updated_ids = set()
    try:
        response = supabase.table("ads") \
            .select("id, gpu_detected, cpu_detected, price") \
            .eq("item_type", "pc") \
            .eq("status", "active") \
            .eq("has_defects", 0) \
            .not_.is_("gpu_detected", "null") \
            .not_.is_("cpu_detected", "null") \
            .neq("seller_risk_score", "suspicious") \
            .gt("price", 1000) \
            .execute()
        all_pcs = response.data or []
    except Exception as e:
        print(f"❌ [SUPABASE ERROR]: {e}")
        return updated_ids

    if not all_pcs:
        print("[COMPETITORS] Активних ПК з розпізнаним залізом немає.")
        return updated_ids

    build_items = defaultdict(list)
    for pc in all_pcs:
        gpu = pc.get("gpu_detected") or ""
        cpu = pc.get("cpu_detected") or ""
        if "unknown" in gpu.lower() or "unknown" in cpu.lower():
            continue
        build_key = f"{gpu.lower()}_{cpu.lower()}"
        build_items[build_key].append({"id": pc["id"], "price": pc["price"]})

    print(f"[COMPETITORS] Перераховуємо ціни конкурентів для {len(all_pcs)} ПК...")

    pc_updates = []
    for build_key, items in build_items.items():
        for current_item in items:
            cur_id = current_item["id"]
            other_prices = [it["price"] for it in items if it["id"] != cur_id]

            avg_competitor_price = current_item["price"] if not other_prices else int(sum(other_prices) / len(other_prices))

            pc_updates.append({
                "id": cur_id,
                "competitor_price": avg_competitor_price
            })
            updated_ids.add(cur_id)

    if pc_updates:
        try:
            with ThreadPoolExecutor(max_workers=4) as executor:
                list(executor.map(_safe_update_ad, pc_updates))
            print(f"✅ Комп'ютери оновлено! Розраховано ціни конкурентів для {len(pc_updates)} ПК.")
        except Exception as e:
            print(f"❌ [ПОМИЛКА ЗБЕРЕЖЕННЯ КОНКУРЕНТІВ ПК]: {e}")

    return updated_ids


def main() -> list[int]:
    print("\n" + "="*50)
    print("📊 ЗАПУСК АНАЛІЗУ КОНКУРЕНТНОГО СЕРЕДОВИЩА")
    print("="*50)

    hw_ids = update_hardware_competitor_prices()
    pc_ids = update_pcs_competitor_prices()

    all_updated_ids = list(hw_ids | pc_ids)

    print(f"[УСПІХ] Повний аналіз ринку конкурентів завершено! Змінено {len(all_updated_ids)} лотів.")
    return all_updated_ids


if __name__ == "__main__":
    main()
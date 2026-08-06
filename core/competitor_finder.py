import os
import sys
import asyncio
from pathlib import Path
from collections import defaultdict
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


async def update_pcs_competitor_prices_async(db_lock: asyncio.Lock | None = None) -> set[int]:
    updated_ids = set()

    def _fetch_pcs():
        try:
            response = (
                supabase.table("ads")
                .select("ad_id, gpu_detected, cpu_detected, price")
                .eq("item_type", "pc")
                .eq("status", "active")
                .eq("has_defects", 0)
                .not_.is_("gpu_detected", "null")
                .not_.is_("cpu_detected", "null")
                .neq("seller_risk_score", "suspicious")
                .gt("price", 1000)
                .execute()
            )
            return response.data or []
        except Exception as e:
            print(f"❌ [SUPABASE ERROR]: {e}")
            return []

    all_pcs = await asyncio.to_thread(_fetch_pcs)

    if not all_pcs:
        print("[COMPETITORS] Активних ПК з розпізнаним залізом немає.")
        return updated_ids

    build_items = defaultdict(list)
    for pc in all_pcs:
        gpu = pc.get("gpu_detected") or ""
        cpu = pc.get("cpu_detected") or ""
        ad_id = pc.get("ad_id")
        
        if not ad_id or "unknown" in gpu.lower() or "unknown" in cpu.lower():
            continue
            
        build_key = f"{gpu.lower()}_{cpu.lower()}"
        build_items[build_key].append({"ad_id": ad_id, "price": pc["price"]})

    print(f"[COMPETITORS] Перераховуємо ціни конкурентів для {len(all_pcs)} ПК...")

    grouped_updates = defaultdict(list)
    for build_key, items in build_items.items():
        for current_item in items:
            cur_ad_id = current_item["ad_id"]
            other_prices = [it["price"] for it in items if it["ad_id"] != cur_ad_id]

            avg_competitor_price = (
                current_item["price"]
                if not other_prices
                else int(sum(other_prices) / len(other_prices))
            )

            grouped_updates[avg_competitor_price].append(cur_ad_id)
            updated_ids.add(cur_ad_id)

    if grouped_updates:
        def _apply_updates():
            for price_val, ids in grouped_updates.items():
                chunk_size = 100
                for i in range(0, len(ids), chunk_size):
                    batch = ids[i : i + chunk_size]
                    supabase.table("ads").update({"competitor_price": price_val}).in_("ad_id", batch).execute()

        try:
            if db_lock:
                async with db_lock:
                    await asyncio.to_thread(_apply_updates)
            else:
                await asyncio.to_thread(_apply_updates)

            print(f"✅ Комп'ютери оновлено! Розраховано ціни конкурентів для {len(updated_ids)} ПК.")
        except Exception as e:
            print(f"❌ [ПОМИЛКА ЗБЕРЕЖЕННЯ КОНКУРЕНТІВ ПК]: {e}")

    return updated_ids


async def main_async(db_lock: asyncio.Lock | None = None) -> list[int]:
    """Головний асинхронний метод для оркестратора."""
    print("\n" + "=" * 50)
    print(" ЗАПУСК АНАЛІЗУ КОНКУРЕНТНОГО СЕРЕДОВИЩА (ТІЛЬКИ ПК)")
    print("=" * 50)

    pc_ids = await update_pcs_competitor_prices_async(db_lock=db_lock)
    all_updated_ids = list(pc_ids)

    print(f"[УСПІХ] Повний аналіз ринку конкурентів завершено! Змінено {len(all_updated_ids)} лотів.")
    return all_updated_ids


def main() -> list[int]:
    """Точка входу для ручного запуску з консолі."""
    return asyncio.run(main_async())


if __name__ == "__main__":
    main()
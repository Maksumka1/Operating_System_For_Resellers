import os
import re
import sys
import asyncio
from datetime import datetime, timezone
from pathlib import Path
from collections import defaultdict
from dotenv import load_dotenv
from supabase import create_client, Client

PROJECT_ROOT = Path(__file__).resolve().parent
if not (PROJECT_ROOT / "config.py").exists():
    PROJECT_ROOT = PROJECT_ROOT.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from config import HARDWARE_TARGETS
from hardware_matchers import (
    normalize_title,
    extract_gpu,
    extract_cpu,
    extract_motherboard,
    extract_ram,
    extract_storage,
    extract_psu,
)

load_dotenv(PROJECT_ROOT / ".env")
SUPABASE_URL = os.getenv("SUPABASE_URL", "https://nfhtmfhckctuyhfolhou.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_SECRET_KEY") or os.getenv("SUPABASE_PUBLISHABLE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY or "")


def load_latest_prices_sync() -> dict[str, int]:
    """Витягує актуальні середні ціни комплектуючих із Supabase."""
    clean_prices = {}

    try:
        res = (
            supabase.table("component_prices")
            .select("component_name, price")
            .order("date", desc=True)
            .execute()
        )
        if res.data:
            clean_prices = {row["component_name"]: row["price"] for row in res.data}
    except Exception as e:
        print(f"[EVALUATOR WARN] Помилка читання component_prices: {e}")

    if not clean_prices:
        try:
            res = (
                supabase.table("ads")
                .select("component_name, competitor_price")
                .in_("item_type", ["gpu", "cpu", "motherboard", "psu", "storage", "ram", "bundle"])
                .eq("status", "active")
                .gt("competitor_price", 0)
                .not_.is_("component_name", "null")
                .execute()
            )
            if res.data:
                clean_prices = {row["component_name"]: row["competitor_price"] for row in res.data}
        except Exception as e:
            print(f"[EVALUATOR ERR] Помилка резервного читання цін: {e}")

    return clean_prices


def evaluate_pc(ad_id: int, title: str, description: str, seller_price: int, component_prices: dict) -> dict:
    """Вираховує собівартість ПК на основі всіх розпізнаних комплектуючих."""
    full_text = f"{title} {description if description else ''}"
    full_text_clean = normalize_title(full_text)
    full_text_clean = re.split(r"додатков|опці|за доплат|доплати", full_text_clean)[0]

    gpu_candidates = [g for c in extract_gpu(full_text_clean) if (g := c) in HARDWARE_TARGETS]
    gpu = gpu_candidates[0] if gpu_candidates else None
    gpu_price = component_prices.get(gpu, 0) if gpu else 0
    gpu_display = gpu if gpu else "Unknown GPU"

    cpu_candidates = [c for c in extract_cpu(full_text_clean) if c in HARDWARE_TARGETS]
    cpu = cpu_candidates[0] if cpu_candidates else None
    cpu_price = component_prices.get(cpu, 0) if cpu else 0
    cpu_display = cpu if cpu else "Unknown CPU"

    mb_candidates = [m for m in extract_motherboard(full_text_clean) if m in HARDWARE_TARGETS]
    mb = mb_candidates[0] if mb_candidates else None
    mb_price = component_prices.get(mb, 0) if mb else 0

    ram_candidates = [r for r in extract_ram(full_text_clean) if r in HARDWARE_TARGETS]
    ram = ram_candidates[0] if ram_candidates else None
    ram_price = component_prices.get(ram, 0) if ram else 0

    st_candidates = [s for s in extract_storage(full_text_clean) if s in HARDWARE_TARGETS]
    storage = st_candidates[0] if st_candidates else None
    storage_price = component_prices.get(storage, 0) if storage else 0

    psu_candidates = [p for p in extract_psu(full_text_clean) if p in HARDWARE_TARGETS]
    psu = psu_candidates[0] if psu_candidates else None
    psu_price = component_prices.get(psu, 0) if psu else 0

    known_extra_price = mb_price + ram_price + storage_price + psu_price

    if known_extra_price > 0:
        base_case_cooler_cost = 1200
        fair_price = gpu_price + cpu_price + known_extra_price + base_case_cooler_cost
    else:
        base_pc_cost = 3800
        fair_price = gpu_price + cpu_price + base_pc_cost

    safe_seller_price = seller_price if seller_price > 0 else 1
    saving = fair_price - safe_seller_price
    saving_percent = (saving / fair_price) * 100 if fair_price > 0 else 0

    if saving_percent >= 20 or saving >= 2000:
        deal_status = "🔥 SUPER DEAL"
    elif saving_percent >= 8 or saving >= 800:
        deal_status = "⭐ GOOD DEAL"
    elif saving_percent <= -5:
        deal_status = "❌ OVERPRICED"
    else:
        deal_status = "regular"

    if cpu_display == "Unknown CPU":
        deal_status = "regular"
        saving = 0

    return {
        "ad_id": ad_id,
        "seller_price_clean": seller_price,
        "gpu_detected": gpu_display,
        "gpu_market_price": gpu_price,
        "cpu_detected": cpu_display,
        "cpu_market_price": cpu_price,
        "estimated_fair_price": int(fair_price),
        "saving_uah": int(round(saving)),
        "saving_percent": int(round(saving_percent, 1)),
        "deal_status": deal_status,
        "evaluated_at": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M")
    }


async def main_async(db_lock: asyncio.Lock | None = None) -> None:
    """Головна асинхронна точка входу для оцінки ПК."""
    today_sql = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    print(f"--- СТАРТ МОДУЛЯ ОЦІНКИ ПК ({today_sql}) ---")
    
    prices = await asyncio.to_thread(load_latest_prices_sync)
    if not prices: 
        print("[WARN] Прайс-лист комплектуючих порожній. Пропускаємо оцінку.")
        return

    def _fetch_unrated_pcs():
        try:
            response = (
                supabase.table("ads")
                .select("ad_id, title, description, price, url")
                .eq("item_type", "pc")
                .eq("status", "active")
                .or_("has_defects.eq.0,has_defects.is.null")
                .is_("estimated_fair_price", "null")
                .execute()
            )
            return response.data or []
        except Exception as e:
            print(f"❌ [SUPABASE ERROR]: {e}")
            return []

    unrated_pcs = await asyncio.to_thread(_fetch_unrated_pcs)

    if not unrated_pcs:
        print("[INFO] Немає нових чистих ПК для оцінки.")
        return

    print(f"[EVALUATOR] Знайдено {len(unrated_pcs)} комп'ютерів для розпізнавання та оцінки...")
    
    updates_grouped = defaultdict(list)
    count_evaluated = 0

    for pc in unrated_pcs:
        ad_id = pc["ad_id"]
        title = pc.get("title") or ""
        description = pc.get("description") or ""
        price = pc.get("price") or 0

        evaluation = evaluate_pc(ad_id, title, description, price, prices)
        
        # Групуємо за характеристиками payload для пакетного оновлення
        payload_key = (
            evaluation["seller_price_clean"],
            evaluation["gpu_detected"],
            evaluation["cpu_detected"],
            evaluation["gpu_market_price"],
            evaluation["cpu_market_price"],
            evaluation["estimated_fair_price"],
            evaluation["saving_uah"],
            evaluation["saving_percent"],
            evaluation["deal_status"],
            evaluation["evaluated_at"]
        )
        updates_grouped[payload_key].append(ad_id)
        count_evaluated += 1

    if updates_grouped:
        def _apply_grouped_updates():
            for payload_tuple, ids in updates_grouped.items():
                payload = {
                    "seller_price_clean": payload_tuple[0],
                    "gpu_detected": payload_tuple[1],
                    "cpu_detected": payload_tuple[2],
                    "gpu_market_price": payload_tuple[3],
                    "cpu_market_price": payload_tuple[4],
                    "estimated_fair_price": payload_tuple[5],
                    "saving_uah": payload_tuple[6],
                    "saving_percent": payload_tuple[7],
                    "deal_status": payload_tuple[8],
                    "evaluated_at": payload_tuple[9]
                }
                chunk_size = 100
                for i in range(0, len(ids), chunk_size):
                    batch = ids[i : i + chunk_size]
                    supabase.table("ads").update(payload).in_("ad_id", batch).execute()

        try:
            if db_lock:
                async with db_lock:
                    await asyncio.to_thread(_apply_grouped_updates)
            else:
                await asyncio.to_thread(_apply_grouped_updates)

            print(f"\n✅ [УСПІХ] Пакетно розпізнано та оцінено у хмарі: {count_evaluated} комп'ютерів.")
        except Exception as e:
            print(f"\n❌ [ПОМИЛКА ЗБЕРЕЖЕННЯ ОЦІНКИ В SUPABASE]: {e}")


def main() -> None:
    """Точка входу для ручного запуску з консолі."""
    asyncio.run(main_async())


if __name__ == "__main__":
    main()
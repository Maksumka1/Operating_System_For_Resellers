import os
import re
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


def load_latest_prices() -> dict[str, int]:
    """Витягує актуальні середні ціни комплектуючих із Supabase."""
    clean_prices = {}

    try:
        # 1. Спроба завантажити найсвіжіші ціни з component_prices
        res = supabase.table("component_prices") \
            .select("component_name, price") \
            .order("date", desc=True) \
            .execute()
        if res.data:
            clean_prices = {row["component_name"]: row["price"] for row in res.data}
    except Exception as e:
        print(f"[EVALUATOR WARN] Помилка читання component_prices: {e}")

    # 2. Якщо component_prices порожній — беремо резервні ціни з активних оголошень (включаючи ram та bundle)
    if not clean_prices:
        try:
            res = supabase.table("ads") \
                .select("component_name, competitor_price") \
                .in_("item_type", ["gpu", "cpu", "motherboard", "psu", "storage", "ram", "bundle"]) \
                .eq("status", "active") \
                .gt("competitor_price", 0) \
                .not_.is_("component_name", "null") \
                .execute()
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

    # 1. Детекція та оцінка відеокарти
    gpu_candidates = [g for c in extract_gpu(full_text_clean) if (g := c) in HARDWARE_TARGETS]
    gpu = gpu_candidates[0] if gpu_candidates else None
    gpu_price = component_prices.get(gpu, 0) if gpu else 0
    gpu_display = gpu if gpu else "Unknown GPU"

    # 2. Детекція та оцінка процесора
    cpu_candidates = [c for c in extract_cpu(full_text_clean) if c in HARDWARE_TARGETS]
    cpu = cpu_candidates[0] if cpu_candidates else None
    cpu_price = component_prices.get(cpu, 0) if cpu else 0
    cpu_display = cpu if cpu else "Unknown CPU"

    # 3. Додаткова детекція решти комплектуючих для точнішої собівартості
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

    # Оцінка суми знайдених додаткових комплектуючих
    known_extra_price = mb_price + ram_price + storage_price + psu_price

    if known_extra_price > 0:
        base_case_cooler_cost = 1200
        fair_price = gpu_price + cpu_price + known_extra_price + base_case_cooler_cost
    else:
        # Стандартна резервна вартість б/в платформи (Плата, ОЗП, SSD, Корпус, БЖ)
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
        "id": ad_id,
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


def main() -> None:
    today_sql = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    print(f"--- СТАРТ МОДУЛЯ ОЦІНКИ ПК ({today_sql}) ---")
    
    prices = load_latest_prices()
    if not prices: 
        print("[WARN] Прайс-лист комплектуючих порожній. Пропускаємо оцінку.")
        return

    # 1. Беремо з Supabase тільки АКТИВНІ, НЕУШКОДЖЕНІ та ЩЕ НЕ ОЦІНЕНІ ПК
    try:
        response = supabase.table("ads") \
            .select("id, title, description, price, url") \
            .eq("item_type", "pc") \
            .eq("status", "active") \
            .or_("has_defects.eq.0,has_defects.is.null") \
            .is_("estimated_fair_price", "null") \
            .execute()
        unrated_pcs = response.data or []
    except Exception as e:
        print(f"❌ [SUPABASE ERROR]: {e}")
        return

    if not unrated_pcs:
        print("[INFO] Немає нових чистих ПК для оцінки.")
        return

    print(f"[EVALUATOR] Знайдено {len(unrated_pcs)} комп'ютерів для розпізнавання та оцінки...")
    
    count_evaluated = 0
    updates_pool = []

    for pc in unrated_pcs:
        ad_id = pc["id"]
        title = pc.get("title") or ""
        description = pc.get("description") or ""
        price = pc.get("price") or 0

        evaluation = evaluate_pc(ad_id, title, description, price, prices)
            
        updates_pool.append({
            "id": evaluation["id"],
            "seller_price_clean": evaluation["seller_price_clean"],
            "gpu_detected": evaluation["gpu_detected"],
            "cpu_detected": evaluation["cpu_detected"],
            "gpu_market_price": evaluation["gpu_market_price"],
            "cpu_market_price": evaluation["cpu_market_price"],
            "estimated_fair_price": evaluation["estimated_fair_price"],
            "saving_uah": evaluation["saving_uah"],
            "saving_percent": evaluation["saving_percent"],
            "deal_status": evaluation["deal_status"],
            "evaluated_at": evaluation["evaluated_at"]
        })
        
        count_evaluated += 1

        if evaluation["saving_percent"] >= 10:
            print(f"\n[{evaluation['deal_status']}] {title[:60]}...")
            print(f"   Відеокарта: {evaluation['gpu_detected']} ({evaluation['gpu_market_price']} грн)")
            print(f"   Процесор:   {evaluation['cpu_detected']} ({evaluation['cpu_market_price']} грн)")
            print(f"   🔥 Вигода:  {evaluation['saving_uah']} грн ({evaluation['saving_percent']}%)")

    # 2. Оновлюємо розраховані значення у Supabase
    if updates_pool:
        try:
            for item in updates_pool:
                ad_id = item.pop("id")  # Витягуємо ID для умови .eq()
                supabase.table("ads").update(item).eq("id", ad_id).execute()

            print(f"\n✅ [УСПІХ] Успішно розпізнано та оцінено у хмарі: {count_evaluated} комп'ютерів.")
        except Exception as e:
            print(f"\n❌ [ПОМИЛКА ЗБЕРЕЖЕННЯ ОЦІНКИ В SUPABASE]: {e}")


if __name__ == "__main__":
    main()
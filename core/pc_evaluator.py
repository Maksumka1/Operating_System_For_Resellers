from __future__ import annotations

import sys
import sqlite3
import re
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
if not (PROJECT_ROOT / "config.py").exists():
    PROJECT_ROOT = PROJECT_ROOT.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from config import HARDWARE_TARGETS, DB_FILE


def get_db_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_FILE)
    conn.execute("PRAGMA journal_mode=WAL;")
    return conn


def load_latest_prices() -> dict[str, int]:
    """
    Витягує актуальні середні ціни комплектуючих з таблиці ads.
    Якщо є окрема таблиця component_prices, використовує її.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    clean_prices = {}

    # 1. Пробуємо завантажити з таблиці component_prices (якщо вона існує)
    try:
        cursor.execute("SELECT MAX(date) FROM component_prices")
        latest_date_row = cursor.fetchone()
        if latest_date_row and latest_date_row[0]:
            cursor.execute("""
                SELECT component_name, price 
                FROM component_prices 
                WHERE date = ?
            """, (latest_date_row[0],))
            clean_prices = {row[0]: row[1] for row in cursor.fetchall()}
    except sqlite3.OperationalError:
        pass

    # 2. Якщо component_prices порожня — беремо пораховані competitor_price з таблиці ads
    if not clean_prices:
        cursor.execute("""
            SELECT component_name, competitor_price 
            FROM ads 
            WHERE item_type IN ('gpu', 'cpu', 'motherboard', 'psu', 'storage') 
              AND status = 'active'
              AND competitor_price > 0
              AND component_name IS NOT NULL
            GROUP BY component_name
        """)
        clean_prices = {row[0]: row[1] for row in cursor.fetchall()}

    conn.close()
    return clean_prices


def detect_component_by_keywords(text_lower: str, target_keys: list[str]) -> str | None:
    """
    Шукає найдовший збіг ключового слова у тексті з використанням меж слів (word boundaries).
    """
    # Сортуємо ключі за довжиною назви для запобігання хибним збігам (наприклад, i5_10400f перед i5_10400)
    sorted_keys = sorted(target_keys, key=lambda k: len(k), reverse=True)
    
    for comp_key in sorted_keys:
        required_keywords = HARDWARE_TARGETS[comp_key].get("required_keywords", [])
        
        for keyword in required_keywords:
            kw_clean = keyword.lower().strip()
            if not kw_clean:
                continue
            
            # Використовуємо \b для точного збігу слова
            pattern = r"\b" + re.escape(kw_clean.replace("-", " ")) + r"\b"
            if re.search(pattern, text_lower.replace("-", " ")):
                return comp_key
                
    return None


def evaluate_pc(ad_id: int, title: str, description: str, seller_price: int, component_prices: dict) -> dict:
    title_clean = title.replace("-", " ")
    desc_clean = description.replace("-", " ") if description else ""
    
    full_text_lower = f"{title_clean} {desc_clean}".lower()

    # 🎯 Беремо список ключів суворо за item_type з config.py
    gpus_keys = [k for k, v in HARDWARE_TARGETS.items() if v.get("item_type") == "gpu"]
    cpus_keys = [k for k, v in HARDWARE_TARGETS.items() if v.get("item_type") == "cpu"]

    # 1. Детекція та оцінка відеокарти
    gpu = detect_component_by_keywords(full_text_lower, gpus_keys)
    if gpu:
        gpu_price = component_prices.get(gpu, 0)
        gpu_display = gpu
    else:
        gpu_display = "Unknown GPU"
        gpu_price = 0

    # 2. Детекція та оцінка процесора
    cpu = detect_component_by_keywords(full_text_lower, cpus_keys)
    if cpu:
        cpu_price = component_prices.get(cpu, 0)
        cpu_display = cpu
    else:
        cpu_display = "Unknown CPU"
        cpu_price = 0

    safe_seller_price = seller_price if seller_price > 0 else 1

    # Базова вартість платформи б/в (Плата, ОЗП, SSD, Корпус, БЖ)
    base_pc_cost = 3800 
    fair_price = gpu_price + cpu_price + base_pc_cost
    
    saving = fair_price - safe_seller_price
    saving_percent = (saving / fair_price) * 100 if fair_price > 0 else 0
    
    if saving_percent >= 20:
        deal_status = "🔥 SUPER DEAL"
    elif saving_percent >= 10:
        deal_status = "⭐ GOOD DEAL"
    elif saving_percent <= -15:
        deal_status = "❌ OVERPRICED"
    else:
        deal_status = "regular"

    return {
        "id": ad_id,
        "seller_price_clean": seller_price,
        "gpu_detected": gpu_display,
        "gpu_market_price": gpu_price,
        "cpu_detected": cpu_display,
        "cpu_market_price": cpu_price,
        "estimated_fair_price": fair_price,
        "saving_uah": saving,
        "saving_percent": round(saving_percent, 1),
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
        
    conn = get_db_connection()
    cursor = conn.cursor()

    # 🎯 Беремо тільки АКТИВНІ, НЕУШКОДЖЕНІ та ЩЕ НЕ ОЦІНЕНІ ПК
    cursor.execute("""
        SELECT id, title, description, price, url 
        FROM ads 
        WHERE item_type = 'pc' 
          AND status = 'active' 
          AND (has_defects = 0 OR has_defects IS NULL)
          AND estimated_fair_price IS NULL
    """)
    unrated_pcs = cursor.fetchall()

    if not unrated_pcs:
        print("[INFO] Немає нових чистих ПК для оцінки.")
        conn.close()
        return

    print(f"[EVALUATOR] Знайдено {len(unrated_pcs)} комп'ютерів для розпізнавання та оцінки...")
    
    count_evaluated = 0
    updates_pool = []

    for ad_id, title, description, price, url in unrated_pcs:
        evaluation = evaluate_pc(ad_id, title, description, price, prices)
            
        updates_pool.append((
            evaluation["seller_price_clean"],
            evaluation["gpu_detected"],
            evaluation["cpu_detected"],
            evaluation["cpu_market_price"],
            evaluation["gpu_market_price"],
            evaluation["estimated_fair_price"],
            evaluation["saving_uah"],
            evaluation["saving_percent"],
            evaluation["deal_status"],
            evaluation["evaluated_at"],
            evaluation["id"]
        ))
        
        count_evaluated += 1

        if evaluation["saving_percent"] >= 10:
            print(f"\n[{evaluation['deal_status']}] {title[:60]}...")
            print(f"   Відеокарта: {evaluation['gpu_detected']} ({evaluation['gpu_market_price']} грн)")
            print(f"   Процесор:   {evaluation['cpu_detected']} ({evaluation['cpu_market_price']} грн)")
            print(f"   🔥 Вигода:  {evaluation['saving_uah']} грн ({evaluation['saving_percent']}%)")

    if updates_pool:
        cursor.executemany("""
            UPDATE ads 
            SET 
                seller_price_clean = ?,
                gpu_detected = ?,
                cpu_detected = ?,
                cpu_market_price = ?,
                gpu_market_price = ?,
                estimated_fair_price = ?,
                saving_uah = ?,
                saving_percent = ?,
                deal_status = ?,
                evaluated_at = ?
            WHERE id = ?
        """, updates_pool)
        conn.commit()
        print(f"\n✅ [УСПІХ] Успішно розпізнано та оцінено: {count_evaluated} комп'ютерів.")
    
    conn.close()


if __name__ == "__main__":
    main()
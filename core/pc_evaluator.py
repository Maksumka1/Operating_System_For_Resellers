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


def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.execute("PRAGMA journal_mode=WAL;")
    return conn


def load_latest_prices() -> dict[str, int]:
    """Витягує найсвіжіші ціни комплектуючих з бази даних за останню наявну дату"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT MAX(date) FROM component_prices")
    latest_date_row = cursor.fetchone()
    
    if not latest_date_row or not latest_date_row[0]:
        print("[ПОМИЛКА] База цін комплектуючих порожня! Спочатку запустіть парсер заліза.")
        conn.close()
        return {}
        
    latest_date = latest_date_row[0]
    print(f"[EVALUATOR] Використовуємо прайс-лист з бази за дату: {latest_date}")
    
    cursor.execute("""
        SELECT component_name, price 
        FROM component_prices 
        WHERE date = ?
    """, (latest_date,))
    
    clean_prices = {row[0]: row[1] for row in cursor.fetchall()}
    conn.close()
    return clean_prices


def detect_component_by_keywords(text_lower: str, target_keys: list[str]) -> str | None:
    """
    🔥 ПРАВИЛЬНИЙ РАДАР:
    Проходить по кожній моделі, бере її список 'required_keywords' з config.py
    і перевіряє, чи є хоча б ОДНЕ ключове слово в очищеному тексті оголошення.
    """
    # Сортуємо ключі за довжиною (щоб rtx_3060_ti перевірявся раніше за rtx_3060)
    sorted_keys = sorted(target_keys, key=len, reverse=True)
    
    for comp_key in sorted_keys:
        # Беремо масив згенерованих сленгових слів для цієї моделі
        required_keywords = HARDWARE_TARGETS[comp_key].get("required_keywords", [])
        
        for keyword in required_keywords:
            keyword_lower = keyword.lower()
            
            # Перевіряємо суворе входження слова (як разом, так і окремо, як у тебе в конфігу)
            if keyword_lower in text_lower:
                return comp_key  # Знайшли! Повертаємо назву моделі (наприклад, 'gtx_1060')
                
    return None


def evaluate_pc(ad_id: int, title: str, description: str, seller_price: int, component_prices: dict) -> dict:
    title_clean = title.replace("-", " ")
    desc_clean = description.replace("-", " ") if description else ""
    
    full_text_lower = f"{title_clean} {desc_clean}".lower()

    hardware_keys = [k for k in HARDWARE_TARGETS.keys() if not k.startswith("pc_")]
    
    gpus_keys = [k for k in hardware_keys if any(x in k.lower() for x in ["rtx", "gtx", "rx", "hd", "r9"])]
    cpus_keys = [k for k in hardware_keys if any(x in k.lower() for x in ["ryzen", "i3", "i5", "i7", "i9", "xeon"])]

    # 1. Шукаємо відеокарту за її required_keywords
    gpu = detect_component_by_keywords(full_text_lower, gpus_keys)
    if gpu:
        gpu_price = component_prices.get(gpu, 0)
        if gpu_price == 0:
            gpu_display = f"{gpu} (Дефолт прайс)"
            gpu_price = 0
        else:
            gpu_display = gpu
    else:
        gpu_display = "Unknown GPU"
        gpu_price = 0

    # 2. Шукаємо процесор за його required_keywords
    cpu = detect_component_by_keywords(full_text_lower, cpus_keys)
    if cpu:
        cpu_price = component_prices.get(cpu, 0)
        if cpu_price == 0:
            cpu_display = f"{cpu} (Дефолт прайс)"
            cpu_price = 0
        else:
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
        return
        
    conn = get_db_connection()
    cursor = conn.cursor()

    # Вибираємо тільки не оцінені ПК
    cursor.execute("""
        SELECT id, title, description, price, url 
        FROM ads 
        WHERE item_type = 'pc' 
          AND status = 'active' 
    """)
    # AND has_ban_word = 0 
    # AND estimated_fair_price IS NULL
    unrated_pcs = cursor.fetchall()

    if not unrated_pcs:
        print("[INFO] Немає нових чистих ПК для оцінки.")
        conn.close()
        return

    print(f"[EVALUATOR] Знайдено {len(unrated_pcs)} комп'ютерів для тотального аналізу за ключами.")
    
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
            print(f"   🔥 Маржа перепродажу: {evaluation['saving_uah']} грн ({evaluation['saving_percent']}%)")

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
        print(f"\n[УСПІХ] Оцінку завершено! Оброблено за required_keywords: {count_evaluated} комп'ютерів.")
    
    conn.close()


if __name__ == "__main__":
    main()
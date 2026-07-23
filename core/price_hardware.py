from __future__ import annotations

import sys
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
if not (PROJECT_ROOT / "config.py").exists():
    PROJECT_ROOT = PROJECT_ROOT.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from config import HARDWARE_TARGETS, DB_FILE

hardware_items = {k: v for k, v in HARDWARE_TARGETS.items() if not k.startswith("pc_")}


def get_db_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_FILE)
    conn.execute("PRAGMA journal_mode=WAL;")
    return conn


def calculate_percentile_price(prices: list[int], percentile: float = 0.33) -> int:
    if not prices:
        return 0
    
    sorted_prices = sorted(prices)
    n = len(sorted_prices)

    if n >= 8:
        trim_size = int(n * 0.1)
        sorted_prices = sorted_prices[trim_size : n - trim_size]
        n = len(sorted_prices)

    index = int(n * percentile)
    if index >= n:
        index = n - 1
        
    return sorted_prices[index]


def main() -> None:
    today_sql = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    if not DB_FILE.exists():
        print("[ПОМИЛКА] Базу даних не знайдено! Спочатку запустіть db_init.py.")
        return

    conn = get_db_connection()
    cursor = conn.cursor()

    print(f"--- ПОЧАТОК АНАЛІЗУ ЦІН ЗА {today_sql} ---")

    for target_name in hardware_items.keys():
        cursor.execute("""
            SELECT price FROM ads 
            WHERE component_name = ? AND parsed_date = ? AND price > 100 AND seller_risk_score = 'safe' AND has_defects = 0
        """, (target_name, today_sql))
        
        prices_list = [row[0] for row in cursor.fetchall()]

        if prices_list:
            real_price = calculate_percentile_price(prices_list, percentile=0.33)
            cursor.execute("""
                INSERT OR REPLACE INTO component_prices (component_name, price, date)
                VALUES (?, ?, ?)
            """, (target_name, real_price, today_sql))
            print(f"[RESULT] -> {target_name}: {real_price} UAH (вибірка: {len(prices_list)} оголошень)")

    conn.commit()
    conn.close()
    print("\n[УСПІХ] База даних повністю оновлена та закрита!")


if __name__ == "__main__":
    main()
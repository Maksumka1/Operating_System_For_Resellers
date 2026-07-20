import sys
from datetime import datetime, timezone
import json
import re
import sqlite3
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
if not (PROJECT_ROOT / "config.py").exists():
    PROJECT_ROOT = PROJECT_ROOT.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from config import DB_FILE, STATS_FILE

BANNED_WORDS = [
    "athlon", "ddr2", "ddr1", "ddr 2", "ddr 1", "ddr-2", "ddr-1",  
    "core2duo", "core 2 duo", "core 2duo", "f2a55m", "fm2a88", "fm2a85", "fm2a75", "fm2a68", "fm2a55", "fm2a45", "fm2a35", 
    "fm2a25", "fm2a15", "fm2a05", "fm2a00", "fm1a88", "fm1a85", "fm1a75", "fm1a68", "fm1a55", "fm1a45", "fm1a35", "fm1a25", 
    "fm1a15", "fm1a05", "fm1a00", "a8-76", "a8-75", "a8-74", "a8-73", "a8-72", "a8-71", "a8-70", "a6-76", "a6-75", "a6-74", 
    "a6-73", "a6-72", "a6-71", "a6-70", "a4-76", "a4-75", "a4-74", "a4-73", "a4-72", "a4-71", "a4-70",  
    "athlon ii", "athlon x2", "athlon x4", "athlon x6", "athlon x8"
]


def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.execute("PRAGMA journal_mode=WAL;")
    return conn


def contains_banned_words(text: str) -> bool:
    if not text:
        return False
    lowered_text = text.lower()
    return any(word.lower() in lowered_text for word in BANNED_WORDS)


def update_statistics(section: str, metrics: dict) -> None:
    today_str = datetime.now(timezone.utc).strftime("%d-%m-%Y")
    stats = {}
    
    if STATS_FILE.exists():
        try:
            stats = json.loads(STATS_FILE.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            stats = {}
            
    if today_str not in stats:
        stats[today_str] = {
            "parsing": {"parsed_total_new": 0, "duplicates_skipped": 0, "avg_parsing_time_ms": 0.0, "total_time_seconds": 0.0},
            "filtering": {"banned_words_triggered": 0, "filtered_total_active": 0},
            "market_analysis": {"avg_ad_price_uah": 0, "min_price_today": 0, "max_price_today": 0},
            "system_health": {"network_errors": 0, "parsing_errors": 0}
        }
        
    if section in stats[today_str]:
        stats[today_str][section].update(metrics)
            
    STATS_FILE.write_text(json.dumps(stats, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> None:
    if not DB_FILE.exists():
        print("[ПОМИЛКА] Базу даних не знайдено! Спочатку запустіть db_init.py.")
        return

    conn = get_db_connection()
    cursor = conn.cursor()


    cursor.execute("""
        SELECT id, title, description 
        FROM ads 
        WHERE item_type = 'pc' 
          AND status = 'active' 
          AND estimated_fair_price IS NULL
          AND has_ban_word = 0
    """)
    unfiltered_pcs = cursor.fetchall()

    if not unfiltered_pcs:
        print("[INFO] Немає нових невідфільтрованих комп'ютерів у базі.")
        conn.close()
        return

    print(f"[FILTER] Знайдено {len(unfiltered_pcs)} нових комп'ютерів для перевірки на бан-ворди...")

    banned_words_count = 0
    new_approved_count = 0

    ids_with_banned_hardware = []


    for db_id, title, description in unfiltered_pcs:
        full_text = f"{title} {description}"
        
        if contains_banned_words(full_text):
            ids_with_banned_hardware.append((db_id,))
            banned_words_count += 1
        else:
            new_approved_count += 1


    if ids_with_banned_hardware:
        cursor.executemany("""
            UPDATE ads 
            SET has_ban_word = 1 
            WHERE id = ?
        """, ids_with_banned_hardware)
        conn.commit()
        print(f"[УСПІХ] Помічено {banned_words_count} оголошень як такі, що містять сміттєві деталі (has_ban_word = 1).")
    
    print(f"[УСПІХ] Фільтрація завершена. Схвалено для подальшої оцінки: {new_approved_count} ПК.")

    cursor.execute("""
        SELECT price 
        FROM ads 
        WHERE item_type = 'pc' AND status = 'active' AND has_ban_word = 0
    """)
    active_prices = [row[0] for row in cursor.fetchall()]

    market_metrics = {"avg_ad_price_uah": 0, "min_price_today": 0, "max_price_today": 0}
    if active_prices:
        market_metrics = {
            "avg_ad_price_uah": int(sum(active_prices) / len(active_prices)),
            "min_price_today": min(active_prices),
            "max_price_today": max(active_prices)
        }

    cursor.execute("SELECT COUNT(*) FROM ads WHERE item_type = 'pc' AND status = 'active' AND has_ban_word = 0")
    active_total = cursor.fetchone()[0]

    update_statistics("filtering", {
        "banned_words_triggered": banned_words_count,
        "filtered_total_active": active_total
    })
    update_statistics("market_analysis", market_metrics)

    print(f"\n[INFO] Статистика ЧИСТИХ активних оголошень у базі (Всього: {active_total})")
    print(f"  - Середня ціна: {market_metrics['avg_ad_price_uah']} грн")
    print(f"  - Мінімальна ціна: {market_metrics['min_price_today']} грн")

    conn.close()


if __name__ == "__main__":
    main()
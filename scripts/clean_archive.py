from __future__ import annotations

import sys
import sqlite3
import time
from datetime import datetime, timezone
from pathlib import Path
import requests
from concurrent.futures import ThreadPoolExecutor

PROJECT_ROOT = Path(__file__).resolve().parent
if not (PROJECT_ROOT / "config.py").exists():
    PROJECT_ROOT = PROJECT_ROOT.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from config import DB_FILE


def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.execute("PRAGMA journal_mode=WAL;")
    return conn


def check_single_ad_status(ad_id: int, url: str) -> tuple[int, str, str | None]:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    new_status = "active"
    deactivated_at = None

    try:
        response = requests.head(url, headers=headers, timeout=5, allow_redirects=True)
        
        if response.status_code in [404, 410] or "obyavlenie/arkhiv" in response.url or "/d/uk/obyavlenie/" not in response.url:
            new_status = "deactivated"
            deactivated_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M")
            
    except requests.RequestException:
        pass

    return ad_id, new_status, deactivated_at


def main() -> None:
    today_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    print(f"--- СТАРТ БАГАТОПОТОКОВОЇ ПЕРЕВІРКИ АКТИВНОСТІ ОГОЛОШЕНЬ ({today_str}) ---")

    if not DB_FILE.exists():
        print("[ПОМИЛКА] Базу даних не знайдено! Спочатку запустіть db_init.py.")
        return

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id, url FROM ads WHERE status = 'active'")
    active_ads = cursor.fetchall()

    if not active_ads:
        print("[INFO] У базі немає активних оголошень для перевірки.")
        conn.close()
        return

    print(f"[VERIFIER] Знайдено {len(active_ads)} активних оголошень у базі.")
    print("Запуск перевірки в 15 потоків...")

    tasks = [(ad_id, url) for ad_id, url in active_ads]
    
    results = []

    start_time = time.time()
    with ThreadPoolExecutor(max_workers=15) as executor:
        futures = [executor.submit(check_single_ad_status, ad_id, url) for ad_id, url in tasks]
        for future in futures:
            results.append(future.result())

    deactivated_pool = [
        (new_status, deac_at, ad_id) 
        for ad_id, new_status, deac_at in results 
        if new_status == "deactivated"
    ]

    if deactivated_pool:
        cursor.executemany("""
            UPDATE ads 
            SET status = ?, deactivated_at = ?
            WHERE id = ?
        """, deactivated_pool)
        conn.commit()
        print(f"[УСПІХ] Автоматично деактивовано (відправлено в архів): {len(deactivated_pool)} шт.")
    else:
        print("[INFO] Всі перевірені оголошення досі активні на OLX.")

    conn.close()
    
    end_time = time.time()
    print(f"--- ПЕРЕВІРКУ ЗАВЕРШЕНО ЗА {end_time - start_time:.2f} СЕКУНД ---")


if __name__ == "__main__":
    main()
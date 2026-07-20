from __future__ import annotations

import sys
import json
import sqlite3
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import requests 
import re
from datetime import datetime, timezone
from pathlib import Path
import time
from concurrent.futures import ThreadPoolExecutor  # Підключаємо пул потоків

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


def validate_title(title: str, required_keywords: list[str]) -> bool:
    title_lower = title.lower()
    return any(word.lower() in title_lower for word in required_keywords)


def is_broken_ad(title: str) -> bool:
    title_lower = title.lower()
    broken_keywords = [
        "неробоч", "не робоч", "запчастин", "запчасть", "ремонт", "дефект", 
        "відновлен", "восстановлен", "артефакт", "поломан", "неисправн", 
        "не справн", "на детал", "запчасті", "прогрів", "не стартует",
        "комплект", "не включа", "не включається", "не включается", "не працює",
        "не работает", "не працює", "не робочий"
    ]
    return any(word in title_lower for word in broken_keywords)


def clean_url(url: str) -> str:
    parsed = urlparse(url)
    return f"{parsed.scheme}://{parsed.netloc}{parsed.path}"


def linkResponse(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    response = requests.get(url, headers=headers, timeout=10)
    soup = BeautifulSoup(response.text, 'lxml')
    return soup


def extract_price(price_str: str) -> int:
    digits = re.sub(r"\D", "", price_str)
    return int(digits) if digits else 0


def calculate_percentile_price(prices: list[int], percentile: float = 0.33) -> int:
    if not prices:
        return 0
    
    sorted_prices = sorted(prices)
    n = len(sorted_prices)

    if n > 5:
        trim_size = int(n * 0.1)
        if trim_size == 0:
            trim_size = 1
        sorted_prices = sorted_prices[trim_size : n - trim_size]
        n = len(sorted_prices)

    index = int(n * percentile)
    
    if index >= n:
        index = n - 1
        
    return sorted_prices[index]


def parse_single_hardware(target_name: str, config: dict, seen_urls: set[str], today_sql: str) -> list[tuple]:
    print(f"📡 [ПОТОК] Початок парсингу: {target_name}")
    local_parsed = []
    
    item_type = "gpu" if any(x in target_name.lower() for x in ["rtx", "gtx", "rx"]) else "cpu"

    try:
        soup = linkResponse(config["url"])
        advertisament = soup.find_all('div', class_='css-ri9uxm')
    except requests.RequestException:
        print(f"❌ [ПОМИЛКА МЕРЕЖІ] Не вдалося завантажити OLX для {target_name}.")
        return []
    
    count_added = 0
    count_skipped_validation = 0
    
    for i in advertisament:
        advert_url = "Невідомо"
        try:
            link_element = i.find('a')
            if not link_element: 
                continue
                
            raw_url = "https://www.olx.ua" + link_element.get('href')
            advert_url = clean_url(raw_url) 

            if advert_url in seen_urls:
                continue
                
            title_element = i.find('h4', class_='css-wlcw7o')
            if not title_element: 
                continue

            city_element = i.find('p', class_='css-1453zif')
            price_element = i.find('p', class_='css-61fb99') 

            title = title_element.text.replace("'", "").strip()
            price_raw = price_element.text.strip() if price_element else "0"
            price = extract_price(price_raw)

            # Парсинг фото прибрали. Передаємо "Невідомо" як плейсхолдер.
            # seller_analyzer згодом перезапише його на справжній якісний URL
            photo_url = "Невідомо"

            city = "Невідомо"
            ad_date = "Невідомо"
            if city_element:
                city_date_text = city_element.text.strip()
                if " - " in city_date_text:
                    parts = city_date_text.split(" - ", 1)
                    city = parts[0].strip()
                    ad_date = parts[1].strip()
                else:
                    city = city_date_text

            if not validate_title(title, config["required_keywords"]) or is_broken_ad(title):
                count_skipped_validation += 1
                continue

            local_parsed.append((
                advert_url, title, None, price, item_type, target_name, 
                city, ad_date, photo_url, today_sql, "active"
            ))
            count_added += 1
        
        except AttributeError:
            continue
        except Exception:
            continue

    print(f"✨ [ГОТОВО] {target_name}: додано {count_added}, відсіяно {count_skipped_validation}")
    return local_parsed


def main() -> None:
    today_sql = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    if not DB_FILE.exists():
        print("[ПОМИЛКА] Базу даних не знайдено! Спочатку запустіть db_init.py.")
        return

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT url FROM ads")
    seen_urls = set(row[0] for row in cursor.fetchall())
    print(f"[БАЗА] Завантажено {len(seen_urls)} раніше спарсених оголошень для дедуплікації.")

    new_ads_to_insert = []
    hardware_items = {k: v for k, v in HARDWARE_TARGETS.items() if not k.startswith("pc_")}

    # =====================================================================
    # 🔥 ПАРАЛЕЛЬНИЙ МУЛЬТИТРЕДИНГ 
    # =====================================================================
    start_time = time.time()
    
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = [
            executor.submit(parse_single_hardware, name, cfg, seen_urls, today_sql)
            for name, cfg in hardware_items.items()
        ]
        
        for future in futures:
            new_ads_to_insert.extend(future.result())

    print(f"\n⏱️ Мережевий збір завершено за {time.time() - start_time:.2f} сек.")

    if new_ads_to_insert:
        cursor.executemany("""
        INSERT OR IGNORE INTO ads (
            url, title, description, price, item_type, component_name, 
            city, created_at_olx, photo_url, parsed_date, status
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, new_ads_to_insert)
        conn.commit()
        print(f"\n[УСПІХ] Збережено {len(new_ads_to_insert)} нових унікальних комплектуючих в 'ads'.")
    else:
        print("[INFO] Нових оголошень для запису не знайдено.")

    # =====================================================================
    # --- АНАЛІЗ ЦІН ---
    # =====================================================================
    print(f"\n--- ПОЧАТОК АНАЛІЗУ ЦІН ЗА {today_sql} ---")
    
    for target_name in hardware_items.keys():
        cursor.execute("""
            SELECT price FROM ads 
            WHERE component_name = ? AND parsed_date = ? AND price > 100
        """, (target_name, today_sql))
        
        prices_list = [row[0] for row in cursor.fetchall()]

        if prices_list:
            real_price = calculate_percentile_price(prices_list, percentile=0.33)
            cursor.execute("""
                INSERT OR REPLACE INTO component_prices (component_name, price, date)
                VALUES (?, ?, ?)
            """, (target_name, real_price, today_sql))
            print(f"[RESULT] -> {target_name}: {real_price} uah")

    conn.commit()
    conn.close()
    print("\n[УСПІХ] База даних повністю оновлена та закрита!")


if __name__ == "__main__":
    main()
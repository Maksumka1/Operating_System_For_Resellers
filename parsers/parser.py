from __future__ import annotations

import asyncio
import json
import re
import sqlite3
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

from curl_cffi.requests import AsyncSession

PROJECT_ROOT = Path(__file__).resolve().parent
if not (PROJECT_ROOT / "config.py").exists():
    PROJECT_ROOT = PROJECT_ROOT.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from config import DB_FILE, STATS_FILE

TIMEOUT = 15

# СТОП-СЛОВА: Якщо це є в назві, але немає маркерів цілого ПК — це окрема запчастина
NOT_A_PC_WORDS = [
    "материнська плата", "материнская плата", "материнка", "мать",
    "блок питания", "блок живлення", "дбж", "ups", "бесперебойник",
    "оперативна память", "оперативная память", "озу", "ram",
    "кулер", "вентилятор", "корпус без", "видеокарта", "відеокарта", 
    "процессор", "процесор", "ssd", "hdd", "жесткий диск", "жорсткий диск"
]

HEADERS = {
    "accept": "application/json",
    "accept-language": "uk",
    "content-type": "application/json",
    "origin": "https://www.olx.ua",
    "priority": "u=1, i",
    "referer": "https://www.olx.ua/",
    "sec-ch-ua": '"Not;A=Brand";v="8", "Chromium";v="124", "Google Chrome";v="124"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "x-client": "DESKTOP",  # 👈 КРИТИЧНИЙ ХЕДЕР ДЛЯ GRAPHQL
}

# GraphQL запит без текстових прив'язок
GRAPHQL_QUERY = """query ListingSearchQuery($searchParameters: [SearchParameter!] = []) {
  clientCompatibleListings(searchParameters: $searchParameters) {
    ... on ListingSuccess {
      data {
        id title status url created_time description
        location { city { name } }
        params {
          key name
          value {
            ... on PriceParam { value currency label }
          }
        }
      }
    }
  }
}"""


def get_db_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_FILE)
    conn.execute("PRAGMA journal_mode=WAL;")
    return conn


def clean_url(url: str) -> str:
    parsed = urlparse(url)
    return f"{parsed.scheme}://{parsed.netloc}{parsed.path}"


def extract_price(price_val: str | int | float) -> int:
    if isinstance(price_val, (int, float)):
        return int(price_val)
    digits = re.sub(r"\D", "", str(price_val))
    return int(digits) if digits else 0


def is_real_pc(title: str) -> bool:
    """Перевіряє, чи є оголошення цілим комп'ютером, а не окремою запчастиною."""
    if not title:
        return False
        
    title_lower = title.lower()
    pc_indicators = ["пк", "комп", "системний блок", "системный блок", "компьютер", "комп’ютер", "системник", "pc", "mac", "блок"]

    for bad_word in NOT_A_PC_WORDS:
        if bad_word in title_lower:
            if title_lower.startswith(bad_word):
                return False
            if not any(indicator in title_lower for indicator in pc_indicators):
                return False

    return True


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
            "parsing": {
                "parsed_total_new": 0,
                "duplicates_skipped": 0,
                "avg_parsing_time_ms": 0.0,
                "total_time_seconds": 0.0,
            },
            "filtering": {
                "banned_words_triggered": 0,
                "filtered_total_active": 0,
            },
            "market_analysis": {
                "avg_ad_price_uah": 0,
                "min_price_today": 0,
                "max_price_today": 0,
            },
            "system_health": {"network_errors": 0, "parsing_errors": 0},
        }

    if section in stats[today_str]:
        stats[today_str][section].update(metrics)

    STATS_FILE.write_text(
        json.dumps(stats, ensure_ascii=False, indent=2), encoding="utf-8"
    )


async def fetch_latest_pcs(
    session: AsyncSession,
    seen_urls: set[str],
    max_retries: int = 5,
) -> tuple[list[tuple], int, int, int]:
    print("\n🎯 Завантажуємо свіжий потік комп'ютерів (Категорія 78)...")

    json_payload = {
        "query": GRAPHQL_QUERY,
        "variables": {
            "searchParameters": [
                {"key": "category_id", "value": "78"},
                {"key": "limit", "value": "50"},
            ]
        },
    }

    new_items = []
    duplicates_count = 0
    network_errors = 0
    parsing_errors = 0

    today_sql = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    for attempt in range(1, max_retries + 1):
        try:
            resp = await session.post(
                "https://www.olx.ua/apigateway/graphql",
                json=json_payload,
                timeout=TIMEOUT,
            )

            if resp.status_code in (401, 403):
                print(f"[WARN GraphQL] 403 Forbidden. Спроба {attempt}/{max_retries}. Прогрів та чекаємо 10s...")
                network_errors += 1
                
                # Прогрів через каталог, а не просто головну
                try:
                    await session.get("https://www.olx.ua/uk/elektronika/", timeout=10)
                except Exception:
                    pass
                
                # Пауза 10 секунд дає DataDome час скинути ліміт
                await asyncio.sleep(10)
                continue

            if resp.status_code != 200:
                print(f"[ERR GraphQL] HTTP status {resp.status_code}. Спроба {attempt}/{max_retries}...")
                network_errors += 1
                await asyncio.sleep(attempt * 3)
                continue

            data = resp.json()
            listings = (
                data.get("data", {})
                .get("clientCompatibleListings", {})
                .get("data", [])
            )

            for item in listings:
                try:
                    raw_id = item.get("id")
                    ad_id = int(raw_id) if raw_id and str(raw_id).isdigit() else None

                    raw_url = item.get("url", "")
                    if not raw_url:
                        continue

                    if not raw_url.startswith("http"):
                        raw_url = "https://www.olx.ua" + raw_url

                    advert_url = clean_url(raw_url)

                    if advert_url in seen_urls:
                        duplicates_count += 1
                        continue

                    title = item.get("title", "").replace("'", "").strip()

                    if not is_real_pc(title):
                        print(f"  [🚫 ВІДСІЯНО ЗАПЧАСТИНУ]: {title[:50]}...")
                        continue

                    description = item.get("description", "").strip().replace("<br />", "")

                    price = 0
                    for param in item.get("params", []):
                        if param.get("key") == "price":
                            val_data = param.get("value", {})
                            price = extract_price(val_data.get("value", 0))
                            break

                    loc_data = item.get("location", {}) or {}
                    city = loc_data.get("city", {}).get("name", "Невідомо")

                    new_items.append(
                        (
                            ad_id,
                            advert_url,
                            today_sql,
                            "active",
                            title,
                            description,
                            price,
                            "pc",
                            None,
                            city,
                            price,
                        )
                    )

                    seen_urls.add(advert_url)
                    print(f"  [+] Новий ПК [ID: {ad_id}]: {title[:45]}... ({price} грн)")

                except Exception as ex:
                    parsing_errors += 1
                    print(f"[ПОМИЛКА ПАРСИНГУ] Елемент оголошення: {ex}")

            return new_items, duplicates_count, network_errors, parsing_errors

        except Exception as ex:
            network_errors += 1
            print(f"[ПОМИЛКА МЕРЕЖІ] Спроба {attempt}/{max_retries}: {ex}")
            await asyncio.sleep(attempt * 2)

    print(f"❌ [КРИТИЧНО] Не вдалося завантажити ПК після {max_retries} спроб.")
    return new_items, duplicates_count, network_errors, parsing_errors

async def main_async() -> None:
    if not DB_FILE.exists():
        print("[ПОМИЛКА] Базу даних не знайдено!")
        return

    start_time = time.time()

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT url FROM ads")
    seen_urls = set(row[0] for row in cursor.fetchall())
    conn.close()
    print(f"[БАЗА] Завантажено {len(seen_urls)} оголошень для дедуплікації.")

    async with AsyncSession(headers=HEADERS, impersonate="chrome124") as session:
        print("🔥 Прогріваємо сесію OLX...")
        try:
            await session.get("https://www.olx.ua/", timeout=15)
            await asyncio.sleep(0.5)
        except Exception as e:
            print(f"[WARN Warmup] Помилка прогріву: {e}")

        all_new_pcs, duplicates_count, network_errors_count, parsing_errors_count = (
            await fetch_latest_pcs(session, seen_urls, max_retries=5)
        )

    new_parsed_count = len(all_new_pcs)

    if all_new_pcs:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.executemany(
            """
            INSERT OR IGNORE INTO ads (
                ad_id, 
                url, 
                parsed_date, 
                status, 
                title, 
                description, 
                price, 
                item_type, 
                component_name, 
                city, 
                seller_price_clean
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            all_new_pcs,
        )
        conn.commit()
        conn.close()
        print(f"\n[УСПІХ] Збережено {new_parsed_count} нових ПК у таблицю 'ads'.")
    else:
        print("\n[INFO] Нових комп'ютерів у цій ітерації немає.")

    end_time = time.time()
    total_time_seconds = end_time - start_time
    total_time_ms = total_time_seconds * 1000
    avg_time = (
        round(total_time_ms / new_parsed_count, 2)
        if new_parsed_count > 0
        else 0
    )

    print(f"⏱️ Час парсингу: {total_time_seconds:.2f} сек")

    update_statistics(
        "parsing",
        {
            "parsed_total_new": new_parsed_count,
            "duplicates_skipped": duplicates_count,
            "avg_parsing_time_ms": avg_time,
            "total_time_seconds": round(total_time_seconds, 2),
        },
    )

    update_statistics(
        "system_health",
        {
            "network_errors": network_errors_count,
            "parsing_errors": parsing_errors_count,
        },
    )


def main() -> None:
    asyncio.run(main_async())


if __name__ == "__main__":
    main()
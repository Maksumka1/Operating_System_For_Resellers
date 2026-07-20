import sys
import sqlite3
import re
import json
import requests
from bs4 import BeautifulSoup
from pathlib import Path
import time
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor

# Налаштування шляхів для коректного імпорту конфігу
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


def find_key_recursively(data, target_key):
    if isinstance(data, dict):
        if target_key in data and isinstance(data[target_key], dict) and "id" in data[target_key]:
            return data[target_key]
        for key, value in data.items():
            result = find_key_recursively(value, target_key)
            if result:
                return result
    elif isinstance(data, list):
        for item in data:
            result = find_key_recursively(item, target_key)
            if result:
                return result
    return None


def extract_olx_json_state(html_text: str) -> dict | None:
    try:
        match = re.search(r'window\.__PRERENDERED_STATE__\s*=\s*"((?:\\.|[^"\\])*)"', html_text, re.DOTALL)
        if not match:
            match = re.search(r"window\.__PRERENDERED_STATE__\s*=\s*'((?:\\.|[^'\\])*)'", html_text, re.DOTALL)
            
        if match:
            raw_escaped_json = match.group(1)
            clean_json_str = json.loads(f'"{raw_escaped_json}"')
            return json.loads(clean_json_str)
    except Exception as e:
        print(f"[ERROR] Помилка розпакування __PRERENDERED_STATE__: {e}")
    return None


def fetch_delivery_deals(seller_id: str) -> int:
    if not seller_id or seller_id == "failed":
        return 0
    url = f"https://khonor.eu-sharedservices.olxcdn.com/api/olx/ua/user/{seller_id}/badge/delivery"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "uk,en-US;q=0.9,en;q=0.8",
        "Origin": "https://www.olx.ua",
        "Referer": "https://www.olx.ua/",
        "X-Market": "ua",
        "X-Platform": "web"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code != 200:
            return 0
            
        data = response.json()
        for badge in data.get("body", []):
            if badge.get("name") == "delivery":
                return int(badge.get("data", {}).get("amount", 0))
    except Exception:
        pass
    return 0


def fetch_seller_rating(seller_uuid: str) -> str:
    if not seller_uuid:
        return "немає оцінок"
    url = f"https://rating-cdn.css.olx.io/ratings/v1/public/olxua/user/{seller_uuid}/eligibleClusters?includeScores=true"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            data = response.json()
            clusters = data.get("clusters", [])
            if clusters:
                cluster = clusters[0]
                score = cluster.get("scoreDetails", {}).get("value", None)
                total_ratings = cluster.get("scoreDetails", {}).get("ratings", {}).get("totalCount", 0)
                
                if score is not None and total_ratings > 0:
                    return f"{score}/5.0 ({total_ratings} оцінок)"
    except Exception:
        pass
    return "немає оцінок"


def fetch_and_analyze_seller(url: str) -> dict | None:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            return None
            
        state = extract_olx_json_state(response.text)
        if not state:
            return None

        user_data = find_key_recursively(state, "user")
        if not user_data:
            return None

        is_business_flag = False
        olx_created_time = None
        olx_refresh_time = None
        olx_city_name = None
        olx_photo_url = None
        olx_description = None

        if "ad" in state and isinstance(state["ad"], dict):
            inner_ad = state["ad"].get("ad", {})
            if isinstance(inner_ad, dict):
                is_business_flag = inner_ad.get("isBusiness", False)
                olx_created_time = inner_ad.get("createdTime")
                olx_refresh_time = inner_ad.get("lastRefreshTime")
                olx_description = inner_ad.get("description") # 🔥 Забираємо опис з JSON
                
                location_data = inner_ad.get("location", {})
                if isinstance(location_data, dict):
                    olx_city_name = location_data.get("cityName")
                
                photos_array = inner_ad.get("photos", [])
                if photos_array and len(photos_array) > 0:
                    olx_photo_url = photos_array[0]

        seller_id = str(user_data.get("id", ""))
        seller_uuid = str(user_data.get("uuid", ""))  
        seller_name = user_data.get("name", "Невідомо")
        created_raw = user_data.get("created", "")
        
        created_year = "Невідомо"
        if created_raw:
            try:
                created_year = created_raw.split("-")[0]
            except Exception:
                pass

        successful_deals = fetch_delivery_deals(seller_id)
        seller_rating = fetch_seller_rating(seller_uuid)

        return {
            "seller_id": seller_id,
            "seller_name": seller_name,
            "seller_created_at": created_year,
            "seller_successful_deals": successful_deals,  
            "seller_rating": seller_rating,                
            "is_company": is_business_flag,
            "olx_created_time": olx_created_time,
            "olx_refresh_time": olx_refresh_time,
            "olx_city_name": olx_city_name,
            "olx_photo_url": olx_photo_url,
            "description": olx_description
        }

    except Exception as e:
        print(f"[ERROR] Не вдалося обробити URL {url}: {e}")
        return None


def process_single_ad_worker(ad_data: tuple) -> dict | None:
    """Функція для роботи всередині окремого потоку (Тільки мережа та аналітика)"""
    ad_id, url, price, item_type, title = ad_data
    print(f"📡 [ПОТОК] Збір профілю для: {url[:50]}...")
    
    seller_info = fetch_and_analyze_seller(url)
    if not seller_info:
        return {"ad_id": ad_id, "status": "failed"}

    real_olx_ads_count = seller_info["seller_successful_deals"]
    rating_str = seller_info["seller_rating"]
    
    # 🔍 Обробка зірок
    if rating_str and rating_str != "немає оцінок":
        try:
            match = re.match(r"([0-9.]+)/5\.0", rating_str)
            seller_stars = float(match.group(1)) if match else 0.0
        except Exception:
            seller_stars = 0.0
    else:
        seller_stars = 0.0

    # ⏳ Вік акаунту
    today_year = datetime.now(timezone.utc).year
    try:
        reg_year = int(seller_info["seller_created_at"])
        acc_age_years = today_year - reg_year
    except ValueError:
        acc_age_years = 0

    # 🛡️ Розрахунок ризику (Твої покращені ліміти)
    is_low_deals = real_olx_ads_count < 20
    is_bad_rating = seller_stars < 4.0
    is_new_account = acc_age_years < 1

    if is_low_deals or is_bad_rating or is_new_account:
        seller_risk = "suspicious"
    elif acc_age_years >= 2:
        seller_risk = "safe"
    else:
        seller_risk = "neutral"

    # 📊 Розрахунок типу
    is_company = seller_info["is_company"]
    if is_company or (real_olx_ads_count > 50 and seller_stars >= 4.0):
        seller_type = "shop"
    elif not is_company and real_olx_ads_count > 50:
        seller_type = "reseller"
    else:
        seller_type = "private_person"

    return {
        "status": "success",
        "ad_id": ad_id,
        "url": url,
        "price": price,
        "title": title,
        "item_type": item_type,
        "seller_info": seller_info,
        "real_olx_ads_count": real_olx_ads_count,
        "seller_type": seller_type,
        "seller_risk": seller_risk
    }


def run_seller_analysis():
    print("\n" + "="*60)
    print("🕵️‍♂️ ЗАПУСК МОДУЛЯ АНАЛІЗУ ПРОДАВЦІВ OLX (МУЛЬТИТРЕДИНГ)")
    print("="*60)

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, url, price, item_type, title 
        FROM ads 
        WHERE seller_id IS NULL AND status = 'active' AND has_ban_word = 0
    """)
    ads_to_check = cursor.fetchall()
    conn.close()

    if not ads_to_check:
        print("[ANALYZER] Немає нових оголошень для аналізу профілів.")
        return

    print(f"[ANALYZER] Знайдено {len(ads_to_check)} нових лотів. Запуск пулу потоків...")

    with ThreadPoolExecutor(max_workers=15) as executor:
        results = list(executor.map(process_single_ad_worker, ads_to_check))

    # З'єднання для послідовного швидкого запису результатів
    conn = get_db_connection()
    cursor = conn.cursor()
    
    success_ids = []
    failed_count = 0

    print("\n💾 Запис результатів аналізу в базу даних...")
    for res in results:
        if not res:
            continue
            
        ad_id = res["ad_id"]
        
        if res["status"] == "failed":
            cursor.execute("UPDATE ads SET seller_id = 'failed' WHERE id = ?", (ad_id,))
            failed_count += 1
            continue

        info = res["seller_info"]
        
        # 1. Запис базового профайлу продавця та опису лоту (якщо опис підтягнувся)
        cursor.execute("""
            UPDATE ads 
            SET 
                seller_id = ?,
                seller_name = ?,
                seller_created_at = ?,
                seller_successful_deals = ?,
                seller_rating = ?,
                seller_type = ?,
                seller_risk_score = ?,
                photo_url = COALESCE(?, photo_url),
                description = COALESCE(?, description)
            WHERE id = ?
        """, (
            info["seller_id"], info["seller_name"], info["seller_created_at"],
            res["real_olx_ads_count"], info["rating_str" if "rating_str" in info else info["seller_rating"]], 
            res["seller_type"], res["seller_risk"], info.get("olx_photo_url"), info.get("description"), ad_id
        ))

        # 2. Додатковий запис параметрів збірки
        update_fields = {}
        if info.get("olx_city_name"):
            update_fields["city"] = info["olx_city_name"]
        
        if info.get("olx_created_time"):
            try:
                update_fields["created_at_olx"] = info["olx_created_time"].split("T")[0]
            except Exception:
                update_fields["created_at_olx"] = info["olx_created_time"]

        if info.get("olx_refresh_time"):
            update_fields["last_refresh_time"] = info["olx_refresh_time"]

        if update_fields:
            sql_set_parts = [f"{key} = ?" for key in update_fields.keys()]
            sql_query = f"UPDATE ads SET {', '.join(sql_set_parts)} WHERE id = ?"
            sql_params = list(update_fields.values()) + [ad_id]
            cursor.execute(sql_query, sql_params)
                
        success_ids.append(ad_id)
        time.sleep(0.01)

    conn.commit()

    # 🔥 ФІНАЛЬНИЙ ЗБІР ЗБАГАЧЕНИХ АНАЛІТИЧНИХ ДАНИХ ДЛЯ САЙТУ
    ads_to_broadcast = []
    if success_ids:
        print("📊 Підготовка розширених даних аналітики цін для пушу в WebSocket...")
        for ad_id in success_ids:
            cursor.execute("""
                SELECT 
                    url, title, description, price, item_type, city, created_at_olx, photo_url,
                    seller_name, seller_created_at, seller_successful_deals, seller_rating, seller_risk_score,
                    estimated_fair_price, competitor_price, saving_uah, saving_percent, evaluated_at
                FROM ads WHERE id = ?
            """, (ad_id,))
            r = cursor.fetchone()
            if r:
                ads_to_broadcast.append({
                    "url": r[0], "title": r[1], "description": r[2], "price": r[3], "item_type": r[4],
                    "city": r[5], "created_at_olx": r[6], "photo_url": r[7],
                    "seller_name": r[8], "seller_created_at": r[9], "seller_successful_deals": r[10] or 0,
                    "seller_rating": r[11] or "немає оцінок", "seller_risk": r[12] or "neutral",
                    "estimated_fair_price": r[13], "competitor_price": r[14],
                    "saving_uah": r[15], "saving_percent": r[16], "evaluated_at": r[17]
                })
    
    conn.close()
    
    # 🔥 НАДСИЛАННЯ ПОВНОГО JSON ВЕБ-ХУКУ НА ВЕБСЕРВЕР
    if ads_to_broadcast:
        print(f"\n🚀 Пушимо {len(ads_to_broadcast)} повністю проаналізованих лотів на Live-сайт...")
        for ad_payload in ads_to_broadcast:
            try:
                requests.post("http://localhost:8000/api/trigger-new-ad", json=ad_payload, timeout=2)
            except Exception as e:
                print(f"  ⚠️ Не вдалося відправити лот на веб-сервер реалтайму: {e}")

    print(f"\n[УСПІХ] Обробку завершено! Успішно проаналізовано: {len(success_ids)}, Помилок: {failed_count}")


if __name__ == "__main__":
    run_seller_analysis()
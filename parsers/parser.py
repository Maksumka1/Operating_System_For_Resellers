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

PROJECT_ROOT = Path(__file__).resolve().parent
if not (PROJECT_ROOT / "config.py").exists():
    PROJECT_ROOT = PROJECT_ROOT.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from config import HARDWARE_TARGETS, DB_FILE, STATS_FILE
def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.execute("PRAGMA journal_mode=WAL;")
    return conn


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
    today_sql = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    
    if not DB_FILE.exists():
        print("[ПОМИЛКА] Базу даних не знайдено! Спочатку запустіть db_init.py.")
        return

    start_time = time.time()
    new_parsed_count = 0
    duplicates_count = 0
    parsing_errors_count = 0  
    network_errors_count = 0

    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT url FROM ads")
    seen_urls = set(row[0] for row in cursor.fetchall())
    print(f"[БАЗА] Завантажено {len(seen_urls)} оголошень для дедуплікації.")


    pc_targets = {k: v for k, v in HARDWARE_TARGETS.items() if k.startswith("pc_")}

    print(f"[PC_PARSER] Знайдено {len(pc_targets)} цільових сторінок пошуку.")
    for target_name, target_info in pc_targets.items():
        search_url = target_info["url"]
        print(f"\n🎯 Завантажуємо вибірку ПК: {target_name.replace('pc_', '').upper()}")
        print(f"🔗 URL запиту: {search_url}")

        try:
            soup = linkResponse(search_url)
            advertisament = soup.find_all('div', class_='css-ri9uxm')
        except requests.RequestException:
            print("[ПОМИЛКА] Не вдалося підключитися до головної сторінки пошуку OLX.")
            update_statistics("system_health", {"network_errors": 1})
            conn.close()
            return

        new_pcs_to_insert = []

        for i in advertisament:
            advert_url = "Невідомо"
            try:
                link_element = i.find('a')
                if not link_element: 
                    continue
                    
                raw_url = "https://www.olx.ua" + link_element.get('href')
                advert_url = clean_url(raw_url) 

                if advert_url in seen_urls:
                    duplicates_count += 1
                    print(f"Пропущено (вже є в базі): {advert_url}")
                    continue

                advert_soup = linkResponse(advert_url)

                description = advert_soup.find('div', class_='css-fl29zg').text.strip()
                price_raw = advert_soup.find('h3', class_='css-yauxmy').text.strip()
                price = extract_price(price_raw)
                title = advert_soup.find('h4', class_='css-1hd136p').text.replace("'", "").strip()
                
                city = "Невідомо"

                new_pcs_to_insert.append((
                    advert_url,
                    title,
                    description,
                    price,
                    "pc",
                    None,        
                    city,
                    today_sql,
                    "active",
                    price        
                ))
                
                seen_urls.add(advert_url)
                new_parsed_count += 1
                print(f"Знайдено ПК: {title} ({price} грн)")
                
                # time.sleep(1.5)

            except AttributeError:
                parsing_errors_count += 1
                print(f"[ПОМИЛКА ПАРСИНГУ] Не вдалося розібрати елементи на сторінці: {advert_url}")
                continue
            except requests.RequestException:
                network_errors_count += 1
                print(f"[ПОМИЛКА МЕРЕЖІ] Помилка завантаження сторінки оголошення: {advert_url}")
                continue

        if new_pcs_to_insert:
            cursor.executemany("""
            INSERT OR IGNORE INTO ads (
                url, title, description, price, item_type, component_name, city, parsed_date, status, seller_price_clean
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, new_pcs_to_insert)
            conn.commit()
            print(f"\n[УСПІХ] Збережено {len(new_pcs_to_insert)} нових унікальних комп'ютерів у таблицю 'ads'.")
        else:
            print("\n[INFO] Нових комп'ютерів для запису в базу не виявлено.")

    conn.close()
    end_time = time.time()
    total_time_seconds = end_time - start_time
    total_time_ms = total_time_seconds * 1000
    avg_time = round(total_time_ms / new_parsed_count, 2) if new_parsed_count > 0 else 0

    print(f"Час виконання: {total_time_seconds:.2f} сек")

    update_statistics("parsing", {
        "parsed_total_new": new_parsed_count,
        "duplicates_skipped": duplicates_count,
        "avg_parsing_time_ms": avg_time,
        "total_time_seconds": round(total_time_seconds, 2)
    })

    update_statistics("system_health", {
        "network_errors": network_errors_count,
        "parsing_errors": parsing_errors_count
    })

    


if __name__ == "__main__":
    main()

# MVP - Готово!

# - парсинг
# - фільтрація
# - дедуплікація
# - збереження статусу оголошень
# - базова статистика

#----------------------------------------------------------------------------------------
#----------------------------------IDEAS-------------------------------------------------
#----------------------------------------------------------------------------------------
# Наприклад є базове оголошення про комп який дешевший за ринок на 1000грн, і продавець надійний, Але проблемка що це офісник і без відеокарти, він буде довго продавтися і програма так і написала навіть про нереальні 14-28днів!!! Це дуже багато, і знаєш що? Замічаю блок біля Аналізу ціни де пишуть рекомендації, там прямим текстом написано що можна докупити gtx_1060_3gb за 2200грн і зібравши до купи прибуток буде вже 2000грн і продасться він вже від 3-14 днів, це просто нереально, знизу кнопка знайти відеокарту? І як тільки я нажав то показало список з 5 найсвіжіих відеокарт gtx_1060



#----------------------------------------------------------------------------------------
### Система ринкової аналітики та сезонного прогнозування

#OLXSniper містить окремий модуль ринкової аналітики, який оновлюється приблизно кожні 5 хвилин і відображає живі метрики маркетплейсу: кількість нових оголошень, частку вигідних пропозицій, середній потенційний прибуток, швидкість продажу та інші агреговані показники. Інтерфейс побудований як real-time dashboard — цифри змінюються на очах, що створює відчуття постійно живого ринку.

#Особливо виділяється блок сезонного прогнозування. Система не лише показує прогноз на наступний місяць (наприклад, очікуване зростання кількості оголошень або прискорення продажів), а й пояснює причини цього прогнозу. При відкритті блоку «Причини прогнозу» користувач бачить:

#* тренд кількості оголошень за останні тижні;
#* тренд швидкості продажу;
#* порівняння з аналогічним періодом минулого року (year-over-year analysis);
#* невелику діаграму сезонності.

#З діаграми видно, що кінець літа та початок осені є піковим періодом для ринку комп’ютерної техніки: збільшується і кількість оголошень, і швидкість їх продажу. Другий виражений пік припадає на кінець осені та початок зими, тоді як решта року характеризується нижчою та відносно стабільною активністю.

#Така подача перетворює сервіс із простого парсера оголошень на інструмент ринкової аналітики, який допомагає приймати рішення не лише щодо окремого лота, а й щодо часу входу в ринок, швидкості обороту товару та очікуваної ліквідності категорії.


#----------------------------------------------------------------------------------------
### Progressive Trust Building — поступове нарощування довіри через візуалізацію процесу.
#OpenAI, Stripe, Vercel, Datadog, GitHub — усі великі SaaS роблять щось подібне:

#логи біжать,
#деплой “крутиться”,
#пайплайн світиться,
#сервіси з’єднані лініями.
#Людина відчуває: “Тут щось складне реально працює”.











# Parsing: Беремо масив з json файлу і додаємо нові оголошення, які парсимо з сайту. Записуємо їх у json файл.
# Filtring: Фільтруємо та вибираємо лише ті оголошення, які відповідають нашим критеріям (ціна, категорія, тощо). Нормалізує дані до єдиного формату. Фільтрує повторки. Записуємо їх у новий json файл.
# Price Finder: Використовуємо фільтровані оголошення для знаходження ринкової вартості. Підраховуємо середню ціну, мінімальну та максимальну ціну, записуємо дату оголошення, а також інші статистичні дані. Записуємо результати у новий json файл.

# A tool for fiding good deals: Беремо фільтровані оголошення комп'ютерів та знаходимо ринкову вартість, спираючись на ринкову ціну комплектуючів. Надсилати вигідні пропозиції на телеграм.
# Competitor Analysis Tool: Спираючись на фільровані оголошення в близькій ціновій категорії, порівнюємо з цінами конкурентів та знаходимо ідеальну ціну для продажу.
# Ads Verifier: Надсилає запроси на olx.com по оголошенням і перевіряє чи вони ще активні. Якщо оголошення не активне, знайти в json файлі та записати що воно продане. Записати скільки днів продавалося. Якщо через час це оголошення знову появляється на сайті, то записати що воно знову активне.

# Statistical Functions: Підраховуємо статистику по оголошенням. Наприклад, середня кількість оголошень в день, середня кількість оголошень в тиждень, середня кількість оголошень в місяць, середня кількість оголошень в рік. Середня кількість вигідних оголошень в день. Графіки цін до кожного товару. Графіки кількості оголошень до кожного товару. Графіки кількості вигідних оголошень до кожного товару. Графіки кількості оголошень по категоріям. Графіки кількості вигідних оголошень по категоріям. Графіки кількості оголошень по регіонах. Графіки кількості вигідних оголошень по регіонах.

# Goal Setter: Встановлюємо реалістичні цілі по заробітку на основі статистики по оголошенням. Наприклад, встановлюємо ціль заробити 1000$ за місяць, 5000$ за квартал, 20000$ за рік. Підраховуємо скільки потрібно продати товарів, щоб досягти цілі. Підраховуємо скільки потрібно знайти вигідних оголошень, щоб досягти цілі. Підраховуємо скільки потрібно знайти вигідних оголошень в день, тиждень, місяць, рік.

# Finance Manager: Підраховуємо скільки грошей заробили на основі статистики по оголошенням. Підраховуємо скільки грошей заробили в день, тиждень, місяць, рік. Підраховуємо скільки грошей заробили на кожному товарі. Підраховуємо скільки грошей заробили на кожній категорії. Підраховуємо скільки грошей заробили на кожному регіоні. Записує чистий прибуток, отриманий завдяки сервісу. Записує всі продажі, всі покупки, всі витрати, всі доходи в json файл.

# Main: Запускає парсинг, фільтрування, знаходження ринкової вартості, знаходження вигідних пропозицій, порівняння з конкурентами, перевірку активності оголошень, підрахунок статистики, встановлення цілей та підрахунок заробітку. 


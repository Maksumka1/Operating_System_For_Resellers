import sys
import sqlite3
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
if not (PROJECT_ROOT / "config.py").exists():
    PROJECT_ROOT = PROJECT_ROOT.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from config import DB_FILE

def init_db():
    print(f"--- ІНІЦІАЛІЗАЦІЯ БАЗИ ДАНИХ SQLite ({DB_FILE.name}) ---")
    
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("PRAGMA journal_mode=WAL;")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ads (
        -- СЛУЖБОВІ ТА СИСТЕМНІ ДАНІ
        id INTEGER PRIMARY KEY AUTOINCREMENT,  -- Унікальний порядковий номер запису в базі
        url TEXT UNIQUE,                       -- Чисте посилання на оголошення (використовується для дедуплікації)
        parsed_date TEXT NOT NULL,             -- Дата, коли наш парсер вперше знайшов лот (РРРР-ММ-ДД)
        status TEXT NOT NULL DEFAULT 'active', -- Стан лоту в системі: 'active' (активний) або 'deactivated' (архівований)
        deactivated_at TEXT,                   -- Дата й час, коли робот помітив, що оголошення на OLX видалили чи закрили

        -- БАЗОВА ІНФОРМАЦІЯ ПРО ЛОТ (ПАРСЕР СПИСКІВ)
        title TEXT NOT NULL,                   -- Заголовок оголошення з OLX (як написав продавець)
        description TEXT,                      -- Повний текст опису товару (для глибинного аналізу)
        price INTEGER NOT NULL,                -- Початкова сира ціна, вказана продавцем на сайті (в грн)
        item_type TEXT NOT NULL,               -- Категорія лоту: 'gpu' (відяха), 'cpu' (проц) або 'pc' (готовий комп)
        component_name TEXT,                   -- Назва конкретної залізяки з нашого конфігу (наприклад, 'gtx_1060' або NULL для ПК)
        city TEXT,                             -- Місто продажу (чисте значення з JSON або зі списку)
        created_at_olx TEXT,                   -- Чиста дата публікації оголошення продавцем на OLX
        last_refresh_time TEXT,                -- Точний час останнього підняття (refresh) оголошення на OLX
        photo_url TEXT,                        -- Лінк на головну картинку лоту (оригінальна якість з CDN OLX)
        has_ban_word INTEGER DEFAULT 0,        -- Прапорець сміття: 1 якщо знайдено бан-ворд (дефекти/ремонт), 0 якщо чисто

        -- ДАНІ ПРОДАВЦЯ (SELLER ANALYZER)
        seller_id TEXT,                        -- Цифровий ID профілю на OLX (потрібен для Delivery API)
        seller_name TEXT,                      -- Ім'я або нікнейм продавця
        seller_created_at TEXT,                -- Рік реєстрації акаунту на OLX (наприклад, '2019')
        seller_successful_deals INTEGER,       -- Точна кількість успішних угод через OLX Доставку
        seller_rating TEXT,                    -- Сирий рядок рейтингу з API (наприклад, '4.8/5.0 (25 оцінок)')
        seller_type TEXT,                      -- Аналітичний тип: 'private_person' (звичайний), 'reseller' (перекуп), 'shop' (магазин)
        seller_risk_score TEXT,                -- Рівень небезпеки: 'safe' (надійний), 'neutral' (нейтральний), 'suspicious' (підозрілий новорег/без оцінок)

        -- АНАЛІТИКА, ОЦІНКА ВАРТОСТІ ТА ВИГОДИ
        seller_price_clean INTEGER,            -- Очищена ціна продавця (без копійок та зайвих символів для калькуляцій)
        gpu_detected TEXT,                     -- Модель відеокарти, яку нейронка/оцінювач розпізнав у готовому ПК
        cpu_detected TEXT,                     -- Модель процесора, яку оцінювач розпізнав у готовому ПК
        gpu_market_price INTEGER,              -- Ринкова ціна знайденої відяхи (вирахована за 33-м перцентилем)
        cpu_market_price INTEGER,              -- Ринкова ціна знайденого проца (вирахована за 33-м перцентилем)
        estimated_fair_price INTEGER,          -- Справедлива собівартість деталей ПК (сума ринкових цін комплектуючих + дефолти)
        competitor_price INTEGER,              -- Середня ціна точно таких самих готових збірок-конкурентів на OLX прямо зараз
        saving_uah INTEGER,                    -- Чиста вигода в гривнях (Справедлива ціна деталей мінус ціна продавця)
        saving_percent INTEGER,                -- Вигода у відсотках відносно середнього ринку деталей
        deal_status TEXT DEFAULT 'unknown',    -- Вердикт для перекупа: 'super', 'good', 'neutral', 'overpriced', 'bad'
        evaluated_at TEXT                      -- Дата й час, коли оцінювач востаннє прораховував математику цього лоту
    );""")

    # 3. Створюємо таблицю component_prices (історія цін для аналітики)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS component_prices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        component_name TEXT NOT NULL,
        price INTEGER NOT NULL,
        date TEXT NOT NULL,          -- Формат: YYYY-MM-DD
        UNIQUE(component_name, date)  -- Захист від дублів цін на одну дату
    );
    """)

    cursor.execute("CREATE INDEX IF NOT EXISTS idx_ads_lookup ON ads(item_type, status, parsed_date);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_prices_history ON component_prices(component_name, date);")

    conn.commit()
    conn.close()
    print("[УСПІХ] Базу даних успішно створено, таблиці та індекси налаштовано!")

if __name__ == "__main__":
    init_db()
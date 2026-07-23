from __future__ import annotations

import json
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
if not (PROJECT_ROOT / "config.py").exists():
    PROJECT_ROOT = PROJECT_ROOT.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from config import DB_FILE, STATS_FILE

# 1. ЗАСТАРІЛЕ ЗАЛІЗО ТА СОКЕТИ
OBSOLETE_WORDS = [
    "athlon", "ddr2", "ddr1", "ddr 2", "ddr 1", "ddr-2", "ddr-1",
    "core2duo", "core 2 duo", "core 2duo", "f2a55m", "fm2a88", "fm2a85", "fm2a75", "fm2a68", "fm2a55",
    "athlon ii", "athlon x2", "athlon x4", "athlon x6", "athlon x8",
    "775", "lga775", "lga 775", "socket 775", "am2", "am2+", "am3", "am3+",
    "fm1", "fm2", "fm2+"
]

# 2. ОПТОВІ СЛОВА
WHOLESALE_WORDS = [
    "опт", "оптом", "склад", "пачка", "пачкою", "партией", "партія", 
    "комплектом", "кілька шт", "несколько шт", "розпродаж офісу", "распродажа офиса"
]

# 3. БРЕНДОВІ СИСТЕМНИКИ / НЕТТОПИ
BRAND_WORDS = [
    "dell", "optiplex", "hp", "prodesk", "elitedesk", "workstation",
    "lenovo", "thinkcentre", "fujitsu", "esprimo", "acer veriton"
]

# 4. ІГРОВІ МАРКЕРИ
GAMING_WORDS = [
    "ігровий", "игровой", "gaming", "rtx", "gtx", "rx 5", "rx 6", "rx 7", "rx 4", 
    "геймерский", "геймерський", "ігровий пк", "игровой пк"
]

MAINING_WORDS = [
    "майнинг", "майнінг"
]

def get_db_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_FILE)
    conn.execute("PRAGMA journal_mode=WAL;")
    return conn


def detect_pc_category(text: str) -> str:
    """Визначає категорію ПК на основі аналізу тексту."""
    if not text:
        return "home_office"

    lowered = text.lower()

    if any(word in lowered for word in OBSOLETE_WORDS):
        return "obsolete"
    if any(word in lowered for word in WHOLESALE_WORDS):
        return "wholesale"
    if any(word in lowered for word in BRAND_WORDS):
        return "brand_office"
    if any(word in lowered for word in GAMING_WORDS):
        return "gaming"
    if any(word in lowered for word in MAINING_WORDS):
            return "maining"

    return "home_office"


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
            "parsing": {"parsed_total_new": 0, "duplicates_skipped": 0},
            "filtering": {"defects_found": 0, "filtered_total_active": 0},
            "categories": {},
            "market_analysis": {"avg_ad_price_uah": 0, "min_price_today": 0, "max_price_today": 0},
        }

    if section in stats[today_str]:
        stats[today_str][section].update(metrics)

    STATS_FILE.write_text(json.dumps(stats, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> None:
    if not DB_FILE.exists():
        print("[ПОМИЛКА] Базу даних не знайдено!")
        return

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("ALTER TABLE ads ADD COLUMN pc_category TEXT DEFAULT 'uncategorized';")
        conn.commit()
    except sqlite3.OperationalError:
        pass

    cursor.execute("""
        SELECT id, title, description 
        FROM ads 
        WHERE item_type = 'pc' 
          AND status = 'active'
          AND (pc_category = 'uncategorized' OR pc_category IS NULL)
    """)
    unfiltered_pcs = cursor.fetchall()

    if not unfiltered_pcs:
        print("[INFO] Немає нових ПК для категоризації.")
        conn.close()
        return

    print(f"[CATEGORY] Знайдено {len(unfiltered_pcs)} нових ПК для розподілу по категоріям...")

    category_counts = {
        "obsolete": 0,
        "wholesale": 0,
        "brand_office": 0,
        "gaming": 0,
        "home_office": 0,
    }

    updates_pool = []

    for db_id, title, description in unfiltered_pcs:
        full_text = f"{title or ''} {description or ''}"
        category = detect_pc_category(full_text)

        category_counts[category] += 1
        updates_pool.append((category, db_id))

    if updates_pool:
        cursor.executemany("""
            UPDATE ads 
            SET pc_category = ? 
            WHERE id = ?
        """, updates_pool)
        conn.commit()

    print("\n✅ [УСПІХ] Розподіл по категоріям завершено:")
    print(f" 🗑️  Застарілі (obsolete):     {category_counts['obsolete']} шт.")
    print(f" 📦 Оптові (wholesale):      {category_counts['wholesale']} шт.")
    print(f" 🏢 Брендові (brand_office): {category_counts['brand_office']} шт.")
    print(f" 🎮 Ігрові (gaming):          {category_counts['gaming']} шт.")
    print(f" 🖥️  Домашні (home_office):   {category_counts['home_office']} шт.")

    # Рахуємо загальну кількість чистих ПК (без дефектів та не застарілих)
    cursor.execute("""
        SELECT COUNT(*) FROM ads 
        WHERE item_type = 'pc' 
          AND status = 'active' 
          AND (has_defects = 0 OR has_defects IS NULL) 
          AND pc_category != 'obsolete'
    """)
    active_clean_total = cursor.fetchone()[0]

    update_statistics("filtering", {
        "filtered_total_active": active_clean_total,
    })
    update_statistics("categories", category_counts)

    conn.close()


if __name__ == "__main__":
    main()
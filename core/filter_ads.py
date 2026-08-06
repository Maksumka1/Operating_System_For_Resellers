import os
import json
import sys
import asyncio
from datetime import datetime, timezone
from pathlib import Path
from collections import defaultdict
from dotenv import load_dotenv
from supabase import create_client, Client

PROJECT_ROOT = Path(__file__).resolve().parent
if not (PROJECT_ROOT / "config.py").exists():
    PROJECT_ROOT = PROJECT_ROOT.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from config import STATS_FILE
load_dotenv(PROJECT_ROOT / ".env")

SUPABASE_URL = os.getenv("SUPABASE_URL", "https://nfhtmfhckctuyhfolhou.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_SECRET_KEY") or os.getenv("SUPABASE_PUBLISHABLE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY or "")


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
    "комплектом", "кілька шт", "несколько шт", "розпродаж офісу", "рас распродажа офиса"
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
    "майнинг", "майнінг", "майнер", "майнит"
]


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


async def update_statistics_async(section: str, metrics: dict) -> None:
    def _file_io():
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

    await asyncio.to_thread(_file_io)


async def main_async(db_lock: asyncio.Lock | None = None) -> None:
    """Головний асинхронний метод для оркестратора."""
    def _fetch_unfiltered_pcs():
        try:
            response = supabase.table("ads") \
                .select("ad_id, title, description") \
                .eq("item_type", "pc") \
                .eq("status", "active") \
                .or_("pc_category.eq.uncategorized,pc_category.is.null") \
                .execute()
            return response.data or []
        except Exception as e:
            print(f"❌ [SUPABASE ERROR]: {e}")
            return []

    unfiltered_pcs = await asyncio.to_thread(_fetch_unfiltered_pcs)

    if not unfiltered_pcs:
        print("[INFO] Немає нових ПК для категоризації.")
        return

    print(f"[CATEGORY] Знайдено {len(unfiltered_pcs)} нових ПК для розподілу по категоріях...")

    category_counts = {
        "obsolete": 0, "wholesale": 0, "brand_office": 0,
        "gaming": 0, "home_office": 0, "maining": 0
    }

    ids_by_category = defaultdict(list)

    for pc in unfiltered_pcs:
        db_id = pc["ad_id"]
        title = pc.get("title") or ""
        description = pc.get("description") or ""
        
        full_text = f"{title} {description}"
        category = detect_pc_category(full_text)

        category_counts[category] += 1
        ids_by_category[category].append(db_id)

    def _update_categories():
        updated_total = 0
        for category, ids in ids_by_category.items():
            if not ids:
                continue
            chunk_size = 100
            for i in range(0, len(ids), chunk_size):
                batch_ids = ids[i : i + chunk_size]
                supabase.table("ads") \
                    .update({"pc_category": category}) \
                    .in_("ad_id", batch_ids) \
                    .execute()
                updated_total += len(batch_ids)
        print(f"✅ Успішно оновлено категорії для {updated_total} ПК")

    try:
        if db_lock:
            async with db_lock:
                await asyncio.to_thread(_update_categories)
        else:
            await asyncio.to_thread(_update_categories)
    except Exception as e:
        print(f"❌ [ПОМИЛКА ЗБЕРЕЖЕННЯ КАТЕГОРІЙ В SUPABASE]: {e}")

    print("\n [УСПІХ] Розподіл по категоріям завершено:")
    print(f"   Застарілі (obsolete):     {category_counts['obsolete']} шт.")
    print(f"  Оптові (wholesale):      {category_counts['wholesale']} шт.")
    print(f"  Брендові (brand_office): {category_counts['brand_office']} шт.")
    print(f"  Ігрові (gaming):          {category_counts['gaming']} шт.")
    print(f"   Домашні (home_office):   {category_counts['home_office']} шт.")
    print(f"   Майнінг (maining):       {category_counts['maining']} шт.")

    def _fetch_active_clean_total():
        try:
            active_res = supabase.table("ads") \
                .select("ad_id", count="exact") \
                .eq("item_type", "pc") \
                .eq("status", "active") \
                .eq("has_defects", 0) \
                .neq("pc_category", "obsolete") \
                .execute()
            return active_res.count or 0
        except Exception:
            return 0

    active_clean_total = await asyncio.to_thread(_fetch_active_clean_total)

    await update_statistics_async("filtering", {
        "filtered_total_active": active_clean_total,
    })
    await update_statistics_async("categories", category_counts)


def main() -> None:
    """Точка входу для ручного запуску з консолі."""
    asyncio.run(main_async())


if __name__ == "__main__":
    main()
import os
import json
import re
import sys
from pathlib import Path
from dotenv import load_dotenv
from supabase import create_client, Client

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

load_dotenv(PROJECT_ROOT / ".env")

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SECRET_KEY") or os.getenv("SUPABASE_PUBLISHABLE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY or "")

JSON_PATH = PROJECT_ROOT / "data" / "parsed_gpus.json"


def normalize_gpu_slug(raw_name: str) -> str:
    """Генерує чистий slug без сміття для збігу з Matcher та Evaluator (наприклад, gtx_1060_3gb)."""
    clean = raw_name.lower()
    clean = re.sub(r"\b(nvidia|geforce|amd|radeon|intel|arc|graphics)\b", "", clean)
    clean = re.sub(r"\b(rev|revision|oem|edition)\b.*", "", clean)
    clean = re.sub(r"[^a-z0-9]+", "_", clean).strip("_")
    return clean


def parse_memory(memory_str: str) -> tuple[float, str, int]:
    if not memory_str:
        return 0.0, "", 0

    parts = [p.strip() for p in memory_str.split("/")]
    
    # 1. Розмір VRAM у GB
    vram_gb = 0.0
    if len(parts) >= 1:
        size_part = parts[0].lower()
        match_gb = re.search(r"(\d+\.?\d*)\s*gb", size_part)
        match_mb = re.search(r"(\d+)\s*mb", size_part)
        if match_gb:
            vram_gb = float(match_gb.group(1))
        elif match_mb:
            vram_gb = round(float(match_mb.group(1)) / 1024.0, 2)

    # 🛡️ Захист від аномальних значень > 512 GB
    if vram_gb > 512.0:
        vram_gb = 0.0

    # 2. Тип пам'яті (GDDR5, DDR4, GDDR6X)
    vram_type = parts[1] if len(parts) >= 2 else ""

    # 3. Шина у бітах
    bus_width = 0
    if len(parts) >= 3:
        match_bit = re.search(r"(\d+)", parts[2])
        if match_bit:
            bus_width = int(match_bit.group(1))

    return round(vram_gb, 2), vram_type, bus_width


def parse_clock(clock_str: str) -> int:
    """Витягує частоту в MHz ('1468 MHz')."""
    if not clock_str:
        return 0
    match = re.search(r"(\d+)", str(clock_str))
    return int(match.group(1)) if match else 0


def parse_year(date_str: str) -> int | None:
    """Витягує рік випуску ('May 17th, 2017')."""
    if not date_str:
        return None
    match = re.search(r"\b(19\d{2}|20\d{2})\b", str(date_str))
    return int(match.group(1)) if match else None


def is_desktop_consumer_gpu(item: dict) -> bool:
    """Фільтрує мобільні (ноутбучні), серверні та впаяні карти."""
    gpu_name = item.get("gpu", "")
    
    # Ігноруємо мобільні (M / Mobile / Max-Q)
    if any(ignore in gpu_name for ignore in ["Mobile", "Max-Q", "MX110", "MX130", "MX150", "MX230", "MX250"]):
        return False
        
    return True


def main():
    if not JSON_PATH.exists():
        print(f"❌ Файл JSON не знайдено за шляхом: {JSON_PATH}")
        print("💡 Поклади свій спарсений JSON у папку 'data/parsed_gpus.json'")
        return

    print(f"📂 Завантаження {JSON_PATH}...")
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        raw_data = json.load(f)

    print(f"📊 Всього моделей у сирому JSON: {len(raw_data)}")

    deduplicated_records: dict[str, dict] = {}
    skipped_count = 0

    for item in raw_data:
        if not is_desktop_consumer_gpu(item):
            skipped_count += 1
            continue

        raw_name = item.get("gpu", "").strip()
        if not raw_name:
            continue

        slug = normalize_gpu_slug(raw_name)
        if not slug:
            continue

        # Визначаємо бренд
        raw_lower = raw_name.lower()
        if any(k in raw_lower for k in ["radeon", "rx", "hd ", "r7", "r9", "r5", "vega"]):
            brand = "AMD"
        elif "arc" in raw_lower or "iris" in raw_lower:
            brand = "Intel"
        else:
            brand = "NVIDIA"

        vram_gb, vram_type, bus_width = parse_memory(item.get("memory", ""))
        gpu_clk = parse_clock(item.get("gpu_clock", ""))
        mem_clk = parse_clock(item.get("memory_clock", ""))
        rel_year = parse_year(item.get("released", ""))

        record = {
            "slug": slug,
            "raw_name": raw_name,
            "brand": brand,
            "chip": item.get("chip"),
            "bus": item.get("bus"),
            "vram_size_gb": vram_gb,
            "vram_type": vram_type,
            "bus_width_bit": bus_width,
            "gpu_clock_mhz": gpu_clk,
            "memory_clock_mhz": mem_clk,
            "shading_units": item.get("shading_units"),
            "released_year": rel_year,
            "techpowerup_url": item.get("url")
        }

        # Дедуплікація в пам'яті
        deduplicated_records[slug] = record



    found_5060 = [r for r in deduplicated_records.values() if "5060" in r["raw_name"].lower()]
    print(f"🔍 Знайдено 5060 у підготовленому списку ({len(found_5060)} шт.):")
    for f in found_5060:
        print(" -", f["raw_name"], "---> slug:", f["slug"])
    
    records_to_upsert = list(deduplicated_records.values())

    print(f"🧹 Профільтровано: відсієно {skipped_count} мобільних/неактуальних моделей.")
    print(f"✅ Підготовлено {len(records_to_upsert)} унікальних десктопних відеокарт до імпорту.")

    if records_to_upsert:
        print("\n💾 Збереження у Supabase (таблиця gpu_specs)...")
        chunk_size = 100
        imported_count = 0
        try:
            for i in range(0, len(records_to_upsert), chunk_size):
                chunk = records_to_upsert[i : i + chunk_size]
                supabase.table("gpu_specs").upsert(chunk, on_conflict="slug").execute()
                imported_count += len(chunk)
                print(f" └─ Завантажено {imported_count}/{len(records_to_upsert)}...")

            print(f"\n🎉 [УСПІХ] Базу специфікацій відеокарт оновлено! Успішно завантажено {imported_count} лотів.")
        except Exception as e:
            print(f"❌ [ПОМИЛКА ЗБЕРЕЖЕННЯ В SUPABASE]: {e}")


if __name__ == "__main__":
    main()
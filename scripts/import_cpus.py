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

SUPABASE_URL = os.getenv("SUPABASE_URL", "https://nfhtmfhckctuyhfolhou.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_SECRET_KEY") or os.getenv("SUPABASE_PUBLISHABLE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY or "")

JSON_PATH = PROJECT_ROOT / "data" / "parsed_cpus.json"


def normalize_slug(raw_name: str) -> str:
    """Генерує чистий slug (без префікса cpu_) для збігу з ключами в config.py."""
    clean = raw_name.lower()
    clean = re.sub(r"\b(intel|amd|core|processor|cpu)\b", "", clean)
    clean = re.sub(r"[^a-z0-9]+", "_", clean).strip("_")
    return clean


def parse_cores_threads(val: str) -> tuple[int, int]:
    if not val:
        return 0, 0
    nums = [int(n) for n in re.findall(r"\d+", str(val))]
    if len(nums) >= 2:
        return nums[0], nums[1]
    if len(nums) == 1:
        return nums[0], nums[0]
    return 0, 0


def parse_clock(val: str) -> tuple[float, float]:
    if not val:
        return 0.0, 0.0
    val_lower = str(val).lower()
    nums = [float(n) for n in re.findall(r"\d+\.?\d*", val_lower)]
    
    if "mhz" in val_lower:
        nums = [n / 1000.0 for n in nums]

    if len(nums) >= 2:
        return min(nums), max(nums)
    if len(nums) == 1:
        return nums[0], nums[0]
    return 0.0, 0.0


def parse_tdp(val: str) -> int:
    if not val:
        return 0
    match = re.search(r"(\d+)", str(val))
    return int(match.group(1)) if match else 0


def parse_cache(val: str) -> float:
    if not val:
        return 0.0
    val_lower = str(val).lower()
    match = re.search(r"(\d+\.?\d*)", val_lower)
    if not match:
        return 0.0
    num = float(match.group(1))
    if "kb" in val_lower:
        num = num / 1024.0
    return round(num, 1)


def parse_year(val: str) -> int | None:
    if not val:
        return None
    match = re.search(r"\b(19\d{2}|20\d{2})\b", str(val))
    return int(match.group(1)) if match else None


def is_desktop_consumer_gpu(item: dict) -> bool:
    gpu_name = item.get("gpu", "")
    socket = item.get("socket", "")

    if "BGA" in socket.upper() or gpu_name.startswith("Atom"):
        return False

    if any(ignore in gpu_name for ignore in ["Mobile", "Embedded"]):
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
    skipped_bga = 0

    for item in raw_data:
        if not is_desktop_consumer_gpu(item):
            skipped_bga += 1
            continue

        raw_name = item.get("gpu", "").strip()
        if not raw_name:
            continue

        slug = normalize_slug(raw_name)
        if not slug:
            continue

        brand = "AMD" if any(k in raw_name.lower() for k in ["ryzen", "athlon", "threadripper", "fx-"]) else "Intel"
        cores, threads = parse_cores_threads(item.get("cores_threads"))
        base_clock, boost_clock = parse_clock(item.get("clock"))

        record = {
            "slug": slug,
            "raw_name": raw_name,
            "brand": brand,
            "family": item.get("model"),
            "architecture": item.get("model"),
            "cores": cores,
            "threads": threads,
            "base_clock_ghz": base_clock,
            "boost_clock_ghz": boost_clock,
            "socket": item.get("socket"),
            "process_nm": item.get("process"),
            "l3_cache_mb": parse_cache(item.get("l3_cache")),
            "tdp_w": parse_tdp(item.get("tdp")),
            "released_year": parse_year(item.get("released")),
            "techpowerup_url": item.get("url")
        }

        deduplicated_records[slug] = record

    records_to_upsert = list(deduplicated_records.values())

    print(f"🧹 Профільтровано: відсієно {skipped_bga} BGA/ноутбучних/неактуальних моделей.")
    print(f"✅ Підготовлено {len(records_to_upsert)} унікальних десктопних процесорів до імпорту.")

    if records_to_upsert:
        print("\n💾 Збереження у Supabase (таблиця cpu_specs)...")
        chunk_size = 100
        imported_count = 0
        try:
            for i in range(0, len(records_to_upsert), chunk_size):
                chunk = records_to_upsert[i : i + chunk_size]
                supabase.table("cpu_specs").upsert(chunk, on_conflict="slug").execute()
                imported_count += len(chunk)
                print(f" └─ Завантажено {imported_count}/{len(records_to_upsert)}...")

            print(f"\n🎉 [УСПІХ] Базу специфікацій оновлено! Успішно завантажено {imported_count} процесорів.")
        except Exception as e:
            print(f"❌ [ПОМИЛКА ЗБЕРЕЖЕННЯ В SUPABASE]: {e}")


if __name__ == "__main__":
    main()
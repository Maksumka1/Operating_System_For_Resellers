"""
PC Competitor Finder — Прямий пошук по CPU / GPU
"""

import os
import sys
import asyncio
import logging
from collections import defaultdict
from pathlib import Path
from typing import Any, List, Optional
from dotenv import load_dotenv
from supabase import create_client

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] — %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)

project_root = Path(__file__).resolve().parent
if not (project_root / ".env").exists():
    project_root = project_root.parent
load_dotenv(project_root / ".env")

SUPABASE_URL = os.getenv("SUPABASE_URL", "").strip()
SUPABASE_KEY = os.getenv("SUPABASE_SECRET_KEY", "").strip()

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("Відсутні SUPABASE_URL або SUPABASE_SECRET_KEY у .env")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


def clean_val(val: str | None) -> str | None:
    if not val:
        return None
    v = str(val).strip()
    if not v or "unknown" in v.lower() or "невідомо" in v.lower() or v.lower() == "null":
        return None
    return v


async def fetch_all_ads() -> list[dict]:
    """Завантажує всі активні ПК з бази частинами по 1000 шт."""
    all_rows = []
    offset = 0
    limit = 1000

    while True:
        resp = await asyncio.to_thread(
            lambda: supabase.table("ads")
            .select("ad_id, cpu_detected, gpu_detected, price")
            .eq("item_type", "pc")
            .eq("status", "active")
            .eq("has_defects", 0)
            .gt("price", 1000)
            .range(offset, offset + limit - 1)
            .execute()
        )
        rows = resp.data or []
        all_rows.extend(rows)
        if len(rows) < limit:
            break
        offset += limit

    return all_rows


async def main_async(db_lock: Optional[asyncio.Lock] = None, **kwargs: Any) -> List[int]:
    """Головна асинхронна функція для запуску з оркестратора."""
    logger.info("Завантажуємо всі ПК з бази даних...")
    ads = await fetch_all_ads()
    if not ads:
        logger.info("Оголошень не знайдено.")
        return []

    logger.info(f"Завантажено {len(ads)} оголошень. Групуємо...")

    # Словники для прямого пошуку
    by_cpu = defaultdict(list)
    by_gpu = defaultdict(list)

    cleaned_ads = []
    for ad in ads:
        cpu = clean_val(ad.get("cpu_detected"))
        gpu = clean_val(ad.get("gpu_detected"))
        item = {
            "ad_id": ad["ad_id"],
            "price": int(ad["price"]),
            "cpu": cpu,
            "gpu": gpu,
        }
        cleaned_ads.append(item)

        if cpu:
            by_cpu[cpu].append(item)
        if gpu:
            by_gpu[gpu].append(item)

    # Збираємо конкурентів для кожного ПК
    grouped_updates = defaultdict(list)
    all_updated_ids: List[int] = []

    for item in cleaned_ads:
        ad_id = item["ad_id"]
        cpu = item["cpu"]
        gpu = item["gpu"]

        if cpu:
            # Всі інші ПК з ТАКИМ САМИМ процесором
            matches = [m for m in by_cpu[cpu] if m["ad_id"] != ad_id]
        elif gpu:
            # Всі інші ПК з ТАКОЮ САМОЮ відеокартою
            matches = [m for m in by_gpu[gpu] if m["ad_id"] != ad_id]
        else:
            matches = []

        if matches:
            prices = [m["price"] for m in matches]
            avg_price = int(sum(prices) / len(prices))
            competitor_ids = [m["ad_id"] for m in matches]
        else:
            avg_price = item["price"]
            competitor_ids = []

        # Групуємо для безпечного батч-оновлення
        payload_key = (avg_price, tuple(sorted(competitor_ids)))
        grouped_updates[payload_key].append(ad_id)

    logger.info(f"Оновлюємо базу даних ({len(grouped_updates)} унікальних груп)...")

    batch_size = 100

    for (avg_price, comp_ids_tuple), ad_ids in grouped_updates.items():
        payload = {
            "competitor_price": avg_price,
            "competitor_ids": list(comp_ids_tuple),
        }

        for i in range(0, len(ad_ids), batch_size):
            batch = ad_ids[i : i + batch_size]
            try:
                if db_lock:
                    async with db_lock:
                        await asyncio.to_thread(
                            lambda: supabase.table("ads")
                            .update(payload)
                            .in_("ad_id", batch)
                            .execute()
                        )
                else:
                    await asyncio.to_thread(
                        lambda: supabase.table("ads")
                        .update(payload)
                        .in_("ad_id", batch)
                        .execute()
                    )
                all_updated_ids.extend(batch)
            except Exception as exc:
                logger.error(f"Помилка оновлення: {exc}")

    logger.info(f"✅ Успішно оновлено {len(all_updated_ids)} оголошень у базі.")
    return all_updated_ids


# Аліас для зворотної сумісності
run = main_async


def main():
    if sys.platform == "win32":
        asyncio.run(main_async(), loop_factory=asyncio.SelectorEventLoop)
    else:
        asyncio.run(main_async())


if __name__ == "__main__":
    main()
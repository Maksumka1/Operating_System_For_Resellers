import os
import asyncio
import sys
import time
from datetime import datetime, timezone
from dotenv import load_dotenv
from pathlib import Path

from curl_cffi.requests import AsyncSession
from supabase import create_client, Client

PROJECT_ROOT = Path(__file__).resolve().parent
if not (PROJECT_ROOT / "config.py").exists():
    PROJECT_ROOT = PROJECT_ROOT.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

load_dotenv(PROJECT_ROOT / ".env")

SUPABASE_URL = os.getenv("SUPABASE_URL", "https://nfhtmfhckctuyhfolhou.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_SECRET_KEY") or os.getenv("SUPABASE_PUBLISHABLE_KEY")
OLX_PROXY_URL = os.getenv("OLX_PROXY_URL") or None

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY or "")

# Налаштування швидкості
CONCURRENT_REQUESTS = 25  # Паралельні асинхронні запити
TIMEOUT = 8               # Таймаут на перевірку 1 оголошення

HEADERS = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "accept-language": "uk-UA,uk;q=0.9,en-US;q=0.8,en;q=0.7",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
}

processed_counter = 0
counter_lock = asyncio.Lock()


async def check_single_url(
    session: AsyncSession,
    ad_id: int,
    url: str,
    semaphore: asyncio.Semaphore,
    total_count: int,
) -> tuple[int, str]:
    global processed_counter
    async with semaphore:
        full_url = url if url.startswith("http") else f"https://www.olx.ua{url}"
        
        try:
            resp = await session.get(full_url, allow_redirects=True, timeout=TIMEOUT)
            final_url = str(resp.url).lower()
            status_code = resp.status_code

            status = "active"

            # 1. Перевірка на 404 / 410
            if status_code in (404, 410):
                status = "deactivated"
                print(f"🔴 [ID {ad_id}] Деактивовано (HTTP {status_code}) -> {full_url}")

            # 2. Перевірка на редірект в архів чи категорію
            elif "arkhiv" in final_url or "archive" in final_url:
                status = "deactivated"
                print(f"🔴 [ID {ad_id}] Перенаправлено в Архів -> {final_url}")
            elif "/obyavlenie/" not in final_url and "/d/uk/obyavlenie/" not in final_url:
                status = "deactivated"
                print(f"🔴 [ID {ad_id}] Перенаправлено на сторінку категорії -> {final_url}")

        except Exception as e:
            status = "active"
            print(f"⚠️ [ID {ad_id}] Збій мережі ({e}). Залишено активним.")

        async with counter_lock:
            processed_counter += 1
            if processed_counter % 50 == 0 or processed_counter == total_count:
                percent = (processed_counter / total_count) * 100
                print(f"⏳ Прогрес перевірки архіву: {processed_counter}/{total_count} ({percent:.1f}%)")

        return ad_id, status


async def main_async(db_lock: asyncio.Lock | None = None) -> None:
    """Головна асинхронна точка входу для оркестратора."""
    global processed_counter
    processed_counter = 0
    today_str = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M")
    print(f"\n🚀 [ARCHIVE] СТАРТ ПЕРЕВІРКИ СТАТУСІВ REDIRECT ({today_str})")

    def _fetch_active_ads():
        try:
            response = (
                supabase.table("ads")
                .select("ad_id, url")
                .eq("status", "active")
                .not_.is_("ad_id", "null")
                .execute()
            )
            return response.data or []
        except Exception as e:
            print(f"❌ [SUPABASE ERROR]: Помилка читання з БД: {e}")
            return []

    active_ads = await asyncio.to_thread(_fetch_active_ads)

    if not active_ads:
        print("ℹ️ [INFO] Немає активних оголошень для перевірки архіву.")
        return

    print(f"📡 Знайдено активних оголошень для перевірки: {len(active_ads)}")
    start_time = time.time()

    semaphore = asyncio.Semaphore(CONCURRENT_REQUESTS)
    proxy_kwargs = {"proxies": {"http": OLX_PROXY_URL, "https": OLX_PROXY_URL}} if OLX_PROXY_URL else {}

    async with AsyncSession(headers=HEADERS, impersonate="chrome120", **proxy_kwargs) as session:
        print("🔥 Прогріваємо сесію...")
        try:
            warmup = await session.get("https://www.olx.ua/", timeout=5)
            print(f"🔥 Прогрів завершено (HTTP {warmup.status_code})")
        except Exception as e:
            print(f"⚠️ Прогрів пропущено: {e}")

        total = len(active_ads)
        tasks = [
            check_single_url(session, ad["ad_id"], ad["url"], semaphore, total)
            for ad in active_ads
        ]
        
        print(f"⚡ Перевіряємо {total} URL у {CONCURRENT_REQUESTS} паралельних потоків...\n")
        results = await asyncio.gather(*tasks)

    deactivated_ids = [ad_id for ad_id, status in results if status == "deactivated"]
    elapsed = time.time() - start_time

    print("\n--- 📊 РЕЗУЛЬТАТИ ПЕРЕВІРКИ АРХІВУ ---")
    print(f"🔹 Всього перевірено: {len(results)}")
    print(f"🟢 Активні: {len(results) - len(deactivated_ids)}")
    print(f"🔴 Деактивовані / Архів: {len(deactivated_ids)}")
    print(f"⏱️ Тривалість перевірки: {elapsed:.2f} сек")

    if deactivated_ids:
        print(f"\n💾 Оновлюємо {len(deactivated_ids)} деактивованих лотів у Supabase...")

        def _update_deactivated():
            chunk_size = 100
            for i in range(0, len(deactivated_ids), chunk_size):
                batch = deactivated_ids[i : i + chunk_size]
                supabase.table("ads").update({
                    "status": "deactivated",
                    "deactivated_at": today_str
                }).in_("ad_id", batch).execute()
                print(f"  └─ Позначено деактивованими: {len(batch)} шт.")

        try:
            if db_lock:
                async with db_lock:
                    await asyncio.to_thread(_update_deactivated)
            else:
                await asyncio.to_thread(_update_deactivated)

            print("✅ [УСПІХ] Усі закриті лоти успішно замарковано у базі даних!")
        except Exception as e:
            print(f"❌ [ПОМИЛКА ОНОВЛЕННЯ SUPABASE]: {e}")
    else:
        print("ℹ️ [INFO] Усі оголошення досі активні на OLX.")


def main() -> None:
    """Точка входу для ручного запуску з консолі."""
    asyncio.run(main_async())


if __name__ == "__main__":
    main()
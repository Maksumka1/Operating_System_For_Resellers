import os
from collections import defaultdict
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

supabase = create_client(
    os.getenv("SUPABASE_URL", "").strip(),
    os.getenv("SUPABASE_SECRET_KEY", "").strip(),
)


def clean_val(val: str | None) -> str | None:
    if not val:
        return None
    v = str(val).strip()
    return None if v.lower() in ("unknown", "невідомо", "null", "") else v


def process_latest_100_ads():
    print("1. Отримуємо всі активні ПК для бази порівняння...")
    # Отримуємо пул активних оголошень для швидкого пошуку в пам'яті
    all_ads_resp = (
        supabase.table("ads")
        .select("ad_id, cpu_detected, gpu_detected")
        .execute()
    )
    all_ads = all_ads_resp.data or []

    # Індексуємо для миттєвого пошуку O(1)
    by_cpu = defaultdict(list)
    by_gpu = defaultdict(list)

    for ad in all_ads:
        cpu = clean_val(ad.get("cpu_detected"))
        gpu = clean_val(ad.get("gpu_detected"))
        ad_id = ad["ad_id"]

        if cpu:
            by_cpu[cpu].append(ad_id)
        if gpu:
            by_gpu[gpu].append(ad_id)

    print(f"Всього активних оголошень для порівняння: {len(all_ads)}")

    # 2. Отримуємо 100 найновіших активних оголошень
    print("2. Отримуємо всі найновіші активні оголошення...")
    targets_resp = (
        supabase.table("ads")
        .select("ad_id, title, cpu_detected, gpu_detected")
        .eq("status", "active")
        .order("ad_id", desc=True)  # або "created_at", якщо є таке поле
        .execute()
    )
    target_ads = targets_resp.data or []

    if not target_ads:
        print("Активних оголошень не знайдено.")
        return

    print(f"Знайдено {len(target_ads)} оголошень для обробки. Шукаємо конкурентів...")

    # 3. Формуємо списки конкурентів та групуємо для батч-оновлення
    grouped_updates = defaultdict(list)

    for ad in target_ads:
        ad_id = ad["ad_id"]
        cpu = clean_val(ad.get("cpu_detected"))
        gpu = clean_val(ad.get("gpu_detected"))

        if cpu:
            # Шукаємо за CPU, виключаючи саме оголошення
            comp_ids = [m_id for m_id in by_cpu[cpu] if m_id != ad_id]
        elif gpu:
            # Якщо CPU немає — шукаємо за GPU
            comp_ids = [m_id for m_id in by_gpu[gpu] if m_id != ad_id]
        else:
            comp_ids = []

        # Групуємо однакові списки ID для масового оновлення
        payload_key = tuple(sorted(comp_ids))
        grouped_updates[payload_key].append(ad_id)

    # 4. Записуємо пачками в базу через .update()
    print(f"3. Оновлюємо базу даних ({len(grouped_updates)} унікальних груп)...")
    updated_count = 0
    batch_size = 50

    for comp_ids_tuple, ad_ids in grouped_updates.items():
        payload = {"competitor_ids": list(comp_ids_tuple)}

        for i in range(0, len(ad_ids), batch_size):
            batch = ad_ids[i : i + batch_size]
            try:
                (
                    supabase.table("ads")
                    .update(payload)
                    .in_("ad_id", batch)
                    .execute()
                )
                updated_count += len(batch)
            except Exception as e:
                print(f"❌ Помилка оновлення для батчу: {e}")

    print(f"\n✅ Готово! Успішно оновлено `competitor_ids` для {updated_count} оголошень.")


if __name__ == "__main__":
    process_latest_100_ads()
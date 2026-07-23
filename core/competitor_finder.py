import sys
import sqlite3
from pathlib import Path
from collections import Counter, defaultdict

PROJECT_ROOT = Path(__file__).resolve().parent
if not (PROJECT_ROOT / "config.py").exists():
    PROJECT_ROOT = PROJECT_ROOT.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from config import DB_FILE


def get_db_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_FILE)
    conn.execute("PRAGMA journal_mode=WAL;")
    return conn


def calculate_bucket_price(prices: list[int]) -> int:
    """Вираховує модальну (найбільш популярну) цінову зону для списку цін"""
    if not prices:
        return 0

    # Фільтруємо аномальні ціни (менше 100 грн та явно помилкові)
    valid_prices = [p for p in prices if p > 100]
    if not valid_prices:
        return 0

    max_p = max(valid_prices)
    min_p = min(valid_prices)

    # Динамічний крок кластеризації залежно від розкиду цін
    diff = max_p - min_p
    if diff < 1000:
        step = 100
    elif diff < 3000:
        step = 200
    else:
        step = 500

    ranges = []
    for price in valid_prices:
        bucket_start = (price // step) * step
        ranges.append(bucket_start + (step // 2))

    range_counts = Counter(ranges)
    best_bucket = range_counts.most_common(1)[0][0]
    
    return int(best_bucket)


def update_hardware_competitor_prices() -> None:
    """Прораховує ринкову ціну для ВСІХ типів комплектуючих за ОДИН асинхронний прохід"""
    conn = get_db_connection()
    cursor = conn.cursor()

    # 🎯 ОДИН запит: витягуємо ціни всіх активних деталей без дефектів
    cursor.execute("""
        SELECT component_name, price, id 
        FROM ads 
        WHERE item_type IN ('gpu', 'cpu', 'motherboard', 'psu', 'storage') 
          AND status = 'active' 
          AND (has_defects = 0 OR has_defects IS NULL)
          AND (seller_risk_score != 'suspicious' OR seller_risk_score IS NULL)
          AND price > 100
          AND component_name IS NOT NULL
    """)
    rows = cursor.fetchall()

    if not rows:
        print("[COMPETITORS] Активних комплектуючих для аналізу не знайдено.")
        conn.close()
        return

    # Групуємо ціни та ID оголошень за назвою компонента у пам'яті
    comp_prices = defaultdict(list)
    comp_ad_ids = defaultdict(list)

    for comp_name, price, ad_id in rows:
        comp_prices[comp_name].append(price)
        comp_ad_ids[comp_name].append(ad_id)

    print(f"[COMPETITORS] Аналізуємо ринкові ціни для {len(comp_prices)} унікальних моделей заліза...")

    updates = []
    for comp_name, prices in comp_prices.items():
        market_price = calculate_bucket_price(prices)
        if market_price > 0:
            for ad_id in comp_ad_ids[comp_name]:
                updates.append((market_price, ad_id))

    if updates:
        cursor.executemany("""
            UPDATE ads 
            SET competitor_price = ? 
            WHERE id = ?
        """, updates)
        conn.commit()
        print(f"✅ Комплектуючі оновлено! Розраховано середні ціни для {len(updates)} оголошень.")

    conn.close()


def update_pcs_competitor_prices() -> None:
    """Прораховує середню ціну конкурентів для всіх ПК зі схожою конфігурацією (CPU + GPU)"""
    conn = get_db_connection()
    cursor = conn.cursor()

    # 1. Отримуємо всі активні ПК з розпізнаними процесором та відеокартою
    cursor.execute("""
        SELECT id, gpu_detected, cpu_detected, price 
        FROM ads 
        WHERE item_type = 'pc' 
          AND status = 'active' 
          AND (has_defects = 0 OR has_defects IS NULL)
          AND gpu_detected IS NOT NULL 
          AND cpu_detected IS NOT NULL
          AND price > 1000
    """)
    all_pcs = cursor.fetchall()

    if not all_pcs:
        print("[COMPETITORS] Активних ПК з розпізнаним залізом немає.")
        conn.close()
        return

    # 2. Групуємо ціни за зв'язкою (gpu, cpu) в пам'яті Python (замість 1000 SQL запитів)
    build_prices = defaultdict(list)
    for ad_id, gpu, cpu, price in all_pcs:
        build_key = f"{gpu.lower()}_{cpu.lower()}"
        build_prices[build_key].append((price, ad_id))

    print(f"[COMPETITORS] Перераховуємо ціни конкурентів для {len(all_pcs)} ПК...")

    updates = []
    for build_key, items in build_prices.items():
        all_prices_for_build = [price for price, _ in items]
        
        # Якщо в категорії є хоча б 2+ комп'ютери
        for price, ad_id in items:
            # Беремо ціни інших ПК з такою ж конфігурацією
            other_prices = [p for p in all_prices_for_build if p != price]
            if not other_prices:
                other_prices = all_prices_for_build  # Якщо це єдиний ПК, беремо його ж ціну як базис

            avg_competitor_price = int(sum(other_prices) / len(other_prices))
            updates.append((avg_competitor_price, ad_id))

    if updates:
        cursor.executemany("""
            UPDATE ads 
            SET competitor_price = ? 
            WHERE id = ?
        """, updates)
        conn.commit()
        print(f"✅ Комп'ютери оновлено! Розраховано ціни конкурентів для {len(updates)} збірок.")

    conn.close()


def main():
    print("\n" + "="*50)
    print("📊 ЗАПУСК АНАЛІЗУ КОНКУРЕНТНОГО СЕРЕДОВИЩА")
    print("="*50)
    
    update_hardware_competitor_prices()
    update_pcs_competitor_prices()
    
    print("[УСПІХ] Повний аналіз ринку конкурентів завершено успішно!")


if __name__ == "__main__":
    main()
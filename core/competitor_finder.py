import sys
import sqlite3
from pathlib import Path
from collections import Counter

PROJECT_ROOT = Path(__file__).resolve().parent
if not (PROJECT_ROOT / "config.py").exists():
    PROJECT_ROOT = PROJECT_ROOT.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from config import DB_FILE


def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.execute("PRAGMA journal_mode=WAL;")
    return conn


def calculate_market_bucket_price(component_name: str) -> int:
    """Внутрішня функція: вираховує найбільш популярний ціновий діапазон ринку для залізяки"""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT price FROM ads 
        WHERE component_name = ? 
          AND status = 'active' 
          AND has_ban_word = 0 
          AND price > 100
          AND seller_risk_score = 'safe'
    """, (component_name,))
    
    prices = [row[0] for row in cursor.fetchall()]
    conn.close()

    if not prices:
        return 0

    max_price = max(prices)
    min_price = min(prices)

    # Динамічний крок кластеризації ринку
    step = 200 if max_price - min_price < 2000 else 400
    ranges = []
    for price in prices:
        bucket_start = (price // step) * step
        ranges.append(bucket_start + (step // 2))  # Беремо серединну ціну популярного бакету

    range_counts = Counter(ranges)
    best_bucket_price = range_counts.most_common(1)[0][0]
    
    return int(best_bucket_price)


def update_hardware_competitor_prices():
    """Прораховує та записує моду ринкової ціни для ВСІХ активних відеокарт та процесорів"""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Беремо всі унікальні активні моделі комплектуючих, що зараз є на ринку та від надійних продавців
    cursor.execute("""
        SELECT DISTINCT component_name FROM ads 
        WHERE item_type IN ('gpu', 'cpu') 
          AND status = 'active' 
          AND component_name IS NOT NULL
          AND seller_risk_score = 'safe'
    """)
    active_components = [row[0] for row in cursor.fetchall()]

    if not active_components:
        print("[COMPETITORS] Активних комплектуючих для аналізу не знайдено.")
        conn.close()
        return

    print(f"[COMPETITORS] Аналізуємо ринкові бакети для {len(active_components)} моделей заліза...")
    
    updates = []
    for comp_name in active_components:
        market_price = calculate_market_bucket_price(comp_name)
        if market_price > 0:
            # Знайдемо всі ID оголошень цієї моделі, щоб масово оновити їм ціну конкурента
            cursor.execute("""
                SELECT id FROM ads 
                WHERE component_name = ? AND status = 'active'
            """, (comp_name,))
            ad_ids = [row[0] for row in cursor.fetchall()]
            
            for ad_id in ad_ids:
                updates.append((market_price, ad_id))

    if updates:
        cursor.executemany("""
            UPDATE ads 
            SET competitor_price = ? 
            WHERE id = ?
        """, updates)
        conn.commit()
        print(f"✅ Комплектуючі оновлено! Розраховано прайсів для {len(updates)} карток заліза.")

    conn.close()


def update_pcs_competitor_prices():
    """Прораховує та ПЕРЕЗАПИСУЄ середню ціну конкурентів для ВСІХ активних ПК"""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Беремо абсолютно всі активні ПК в базі для динамічного перерахунку ринку
    cursor.execute("""
        SELECT id, title, gpu_detected, cpu_detected, price 
        FROM ads 
        WHERE item_type = 'pc' 
          AND status = 'active' 
          AND gpu_detected IS NOT NULL 
          AND cpu_detected IS NOT NULL
    """)
    pcs_to_analyze = cursor.fetchall()

    if not pcs_to_analyze:
        print("[COMPETITORS] Активних ПК в базі для аналізу ринку немає.")
        conn.close()
        return

    print(f"[COMPETITORS] Перераховуємо ціни конкурентів для {len(pcs_to_analyze)} активних ПК...")
    
    updates = []

    for ad_id, title, gpu, cpu, seller_price in pcs_to_analyze:
        # Шукаємо схожі збірки (такі ж CPU + GPU, крім цього ж оголошення)
        cursor.execute("""
            SELECT price FROM ads 
            WHERE item_type = 'pc' 
              AND status = 'active' 
              AND has_ban_word = 0
              AND gpu_detected = ? 
              AND cpu_detected = ?
              AND id != ?
              AND price > 1000
        """, (gpu, cpu, ad_id))
        
        comp_prices = [row[0] for row in cursor.fetchall()]

        if comp_prices:
            avg_competitor_price = int(sum(comp_prices) / len(comp_prices))
        else:
            avg_competitor_price = 0  # Якщо унікальний лот на ринку

        updates.append((avg_competitor_price, ad_id))

    if updates:
        cursor.executemany("""
            UPDATE ads 
            SET competitor_price = ? 
            WHERE id = ?
        """, updates)
        conn.commit()
        print(f"✅ Комп'ютери оновлено! Перераховано збірок: {len(updates)} шт.")

    conn.close()


def main():
    """Головна точка входу для оркестратора в main.py"""
    print("\n" + "="*50)
    print("📊 ЗАПУСК АНАЛІЗУ КОНКУРЕНТНОГО СЕРЕДОВИЩА")
    print("="*50)
    
    # 1. Оновлюємо прайси для відях та проців
    update_hardware_competitor_prices()
    
    # 2. Оновлюємо ринкові прайси схожих збірок для ПК
    update_pcs_competitor_prices()
    
    print("[УСПІХ] Повний аналіз ринку конкурентів завершено успішно!")


if __name__ == "__main__":
    main()
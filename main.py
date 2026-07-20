import sys
import time
import sqlite3
from datetime import datetime, timezone, timedelta
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
if not (PROJECT_ROOT / "config.py").exists():
    PROJECT_ROOT = PROJECT_ROOT.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from config import DB_FILE

# Імпортуємо модулі
try:
    import scripts.db_init as db_init
    import parsers.parser_hardware as parser_hardware
    import parsers.parser as parser
    import core.filter_ads as filter_ads
    import core.pc_evaluator as pc_evaluator
    import scripts.clean_archive as clean_archive
    import core.seller_analyzer as seller_analyzer
    import core.competitor_finder as competitor_finder
except ImportError as e:
    print(f"[ПОМИЛКА ІМПОРТУ] Переконайся, що всі скрипти лежать в одній папці: {e}")
    sys.exit(1)

def should_parse_hardware() -> bool:
    """
    Перевіряє, чи потрібно запускати парсинг комплектуючих.
    Повертає True, якщо в базі немає цін АБО остання ціна старіша за 7 днів.
    """
    if not DB_FILE.exists():
        return True

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT MAX(date) FROM component_prices")
        row = cursor.fetchone()
        
        if not row or not row[0]:
            print("[ORCHESTRATOR] База цін порожня. Потрібен повний парсинг заліза.")
            return True
            
        latest_date_str = row[0] 
        latest_date = datetime.strptime(latest_date_str, "%Y-%m-%d").replace(tzinfo=timezone.utc)
        today = datetime.now(timezone.utc)
        
        days_passed = (today - latest_date).days
        
        if days_passed >= 7:
            print(f"[ORCHESTRATOR] Ціни оновлювалися {days_passed} днів тому (>= 7). Запускаємо оновлення прайсів.")
            return True
        else:
            print(f"[ORCHESTRATOR] Ціни заліза актуальні. Останнє оновлення: {latest_date_str} ({days_passed} дн. тому). Пропускаємо парсинг комплектуючих.")
            return False
            
    except sqlite3.OperationalError:
        return True
    finally:
        conn.close()


def run_step(step_name: str, step_function) -> float:
    """Запускає окремий крок системи та міряє час його виконання"""
    print(f"\n" + "="*60)
    print(f"🚀 ЗАПУСК ЕТАПУ: {step_name.upper()}")
    print("="*60)
    
    start_time = time.time()
    try:
        step_function()
        elapsed = time.time() - start_time
        print(f"✅ ЕТАП {step_name.upper()} ЗАВЕРШЕНО ЗА {elapsed:.2f} сек.")
        return elapsed
    except Exception as e:
        print(f"❌ ПОМИЛКА під час виконання {step_name}: {e}")
        return 0.0


def main():
    total_start = time.time()
    today_str = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    
    print(f"==========================================================")
    print(f"🏁    СТАРТ ПОВНОГО ЦИКЛУ АВТОМАТИЗАЦІЇ OLX ({today_str})   ")
    print(f"==========================================================")

    run_step("Ініціалізація бази даних", db_init.init_db)

    # Крок 1: Розумний парсинг комплектуючих (лише раз на 7 днів)
    if should_parse_hardware():
        run_step("Парсинг комплектуючих", parser_hardware.main)
    else:
        print("\n[INFO] Етап 'Парсинг комплектуючих' пропущено (ціни ще свіжі).")

    # Крок 2: Парсинг нових комп'ютерів (сирих оголошень) — запускається завжди
    run_step("Парсинг готових ПК", parser.main)

    # Крок 3: Локальна фільтрація (маркування бан-вордів)
    run_step("Фільтрація оголошень", filter_ads.main)

    # Крок 4: Оцінка продавців
    run_step("Оцінка продавців", seller_analyzer.run_seller_analysis)

    # Крок 5: Оцінка вартості комп'ютерів
    run_step("Оцінка вигідності ПК", pc_evaluator.main)

    # Крок 6: Визначення справедливою ціни для продажи
    run_step("Визначення справедливою ціни для продажи", competitor_finder.main)

    # Крок 6: Перевірка життєздатності старих оголошень (архівування)
    run_step("Верифікація активності оголошень", clean_archive.main)

    total_elapsed = time.time() - total_start
    print(f"\n" + "="*60)
    print(f"🎉 ВСЕБІЧНИЙ АНАЛІЗ ЗАВЕРШЕНО УСПІШНО ЗА {total_elapsed/60:.2f} хв.")
    print("="*60)


if __name__ == "__main__":
    main()
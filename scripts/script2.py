import sqlite3
import sys
from pathlib import Path

# Визначення кореневої директорії проєкту
PROJECT_ROOT = Path(__file__).resolve().parent
if not (PROJECT_ROOT / "config.py").exists():
    PROJECT_ROOT = PROJECT_ROOT.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from config import DB_FILE


def delete_ads_by_parsed_date(target_date: str):
    """Видаляє всі записи з таблиці ads за вказану дату parsed_date (YYYY-MM-DD)."""
    if not DB_FILE.exists():
        print(f"[ПОМИЛКА] Файл бази даних не знайдено: {DB_FILE}")
        return

    print(
        f"--- ОЧИЩЕННЯ ТАБЛИЦІ ads У SQLite ({DB_FILE.name}) ЗA {target_date} ---"
    )

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    try:
        # Увімкнення режиму WAL для стабільності
        cursor.execute("PRAGMA journal_mode=WAL;")

        # Виконання запиту на видалення
        cursor.execute(
            "DELETE FROM ads WHERE parsed_date = ?;", (target_date,)
        )

        deleted_count = cursor.rowcount
        conn.commit()

        print(
            f"[УСПІХ] Видалено записів за {target_date}: {deleted_count} шт."
        )

    except sqlite3.Error as error:
        conn.rollback()
        print(f"[ПОМИЛКА] Не вдалося видалити дані з бази: {error}")

    finally:
        conn.close()


if __name__ == "__main__":
    TARGET_DATE = "2026-07-25"
    delete_ads_by_parsed_date(TARGET_DATE)
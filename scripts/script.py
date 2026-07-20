import sys
import sqlite3
import requests
from bs4 import BeautifulSoup
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
if not (PROJECT_ROOT / "config.py").exists():
    PROJECT_ROOT = PROJECT_ROOT.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from config import DB_FILE, HTML_FILE

def debug_olx_scripts():
    if not DB_FILE.exists():
        print("[ПОМИЛКА] Базу даних не знайдено!")
        return

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    # Беремо будь-яке одне живе посилання на комп'ютер чи деталь
    cursor.execute("SELECT url FROM ads WHERE status = 'active' LIMIT 1")
    row = cursor.fetchone()
    conn.close()

    if not row:
        print("[INFO] Немає активних оголошень для тесту.")
        return

    url = "https://www.olx.ua/d/uk/obyavlenie/vdeokarta-gtx-1060-3gb-ID10QvVa.html"
    print(f"📡 Завантажуємо сторінку для аналізу: {url}")

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            print(f"[ПОМИЛКА] OLX повернув статус-код: {response.status_code}")
            return

        soup = BeautifulSoup(response.text, "html.parser")
        scripts = soup.find_all("script")

        debug_lines = []
        for i, script in enumerate(scripts):
            script_text = script.string or script.text or ""
            if not script_text.strip():
                # Якщо це просто підключений зовнішній файл js (типу <script src="..."></script>)
                src = script.get("src", "inline")
                debug_lines.append(f"--- Скрипт #{i} (зовнішнє джерело: {src}) ---\n")
                continue
            
            # Якщо всередині скрипта є щось схоже на великі дані (наприклад, JSON)
            length = len(script_text)
            first_chars = script_text.strip()[:150].replace('\n', ' ')
            debug_lines.append(f"--- Скрипт #{i} (Довжина: {length} символів) ---\n")
            debug_lines.append(f"Початок: {first_chars}...\n\n")

        # Зберігаємо результати у файл
        debug_file = PROJECT_ROOT / "data" / "olx_scripts_debug.txt"
        debug_file.write_text("".join(debug_lines), encoding="utf-8")
        
        # Також збережемо повний HTML для детального пошуку, якщо знадобиться
        html_file = HTML_FILE
        html_file.write_text(response.text, encoding="utf-8")

        print(f"\n[УСПІХ] Аналіз завершено!")
        print(f"📄 Огляд скриптів збережено в: {debug_file.name}")
        print(f"🌐 Повний вихідний код сторінки збережено в: {html_file.name}")
        print("\nВідкрийте файл 'olx_scripts_debug.txt' та подивіться, які скрипти мають велику довжину (зазвичай > 10000) і що там написано на початку.")

    except Exception as e:
        print(f"❌ Помилка під час діагностики: {e}")

if __name__ == "__main__":
    debug_olx_scripts()
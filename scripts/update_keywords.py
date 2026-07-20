import sys
import json
import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
if not (PROJECT_ROOT / "config.py").exists():
    PROJECT_ROOT = PROJECT_ROOT.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from config import HTML_FILE, CLEANED_STATE_FILE


def decode_prerendered_state():
    if not HTML_FILE.exists():
        print(
            "❌ Файл 'olx_page_source.html' не знайдено! Спочатку запустіть діагностику."
        )
        return

    html_text = HTML_FILE.read_text(encoding="utf-8")
    print("⏳ Шукаємо window.__PRERENDERED_STATE__ у збереженому HTML...")

    # Шукаємо вміст змінної window.__PRERENDERED_STATE__
    # Вона загорнута в подвійні лапки і містить екранований JSON
    match = re.search(
        r'window\.__PRERENDERED_STATE__\s*=\s*"((?:\\.|[^"\\])*)"', html_text
    )
    if not match:
        match = re.search(
            r"window\.__PRERENDERED_STATE__\s*=\s*'((?:\\.|[^'\\])*)'", html_text
        )

    if not match:
        # Якщо раптом вона там лежить як чистий об'єкт без екранування (хоча навряд чи)
        match = re.search(
            r"window\.__PRERENDERED_STATE__\s*=\s*({.*?})\s*;?",
            html_text,
            re.DOTALL,
        )
        if match:
            print("💡 Знайдено чистий JSON без екранування.")
            try:
                state = json.loads(match.group(1))
                save_json(state)
                return
            except Exception as e:
                print(f"Помилка швидкого парсингу: {e}")

    if not match:
        print("❌ Не вдалося знайти window.__PRERENDERED_STATE__ у файлі!")
        return

    try:
        raw_escaped_json = match.group(1)

        # Розпаковуємо екрановані лапки \" назад у звичайні "
        clean_json_str = json.loads(f'"{raw_escaped_json}"')

        # Перетворюємо в нормальний Python-словник
        state = json.loads(clean_json_str)

        save_json(state)

    except Exception as e:
        print(f"❌ Помилка обробки JSON: {e}")


def save_json(state_dict):
    output_file = CLEANED_STATE_FILE
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(state_dict, f, ensure_ascii=False, indent=2)

    print(
        f"\n🎉 УСПІХ! Дані оголошення та продавця розпаковано й збережено!"
    )
    print(f"📄 Відкривайте файл: {output_file.name}")
    print(
        "💡 Шукайте там через Ctrl + F: 'user', 'ratingStatus', 'deliveryDeals' або 'created'"
    )


if __name__ == "__main__":
    decode_prerendered_state()
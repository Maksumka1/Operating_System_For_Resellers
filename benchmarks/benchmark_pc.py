"""
Benchmark & Ground Truth Validator for OLX PC Parser
====================================================
Інструмент для ручної розмітки оголошень та тестування точності функції `is_real_pc`.

Запуск:
  python benchmark_pc.py
"""

from __future__ import annotations

import json
import os
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from supabase import Client, create_client

# ---------------------------------------------------------------------------
# 1. КОНФІГУРАЦІЯ ТА ФУНКЦІЯ З ПАРСЕРА
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class PcParserConfig:
    category_id: str = "78"

    # 1. Завжди заборонена периферія (жодні прикметники на зразок "комп'ютерні" не скасовують блокування)
    strictly_forbidden_peripherals: tuple[str, ...] = field(default_factory=lambda: (
        "колонки", "колонка", "акустика", "навушники", "наушники",
        "гарнітура", "гарнитура", "рентген", "техніка б/у", "техника б/у"
    ))

    # 2. Периферія, яка дозволена, ТІЛЬКИ якщо продається разом із готовим ПК
    allowed_with_pc_peripherals: tuple[str, ...] = field(default_factory=lambda: (
        "мишка", "мышка", "клавіатура", "клавиатура"
    ))

    # 3. Запчастини
    not_a_pc_words: tuple[str, ...] = field(default_factory=lambda: (
        "материнська плата", "материнская плата", "материнка", "мать",
        "блок питания", "блок живлення", "дбж", "ups", "бесперебойник",
        "оперативна память", "оперативная память", "озу", "ram",
        "кулер", "вентилятор", "корпус без", "видеокарта", "відеокарта",
        "процессор", "процесор", "ssd", "hdd", "жесткий диск", "жорсткий диск",
        "лікар", "операці", "хвороба"
    ))

    # 4. Індикатори комп'ютера
    pc_indicators: tuple[str, ...] = field(default_factory=lambda: (
        "пк", "pc", "комп", "компютер", "комп'ютер", "компьютер", "комьютер",
        "системник", "системничек", "системний блок", "системный блок", "системний", "системный",
        "моноблок", "imac", "mac mini", "macmini", "macstudio", "mac pro", "workstation",
        "неттоп", "nettop", "ноутбук", "laptop", "ігровий", "игровой",
        "optiplex", "thinkcentre", "elitedesk", "prodesk", "micro",
        "тонкий клієнт", "тонкий клиент", "thin client", "raspberry", "мікрокомп",
        "asic", "antminer", "майнер"
    ))


def is_real_pc(title: str, cfg: PcParserConfig) -> tuple[bool, str]:
    if not title:
        return False, "empty_title"

    t = title.lower().replace("’", "'").replace("`", "'").replace("ʼ", "'").strip()

    # 1. Спам та службові оголошення
    if re.search(r"\b(відгукніться|важливо|увага|куплю|шукаю)\b", t):
        return False, "spam_or_notice"

    # 2. Послуги збірки та налаштування (блокуємо безумовно)
    if re.search(r"\b(зберу|соберу|під замовлення|под заказ|на замовлення|на заказ|збірка пк|сборка пк)\b", t):
        return False, "pc_assembly_service"

    # 3. Набори офісної техніки / різного заліза
    if re.search(r"комп[']?ютерн(ої|ой)\s+технік(и|а)", t):
        return False, "bundle_of_misc_hardware"

    # 4. Абсолютно заборонена периферія
    for word in cfg.strictly_forbidden_peripherals:
        if re.search(rf"\b{re.escape(word)}\b", t):
            return False, f"strictly_forbidden: {word}"

    # 5. Комплектуючі / деталі до ПК (з урахуванням одруківок типу "комлеткиуючі")
    if re.search(r"\bком[пл]+[еиа-я]*[тк]+[уюіючих]+\s*(до|к)?\s*(пк|pc|комп)", t):
        return False, "parts_bundle_for_pc"

    # 6. Детекція компонентів заліза
    has_cpu = bool(re.search(r"(ryzen|i[3579]-?\d{4,5}|xeon|core\s*i[3579]|pentium|celeron|\b2020m\b|\ba[468]-?\d{4}\b|\bm[1234]\b)", t))
    has_gpu = bool(re.search(r"(gtx\s*\d{3,4}|rtx\s*\d{3,4}|rx\s*\d{3,4}|radeon|quadro|\b1060\b|\b1070\b|\b1080\b|\b1050\b|\b3080\b|\b3060\b|\b3070\b|\b4060\b|geforce)", t))
    has_ram_or_ssd = bool(re.search(r"(ddr[345]|\d+\s*gb|\d+\s*гб|ssd|nvme|m\.2|\b500\b|\b240\b|\b256\b|\b16\b|\b32\b|\b4tb\b)", t))

    # 7. Базові індикатори ПК
    has_pc_indicator = any(
        re.search(rf"(?<![a-zа-яіїєґ0-9]){re.escape(ind)}", t)
        for ind in cfg.pc_indicators
    )

    # 8. Обробка комплектів (ПК + монітор / девайси)
    if re.search(r"\b(комплект[а-яіїєґ]*|проц\+)\b", t):
        # Якщо це окремий апгрейд-набір без корпусу/відеокарти — блокуємо
        is_real_pc_bundle = has_pc_indicator and (has_gpu or any(ind in t for ind in ("системний блок", "системный блок", "компьютер", "комп'ютер", "компютер", "пк")))
        if not is_real_pc_bundle:
            return False, "parts_bundle_or_service"

    # 9. Клавіатури / мишки без чіткого індикатора ПК
    for word in cfg.allowed_with_pc_peripherals:
        if re.search(rf"\b{re.escape(word)}\b", t):
            if not has_pc_indicator:
                return False, f"peripheral_without_pc: {word}"

    # 10. ПК за конфігурацією заліза
    is_spec_pc = (has_cpu and has_gpu) or (has_cpu and has_ram_or_ssd and has_pc_indicator) or (has_gpu and has_ram_or_ssd and has_pc_indicator)

    # 11. Окремі відеокарти
    if has_gpu and not has_cpu and not has_pc_indicator:
        return False, "standalone_gpu"

    # 12. Окремі процесори
    if has_cpu and not has_gpu and not has_pc_indicator and not is_spec_pc:
        return False, "standalone_cpu"

    # 13. Заборонені запчастини
    for bad_word in cfg.not_a_pc_words:
        if bad_word in t and not (has_pc_indicator or is_spec_pc):
            return False, f"banned_word_without_pc_indicator: {bad_word}"

    # 14. Відсутність ключових слів
    if not (has_pc_indicator or is_spec_pc):
        return False, "no_pc_keywords_or_hardware"

    return True, "valid_pc"


# ---------------------------------------------------------------------------
# 2. УПРАВЛІННЯ ДАТАСЕТОМ
# ---------------------------------------------------------------------------
DATASET_FILE = Path("pc_benchmark_dataset.json")


def load_dataset() -> dict[str, dict[str, Any]]:
    """Завантажує існуючий еталонний датасет."""
    if DATASET_FILE.exists():
        try:
            return json.loads(DATASET_FILE.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}



def save_dataset(data: dict[str, dict[str, Any]]) -> None:
    """Зберігає еталонний датасет у файл."""
    DATASET_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def get_supabase_client() -> Client:
    load_dotenv()
    url = os.getenv("SUPABASE_URL", "").strip()
    key = os.getenv("SUPABASE_SECRET_KEY", "").strip()
    if not url or not key:
        print("❌ Помилка: Вкажіть SUPABASE_URL та SUPABASE_SECRET_KEY у файлі .env")
        sys.exit(1)
    return create_client(url, key)


def fetch_ads_from_db(client: Client, offset: int = 0, limit: int = 200) -> list[dict[str, Any]]:
    """Дістає наступну пачку оголошень з бази даних зі зміщенням."""
    print(f"📡 Завантажуємо {limit} оголошень з бази Supabase (починаючи з #{offset + 1})...")
    try:
        resp = (
            client.table("ads")
            .select("ad_id, title, price, city, url")
            .eq("item_type", "pc")
            .order("created_at_olx", desc=True)
            .range(offset, offset + limit - 1)
            .execute()
        )
        return resp.data or []
    except Exception as exc:
        print(f"❌ Помилка читання з БД: {exc}")
        return []


# ---------------------------------------------------------------------------
# 3. ІНТЕРАКТИВНА РОЗМІТКА
# ---------------------------------------------------------------------------
def interactive_labeling(ads: list[dict[str, Any]], dataset: dict[str, dict[str, Any]]) -> None:
    print("\n" + "=" * 70)
    print("🎯 РЕЖИМ РОЗМІТКИ ДАНИХ (Ground Truth Labeling)")
    print("   [y] / [1] / [Enter] -> ТАК, це повноцінний комп'ютер")
    print("   [n] / [0]           -> НІ, це деталь / інший товар")
    print("   [s]                 -> Пропустити лот")
    print("   [q]                 -> Завершити розмітку і перейти до тесту")
    print("=" * 70 + "\n")

    unlabeled = [ad for ad in ads if str(ad.get("ad_id")) not in dataset]
    if not unlabeled:
        print("✅ Усі завантажені оголошення вже розмічені у датасеті!")
        return

    print(f"📋 Залишилось розмітити: {len(unlabeled)} лотів\n")

    for idx, ad in enumerate(unlabeled, 1):
        ad_id = str(ad.get("ad_id"))
        title = ad.get("title", "").strip()
        price = ad.get("price", 0)
        city = ad.get("city", "Невідомо")

        print(f"[{idx}/{len(unlabeled)}] 🏷️  ID: {ad_id} | 💰 {price} грн | 📍 {city}")
        print(f"👉 Назва: \033[1;36m{title}\033[0m")

        while True:
            choice = input("Це комп'ютер? (y/n/s/q) [y]: ").strip().lower()

            if choice in ("y", "1", "д", "так", ""):
                dataset[ad_id] = {"title": title, "is_pc": True, "price": price, "city": city}
                break
            elif choice in ("n", "0", "н", "ні"):
                dataset[ad_id] = {"title": title, "is_pc": False, "price": price, "city": city}
                break
            elif choice == "s":
                print("⏩ Пропущено.")
                break
            elif choice == "q":
                print("\n💾 Зберігаємо розмічені дані та запускаємо бенчмарк...")
                save_dataset(dataset)
                return
            else:
                print("Невідома команда. Введіть 'y', 'n', 's' або 'q'.")

        print("-" * 50)
        # Автозбереження кожні 5 записів
        if idx % 5 == 0:
            save_dataset(dataset)

    save_dataset(dataset)
    print("🎉 Усі лоти розмічено та збережено!")


# ---------------------------------------------------------------------------
# 4. БЕНЧМАРК ТА ЗВІТ ТОЧНОСТІ
# ---------------------------------------------------------------------------
def run_benchmark(dataset: dict[str, dict[str, Any]]) -> None:
    if not dataset:
        print("⚠️ Датасет порожній. Розмітьте хоча б кілька лотів для тесту.")
        return

    cfg = PcParserConfig()

    tp = 0  # True Positive: Комп -> Код сказав Комп (✅)
    tn = 0  # True Negative: Не комп -> Код сказав Не комп (✅)
    fp = 0  # False Positive: Не комп -> Код сказав Комп (❌ Сміття просочилося)
    fn = 0  # False Negative: Комп -> Код відкинув (❌ Втрачений лот)

    false_positives: list[dict[str, Any]] = []
    false_negatives: list[dict[str, Any]] = []

    for ad_id, item in dataset.items():
        title = item["title"]
        expected_is_pc = item["is_pc"]

        pred_is_pc, reason = is_real_pc(title, cfg)

        if expected_is_pc and pred_is_pc:
            tp += 1
        elif not expected_is_pc and not pred_is_pc:
            tn += 1
        elif not expected_is_pc and pred_is_pc:
            fp += 1
            false_positives.append({"title": title, "ad_id": ad_id, "reason": reason})
        elif expected_is_pc and not pred_is_pc:
            fn += 1
            false_negatives.append({"title": title, "ad_id": ad_id, "reason": reason})

    total = len(dataset)
    accuracy = ((tp + tn) / total) * 100 if total else 0
    precision = (tp / (tp + fp)) * 100 if (tp + fp) else 0
    recall = (tp / (tp + fn)) * 100 if (tp + fn) else 0
    f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) else 0

    print("\n" + "=" * 70)
    print("📊 РЕЗУЛЬТАТИ БЕНЧМАРКУ (Accuracy Evaluation)")
    print("=" * 70)
    print(f"📦 Всього лотів у базі тесту : {total}")
    print(f"✅ Правильно розпізнано     : {tp + tn} ({accuracy:.2f}%)")
    print(f"   • Справжніх ПК знайдено  : {tp}")
    print(f"   • Сміття відфільтровано  : {tn}")
    print("-" * 70)
    print(f"📈 Метрики класифікації:")
    print(f"   • Accuracy  (Загальна точність) : \033[1;32m{accuracy:.2f}%\033[0m")
    print(f"   • Precision (Чистота вибірки)   : \033[1;32m{precision:.2f}%\033[0m")
    print(f"   • Recall    (Повнота знахідок)  : \033[1;32m{recall:.2f}%\033[0m")
    print(f"   • F1 Score                      : \033[1;32m{f1:.2f}%\033[0m")
    print("=" * 70)

    # 🔴 Деталізація помилок
    if false_positives:
        print(f"\n🚨 ПОМИЛКОВІ ПРОПУСКИ (False Positives — {len(false_positives)} шт.)")
        print("   (Це НЕ комп'ютери, але код їх пропустив як ПК):")
        for i, item in enumerate(false_positives, 1):
            print(f"   {i}. [\033[1;31mID {item['ad_id']}\033[0m] {item['title']}")

    if false_negatives:
        print(f"\n⚠️ ВТРАЧЕНІ КОМП'ЮТЕРИ (False Negatives — {len(false_negatives)} шт.)")
        print("   (Це реальні ПК, але код їх заблокував):")
        for i, item in enumerate(false_negatives, 1):
            print(f"   {i}. [\033[1;33mID {item['ad_id']}\033[0m] {item['title']}")
            print(f"      └── Причина блокування: {item['reason']}")

    if not false_positives and not false_negatives:
        print("\n🏆 ІДЕАЛЬНО! 100% збіг логіки коду з вашою ручною розміткою!")
    print("\n" + "=" * 70 + "\n")


# ---------------------------------------------------------------------------
# 5. ГОЛОВНЕ МЕНЮ
# ---------------------------------------------------------------------------
def main():
    dataset = load_dataset()
    print(f"📂 Завантажено розмічених записів: {len(dataset)}")

    print("\nОберіть дію:")
    print("1. Завантажити наступну пачку лотів з БД і продовжити розмітку")
    print("2. Запустити швидкий тест на існуючому датасеті")
    print("3. Очистити датасет і почати з нуля")
    
    choice = input("\nВаш вибір (1/2/3) [1]: ").strip()

    if choice == "3":
        confirm = input("⚠️ Ви впевнені, що хочете видалити датасет? (y/n): ").strip().lower()
        if confirm in ("y", "yes", "д"):
            if DATASET_FILE.exists():
                DATASET_FILE.unlink()
            dataset = {}
            print("🗑️ Датасет очищено.")

    if choice in ("1", "", "3"):
        client = get_supabase_client()
        # 🎯 Беремо наступні 200 лотів після вже розмічених
        batch_size = 200
        ads = fetch_ads_from_db(client, offset=len(dataset), limit=batch_size)
        interactive_labeling(ads, dataset)

    # Запускаємо перевірку результатів
    run_benchmark(dataset)


if __name__ == "__main__":
    main()
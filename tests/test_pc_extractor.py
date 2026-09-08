"""
Тестовий стенд для діагностики розпізнавання комплектуючих ПК
Запуск: python -m tests.test_pc_extractor
"""

import sys
from pathlib import Path

# Додаємо корінь проєкту до sys.path
root_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root_dir))

from config import HARDWARE_TARGETS
from hardware_matchers import (
    extract_cpu,
    extract_gpu,
    extract_motherboard,
    extract_psu,
    extract_ram,
    extract_storage,
    normalize_title,
)
from core.pc_evaluator import HardwareMatchersExtractor, PcEvaluatorConfig

def run_extraction_diagnostics():
    config = PcEvaluatorConfig(hardware_targets=frozenset(HARDWARE_TARGETS))
    extractor = HardwareMatchersExtractor(
        hardware_targets=config.hardware_targets,
        extract_gpu_fn=extract_gpu,
        extract_cpu_fn=extract_cpu,
        extract_motherboard_fn=extract_motherboard,
        extract_ram_fn=extract_ram,
        extract_storage_fn=extract_storage,
        extract_psu_fn=extract_psu,
        normalize_fn=normalize_title,
    )

    # Тестові оголошення з різними форматами опису OLX
    test_cases = [
        {
            "name": "Збірка Ryzen + RTX + повний опис",
            "text": "Ігровий ПК Ryzen 5 5600 / RTX 3060 12GB / B450M / 16GB DDR4 / SSD 512GB / БЖ 600W",
        },
        {
            "name": "Intel з дефісами та маркуванням планки",
            "text": "Комп'ютер i5-10400F, GTX 1660 Super, плата H410, ОЗУ 2x8 16gb ddr4, блок aerocool 500w, m.2 256gb",
        },
        {
            "name": "Опис із шумом та іншими компонентами",
            "text": "ПК для ігор i7 7700K 16gb ram gtx 1070 8gb hdd 1tb + ssd 120gb блок живлення 650w chieftec стан супер",
        },
        {
            "name": "Складний випадок з розширеним описом",
            "text": "Продам системний блок ryzen 7 2700x / asus prime b450m / 32 gb ddr4 / gtx 1650 super / ssd 256gb / 600w",
        },
        {
            "name": "Сучасна збірка AM5 / DDR5 / Radeon RX",
            "text": "Ігровий системник Ryzen 5 7500F, плата MSI B650 Gaming Plus WiFi, ОЗП Kingston Fury 32GB DDR5 6000MHz, RX 6700 XT 12Gb, швидкий m.2 nvme 1tb, блок живлення DeepCool PK650D 650w",
        },
        # 2. Популярні китайські збірки на сокеті LGA2011-3 (Xeon)
        {
            "name": "Серверний Xeon LGA2011-3 + сапфір RX 580",
            "text": "ПК для роботи та ігор Xeon E5 2670 v3, матплата X99 titanium, 16gb ddr4 ram, sapphire nitro+ rx 580 8gb, ссд 500gb, бж чифтек 500w",
        },
        # 3. Суфікси Ti Super / Super + Intel LGA1700
        {
            "name": "Intel Core 12-14th gen + RTX 4070 Ti Super",
            "text": "Потужний комп i5 13400f / Asus TUF B760-Plus / 32 гб ddr5 / Palit GeForce RTX 4070 Ti Super 16GB / ssd m2 1000gb / БЖ Corsair RM750x 750w",
        },
        # 4. Скорочення Intel Core без слова "Core" чи дефіса
        {
            "name": "Intel Core скорочено + стара відеокарта GTX",
            "text": "Ігровий пк i3 12100f, gtx 1060 6gb, h610m, озу 16 gb ddr4, ssd m.2 256 gb, бж 450 вт",
        },
        # 5. Стара бюджетна збірка DDR3 (LGA1150)
        {
            "name": "Старий сокет LGA1150 / DDR3 / H81",
            "text": "Системний блок i5 4570 / 16gb ddr3 / asus h81m-k / gtx 960 4gb / ssd 120gb + hdd 500gb / блок 500w",
        },
        # 6. Тільки вбудована графіка (APU без дискретної відеокарти)
        {
            "name": "APU з інтегрованою графікою Vega (без дискретної GPU)",
            "text": "Компактний пк amd ryzen 5 4600g / vega 7 / b450 aorus elite / 16gb озу 3200mhz / швидкий ssd 480gb / блок живлення vinga 400w",
        },
        # 7. Комплектація кількома накопичувачами через плюс
        {
            "name": "Кілька накопичувачів (NVMe + SSD SATA + HDD)",
            "text": "ПК ryzen 5 3600 / rtx 2060 super 8gb / b450m pro4 / 16gb ddr4 / m2 nvme 512gb + ssd 240gb + hdd 2tb / chieftec proton 600w",
        },
        # 8. Суцільний текст без роздільників, маркування "2 по 8"
        {
            "name": "Сленговий опис з '2 по 8' та нестандартними відступами",
            "text": "ігровий компютер i5 11400f rtx 3050 8gb b560m озу 2 по 8гб ddr4 m2 ssd 512gb блок zalman 600 вт ідеальний стан",
        },
        # 9. Суфікс X3D + флагманські карти
        {
            "name": "Топовий геймінг Ryzen X3D + RTX 4080",
            "text": "Топовий ПК Ryzen 7 7800X3D / X670E Taichi / 64GB DDR5 / RTX 4080 Super 16GB / Samsung 980 Pro 2TB M.2 / Seasonic Focus 850W Gold",
        },
        # 10. AMD FX старого покоління + Radeon серії R9/HD
        {
            "name": "Ретро AMD FX + чипсет 970",
            "text": "Системник fx 8300, плата gigabyte 970a, пам'ять 16gb ddr3, відеокарта rx 470 4gb, ssd 120 gb, блок живлення aerocool vx 500",
        },
    ]

    print("=" * 80)
    print(f"Запуск діагностики. У базі HARDWARE_TARGETS: {len(config.hardware_targets)} моделей.")
    print("=" * 80)

    for case in test_cases:
        print(f"\nТест: {case['name']}")
        print(f"Вхідний текст: \"{case['text']}\"")
        clean_text = normalize_title(case["text"])
        print(f"Нормалізований текст: \"{clean_text}\"")

        # 1. Сирий вихід матчерів (без фільтрації HARDWARE_TARGETS)
        raw_cpu = extract_cpu(clean_text)
        raw_gpu = extract_gpu(clean_text)
        raw_mb = extract_motherboard(clean_text)
        raw_ram = extract_ram(clean_text)
        raw_storage = extract_storage(clean_text)
        raw_psu = extract_psu(clean_text)

        print(f"  [Матчери сирі] -> CPU: {raw_cpu}, GPU: {raw_gpu}, MB: {raw_mb}, RAM: {raw_ram}, Storage: {raw_storage}, PSU: {raw_psu}")

        # 2. Фільтрований вихід через HardwareMatchersExtractor
        extracted = extractor.extract(case["text"])
        print(f"  [Результат екстрактора] ->")
        print(f"    • CPU:     {extracted.cpu or '❌ Не знайдено в targets'}")
        print(f"    • GPU:     {extracted.gpu or '❌ Не знайдено в targets'}")
        print(f"    • MB:      {extracted.motherboard or '❌ Не знайдено в targets'}")
        print(f"    • RAM:     {extracted.ram or '❌ Не знайдено в targets'}")
        print(f"    • Storage: {extracted.storage or '❌ Не знайдено в targets'}")
        print(f"    • PSU:     {extracted.psu or '❌ Не знайдено в targets'}")

if __name__ == "__main__":
    run_extraction_diagnostics()
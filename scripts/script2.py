import json
import math
import time
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

BASE_URL = "https://www.techpowerup.com/gpu-specs/"
MANUFACTURERS = ["AMD", "NVIDIA"]


def parse_gpu_table(html_content: str) -> list[dict]:
    if not html_content:
        return []

    soup = BeautifulSoup(html_content, "lxml")
    rows = soup.select(".items-desktop-table tr")
    gpus = []

    for row in rows:
        if (
            row.find("th")
            or "colheader" in row.get("class", [])
            or "generation-header" in str(row)
        ):
            continue

        cols = row.find_all("td")
        if len(cols) >= 6:
            item_name_el = cols[0].select_one(".item-name a")
            item_released_el = cols[0].select_one(".item-released")
            item_chip_el = cols[0].select_one(".item-chip a")

            if not item_name_el:
                continue

            gpu_name = item_name_el.text.strip()
            href = item_name_el.get("href")
            full_url = f"https://www.techpowerup.com{href}" if href else None

            released = (
                item_released_el.text.strip() if item_released_el else None
            )
            chip = item_chip_el.text.strip() if item_chip_el else None

            bus = cols[1].text.strip()
            memory = " ".join(cols[2].text.split())
            gpu_clock = cols[3].text.strip()
            memory_clock = cols[4].text.strip()
            shading_units = " ".join(cols[5].text.split())

            gpu_data = {
                "gpu": gpu_name,
                "chip": chip,
                "released": released,
                "bus": bus,
                "memory": memory,
                "gpu_clock": gpu_clock,
                "memory_clock": memory_clock,
                "shading_units": shading_units,
                "url": full_url,
            }
            gpus.append(gpu_data)

    return gpus


def get_total_pages(html_content: str) -> int:
    soup = BeautifulSoup(html_content, "lxml")
    counts_span = soup.select_one(".pager .counts")

    if counts_span:
        b_tags = counts_span.find_all("b")
        if len(b_tags) >= 3:
            try:
                total_items = int(b_tags[2].text.strip())
                return math.ceil(total_items / 100)
            except ValueError:
                pass
    return 1


def main():
    print("[*] Запуск Playwright (у режимі реального Chrome)...")

    all_gpus = []

    with sync_playwright() as p:
        # 💡 headless=False ТА channel="chrome" — ключовий момент для обходу захисту!
        browser = p.chromium.launch(
            headless=False,
            channel="chrome",
            args=["--disable-blink-features=AutomationControlled"],
        )
        context = browser.new_context(
            viewport={"width": 1920, "height": 1080},
        )
        page = context.new_page()

        for mfgr in MANUFACTURERS:
            print(f"\n[===] Збір відеокарт: {mfgr} [===]")

            url = f"{BASE_URL}?mfgr={mfgr}"
            page.goto(url)

            # Чекаємо проходження JS-перевірки та появи таблиці (до 25 секунд)
            try:
                page.wait_for_selector(".items-desktop-table", timeout=25000)
            except Exception:
                print(
                    f"[!] Авто-перевірка не пройшла для {mfgr}. Спробуйте"
                    " проклікнути її у відкритому вікні браузера..."
                )
                continue

            first_html = page.content()
            total_pages = get_total_pages(first_html)
            print(f"[+] Знайдено сторінок для {mfgr}: {total_pages}")

            parsed = parse_gpu_table(first_html)
            all_gpus.extend(parsed)
            print(f"  [✓] Спарсено сторінку 1/{total_pages} ({len(parsed)} шт.)")

            for p_num in range(2, total_pages + 1):
                page_url = f"{BASE_URL}?mfgr={mfgr}&p={p_num}"
                page.goto(page_url)

                try:
                    page.wait_for_selector(
                        ".items-desktop-table", timeout=15000
                    )
                    html = page.content()
                    parsed_p = parse_gpu_table(html)
                    all_gpus.extend(parsed_p)
                    print(
                        f"  [✓] Спарсено сторінку {p_num}/{total_pages}"
                        f" (+{len(parsed_p)} шт.)"
                    )
                except Exception as e:
                    print(f"  [❌] Помилка на сторінці {p_num}: {e}")

                time.sleep(0.8)

        browser.close()

    # Дедуплікація
    unique_gpus = list(
        {gpu["url"]: gpu for gpu in all_gpus if gpu.get("url")}.values()
    )

    filename = "all_gpus.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(unique_gpus, f, indent=4, ensure_ascii=False)

    print(f"\n{'='*50}")
    print(
        f"[✓] ГОТОВО! Зібрано унікальних відеокарт: {len(unique_gpus)} через"
        " Playwright."
    )
    print(f"[✓] Збережено у `{filename}`")
    print(f"{'='*50}")


if __name__ == "__main__":
    main()
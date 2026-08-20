"""
Hardware Benchmark & Calibration Tool
Запуск: python benchmarks/hardware_benchmark.py
"""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path
from typing import Any

# Додаємо корінь проєкту до sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.prompt import Prompt
    from rich.table import Table
    _HAS_RICH = True
except ImportError:
    _HAS_RICH = False

from dotenv import load_dotenv
from supabase import create_client

# Імпортуємо тільки те, що безпосередньо викликається у бенчмарку
from parsers.parser_hardware import detect_socket, is_broken_ad, match_ad_to_hardware_target

load_dotenv(PROJECT_ROOT / ".env")
SUPABASE_URL = os.getenv("SUPABASE_URL", "").strip()
SUPABASE_KEY = os.getenv("SUPABASE_SECRET_KEY", "").strip()
DATASET_FILE = PROJECT_ROOT / "benchmarks" / "golden_hardware.json"

console = Console() if _HAS_RICH else None
VALID_ITEM_TYPES = ["gpu", "cpu", "motherboard", "ram", "storage", "psu", "bundle", "other"]


def clean_desc(text: str | None) -> str:
    return re.sub(r"(\r?\n\s*){2,}", "\n", (text or "Немає опису").strip())


def evaluate_ad(title: str, description: str) -> dict[str, Any]:
    """Проганяє оголошення через усі ланцюжки екстракції."""
    matched = match_ad_to_hardware_target(title)
    target_name = matched[0] if matched else "unmatched"
    cfg = matched[1] if matched else {}
    item_type = cfg.get("item_type", "other") if matched else "other"

    full_text = f"{title} {description}"
    has_defects = 1 if is_broken_ad(full_text) else 0

    detected_sock = None
    if item_type in ("motherboard", "cpu"):
        detected_sock = detect_socket(title, description, target_name)

    return {
        "component_name": target_name,
        "item_type": item_type,
        "socket": detected_sock,
        "has_defects": has_defects,
    }


def run_test_on_saved_dataset(golden_dataset: dict[str, dict]) -> None:
    """Проганяє збережений датасет та виводить детальну матрицю точності."""
    if not golden_dataset:
        print("Датасет порожній. Спочатку додайте оголошення через режим калібрування.")
        return

    total = len(golden_dataset)
    comp_passed = 0
    sock_passed = 0
    defect_passed = 0
    full_match_count = 0
    results = []

    for item in golden_dataset.values():
        title = item.get("title", "")
        desc = item.get("description", "")
        actual = evaluate_ad(title, desc)

        exp_comp = item.get("expected_component_name")
        exp_type = item.get("expected_item_type")
        exp_sock = item.get("expected_socket")
        exp_defect = item.get("expected_has_defects", 0)

        comp_ok = (actual["component_name"] == exp_comp) and (actual["item_type"] == exp_type)
        sock_ok = (actual["socket"] == exp_sock)
        defect_ok = (actual["has_defects"] == exp_defect)
        full_match = comp_ok and sock_ok and defect_ok

        if comp_ok:
            comp_passed += 1
        if sock_ok:
            sock_passed += 1
        if defect_ok:
            defect_passed += 1
        if full_match:
            full_match_count += 1

        results.append({
            "ad_id": item.get("ad_id"),
            "title": title,
            "actual_comp": actual["component_name"],
            "expected_comp": exp_comp,
            "comp_ok": comp_ok,
            "actual_sock": actual["socket"] or "-",
            "expected_sock": exp_sock or "-",
            "sock_ok": sock_ok,
            "actual_def": actual["has_defects"],
            "expected_def": exp_defect,
            "defect_ok": defect_ok,
            "full_match": full_match,
        })

    if console:
        table = Table(title=f"\n📊 Результати тесту Golden Dataset Комплектуючих ({total} лотів)")
        table.add_column("ID", style="cyan", no_wrap=True)
        table.add_column("Назва", style="white")
        table.add_column("Компонент (Sys / Exp)", justify="center")
        table.add_column("Сокет (Sys / Exp)", justify="center")
        table.add_column("Дефект (Sys / Exp)", justify="center")
        table.add_column("Статус", justify="center")

        for r in results:
            comp_style = "green" if r["comp_ok"] else "red"
            sock_style = "green" if r["sock_ok"] else "red"
            def_style = "green" if r["defect_ok"] else "red"

            comp_str = f"[{comp_style}]{r['actual_comp']} / {r['expected_comp']}[/{comp_style}]"
            sock_str = f"[{sock_style}]{r['actual_sock']} / {r['expected_sock']}[/{sock_style}]"
            def_str = f"[{def_style}]{r['actual_def']} / {r['expected_def']}[/{def_style}]"
            status_str = "[bold green]PASSED[/bold green]" if r["full_match"] else "[bold red]FAILED[/bold red]"

            table.add_row(
                str(r["ad_id"]),
                r["title"][:28] + "...",
                comp_str,
                sock_str,
                def_str,
                status_str,
            )

        console.print(table)
        console.print("\n[bold white]📈 Зведена точність за метриками:[/bold white]")
        console.print(f"  • Компоненти / Моделі: [cyan]{comp_passed}/{total}[/cyan] ([bold green]{(comp_passed/total)*100:.1f}%[/bold green])")
        console.print(f"  • Сокети (CPU/MB):     [cyan]{sock_passed}/{total}[/cyan] ([bold green]{(sock_passed/total)*100:.1f}%[/bold green])")
        console.print(f"  • Детекція дефектів:   [cyan]{defect_passed}/{total}[/cyan] ([bold green]{(defect_passed/total)*100:.1f}%[/bold green])")
        console.print(f"  • Повний збіг (All-in):[cyan]{full_match_count}/{total}[/cyan] ([bold green]{(full_match_count/total)*100:.1f}%[/bold green])\n")
    else:
        print(f"\nТочність повної відповідності: {(full_match_count/total)*100:.1f}% ({full_match_count}/{total})")


def main() -> None:
    DATASET_FILE.parent.mkdir(exist_ok=True)
    golden_dataset: dict[str, dict] = {}
    if DATASET_FILE.exists():
        try:
            golden_dataset = json.loads(DATASET_FILE.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            golden_dataset = {}

    if console:
        console.print(Panel.fit("[bold white on blue] ⚙️ HARDWARE PARSER BENCHMARK & КАЛІБРУВАННЯ ⚙️ [/bold white on blue]"))

    if golden_dataset:
        if console:
            console.print(f"[bold green]Знайдено {len(golden_dataset)} еталонів у {DATASET_FILE.name}[/bold green]")

        mode = Prompt.ask(
            "Оберіть режим:\n1 - Швидкий тест на збереженому датасеті\n2 - Розмітити нові оголошення з БД\nВибір",
            choices=["1", "2"],
            default="1",
        ) if _HAS_RICH else input("Вибір режиму (1 = Тест, 2 = Додати): ").strip()

        if mode == "1":
            run_test_on_saved_dataset(golden_dataset)
            return

    if not SUPABASE_URL or not SUPABASE_KEY:
        raise RuntimeError("❌ Відсутній SUPABASE_URL або SUPABASE_SECRET_KEY у .env")

    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    count_str = input("\nСкільки нових оголошень завантажити для розмітки? (за замовчуванням 20): ").strip()
    limit = int(count_str) if count_str.isdigit() else 20

    already_verified_ids = set(golden_dataset.keys())
    fetch_limit = limit + len(already_verified_ids) + 50

    # Витягуємо виключно комплектуючі (без готових ПК)
    resp = (
        supabase.table("ads")
        .select("id, ad_id, title, description, price, item_type, component_name, socket, has_defects")
        .neq("item_type", "pc")
        .order("id", desc=True)
        .limit(fetch_limit)
        .execute()
    )
    raw_ads = resp.data or []
    untested_ads = [ad for ad in raw_ads if str(ad.get("ad_id")) not in already_verified_ids][:limit]

    if not untested_ads:
        print("✅ Немає нових оголошень для розмітки.")
        return

    for i, ad in enumerate(untested_ads, 1):
        ad_id_str = str(ad["ad_id"])
        title = ad.get("title", "")
        desc = ad.get("description", "")
        detected = evaluate_ad(title, desc)

        if console:
            console.print(f"\n[bold cyan]{'=' * 75}[/bold cyan]")
            console.print(f"📦 [bold white][{i}/{len(untested_ads)}][/bold white] ID: [cyan]{ad['ad_id']}[/cyan] | Ціна: [yellow]{ad.get('price', 0):,} грн[/yellow]")
            console.print(f"📌 [bold green]Назва:[/bold green] {title}")
            console.print(f"🤖 [bold magenta]Визначено модель:[/bold magenta] [bold yellow]{detected['component_name']}[/bold yellow] ({detected['item_type']})")
            if detected["socket"]:
                console.print(f"🔌 [bold magenta]Визначено сокет:[/bold magenta] [bold cyan]{detected['socket']}[/bold cyan]")
            if detected["has_defects"]:
                console.print("⚠️  [bold red]Позначено як дефектне/на запчастини[/bold red]")
            console.print(f"\n[dim]── Опис ──\n{clean_desc(desc)[:400]}\n──────────[/dim]\n")

        # 1. Валідація моделі / компонента
        is_comp_correct = Prompt.ask(
            "Модель/тип розпізнано вірно?",
            choices=["y", "n"],
            default="y"
        ) == "y" if _HAS_RICH else input("Модель/тип розпізнано вірно? (y/n): ").strip().lower() == "y"

        if is_comp_correct:
            exp_comp = detected["component_name"]
            exp_type = detected["item_type"]
        else:
            exp_type = Prompt.ask("Вкажіть точний item_type", choices=VALID_ITEM_TYPES, default="gpu") if _HAS_RICH else input(f"item_type ({VALID_ITEM_TYPES}): ")
            exp_comp = Prompt.ask("Вкажіть ключ таргету (наприклад rtx_3060_12gb або unmatched)", default="unmatched") if _HAS_RICH else input("Ключ таргету: ")

        # 2. Валідація сокета (якщо це CPU або плата)
        exp_sock = detected["socket"]
        if exp_type in ("cpu", "motherboard"):
            is_sock_correct = Prompt.ask(
                f"Сокет [{detected['socket'] or 'None'}] правильний?",
                choices=["y", "n"],
                default="y"
            ) == "y" if _HAS_RICH else input(f"Сокет [{detected['socket']}] вірний? (y/n): ").strip().lower() == "y"

            if not is_sock_correct:
                exp_sock = Prompt.ask("Вкажіть точний сокет (lga1700, am4, am5 тощо, або 'none')", default="none") if _HAS_RICH else input("Вкажіть сокет: ")
                exp_sock = None if exp_sock.lower() in ("none", "") else exp_sock.lower()

        # 3. Валідація дефектів
        defect_default = "y" if detected["has_defects"] else "n"
        has_defect_input = Prompt.ask(
            "Оголошення має дефекти/на запчастини?",
            choices=["y", "n"],
            default=defect_default
        ) == "y" if _HAS_RICH else input("Є дефекти? (y/n): ").strip().lower() == "y"
        exp_defect = 1 if has_defect_input else 0

        golden_dataset[ad_id_str] = {
            "ad_id": ad["ad_id"],
            "title": title,
            "description": desc,
            "expected_item_type": exp_type,
            "expected_component_name": exp_comp,
            "expected_socket": exp_sock,
            "expected_has_defects": exp_defect,
            "system_snapshot": detected,
        }

        DATASET_FILE.write_text(json.dumps(golden_dataset, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"\n✅ Калібрування завершено! Всього у датасеті: {len(golden_dataset)} лотів.")


if __name__ == "__main__":
    main()
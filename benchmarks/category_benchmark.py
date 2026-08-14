"""
Category Benchmark & Calibration Tool
Запуск: python benchmarks/category_benchmark.py
"""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.prompt import Confirm, Prompt
    from rich.table import Table
    _HAS_RICH = True
except ImportError:
    _HAS_RICH = False

from dotenv import load_dotenv
from supabase import create_client
from core.filter_ads import PcCategoryConfig, PcCategoryDetector

load_dotenv(PROJECT_ROOT / ".env")
SUPABASE_URL = os.getenv("SUPABASE_URL", "").strip()
SUPABASE_KEY = os.getenv("SUPABASE_SECRET_KEY", "").strip()
DATASET_FILE = PROJECT_ROOT / "benchmarks" / "golden_categories.json"

console = Console() if _HAS_RICH else None
VALID_CATEGORIES = ["gaming", "home_office", "brand_office", "obsolete", "wholesale", "mining"]


def clean_desc(text: str | None) -> str:
    return re.sub(r"(\r?\n\s*){2,}", "\n", (text or "Немає опису").strip())


def run_test_on_saved_dataset(detector: PcCategoryDetector, golden_dataset: dict[str, dict]) -> None:
    """Проганяє збережений датасет через актуальний код без запитів до користувача."""
    if not golden_dataset:
        print("Датасет порожній. Спочатку додайте оголошення через режим калібрування.")
        return

    passed_count = 0
    total = len(golden_dataset)
    results = []

    for item in golden_dataset.values():
        full_text = f"{item.get('title', '')} {item.get('description', '')}".strip()
        actual_cat = detector.detect(full_text)
        expected_cat = item["expected_category"]
        is_match = (actual_cat == expected_cat)

        if is_match:
            passed_count += 1

        results.append({
            "ad_id": item["ad_id"],
            "title": item["title"],
            "actual": actual_cat,
            "expected": expected_cat,
            "is_match": is_match
        })

    accuracy = (passed_count / total) * 100

    if console:
        table = Table(title=f"\n📊 Результати тесту на збереженому Golden Dataset ({total} лотів)")
        table.add_column("ID", style="cyan", no_wrap=True)
        table.add_column("Назва", style="white")
        table.add_column("Система", justify="center")
        table.add_column("Еталон", justify="center")
        table.add_column("Результат", justify="center")

        for r in results:
            status_str = "[bold green]PASSED[/bold green]" if r["is_match"] else "[bold red]FAILED[/bold red]"
            table.add_row(
                str(r["ad_id"]),
                r["title"][:35] + "...",
                r["actual"],
                r["expected"],
                status_str
            )

        console.print(table)
        console.print(f"\n[bold white]Фінальна точність: {passed_count}/{total} ([/bold white][bold green]{accuracy:.1f}%[/bold green][bold white])[/bold white]\n")
    else:
        print(f"\nТочність системи: {accuracy:.1f}% ({passed_count}/{total} збігів)")


def main() -> None:
    DATASET_FILE.parent.mkdir(exist_ok=True)
    golden_dataset: dict[str, dict] = {}
    if DATASET_FILE.exists():
        try:
            golden_dataset = json.loads(DATASET_FILE.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            golden_dataset = {}

    detector = PcCategoryDetector(PcCategoryConfig())

    if console:
        console.print(Panel.fit("[bold white on blue] 🎯 BENCHMARK & КАЛІБРУВАННЯ КАТЕГОРІЙ ПК 🎯 [/bold white on blue]"))

    # Якщо датасет вже існує — запитуємо дію
    if golden_dataset:
        if console:
            console.print(f"[bold green]Знайдено {len(golden_dataset)} збережених еталонів у {DATASET_FILE.name}[/bold green]")
        
        mode = Prompt.ask(
            "Оберіть режим:\n1 - Запустити швидкий тест коду на збережених даних\n2 - Додати нові оголошення з бази\nВибір",
            choices=["1", "2"],
            default="1"
        ) if _HAS_RICH else input("Вибір режиму (1 = Тест, 2 = Додати нові): ").strip()

        if mode == "1":
            run_test_on_saved_dataset(detector, golden_dataset)
            return

    # Режим додавання нових оголошень
    if not SUPABASE_URL or not SUPABASE_KEY:
        raise RuntimeError("❌ Відсутній SUPABASE_URL або SUPABASE_SECRET_KEY у .env")

    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    count_str = input("\nСкільки нових оголошень завантажити для розмітки? (за замовчуванням 20): ").strip()
    limit = int(count_str) if count_str.isdigit() else 20

    already_verified_ids = set(golden_dataset.keys())
    fetch_limit = limit + len(already_verified_ids) + 50

    resp = (
        supabase.table("ads")
        .select("id, ad_id, title, description, pc_category, price")
        .eq("item_type", "pc")
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
        full_text = f"{ad.get('title', '')} {ad.get('description', '')}".strip()
        current_detected_cat = detector.detect(full_text)

        if console:
            console.print(f"\n[bold cyan]{'=' * 65}[/bold cyan]")
            console.print(f"📦 [bold white][{i}/{len(untested_ads)}][/bold white] ID: [cyan]{ad['ad_id']}[/cyan] | Ціна: [yellow]{ad.get('price', 0):,} грн[/yellow]")
            console.print(f"📌 [bold green]Назва:[/bold green] {ad['title']}")
            console.print(f"🤖 [bold magenta]Система визначила:[/bold magenta] [bold white on blue] {current_detected_cat.upper()} [/bold white on blue]")
            console.print(f"\n[dim]── Опис ──\n{clean_desc(ad.get('description'))}\n──────────[/dim]\n")

        user_input = Prompt.ask(
            "Категорія правильна?",
            choices=["y", "n"] + VALID_CATEGORIES,
            default="y"
        ).strip().lower() if _HAS_RICH else input(f"Категорія правильна? (y/n/{VALID_CATEGORIES}): ").strip().lower()

        if user_input in ("", "y", "yes"):
            expected_cat = current_detected_cat
        else:
            expected_cat = Prompt.ask("Вкажи правильну категорію", choices=VALID_CATEGORIES) if user_input == "n" else user_input

        golden_dataset[ad_id_str] = {
            "ad_id": ad["ad_id"],
            "title": ad["title"],
            "description": ad.get("description", ""),
            "db_category": current_detected_cat,
            "expected_category": expected_cat,
            "is_match": (current_detected_cat == expected_cat),
        }

        DATASET_FILE.write_text(json.dumps(golden_dataset, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"\n✅ Розмітку завершено! Всього у датасеті: {len(golden_dataset)} лотів.")


if __name__ == "__main__":
    main()
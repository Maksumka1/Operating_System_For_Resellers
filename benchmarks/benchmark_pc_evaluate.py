"""
PC Evaluator Benchmark & Calibration Tool
Запуск: python benchmarks/pc_evaluator_benchmark.py
"""

from __future__ import annotations

import asyncio
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

# Імпорт доменних моделей та класів оцінки ПК
try:
    from core.pc_evaluator import (
        ExtractedComponents,
        HardwareMatchersExtractor,
        PcAdRecord,
        PcEvaluator,
        PcEvaluatorConfig,
        SupabaseComponentPriceRepository,
    )
except ImportError:
    from core.pc_evaluator import (  # type: ignore
        ExtractedComponents,
        HardwareMatchersExtractor,
        PcAdRecord,
        PcEvaluator,
        PcEvaluatorConfig,
        SupabaseComponentPriceRepository,
    )

load_dotenv(PROJECT_ROOT / ".env")
SUPABASE_URL = os.getenv("SUPABASE_URL", "").strip()
SUPABASE_KEY = os.getenv("SUPABASE_SECRET_KEY", "").strip()
DATASET_FILE = PROJECT_ROOT / "benchmarks" / "golden_pc_eval.json"

console = Console() if _HAS_RICH else None
VALID_DEAL_STATUSES = ["🔥 SUPER DEAL", "⭐ GOOD DEAL", "❌ OVERPRICED", "regular"]


def clean_desc(text: str | None) -> str:
    return re.sub(r"(\r?\n\s*){2,}", "\n", (text or "Немає опису").strip())


def run_test_on_saved_dataset(
    evaluator: PcEvaluator,
    extractor: HardwareMatchersExtractor,
    prices: dict[str, int],
    golden_dataset: dict[str, dict],
) -> None:
    """Проганяє збережений датасет ПК через поточний екстрактор та калькулятор цін."""
    if not golden_dataset:
        print("Датасет порожній. Спочатку додайте ПК через режим розмітки.")
        return

    total = len(golden_dataset)
    cpu_passed = 0
    gpu_passed = 0
    components_all_passed = 0
    status_passed = 0
    price_diff_total = 0
    results = []

    for item in golden_dataset.values():
        ad_record = PcAdRecord(
            ad_id=int(item["ad_id"]),
            title=item.get("title", ""),
            description=item.get("description", ""),
            price=int(item.get("price", 1)),
        )

        extracted = extractor.extract(ad_record.full_text)
        evaluated = evaluator.evaluate(ad_record, extracted, prices)

        exp_cpu = item.get("expected_cpu")
        exp_gpu = item.get("expected_gpu")
        exp_mb = item.get("expected_mb")
        exp_ram = item.get("expected_ram")
        exp_storage = item.get("expected_storage")
        exp_psu = item.get("expected_psu")
        exp_status = item.get("expected_deal_status")
        exp_fair_price = item.get("expected_fair_price")

        cpu_ok = (extracted.cpu == exp_cpu)
        gpu_ok = (extracted.gpu == exp_gpu)
        all_comp_ok = (
            cpu_ok
            and gpu_ok
            and (extracted.motherboard == exp_mb)
            and (extracted.ram == exp_ram)
            and (extracted.storage == exp_storage)
            and (extracted.psu == exp_psu)
        )
        status_ok = (evaluated.deal_status == exp_status)

        if cpu_ok:
            cpu_passed += 1
        if gpu_ok:
            gpu_passed += 1
        if all_comp_ok:
            components_all_passed += 1
        if status_ok:
            status_passed += 1

        if exp_fair_price:
            price_diff_total += abs(evaluated.estimated_fair_price - int(exp_fair_price))

        results.append({
            "ad_id": ad_record.ad_id,
            "title": ad_record.title,
            "seller_price": ad_record.price,
            "cpu_match": f"{extracted.cpu or '-'} / {exp_cpu or '-'}",
            "cpu_ok": cpu_ok,
            "gpu_match": f"{extracted.gpu or '-'} / {exp_gpu or '-'}",
            "gpu_ok": gpu_ok,
            "fair_price": evaluated.estimated_fair_price,
            "exp_price": exp_fair_price or "-",
            "actual_status": evaluated.deal_status,
            "expected_status": exp_status,
            "status_ok": status_ok,
            "all_comp_ok": all_comp_ok,
        })

    if console:
        table = Table(title=f"\n📊 Результати тесту Golden Dataset Оцінки ПК ({total} лотів)")
        table.add_column("ID", style="cyan", no_wrap=True)
        table.add_column("Назва ПК", style="white")
        table.add_column("CPU (Sys / Exp)", justify="center")
        table.add_column("GPU (Sys / Exp)", justify="center")
        table.add_column("Ціна / Оцінка", justify="center")
        table.add_column("Статус (Sys / Exp)", justify="center")
        table.add_column("Результат", justify="center")

        for r in results:
            cpu_style = "green" if r["cpu_ok"] else "red"
            gpu_style = "green" if r["gpu_ok"] else "red"
            status_style = "green" if r["status_ok"] else "red"

            cpu_str = f"[{cpu_style}]{r['cpu_match']}[/{cpu_style}]"
            gpu_str = f"[{gpu_style}]{r['gpu_match']}[/{gpu_style}]"
            price_str = f"{r['seller_price']} / [bold yellow]{r['fair_price']}[/bold yellow]"
            status_str = f"[{status_style}]{r['actual_status']}[/{status_style}]"
            full_status = "[bold green]PASSED[/bold green]" if (r["all_comp_ok"] and r["status_ok"]) else "[bold red]FAILED[/bold red]"

            table.add_row(
                str(r["ad_id"]),
                r["title"][:26] + "...",
                cpu_str,
                gpu_str,
                price_str,
                status_str,
                full_status,
            )

        console.print(table)
        console.print("\n[bold white]📈 Зведена точність розпізнавання та оцінки ПК:[/bold white]")
        console.print(f"  • Точність CPU:              [cyan]{cpu_passed}/{total}[/cyan] ([bold green]{(cpu_passed/total)*100:.1f}%[/bold green])")
        console.print(f"  • Точність GPU:              [cyan]{gpu_passed}/{total}[/cyan] ([bold green]{(gpu_passed/total)*100:.1f}%[/bold green])")
        console.print(f"  • Повний білд (6 з 6 точні): [cyan]{components_all_passed}/{total}[/cyan] ([bold green]{(components_all_passed/total)*100:.1f}%[/bold green])")
        console.print(f"  • Точність Deal Status:      [cyan]{status_passed}/{total}[/cyan] ([bold green]{(status_passed/total)*100:.1f}%[/bold green])")
        if total > 0:
            console.print(f"  • Середня похибка оцінки:    [yellow]±{price_diff_total // total:,} грн[/yellow]\n")
    else:
        print(f"\nТочність CPU: {(cpu_passed/total)*100:.1f}% | Точність GPU: {(gpu_passed/total)*100:.1f}% | Статус: {(status_passed/total)*100:.1f}%")


async def main_async() -> None:
    DATASET_FILE.parent.mkdir(exist_ok=True)
    golden_dataset: dict[str, dict] = {}
    if DATASET_FILE.exists():
        try:
            golden_dataset = json.loads(DATASET_FILE.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            golden_dataset = {}

    if not SUPABASE_URL or not SUPABASE_KEY:
        raise RuntimeError("❌ Відсутній SUPABASE_URL або SUPABASE_SECRET_KEY у .env")

    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
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
    evaluator = PcEvaluator(config)
    price_repo = SupabaseComponentPriceRepository(supabase)

    if console:
        console.print(Panel.fit("[bold white on blue] 🖥️ PC EVALUATOR BENCHMARK & КАЛІБРУВАННЯ 🖥️ [/bold white on blue]"))

    prices = await price_repo.fetch_prices()
    if console:
        console.print(f"[dim]Завантажено {len(prices)} цін комплектуючих із бази для розрахунку вартості.[/dim]")

    if golden_dataset:
        if console:
            console.print(f"[bold green]Знайдено {len(golden_dataset)} еталонів у {DATASET_FILE.name}[/bold green]")

        mode = Prompt.ask(
            "Оберіть режим:\n1 - Запустити тест оцінки на збереженому датасеті\n2 - Розмітити нові ПК з бази\nВибір",
            choices=["1", "2"],
            default="1",
        ) if _HAS_RICH else input("Вибір режиму (1 = Тест, 2 = Додати нові): ").strip()

        if mode == "1":
            run_test_on_saved_dataset(evaluator, extractor, prices, golden_dataset)
            return

    count_str = input("\nСкільки нових ПК завантажити для розмітки? (за замовчуванням 15): ").strip()
    limit = int(count_str) if count_str.isdigit() else 15

    already_verified_ids = set(golden_dataset.keys())
    fetch_limit = limit + len(already_verified_ids) + 40

    resp = (
        supabase.table("ads")
        .select("ad_id, title, description, price, url, pc_category")
        .eq("item_type", "pc")
        .eq("status", "active")
        .or_("has_defects.eq.0,has_defects.is.null")
        .order("id", desc=True)
        .limit(fetch_limit)
        .execute()
    )
    raw_ads = resp.data or []
    untested_ads = [ad for ad in raw_ads if str(ad.get("ad_id")) not in already_verified_ids][:limit]

    if not untested_ads:
        print("✅ Немає нових оголошень ПК для розмітки.")
        return

    for i, ad in enumerate(untested_ads, 1):
        ad_id_str = str(ad["ad_id"])
        ad_record = PcAdRecord(
            ad_id=int(ad["ad_id"]),
            title=ad.get("title", ""),
            description=ad.get("description", ""),
            price=int(ad.get("price", 1)),
        )

        extracted = extractor.extract(ad_record.full_text)
        evaluated = evaluator.evaluate(ad_record, extracted, prices)

        if console:
            console.print(f"\n[bold cyan]{'=' * 80}[/bold cyan]")
            console.print(f"📦 [bold white][{i}/{len(untested_ads)}][/bold white] ID: [cyan]{ad_record.ad_id}[/cyan] | Ціна продавця: [yellow]{ad_record.price:,} грн[/yellow]")
            console.print(f"📌 [bold green]Назва:[/bold green] {ad_record.title}")
            console.print(f"🤖 [bold magenta]Розпізнано комплектуючі:[/bold magenta]")
            console.print(f"   • CPU:     [bold yellow]{extracted.cpu or 'None'}[/bold yellow] ({evaluated.cpu_market_price:,} грн)")
            console.print(f"   • GPU:     [bold yellow]{extracted.gpu or 'None'}[/bold yellow] ({evaluated.gpu_market_price:,} грн)")
            console.print(f"   • Плата:   {extracted.motherboard or 'None'} ({evaluated.mb_market_price:,} грн)")
            console.print(f"   • ОЗП:     {extracted.ram or 'None'} ({evaluated.ram_market_price:,} грн)")
            console.print(f"   • Диск:    {extracted.storage or 'None'} ({evaluated.storage_market_price:,} грн)")
            console.print(f"   • БЖ:      {extracted.psu or 'None'} ({evaluated.psu_market_price:,} грн)")
            console.print(f"💰 [bold green]Оцінка справедливої ціни:[/bold green] [bold yellow]{evaluated.estimated_fair_price:,} грн[/bold yellow]")
            console.print(f"🏷️  [bold magenta]Статус угоди:[/bold magenta] {evaluated.deal_status} (Вигода: {evaluated.saving_uah:,} грн / {evaluated.saving_percent}%)")
            console.print(f"\n[dim]── Опис ──\n{clean_desc(ad_record.description)[:500]}\n──────────[/dim]\n")

        # 1. Валідація CPU та GPU
        exp_cpu = extracted.cpu
        if not Confirm.ask(f"CPU [{extracted.cpu or 'None'}] правильний?", default=True):
            exp_cpu = Prompt.ask("Вкажіть точний CPU (або 'none')", default="none").strip()
            exp_cpu = None if exp_cpu.lower() in ("none", "") else exp_cpu

        exp_gpu = extracted.gpu
        if not Confirm.ask(f"GPU [{extracted.gpu or 'None'}] правильна?", default=True):
            exp_gpu = Prompt.ask("Вкажіть точну GPU (або 'none')", default="none").strip()
            exp_gpu = None if exp_gpu.lower() in ("none", "") else exp_gpu

        # 2. Валідація інших компонентів
        exp_mb = extracted.motherboard
        exp_ram = extracted.ram
        exp_storage = extracted.storage
        exp_psu = extracted.psu

        if not Confirm.ask("Інші комплектуючі (MB/RAM/SSD/PSU) розпізнано вірно?", default=True):
            mb_in = Prompt.ask("Плата", default=extracted.motherboard or "none")
            exp_mb = None if mb_in.lower() in ("none", "") else mb_in
            ram_in = Prompt.ask("RAM", default=extracted.ram or "none")
            exp_ram = None if ram_in.lower() in ("none", "") else ram_in
            st_in = Prompt.ask("Storage/SSD", default=extracted.storage or "none")
            exp_storage = None if st_in.lower() in ("none", "") else st_in
            psu_in = Prompt.ask("PSU", default=extracted.psu or "none")
            exp_psu = None if psu_in.lower() in ("none", "") else psu_in

        # 3. Валідація фінального Deal Status
        exp_status = evaluated.deal_status
        if not Confirm.ask(f"Статус угоди [{evaluated.deal_status}] вірний?", default=True):
            exp_status = Prompt.ask("Оберіть правильний статус", choices=VALID_DEAL_STATUSES, default="regular")

        golden_dataset[ad_id_str] = {
            "ad_id": ad_record.ad_id,
            "title": ad_record.title,
            "description": ad_record.description,
            "price": ad_record.price,
            "expected_cpu": exp_cpu,
            "expected_gpu": exp_gpu,
            "expected_mb": exp_mb,
            "expected_ram": exp_ram,
            "expected_storage": exp_storage,
            "expected_psu": exp_psu,
            "expected_deal_status": exp_status,
            "expected_fair_price": evaluated.estimated_fair_price,
        }

        DATASET_FILE.write_text(json.dumps(golden_dataset, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"\n✅ Розмітку ПК завершено! Всього у датасеті: {len(golden_dataset)} збірок.")


def main() -> None:
    try:
        if sys.platform == "win32":
            asyncio.run(main_async(), loop_factory=asyncio.SelectorEventLoop)
        else:
            asyncio.run(main_async())
    except KeyboardInterrupt:
        print("\nКалібрування перервано користувачем.")


if __name__ == "__main__":
    main()
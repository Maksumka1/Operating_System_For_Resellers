"""
OLX Market Pipeline — Universal Golden Dataset Benchmark & Health Tester
========================================================================
Запуск: python -m benchmarks.benchmark_cli
"""

from __future__ import annotations

import asyncio
import json
import os
import re
import sys
from pathlib import Path
from typing import Any
from pydantic import BaseModel, Field

# Додаємо корінь проєкту до sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Встановлення Rich для гарного CLI
try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.prompt import Confirm, Prompt
    from rich.table import Table
    _HAS_RICH = True
except ImportError:
    _HAS_RICH = False

from dotenv import load_dotenv
from supabase import Client, create_client

# Імпорти чистих модулів проєкту
try:
    from core.filter_ads import PcCategoryConfig, PcCategoryDetector
    from core.seller_analyzer import SellerAnalyzerConfig, RiskClassifier, RatingParser, YearExtractor
    from parsers.parser_hardware import is_broken_ad, match_ad_to_hardware_target
    from hardware_matchers import (
        extract_cpu,
        extract_gpu,
        extract_motherboard,
        extract_psu,
        extract_ram,
        extract_storage,
        normalize_title,
    )
    from config import HARDWARE_TARGETS
except ImportError as exc:
    print(f"❌ [CRITICAL IMPORT ERROR]: {exc}")
    sys.exit(1)


# ===========================================================================
# 1. HELPERS & TEXT CLEANING
# ===========================================================================
def clean_description(desc: str | None) -> str:
    """Прибирає купу порожніх рядків і форматує опис для повного показу."""
    if not desc:
        return "Опис відсутній."
    cleaned = re.sub(r"(\r?\n\s*){2,}", "\n", desc.strip())
    return cleaned


# ===========================================================================
# 2. CONTRACT DTOs (Data Transfer Objects)
# ===========================================================================
class BenchmarkAd(BaseModel):
    """Сирі дані оголошення для бенчмарку з Supabase."""
    ad_id: int
    item_type: str
    title: str
    description: str | None = ""
    price: int
    component_name: str | None = None
    url: str | None = None
    seller_id: str | None = None
    seller_created_at: str | None = None
    seller_successful_deals: int = 0
    seller_rating: str = "немає оцінок"


class ExpectedAnswer(BaseModel):
    """Еталонні відповіді від людини (Golden Dataset)."""
    is_defect: bool
    pc_category: str | None = None        # Тільки для ПК
    gpu_model: str | None = None          # Тільки для ПК
    cpu_model: str | None = None          # Тільки для ПК
    mb_model: str | None = None           # Тільки для ПК (Материнка)
    ram_model: str | None = None          # Тільки для ПК (RAM)
    storage_model: str | None = None      # Тільки для ПК (SSD/HDD)
    psu_model: str | None = None          # Тільки для ПК (Блок живлення)
    component_name: str | None = None     # Для окремих комплектуючих (GPU, CPU і т.д.)
    seller_risk: str                      # safe | neutral | suspicious


class SystemOutput(BaseModel):
    """Фактичні результати роботи модулів системи."""
    is_defect: bool
    pc_category: str | None = None
    gpu_model: str | None = None
    cpu_model: str | None = None
    mb_model: str | None = None
    ram_model: str | None = None
    storage_model: str | None = None
    psu_model: str | None = None
    component_name: str | None = None
    seller_risk: str


class GoldenBenchmarkItem(BaseModel):
    ad: BenchmarkAd
    expected: ExpectedAnswer


# ===========================================================================
# 3. SYSTEM ADAPTER (Black-Box Wrapper)
# ===========================================================================
class SystemPipelineAdapter:
    """Обгортка, яка викликає чисті модулі системи залежно від типу товару."""

    def __init__(self) -> None:
        self.cat_detector = PcCategoryDetector(PcCategoryConfig())
        self.risk_classifier = RiskClassifier(SellerAnalyzerConfig())
        self.rating_parser = RatingParser()
        self.year_extractor = YearExtractor()

    def process_ad(self, ad: BenchmarkAd) -> SystemOutput:
        full_text = f"{ad.title} {ad.description or ''}"

        # 1. Детекція дефекту / неробочого
        is_defect = is_broken_ad(full_text)

        # 2. Оцінка ризику продавця
        stars, has_rating = self.rating_parser.parse(ad.seller_rating)
        reg_year = self.year_extractor.extract(ad.seller_created_at)
        age_years = max(0, 2026 - reg_year) if reg_year else None
        seller_risk = self.risk_classifier.classify(
            deals=ad.seller_successful_deals,
            stars=stars,
            has_rating=has_rating,
            age_years=age_years
        )

        # 3. Логіка за типами оголошень
        if ad.item_type == "pc":
            category = self.cat_detector.detect(full_text)
            clean_text = normalize_title(full_text)

            gpus = extract_gpu(clean_text)
            cpus = extract_cpu(clean_text)
            mbs = extract_motherboard(clean_text)
            rams = extract_ram(clean_text)
            storages = extract_storage(clean_text)
            psus = extract_psu(clean_text)

            detected_gpu = gpus[0] if gpus and gpus[0] in HARDWARE_TARGETS else None
            detected_cpu = cpus[0] if cpus and cpus[0] in HARDWARE_TARGETS else None
            detected_mb = mbs[0] if mbs and mbs[0] in HARDWARE_TARGETS else None
            detected_ram = rams[0] if rams and rams[0] in HARDWARE_TARGETS else None
            detected_storage = storages[0] if storages and storages[0] in HARDWARE_TARGETS else None
            detected_psu = psus[0] if psus and psus[0] in HARDWARE_TARGETS else None

            return SystemOutput(
                is_defect=is_defect,
                pc_category=category,
                gpu_model=detected_gpu,
                cpu_model=detected_cpu,
                mb_model=detected_mb,
                ram_model=detected_ram,
                storage_model=detected_storage,
                psu_model=detected_psu,
                seller_risk=seller_risk
            )
        else:
            # Для комплектуючих (gpu, cpu, motherboard, ram, storage, psu)
            matched = match_ad_to_hardware_target(ad.title)
            detected_component = matched[0] if matched else None

            return SystemOutput(
                is_defect=is_defect,
                component_name=detected_component,
                seller_risk=seller_risk
            )


# ===========================================================================
# 4. DIFF & COMPARISON ENGINE
# ===========================================================================
class BenchmarkDiffEngine:
    @staticmethod
    def _norm(val: str | None) -> str:
        if not val or val.lower() in ("unknown gpu", "unknown cpu", "none"):
            return ""
        # Видаляємо пробіли, підкреслення та дефіси для гнучкого порівняння
        return re.sub(r"[_\s\-]+", "", val.lower())

    @classmethod
    def compare(cls, expected: ExpectedAnswer, actual: SystemOutput) -> list[str]:
        errors: list[str] = []

        # 1. Перевірка дефекту
        if expected.is_defect != actual.is_defect:
            errors.append(f"Дефект: Очікувалося {expected.is_defect}, система поставила {actual.is_defect}")

        # 2. Специфічні перевірки за типом
        if expected.pc_category is not None:
            # Це ПК
            if expected.pc_category != actual.pc_category:
                errors.append(f"Категорія: Очікувалося '{expected.pc_category}', система вказала '{actual.pc_category}'")

            if cls._norm(expected.gpu_model) != cls._norm(actual.gpu_model):
                errors.append(f"GPU: Очікувалося '{expected.gpu_model}', система розпізнала '{actual.gpu_model}'")

            if cls._norm(expected.cpu_model) != cls._norm(actual.cpu_model):
                errors.append(f"CPU: Очікувалося '{expected.cpu_model}', система розпізнала '{actual.cpu_model}'")

            if cls._norm(expected.mb_model) != cls._norm(actual.mb_model):
                errors.append(f"Motherboard: Очікувалося '{expected.mb_model}', система розпізнала '{actual.mb_model}'")

            if cls._norm(expected.ram_model) != cls._norm(actual.ram_model):
                errors.append(f"RAM: Очікувалося '{expected.ram_model}', система розпізнала '{actual.ram_model}'")

            if cls._norm(expected.storage_model) != cls._norm(actual.storage_model):
                errors.append(f"Storage: Очікувалося '{expected.storage_model}', система розпізнала '{actual.storage_model}'")

            if cls._norm(expected.psu_model) != cls._norm(actual.psu_model):
                errors.append(f"PSU: Очікувалося '{expected.psu_model}', система розпізнала '{actual.psu_model}'")
        else:
            # Це окреме Комплектуюче
            if cls._norm(expected.component_name) != cls._norm(actual.component_name):
                errors.append(f"Деталь: Очікувалося '{expected.component_name}', система визначила '{actual.component_name}'")

        # 3. Перевірка ризику продавця
        if expected.seller_risk != actual.seller_risk:
            errors.append(f"Ризик продавця: Очікувалося '{expected.seller_risk}', система визначила '{actual.seller_risk}'")

        return errors


# ===========================================================================
# 5. BENCHMARK CLI & FLOW ORCHESTRATOR
# ===========================================================================
class BenchmarkCLI:
    def __init__(self) -> None:
        self.console = Console() if _HAS_RICH else None
        self.dataset_file = PROJECT_ROOT / "benchmarks" / "golden_dataset.json"
        self.dataset_file.parent.mkdir(exist_ok=True)
        self.adapter = SystemPipelineAdapter()

    def print(self, msg: str, style: str = "") -> None:
        if self.console:
            self.console.print(msg, style=style)
        else:
            print(msg)

    async def fetch_ads_by_type(self, item_type: str, count: int = 20) -> list[BenchmarkAd]:
        load_dotenv(PROJECT_ROOT / ".env")
        url = os.getenv("SUPABASE_URL", "").strip()
        key = os.getenv("SUPABASE_SECRET_KEY", "").strip()

        if not url or not key:
            self.print("[bold red]❌ SUPABASE_URL або SUPABASE_SECRET_KEY відсутні у .env[/bold red]")
            return []

        client: Client = create_client(url, key)

        def _query() -> list[dict[str, Any]]:
            resp = client.table("ads").select(
                "ad_id, item_type, title, description, price, component_name, url, seller_id, seller_created_at, seller_successful_deals, seller_rating"
            ).eq("item_type", item_type).eq("status", "active").limit(count).execute()
            return resp.data or []

        rows = await asyncio.to_thread(_query)
        return [BenchmarkAd(**r) for r in rows]

    def prompt_human_answers(self, ad: BenchmarkAd, index: int, total: int) -> ExpectedAnswer:
        self.print(f"\n[bold cyan]──────── {ad.item_type.upper()} {index}/{total} (ID: {ad.ad_id}) ────────[/bold cyan]")
        self.print(f"[bold yellow]Заголовок:[/bold yellow] {ad.title}")
        self.print(f"[bold yellow]Ціна продавця:[/bold yellow] {ad.price:,} грн")
        self.print(f"[bold yellow]Продавець:[/bold yellow] Угод: {ad.seller_successful_deals} | Рейтинг: {ad.seller_rating} | Аккаунт з: {ad.seller_created_at or 'Невідомо'}")
        
        # Вивід повного опису без зайвих порожніх рядків
        cleaned_desc = clean_description(ad.description)
        self.print(f"\n[dim]── Повний опис ──\n{cleaned_desc}\n──────────────────[/dim]\n")

        is_defect = Confirm.ask("1. Це дефект / неробоче / сміття / сервіс?", default=False)
        
        pc_category = None
        gpu_model = None
        cpu_model = None
        mb_model = None
        ram_model = None
        storage_model = None
        psu_model = None
        component_name = None

        if ad.item_type == "pc":
            pc_category = Prompt.ask(
                "2. Вкажи категорію ПК",
                choices=["gaming", "home_office", "brand_office", "obsolete", "wholesale", "maining"],
                default="gaming"
            )
            gpu_model = Prompt.ask("3. Еталонна модель GPU ( або Enter)", default="")
            cpu_model = Prompt.ask("4. Еталонна модель CPU ( або Enter)", default="")
            mb_model = Prompt.ask("5. Еталонна Материнка (напр. b550 або Enter)", default="")
            ram_model = Prompt.ask("6. Еталонна RAM (напр. ram_ddr4_16gb або Enter)", default="")
            storage_model = Prompt.ask("7. Еталонний Накопичувач (напр. ssd_1tb або Enter)", default="")
            psu_model = Prompt.ask("8. Еталонний Блок живлення (напр. 600w або Enter)", default="")
        else:
            component_name = Prompt.ask(
                f"2. Введи еталонну назву/модель для {ad.item_type.upper()} (component_name)",
                default=ad.component_name or ""
            )

        seller_risk = Prompt.ask(
            "9. Оціни ризик продавця" if ad.item_type == "pc" else "3. Оціни ризик продавця",
            choices=["safe", "neutral", "suspicious"],
            default="safe"
        )

        return ExpectedAnswer(
            is_defect=is_defect,
            pc_category=pc_category,
            gpu_model=gpu_model.strip() or None if gpu_model else None,
            cpu_model=cpu_model.strip() or None if cpu_model else None,
            mb_model=mb_model.strip() or None if mb_model else None,
            ram_model=ram_model.strip() or None if ram_model else None,
            storage_model=storage_model.strip() or None if storage_model else None,
            psu_model=psu_model.strip() or None if psu_model else None,
            component_name=component_name.strip() or None if component_name else None,
            seller_risk=seller_risk
        )

    def load_existing_dataset(self) -> dict[int, GoldenBenchmarkItem]:
        if self.dataset_file.exists():
            try:
                raw_data = json.loads(self.dataset_file.read_text(encoding="utf-8"))
                return {item["ad"]["ad_id"]: GoldenBenchmarkItem.model_validate(item) for item in raw_data}
            except Exception:
                return {}
        return {}

    def save_dataset(self, dataset: dict[int, GoldenBenchmarkItem]) -> None:
        dump_data = [item.model_dump() for item in dataset.values()]
        self.dataset_file.write_text(json.dumps(dump_data, ensure_ascii=False, indent=2), encoding="utf-8")

    async def run_benchmark(self) -> None:
        self.print(Panel.fit("[bold white on blue] 🚀 UNIVERSAL OLX BENCHMARK TESTER 🚀 [/bold white on blue]"))

        existing_dataset = self.load_existing_dataset()
        
        categories = [
            ("pc", "Готові комп'ютери (ПК)"),
            ("cpu", "Процесори (CPU)"),
            ("gpu", "Відеокарти (GPU)"),
            ("motherboard", "Материнські плати"),
            ("ram", "Оперативна пам'ять (RAM)"),
            ("storage", "Накопичувачі (SSD/HDD)"),
            ("psu", "Блоки живлення (PSU)")
        ]

        for item_type, type_title in categories:
            self.print(f"\n\n[bold yellow]════════════════════════════════════════════════════════════[/bold yellow]")
            self.print(f"[bold yellow] 📦 КАТЕГОРИЯ: {type_title} ({item_type.upper()})[/bold yellow]")
            self.print(f"[bold yellow]════════════════════════════════════════════════════════════[/bold yellow]")

            ads = await self.fetch_ads_by_type(item_type, count=20)
            if not ads:
                self.print(f"[dim]Не знайдено активних оголошень для категорії {item_type}. Пропускаємо.[/dim]")
                continue

            batch_items: list[GoldenBenchmarkItem] = []

            for index, ad in enumerate(ads, 1):
                if ad.ad_id in existing_dataset:
                    self.print(f"[dim]✓ Оголошення ID #{ad.ad_id} вже є у збереженому датасеті (пропущено ввід)[/dim]")
                    batch_items.append(existing_dataset[ad.ad_id])
                else:
                    expected = self.prompt_human_answers(ad, index, len(ads))
                    benchmark_item = GoldenBenchmarkItem(ad=ad, expected=expected)
                    existing_dataset[ad.ad_id] = benchmark_item
                    batch_items.append(benchmark_item)
                    self.save_dataset(existing_dataset)

            # Прогін тесту для поточної пачки з 20 оголошень
            self.print(f"\n[bold green]⚡ Тестуємо модулі на 20 лотах з категорії '{type_title}'...[/bold green]\n")
            
            passed = 0
            table = Table(title=f"Звіт перевірки: {type_title}")
            table.add_column("ID", style="cyan", no_wrap=True)
            table.add_column("Заголовок", style="white")
            table.add_column("Результат", justify="center")
            table.add_column("Невідповідності", style="red")

            for item in batch_items:
                actual = self.adapter.process_ad(item.ad)
                errors = BenchmarkDiffEngine.compare(item.expected, actual)

                if not errors:
                    passed += 1
                    table.add_row(str(item.ad.ad_id), item.ad.title[:40] + "...", "[green]PASSED[/green]", "[dim]ОК[/dim]")
                else:
                    err_text = "\n".join(f"• {e}" for e in errors)
                    table.add_row(str(item.ad.ad_id), item.ad.title[:40] + "...", "[bold red]FAILED[/bold red]", err_text)

            if self.console:
                self.console.print(table)

            accuracy = (passed / len(batch_items)) * 100
            self.print(f"\n[bold white]Результат по {type_title}: {passed}/{len(batch_items)} пройдено ({accuracy:.1f}% accuracy)[/bold white]")

            # Запит на продовження до наступної категорії
            if not Confirm.ask(f"\n👉 Бажаєш продовжити тест і перейти до наступної категорії?", default=True):
                self.print("\n[bold yellow]Тестування зупинено користувачем.[/bold yellow]")
                break

        self.print("\n[bold green]🎉 Всі вибрані категорії успішно перевірені![/bold green]")


# ===========================================================================
# 6. ENTRY POINT
# ===========================================================================
def main() -> None:
    cli = BenchmarkCLI()
    try:
        asyncio.run(cli.run_benchmark())
    except KeyboardInterrupt:
        print("\nЗупинено.")


if __name__ == "__main__":
    main()
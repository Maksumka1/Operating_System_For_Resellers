from pathlib import Path

# Робочий стіл та шляхи
desktop = Path.home() / "OneDrive" / "Desktop"
print(desktop)
user_marker_src = desktop / "Projects" / "website_lovable" / "src"

# --- 1. Збір файлів бекенду / поточного проєкту ---
backend_root = Path(__file__).resolve().parent.parent
backend_output = desktop / "backend_combined.txt"

backend_files = [
    "main.py", "config.py", "docker-compose.yml", "Dockerfile", "requirements.txt", "hardware_matchers.py", "Caddyfile",
    "services/telegram_notifier.py",
    "server/server.py",
    "scripts/clean_archive.py",
    "parsers/parser.py", "parsers/parser_hardware.py",
    "core/competitor_finder.py", "core/filter_ads.py", "core/hardware_evaluator.py",
    "core/pc_evaluator.py", "core/price_hardware.py", "core/seller_analyzer.py"
]

with open(backend_output, "w", encoding="utf-8") as out:
    for rel_path in backend_files:
        file_path = backend_root / rel_path
        if file_path.exists():
            out.write(f"=== {rel_path} ===\n")
            try:
                out.write(file_path.read_text(encoding="utf-8"))
            except Exception as e:
                out.write(f"[Помилка читання файлу: {e}]")
            out.write("\n\n")
        else:
            print(f"[Backend] Файл не знайдено: {rel_path}")

print(f"Готово: {backend_output.name}")


# --- Функція побудови дерева (аналог команди tree) ---
def generate_tree(dir_path: Path, prefix: str = "") -> list[str]:
    lines = []
    # Сортуємо: спочатку папки, потім файли (в алфавітному порядку)
    items = sorted(list(dir_path.iterdir()), key=lambda x: (not x.is_dir(), x.name.lower()))
    total = len(items)

    for i, item in enumerate(items):
        is_last = (i == total - 1)
        connector = "└── " if is_last else "├── "
        lines.append(f"{prefix}{connector}{item.name}")

        if item.is_dir():
            extension = "    " if is_last else "│   "
            lines.extend(generate_tree(item, prefix + extension))

    return lines


# --- 2 & 3. Обробка другої папки (user marker/src) ---
if user_marker_src.exists() and user_marker_src.is_dir():
    # Файл 2: Дерево структури
    tree_output = desktop / "user_marker_tree.txt"
    tree_lines = [f"src/ ({user_marker_src})\n"]
    tree_lines.extend(generate_tree(user_marker_src))
    tree_output.write_text("\n".join(tree_lines), encoding="utf-8")
    print(f"Готово: {tree_output.name}")

    # Файл 3: Дамп усього коду з src
    src_combined_output = desktop / "user_marker_combined.txt"
    with open(src_combined_output, "w", encoding="utf-8") as out:
        # Рекурсивний обхід усіх файлів у src
        for file_path in sorted(user_marker_src.rglob("*")):
            if file_path.is_file():
                # Пропускаємо бінарні та службові файли за потреби (картинки, шрифти, кеш)
                if file_path.suffix.lower() in [".png", ".jpg", ".jpeg", ".webp", ".ico", ".svg", ".woff", ".woff2", ".ttf"]:
                    continue

                rel_path = file_path.relative_to(user_marker_src)
                out.write(f"=== src/{rel_path} ===\n")
                try:
                    out.write(file_path.read_text(encoding="utf-8"))
                except Exception as e:
                    out.write(f"[Помилка читання файлу: {e}]")
                out.write("\n\n")

    print(f"Готово: {src_combined_output.name}")
else:
    print(f"Папку не знайдено: {user_marker_src}")
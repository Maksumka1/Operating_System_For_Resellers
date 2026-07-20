
import sys
import sqlite3
from pathlib import Path
import os
import re
from datetime import datetime, timezone

PROJECT_ROOT = Path(__file__).resolve().parent
if not (PROJECT_ROOT / "config.py").exists():
    PROJECT_ROOT = PROJECT_ROOT.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from config import DB_FILE

# ANSI кольори для професійного оформлення терміналу
CLR_HEADER = "\033[95m"
CLR_BLUE = "\033[94m"
CLR_CYAN = "\033[96m"
CLR_GREEN = "\033[92m"
CLR_YELLOW = "\033[93m"
CLR_RED = "\033[91m"
CLR_RESET = "\033[0m"
CLR_BOLD = "\033[1m"


def get_db_connection():
    if not DB_FILE.exists():
        print(f"{CLR_RED}[ПОМИЛКА] Базу даних 'hardware.db' не знайдено за шляхом {DB_FILE}!{CLR_RESET}")
        print("Будь ласка, запустіть db_init.py та парсери перед використанням аналітики.")
        sys.exit(1)
    conn = sqlite3.connect(DB_FILE)
    conn.execute("PRAGMA journal_mode=WAL;")
    return conn


def clear_terminal():
    os.system("cls" if os.name == "nt" else "clear")


def print_title(text: str):
    print(f"\n{CLR_HEADER}{CLR_BOLD}" + "=" * 80)
    print(f"📊 {text.upper() : ^76} 📊")
    print("=" * 80 + f"{CLR_RESET}\n")


def press_any_key():
    print(f"\n{CLR_CYAN}" + "-" * 80 + f"{CLR_RESET}")
    input(f"{CLR_CYAN}Натисніть Enter, щоб повернутися до головного меню...{CLR_RESET}")


# =====================================================================
# 📊 1. ЗАГАЛЬНИЙ ЗРІЗ БАЗИ ДАНИХ
# =====================================================================
def show_global_summary():
    clear_terminal()
    print_title("Глобальний зріз бази даних")
    
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM ads")
    total_records = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM ads WHERE status = 'active'")
    active_records = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM ads WHERE status = 'deactivated'")
    archived_records = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM ads WHERE item_type = 'gpu' AND status = 'active'")
    active_gpus = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM ads WHERE item_type = 'cpu' AND status = 'active'")
    active_cpus = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM ads WHERE item_type = 'pc' AND status = 'active'")
    active_pcs = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM ads WHERE has_ban_word = 1")
    banned_ads = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM ads WHERE deal_status IN ('🔥 SUPER DEAL', '⭐ GOOD DEAL')")
    total_deals = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM ads WHERE deal_status = '🔥 SUPER DEAL' AND status = 'active'")
    active_super_deals = cursor.fetchone()[0]

    conn.close()

    print(f"{CLR_BOLD}📂 Загальний обсяг даних:{CLR_RESET}")
    print(f"  • Всього оголошень у базі:   {CLR_CYAN}{total_records}{CLR_RESET}")
    print(f"  • Активних зараз на OLX:     {CLR_GREEN}{active_records}{CLR_RESET}")
    print(f"  • Перебувають в архіві:      {CLR_YELLOW}{archived_records}{CLR_RESET}")
    print(f"  • Відсіяно фільтром (бан):   {CLR_RED}{banned_ads}{CLR_RESET}")
    
    print(f"\n{CLR_BOLD}🛍️ Розподіл АКТИВНОГО асортименту:{CLR_RESET}")
    print(f"  • Відеокарти (GPU):          {CLR_CYAN}{active_gpus}{CLR_RESET}")
    print(f"  • Процесори (CPU):           {CLR_CYAN}{active_cpus}{CLR_RESET}")
    print(f"  • Готові комп'ютери (PC):    {CLR_CYAN}{active_pcs}{CLR_RESET}")

    print(f"\n{CLR_BOLD}🔥 Рівень вигідності в базі:{CLR_RESET}")
    print(f"  • Всього знайдено хороших угод: {CLR_GREEN}{total_deals}{CLR_RESET}")
    print(f"  • Активних 🔥 SUPER DEAL зараз: {CLR_GREEN}{active_super_deals}{CLR_RESET}")

    press_any_key()


# =====================================================================
# 📈 2. АНАЛІЗ ЦІН НА КОМПЛЕКТУЮЧІ
# =====================================================================
def show_hardware_prices():
    clear_terminal()
    print_title("Ринкові ціни на комплектуючі")

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            component_name, 
            item_type,
            COUNT(*) as ad_count,
            MIN(price) as min_p,
            AVG(price) as avg_p,
            MAX(price) as max_p,
            AVG(competitor_price) as avg_comp
        FROM ads
        WHERE item_type IN ('gpu', 'cpu') AND status = 'active' AND price > 100 AND has_ban_word = 0
        GROUP BY component_name
        ORDER BY item_type DESC, component_name ASC
    """)
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        print(f"{CLR_YELLOW}Немає даних для розрахунку цін комплектуючих.{CLR_RESET}")
        press_any_key()
        return

    header = f"| {'Назва компонента' : <15} | {'Тип' : <4} | {'Обсяг' : <5} | {'Мін. ціна' : <9} | {'Сер. ціна' : <9} | {'Мода (Рин)' : <10} |"
    print(CLR_BOLD + "-" * len(header))
    print(header)
    print("-" * len(header) + CLR_RESET)

    for name, itype, count, min_p, avg_p, max_p, avg_comp in rows:
        name_str = name if name else "Невідомо"
        avg_p_clean = int(avg_p)
        comp_p_str = f"{int(avg_comp)} грн" if avg_comp and avg_comp > 0 else "Рахується"
        print(f"| {name_str : <15} | {itype.upper() : <4} | {count : ^5} | {min_p : >7} грн | {avg_p_clean : >7} грн | {comp_p_str : >10} |")

    print("-" * len(header))
    press_any_key()


# =====================================================================
# 🖥️ 3. АНАЛІТИКА ГОТОВИХ ПК ТА ШУКАЧ ГАРЯЧИХ УГОД
# =====================================================================
def show_pc_deals():
    clear_terminal()
    print_title("Аналітика готових ПК та вигідних угод")

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            title, seller_price_clean, estimated_fair_price, competitor_price,
            saving_uah, saving_percent, deal_status, url
        FROM ads
        WHERE item_type = 'pc' 
          AND status = 'active' 
          AND has_ban_word = 0
          AND estimated_fair_price IS NOT NULL
        ORDER BY saving_uah DESC
        LIMIT 10
    """)
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        print(f"{CLR_YELLOW}Немає активних оцінених комп'ютерів в базі.{CLR_RESET}")
        press_any_key()
        return

    print(f"{CLR_BOLD}Топ-10 найбільш вигідних комп'ютерів на ринку деталей:{CLR_RESET}\n")

    for i, (title, seller_p, fair_p, comp_p, saving, percent, status, url) in enumerate(rows, 1):
        if "SUPER" in status:
            status_color = CLR_RED + CLR_BOLD + status + CLR_RESET
        elif "GOOD" in status:
            status_color = CLR_GREEN + CLR_BOLD + status + CLR_RESET
        else:
            status_color = CLR_BLUE + status + CLR_RESET

        comp_str = f"{comp_p} грн" if comp_p and comp_p > 0 else "Немає схожих"
        print(f"{CLR_BOLD}{i}. {title[:65]}...{CLR_RESET}")
        print(f"  💸 Статус вигоди: {status_color}")
        print(f"  💵 Ціна продавця: {CLR_YELLOW}{seller_p} грн{CLR_RESET} | Собівартість деталей: {fair_p} грн")
        print(f"  🖥️ Середня ціна у конкурентів на OLX: {CLR_CYAN}{comp_str}{CLR_RESET}")
        print(f"  📈 Чистий профіт: +{CLR_GREEN}{saving} грн ({percent}%){CLR_RESET}")
        print(f"  🔗 Лінк:          {CLR_BLUE}{url}{CLR_RESET}")
        print("-" * 80)

    press_any_key()


# =====================================================================
# 🥊 4. [НОВЕ] АНАЛІТИКА КОНКУРЕНТНОГО СЕРЕДОВИЩА ДЛЯ ПК
# =====================================================================
def show_pc_competition_analysis():
    clear_terminal()
    print_title("Аналіз конкуренції готових збірок")

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            cpu_detected, gpu_detected,
            COUNT(*) as count,
            MIN(price) as min_p,
            AVG(price) as avg_p,
            MAX(price) as max_p
        FROM ads
        WHERE item_type = 'pc' AND status = 'active' AND gpu_detected IS NOT NULL AND cpu_detected IS NOT NULL
        GROUP BY cpu_detected, gpu_detected
        HAVING count > 1
        ORDER BY count DESC
        LIMIT 15
    """)
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        print(f"{CLR_YELLOW}Недостатньо обсягу даних для групування конкурентних зв'язок CPU+GPU.{CLR_RESET}")
        press_any_key()
        return

    print(f"{CLR_BOLD}Аналіз щільності ринку готових ПК за конфігураціями:{CLR_RESET}\n")
    header = f"| {'Процесор' : <12} | {'Відеокарта' : <12} | {'Збірок' : <6} | {'Мін. ціна' : <9} | {'Сер. ціна' : <9} | {'Макс. ціна' : <9} |"
    print(CLR_BOLD + "-" * len(header))
    print(header)
    print("-" * len(header) + CLR_RESET)

    for cpu, gpu, count, min_p, avg_p, max_p in rows:
        print(f"| {cpu[:12] : <12} | {gpu[:12] : <12} | {count : ^6} | {min_p : >7} грн | {int(avg_p) : >7} грн | {max_p : >7} грн |")
        
    print("-" * len(header))
    press_any_key()


# =====================================================================
# 🕵️‍♂️ 5. [НОВЕ] АУДИТ НАДІЙНОСТІ ПРОДАВЦІВ (Профайл ризиків)
# =====================================================================
def show_seller_risk_profiles():
    clear_terminal()
    print_title("Аудит надійності та типів продавців")

    conn = get_db_connection()
    cursor = conn.cursor()

    # Загальний розподіл за типами
    cursor.execute("""
        SELECT seller_type, COUNT(*), AVG(seller_successful_deals)
        FROM ads 
        WHERE seller_type IS NOT NULL AND status = 'active'
        GROUP BY seller_type
    """)
    types_data = cursor.fetchall()

    # Розподіл за рівнем ризику
    cursor.execute("""
        SELECT seller_risk_score, COUNT(*)
        FROM ads 
        WHERE seller_risk_score IS NOT NULL AND status = 'active'
        GROUP BY seller_risk_score
    """)
    risks_data = cursor.fetchall()
    conn.close()

    print(f"{CLR_BOLD}📊 Розподіл сил на ринку OLX (Хто продає залізо):{CLR_RESET}")
    for stype, count, avg_deals in types_data:
        type_name = "🧑‍💻 ПЕРЕКУПИ" if stype == "reseller" else "🏪 МАГАЗИНИ" if stype == "shop" else "👤 ПРИВАТНИКИ"
        print(f"  • {type_name : <15}: {CLR_CYAN}{count : <5}{CLR_RESET} активних лотів | Сер. кількість доставок: {CLR_YELLOW}{int(avg_deals or 0)} угод{CLR_RESET}")

    print(f"\n{CLR_BOLD}🛡️ Стан безпеки та надійності пропозицій:{CLR_RESET}")
    for srisk, count in risks_data:
        if srisk == "safe":
            risk_str = f"{CLR_GREEN}🟢 БЕЗПЕЧНІ (Акаунти > 2 років){CLR_RESET}"
        elif srisk == "suspicious":
            risk_str = f"{CLR_RED}🔴 ПІДОЗРІЛІ (Новореги / Без оцінок / Скам){CLR_RESET}"
        else:
            risk_str = f"{CLR_BLUE}🟡 НЕЙТРАЛЬНІ{CLR_RESET}"
        print(f"  • {risk_str : <45}: {CLR_BOLD}{count}{CLR_RESET} лотів")
        
    press_any_key()


# =====================================================================
# 👑 6. [НОВЕ] РЕЙТИНГ ТОП-ПРОДАВЦІВ ЗА ОБСЯГОМ УГОД
# =====================================================================
def show_top_sellers():
    clear_terminal()
    print_title("Рейтинг найбільших продавців")

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT seller_name, seller_id, seller_type, seller_rating, seller_successful_deals, COUNT(*) as active_ads
        FROM ads
        WHERE seller_id IS NOT NULL AND seller_id != 'failed' AND status = 'active'
        GROUP BY seller_id
        ORDER BY seller_successful_deals DESC
        LIMIT 10
    """)
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        print(f"{CLR_YELLOW}Немає проаналізованих профілів продавців у базі.{CLR_RESET}")
        press_any_key()
        return

    print(f"{CLR_BOLD}ТОП-10 лідерів продажів за кількістю успішних OLX Доставок:{CLR_RESET}\n")
    
    for i, (name, s_id, stype, rating, deals, ads_count) in enumerate(rows, 1):
        type_label = "МАГАЗИН" if stype == "shop" else "ПЕРЕКУП" if stype == "reseller" else "ПРИВАТНИК"
        print(f"{CLR_BOLD}{i}. {name} (ID: {s_id}) [{CLR_CYAN}{type_label}{CLR_RESET}]")
        print(f"   📦 Успішних доставок: {CLR_GREEN}{deals}{CLR_RESET} угод | Лотів у нашій базі: {ads_count} шт.")
        print(f"   ⭐ Рейтинг профілю:  {CLR_YELLOW}{rating}{CLR_RESET}")
        print("-" * 80)

    press_any_key()


# =====================================================================
# 🗺️ 7. ГЕОГРАФІЧНИЙ РОЗПОДІЛ
# =====================================================================
def show_geographical_stats():
    clear_terminal()
    print_title("Географія оголошень")

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT city, COUNT(*) as count, AVG(price) as avg_price
        FROM ads
        WHERE status = 'active' AND price > 100 AND city IS NOT NULL AND city != 'Невідомо'
        GROUP BY city
        ORDER BY count DESC
        LIMIT 10
    """)
    top_cities = cursor.fetchall()
    conn.close()

    if not top_cities:
        print(f"{CLR_YELLOW}Немає географічних даних для аналізу.{CLR_RESET}")
        press_any_key()
        return

    print(f"{CLR_BOLD}Топ-10 міст України за кількістю активних пропозицій:{CLR_RESET}\n")
    
    header = f"| {'Місто / Регіон' : <35} | {'Кількість' : <10} | {'Середній чек' : <14} |"
    print(CLR_BOLD + "-" * len(header))
    print(header)
    print("-" * len(header) + CLR_RESET)

    for city, count, avg_p in top_cities:
        clean_city = city.split(" - ")[0][:33]
        print(f"| {clean_city : <35} | {count : ^10} | {int(avg_p) : >10} грн |")

    print("-" * len(header))
    press_any_key()


# =====================================================================
# ⏱️ 8. АНАЛІЗ ШВИДКОСТІ ПРОДАЖІВ
# =====================================================================
def show_sales_speed():
    clear_terminal()
    print_title("Швидкість продажу заліза")

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT created_at_olx, deactivated_at, item_type
        FROM ads
        WHERE status = 'deactivated' AND deactivated_at IS NOT NULL AND created_at_olx IS NOT NULL AND created_at_olx != 'Невідомо'
    """)
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        print(f"{CLR_YELLOW}В архіві бази даних ще немає деактивованих товарів з мітками дат.{CLR_RESET}")
        press_any_key()
        return

    durations = []
    pc_durations = []
    gpu_durations = []
    cpu_durations = []

    for parsed, deactivated, itype in rows:
        try:
            # Очищаємо дати: parsed може бути як YYYY-MM-DD, так і рядком з OLX
            clean_p = parsed.split(" ")[0]
            if not re.match(r"\d{4}-\d{2}-\d{2}", clean_p):
                continue
                
            p_date = datetime.strptime(clean_p, "%Y-%m-%d")
            d_date = datetime.strptime(deactivated.split(" ")[0], "%Y-%m-%d")
            
            days = (d_date - p_date).days
            if days < 0: days = 0

            durations.append(days)
            if itype == "pc":
                pc_durations.append(days)
            elif itype == "gpu":
                gpu_durations.append(days)
            elif itype == "cpu":
                cpu_durations.append(days)
        except Exception:
            continue

    if not durations:
        print(f"{CLR_YELLOW}Не вдалося розпарсити мітки часу створення оголошень для аналізу.{CLR_RESET}")
        press_any_key()
        return

    print(f"{CLR_BOLD}📊 Аналітика швидкості продажів (на основі чистих дат OLX):{CLR_RESET}\n")
    print(f"  • Загалом зафіксовано продажів:       {CLR_GREEN}{len(durations)}{CLR_RESET} шт.")
    print(f"  • Середній час експозиції товару:     {CLR_CYAN}{sum(durations)/len(durations):.1f}{CLR_RESET} дн.")
    print(f"  • Найшвидший викуп лоту:              {CLR_GREEN}{min(durations)}{CLR_RESET} дн.")
    print(f"  • Максимальний термін продажу:        {CLR_YELLOW}{max(durations)}{CLR_RESET} дн.")

    print(f"\n{CLR_BOLD}📦 Швидкість реалізації за категоріями:{CLR_RESET}")
    if pc_durations:
        print(f"  • Готові комп'ютери (PC): {CLR_CYAN}{sum(pc_durations)/len(pc_durations):.1f}{CLR_RESET} днів (продано: {len(pc_durations)})")
    if gpu_durations:
        print(f"  • Відеокарти (GPU):       {CLR_CYAN}{sum(gpu_durations)/len(gpu_durations):.1f}{CLR_RESET} днів (продано: {len(gpu_durations)})")
    if cpu_durations:
        print(f"  • Процесори (CPU):        {CLR_CYAN}{sum(cpu_durations)/len(cpu_durations):.1f}{CLR_RESET} днів (продано: {len(cpu_durations)})")

    press_any_key()


# =====================================================================
# 🔄 9. [НОВЕ] ХРОНОЛОГІЧНИЙ АНАЛІЗ «СВІЖОСТІ» РИНКУ
# =====================================================================
def show_market_freshness():
    clear_terminal()
    print_title("Аналіз свіжості та активності ринку")

    conn = get_db_connection()
    cursor = conn.cursor()

    # Поточна дата у форматі SQL
    today_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    cursor.execute("SELECT COUNT(*) FROM ads WHERE parsed_date = ? AND status = 'active'", (today_str,))
    parsed_today = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM ads WHERE created_at_olx = ? AND status = 'active'", (today_str,))
    created_today = cursor.fetchone()[0]

    # Рахуємо скільки оголошень було оновлено (last_refresh_time) за останні 24 години
    cursor.execute("""
        SELECT COUNT(*) FROM ads 
        WHERE last_refresh_time LIKE ? AND status = 'active'
    """, (f"{today_str}%",))
    refreshed_today = cursor.fetchone()[0]
    conn.close()

    print(f"{CLR_BOLD}⏱️ Пульс ринку за сьогодні ({today_str}):{CLR_RESET}\n")
    print(f"  • Вперше знайдено нашим ботом сьогодні   : {CLR_GREEN}{parsed_today}{CLR_RESET} нових лотів")
    print(f"  • Опубліковано авторами на OLX сьогодні  : {CLR_CYAN}{created_today}{CLR_RESET} оголошень")
    print(f"  • Продавці підняли в ТОП (Refresh) сьогодні: {CLR_YELLOW}{refreshed_today}{CLR_RESET} разів")
    print(f"\n{CLR_BOLD}💡 Порада для перекупа:{CLR_RESET} Якщо показник оновлень суттєво перевищує нові публікації, "
          f"ринок перенасичений професійними продавцями (шопами/resellers), які масово демпінгують ціни.")
    
    press_any_key()


# =====================================================================
# 🔍 10. ПАРАМЕТРИЧНИЙ ПОШУК ТА ШВИДКИЙ ОЦІНЮВАЧ ЗАЛІЗА
# =====================================================================
def search_and_evaluate():
    clear_terminal()
    print_title("Параметричний пошук по базі")
    
    keyword = input("Введіть ключове слово для пошуку (наприклад, '1060' або 'ryzen'): ").strip().lower()
    if not keyword:
        return

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT title, price, status, seller_type, url 
        FROM ads 
        WHERE (LOWER(title) LIKE ? OR LOWER(description) LIKE ?)
          AND price > 100
        ORDER BY price ASC
        LIMIT 15
    """, (f"%{keyword}%", f"%{keyword}%"))
    
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        print(f"\n{CLR_RED}Нічого не знайдено за запитом '{keyword}'.{CLR_RESET}")
        press_any_key()
        return

    print(f"\n{CLR_BOLD}Знайдено {len(rows)} відповідних оголошень (сортування від найдешевших):{CLR_RESET}\n")
    
    for title, price, status, stype, url in rows:
        status_str = f"{CLR_GREEN}АКТИВНИЙ{CLR_RESET}" if status == "active" else f"{CLR_YELLOW}АРХІВ{CLR_RESET}"
        type_str = f" | {stype.upper()}" if stype else ""
        print(f"• {title[:65]}...")
        print(f"   Ціна: {CLR_YELLOW}{price} грн{CLR_RESET} | Статус: {status_str}{type_str}")
        print(f"   Лінк: {CLR_BLUE}{url}{CLR_RESET}\n")

    press_any_key()


# =====================================================================
# 📋 ГОЛОВНЕ ІНТЕРАКТИВНЕ МЕНЮ
# =====================================================================
def main_menu():
    while True:
        clear_terminal()
        print(f"{CLR_CYAN}{CLR_BOLD}" + "="*80)
        print(f"⚙️       PROFESSIONAL HARDWARE MARKET INTELLIGENCE DASHBOARD       ⚙️")
        print("="*80 + CLR_RESET)
        print(f"  {CLR_BLUE}1.{CLR_RESET} Глобальний зріз бази даних (Обсяги, ліміти, зріз угод)")
        print(f"  {CLR_BLUE}2.{CLR_RESET} Ринкові ціни комплектуючих (Мін / Сер / Мода ринку заліза)")
        print(f"  {CLR_BLUE}3.{CLR_RESET} Топ-10 найвигідніших комп'ютерів за маржою деталей")
        print(f"  {CLR_BLUE}4.{CLR_RESET} Аналіз конкуренції готових збірок (Щільність зв'язок CPU+GPU)")
        print(f"  {CLR_BLUE}5.{CLR_RESET} Аудит надійності продавців (Шопи / Перекупи / Аналіз ризиків)")
        print(f"  {CLR_BLUE}6.{CLR_RESET} ТОП-10 найбільших B2B лідерів продажів на OLX")
        print(f"  {CLR_BLUE}7.{CLR_RESET} Географія пропозицій (Обсяги міст та середні чеки заліза)")
        print(f"  {CLR_BLUE}8.{CLR_RESET} Швидкість ліквідності товарів (Аналітика часу життя оголошень)")
        print(f"  {CLR_BLUE}9.{CLR_RESET} Моніторинг активності та свіжості ринку (Пульс за сьогодні)")
        print(f"  {CLR_BLUE}10.{CLR_RESET} Параметричний пошук лотів з розширеними профілями")
        print(f"  {CLR_RED}0. Закрити аналітичну панель дашборду{CLR_RESET}")
        print(f"{CLR_CYAN}" + "="*80 + CLR_RESET)

        choice = input(f"{CLR_BOLD}Оберіть опцію (0-10): {CLR_RESET}").strip()

        if choice == "1": show_global_summary()
        elif choice == "2": show_hardware_prices()
        elif choice == "3": show_pc_deals()
        elif choice == "4": show_pc_competition_analysis()
        elif choice == "5": show_seller_risk_profiles()
        elif choice == "6": show_top_sellers()
        elif choice == "7": show_geographical_stats()
        elif choice == "8": show_sales_speed()
        elif choice == "9": show_market_freshness()
        elif choice == "10": search_and_evaluate()
        elif choice == "0":
            clear_terminal()
            print(f"\n{CLR_GREEN}Аналітичну панель успішно закрито. Профітних вам угод! 🚀{CLR_RESET}\n")
            break
        else:
            print(f"\n{CLR_RED}Неправильний вибір. Повторіть введення...{CLR_RESET}")
            import time
            time.sleep(1)


if __name__ == "__main__":
    main_menu()
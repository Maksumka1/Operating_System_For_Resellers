# 🐛 ДЕБАГ-ЗВІТ ПАРСИНГУ ГОТОВИХ ПК (OLX Category 78)
**Дата та час запуску:** 2026-08-03 23:02:26
**Тривалість виконання:** 116.81 сек
**Шлях до звіту:** `C:\Users\marke\OneDrive\Desktop\Operating_System\debug\debug_report_parse_pc.md`

## 📌 1. Задача та мета коду
Основна мета: асинхронний збір оголошень готових ПК та системних блоків з OLX GraphQL API.
1. Запит до категорії 78 (Комп'ютери та комплектуючі / ПК).
2. Перевірка на дублікати за URL серед збережених раніше оголошень у Supabase.
3. Фільтрація поодиноких комплектуючих/запчастин за допомогою функції `is_real_pc` та стоп-слів (`NOT_A_PC_WORDS`).
4. Парсинг цін, продавця (тип: shop/private), локації, фотографій та дат.
5. Масовий `upsert` нових лотів у таблицю `ads` та надсилання тригеру для WebSocket-стріму.

## 📊 2. Загальна статистика вхідних даних та відсіювання
### ⚙️ Секція: Supabase_Input
- **Завантажено URLs для дедуплікації:** 13691

### ⚙️ Секція: OLX_GraphQL
- **Отримано сирих оголошень ПК:** 259

### ⚙️ Секція: Filtering_Rules
- **Відсіяно if (Дублікат URL в DB):** 245
- **Відсіяно if (Спрацював фільтр запчастин is_real_pc):** 5

### ⚙️ Секція: Parsing_Metrics
- **Успішно розпаршено ПК:** 9

### ⚙️ Секція: Summary
- **Знайдено нових ПК:** 9
- **Пропущено дублікатів:** 245
- **Немає нових лотів для відправки:** 1

### ⚙️ Секція: Supabase_Output
- **Успішно збережено в DB:** 9

### ⚙️ Секція: WebSocket
- **Успішно тригернуто живий стрім:** 1

## 🔄 3. Детальні приклади даних
### 🔹 Відсіяні оголошення (запчастини, окремі комплектуючі, дублікати) (Показано 100 з max 100):
**Семпл #1:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/rozprodazh-robochih-stantsy-hp-z4-g4-s2066-dell-precision-3420-3620-3640-hp-z420-cmt-s2011-pk-opt-kiv-samovivz-garantya-ID10fEAz.html",
  "title": "РОЗПРОДАЖ Робочих станцій HP Z4 G4 s2066, Dell Precision 3420/3620/3640, HP Z420 CMT s2011 • ПК ОПТ  КИЇВ Самовивіз • Гарантія !"
}
```
**Семпл #2:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/groviy-pk-gtx-1080ti-11gb-ryzen-5-3600-16gb-512-ssd-kompyuter-ID10V6ND.html",
  "title": "Ігровий ПК | GTX 1080Ti 11gb | Ryzen 5 3600 | 16GB/512 SSD | Комп'ютер"
}
```
**Семпл #3:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/groviy-kompyuter-pk-zbrka-ryzen-5-5500-rx-5700xt-16gb-ddr4-ssd-m2-nvme-500gb-ID10P9H3.html",
  "title": "Ігровий Компʼютер ПК Збірка Ryzen 5 5500 | RX 5700XT | 16GB DDR4 | SSD M2 Nvme 500gb"
}
```
**Семпл #4:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/sistemniy-blok-hp-prodesk-600g5-sff-i5-9500-8gbddr4-ssd256gb-nvme-kompyuter-ID10azJk.html",
  "title": "Системний блок Hp ProDesk 600G5 sff i5-9500/8gbddr4/ssd256gb nvme комп'ютер"
}
```
**Семпл #5:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/potuzhniy-pk-ryzen-9-5950x-rtx-4060-32gb-ssd-1tb-mayzhe-ne-vikoristovuvavsya-ID10V3pt.html",
  "title": "Потужний ПК Ryzen 9 5950X / RTX 4060 / 32GB / SSD 1TB — майже не використовувався"
}
```
**Семпл #6:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/kompyuter-sistemnyy-blok-pk-kopmlekty-opt-komptyutery-beznal-usdt-IDXE437.html",
  "title": "Компьютер Системный блок ПК копмлекты Опт! Комптютеры БЕЗНАЛ/USDT"
}
```
**Семпл #7:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/monoblok-dell-7450-i5-6500-16ddr4-256ssd-touchscreen-trsnutiyrobochiy-bez-lapi-IDZomg9.html",
  "title": "Моноблок DELL 7450 i5-6500/16DDR4/256SSD/touchscreen Тріснутий(робочий)/ без Лапи"
}
```
**Семпл #8:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/prodam-pk-ryzen-5-5500-16-gb-ddr4-rx580-8gb-m2-ssd-IDXyHaK.html",
  "title": "Продам ПК Ryzen 5 5500 | 16 Gb DDR4  | RX580 8Gb | M2 SSD |"
}
```
**Семпл #9:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/prodam-sistemniy-blok-IDZxy6L.html",
  "title": "Продам системний блок"
}
```
**Семпл #10:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/groviy-pk-ryzen-5-3600-gtx-1660-6gb-16gb-ram-ssd-240gb-ID10YFbv.html",
  "title": "Ігровий ПК Ryzen 5 3600 / GTX 1660 6GB / 16GB RAM / SSD 240GB"
}
```
**Семпл #11:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/suchasniy-groviy-pk-IDYrGLm.html",
  "title": "Сучасний ігровий ПК"
}
```
**Семпл #12:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/prodam-komp-ryzen-5-8400f-5060ti-16-gb-ID10Y4Kk.html",
  "title": "Продам комп Ryzen 5 8400F + 5060TI 16 GB !"
}
```
**Семпл #13:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/korol-i7-gtx-1660s-16gb-1tb-groviy-kompyuter-igrovoy-kompyuter-pk-IDVvPaX.html",
  "title": "КОРОЛЬ i7/GTX 1660s/16gb/1tb Ігровий комп’ютер игровой компьютер пк"
}
```
**Семпл #14:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/igrovoy-pk-rtx-3070ti-ryzen-7-8700f-ddr5-32gb-ID10RwHi.html",
  "title": "Игровой ПК / RTX 3070TI / Ryzen 7 8700f / DDR5 32GB"
}
```
**Семпл #15:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/kompaktniy-pk-u-horoshomu-stan-ID10IPxQ.html",
  "title": "Компактний ПК у хорошому стані"
}
```
**Семпл #16:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/sistemniy-blok-dell-intel-i3-ID10NZa7.html",
  "title": "Системний блок Dell, Intel i3"
}
```
**Семпл #17:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/prodam-kompyuter-montor-IDVWH6l.html",
  "title": "Продам компʼютер і монітор"
}
```
**Семпл #18:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/prodam-kompyuter-IDZ5csi.html",
  "title": "Продам компютер"
}
```
**Семпл #19:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/zaryadki-yusb-novye-IDVWGZs.html",
  "title": "зарядки  юсб новые"
}
```
**Семпл #20:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/sstemniy-blok-v-IDSv6q4.html",
  "title": "Сістемний блок в"
}
```
**Семпл #21:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/sistemniy-blok-intel-e6500-2yadra-8gb-250gb-IDSMHFX.html",
  "title": "системний блок Intel E6500/2ядра/8Gb/250Gb"
}
```
**Семпл #22:**
```json
{
  "reason": "starts_with_banned_word: мать",
  "title": "Мать проц+озу+блок живлення"
}
```
**Семпл #23:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/sistemniy-blok-delux-amd-4gb-op-ddr3-160gb-hdd-kompyuter-sistemnik-pk-dop-pitanie-dlya-videokarty-ID10CVko.html",
  "title": "Системний блок DELUX AMD/4GB ОП DDR3/160GB HDD Компьютер системник ПК доп питание для видеокарты"
}
```
**Семпл #24:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/kompyuter-groviy-grafchna-stantsya-IDVhaV3.html",
  "title": "Комп'ютер ігровий, графічна станція."
}
```
**Семпл #25:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/groviy-pk-intel-i5-2400-4x3-4mhz-nvidia-gtx-750-4gb-8-ozu-IDZPdbW.html",
  "title": "Ігровий ПК Intel i5 2400 4x3,4MHz, Nvidia GTX 750 4GB, 8 ОЗУ"
}
```
**Семпл #26:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/prodazh-pk-r5-5600x-rtx-306012gb-ID10OLGf.html",
  "title": "Продаж ПК R5 5600x+rtx 3060(12gb)"
}
```
**Семпл #27:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/touch-monoblok-lenovo-thinkcentre-neo-50a-g5-i5-13-16-512-fhd-2024r-ID10mbxJ.html",
  "title": "Touch/Моноблок Lenovo ThinkCentre Neo 50a g5/i5-13/16/512/FHD/2024р."
}
```
**Семпл #28:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/prodam-proizvoditelnyy-sistemnyy-blok-polnostyu-gotovyy-k-lyubym-sovremennym-igram-na-ultra-nastroykah-v-high-fps-i-tyazhelym-rabochim-zadacham-ID10XPbE.html",
  "title": "Продам производительный системный блок, полностью готовый к любым современным играм на ультра-настройках в high-FPS и тяжелым рабочим задачам."
}
```
**Семпл #29:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/prodayu-sistemniy-blok-IDYfqaZ.html",
  "title": "Продаю системний блок"
}
```
**Семпл #30:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/novyy-moschnyy-pk-itx-kompyuter-ryzen-4350g-v-superkorpuse-in-win-b1-IDLEa47.html",
  "title": "Новый мощный ПК ITX компьютер Ryzen 4350g в суперкорпусе In Win B1"
}
```
**Семпл #31:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/montor-kompyuterniy-samsung-IDTVFnL.html",
  "title": "Монітор комп'ютерний Samsung"
}
```
**Семпл #32:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/kompyuter-dlya-navchannya-ta-roboti-IDZuqZ1.html",
  "title": "Компьютер для навчання та роботи"
}
```
**Семпл #33:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/kompyuter-4yadra-8gb-ssd256-bzh-550vt-r7-360-2gb-IDXm9J3.html",
  "title": "Комп'ютер 4ядра, 8гб, ssd256, бж 550вт, р7 360 2гб"
}
```
**Семпл #34:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/prodatsya-kompyuter-ID10Zxtl.html",
  "title": "Продається комп’ютер"
}
```
**Семпл #35:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/pk-na-i5-12400f-rtx-4060-ddr5-garant-abo-obmn-rossrochka-IDYIpjS.html",
  "title": "Пк на i5 12400f + rtx 4060 + ddr5 (гарантіі) або ОБМІН (россрочка)"
}
```
**Семпл #36:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/groviy-kompyuter-rtx-4060-aero-white-i5-11400f-16gb-ram-ID10Okmd.html",
  "title": "Ігровий комп’ютер RTX 4060 AERO White / i5-11400F / 16GB RAM"
}
```
**Семпл #37:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/kompyuter-v-horoshem-sostoyanii-ID10CVbo.html",
  "title": "Комп'ютер в хорошем состоянии"
}
```
**Семпл #38:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/groviy-pk-rtx3080-r5-8400f-ID10fnUo.html",
  "title": "Ігровий ПК rtx3080+r5 8400f"
}
```
**Семпл #39:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/top-pk-premum-rvnya-i7-14700kf-rtx-4070-ti-super-16gb-64gb-ddr5-ID10Msnf.html",
  "title": "ТОП ПК преміум-рівня i7-14700KF | RTX 4070 Ti Super 16GB | 64GB DDR5"
}
```
**Семпл #40:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/antminer-l9-16-gh-s-ID10WVwg.html",
  "title": "Antminer L9 16 GH/s"
}
```
**Семпл #41:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/sistemniy-blok-dell-optiplex-3040-micro-usff-core-i3-6100t-8-gb-128-gb-ssd-kompyuter-nettop-ID10nZuS.html",
  "title": "Системний блок Dell OptiPlex 3040 Micro USFF Core i3-6100T 8 GB  128 GB SSD  комп'ютер неттоп"
}
```
**Семпл #42:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/groviy-kompyuter-ryzen-5-gtx-1060-6gb-16-gb-ssd-m2-500gb-ID10YK17.html",
  "title": "Ігровий компютер Ryzen 5 GTX 1060 6GB 16 GB ssd m2 500gb"
}
```
**Семпл #43:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/pk-core-i7-3770-16-gb-ddr3-ssd-256-gb-bp650-ID10Zxp0.html",
  "title": "ПК core i7 3770, 16 gb ddr3, ssd 256 gb, БП650"
}
```
**Семпл #44:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/mn-pk-nuc8i3-intel-nuc-nuc8i3beh2-ID107E7F.html",
  "title": "Міні ПК NUC8i3 , Intel NUC NUC8i3BEH2"
}
```
**Семпл #45:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/lenovo-thinkcentre-m910q-ID10ZxnL.html",
  "title": "Lenovo ThinkCentre M910q"
}
```
**Семпл #46:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/moschnyy-igrovoy-pk-rtx-4070-r5-5600-64gb-ram-2tb-ssd-b-w-design-idealnoe-sostoyanie-ID10ALEf.html",
  "title": "Мощный Игровой ПК - RTX 4070 / R5 5600 / 64GB RAM / 2TB SSD | B&W - Design | Идеальное Состояние!"
}
```
**Семпл #47:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/mn-pk-nuc5-mn-kompyuter-intel-nuc5cpyh-IDZns9P.html",
  "title": "Міні ПК NUC5 міні-комп’ютер Intel NUC5CPYH"
}
```
**Семпл #48:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/groviy-kompyuter-IDZitbw.html",
  "title": "Ігровий комп'ютер"
}
```
**Семпл #49:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/groviy-pk-gtx-1660-super-i3-10100-16gb-ram-nvme-ssd-ID102Slw.html",
  "title": "Ігровий ПК: GTX 1660 Super / i3-10100 / 16GB RAM / NVMe SSD"
}
```
**Семпл #50:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/asus-maximus-xii-apex-s1200-IDUKUha.html",
  "title": "Asus Maximus XII Apex s1200"
}
```
**Семпл #51:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/staryy-pk-na-zapchasti-ili-pod-pochinku-IDYDSF4.html",
  "title": "Старый ПК, на запчасти или под починку"
}
```
**Семпл #52:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/igrovoy-pk-rtx-4060-ti-8gb-64-gb-ram-2-5-tb-pamyati-otlichnoe-sostoyanie-ID10Txqw.html",
  "title": "Игровой ПК RTX 4060 Ti 8GB / 64 ГБ RAM / 2.5 ТБ памяти / Отличное состояние"
}
```
**Семпл #53:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/mn-pk-nettop-hp-elitedesk-800-g4-65w-i5-8500-8gb-240gb-ssd-bzh-IDZuQyc.html",
  "title": "Міні ПК nettop HP EliteDesk 800 G4 65W i5-8500/8Gb/240Gb SSD БЖ"
}
```
**Семпл #54:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/pk-amd-9950x-4070ti-super-128gb-ddr5-ID10XfxL.html",
  "title": "ПК AMD 9950X 4070TI SUPER 128GB DDR5"
}
```
**Семпл #55:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/groviy-pk-rtx3080-r5-8400f-ID10fnUo.html",
  "title": "Ігровий ПК rtx3080+r5 8400f"
}
```
**Семпл #56:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/groviy-kompyuter-ryzen-5-gtx-1060-6gb-16-gb-ssd-m2-500gb-ID10YK17.html",
  "title": "Ігровий компютер Ryzen 5 GTX 1060 6GB 16 GB ssd m2 500gb"
}
```
**Семпл #57:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/pk-core-i7-3770-16-gb-ddr3-ssd-256-gb-bp650-ID10Zxp0.html",
  "title": "ПК core i7 3770, 16 gb ddr3, ssd 256 gb, БП650"
}
```
**Семпл #58:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/mn-pk-nuc8i3-intel-nuc-nuc8i3beh2-ID107E7F.html",
  "title": "Міні ПК NUC8i3 , Intel NUC NUC8i3BEH2"
}
```
**Семпл #59:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/lenovo-thinkcentre-m910q-ID10ZxnL.html",
  "title": "Lenovo ThinkCentre M910q"
}
```
**Семпл #60:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/moschnyy-igrovoy-pk-rtx-4070-r5-5600-64gb-ram-2tb-ssd-b-w-design-idealnoe-sostoyanie-ID10ALEf.html",
  "title": "Мощный Игровой ПК - RTX 4070 / R5 5600 / 64GB RAM / 2TB SSD | B&W - Design | Идеальное Состояние!"
}
```
**Семпл #61:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/mn-pk-nuc5-mn-kompyuter-intel-nuc5cpyh-IDZns9P.html",
  "title": "Міні ПК NUC5 міні-комп’ютер Intel NUC5CPYH"
}
```
**Семпл #62:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/groviy-kompyuter-IDZitbw.html",
  "title": "Ігровий комп'ютер"
}
```
**Семпл #63:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/groviy-pk-gtx-1660-super-i3-10100-16gb-ram-nvme-ssd-ID102Slw.html",
  "title": "Ігровий ПК: GTX 1660 Super / i3-10100 / 16GB RAM / NVMe SSD"
}
```
**Семпл #64:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/asus-maximus-xii-apex-s1200-IDUKUha.html",
  "title": "Asus Maximus XII Apex s1200"
}
```
**Семпл #65:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/groviy-kompyuter-rtx-4090-suprim-liquid-x-intel-core-i9-13900kf-asus-rog-maximus-z790-hero-kingston-fury-32gb-6000-mt-s-ID10AUtb.html",
  "title": "Ігровий компютер RTX 4090 Suprim Liquid X + Intel Core i9-13900KF + ASUS ROG Maximus Z790 Hero + Kingston Fury 32GB 6000 MT/s"
}
```
**Семпл #66:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/kompyuter-sistemniy-blok-kompyuter-z-skladu-komplekti-kompyuteri-IDYa1Si.html",
  "title": "Компʼютер, системний блок, компютер зі складу Комплекти, Компʼютери"
}
```
**Семпл #67:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/staryy-pk-na-zapchasti-ili-pod-pochinku-IDYDSF4.html",
  "title": "Старый ПК, на запчасти или под починку"
}
```
**Семпл #68:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/proizvoditelnyy-pk-ryzen-7-2700x-16gb-ram-ssd-600gb-gtx-950-ID10ZxhI.html",
  "title": "Производительный ПК Ryzen 7 2700X / 16GB RAM / SSD 600GB / GTX 950"
}
```
**Семпл #69:**
```json
{
  "reason": "starts_with_banned_word: hdd",
  "title": "HDD 500 Гб Maxtor STM3500320AS з бед блоками"
}
```
**Семпл #70:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/igrovoy-kompyuter-geforce-gtx-1650-super-ryzen-5-3600-IDYrGiW.html",
  "title": "Игровой компьютер, Geforce Gtx 1650 super, ryzen 5 3600"
}
```
**Семпл #71:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/groviy-pk-i5-10400f-gtx-1660-super-16gb-ssd-500gb-windows-11-ID10YKZj.html",
  "title": "Ігровий ПК i5-10400F / GTX 1660 Super / 16GB / SSD 500GB / Windows 11"
}
```
**Семпл #72:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/kompyuter-robochiy-ID10Zxgg.html",
  "title": "Компʼютер робочий"
}
```
**Семпл #73:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/obmnyayu-kompyuter-groviy-na-noutbuk-groviy-IDZSeEo.html",
  "title": "Обміняю  компьютер ігровий на ноутбук ігровий"
}
```
**Семпл #74:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/prodatsya-kompyuter-IDW32Nk.html",
  "title": "Продається Комп'ютер!!!"
}
```
**Семпл #75:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/rtx-5090-ssd-2tb-sistemniy-blok-kompyuter-ID10Zx7V.html",
  "title": "RTX 5090 SSD 2Tb системний блок комп'ютер"
}
```
**Семпл #76:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/prodam-sistemniy-blok-pk-IDWfOxN.html",
  "title": "Продам системний блок ПК"
}
```
**Семпл #77:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/groviy-pk-expert-pc-ultimate-u-podaronuok-klavatura-ta-misha-intel-core-i5-12400f-32gb-ram-rtx-5060-ssd-1tb-ID10U706.html",
  "title": "Ігровий ПК Expert PC Ultimate + у подаронуок клавіатура та миша (Intel Core i5-12400F / 32GB RAM / RTX 5060 / SSD 1TB)"
}
```
**Семпл #78:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/prodam-groviy-pk-ryzen-5-8400f-rtx-5060-8gb-32gb-ddr5-ssd-1tb-ID10HcUp.html",
  "title": "Продам ігровий ПК Ryzen 5 8400F / RTX 5060 8GB / 32GB DDR5 / SSD 1TB"
}
```
**Семпл #79:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/igrovoy-ppk-kompyuter-nvidia-geforce-rtx-4060-ti-16-ID10WnDT.html",
  "title": "Игровой ппк Компьютер Nvidia GeForce RTX 4060 ti 16"
}
```
**Семпл #80:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/serverniy-pk-dual-xeon-e5-2697-v4-rtx-3060-128gb-ecc-ID10V4SX.html",
  "title": "Серверний ПК Dual Xeon E5-2697 v4 | RTX 3060 | 128GB ECC"
}
```
**Семпл #81:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/sistemniy-blok-amd-athlon-ii-245-22-2-9-ghz-65w-IDYKx0N.html",
  "title": "Системний блок AMD Athlon II 245 2*2 2,9 GHz 65W"
}
```
**Семпл #82:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/prodam-pk-na-ryzen-5500-ID10Zxbb.html",
  "title": "Продам ПК на Ryzen 5500"
}
```
**Семпл #83:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/nedorogiy-pk-dlya-ofisa-navchannya-nternetu-gotoviy-do-roboti-IDZisZj.html",
  "title": "Недорогий ПК для офиса, навчання, інтернету- готовий до роботи."
}
```
**Семпл #84:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/kompyuter-povniy-komplkt-IDYfpKl.html",
  "title": "Комп'ютер повний комплєкт"
}
```
**Семпл #85:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/igrovoy-pk-ryzen-5-5600x-rtx-3070-gigabyte-32-gb-ssd-nvme-1-tb-ID10VstY.html",
  "title": "Игровой ПК Ryzen 5 5600X | RTX 3070 Gigabyte | 32 ГБ | SSD NVMe 1 ТБ"
}
```
**Семпл #86:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/okremo-takozh-ves-komplekt-kompyuter-2-montori-mishka-klavatura-ID10XbCN.html",
  "title": "ОКРЕМО ТАКОЖ. Весь комплект компʼютер, 2 монітори, мишка, клавіатура"
}
```
**Семпл #87:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/bliy-lev-rtx-5060-ti-8gb-ryzen-5-9600-ddr5-16gb-m-2-ssd-500gb-groviy-kompyuter-pk-dlya-gor-geymerskiy-igrovoy-kompyuter-ID10CWP2.html",
  "title": "Білий Лев! RTX 5060 Ti 8GB+Ryzen 5 9600+DDR5 16GB+M.2 SSD 500GB –  Ігровий комп'ютер ПК для ігор геймерський игровой компьютер"
}
```
**Семпл #88:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/kompyuter-sistemniy-blok-ta-montor-intel-core-2-duo-e6600-ID10pDQd.html",
  "title": "Компьютер Системний блок та монітор Intel Core 2 Duo E6600"
}
```
**Семпл #89:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/kompyuter-dlya-roboti-abo-dlya-navchannya-ID10fbMg.html",
  "title": "Комп'ютер для роботи, або для навчання"
}
```
**Семпл #90:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/prodam-kompyuter-ID10hPL0.html",
  "title": "Продам компютер."
}
```
**Семпл #91:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/2600-mayner-bitmain-antminer-s21-hydro-358th-v-nayavnost-IDZede7.html",
  "title": "2600$ Майнер Bitmain Antminer S21+ HYDRO 358Th В наявності!"
}
```
**Семпл #92:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/imac-27-5k-2019-i5-8600-32-1tb-ssd-radeon-pro-575x-4gb-ID10O5D1.html",
  "title": "iMac 27\" 5K • 2019 •i5-8600 • 32/1TB SSD • Radeon Pro 575X 4GB"
}
```
**Семпл #93:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/mayning-ferma-7h1080-7-videokart-gigabit-gaming-gtx-1080-IDOFxj3.html",
  "title": "Майнинг ферма 7х1080 7 видеокарт Gigabit Gaming GTX-1080"
}
```
**Семпл #94:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/noviy-kompyuter-sff-lenovo-ideacentre-tower-ryzen-7-ID10ZvOT.html",
  "title": "Новий компютер SFF Lenovo IdeaCentre Tower ryzen 7"
}
```
**Семпл #95:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/medichniy-monoblok-athena-a219i-aio-21-5-ips-led-core-i5-7200u-8gb-120gb-b-u-bez-nogi-ID10NR0h.html",
  "title": "Медичний моноблок athena A219i AIO 21.5\" IPS LED (Core i5-7200U/8GB/120GB) б/у без ноги"
}
```
**Семпл #96:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/topoviy-pk-ryzen-9-9950x3d-asus-rog-astral-rtx-5090-oc-64gb128gb-4tb-m2-ID10Rtnn.html",
  "title": "Топовий ПК Ryzen 9 9950X3D / ASUS ROG Astral RTX 5090 OC / 64GB(128GB) / 4TB M2"
}
```
**Семпл #97:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/moschnyy-pk-ryzen-5-5600-rtx5060-32gb-ram-stalker2-cs2-rust-pubg-gtav-ID10fIeo.html",
  "title": "Мощный Пк Ryzen 5 5600 RTX5060 32gb ram Stalker2 Cs2 RusT PubG GtaV"
}
```
**Семпл #98:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/kompyuter-hp-prodesk-600-g4-sff-i5-8500-16gb-ram-ssd-256gb-ID10CTzj.html",
  "title": "Комп’ютер HP ProDesk 600 G4 SFF • i5 8500 • 16GB RAM • SSD 256GB"
}
```
**Семпл #99:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/personalniy-kompyuter-ID10pPEO.html",
  "title": "Персональний комп'ютер"
}
```
**Семпл #100:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/prodam-montor-ta-sistemniy-blok-IDKpFqr.html",
  "title": "Продам монітор та системний блок."
}
```

### 🔹 Валідовані оголошення ПК (пройшли перевірку is_real_pc) (Показано 9 з max 100):
**Семпл #1:**
```json
{
  "ad_id": 930563159,
  "title": "Ігровий компьютер",
  "status": "passed_is_real_pc"
}
```
**Семпл #2:**
```json
{
  "ad_id": 930525944,
  "title": "Ігровий Комп на 1080ті 11Гб, Системний блок, ПК",
  "status": "passed_is_real_pc"
}
```
**Семпл #3:**
```json
{
  "ad_id": 930166894,
  "title": "Ігровий системний блок(gtx 960 turbo,16gb ram)",
  "status": "passed_is_real_pc"
}
```
**Семпл #4:**
```json
{
  "ad_id": 930270066,
  "title": "Ігровий ПК Ryzen 3 3100 + RX 6600 8GB | 16GB RAM | SSD 2TB",
  "status": "passed_is_real_pc"
}
```
**Семпл #5:**
```json
{
  "ad_id": 914294690,
  "title": "Intel i5-3470 3.6ghz 4ядра/16gb озу системний блок компьютер",
  "status": "passed_is_real_pc"
}
```
**Семпл #6:**
```json
{
  "ad_id": 916990510,
  "title": "Asic Antminer S21+ Hydro 358 Th, нові в наявності, Aml, асік, майнер",
  "status": "passed_is_real_pc"
}
```
**Семпл #7:**
```json
{
  "ad_id": 929705117,
  "title": "Игровой Компьютер | DDR4 16Gb  | Видеокарта NVIDIA GeForce RTX 2080 | SSD 500 |",
  "status": "passed_is_real_pc"
}
```
**Семпл #8:**
```json
{
  "ad_id": 929134323,
  "title": "Пк під ваш бюджет. Як і новий так і б/в. Ігровий так і офісний",
  "status": "passed_is_real_pc"
}
```
**Семпл #9:**
```json
{
  "ad_id": 929311238,
  "title": "Ігровий ПК в чудовому стані",
  "status": "passed_is_real_pc"
}
```

============================================================

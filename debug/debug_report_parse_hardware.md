# 🐛 ДЕБАГ-ЗВІТ ПАРСИНГУ КОМПЛЕКТУЮЧИХ OLX (GraphQL)
**Дата та час запуску:** 2026-08-03 23:02:26
**Тривалість виконання:** 178.53 сек
**Шлях до звіту:** `C:\Users\marke\OneDrive\Desktop\Operating_System\debug\debug_report_parse_hardware.md`

## 📌 1. Задача та мета коду
Основна мета: асинхронний збір свіжих оголошень комплектуючих з OLX (GraphQL API).
1. Отримання оголошень по підкатегоріях (відеокарти, процесори, материнські плати, БЖ, накопичувачі).
2. Фільтрація дублікатів за URL та перевірка приналежності до підкатегорії.
3. Сувора ідентифікація моделі заліза (`match_ad_to_hardware_target`) з очищенням порівняльних фраз.
4. Детекція сокетів, перевірка на дефекти/неробочий стан (`is_broken_ad`) та розпарсинг фото/продавця.
5. Відправка готових записів у Supabase (`ads`) та тригер WebSocket стріму.

## 📊 2. Загальна статистика вхідних даних та відсіювання
### ⚙️ Секція: Supabase_Input
- **Завантажено URLs для дедуплікації:** 13700

### ⚙️ Секція: Parser_Config
- **Цільових моделей комплектуючих:** 10594

### ⚙️ Секція: OLX_GraphQL
- **Отримано оголошень [videokarty]:** 208
- **Отримано оголошень [protsessory]:** 258
- **Отримано оголошень [materinskie-platy]:** 260
- **Отримано оголошень [bloki-pitaniya]:** 257
- **Отримано оголошень [zhestkie-diski]:** 256
- **Отримано оголошень [moduli-pamyati]:** 259

### ⚙️ Секція: Filtering_Rules
- **Відсіяно if (Не розпізнано модель заліза):** 526

### ⚙️ Секція: Parsing_Metrics
- **Успішно розпізнано [gpu]:** 1
- **Успішно розпізнано [cpu]:** 1
- **Успішно розпізнано [motherboard]:** 1
- **Виявлено товарів з дефектами:** 1
- **Успішно розпізнано [storage]:** 1

### ⚙️ Секція: Summary
- **Знайдено нових унікальних оголошень:** 4
- **Немає нових оголошень для відправки в DB:** 1

### ⚙️ Секція: Supabase_Output
- **Успішно збережено нових оголошень:** 4

### ⚙️ Секція: WebSocket
- **Успішно надіслано тригер стріму:** 1

### ⚙️ Секція: Network
- **HTTP 403 (Блокування videokarty):** 3
- **HTTP 403 (Блокування protsessory):** 2

## 🔄 3. Детальні приклади даних
### 🚫 Відсіяні оголошення (по 100 прикладів для кожної категорії):
#### 🎮 Відеокарти (GPU) — Відсіяно (Показано 100 з max 100):
**Семпл #1:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/ventilyatori-asus-rog-strix-tuf-t129215su-20-60-70-80-3070-3080-3090-IDTQGpV.html",
  "title": "Вeнтилятори ASUS ROG/STRIX/TUF T129215SU 20 60/70/80 3070/3080/3090"
}
```
**Семпл #2:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/vdeokarta-msi-ventus-3x-plus-geforce-rtx-3080vdeokarta-msi-geforce-rtx-3080-ven-ID10KjOz.html",
  "title": "Відеокарта MSI Ventus 3X Plus Geforce RTX 3080\nВідеокарта MSI GeForce RTX 3080 VEN"
}
```
**Семпл #3:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/videokarta-rx9070-xt-red-devil-na-garantii-ID10ThRg.html",
  "title": "Видеокарта RX9070 XT Red Devil (на гарантии)"
}
```
**Семпл #4:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/asus-tuf-gaming-geforce-gtx-1660-super-6gb-v-idealnom-sostoyanii-ID10XZge.html",
  "title": "ASUS TUF Gaming GeForce GTX 1660 SUPER 6GB в идеальном состоянии"
}
```
**Семпл #5:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/vdeokarta-gigabyte-geforce-gtx-1080-ti-aorus-11g-b-v-garantya-3-msyats-ID10XVEW.html",
  "title": "Відеокарта GIGABYTE GeForce GTX 1080 Ti AORUS 11G Б/в + Гарантія 3 місяці!"
}
```
**Семпл #6:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Продам відеокарту MSI RTX 3060 VENTUS 12 Gb",
  "item_type": "gpu"
}
```
**Семпл #7:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/na-garantii-ideal-polnyy-komplekt-msi-rtx-5090-32gb-ventus-3x-oc-ID10VDQB.html",
  "title": "на гарантии, идеал, полный комплект MSI RTX 5090 32GB VENTUS 3X OC"
}
```
**Семпл #8:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/vdeokarta-gts-250-IDZqPwU.html",
  "title": "Відеокарта Gts 250"
}
```
**Семпл #9:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/vdeokarta-rtx3090-24gb-gigabyte-vision-vdmnniy-stan-tiha-trade-in-ID10Hdzb.html",
  "title": "відеокарта RTX3090 24GB Gigabyte VISION відмінний стан. Тиха. Trade-IN"
}
```
**Семпл #10:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/gigabyte-geforce-rtx-2080-super-8gb-gddr6-otlichnoe-sostoyanie-ID10ZxEv.html",
  "title": "Gigabyte GeForce RTX 2080 SUPER 8GB GDDR6 / Отличное состояние"
}
```
**Семпл #11:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/asus-rog-strix-rtx4070ti-ID10ZxFu.html",
  "title": "Asus Rog Strix RTX4070TI"
}
```
**Семпл #12:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/msi-geforce-rtx-3070-gaming-x-trio-8gb-gddr6-ID10ZxAG.html",
  "title": "MSI GeForce RTX 3070 Gaming X Trio 8GB GDDR6"
}
```
**Семпл #13:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/ventilyatori-kulera-sapphire-rx-6700-6800-xt-nitro-nov-orignal-3-sht-ID10WsEF.html",
  "title": "Вентилятори кулера Sapphire RX 6700/6800 XT Nitro+ — нові, оригінал, 3 шт"
}
```
**Семпл #14:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/vdeokarta-gigabyte-rx-570-4gb-ID101GjE.html",
  "title": "Відеокарта Gigabyte rx  570 4gb"
}
```
**Семпл #15:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/vdeokarta-grova-asus-stix-gaming-rx570-4gb-potuzhna-deal-ID10Zvqu.html",
  "title": "Відеокарта ігрова Asus Stix Gaming RX570 4GB  потужна, ідеал"
}
```
**Семпл #16:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/palit-rtx-3060ti-dual-oc-v1-lhr-vdeokarta-nvidia-IDZEenv.html",
  "title": "Palit RTX 3060Ti Dual OC V1 LHR відеокарта NVIDIA"
}
```
**Семпл #17:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/zotac-geforce-gtx-670-1-5-gb-gddr5-ID10Zxuu.html",
  "title": "ZOTAC GeForce GTX 670 1.5 GB GDDR5"
}
```
**Семпл #18:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Затычка msi  R3650 робочая",
  "item_type": "gpu"
}
```
**Семпл #19:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/vdeokarta-amd-radeon-rx6600-gigabyte-ID10Zxs6.html",
  "title": "Відеокарта Amd Radeon RX6600 gigabyte"
}
```
**Семпл #20:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/vdeokarta-gigabyte-rx5700xt-ID10ZxpZ.html",
  "title": "Відеокарта Gigabyte RX5700XT"
}
```
**Семпл #21:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/vdeokarta-palit-rtx2060-12gb-ID10ZxoY.html",
  "title": "Відеокарта Palit RTX2060 12Gb"
}
```
**Семпл #22:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Видеокарты за все 800",
  "item_type": "gpu"
}
```
**Семпл #23:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/v-deal-grova-vdeokarta-rx580-8gb-256bit-sapphire-nitro-trade-in-ID10wK36.html",
  "title": "в ідеалі! ігрова відеокарта RX580 8GB 256bit Sapphire NITRO+. Trade-in"
}
```
**Семпл #24:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Видеокарта ASUS GeForce 7600 GT",
  "item_type": "gpu"
}
```
**Семпл #25:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/msi-rtx-3060-ti-ventus-2x-ID10YqP0.html",
  "title": "Msi rtx 3060 ti ventus 2x"
}
```
**Семпл #26:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/vdeokarta-palit-geforce-rtx-2060-12-gb-ID10Yx0N.html",
  "title": "Відеокарта Palit GeForce RTX 2060 12 GB"
}
```
**Семпл #27:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/na-garantii-ideal-polnyy-komplekt-msi-rtx-5090-32gb-ventus-3x-oc-ID10VDQB.html",
  "title": "на гарантии, идеал, полный комплект MSI RTX 5090 32GB VENTUS 3X OC"
}
```
**Семпл #28:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "PowerColor Red Dragon AMD 6800",
  "item_type": "gpu"
}
```
**Семпл #29:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/prodam-vdeokartu-asus-geforce-gtx550ti-IDTVKGm.html",
  "title": "Продам відеокарту ASUS GeForce GTX550Ti"
}
```
**Семпл #30:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/msi-rtx-4060-ti-16-gb-ventus-x3-ID10My4C.html",
  "title": "MSI rtx 4060 ti 16 gb ventus x3"
}
```
**Семпл #31:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/vidiokarta-geforce-gts-450-ID10P8vm.html",
  "title": "Видиокарта GeForce GTS 450"
}
```
**Семпл #32:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Palit NE29500TH0851-PM8G96 NVIDIA GeForce 9500 GT 512Mb DDR2 PCI Ex",
  "item_type": "gpu"
}
```
**Семпл #33:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/nvidia-geforce-rtx-3070-inno3d-ichill-x3-ID10Zx4E.html",
  "title": "Nvidia GeForce RTX 3070 Inno3d Ichill x3"
}
```
**Семпл #34:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/msi-radeon-rx580-armor-8g-ID10Zx3m.html",
  "title": "MSI RADEON Rx580 Armor 8g"
}
```
**Семпл #35:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/gtx-1660-mining-edition-cmp-30hx-ID10Zx3c.html",
  "title": "GTX 1660 Mining Edition  CMP 30HX"
}
```
**Семпл #36:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/vdeokarta-rx-570-8gb-ID10Zx1w.html",
  "title": "відеокарта rx 570 8gb"
}
```
**Семпл #37:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/vdeokarta-msi-geforce-gtx1650-4096mb-ventus-xs-oc-IDZPcqK.html",
  "title": "Відеокарта MSI GeForce GTX1650 4096Mb VENTUS XS OC"
}
```
**Семпл #38:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Видеокарта Asus Geforce Gtx 1060 6gb",
  "item_type": "gpu"
}
```
**Семпл #39:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/evga-geforce-rtx-3080-ti-ftw3-IDZFyMd.html",
  "title": "EVGA GeForce RTX 3080 TI FTW3"
}
```
**Семпл #40:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/msi-geforce-rtx-3070-ventus-3x-oc-8gb-gddr6-garantya-komplekt-ID10Py4s.html",
  "title": "MSI GeForce RTX 3070 Ventus 3X OC 8GB GDDR6 | Гарантія | Комплект"
}
```
**Семпл #41:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/amd-radeon-rx-580-sapphire-nitro-4gb-ID10YVIM.html",
  "title": "AMD Radeon RX 580 Sapphire Nitro+ 4GB"
}
```
**Семпл #42:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/vdeokarta-gigabyte-radeon-rx-9070-xt-gaming-oc-16gb-nova-ID10VRZF.html",
  "title": "Відеокарта GIGABYTE Radeon RX 9070 XT GAMING OC 16GB — Нова!"
}
```
**Семпл #43:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Відеокарта AMD FirePro V4900 1 GB GDDR5 +тести",
  "item_type": "gpu"
}
```
**Семпл #44:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/vdeokarta-palit-geforce-rtx-3070-gamingpro-oc-8gb-rozetka-IDYU17l.html",
  "title": "Відеокарта Palit GeForce RTX 3070 GamingPro OC 8GB (Розетка)"
}
```
**Семпл #45:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/videokarta-gigabyte-rtx-3050-windforce-oc-v2-8gv-ID10ZvLM.html",
  "title": "Видеокарта Gigabyte RTX 3050 WINDFORCE OC V2 8GВ"
}
```
**Семпл #46:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Відеокарта  до настільного пк.",
  "item_type": "gpu"
}
```
**Семпл #47:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/gigabyte-aorus-rtx-3070-master-potuzhnst-stil-ta-legendarne-oholodzhennya-ID10NUpm.html",
  "title": "Gigabyte Aorus RTX 3070 Master — Потужність, стиль та легендарне охолодження!"
}
```
**Семпл #48:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/vdeokarta-asus-rog-strix-rx-480-8gb-IDZPcbx.html",
  "title": "Відеокарта ASUS ROG Strix RX 480 8GB"
}
```
**Семпл #49:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Відеокарта на запчастини",
  "item_type": "gpu"
}
```
**Семпл #50:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/vdeo-karti-gt-710-radeon-hd5570-ID10ZvBJ.html",
  "title": "Відео карти, gt 710, radeon hd5570"
}
```
**Семпл #51:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/karta-hp-quadro-p6000-913197-002-24gb-gddr5x-ID10Rtrq.html",
  "title": "карта HP QUADRO P6000  913197-002 24GB GDDR5X"
}
```
**Семпл #52:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/videokarta-tuf-rtx-4090-24-gb-ID10WAoy.html",
  "title": "Видеокарта Tuf Rtx 4090 24 gb"
}
```
**Семпл #53:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/vdeokarta-msi-geforce-gtx-1050-ti-4gb-gddr5-gtx-1050-ti-4gt-bla-tserkva-ID10YQWO.html",
  "title": "Відеокарта MSI GeForce GTX 1050 Ti 4GB GDDR5 (GTX 1050 Ti 4GT) Біла церква"
}
```
**Семпл #54:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/rx-470-480-570-garantya-6ms-stan-praktichno-yak-nov-IDZyKgo.html",
  "title": "RX 470/480/570|Гарантія 6міс|Стан практично як нові"
}
```
**Семпл #55:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/asus-rog-strix-2070super-8gb-ID10ZvwO.html",
  "title": "ASUS ROG strix 2070super 8gb"
}
```
**Семпл #56:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/rozstrochka-mono-na-3-msyats-asus-tuf-rx7900xtx-24gb-potuzhna-topova-grova-vdeokarta-ID10Zvt9.html",
  "title": "РОЗСТРОЧКА МОНО НА 3 місяці! Asus TUF RX7900XTX 24gb потужна топова ігрова відеокарта"
}
```
**Семпл #57:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/vdeokarta-grova-asus-stix-gaming-rx570-4gb-potuzhna-deal-ID10Zvqu.html",
  "title": "Відеокарта ігрова Asus Stix Gaming RX570 4GB  потужна, ідеал"
}
```
**Семпл #58:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Видеокарта КАК новая MSI GTX 1060  3GB и другие",
  "item_type": "gpu"
}
```
**Семпл #59:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/videokarta-msi-gtx-gaming-1050-ti-4gb-kak-novaya-plomba-i-drugie-IDXhRkC.html",
  "title": "Видеокарта MSI GTX GAMING 1050 Ti 4GB КАК НОВАЯ! пломба и другие"
}
```
**Семпл #60:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/vdeokarta-msi-amd-radeon-rx-6500xt-4gb-ID10P6Tk.html",
  "title": "Відеокарта MSI AMD Radeon RX 6500XT 4GB"
}
```
**Семпл #61:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Компьютеры и комплектующие",
  "item_type": "gpu"
}
```
**Семпл #62:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/videokarta-gigabyte-radeon-rx-470-g1-gaming-4g-perepayana-na-8gb-IDQynDU.html",
  "title": "Видеокарта GIGABYTE Radeon RX 470 G1 Gaming 4G перепаяна на 8Гб!"
}
```
**Семпл #63:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/prodam-vdeokartu-asus-rog-strix-radeon-rx-580-top-8gb-rog-strix-rx580-t8g-gaming-ID10ZvkQ.html",
  "title": "Продам Відеокарту ASUS ROG Strix Radeon RX 580 TOP 8GB (ROG-STRIX-RX580-T8G-GAMING)"
}
```
**Семпл #64:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/videokarta-gigabyte-rtx-4060-gaming-oc-8gb-IDZ5ajX.html",
  "title": "Видеокарта GIGABYTE RTX 4060 GAMING OC 8gb"
}
```
**Семпл #65:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/msi-geforce-rtx-3080-suprim-x-10gb-ID10Y6c3.html",
  "title": "MSI GeForce RTX 3080 SUPRIM X 10GB"
}
```
**Семпл #66:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/sapphire-pulse-radeon-rx-7900-xtx-24gb-384-bit-oc-ID10S0VP.html",
  "title": "Sapphire Pulse RADEON RX 7900 XTX 24GB 384 bit OC"
}
```
**Семпл #67:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/asus-rtx-3070-8gb-tuf-gaming-ID10dzeS.html",
  "title": "ASUS RTX 3070 8GB TUF Gaming"
}
```
**Семпл #68:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/vdeokarta-evga-rtx-3080-10-gb-ID10ZveB.html",
  "title": "Відеокарта EVGA RTX 3080 10 GB"
}
```
**Семпл #69:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/vdeokarta-grova-sapphire-pulse-rx570-4gb-IDXa7Km.html",
  "title": "Відеокарта ігрова Sapphire PULSE RX570 4GB"
}
```
**Семпл #70:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/videokarta-msi-geforce-gtx-1070-armor-8gb-ID10Zv8I.html",
  "title": "Видеокарта MSI Geforce GTX 1070 Armor 8GB"
}
```
**Семпл #71:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/vdeokarta-inno3d-geforce-rtx-5060-ti-twin-x2-8gb-gddr7-dlss4-ID10VuEc.html",
  "title": "Відеокарта INNO3D GeForce RTX 5060 Ti Twin X2 8GB GDDR7 DLSS4"
}
```
**Семпл #72:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/videokarta-nvidia-gt-240-512-mb-ID10Zv4b.html",
  "title": "Видеокарта Nvidia GT 240 512 mb"
}
```
**Семпл #73:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "HD2600PRO sonic 512 мб топ видюха",
  "item_type": "gpu"
}
```
**Семпл #74:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Адаптер-райзер PCI-E x1 to 16x, 60 см USB 3.0 Cable SATA to 6Pin Power",
  "item_type": "gpu"
}
```
**Семпл #75:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Видеокарта nVidia Tesla M40 - 12 Gb",
  "item_type": "gpu"
}
```
**Семпл #76:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/vdeokarta-gigabyte-geforce-rtx-2060-d6-6gb-gddr6-ID10NM5x.html",
  "title": "Відеокарта Gigabyte GeForce RTX 2060 D6 6GB GDDR6"
}
```
**Семпл #77:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Rtx 4060 ti (не робоча)",
  "item_type": "gpu"
}
```
**Семпл #78:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/asus-prime-rx-9070-oc-16gb-ID10Z2S5.html",
  "title": "Asus Prime RX 9070 OC 16GB"
}
```
**Семпл #79:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/povnstyu-robocha-aorus-rx570-4gb-ID10Z4iE.html",
  "title": "Повністю робоча aorus rx570 4gb"
}
```
**Семпл #80:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/asus-tuf-gaming-geforce-gtx-1660-super-6gb-v-idealnom-sostoyanii-ID10XZge.html",
  "title": "ASUS TUF Gaming GeForce GTX 1660 SUPER 6GB в идеальном состоянии"
}
```
**Семпл #81:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/vdeokarta-msi-rtx-2060-ventus-gp-oc-6gb-gddr6-ID10NLNa.html",
  "title": "Відеокарта MSI RTX 2060 Ventus GP OC 6GB GDDR6"
}
```
**Семпл #82:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Відеокарта ATI Radeon HD 2400PRO 256Мб DDR2",
  "item_type": "gpu"
}
```
**Семпл #83:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/msi-geforce-rtx-2080-aero-8gb-IDS6Ikl.html",
  "title": "MSI GeForce RTX 2080 AERO 8GB"
}
```
**Семпл #84:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Видеокарта 1060 6 гб MSI 1060 6GB GAMING",
  "item_type": "gpu"
}
```
**Семпл #85:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/vdeokarta-geforce-gtx-970-jetstream-256-IDZupaU.html",
  "title": "Відеокарта Geforce GTX 970 JetStream 256"
}
```
**Семпл #86:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/asus-rx-580-na-8-gb-videokarta-ID10Zwzu.html",
  "title": "Asus rx 580 на 8 gb видеокарта"
}
```
**Семпл #87:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/vdeokarta-gigabyte-geforce-rtx-5070-ti-windforce-oc-sff-16g-gv-n507twf3oc-16gd-ID10XnUV.html",
  "title": "Відеокарта GIGABYTE GeForce RTX 5070 Ti WINDFORCE OC SFF 16G (GV-N507TWF3OC-16GD)"
}
```
**Семпл #88:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Відеокарта Palit GeForce RTX 5060 Ti Infinity 3 16GB (NE7506T019T1-GB2061S)",
  "item_type": "gpu"
}
```
**Семпл #89:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/vdeokarta-gigabyte-radeon-rx-9070-xt-gaming-oc-16g-gv-r9070xtgaming-oc-16gd-ID10XsjK.html",
  "title": "Відеокарта GIGABYTE Radeon RX 9070 XT GAMING OC 16G (GV-R9070XTGAMING OC-16GD)"
}
```
**Семпл #90:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/vdeokarta-gtx-1660-ti-6-gb-materinka-protsesor-pamyat-ID10ZwyR.html",
  "title": "Відеокарта - gtx 1660 ti 6 gb + материнка + процесор + память"
}
```
**Семпл #91:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/vdeokarta-radeon-rx-6800-xt-16-gb-ID10Y0dW.html",
  "title": "Відеокарта Radeon RX 6800 XT 16 Gb"
}
```
**Семпл #92:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/asus-tuf-gaming-rx5700-xt-8-gb-ID10zUX7.html",
  "title": "Asus Tuf Gaming RX5700 XT 8 gb"
}
```
**Семпл #93:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/videokarta-gainward-phantom-rtx-5090-ID10WAsg.html",
  "title": "Видеокарта Gainward Phantom RTX 5090"
}
```
**Семпл #94:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/vdeokarta-asus-dual-geforce-rtx-5070-oc-edition-12gb-dual-rtx5070-o12g-ID10Xti8.html",
  "title": "Відеокарта ASUS Dual GeForce RTX 5070 OC Edition 12GB (DUAL-RTX5070-O12G)"
}
```
**Семпл #95:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/vdeokarta-msi-geforce-rtx-5070-12g-gaming-trio-oc-g5070-12gtc-ID10XtJG.html",
  "title": "Відеокарта MSI GeForce RTX 5070 12G GAMING TRIO OC (G5070-12GTC)"
}
```
**Семпл #96:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/vdeokarta-asus-prime-geforce-rtx-5070-oc-edition-12gb-prime-rtx5070-o12g-ID10XtqF.html",
  "title": "Відеокарта ASUS Prime GeForce RTX 5070 OC Edition 12GB (PRIME-RTX5070-O12G)"
}
```
**Семпл #97:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/vdeokarta-asus-prime-radeon-rx-9070-xt-oc-edition-16gb-prime-rx9070xt-o16g-ID10XoaH.html",
  "title": "Відеокарта ASUS Prime Radeon RX 9070 XT OC Edition 16GB (PRIME-RX9070XT-O16G)"
}
```
**Семпл #98:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Відеокарта GIGABYTE GeForce RTX 5060 Ti 16GB GDDR7 (GV-N506TWF2-16GD)",
  "item_type": "gpu"
}
```
**Семпл #99:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/vdeokarta-gigabyte-geforce-rtx-5070-windforce-oc-sff-12g-gv-n5070wf3oc-12gd-ID10XpdL.html",
  "title": "Відеокарта GIGABYTE GeForce RTX 5070 WINDFORCE OC SFF 12G (GV-N5070WF3OC-12GD)"
}
```
**Семпл #100:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/vdeokarta-msi-geforce-rtx-5070-ti-16g-ventus-3x-oc-g507t-16v3c-ID10Xtyx.html",
  "title": "Відеокарта MSI GeForce RTX 5070 Ti 16G VENTUS 3X OC (G507T-16V3C)"
}
```

#### 🧠 Процесори (CPU) — Відсіяно (Показано 100 з max 100):
**Семпл #1:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/i7-6700-intel-core-3-40ghz-protsesor-7-6700t-ID10TFUd.html",
  "title": "i7-6700 Intel Core 3.40ghz процесор і7-6700Т"
}
```
**Семпл #2:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/intel-core-i3-9100f-4-core-4-2ghz-lga1151-ID10PozU.html",
  "title": "Intel Core i3-9100F 4-Core 4.2GHz LGA1151"
}
```
**Семпл #3:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Продаю процесор Xeon",
  "item_type": "cpu"
}
```
**Семпл #4:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Процесор Сокет ам4,Amd a-6 9500 із вбудованою графікою radeon r5",
  "item_type": "cpu"
}
```
**Семпл #5:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/s1700-protsesor-intel-core-i5-13600k-14yader-20potokv-5-1ggts-z-vdeoyadrom-trade-in-ID10zmgh.html",
  "title": "s1700 процесор Intel Core i5-13600K 14ядер\\20потоків 5.1ГГц з відеоядром. Trade-IN"
}
```
**Семпл #6:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/protsesor-amd-ryzen-3-2200g-3-5-ID10Zxpv.html",
  "title": "Процесор AMD Ryzen 3 2200G 3.5"
}
```
**Семпл #7:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/protsesor-amd-ryzen-7-3700h-ID10Zxl1.html",
  "title": "Процесор AMD Ryzen 7 3700х"
}
```
**Семпл #8:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/s1151v2-protsesor-intel-core-i5-9600k-6yader-4-6ghz-trade-in-ID10XhJt.html",
  "title": "s1151v2 процесор Intel Core i5-9600K 6ядер 4.6GHz. Trade-in"
}
```
**Семпл #9:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Набор, процессор AMD Ryzen 5 3500, і Кулер",
  "item_type": "cpu"
}
```
**Семпл #10:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/s1200-protsesor-10pokolnnya-intel-pentium-gold-g6405-4-1ggts-z-grafkoyu-IDYLSXO.html",
  "title": "s1200 процесор 10покоління Intel Pentium GOLD G6405 4.1ГГц з графікою"
}
```
**Семпл #11:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/protsessor-amd-fx-4350-IDZPcKz.html",
  "title": "Процессор AMD FX 4350"
}
```
**Семпл #12:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "AMD Athlon II X4 631",
  "item_type": "cpu"
}
```
**Семпл #13:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/intel-core-i5-4460s-42-9-3-4ghz-v-nayavnost-3-sht-IDZLZkb.html",
  "title": "Intel Core i5 4460S 4*2.9-3.4Ghz в наявності 3 шт"
}
```
**Семпл #14:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/noviy-protsesor-amd-ryzen-9-9950x-9000-series-IDY32sj.html",
  "title": "Новий Процесор AMD Ryzen 9 9950X 9000 Series"
}
```
**Семпл #15:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/i3-10100f-h410-komplekt-ID10VWYv.html",
  "title": "i3 10100f/h410 комплект"
}
```
**Семпл #16:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/s1151-set-intel-core-i5-7500-3-8ghz-z-vdeoyadrom-atx-asus-h270-trade-in-ID10HweN.html",
  "title": "s1151 сет Intel Core i5-7500 3.8GHz з відеоядром + ATX ASUS H270. Trade-IN"
}
```
**Семпл #17:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/ryzen-9-3900x-b550m-aorus-16-32gb-ddr4-moschnyy-komplekt-amd-s-am4-ID10Zx4L.html",
  "title": "Ryzen 9 3900X/ B550M AORUS/ 16-32Gb DDR4 мощный комплект AMD s-AM4"
}
```
**Семпл #18:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Коллекция процессо Intel и AMD.",
  "item_type": "cpu"
}
```
**Семпл #19:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/protsesor-intel-core-i3-2120t-35w-IDR5DYb.html",
  "title": "Процесор Intel Core i3 2120T 35W"
}
```
**Семпл #20:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/intel-xeon-e3-1240-v5-e3-1270-v5-s1151-IDZgGMr.html",
  "title": "Intel Xeon E3-1240 V5/ E3-1270 V5 (s1151)"
}
```
**Семпл #21:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/ryzen-9-7900x-asrock-b650-pg-lightning-ID10OTU5.html",
  "title": "Ryzen 9 7900X і Asrock B650 PG LIGHTNING"
}
```
**Семпл #22:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Процесор amd athlon 64x2 з комплектним кулером",
  "item_type": "cpu"
}
```
**Семпл #23:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/protsesor-intel-core-i5-6600-b-v-IDZWJSB.html",
  "title": "Процесор Intel Core i5-6600 (б/в)"
}
```
**Семпл #24:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/protsesor-intel-core-i5-7500-b-v-IDZWJTd.html",
  "title": "Процесор Intel Core i5-7500 (б/в)"
}
```
**Семпл #25:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/protsesor-intel-core-i5-7400-b-v-IDZWJSZ.html",
  "title": "Процесор Intel Core i5-7400 (б/в)"
}
```
**Семпл #26:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/protsessor-intel-core-i5-6500-4-yadra-3-6-ggts-ideal-garantiya-IDZWcb4.html",
  "title": "Процессор intel core i5 6500 4 ядра 3.6 ГГц идеал гарантия"
}
```
**Семпл #27:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/protsesori-intel-i5-4440-4460-4590-4690-4-4-yadra-rozprodazh-krascha-tsna-IDZP2yq.html",
  "title": "Процесори Intel i5-4440/4460/4590/4690 4/4 ядра РОЗПРОДАЖ! КРАЩА ЦІНА"
}
```
**Семпл #28:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/protsessor-intel-core-i5-8500-6-yader-4-1-ggts-chastota-ideal-garantiya-IDZbGKN.html",
  "title": "Процессор intel core i5 8500 6 ядер 4.1 ГГц частота идеал гарантия"
}
```
**Семпл #29:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/protsesor-intel-core-i7-6700-b-v-IDWpB0Z.html",
  "title": "Процесор Intel Core i7-6700 (б/в)"
}
```
**Семпл #30:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/protsesor-intel-core-i5-8500-b-v-IDWo7cm.html",
  "title": "Процесор Intel Core i5-8500 (б/в)"
}
```
**Семпл #31:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/protsesor-intel-core-i5-6500-b-v-IDZWmBn.html",
  "title": "Процесор Intel Core i5-6500 (б/в)"
}
```
**Семпл #32:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/intel-core-i5-7600t-2-8-3-7-ggts-35-vt-s1151-IDXULi5.html",
  "title": "Intel Core i5-7600T 2.8-3.7 ГГц, 35 Вт, s1151"
}
```
**Семпл #33:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/prodam-protsessor-intel-core-i5-9400f-ID10ZvBb.html",
  "title": "Продам  процессор Intel Core i5-9400F"
}
```
**Семпл #34:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/s1700-set-intel-core-i5-14600kf-plata-b760-ddr4-vodyanka-trade-in-ID10THhl.html",
  "title": "s1700 сет Intel Core i5-14600KF + плата B760 DDR4 + водянка. Trade-IN"
}
```
**Семпл #35:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Socket 1700  / 13100f  актуальний бюджетний проц",
  "item_type": "cpu"
}
```
**Семпл #36:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/amd-ryzen-7-7700-am5-protsesor-v-dealnomu-stan-ID10Zv2Z.html",
  "title": "AMD Ryzen 7 7700 AM5 процесор, в ідеальному стані"
}
```
**Семпл #37:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/intel-xeon-e5-2696v3-2011v3-IDYrce9.html",
  "title": "Intel Xeon e5 2696v3 2011v3"
}
```
**Семпл #38:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/protsesor-intel-core-i5-8600k-3-6-ghz-ID10XgDv.html",
  "title": "Процесор Intel Core i5-8600K 3.6 GHz"
}
```
**Семпл #39:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/amd-ryzen-5-1600af-v-neizvestnom-sostoyanii-ID10YiRh.html",
  "title": "AMD Ryzen 5 1600AF в неизвестном состоянии"
}
```
**Семпл #40:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/protsesor-intel-xeon-e5-2623-v4-ID10YAlp.html",
  "title": "Процесор Intel Xeon E5-2623 v4"
}
```
**Семпл #41:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/amd-ryzen-9-3900x-box-ID10VI2q.html",
  "title": "AMD Ryzen 9 3900x box"
}
```
**Семпл #42:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/potuzhniy-set-intel-core-i9-10850k-10yader-20pot-5-2ggts-z-vdeo-plata-asus-z490-trade-in-ID10TGI8.html",
  "title": "потужний сет Intel Core i9-10850K 10ядер\\20пот 5.2ГГц з відео + плата ASUS Z490. Trade-in"
}
```
**Семпл #43:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/s1200-protsesor-intel-core-i9-10850k-10yader-20potokv-5-2ggts-z-grafkoyu-trade-in-ID10TGIm.html",
  "title": "s1200 процесор Intel Core i9-10850K 10ядер\\20потоків 5.2ГГц з графікою. Trade-IN"
}
```
**Семпл #44:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/protsesor-i3-4130-materinka-IDUc3Jg.html",
  "title": "Процесор i3 4130+Материнка"
}
```
**Семпл #45:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/protsesor-amd-a4-6300-IDZPbbn.html",
  "title": "Процесор AMD A4-6300"
}
```
**Семпл #46:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Xeon E-2124 CPU 4 Cores 4 Threads 3.30GHz 8MB 71W DDR4 LGA 1151",
  "item_type": "cpu"
}
```
**Семпл #47:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/i7-6700-intel-core-3-40ghz-protsesor-7-6700t-ID10TFUd.html",
  "title": "i7-6700 Intel Core 3.40ghz процесор і7-6700Т"
}
```
**Семпл #48:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/asus-z270-prime-intel-core-i7-6700k-IDWKW1h.html",
  "title": "Asus Z270 Prime + Intel Core i7 6700k"
}
```
**Семпл #49:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/prodam-protsessor-na-socket-1155-intel-pentium-g2020t-IDY1V8E.html",
  "title": "Продам процессор на socket 1155-Intel Pentium G2020T"
}
```
**Семпл #50:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Процессор Intel Xeon E5 2696 v4 22-44 2,2Ghz - 3,7Ghz 2011v3",
  "item_type": "cpu"
}
```
**Семпл #51:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/protsesor-intel-celeron-g4930-IDXPMFM.html",
  "title": "Процесор Intel Celeron G4930"
}
```
**Семпл #52:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/komplekt-do-pk-i7-6700-16-gb-ddr4-mat-plata-kuller-ID10YXVq.html",
  "title": "Комплект до пк, i7 6700, 16 gb ddr4, мат. плата, куллер"
}
```
**Семпл #53:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Процессор amd ryzen 5500",
  "item_type": "cpu"
}
```
**Семпл #54:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/protsesor-intel-g4560-core-i3-6100-i5-6400-i5-6500-i5-6500t-i5-7400-xeon-e3-1225-v6-s1151-IDZJF2q.html",
  "title": "Процесор Intel G4560/Core i3-6100/i5 6400/i5-6500/i5-6500T/I5-7400/Xeon  E3-1225 v6 s1151"
}
```
**Семпл #55:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/amd-ryzen-7-5700x-IDZLKmF.html",
  "title": "AMD Ryzen 7 5700X"
}
```
**Семпл #56:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Процессор Intel Pentium Gold (LGA 1151)G5400 ,Box 2x3.7 ГГц",
  "item_type": "cpu"
}
```
**Семпл #57:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/prodam-intel-core-i5-9400f-6-yader-6-potokv-ID10ZuAo.html",
  "title": "Продам Intel Core i5-9400F (6 ядер / 6 потоків)"
}
```
**Семпл #58:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/intelr-xeonr-e5-2650v4-sr2n3-2-20ghz-l718b266-e4-m7yb645102218-ID10f8GF.html",
  "title": "Intel(r) xeon(r) e5-2650v4 sr2n3 2.20GHZ L718B266 (e4) M7YB645102218"
}
```
**Семпл #59:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Процессор Intel pentium g3260 LGA1150",
  "item_type": "cpu"
}
```
**Семпл #60:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/protsesor-amd-ryzen-5-5600-ID10Zua8.html",
  "title": "Процесор AMD Ryzen 5 5600"
}
```
**Семпл #61:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/protsesor-intel-xeon-e5-2620v2-6-yader-12-potokov-IDYR0NC.html",
  "title": "Процесор Intel Xeon E5-2620v2 6 ядер/12 потоков"
}
```
**Семпл #62:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Продаю процесор Xeon",
  "item_type": "cpu"
}
```
**Семпл #63:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/intel-core-i3-6100-3-7ghz-ID10ZtUB.html",
  "title": "Intel core i3 6100 3.7ghz"
}
```
**Семпл #64:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/intel-xeon-e5-2699a-v4-ID10Ieb2.html",
  "title": "Intel Xeon e5 2699A v4"
}
```
**Семпл #65:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/komplekt-ryzen-5-5500x3d-32gb-ddr4-3400mhz-groviy-monstr-na-am4-ID10e2ny.html",
  "title": "Комплект Ryzen 5 5500X3D +32gb ddr4 3400MHz ігровий монстр на ам4"
}
```
**Семпл #66:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/cpu-intel-core-i7-10700kf-8-yader-16-potokov-lga-1200-ID10mkNI.html",
  "title": "CPU Intel Core i7-10700KF 8 ядер/ 16 потоков LGA 1200"
}
```
**Семпл #67:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/protsessor-soket-am2-amd-athlon-64-x2-4200-IDLcT6W.html",
  "title": "Процессор сокет AM2 AMD Athlon 64 X2 4200+"
}
```
**Семпл #68:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Процесор Inte I3-10100f",
  "item_type": "cpu"
}
```
**Семпл #69:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/protsesor-ryzen-5-7500f-ID10ZtOF.html",
  "title": "Процесор Ryzen 5 7500f"
}
```
**Семпл #70:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/protsessor-2-yadra-xeon-5148-core-2-duo-e2160-e5400-e6300-na-soket-775-IDEuAn6.html",
  "title": "Процессор 2 ядра Xeon 5148 Core 2 Duo E2160 E5400 E6300 на сокет 775"
}
```
**Семпл #71:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/intel-core-5-6500-s-1151-sky-lake-IDUNmuC.html",
  "title": "Intel Core і5 -6500 -s.1151 Sky lake"
}
```
**Семпл #72:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Кулер на 462, 478, 775, 754, 939, АМ2, 1155, 1150, 1151 сокет",
  "item_type": "cpu"
}
```
**Семпл #73:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Процесор cpu soc 775 1155",
  "item_type": "cpu"
}
```
**Семпл #74:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Процесор Athlon II X3 450 3,2 GHz AM3 95w ADX450WFK32GM",
  "item_type": "cpu"
}
```
**Семпл #75:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/protsesor-intel-core-2-quad-q6600-4x2-4ghz-8mb-cache-1066mhz-bu-s775-pk-IDDusy5.html",
  "title": "Процесор Intel Core 2 Quad Q6600 4x2.4GHz 8mb cache 1066MHz бу s775 пк"
}
```
**Семпл #76:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Amd phenom || x4 925 processor",
  "item_type": "cpu"
}
```
**Семпл #77:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/protsesor-intel-core-i3-10105t-6m-cache-up-to-3-80-ghz-s1200-tray-ID10XKeR.html",
  "title": "Процесор Intel Core i3-10105T (6M Cache, up to 3.80 GHz) s1200 Tray"
}
```
**Семпл #78:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/protsesor-intel-core-i5-9500-8500-8400-7400-7600k-6500-ID10SLfT.html",
  "title": "Процесор intel core i5 9500/8500/8400/7400/7600k/6500"
}
```
**Семпл #79:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Процессор Intel Core i9-7980XE Extreme Edition 18 ядер 36 потоков s2066",
  "item_type": "cpu"
}
```
**Семпл #80:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/prodam-protsessor-i3-4330-2-2-3-5hz-ID10Ztdb.html",
  "title": "Продам процессор i3 4330 2/2 3,5hz"
}
```
**Семпл #81:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/protsessor-intel-core-i7-8700-6-yader-12-potokov-4-6-ggts-chastota-ideal-garantiya-intel-soket-1151v2-8-e-pokolenie-ID10zwVM.html",
  "title": "Процессор intel core i7 8700 6 ядер 12 потоков 4.6 Ггц частота идеал гарантия интел сокет 1151v2 8-е поколение"
}
```
**Семпл #82:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/protsesor-amd-ryzen-7-3800x-tray-IDVIpKC.html",
  "title": "Процесор AMD Ryzen 7 3800x tray"
}
```
**Семпл #83:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Продам AMD Phenom x4 9150e",
  "item_type": "cpu"
}
```
**Семпл #84:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/protsesor-amd-ryzen-7-9700x-ID10ZsWq.html",
  "title": "Процесор AMD Ryzen 7 9700X"
}
```
**Семпл #85:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/protsessor-intel-core-i7-9700k-3-64-9-ghz-8-yader-lga1151-ID10ZsP9.html",
  "title": "Процессор Intel Core i7-9700K 3.6–4.9 GHz (8 ядер, LGA1151)"
}
```
**Семпл #86:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/protsesor-ryzen-5-7500f-ID10ZsO5.html",
  "title": "Процесор Ryzen 5 7500f"
}
```
**Семпл #87:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/protsesor-intel-core-i5-3570-3-40ghz-6mb-5gt-s-sr0t7-s1155-tray-IDZEvol.html",
  "title": "Процесор Intel Core i5-3570 3.40GHz/6MB/5GT/s (SR0T7) s1155, tray"
}
```
**Семпл #88:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/protsessor-amd-ryzen-5-3400g-ID10ZsGX.html",
  "title": "Процессор AMD Ryzen 5 3400G"
}
```
**Семпл #89:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/ryzen-9-7900x-asrock-b650-pg-lightning-ID10OTU5.html",
  "title": "Ryzen 9 7900X і Asrock B650 PG LIGHTNING"
}
```
**Семпл #90:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/protsesor-intel-core-i5-7400-3-00ghz-6mb-8gt-s-sr32w-s1151-tray-ID10Y1Cr.html",
  "title": "Процесор Intel Core i5-7400 3.00GHz/6MB/8GT/s (SR32W) s1151, tray"
}
```
**Семпл #91:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/i7-13700f-16-24-30-mb-opis-ID10Tpzz.html",
  "title": "I7 13700F 16/24 30 mb (опис)"
}
```
**Семпл #92:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Процесор AMD Pnenom ll X4 970 3.5GHz sAM2+/AM3 125W",
  "item_type": "cpu"
}
```
**Семпл #93:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/ryzen-5-2600x-b-u-ID10Zswt.html",
  "title": "Ryzen 5 2600x б/у"
}
```
**Семпл #94:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Продам Процесор  I3-380M и др.",
  "item_type": "cpu"
}
```
**Семпл #95:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/protsesor-intel-core-i7-9700k-8-yader-lga1151-srelt-ID10NsMk.html",
  "title": "Процесор Intel Core i7-9700K 8 ядер LGA1151 (SRELT)"
}
```
**Семпл #96:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/protsesor-amd-fx6200-IDZimXo.html",
  "title": "Процесор AMD FX6200"
}
```
**Семпл #97:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Процессор AMD Athlon 64 TF-20",
  "item_type": "cpu"
}
```
**Семпл #98:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/protsesor-intell-core-i3-3240-3-4-ghz-IDPoQyZ.html",
  "title": "Процесор Intell Core i3-3240 3.4 GHZ"
}
```
**Семпл #99:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Intel pentium b970 рабочий",
  "item_type": "cpu"
}
```
**Семпл #100:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/igrovoy-komplekt-i7-11700f-msi-z490-tomahawk-be-quiet-ID10TiKR.html",
  "title": "Игровой Комплект - i7-11700f/MSI Z490 TOMAHAWK/be quiet!"
}
```

#### 🔌 Материнські плати (Motherboard) — Відсіяно (Показано 100 з max 100):
**Семпл #1:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Материнська плата и комплекти AMD и INTEL та CPU(майже усі сокети)",
  "item_type": "motherboard"
}
```
**Семпл #2:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/materinska-plata-biostar-tb360-lga1151-intel-g4900-ID10MqY7.html",
  "title": "Материнська плата Biostar TB360 LGA1151 + Intel G4900"
}
```
**Семпл #3:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/materinska-plata-msi-z97-pc-mate-intel-core-i5-4400-16-gb-ram-ID10YG03.html",
  "title": "Материнська плата MSI Z97 PC Mate + Intel Core i5-4400 + 16 ГБ RAM"
}
```
**Семпл #4:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "продам материнскую плату",
  "item_type": "motherboard"
}
```
**Семпл #5:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Материнська плата до ноутбука читати оголошення",
  "item_type": "motherboard"
}
```
**Семпл #6:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "ПРОДАМ КОМПЛЕКТ: материнка MSI (Socket AM2), 4 ГБ DDR2, кулер + фігні",
  "item_type": "motherboard"
}
```
**Семпл #7:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/servernaya-materinskaya-plata-asus-p10s-i-1151-c232-2ddr4-mitx-ID10ZxL2.html",
  "title": "Серверная материнская плата Asus P10S-I (1151/ C232/2×DDR4/mITX)"
}
```
**Семпл #8:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/materinska-plata-x79-e5-2650v2-ID10Huqu.html",
  "title": "Материнська плата x79+E5-2650v2"
}
```
**Семпл #9:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "материнська плата asus p5ld2 se",
  "item_type": "motherboard"
}
```
**Семпл #10:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Комплект материнская плата процессор",
  "item_type": "motherboard"
}
```
**Семпл #11:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/gotovyy-komplekt-materinskaya-plata-asrock-h310cm-dvs-core-i3-9100f-ram-12gb-kuler-ID10ZxaL.html",
  "title": "Готовый комплект: Материнская плата ASRock H310CM-DVS + Core i3-9100F + RAM 12GB + Кулер"
}
```
**Семпл #12:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Материнські плати для iPhone 8,  SE 2020, SE 2022 (+ корпус iphone 8)",
  "item_type": "motherboard"
}
```
**Семпл #13:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/komplekt-asus-h170-pro-gaming-celeron-g3930-4gb-ddr4-kuler-ID10uwuG.html",
  "title": "Комплект ASUS H170 PRO GAMING + Celeron G3930 + 4GB DDR4 + кулер"
}
```
**Семпл #14:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/msi-h81m-p33-soc-1150-usb3-dvi-intel-core-i3-4150-IDXfPlV.html",
  "title": "MSI H81M-P33 (soc 1150, USB3, DVI)+Intel Core i3-4150"
}
```
**Семпл #15:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/komplekt-1150-asrock-fatality-b85-core-i7-4771-16gb-ddr3-ID10SEnE.html",
  "title": "Комплект 1150 ASRock Fatality B85/ Core I7 4771/ 16gb ddr3"
}
```
**Семпл #16:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/asus-tuf-b450m-pro-gaming-ID10Zx7P.html",
  "title": "Asus Tuf B450M-pro gaming"
}
```
**Семпл #17:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/prodayu-materinsku-platu-b450m-a-pro-max-ID10NpQ6.html",
  "title": "продаю материнську плату B450M-A PRO MAX"
}
```
**Семпл #18:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/core-i5-3330-3-0ghz-box-asus-p8h77-v-le-intel-h77-socket-1155-IDNF1tW.html",
  "title": "Core i5-3330 3.0GHz BOX + Asus P8H77-V LE Intel H77 Socket 1155"
}
```
**Семпл #19:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/amd-a8-6600k-3-9-zalman-cnps10x-optima-msi-a88x-g41-pc-mate-4gb-IDNwt43.html",
  "title": "AMD A8-6600K 3.9, Zalman CNPS10X Optima, MSI A88X-G41 PC Mate, 4Gb"
}
```
**Семпл #20:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Материнская плата аттракциона силомер боксер груша boxer",
  "item_type": "motherboard"
}
```
**Семпл #21:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/prodam-komplekt-legendarnyy-phenom-ii-x4-965-black-edition-gigabyte-ga-970a-d3-8gb-ddr3-gts-450-1gb-ID10ZvVL.html",
  "title": "Продам комплект - Легендарный Phenom II X4 965 Black Edition + Gigabyte GA-970A-D3 + 8GB DDR3 + GTS 450 1GB"
}
```
**Семпл #22:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/materinskaya-plata-asus-p8h67-s1155-intel-h67-2xpci-ex16-IDWLR6R.html",
  "title": "Материнская плата Asus P8H67 (s1155, Intel H67, 2xPCI-Ex16)"
}
```
**Семпл #23:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/materinska-plata-gigabyte-z790-aorus-master-x-IDZuqkI.html",
  "title": "Материнська плата Gigabyte Z790 Aorus Master X"
}
```
**Семпл #24:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/asus-prime-h310m-k-r2-0-nerobocha-na-donora-ID10ZvQF.html",
  "title": "asus prime h310m-k r2.0 неробоча, на донора."
}
```
**Семпл #25:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/komplekt-msi-a55m-p34-cpu-ram-ID10OHQH.html",
  "title": "Комплект MSI A55m-p34 + CPU + Ram"
}
```
**Семпл #26:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/materinska-plata-athermiter-x79-komplekt-ID10Sa7e.html",
  "title": "материнська плата athermiter x79 комплект"
}
```
**Семпл #27:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/materinskaya-plata-asus-rog-strix-x870-a-gaming-wifi-sam5-amd-x870-IDZYGXL.html",
  "title": "Материнская плата Asus ROG STRIX X870-A GAMING WIFI (sAM5, AMD X870)"
}
```
**Семпл #28:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/materinskaya-plata-gigabyte-x570-gaming-x-am4-x570-atx-ID10X5NU.html",
  "title": "Материнская плата Gigabyte X570 Gaming X (AM4, X570, ATX)"
}
```
**Семпл #29:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/asus-rog-strix-b760-f-gaming-wi-fis1700-intel-b760-na-garantii-ID10NY07.html",
  "title": "Asus ROG STRIX B760-F Gaming Wi-Fi(s1700, Intel B760) на гарантии"
}
```
**Семпл #30:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/komplekt-1150-asrock-fatality-b85-core-i7-4771-16gb-ddr3-ID10SEnE.html",
  "title": "Комплект 1150 ASRock Fatality B85/ Core I7 4771/ 16gb ddr3"
}
```
**Семпл #31:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Продам материнку ASUS P5E Deluxe,",
  "item_type": "motherboard"
}
```
**Семпл #32:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/komplekt-materinska-plata-asus-tuf-b450-pro-gaming-protsesor-amd-ryzen-5-3600-ID10tZBT.html",
  "title": "Комплект Материнська плата Asus TUF B450-PRO Gaming + Процесор AMD Ryzen 5 3600"
}
```
**Семпл #33:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/materinska-plata-asus-prime-z790-a-wi-fi-s1700-intel-z790-pci-ex16-ID10ZvuP.html",
  "title": "Материнська плата Asus PRIME Z790-A Wi-Fi (s1700, Intel Z790, PCI-Ex16)"
}
```
**Семпл #34:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Материнська плата MSI K9N NeoV2",
  "item_type": "motherboard"
}
```
**Семпл #35:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/komplekt-materinska-plata-asus-rog-strix-z390-e-gaming-i7-9700k-ID10CUOz.html",
  "title": "Комплект материнська плата asus rog strix Z390-E GAMING+i7 9700k"
}
```
**Семпл #36:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "материнская плата Lenovo G770",
  "item_type": "motherboard"
}
```
**Семпл #37:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Продам материнські плати на сокеті AM4",
  "item_type": "motherboard"
}
```
**Семпл #38:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Материнська плата монітора AOC I2369V, I2269VW (715G5812-M0D-000-004I)",
  "item_type": "motherboard"
}
```
**Семпл #39:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/komplekt-5-4590-asus-h81m-k-16gb-ram-ID10IPaD.html",
  "title": "комплект і5 4590 + asus h81m-k + 16gb ram"
}
```
**Семпл #40:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/materinskaya-plata-asus-prime-x670e-pro-wifi-ID10BURq.html",
  "title": "Материнская плата Asus Prime X670E-PRO WiFi"
}
```
**Семпл #41:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/materinsk-plati-asus-p8h61-m-lx3-r2-0-asus-h61m-k-s1155-ddr3-vga-dvi-ID10YMX3.html",
  "title": "Материнські плати Asus P8H61-M LX3 R2.0, Asus H61M-K,  s1155 ddr3, vga/dvi"
}
```
**Семпл #42:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Материнська плата Palit N61S V2.0 працює ПРОЦЕСОРУ НЕМА",
  "item_type": "motherboard"
}
```
**Семпл #43:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/gigabyte-ga-h87m-d3h-intel-xeon-e3-1275v3-i7-4771-ID10NRK7.html",
  "title": "Gigabyte GA-H87M-D3H + Intel Xeon E3-1275v3 (i7-4771)"
}
```
**Семпл #44:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Комплект Biostar G31D-M7, s775 E4500 2Gb озу",
  "item_type": "motherboard"
}
```
**Семпл #45:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/komplekt-asus-prime-h310m-k-i3-8100-8gb-ozu-ID10Zwek.html",
  "title": "Комплект Asus Prime H310M-K + i3-8100 + 8Gb ОЗУ"
}
```
**Семпл #46:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Мат. плата Biostar TP35D2-A7",
  "item_type": "motherboard"
}
```
**Семпл #47:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Комплект: материнська плата + процесор + кулер + 16GB RAM",
  "item_type": "motherboard"
}
```
**Семпл #48:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Материньська плата",
  "item_type": "motherboard"
}
```
**Семпл #49:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/materinska-plata-asus-h110m-cs-1151-v-1-IDZDiM1.html",
  "title": "Материнська плата Asus H110M-CS 1151 V.1"
}
```
**Семпл #50:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/lga-2011-bp-2401-x99-p4-ID10f8OH.html",
  "title": "Lga 2011 Bp 2401 x99-P4"
}
```
**Семпл #51:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "ASUS P8B75-M LX , продам материнську плату",
  "item_type": "motherboard"
}
```
**Семпл #52:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/materinska-plata-asus-rog-strix-b550-a-gaming-ID10Vc3Q.html",
  "title": "Материнська плата: ASUS ROG STRIX B550-A GAMING"
}
```
**Семпл #53:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/moschnyy-igrovoy-komplekt-asrock-b450m-pro-4-ryzen-5-3600-amd-amd-rayzen-am4-ID10Habh.html",
  "title": "Мощный игровой комплект ASROCK B450M PRO 4 Ryzen 5 3600 амд amd райзен am4"
}
```
**Семпл #54:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/materinskaya-plata-aorus-elite-b550-ax-v2-ID10YxbD.html",
  "title": "материнская плата aorus elite b550 ax v2"
}
```
**Семпл #55:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Материнская плата Gigabyte GA-EP43T-UD3L",
  "item_type": "motherboard"
}
```
**Семпл #56:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Материнські плати Apple PowerMac G4 (+)",
  "item_type": "motherboard"
}
```
**Семпл #57:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Материнская плата серверная ASUS P10S-M (P10S-M) \nIntel Socket 1151",
  "item_type": "motherboard"
}
```
**Семпл #58:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Материнка MSI H16M процесор G620 оперативка 4 Гб  1155  робоч кулер проц",
  "item_type": "motherboard"
}
```
**Семпл #59:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/materinka-jingyue-x99-titanium-d4-protsessor-2690v3-IDZ57dB.html",
  "title": "Материнка Jingyue x99 titanium D4 + процессор 2690v3"
}
```
**Семпл #60:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/biostar-mcp6pb-m2-amd-athlon-ii-x2-240-ID10qOYJ.html",
  "title": "Biostar MCP6PB M2+ AMD Athlon II X2 240"
}
```
**Семпл #61:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Комплект- Материнська плата+ процесор+ ОЗУ+ Відеокарта",
  "item_type": "motherboard"
}
```
**Семпл #62:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Материнская плата+ жесткий диск",
  "item_type": "motherboard"
}
```
**Семпл #63:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Материнська плата Biostar",
  "item_type": "motherboard"
}
```
**Семпл #64:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/materinskaya-plata-msi-ms-7653-ver-1-0-g41-ddr3-775-IDSE9fo.html",
  "title": "Материнская плата MSI MS-7653 ver 1.0 G41 DDR3 775"
}
```
**Семпл #65:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/igrovoy-komplekt-ryzen-5-3600-soyo-b450m-amd-amd-rayzen-5-am4-ID10S37M.html",
  "title": "Игровой комплект Ryzen 5 3600 SOYO B450M амд amd райзен 5 am4"
}
```
**Семпл #66:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/asus-sabertooth-z170-mark1-ID10Sz22.html",
  "title": "Asus Sabertooth Z170 Mark1"
}
```
**Семпл #67:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/komplekt-amd-ryzen-7800x3d-gigabyte-x870e-aorus-elite-wifi7-ID10U7KA.html",
  "title": "Комплект AMD Ryzen 7800X3D + Gigabyte X870E  AORUS ELITE WIFI7"
}
```
**Семпл #68:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/igrovoy-komplekt-msi-a520m-a-pro-ryzen-5-3500x-amd-amd-rayzen-5-am4-IDXhfMs.html",
  "title": "Игровой комплект MSI A520M A PRO Ryzen 5 3500X амд amd райзен 5 am4"
}
```
**Семпл #69:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Материнська плата msi k9n neo v2",
  "item_type": "motherboard"
}
```
**Семпл #70:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Материнская плата ASUS M2N-MX SE \\ DDR2 \\ сокет АМ2 AM2",
  "item_type": "motherboard"
}
```
**Семпл #71:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/i5-10600-asus-primeb460m-a-ID10CS6F.html",
  "title": "i5-10600 ASUS primeB460m-a"
}
```
**Семпл #72:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/materinskaya-plata-asus-p5kpl-am-na-4-yadra-ddr2-i-soket-775-IDSk23a.html",
  "title": "Материнская плата Asus P5KPL-AM на 4-ядра, DDR2 и сокет 775"
}
```
**Семпл #73:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Материнська  плата 775 сокет",
  "item_type": "motherboard"
}
```
**Семпл #74:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Intel D945GCL сокет 775 с поддержкой Core2Duo DDR2 от Intel",
  "item_type": "motherboard"
}
```
**Семпл #75:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "HP ProLiant DL120 G6 материнська плата на сокет 1156",
  "item_type": "motherboard"
}
```
**Семпл #76:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Материнська плата Intel Desktop Board D945PSN (LGA775, DDR2, PCI-E, GbLAN, 1394) — Перевірена!",
  "item_type": "motherboard"
}
```
**Семпл #77:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Материнская плата ECS G31T-M7 2xDDR2 1xPCIex16 SATA IDE сокет 775",
  "item_type": "motherboard"
}
```
**Семпл #78:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/msi-b760-gaming-plus-wifi-ddr5-igrovaya-materinskaya-plata-lga1700-ID10Lni0.html",
  "title": "MSI B760 GAMING PLUS WIFI DDR5 — игровая материнская плата LGA1700"
}
```
**Семпл #79:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "АКЦІЯ! Материнська плата Asus Prime N100I-D D4, Intel N100 Quad-Core 2.0GHz 1×Ddr4 Sodimm, VGA/HDMI/DP mITX",
  "item_type": "motherboard"
}
```
**Семпл #80:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/msi-x99a-raider-msi-x99a-sli-plus-lga-2011-v3-x99-ID10qtmN.html",
  "title": "MSI X99A Raider, MSI X99А SLI PLUS LGA 2011-v3 X99"
}
```
**Семпл #81:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Материнская плата Socket AM2+.Процессор AMD Athlon II X2.",
  "item_type": "motherboard"
}
```
**Семпл #82:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/materinska-plata-gigabyte-ga-g41m-es2l-g41-pcie-ddr2-quadcore-775-IDWGTRg.html",
  "title": "Материнська плата Gigabyte GA-G41M-ES2L G41 PCIe DDR2 QuadCore 775"
}
```
**Семпл #83:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Мультимедийная плата Acer WMCP78M Nvidia 9200 HDMI сокет AM2+ АМ3",
  "item_type": "motherboard"
}
```
**Семпл #84:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "IBM xSERIES 346 345 RISER Райзер 13M7338 2x PCI 40K6487 PCI-X M75IL",
  "item_type": "motherboard"
}
```
**Семпл #85:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/materinska-plata-msi-mpg-b550-gaming-plus-ID10ZtuL.html",
  "title": "Материнська плата MSI MPG B550 GAMING PLUS"
}
```
**Семпл #86:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/komplekt-gigabyte-ga-m61pme-s2-amd-athlon-5600-ddr2-2gb-IDYQwdT.html",
  "title": "Комплект Gigabyte GA-M61PME-S2 + AMD Athlon 5600 + DDR2 2GB"
}
```
**Семпл #87:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Материнська плата від монітора.",
  "item_type": "motherboard"
}
```
**Семпл #88:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Продам дві материнскі плати",
  "item_type": "motherboard"
}
```
**Семпл #89:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Бюджетний комплект s.1151",
  "item_type": "motherboard"
}
```
**Семпл #90:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "материнская плата, проц, 4 оперативы, б.у",
  "item_type": "motherboard"
}
```
**Семпл #91:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/komplekt-soyo-x99-d4-tpm-2-0-e5-2643-v3-16gb-intel-xeon-lga-2011-3-x99-ddr4-zeon-kseon-ID10S2vz.html",
  "title": "Комплект SOYO X99 D4 TPM 2.0 / E5 2643 v3 / 16GB intel xeon lga 2011-3 x99 ddr4 зеон ксеон"
}
```
**Семпл #92:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/materinska-plata-gigabyte-h310m-ds2-lga-1151-ID10M5RY.html",
  "title": "Материнська плата Gigabyte H310M DS2 LGA 1151"
}
```
**Семпл #93:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/materinskaya-plata-asus-prime-z370-p-1151v2-ID10Nut3.html",
  "title": "материнская плата asus prime z370-p 1151v2"
}
```
**Семпл #94:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/prodam-materinku-i-protsesor-msi-z590-plus-i7-11700k-overlokers-komplekt-ID10Ztjx.html",
  "title": "Продам материнку i процесор MSI Z590 Plus + i7 11700k !!!Overlokers комплект!!!"
}
```
**Семпл #95:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Продам нерабочую материнскую плату Gigabyte GA-970A-DS3P FX (Socket AM3+) под восстановление",
  "item_type": "motherboard"
}
```
**Семпл #96:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Компьютерный комплект",
  "item_type": "motherboard"
}
```
**Семпл #97:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Материнская плата TP.MS6486T.PB753",
  "item_type": "motherboard"
}
```
**Семпл #98:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/materinska-plata-gigabyte-b450-aorus-m-ID10Zt89.html",
  "title": "Материнська плата gigabyte B450 AORUS M"
}
```
**Семпл #99:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/materinska-plata-maynng-b75-12-usb-8gb-kuler-protsesor-ssd-128gb-IDOVHRN.html",
  "title": "Материнська плата  майнінг B75 12 USB, 8Гб, кулер, процесор, SSD 128Гб"
}
```
**Семпл #100:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Ретро комплект socket 462 AMD AthlonXP",
  "item_type": "motherboard"
}
```

#### ⚡ Блоки живлення (PSU) — Відсіяно (Показано 100 з max 100):
**Семпл #1:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "NEW Блоки живлення BITMAIN APW11 для S19/ S21+/ XP Hydro",
  "item_type": "psu"
}
```
**Семпл #2:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Провода от Блока Питания Cougar",
  "item_type": "psu"
}
```
**Семпл #3:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/bp-bzh-750w-z-garantyu-blok-zhivlennya-blok-pitaniya-gigabyte-p750gm-750w-80-gold-ID10RkTA.html",
  "title": "БП / БЖ 750W З ГАРАНТІЄЮ / блок живлення / блок питания Gigabyte P750GM 750W 80+ gold"
}
```
**Семпл #4:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Блок живлення Rittal 110-230 /48В /5A",
  "item_type": "psu"
}
```
**Семпл #5:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/prots-intel-core-i3-2125-blok-pitaniya-vortex-350w-radiatory-dlya-pk-IDYDTbn.html",
  "title": "Проц Intel Core i3- 2125, блок питания Vortex 350W, радиаторы для ПК"
}
```
**Семпл #6:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/atx-blok-zhivlennya-550w-qube-bronze-trade-in-ID10zmzV.html",
  "title": "ATX блок живлення 550W QUBE (bronze). Trade-IN"
}
```
**Семпл #7:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/blok-zhivlennya-premalniy-groviy-topoviy-chieftec-navitas-1250w-sertifkat-gold-plomba-stan-novogo-potuzhniy-ID10suls.html",
  "title": "Блок живлення преміальний,ігровий топовий Chieftec Navitas 1250W сертифікат Gold,пломба , стан нового, потужний"
}
```
**Семпл #8:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/blok-zhivlennya-enermax-marblebron-rgb-white-850w-80-bronze-napvmodulniy-ID10NYXC.html",
  "title": "Блок живлення Enermax MarbleBron RGB White 850W | 80+ Bronze | Напівмодульний"
}
```
**Семпл #9:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Продам блок питания",
  "item_type": "psu"
}
```
**Семпл #10:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Блок живлення модульний Chieftec APS-750CB",
  "item_type": "psu"
}
```
**Семпл #11:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Блок живлення EVGA SuperNOVA G+ 1300 G+",
  "item_type": "psu"
}
```
**Семпл #12:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "EEL-22W и EEL-22D для мониторов",
  "item_type": "psu"
}
```
**Семпл #13:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Vinga VPS-750G. Блок питания",
  "item_type": "psu"
}
```
**Семпл #14:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Блок питания Corsair AX1500 80 Plus Titanium",
  "item_type": "psu"
}
```
**Семпл #15:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/bloki-zhivlennya-fsp-hp-fujitsu-200-850w-IDVRYdh.html",
  "title": "Блоки живлення FSP HP FUJITSU 200-850W"
}
```
**Семпл #16:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "NEW Блоки живлення BITMAIN APW17 (APW171215c) для S21/ T21/ L9/ L11",
  "item_type": "psu"
}
```
**Семпл #17:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "ГАРАНТИЯ! Блок питания GameMax RGB 750 PRO WH (ATX3.1 PCIe5.1)",
  "item_type": "psu"
}
```
**Семпл #18:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Блок живлення Corsair TX650w",
  "item_type": "psu"
}
```
**Семпл #19:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Блок питания Chieftec GPM-1000C",
  "item_type": "psu"
}
```
**Семпл #20:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/blok-zhivlennya-be-quiet-s10-550w-ID10ZvQO.html",
  "title": "Блок живлення be quiet S10-550W"
}
```
**Семпл #21:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/blok-zhivlennya-msi-850w-mag-a850gl-pcie5-ID10ZvKN.html",
  "title": "Блок живлення MSI 850W MAG A850GL PCIE5"
}
```
**Семпл #22:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Оригінальний блок живлення Dell 65W 7.4x5.0 19.5V 3.34A DPN03V2F\n\nПере",
  "item_type": "psu"
}
```
**Семпл #23:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/blok-zhivlennya-corsair-hx1000-1000w-cp-9020139-ID10CjTg.html",
  "title": "Блок живлення Corsair HX1000 1000W (CP-9020139)"
}
```
**Семпл #24:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Продам БП Chieftec 450Ватт",
  "item_type": "psu"
}
```
**Семпл #25:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Продам блок живлення до компа.",
  "item_type": "psu"
}
```
**Семпл #26:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "КАК НОВЫЙ БП Chieftec Navitas  1450W 80+ GOLD ор.пломба и др, БП",
  "item_type": "psu"
}
```
**Семпл #27:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/aktsiya-750w-650w-chieftec-zalman-550w-600w-650w-700w-750w-IDYBWh0.html",
  "title": "•АКЦИЯ• 750w 650w Chieftec,Zalman 550w,600w,650w,700w,750w"
}
```
**Семпл #28:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/blok-zhivlennya-seasonic-prime-titanium-650w-ssr-650td-3734-IDYkaM6.html",
  "title": "Блок живлення Seasonic Prime Titanium 650W (SSR-650TD) - 3734"
}
```
**Семпл #29:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/blok-pitaniya-dlya-pk-750w-850w-21-23-god-vypuska-sostoyanie-novyh-IDWWTgf.html",
  "title": "Блок питания для Пк 750w 850w 21-23 год выпуска состояние новых !"
}
```
**Семпл #30:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/blok-zhivlennya-chieftec-a-90-gdp-750c-750w-80-gold-ID10NVQo.html",
  "title": "Блок живлення Chieftec A-90 GDP-750C 750W 80+ Gold"
}
```
**Семпл #31:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Блок живлення на 12 вольт",
  "item_type": "psu"
}
```
**Семпл #32:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Блок живлення Chieftec Smart PSF-400B",
  "item_type": "psu"
}
```
**Семпл #33:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Блок живлення для компактного компютера HP CE 8300",
  "item_type": "psu"
}
```
**Семпл #34:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/yaksniy-blok-zhivlennya-750w-gigabyte-p750gm-gold-trade-in-ID10uxwN.html",
  "title": "якісний блок живлення 750W Gigabyte P750GM GOLD. Trade-IN"
}
```
**Семпл #35:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Блок живлення Canon K30245",
  "item_type": "psu"
}
```
**Семпл #36:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Блок живлення, мережевий адаптер 5V - 0,8 A",
  "item_type": "psu"
}
```
**Семпл #37:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/blok-zhivlennya-chieftec-500w-proton-bdf-500s-ID10CTue.html",
  "title": "Блок живлення Chieftec 500W Proton (BDF-500S)"
}
```
**Семпл #38:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/prodam-blok-pitaniya-na-500w-ID10NWsV.html",
  "title": "Продам блок питания на 500w"
}
```
**Семпл #39:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Кількість, Кабель для ремонту блоків живлення Lenovo 20v 8.0*7.4 pin",
  "item_type": "psu"
}
```
**Семпл #40:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/be-quiet-dark-power-pro-12-1200w-titanium-p12-pro-1200w-topoviy-ultimativniy-rtx-gtx-rx-gt-gaming-oc-blok-zhivlennya-bzh-pitaniya-mx-ID10WB0I.html",
  "title": "be quiet! Dark Power Pro 12 1200W Titanium [P12-PRO-1200W] топовий Ультимативний RTX GTX RX gt  gaming oc блок живлення бж питания MX"
}
```
**Семпл #41:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/phanteks-amp-750w-80-plus-gold-seasonic-platforma-blok-zhivlennya-modulniy-groviy-bzh-bp-rtx-rx-gtx-gt-gaming-oc-ID10UoVz.html",
  "title": "Phanteks AMP 750W 80 Plus Gold (Seasonic платформа) Блок живлення модульний ігровий бж БП rtx rx gtx gt gaming oc"
}
```
**Семпл #42:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/napvmodulniy-blok-zhivlennya-chieftec-a-90-650w-gdp-650c-ID10V56L.html",
  "title": "Напівмодульний блок живлення Chieftec A-90 650W (GDP-650C)"
}
```
**Семпл #43:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/vinga-450w-topchik-ID10f8WP.html",
  "title": "VINGA 450W топчик"
}
```
**Семпл #44:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Силовий блок EServer WT-2261A-GER-8WAY-WO Black",
  "item_type": "psu"
}
```
**Семпл #45:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/blok-zhivlennya-be-quiet-straight-power-11-750w-IDZEy8m.html",
  "title": "Блок живлення be quiet! Straight Power 11 750W"
}
```
**Семпл #46:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "продам блок питание для системника",
  "item_type": "psu"
}
```
**Семпл #47:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Блок питания TRACO POWER TEN 5-2411",
  "item_type": "psu"
}
```
**Семпл #48:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Корпус блока питания SFP150-20AI",
  "item_type": "psu"
}
```
**Семпл #49:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Блок живлення PSU-B (PSU60B)",
  "item_type": "psu"
}
```
**Семпл #50:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Корпуса от блоков питания",
  "item_type": "psu"
}
```
**Семпл #51:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Транзистор FHP100N03",
  "item_type": "psu"
}
```
**Семпл #52:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/blok-pitaniya-400w-vinga-mini-ID10qObY.html",
  "title": "Блок питания 400w Vinga mini"
}
```
**Семпл #53:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Клавиатура AJAZZ ak820",
  "item_type": "psu"
}
```
**Семпл #54:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Блок Питания, Адаптер Монитора LG 19V 0.84A 1.3A 1.7A 2.1A 2.53A 3.42A",
  "item_type": "psu"
}
```
**Семпл #55:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "NEW Блоки живлення BITMAIN APW12 (APW121215F) для S19/ T19/ L7/ K7",
  "item_type": "psu"
}
```
**Семпл #56:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Corsair RM850x 80 Plus Gold 2023 рік Блок живлення ігровий модульний gtx rtx gt rx mx gaming oc",
  "item_type": "psu"
}
```
**Семпл #57:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/phanteks-amp-750w-80-plus-gold-seasonic-platforma-blok-zhivlennya-modulniy-groviy-bzh-bp-rtx-rx-gtx-gt-gaming-oc-ID10UoVz.html",
  "title": "Phanteks AMP 750W 80 Plus Gold (Seasonic платформа) Блок живлення модульний ігровий бж БП rtx rx gtx gt gaming oc"
}
```
**Семпл #58:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Бж Атх 350-400 Вт  неробочий під ремонт",
  "item_type": "psu"
}
```
**Семпл #59:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Блок живлення Deepcool PF750D-HA для компютера",
  "item_type": "psu"
}
```
**Семпл #60:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Блок живлення Seasonic Core GM-650 Gold (SSR-650LM)",
  "item_type": "psu"
}
```
**Семпл #61:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Блок живлення Chieftec під ремонт",
  "item_type": "psu"
}
```
**Семпл #62:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/blok-pitaniya-650w-chieftec-proton-bdf-650c-IDXInil.html",
  "title": "Блок питания 650W Chieftec Proton BDF-650C"
}
```
**Семпл #63:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/blok-zhivlennya-dell-750w-h750p-00-perehdnik-6-pin-na-8-pin-ID10ZsYO.html",
  "title": "Блок живлення Dell 750W (H750P-00) + перехідник 6-pin на 8-pin"
}
```
**Семпл #64:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Gigabyte P550B Bronze 80 plus блок живлення питания ПК",
  "item_type": "psu"
}
```
**Семпл #65:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Не працючий блок живлення Cougar cmx700",
  "item_type": "psu"
}
```
**Семпл #66:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "NEW Блоки живлення BITMAIN APW12 (APW121215a) для S19/ T19/ L7/ K7",
  "item_type": "psu"
}
```
**Семпл #67:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/lian-li-edge-850w-gold-2025-rk-eksklyuziv-topoviy-bzh-12vhpwr-svzhak-rtx-rx-gtx-mx-gt-gaming-oc-ID10LGw5.html",
  "title": "Lian Li EDGE 850W Gold 2025 рік Ексклюзив  Топовий бж 12VHPWR  Свіжак rtx rx gtx mx gt gaming oc"
}
```
**Семпл #68:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/blok-zhivlennya-thermaltake-berlin-750w-ID10YlER.html",
  "title": "Блок живлення thermaltake Berlin 750w"
}
```
**Семпл #69:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/blok-pitaniya-corsair-rm850x-850w-80-gold-polnostyu-modulnyy-ID10ZsFV.html",
  "title": "Блок питания Corsair RM850x 850W 80+ Gold (полностью модульный)"
}
```
**Семпл #70:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Блок живленя для пк",
  "item_type": "psu"
}
```
**Семпл #71:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/blok-pitaniya-dlya-pk-na-450w-ID10CR3K.html",
  "title": "Блок питания для ПК на 450W"
}
```
**Семпл #72:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Новый Блок питания GameMax GM-500B",
  "item_type": "psu"
}
```
**Семпл #73:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/servernyy-blok-pitaniya-dlya-gpu-na-6-videokart-5700-1400-w-IDT4Edx.html",
  "title": "Серверный блок питания для GPU на 6 видеокарт 5700 (1400 W)"
}
```
**Семпл #74:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/blok-zhivlennya-corsair-rm650x-650w-ID10ZsmW.html",
  "title": "Блок живлення Corsair RM650x 650W."
}
```
**Семпл #75:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/blok-pitaniya-thermaltake-850w-gold-otlichnyy-ID10mlXH.html",
  "title": "Блок питания Thermaltake 850w gold. Отличный"
}
```
**Семпл #76:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Серверний блок живлення hp HSTNS-PR16 2450W",
  "item_type": "psu"
}
```
**Семпл #77:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Блок питания Delta GPS-300JB A  . пример качественного блока питания",
  "item_type": "psu"
}
```
**Семпл #78:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/blok-zhivlennya-seasonic-vertex-gx-1200-1200w-gold-12122-gxafs-5475-IDYEgkT.html",
  "title": "Блок живлення Seasonic Vertex GX-1200 1200W Gold (12122 GXAFS) - 5475"
}
```
**Семпл #79:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/blok-zhivlennya-seasonic-focus-plus-850w-gold-ID10XC3a.html",
  "title": "Блок живлення Seasonic Focus Plus 850W Gold"
}
```
**Семпл #80:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/thermaltake-smart-bm3-650w-na-plomb-80-bronze-ID10jtzp.html",
  "title": "Thermaltake Smart BM3 650W | На пломбі, 80+ Bronze"
}
```
**Семпл #81:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Блоки живлення з ПК , є окремо кабелі живлення",
  "item_type": "psu"
}
```
**Семпл #82:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Блок живлення серверний  Helwett Packard  HP  HSTNS PR09 2250w + pico psu + кулери  розпаяний  2квт  12в",
  "item_type": "psu"
}
```
**Семпл #83:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/blok-zhivlennya-qube-750w-IDX8ZmG.html",
  "title": "Блок живлення qube 750w"
}
```
**Семпл #84:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Блок живлення 12в 400ватт",
  "item_type": "psu"
}
```
**Семпл #85:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Оригінальні кабелі до компютерних блоків живлення Asus",
  "item_type": "psu"
}
```
**Семпл #86:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/novyy-blok-pitaniya-600w-chiftec-gpc-600s-IDBv2YD.html",
  "title": "Новый Блок Питания 600W CHIFTEC GPC-600S"
}
```
**Семпл #87:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "блок питания для стационарного компьютера",
  "item_type": "psu"
}
```
**Семпл #88:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Серверний блок живлення HP 2650W HSTNS-PR42 розпаяний (732604-001)",
  "item_type": "psu"
}
```
**Семпл #89:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/blok-pitaniya-fsp-400w-atx-bez-dop-pitaniya-dlya-ofisa-domashnego-pk-ID101hwn.html",
  "title": "Блок питания FSP 400W (ATX) без доп. питания/ для офиса /домашнего Пк"
}
```
**Семпл #90:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Блок живлення питания зарядка Адаптер 3/4.5/6/7.5/9/12 5W 300mA",
  "item_type": "psu"
}
```
**Семпл #91:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/seasonic-prime-platinum-1300w-ssr-1300pd-platinum-flagman-etalonn-testi-plomba-rtx-rx-gtx-gt-mx-gaming-oc-ID10Paim.html",
  "title": "Seasonic PRIME Platinum 1300W (SSR-1300PD) Platinum Флагман  Еталонні тести  Пломба rtx rx gtx gt mx gaming oc"
}
```
**Семпл #92:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/blok-zhivlennya-seasonic-focus-plus-platinum-650w-ssr-650px-2243-IDYtbRs.html",
  "title": "Блок живлення Seasonic Focus Plus Platinum 650W (SSR-650PX) - 2243"
}
```
**Семпл #93:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/kompyuternyy-blok-pitaniya-450w-550w-650w-750w-850w-IDUqtPm.html",
  "title": "Компютерный блок питания 450w 550w 650w 750w 850w"
}
```
**Семпл #94:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Creative Sound Blaster Roar 2",
  "item_type": "psu"
}
```
**Семпл #95:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Блок живлення Sirtec HPC-350-102",
  "item_type": "psu"
}
```
**Семпл #96:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Блок живлення блок питания HP 365W для ПК стан робочий",
  "item_type": "psu"
}
```
**Семпл #97:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Блок питания на пк",
  "item_type": "psu"
}
```
**Семпл #98:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Блок питания к клавишам. Оригинальный.  MADE IN MEXICO",
  "item_type": "psu"
}
```
**Семпл #99:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Блок живлення Cougar",
  "item_type": "psu"
}
```
**Семпл #100:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/blok-zhivlennya-pk-750w-corsair-vengeance-750m-silver-ID10CPrA.html",
  "title": "Блок живлення ПК 750W CORSAIR Vengeance 750M Silver"
}
```

#### 💾 Накопичувачі (SSD / HDD) — Відсіяно (Показано 100 з max 100):
**Семпл #1:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/ssd-4tb-kingston-kc3000-m-2-2280-pcie-4-0-x4-nvme-3d-tlc-ID10gKah.html",
  "title": "SSD 4TB Kingston KC3000 M.2 2280 PCIe 4.0 x4 NVMe 3D TLC"
}
```
**Семпл #2:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/ssd-patriot-p300-512gb-nvme-95-deal-9-10-ID10TWnu.html",
  "title": "SSD Patriot P300 512GB NVMe  95%Ідеал 9/10"
}
```
**Семпл #3:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Продам жорсткий диск",
  "item_type": "storage"
}
```
**Семпл #4:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/ssd-m-2-512gb-nvme-samsung-pm9b1-2280-r-do-3500-mb-s-w-do-2500-mb-s-mzvl4512hblu-00bh1-pcie-4-0-x4-oem-noviy-klkst-garantya-ID10XfG0.html",
  "title": "SSD M.2 512GB NVMe Samsung PM9B1 2280 R: до 3500 MB/s, W: до 2500 MB/s (MZVL4512HBLU-00BH1) PCIe 4.0 x4 OEM Новий! Є кількість + Гарантія"
}
```
**Семпл #5:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/ssd-nakopichuvach-crucial-bx500-2tb-sata-iii-3-roki-garant-ID10X9sy.html",
  "title": "SSD накопичувач Crucial BX500 2TB Sata III (3 роки гарантії)"
}
```
**Семпл #6:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/ssd-disk-240gb-patriot-burst-sata3-2-5-trade-in-ID10GkbP.html",
  "title": "SSD диск 240GB Patriot BURST (SATA3 \\ 2.5\"). Trade-IN"
}
```
**Семпл #7:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/top-vibr-m-2-ssd-disk-1tb-samsung-970-evo-plus-pci-e-3-0-x4-nvme-trade-in-ID10pEqg.html",
  "title": "ТОП вибір M.2 SSD диск 1TB Samsung 970 EVO PLUS (PCI-e 3.0 x4. NVMe). Trade-in"
}
```
**Семпл #8:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/prodayu-hdd-disk-6-tb-serverniy-sas-pdklyuchennya-IDYDSPH.html",
  "title": "Продаю Hdd диск 6 tb серверний sas підключення"
}
```
**Семпл #9:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/zhorstkiy-disk-3-5-wd-500-gb-wd5003abyx-ID10NYNo.html",
  "title": "Жорсткий диск  3.5 WD 500 Gb WD5003ABYX"
}
```
**Семпл #10:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/ssd-nakopichuvacha-kodak-x200-series-512-gb-ID10Zxgi.html",
  "title": "SSD-накопичувача Kodak X200 Series (512 GB)"
}
```
**Семпл #11:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/nova-kingston-ssd-m2-240-gb-IDZYy4J.html",
  "title": "Нова KINGSTON SSD m2 240 Gb"
}
```
**Семпл #12:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Intel Optane P1600X 118GB NVMe SSD (SSDPEK1A118GA) 3D XPoint 100% Health",
  "item_type": "storage"
}
```
**Семпл #13:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/ssd-disk-nakopichuvach-samsung-evo-860-250gb-ID10mcNn.html",
  "title": "SSD диск накопичувач Samsung EVO 860 250гб"
}
```
**Семпл #14:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/ssd-wd-crucial-500gb-100-zhittya-ID10YCwb.html",
  "title": "Ssd wd crucial 500gb 100% життя"
}
```
**Семпл #15:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/prodam-rostovku-novyh-ssd-diskov-64gb-4tb-priehali-vkusnyashki-IDZQCT0.html",
  "title": "Продам ростовку новых SSD дисков 64гб-4тб (приехали вкусняшки)"
}
```
**Семпл #16:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/prodam-ssd-ssd-nakopitel-2-5-sata-512gb-transcend-ts512gssd230s-ID10BZSw.html",
  "title": "Продам ССД / SSD-накопитель 2.5\" SATA 512GB Transcend (TS512GSSD230S)"
}
```
**Семпл #17:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/zhorstkiy-disk-2-5-seagate-500gb-st500lt012-ID10NXHx.html",
  "title": "жорсткий диск 2.5 Seagate 500gb ST500LT012"
}
```
**Семпл #18:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Ide шлейф кабель fdd для флопіка",
  "item_type": "storage"
}
```
**Семпл #19:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "SSD Goodram SSDPR-PX500-017-80-G3: 1024,2 GB",
  "item_type": "storage"
}
```
**Семпл #20:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/vnchester-zhorstkiy-disk-2-5-noutbuk-250-gb-sata-seagate-st9250315as-IDZupB7.html",
  "title": "Вінчестер жорсткий диск 2,5\" (ноутбук) 250 Gb SATA Seagate ST9250315AS"
}
```
**Семпл #21:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/ssd-micron-512gb-mtfdhba512qfd-mnmalne-napratsyuvannya-ID10ZwWA.html",
  "title": "Ssd Micron 512Gb MTFDHBA512QFD мінімальне напрацювання"
}
```
**Семпл #22:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/ssd-m-2-1tb-nvme-micron-3500-2280-r-do-7000-mb-s-w-do-6900-mb-s-mtfdkba1t0tgd-pcie-4-0-x4-oem-noviy-klkst-garantya-ID10KLEN.html",
  "title": "SSD M.2 1Tb NVMe Micron 3500 2280 R: до 7000 MB/s, W: до 6900 MB/s  (MTFDKBA1T0TGD) PCIe 4.0 x4 OEM Новий! Є кількість + Гарантія"
}
```
**Семпл #23:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/samsung-9100-pro-1tb-nvme-ssd-mz-vap1t0bw-IDZ3v6f.html",
  "title": "Samsung 9100 PRO 1TB NVMe SSD (MZ-VAP1T0BW)"
}
```
**Семпл #24:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/zhestkiy-disk-toshiba-500gb-sata-iii-IDSO5VI.html",
  "title": "Жёсткий диск Toshiba 500Gb SATA III"
}
```
**Семпл #25:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/ssd-kingston-nv3-1tb-m-2-97-ID10WvQV.html",
  "title": "SSD Kingston NV3 1TB M.2  (97%)"
}
```
**Семпл #26:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/noviy-zapakovaniy-ssd-disk-klevv-cras-c910-3d-nand-slc-1tb-m-2-ssd-1tb-ID10UOAU.html",
  "title": "Новий, запакований SSD-диск KLEVV CRAS C910 3D NAND SLC 1TB M.2. ССД 1ТБ"
}
```
**Семпл #27:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/nvme-1tb-samsung-wd-toshiba-sk-hynix-IDNY9hY.html",
  "title": "nvme 1Tb SAMSUNG, WD, Toshiba, SK Hynix"
}
```
**Семпл #28:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/zhorstkiy-disk-wd-purple-500gb-1tb-2tb-3tb-4tb-8tb-IDVoDwf.html",
  "title": "Жорсткий диск WD Purple 500Gb, 1TB, 2TB, 3TB, 4TB, 8TB"
}
```
**Семпл #29:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/ssd-disk-1tb-goodram-cx400-sata3-2-5-trade-in-ID10uxJw.html",
  "title": "SSD диск 1TB GOODRAM CX400 (SATA3 \\ 2.5\"). Trade-IN"
}
```
**Семпл #30:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/ssd-patriot-p300-512gb-nvme-95-deal-9-10-ID10TWnu.html",
  "title": "SSD Patriot P300 512GB NVMe  95%Ідеал 9/10"
}
```
**Семпл #31:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/prodam-disk-ssd-kingston-a400-240gb-ID10Zwoy.html",
  "title": "Продам диск SSD, Kingston A400 240GB"
}
```
**Семпл #32:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/new-ssd-samsung-micron-480gb-sm883-sm863a-rm881-5300max-IDYNQbo.html",
  "title": "NEW! SSD Samsung, Micron 480Gb (SM883, SM863a, РМ881, 5300Max)"
}
```
**Семпл #33:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/prodam-zhorstkiy-disk-hdd-10tb-ID10Zw6v.html",
  "title": "Продам жорсткий диск HDD 10tb"
}
```
**Семпл #34:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/ssd-nvme-seagate-xm1441-2tb-1-92-pamyat-mlc-IDZTaiC.html",
  "title": "SSD NVME Seagate XM1441 2TB (1.92) память MLC"
}
```
**Семпл #35:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/zhostkiy-disk-500gb-tonkiy-slm-nout-IDWvNsW.html",
  "title": "Жосткий Диск 500гб тонкий слім Ноут"
}
```
**Семпл #36:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/ssd-m-2-kingston-snv2s-1-tb-pcie-4-0-x4-3d-nand-ID10Zub3.html",
  "title": "SSD M.2 Kingston SNV2S/1 TB (PCIe 4.0 x4 3D NAND)"
}
```
**Семпл #37:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Жорсткі диски, SDD",
  "item_type": "storage"
}
```
**Семпл #38:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/western-digital-re3-wd1002fbys-3-5-7200rpm-32mb-sata-ii-300-1tb-IDRmUGl.html",
  "title": "Western Digital RE3 WD1002FBYS 3.5 7200rpm 32Mb SATA-II 300 1Tb"
}
```
**Семпл #39:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/disk-ssd-sata3-256-512gb-2-5-nov-IDZwW6p.html",
  "title": "Диск SSD SATA3 256-512Gb 2.5 Нові!"
}
```
**Семпл #40:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/sd-m2-2230-na-256-gb-disk-nakopichuvach-western-digital-kioxia-dlya-noutbukv-ta-pk-ID10Iuui.html",
  "title": "SD m2.2230 на 256 ГБ, диск накопичувач Western Digital, Kioxia для ноутбуків та ПК"
}
```
**Семпл #41:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/ssd-m2-nvme-128-gb-250gb-480gb-1-tb-samsung-hunix-toshiba-perehdniki-do-kompyutera-pci-e-ta-operativna-pamyat-ram-ID102Fzz.html",
  "title": "SSD m2 NVME 128 Гб, 250Gb 480Gb 1 tb Samsung Hunix Toshiba, є перехідники до компютера PCI e та  оперативна память RAM"
}
```
**Семпл #42:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/zhestkiy-disk-3-5-sata-seagate-7200-10-st380815as-80gb-IDGYCtl.html",
  "title": "Жесткий диск 3,5 SATA Seagate 7200.10 ST380815AS 80ГБ"
}
```
**Семпл #43:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/ssd-m2-nvme-2280-samsung-256gb-nvme-2280-512gb-sk-hynix-nvme-western-digital-2230-dlya-pk-noutbuka-IDZPAa7.html",
  "title": "ssd m2 nvme 2280 SAMSUNG 256GB нвме 2280 512gb SK hynix nvme Western Digital 2230 для пк ноутбука"
}
```
**Семпл #44:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/zhestkiy-disk-hdd-3-5-500gb-7200-dlya-kompyutera-ID10aY5b.html",
  "title": "Жесткий диск HDD 3.5 500GB 7200  для компьютера"
}
```
**Семпл #45:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/vinchester-sata-seagate-pipeline-hd-2-st3500312cs-na-500gb-IDPcz6R.html",
  "title": "Винчестер SATA Seagate Pipeline HD.2 ST3500312CS на 500Гб"
}
```
**Семпл #46:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/zhorstkiy-disk-wd-8-tb-purple-ID10Ztyo.html",
  "title": "Жорсткий диск WD 8 TB Purple"
}
```
**Семпл #47:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/prodam-ssd-128-gb-sata-ID10Ztyf.html",
  "title": "Продам ssd 128 gb sata"
}
```
**Семпл #48:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/zhestkiy-disk-western-digital-av-gp-32mb-wd5000avds-3-5-sata-ii-500gb-IDT7Dky.html",
  "title": "Жесткий Диск Western Digital AV-GP 32MB WD5000AVDS 3.5 SATA II 500Гб"
}
```
**Семпл #49:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/prodam-ssd-sata-240-gb-ID10ZtwN.html",
  "title": "Продам ssd sata 240 gb"
}
```
**Семпл #50:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/prodam-hdd-250-gb-ID10ZtoK.html",
  "title": "Продам hdd 250 gb"
}
```
**Семпл #51:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "накопичувач Samsung SSD M2 NVMe 970 EVO Plus",
  "item_type": "storage"
}
```
**Семпл #52:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/ssd-grucial-p3-plus-4tb-ID10ZgyS.html",
  "title": "SSD Grucial P3 Plus 4TB"
}
```
**Семпл #53:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/zhorstkiy-disk-3-5-10tb-wd-wd102purp-noviy-ID10SKEb.html",
  "title": "Жорсткий диск 3.5\" 10TB WD (WD102PURP) (Новий)"
}
```
**Семпл #54:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/prodam-hdd-320-gb-ID10ZtiG.html",
  "title": "Продам hdd 320 gb"
}
```
**Семпл #55:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/ssd-m-2-wd-black-sn770-1tb-ID10Zt7V.html",
  "title": "SSD M.2 WD Black SN770 1TB"
}
```
**Семпл #56:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/zhestkiy-disk-wd-black-500gb-wd5000lplx-2-5-kak-novyy-ID10C0yW.html",
  "title": "Жесткий диск WD Black 500gb WD5000LPLX 2.5 как новый"
}
```
**Семпл #57:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/ssd-kingston-a400-500480-gb-form-faktor-2-5-ID10Zt2e.html",
  "title": "SSD Kingston A400 500(480) GB, форм фактор 2.5"
}
```
**Семпл #58:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/zhorstkiy-disk-4tb-seagate-st4000vx007-4-tb-IDXFTxW.html",
  "title": "Жорсткий диск 4TB Seagate ST4000VX007  4 Tb"
}
```
**Семпл #59:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/ssd-1tb-goodram-cx400-gen-2-2-5-sataiii-3d-nand-qlc-ssdpr-cx400-01t-g2-noviy-ID10f6MM.html",
  "title": "SSD 1TB Goodram CX400 Gen.2 2.5\" SATAIII 3D NAND QLC (SSDPR-CX400-01T-G2) Новий"
}
```
**Семпл #60:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/zhorstkiy-disk-western-digital-blue-12tb-sata-iii-wd120eagz-ID10COBX.html",
  "title": "Жорсткий диск Western Digital Blue 12TB SATA III (WD120EAGZ)"
}
```
**Семпл #61:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/100-helth-hgst-3-5-8tb-sas-12gb-s-7-2k-rpm-nakopichuvach-5-shtuk-IDXHTvL.html",
  "title": "100% helth! HGST 3.5\" 8TB SAS 12Gb/s 7.2K rpm (Накопичувач, є 5 штук)"
}
```
**Семпл #62:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/prodayu-zhestkiy-disk-na-320-gb-IDZGhDI.html",
  "title": "Продаю жёсткий диск на 320 Гб"
}
```
**Семпл #63:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "жоскій діск Seagate FreeAgent GoFlex",
  "item_type": "storage"
}
```
**Семпл #64:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/ssd-nakopichuvach-crucial-bx500-2tb-sata-iii-3-roki-garant-ID10X9sy.html",
  "title": "SSD накопичувач Crucial BX500 2TB Sata III (3 роки гарантії)"
}
```
**Семпл #65:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Жорсткі диски hdd 2,5” (для ноутбуків, компʼютерів)",
  "item_type": "storage"
}
```
**Семпл #66:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/nakopichuvach-ssd-m-2-512gb-apacer-ID10VTXv.html",
  "title": "Накопичувач SSD M.2 512GB Apacer"
}
```
**Семпл #67:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/zhorstkiy-disk-western-digital-black-6tb-sata-iii-wd6004fzbx-ID100PEP.html",
  "title": "Жорсткий Диск Western Digital Black 6TB SATA III (WD6004FZBX)"
}
```
**Семпл #68:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/zhorstkiy-disk-hdd-6tb-12tb-western-digital-wd-ultrastar-seagate-skyhawk-ai-ID10qMYe.html",
  "title": "Жорсткий диск HDD 6TB, 12TB Western Digital (WD) ULTRASTAR, SEAGATE SkyHawk AI"
}
```
**Семпл #69:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Продам жостки діск ссд 512",
  "item_type": "storage"
}
```
**Семпл #70:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/nakopichuvach-na-250gb-IDSpXiC.html",
  "title": "Накопичувач на 250гб"
}
```
**Семпл #71:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/prodam-zhorstkiy-disk-na-500-gb-IDZL7de.html",
  "title": "Продам жорсткий диск на 500 гб"
}
```
**Семпл #72:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/srochno-zhestkiy-disk-2-5-toshiba-mq01abf050-500gb-IDWiSPI.html",
  "title": "Срочно! Жёсткий диск 2,5 Toshiba MQ01ABF050 500Gb"
}
```
**Семпл #73:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "SSD накопитель Samsung 970 EVO",
  "item_type": "storage"
}
```
**Семпл #74:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/noviy-zhorstkiy-disk-toshiba-x300-8tb-7200rpm-performance-pc-hdwr180xzsta-ID10ZqIP.html",
  "title": "Новий жорсткий диск Toshiba X300 8TB 7200rpm Performance PC HDWR180XZSTA"
}
```
**Семпл #75:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Не рабочие жёсткие диски",
  "item_type": "storage"
}
```
**Семпл #76:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/prodam-zhestkiy-disk-8-tb-IDWMt2H.html",
  "title": "Продам жесткий диск 8 тб"
}
```
**Семпл #77:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/lot-25-sht-hdd-500gb-sata-ID10M9va.html",
  "title": "Лот: 25 шт hdd 500Gb Sata"
}
```
**Семпл #78:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/orico-e5000-pcle-4-0-nvme-m-2-ssd-2280-2tb-vnutrenniy-karman-kebid-ID108Tsg.html",
  "title": "ORICO e5000 PCle 4.0 NVMe M.2 SSD (2280) 2Tb + внутренний карман Kebid"
}
```
**Семпл #79:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "SSD-диск Adata Legend 710",
  "item_type": "storage"
}
```
**Семпл #80:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "SSD Intel DC S3610 Series 1.6TB, під відновлення",
  "item_type": "storage"
}
```
**Семпл #81:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/nakopichuvach-dlya-pk-hdd-1tb-2tb-ID10Zou0.html",
  "title": "Накопичувач для ПК HDD 1Tb, 2Tb"
}
```
**Семпл #82:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/prodam-zhestkiy-disk-wd-blue-320-gb-2-5-sata-ID10NRW9.html",
  "title": "Продам жесткий диск WD Blue 320 ГБ (2.5\", SATA)"
}
```
**Семпл #83:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Жорсткий диск Seagate Medalist SL (ST51080N)",
  "item_type": "storage"
}
```
**Семпл #84:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/zhorstkiy-disk-2-5-hitachi-hts541612j9sa00-120gb-IDR5jG2.html",
  "title": "Жорсткий диск 2.5\" HITACHI HTS541612J9SA00 120GB"
}
```
**Семпл #85:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/zhorstkiy-disk-320gb-western-digital-wd-av-wd3200avjb-ID10Zoky.html",
  "title": "Жорсткий диск 320gb Western Digital WD AV (WD3200AVJB)"
}
```
**Семпл #86:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/zhorstkiy-disk-250gb-hitachi-deskstar-t7k250-hdt722525dlat80-ID10Zoih.html",
  "title": "Жорсткий диск 250gb Hitachi Deskstar T7K250 (HDT722525DLAT80)"
}
```
**Семпл #87:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/ssd-wd-blue-sn570-nvme-500-gb-ID10Zohw.html",
  "title": "SSD WD Blue SN570 NVMe, 500 ГБ"
}
```
**Семпл #88:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Жёсткий диск продам",
  "item_type": "storage"
}
```
**Семпл #89:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/zhorstkiy-disk-160gb-samsung-hd160hj-ID10ZofX.html",
  "title": "Жорсткий диск 160gb Samsung HD160HJ"
}
```
**Семпл #90:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/ssd-mlc-samsung-sm883-240-gb-sm863a-ID10UtvQ.html",
  "title": "SSD MLC! Samsung SM883 240 Gb (SM863а)"
}
```
**Семпл #91:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/ssd-diski-goodram-480-512-1tb-IDXF7CU.html",
  "title": "Ssd диски Goodram 480/512/1tb."
}
```
**Семпл #92:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/ssd-crucial-p3-plus-4tb-ID10YNJp.html",
  "title": "SSD Crucial P3 Plus 4TB"
}
```
**Семпл #93:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Оригинал Корзина салазки Hdd caddy dell \" 3.5\" кошки, tray металеві і металево-пластикові з болтами",
  "item_type": "storage"
}
```
**Семпл #94:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/m-2-ssd-disk-512gb-micron-2300-z-buferom-nvme-pci-e-3-0-x4-trade-in-ID108oiC.html",
  "title": "M.2 SSD диск 512GB Micron 2300 з буфером (NVMe\\PCI-e 3.0 x4). Trade-IN"
}
```
**Семпл #95:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Жесткий диск",
  "item_type": "storage"
}
```
**Семпл #96:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/hdd-western-digital-blue-160gb-wd1600aajs-ID10tCwk.html",
  "title": "HDD Western Digital Blue 160GB (WD1600AAJS)"
}
```
**Семпл #97:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/ssd-patriot-128gb-novyy-ne-yuzanyy-prakticheski-lyubye-proverki-testy-po-zaprosu-ID10ZnpJ.html",
  "title": "Ssd Patriot 128gb новый не юзаный практически любые проверки тесты по запросу"
}
```
**Семпл #98:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/ssd-m-2-samsung-970-evo-250gb-z-radatorom-nvme-v-nand-ID10COCC.html",
  "title": "SSD M.2 Samsung 970 EVO 250GB з радіатором / NVMe V-NAND"
}
```
**Семпл #99:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "SSD-диск Adata Legend 710",
  "item_type": "storage"
}
```
**Семпл #100:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "SEAGATE ST-225 HARD DRIVE на подарунок компьютернику",
  "item_type": "storage"
}
```

#### 📟 Оперативна пам'ять (RAM) — Відсіяно (Показано 100 з max 100):
**Семпл #1:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/operativna-pamyat-ddr4-16gb-2x8gb-ID10OEAz.html",
  "title": "Оперативна память DDR4 16GB 2x8GB"
}
```
**Семпл #2:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Оперативная память к ноутбуку DDR 5",
  "item_type": "ram"
}
```
**Семпл #3:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "оперативна память TeamGroup Elite (модель TED34G1600C11BK),",
  "item_type": "ram"
}
```
**Семпл #4:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Оперативна память, озу Ddr1, ddr2",
  "item_type": "ram"
}
```
**Семпл #5:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/grova-operativna-pamyat-xpg-ddr4-32gb-2x16gb-tsna-vkazana-za-2-shtuki-3200mhz-ID100565.html",
  "title": "Ігрова Оперативна память XPG DDR4 32GB 2x16GB ціна вказана за 2 штуки. 3200MHz"
}
```
**Семпл #6:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/kingston-fury-beast-ddr4-32gb-216gb-3600mhz-cl18-ID10ZxKx.html",
  "title": "Kingston Fury Beast DDR4 32GB (2×16GB) 3600MHz CL18"
}
```
**Семпл #7:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Жорсткий диск та память для нетбука.",
  "item_type": "ram"
}
```
**Семпл #8:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/modul-pamyat-operativna-pamyat-dlya-kompyutera-ddr4-32gb-2x16gb-3600-mhz-fury-renegade-black-kingston-fury-ex-hyperx-kf436c16rb12k2-32-ID10Yqw6.html",
  "title": "Модуль памяті (оперативна памʼять) для компютера DDR4 32GB (2x16GB) 3600 MHz Fury Renegade Black Kingston Fury (ex.HyperX) (KF436C16RB12K2/32)"
}
```
**Семпл #9:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Оперативная память ноутбука.",
  "item_type": "ram"
}
```
**Семпл #10:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/servernaya-pamyat-hynix-ddr3-16-gb-vsego-32-gb-1600mhz-ram-IDZEBze.html",
  "title": "серверная память hynix ddr3 16 гб  всего 32 гб 1600mhz ram"
}
```
**Семпл #11:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/pamyat-ddr5-dlya-pk-64gb-2x32-5600mhz-exceleram-trade-in-ID10e0ew.html",
  "title": "память DDR5 для ПК 64GB (2x32) 5600MHz EXCELERAM. Trade-IN"
}
```
**Семпл #12:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "DDR2 Apacer 2 ГБ",
  "item_type": "ram"
}
```
**Семпл #13:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/komplekt-ozu-goodram-irdm-x-ddr4-16gb-2x8gb-3200-mhz-cl16-ID10Zxjn.html",
  "title": "Комплект ОЗУ GoodRAM IRDM X DDR4 16GB (2x8GB) 3200 MHz CL16"
}
```
**Семпл #14:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "оперативна памʼять PATRIOT 16GB (2x8) 3200Mhz (PV416G320C6K)",
  "item_type": "ram"
}
```
**Семпл #15:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Оперативная память DDR2 2 GB / (Intel/Amd)(оперативна память ДДР2-2гб)",
  "item_type": "ram"
}
```
**Семпл #16:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/operativna-pamyat-ddr4-32-gb2x16-3200mhz-netac-ID10VEqd.html",
  "title": "Оперативна память DDR4 32 Gb(2x16) 3200Mhz Netac"
}
```
**Семпл #17:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/operativna-pamyat-hyperx-fury-ddr4-16gb-2x8-3600mhz-cl17-ID10Zxgy.html",
  "title": "Оперативна память HyperX Fury DDR4 16GB (2x8) 3600MHz CL17"
}
```
**Семпл #18:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/servernaya-4gb-8500e-4gb-10600e-4gb-12800e-unbuffered-ddr3-IDDZxhU.html",
  "title": "Серверная 4GB 8500E / 4GB 10600E / 4GB 12800E Unbuffered DDR3"
}
```
**Семпл #19:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Серверная 8GB PC2-5300F ECC REG DDR2 667MHz FB DIMM",
  "item_type": "ram"
}
```
**Семпл #20:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/servernaya-4gb-8gb-pc3-10600r-ecc-reg-ddr3-1333-mhz-rdimm-IDDZBD8.html",
  "title": "Серверная 4GB / 8GB PC3-10600R ECC REG DDR3 1333 MHz RDIMM"
}
```
**Семпл #21:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/operativna-pamyat-kingston-16gb-ddr4-3200-mgts-1-2-v-IDZit2b.html",
  "title": "Оперативна память Kingston 16GB DDR4 3200 МГц 1.2 V"
}
```
**Семпл #22:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Оперативная память к компьютеру A-Data 1Gb DDR PC-3200 400MHz",
  "item_type": "ram"
}
```
**Семпл #23:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/operativna-pamyat-ddr5-32gb-2x16gb-5600-mhz-crucial-komplekt-ID101nSI.html",
  "title": "Оперативна памʼять DDR5 32GB (2x16GB) 5600 MHz Crucial – комплект"
}
```
**Семпл #24:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/ddr3-8-gb-prodam-planki-operativki-ID10NXmU.html",
  "title": "DDR3 8 Gb продам планки оперативки"
}
```
**Семпл #25:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Оперативна память DDR 3 4 Gb",
  "item_type": "ram"
}
```
**Семпл #26:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Продам оперативною память   DDR4  1на 16 Kingston FURY Beast DDR4",
  "item_type": "ram"
}
```
**Семпл #27:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Оперативная память",
  "item_type": "ram"
}
```
**Семпл #28:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/komplekt-operativna-pamyat-ddr4-netac-shadow-ii-3200mhz-2x8gb-2x16gb-ID10OLoH.html",
  "title": "Комплект Оперативна памʼять DDR4 Netac Shadow II 3200Mhz 2x8gb / 2x16gb"
}
```
**Семпл #29:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/geil-evo-x-black-ddr4-3000-mhz-32gb-2x16gb-ID10H4x2.html",
  "title": "GeIL EVO X Black DDR4 3000 Mhz 32GB (2x16GB)"
}
```
**Семпл #30:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Оперативная память 2gb",
  "item_type": "ram"
}
```
**Семпл #31:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/operativnaya-pamyat-kingston-fury-ddr5-5600-pc5-44800-16gb-2x8gb-kf556c40bbk2-16-ID10x1qG.html",
  "title": "Оперативная память Kingston Fury DDR5-5600 PC5-44800 16GB (2x8GB) (KF556C40BBK2-16)"
}
```
**Семпл #32:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/ssd-nakopichuvach-samsung-990-evo-plus-2280-pcie-5-0-x2-nvme-2-0-1tb-ID10ZvIM.html",
  "title": "SSD-накопичувач Samsung 990 Evo Plus 2280 PCIe 5.0 x2 NVMe 2.0 1TB"
}
```
**Семпл #33:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/serverna-operativna-pamyat-rdimm-ecc-ddr3-4-4-8-16gb-1333-2666mgts-IDYVZDZ.html",
  "title": "Серверна оперативна память RDIMM ECC DDR3/4 4/8/16Gb 1333-2666Мгц"
}
```
**Семпл #34:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "оперативна память DDR 3",
  "item_type": "ram"
}
```
**Семпл #35:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/kingston-hyperx-furi-ddr3-1886-8gb-IDQB1du.html",
  "title": "Kingston Hyperx Furi DDR3 -1886 8GB"
}
```
**Семпл #36:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Оперативная память две планки по 512 MB DDR 1",
  "item_type": "ram"
}
```
**Семпл #37:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/kingston-fury-beast-ddr5-32-gb-216-gb-6400-mhz-ID10Zvbg.html",
  "title": "Kingston FURY Beast DDR5 32 ГБ (2×16 ГБ) 6400 MHz"
}
```
**Семпл #38:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/operativka-g-skill-ddr3-8-gb-24-gb-ID10NXlY.html",
  "title": "Оперативка G.Skill DDR3 8 ГБ (2×4 ГБ)"
}
```
**Семпл #39:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/ddr1-ddr2-ddr3-operativnaya-pamyat-1gb-2gb-4gb-8gb-IDQDZVb.html",
  "title": "DDR1, DDR2, DDR3 оперативная память (1gb, 2gb, 4gb, 8gb)"
}
```
**Семпл #40:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/nove-garantya-operativna-pamyat-ddr5-64gb-2x32gb-6000-cl30-g-skill-trident-z5-rgb-black-f5-6000j3040g32gx2-tz5rk-IDZOpsT.html",
  "title": "Нове/ГАРАНТІЯ | Оперативна память DDR5 64GB (2x32GB) 6000/CL30 G.SKILL Trident Z5 RGB Black (F5-6000J3040G32GX2-TZ5RK)"
}
```
**Семпл #41:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/operativna-pamyat-ozu-ram-ddr4-samsung-kingston-sk-hynix-32gb-16x2-dlya-pk-ID10za2i.html",
  "title": "Оперативна памʼять ОЗУ RAM DDR4 Samsung, Kingston, SK Hynix 32gb (16x2) для ПК"
}
```
**Семпл #42:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/operativna-pamyat-netac-shadow-iii-ddr4-16gb-2x8gb-3200mhz-cl16-nova-ID10Yu0S.html",
  "title": "Оперативна память Netac Shadow III DDR4 16GB (2x8GB) 3200MHz CL16. Нова."
}
```
**Семпл #43:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Оперативна память 2 ГБ, DDR3, Micron (1600 МГц, MT8JTF25664AZ-1G6M1)",
  "item_type": "ram"
}
```
**Семпл #44:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/ddr4-16gb-3200-mhz-fury-beast-black-kingston-fury-28gb-ID10VBz2.html",
  "title": "DDR4 16GB 3200 MHz Fury Beast Black Kingston Fury 2*8Gb"
}
```
**Семпл #45:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/prodam-ssd-1tb-2tb-4tb-8tb-ssd-m2-2tb-IDYYVJs.html",
  "title": "Продам  SSD 1TB / 2TB / 4TB /  8TB  |      SSD M2   2TB"
}
```
**Семпл #46:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Планки DDR2 памяти по 512МБ каждая",
  "item_type": "ram"
}
```
**Семпл #47:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/operativna-pamyat-corsair-32-gb-216-gb-ddr5-7200-mhz-dominator-titanium-rgb-white-cmp32gx5m2x7200c34w-ID10XxMI.html",
  "title": "Оперативна Память Corsair 32 GB (2×16 GB) DDR5 7200 MHz Dominator Titanium RGB White (CMP32GX5M2X7200C34W)"
}
```
**Семпл #48:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/operativna-pamyat-fury-beast-black-ddr5-6000-32gb-expo-kf560c36bbe2k2-32-ID10XvmH.html",
  "title": "Оперативна Память FURY Beast Black DDR5-6000 32GB EXPO (KF560C36BBE2K2-32)"
}
```
**Семпл #49:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/operativna-pamyat-patriot-32-gb-216-gb-ddr5-6000-mhz-viper-venom-black-pvv532g600c30k-ID10Xzg6.html",
  "title": "Оперативна Память PATRIOT 32 GB (2×16 GB) DDR5 6000 MHz Viper Venom Black (PVV532G600C30K)"
}
```
**Семпл #50:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/operativna-pamyat-kingston-fury-64-gb-232-gb-so-dimm-ddr5-4800-mhz-fury-impact-kf548s38ibk2-64-ID10Xv2W.html",
  "title": "Оперативна память Kingston FURY 64 GB (2×32 GB) SO-DIMM DDR5 4800 MHz FURY Impact (KF548S38IBK2-64)"
}
```
**Семпл #51:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/operativna-pamyat-g-skill-ripjaws-s5-ddr5-6400-64gb-f5-6400j3239g32gx2-rs5k-ID10XprJ.html",
  "title": "Оперативна память G.Skill Ripjaws S5 DDR5-6400 64GB (F5-6400J3239G32GX2-RS5K)"
}
```
**Семпл #52:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/operativna-pamyat-patriot-32-gb-216-gb-ddr5-6000-mhz-viper-elite-5-ultra-rgb-matte-black-veur532g6028k-ID10XzyG.html",
  "title": "Оперативна память PATRIOT 32 GB (2×16 GB) DDR5 6000 MHz Viper Elite 5 Ultra RGB Matte Black (VEUR532G6028K)"
}
```
**Семпл #53:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/operativna-pamyat-netac-shadow-iii-ddr4-16gb-2x8gb-3200mhz-cl16-nova-ID10Yu0S.html",
  "title": "Оперативна память Netac Shadow III DDR4 16GB (2x8GB) 3200MHz CL16. Нова."
}
```
**Семпл #54:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/g-skill-trident-z5-rgb-ddr5-7200-32gb-2x16gb-cl34-ID10b8CF.html",
  "title": "G.SKILL Trident Z5 RGB DDR5 -7200 32GB (2x16GB) CL34"
}
```
**Семпл #55:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/prodam-pamyat-dlya-noutbukov-ddr4-16-8-4-2gb-ddr3-8-4gb-ddr2-2gb-ID10Qznq.html",
  "title": "Продам память для ноутбуков. DDR4-16-8-4-2GB/DDR3-8-4GB/DDR2-2GB."
}
```
**Семпл #56:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Оперативная память ОЗУ",
  "item_type": "ram"
}
```
**Семпл #57:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/operativna-pamyat-g-skill-trident-z5-neo-ddr5-6000-64gb-f5-6000j3040g32gx2-tz5n-ID10XqBV.html",
  "title": "Оперативна память G.Skill Trident Z5 Neo DDR5-6000 64GB (F5-6000J3040G32GX2-TZ5N)"
}
```
**Семпл #58:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/operativna-pamyat-g-skill-32-gb-216-gb-ddr5-6000-mhz-flare-x5-f5-6000j3636f16gx2-fx5-ID10XyuH.html",
  "title": "Оперативна Память G.Skill 32 GB (2×16 GB) DDR5 6000 MHz Flare X5 (F5-6000J3636F16GX2-FX5)"
}
```
**Семпл #59:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/operativna-pamyat-patriot-32-gb-ddr5-6000-mhz-viper-elite-5-veb532g6030kw-ID10XnHT.html",
  "title": "Оперативна память PATRIOT 32 GB DDR5 6000 MHz Viper Elite 5 (VEB532G6030KW)"
}
```
**Семпл #60:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/operativna-pamyat-corsair-64-gb-232-gb-ddr5-5200-mhz-vengeance-rgb-cmh64gx5m2b5200c40-ID10Xy1s.html",
  "title": "Оперативна память Corsair 64 GB (2×32 GB) DDR5 5200 MHz Vengeance RGB (CMH64GX5M2B5200C40)"
}
```
**Семпл #61:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/operativna-pamyat-kingston-fury-64-gb-232-gb-ddr5-6000-mhz-beast-expo-white-kf560c36bwek2-64-ID10XwV5.html",
  "title": "Оперативна память Kingston FURY 64 GB (2×32 GB) DDR5 6000 MHz Beast EXPO White (KF560C36BWEK2-64)"
}
```
**Семпл #62:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/operativna-pamyat-g-skill-trident-z5-neo-rgb-ddr5-6000-32gb-f5-6000j3038f16gx2-tz5nr-ID10Xs9y.html",
  "title": "Оперативна память G.Skill Trident Z5 Neo RGB DDR5-6000 32GB (F5-6000J3038F16GX2-TZ5NR)"
}
```
**Семпл #63:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/operativna-pamyat-g-skill-trident-z5-rgb-ddr5-6400-64gb-f5-6400j3239g32gx2-tz5rk-ID10Xorv.html",
  "title": "Оперативна память G.Skill Trident Z5 RGB DDR5-6400 64GB (F5-6400J3239G32GX2-TZ5RK)"
}
```
**Семпл #64:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/operativna-pamyat-g-skill-32-gb-216-gb-ddr4-3600-mhz-trident-z-rgb-f4-3600c18d-32gtzr-ID10XyO6.html",
  "title": "Оперативна Память G.Skill 32 GB (2×16 GB) DDR4 3600 MHz Trident Z RGB (F4-3600C18D-32GTZR)"
}
```
**Семпл #65:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/operativna-pamyat-corsair-64-gb-232-gb-ddr5-6000-mhz-vengeance-rgb-cmh64gx5m2b6000z40-ID10XxvC.html",
  "title": "Оперативна Память Corsair 64 GB (2×32 GB) DDR5 6000 MHz Vengeance RGB (CMH64GX5M2B6000Z40)"
}
```
**Семпл #66:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/grova-operativna-pamyat-u-radatorah-ddr3-4-2-4-8-16gb-1333-3200mhz-IDZcpEO.html",
  "title": "Ігрова оперативна память у радіаторах DDR3/4 2/4/8/16гб 1333-3200MHz"
}
```
**Семпл #67:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/g-skill-aegis-ddr4-16gb-operativnaya-pamyat-ID10Z2WS.html",
  "title": "G.Skill Aegis DDR4 16gb оперативная память"
}
```
**Семпл #68:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Продам память до ПК",
  "item_type": "ram"
}
```
**Семпл #69:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/operativna-pamyat-corsair-32-gb-216-gb-ddr5-6000-mhz-vengeance-rgb-amd-expo-cmh32gx5m2e6000z36-ID10XxnA.html",
  "title": "Оперативна Память Corsair 32 GB (2×16 GB) DDR5 6000 MHz Vengeance RGB AMD EXPO (CMH32GX5M2E6000Z36)"
}
```
**Семпл #70:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/operativna-pamyat-kingston-fury-64-gb-232-gb-so-dimm-ddr5-5600-mhz-impact-kf556s40ibk2-64-ID10Xx1b.html",
  "title": "Оперативна память Kingston FURY 64 GB (2×32 GB) SO-DIMM DDR5 5600 MHz Impact (KF556S40IBK2-64)"
}
```
**Семпл #71:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/operativna-pamyat-kingston-fury-32-gb-216-gb-ddr5-6000-mhz-beast-rgb-expo-white-kf560c36bwe2ak2-32-ID10XwGS.html",
  "title": "Оперативна память Kingston FURY 32 GB (2×16 GB) DDR5 6000 MHz Beast RGB EXPO White (KF560C36BWE2AK2-32)"
}
```
**Семпл #72:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/operativna-pamyat-g-skill-ripjaws-m5-neo-rgb-ddr5-6000-96gb-f5-6000j3036f48gx2-rm5nrk-ID10Xp2e.html",
  "title": "Оперативна память G.Skill Ripjaws M5 Neo RGB DDR5-6000 96GB (F5-6000J3036F48GX2-RM5NRK)"
}
```
**Семпл #73:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/operativna-pamyat-kingston-fury-64-gb-6400-mhz-beast-white-kf564c32bwek2-64-ID10XqSK.html",
  "title": "Оперативна память Kingston FURY 64 GB 6400 MHz Beast White (KF564C32BWEK2-64)"
}
```
**Семпл #74:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/operativna-pamyat-team-32-gb-216-gb-ddr5-6000-mhz-t-force-delta-rgb-white-ff4d532g6000hc38adc01-ID10XyYy.html",
  "title": "Оперативна память TEAM 32 GB (2×16 GB) DDR5 6000 MHz T-Force Delta RGB White (FF4D532G6000HC38ADC01)"
}
```
**Семпл #75:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/operativna-pamyat-g-skill-trident-z5-neo-ddr5-32-gb-6000-mhz-ID10Xt6y.html",
  "title": "Оперативна память G.Skill Trident Z5 Neo DDR5 32 GB 6000 MHz"
}
```
**Семпл #76:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/ozu-ddr3-4gb-operativnaya-pamyat-IDWIR54.html",
  "title": "ОЗУ DDR3 4gb, оперативная память"
}
```
**Семпл #77:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Оперативна память для ноутбука DDR-5",
  "item_type": "ram"
}
```
**Семпл #78:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Оперативная память Kingston 2гб",
  "item_type": "ram"
}
```
**Семпл #79:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/geil-ddr4-32gb-2h16-3200mhz-cl16-operativna-pamyat-ID10STnR.html",
  "title": "GeiL DDR4 32GB (2х16) 3200Mhz CL16  Оперативна память"
}
```
**Семпл #80:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Оперативна память ддр4 4гб пк",
  "item_type": "ram"
}
```
**Семпл #81:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/kingston-fury-impact-ddr5-64gb-2x32gb-4800mhz-cl38-ID10YNFU.html",
  "title": "Kingston FURY Impact DDR5 64GB (2x32GB) 4800MHz CL38"
}
```
**Семпл #82:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Оперативна память 512mb ddr2 2gb ddr3",
  "item_type": "ram"
}
```
**Семпл #83:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/operativna-pamyat-ddr3-1-2-4-8gb-1333-1600-1866mhz-IDVCVuF.html",
  "title": "Оперативна память DDR3 1/2/4/8Gb 1333/1600/1866MHz"
}
```
**Семпл #84:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/kingston-48-gb-ddr5-ksm56e46bd8km-48hm-ID10WYDI.html",
  "title": "Kingston 48 Gb DDR5 (KSM56E46BD8KM-48HM)"
}
```
**Семпл #85:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Лот оперативної памяті SO-DIMM DDR3 / DDR3L для ноутбуків — 12 планок (Комплект)",
  "item_type": "ram"
}
```
**Семпл #86:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Оперативна памʼять",
  "item_type": "ram"
}
```
**Семпл #87:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Оперативна память для пк 2gb",
  "item_type": "ram"
}
```
**Семпл #88:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/ozu-samsung-ddr4-3200-4gb-so-dimm-ID10f8I3.html",
  "title": "Озу samsung DDR4 3200 4GB SO-DIMM"
}
```
**Семпл #89:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "DDR 3 на 4 гб оперативка",
  "item_type": "ram"
}
```
**Семпл #90:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "DDR 3 на 2GB оперативна память",
  "item_type": "ram"
}
```
**Семпл #91:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Оперативная память ОЗУ-Good Ram DDR2 1Gb PC2 6400 DIMM",
  "item_type": "ram"
}
```
**Семпл #92:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Комплект Micron DDR3L 1867MHz 16GB (8+8) 1.35V 2Rx8 PC3L-14900 [ максимальна швидкість ], оперативна память, оригінал",
  "item_type": "ram"
}
```
**Семпл #93:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/teamgroup-rgb-ddr4-16gb-2x8-2666mhz-cl15-operativna-pamyat-ID10STtD.html",
  "title": "TeamGroup RGB DDR4 16GB (2X8) 2666Mhz CL15 Оперативна память"
}
```
**Семпл #94:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/operativna-pamyat-so-dimm-ddr5-4800mhz-2x8gb-16gb-ID10XCm8.html",
  "title": "Оперативна память SO-DIMM DDR5 4800MHz 2x8GB (16GB)"
}
```
**Семпл #95:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/operativna-pamyat-kingston-ddr4-32gb-2400mhz-ktd-pe424-32g-ID10NNBR.html",
  "title": "Оперативна память  Kingston DDR4 32GB/2400MHz (KTD-PE424/32G)"
}
```
**Семпл #96:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Продам оперативну память GLOWAY DDR5 24GB (2x12GB) 5600 MT/s Біла (Б/В)",
  "item_type": "ram"
}
```
**Семпл #97:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/ddr3-1600-mgts-4-gb-IDWCSow.html",
  "title": "DDR3 1600 МГц 4 Гб"
}
```
**Семпл #98:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Оперативная память patriot для пк на 2 Gb 2 штуки",
  "item_type": "ram"
}
```
**Семпл #99:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/operativna-pamyat-goodram-32gb-2x16-3200-ddr4-ID10eAe7.html",
  "title": "Оперативна память Goodram 32gb (2x16) 3200 DDR4"
}
```
**Семпл #100:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Оперативная память ddr2, dimm 256mb",
  "item_type": "ram"
}
```

#### 📦 Комплекти (Bundles) — Відсіяно (Показано 0 з max 100):
_Жодного відсіяного оголошення в цій категорії._

### 🎯 Успішно розпізнані моделі заліза (по 40 прикладів для кожної категорії):
#### 🎮 Відеокарти (GPU) — Розпізнано (Показано 1 з max 40):
**Зразок #1:**
```json
{
  "raw_title": "Видеокарта Sapphire PULSE Radeon RX Vega 56 8GB (Аналог GTX1660SUPER) Состояние новой",
  "matched_target": "gtx_1660_super",
  "item_type": "gpu",
  "detected_socket": null,
  "has_defects": false,
  "price_uah": 6200
}
```

#### 🧠 Процесори (CPU) — Розпізнано (Показано 1 з max 40):
**Зразок #1:**
```json
{
  "raw_title": "Процесор Intel Xeon E3-1226 v3",
  "matched_target": "xeon_e3_1226_v3",
  "item_type": "cpu",
  "detected_socket": null,
  "has_defects": false,
  "price_uah": 633
}
```

#### 🔌 Материнські плати (Motherboard) — Розпізнано (Показано 1 з max 40):
**Зразок #1:**
```json
{
  "raw_title": "Мать Asus h110 + проц i5 6400+ охлажление",
  "matched_target": "bundle_i5_6400_h110",
  "item_type": "motherboard",
  "detected_socket": null,
  "has_defects": false,
  "price_uah": 1900
}
```

#### ⚡ Блоки живлення (PSU) — Розпізнано (Показано 0 з max 40):
_Жодного оголошення з цієї категорії не розпізнано під час запуску._

#### 💾 Накопичувачі (SSD / HDD) — Розпізнано (Показано 1 з max 40):
**Зразок #1:**
```json
{
  "raw_title": "Жорсткі диски, жёсткие диски,ssd,250gb,500gb, 750gb",
  "matched_target": "ssd_250gb",
  "item_type": "storage",
  "detected_socket": null,
  "has_defects": true,
  "price_uah": 100
}
```

#### 📟 Оперативна пам'ять (RAM) — Розпізнано (Показано 0 з max 40):
_Жодного оголошення з цієї категорії не розпізнано під час запуску._

#### 📦 Комплекти (Bundles) — Розпізнано (Показано 0 з max 40):
_Жодного оголошення з цієї категорії не розпізнано під час запуску._

============================================================

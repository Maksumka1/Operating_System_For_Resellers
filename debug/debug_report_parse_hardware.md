# 🐛 ДЕБАГ-ЗВІТ ПАРСИНГУ КОМПЛЕКТУЮЧИХ OLX (GraphQL)
**Дата та час запуску:** 2026-08-02 19:28:14
**Тривалість виконання:** 145.88 сек
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
- **Завантажено URLs для дедуплікації:** 10289

### ⚙️ Секція: Parser_Config
- **Цільових моделей комплектуючих:** 1900

### ⚙️ Секція: OLX_GraphQL
- **Отримано оголошень [videokarty]:** 260
- **Отримано оголошень [protsessory]:** 259
- **Отримано оголошень [materinskie-platy]:** 259
- **Отримано оголошень [bloki-pitaniya]:** 257
- **Отримано оголошень [zhestkie-diski]:** 258
- **Отримано оголошень [moduli-pamyati]:** 259

### ⚙️ Секція: Filtering_Rules
- **Відсіяно if (Не розпізнано модель заліза):** 494

### ⚙️ Секція: Parsing_Metrics
- **Успішно розпізнано [gpu]:** 3
- **Успішно розпізнано [cpu]:** 5
- **Успішно розпізнано [motherboard]:** 4
- **Успішно розпізнано [psu]:** 1
- **Успішно розпізнано [storage]:** 2
- **Успішно розпізнано [ram]:** 22
- **Виявлено товарів з дефектами:** 1

### ⚙️ Секція: Summary
- **Знайдено нових унікальних оголошень:** 37

### ⚙️ Секція: Supabase_Output
- **Успішно збережено нових оголошень:** 37

### ⚙️ Секція: WebSocket
- **Успішно надіслано тригер стріму:** 2

## 🔄 3. Детальні приклади даних
### 🚫 Відсіяні оголошення (по 100 прикладів для кожної категорії):
#### 🎮 Відеокарти (GPU) — Відсіяно (Показано 100 з max 100):
**Семпл #1:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/vdeokarta-palit-geforce-gtx-1650-stormx-4gb-gddr5-magazin-garantya-90-dnv-ID102Uy5.html",
  "title": "Відеокарта Palit GeForce GTX 1650 StormX 4GB GDDR5 | МАГАЗИН | Гарантія 90 днів"
}
```
**Семпл #2:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/nvidia-msi-aero-gtx-1080-8gb-ID10AUDP.html",
  "title": "Nvidia MSI Aero GTX 1080 8Gb"
}
```
**Семпл #3:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Видеокарта 1Gb 2Gb DDR3 DDR5",
  "item_type": "gpu"
}
```
**Семпл #4:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/vdeokarta-gtx-1050-ID10CX1d.html",
  "title": "Відеокарта GTX 1050"
}
```
**Семпл #5:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/rx-580-8gb-net-izobrazheniya-ID10Z3UN.html",
  "title": "RX 580 8GB  нет изображения"
}
```
**Семпл #6:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/vdeokarta-gigabyte-aorus-geforce-rtx-5080-master-16g-ID10RewC.html",
  "title": "Відеокарта GIGABYTE AORUS GeForce RTX 5080 MASTER 16G"
}
```
**Семпл #7:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/grova-vdeokarta-msi-gtx-1080-ti-11gb-aero-IDXuxCU.html",
  "title": "ігрова відеокарта MSI GTX 1080 ti 11gb AERO"
}
```
**Семпл #8:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/vdeokarta-asus-expedition-rx470-4gb-IDWvjjP.html",
  "title": "Відеокарта Asus Expedition RX470 4gb"
}
```
**Семпл #9:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/msi-geforce-gtx-1060-3gb-b-v-IDOHNjb.html",
  "title": "MSI GeForce GTX 1060 3GB (б/в)"
}
```
**Семпл #10:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/nvidia-geforce-3060-ti-8-gb-v-otlichnom-sostoyanii-ID10Z3xL.html",
  "title": "Nvidia Geforce 3060 ti 8 gb в отличном состоянии"
}
```
**Семпл #11:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Відеокарта GIGABYTE",
  "item_type": "gpu"
}
```
**Семпл #12:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/videokarta-gainward-phantom-rtx-5090-ID10WAsg.html",
  "title": "Видеокарта Gainward Phantom RTX 5090"
}
```
**Семпл #13:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/vdeokarta-nvida-p104-100-8gb-IDY9OFh.html",
  "title": "Відеокарта Nvida p104-100 8gb"
}
```
**Семпл #14:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/topovaya-sapphire-rx-580-8-gb-lyubye-testy-magazin-compic-IDXxLcf.html",
  "title": "Топовая Sapphire rx 580 8 gb Любые тесты Магазин CompiC"
}
```
**Семпл #15:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Відеокарта Palit 64 мб",
  "item_type": "gpu"
}
```
**Семпл #16:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/prodam-vdeokartu-asus-geforce-gts-450-ID10Lw2E.html",
  "title": "Продам відеокарту,  ASUS GeForce GTS 450"
}
```
**Семпл #17:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/palit-geforce-rtx-4070-ti-super-gamingpro-oc-ID10Z3oG.html",
  "title": "Palit GeForce RTX 4070 Ti SUPER GamingPro OC"
}
```
**Семпл #18:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/vdeokarta-asus-radeon-hd-2600-xt-ID10eIeQ.html",
  "title": "Відеокарта ASUS Radeon HD 2600 XT"
}
```
**Семпл #19:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Відеокарта Radeon 9000 128 Mb, NVIDIA RIVA TNT2 M64 32 Mb AGP Тест ОК",
  "item_type": "gpu"
}
```
**Семпл #20:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Відеокарта GV-RX580GAMING-4GD",
  "item_type": "gpu"
}
```
**Семпл #21:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/vdeokarta-gigabyte-aorus-geforce-gtx-1060-xtreme-gaming-6gb-gddr5-ID10eHZM.html",
  "title": "Відеокарта Gigabyte Aorus GeForce GTX 1060 Xtreme Gaming 6GB GDDR5"
}
```
**Семпл #22:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/videokarta-rx580-4gb-IDZOI8W.html",
  "title": "Видеокарта rx580 4gb"
}
```
**Семпл #23:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Турбинные и коробочные старые PCI видеокарты",
  "item_type": "gpu"
}
```
**Семпл #24:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/vdeokarta-asus-geforce-gtx-1650-4gb-ID10Z35x.html",
  "title": "Відеокарта ASUS GeForce GTX 1650 4GB"
}
```
**Семпл #25:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/vdeokarta-palit-geforce-rtx-2060-12-gb-ID10Yx0N.html",
  "title": "Відеокарта Palit GeForce RTX 2060 12 GB"
}
```
**Семпл #26:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/videokarta-rx9070-xt-red-devil-na-garantii-ID10ThRg.html",
  "title": "Видеокарта RX9070 XT Red Devil (на гарантии)"
}
```
**Семпл #27:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/vdeokarta-gigabyte-geforce-rtx-5060-ti-gaming-oc-16-gb-ID10Lvnw.html",
  "title": "Відеокарта Gigabyte GeForce RTX 5060 Ti Gaming OC 16 GB"
}
```
**Семпл #28:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Відеокарта Dell AMD Radeon HD 8490 1Gb GDDR3 64bit PCI-E Тест ОК",
  "item_type": "gpu"
}
```
**Семпл #29:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/vdeokarta-radeon-rx-580-4gb-xfx-IDVaVFH.html",
  "title": "Відеокарта Radeon RX 580 4GB XFX"
}
```
**Семпл #30:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/rx-550-2g-msi-aero-ID10Z329.html",
  "title": "Rx 550 2g, msi aero"
}
```
**Семпл #31:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/msi-gtx-1050-ti-gaming-x-4gb-holodnaya-v-rabochem-sostoyanii-ID10Z30L.html",
  "title": "MSI Gtx 1050 Ti Gaming X 4gb ( холодная / в рабочем состоянии )"
}
```
**Семпл #32:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/nvidia-gtx-1050-ti4gb-vdnovleno-ID10qjrf.html",
  "title": "Nvidia gtx 1050 ti(4gb) відновлено"
}
```
**Семпл #33:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "продам видеокарту 1660 msi 6gb",
  "item_type": "gpu"
}
```
**Семпл #34:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/prodam-msi-rtx-5060-ti-16gb-shedow-2x-ID10Z2Ur.html",
  "title": "Продам Msi rtx 5060 ti 16gb Shedow 2x"
}
```
**Семпл #35:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/vdeokarta-palit-geforce-gtx-1660-super-6gb-gddr6-ID10Z2U6.html",
  "title": "Відеокарта Palit GeForce GTX 1660 Super 6GB GDDR6"
}
```
**Семпл #36:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/videokarta-nvidia-rtx-2080-asus-strix-8gb-ID10Z2T2.html",
  "title": "Видеокарта Nvidia RTX 2080 Asus Strix 8gb"
}
```
**Семпл #37:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/asus-prime-rx-9070-oc-16gb-ID10Z2S5.html",
  "title": "Asus Prime RX 9070 OC 16GB"
}
```
**Семпл #38:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/vdeokarta-zotac-geforce-rtx-5080-solid-core-16gb-gddr7-dlss4-magazin-compic-ID10FmyV.html",
  "title": "Відеокарта Zotac GeForce RTX 5080 Solid Core 16GB GDDR7 DLSS4 Магазин CompiC"
}
```
**Семпл #39:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/sapphire-nitro-amd-radeon-rx-580-8gb-gddr5-ID10S6X9.html",
  "title": "Sapphire NITRO+ AMD Radeon RX 580 8GB GDDR5"
}
```
**Семпл #40:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/vdeokarta-msi-geforce-gtx-1080-ti-armor-11g-oc-b-v-garantya-3-msyats-ID10MqiG.html",
  "title": "Відеокарта MSI GeForce GTX 1080 TI ARMOR 11G OC Б/в + Гарантія 3 місяці!"
}
```
**Семпл #41:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Робоча рх470 на 4",
  "item_type": "gpu"
}
```
**Семпл #42:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Zotac GT9500 512MB",
  "item_type": "gpu"
}
```
**Семпл #43:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/gigabbyte-rtx-2070-super-windforce-oc-3x-8g-ID10Z2EG.html",
  "title": "Gigabbyte RTX 2070 super windforce OC 3x 8G"
}
```
**Семпл #44:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Asus tuf 3070 8gb",
  "item_type": "gpu"
}
```
**Семпл #45:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/videokarta-nvidia-geforce-1080ti-IDZXfY5.html",
  "title": "Видеокарта Nvidia GeForce 1080ti"
}
```
**Семпл #46:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/videokarta-asus-cmp-40hx-8gb-ddr6-IDYDnVX.html",
  "title": "Видеокарта Asus CMP 40HX  8gb ddr6"
}
```
**Семпл #47:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/vdeokarta-gigabyte-geforce-gtx-650-ti-oc-2gb-gddr5-hynix-hdmi-2x-dvi-vga-opengl-4-6-vulkan-dx12-ID10Z2lJ.html",
  "title": "Відеокарта GIGABYTE GeForce GTX 650 Ti OC 2GB GDDR5 Hynix HDMI 2x DVI VGA OpenGL 4.6 Vulkan Dx12"
}
```
**Семпл #48:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/prodam-vdeokartu-sapphire-pure-radeon-rx-9070-xt-ID10YdJn.html",
  "title": "Продам відеокарту Sapphire Pure Radeon RX 9070 XT"
}
```
**Семпл #49:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/sapphire-amd-radeon-rx550-2gb-gddr5-pci-e-graphics-video-card-dp-dvi-hdmi-ID10Z28U.html",
  "title": "SAPPHIRE AMD Radeon RX550 2GB GDDR5 PCI-E Graphics Video Card DP DVI HDMI"
}
```
**Семпл #50:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/videokarty-p102-100-manli-10gb-ID10074H.html",
  "title": "Видеокарты P102-100 Manli 10Gb"
}
```
**Семпл #51:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/rtx-3080-10gb-evga-ftw3-ultra-IDYDtMD.html",
  "title": "RTX 3080 10GB EVGA FTW3 ultra"
}
```
**Семпл #52:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/palit-geforce-rtx-4060-dual-oc-ID10YYc9.html",
  "title": "Palit GeForce RTX 4060 Dual OC"
}
```
**Семпл #53:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/videokarta-rtx-2080-ti-11-gb-asus-rog-strix-chitat-opisanie-ID10WjNB.html",
  "title": "Видеокарта Rtx 2080 ti 11 gb Asus rog strix Читать описание!"
}
```
**Семпл #54:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/sapphire-amd-radeon-rx550-2gb-gddr5-pci-e-graphics-video-card-dp-dvi-hdmi-ID10Z28U.html",
  "title": "SAPPHIRE AMD Radeon RX550 2GB GDDR5 PCI-E Graphics Video Card DP DVI HDMI"
}
```
**Семпл #55:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/videokarty-p102-100-manli-10gb-ID10074H.html",
  "title": "Видеокарты P102-100 Manli 10Gb"
}
```
**Семпл #56:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/rx470-sapphire-4g-vdeokarta-amd-radeon-ID10Z22R.html",
  "title": "rx470 sapphire 4g Відеокарта amd radeon"
}
```
**Семпл #57:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/vdeokarta-amd-radeon-pro-w6600-8gb-gddr6-4k-8k-10bit-hdr-4h-dp1-4-pcie-4-0-130w-ID10CqRs.html",
  "title": "Відеокарта AMD Radeon Pro W6600 - (8GB GDDR6, 4K/8K 10Bit HDR, 4х DP1.4, PCIe 4.0 130W)"
}
```
**Семпл #58:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/nvidia-rtx-3080-turbo-10-gb-ID10qlcs.html",
  "title": "Nvidia RTX 3080 turbo 10 Gb"
}
```
**Семпл #59:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/vdeokarta-rx-5700xt-asus-strix-ID10Z1GD.html",
  "title": "Відеокарта Rx 5700xt Asus Strix"
}
```
**Семпл #60:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/ideal-gtx-1660-super-6gb-na-plombe-s-korobkoy-ID10wYv0.html",
  "title": "Идеал! GTX 1660 Super 6gb на пломбе с коробкой"
}
```
**Семпл #61:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/rx-470-8gb-artefakty-ID10YUM4.html",
  "title": "Rx 470 8gb артефакты"
}
```
**Семпл #62:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/gtx-1050-ti-4gb-ID10UUgk.html",
  "title": "Gtx 1050 ti 4gb"
}
```
**Семпл #63:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/vdeokarta-amd-radeon-hd-5770-1gb-gddr5-128-bit-ID10Z1yg.html",
  "title": "Відеокарта AMD Radeon HD 5770 1GB GDDR5 (128-bit)"
}
```
**Семпл #64:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/videokarta-nvidia-quadro-p400-ID10WUPM.html",
  "title": "Видеокарта Nvidia Quadro P400."
}
```
**Семпл #65:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/gigabyte-geforce-rtx-5080-gaming-oc-16-gb-gddr-7-256-bit-ID10uOpg.html",
  "title": "GIGABYTE GeForce RTX 5080 GAMING OC 16-Gb GDDR-7 (256 bit)"
}
```
**Семпл #66:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/grova-vdeokarta-asus-rx-570-4gb-dual-klkst-3sht-opt-4200-ID10XGK9.html",
  "title": "Ігрова відеокарта ASUS RX 570 4GB  (Dual). Є кількість 3шт, Опт 4200."
}
```
**Семпл #67:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/videokarta-asus-rog-strix-gtx-1050-ti-4-gb-ID10Z1wO.html",
  "title": "Видеокарта Asus Rog STRIX GTX 1050 Ti 4 GB"
}
```
**Семпл #68:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/sapphire-hd-2600-pro-IDX7h7g.html",
  "title": "Sapphire hd 2600 pro"
}
```
**Семпл #69:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/prodam-vdeokartu-gigabyte-geforce-gtx-760-4gb-IDZE6Rh.html",
  "title": "Продам відеокарту Gigabyte GeForce GTX 760 4GB"
}
```
**Семпл #70:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/videokarta-gainward-geforce-gtx-650-ti-1gb-gddr5-128bit-smotr-opisanie-IDZOGeb.html",
  "title": "Видеокарта Gainward GeForce GTX 650 Ti  1GB GDDR5 (128bit) смотр.описание"
}
```
**Семпл #71:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/vdeokarta-asus-radeon-hd-7770-1-gb-artefakti-na-zapchastini-IDZGY1i.html",
  "title": "Відеокарта  Asus Radeon HD 7770 1 GB, артефакти , на запчастини."
}
```
**Семпл #72:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "35 см PSU кабель 12V-2×6 PCIe conneсtor 450W PCIe 5.0",
  "item_type": "gpu"
}
```
**Семпл #73:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Сетевые и видеокарты на ПК б/у.",
  "item_type": "gpu"
}
```
**Семпл #74:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/kuleri-dlya-vdeokarti-1660-super-gigabyte-komplekt-IDYoztb.html",
  "title": "Кулери для відеокарти 1660 Super Gigabyte (комплект)"
}
```
**Семпл #75:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/videokarta-msi-nvidia-geforce-nx8800gt-t2d512e-oc-512mb-ID10qkte.html",
  "title": "Видеокарта  MSI nVidia  GeForce NX8800GT-T2D512E-OC 512MB:"
}
```
**Семпл #76:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/vdeokarta-asus-pci-ex-geforce-gtx-260-896-mb-gddr3-448bit-576-1998-dvi-x-2-engtx260-2di-896md3-ID10eFEI.html",
  "title": "Відеокарта Asus PCI-Ex GeForce GTX 260 896 MB GDDR3 (448bit) (576/1998) (DVI x 2) (ENGTX260/2DI/896MD3)"
}
```
**Семпл #77:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/vdeokarta-msi-ventus-3x-plus-geforce-rtx-3080vdeokarta-msi-geforce-rtx-3080-ven-ID10KjOz.html",
  "title": "Відеокарта MSI Ventus 3X Plus Geforce RTX 3080\nВідеокарта MSI GeForce RTX 3080 VEN"
}
```
**Семпл #78:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/vdeokarta-gigabyte-geforce-gtx-1080-ti-aorus-11g-b-v-garantya-3-msyats-ID10XVEW.html",
  "title": "Відеокарта GIGABYTE GeForce GTX 1080 Ti AORUS 11G Б/в + Гарантія 3 місяці!"
}
```
**Семпл #79:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/videokarta-1650-ID10TBsk.html",
  "title": "Видеокарта 1650"
}
```
**Семпл #80:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/vdeokarta-radeon-hd5770-gddr5-4800-mgts-IDXzB3A.html",
  "title": "Відеокарта RADEON HD5770 GDDR5 4800 МГц"
}
```
**Семпл #81:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/radeon-rx-480-8-gb-asus-dual-oc-pratsyu-deklka-vdeovihodv-ID10Z15A.html",
  "title": "Radeon RX 480 8 GB ASUS DUAL OC працює декілька відеовиходів"
}
```
**Семпл #82:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/vdeokarta-msi-geforce-gtx-1060-gaming-x-6g-ID10Z0Ra.html",
  "title": "Відеокарта MSI GeForce GTX 1060 Gaming X 6G"
}
```
**Семпл #83:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/videokarta-asus-rt-5700-xt-strix-ID10Z0Yn.html",
  "title": "Видеокарта asus rt 5700 xt strix"
}
```
**Семпл #84:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/vdeokarta-msi-rtx-3050-ventus-2x-8gb-ID10Z0XN.html",
  "title": "Відеокарта MSI RTX 3050 Ventus 2X 8GB"
}
```
**Семпл #85:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/vdeo-karta-gtx-1060-8-gb-ID10Z0Vs.html",
  "title": "Відео карта GTX 1060 8 gb"
}
```
**Семпл #86:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/geforce-8800-gts-512mb-IDZOFL8.html",
  "title": "GeForce 8800 GTS 512мб"
}
```
**Семпл #87:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/vdeokarta-asus-tuf-gaming-gtx-1650-super-oc-ID10Z0QX.html",
  "title": "Відеокарта ASUS TUF Gaming GTX 1650 SUPER OC"
}
```
**Семпл #88:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/vdeokarta-sapphire-radeon-hd-6770-1-gb-IDUon1v.html",
  "title": "Відеокарта Sapphire RADEON HD 6770 1 GB"
}
```
**Семпл #89:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/videokarta-msi-nvidia-geforce-gtx-650ti-2g-gddr5-ID10Z0DO.html",
  "title": "Видеокарта MSI NVIDIA GeForce GTX 650Ti 2G GDDR5"
}
```
**Семпл #90:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/luchshaya-rtx-4090-asus-rog-strix-nvidia-pci-ex-geforce-24gb-ID10PVNZ.html",
  "title": "Лучшая RTX 4090 ASUS ROG Strix NVIDIA PCI-Ex GeForce 24Gb"
}
```
**Семпл #91:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/vdeokarta-gtx-1050-ID10CX1d.html",
  "title": "Відеокарта GTX 1050"
}
```
**Семпл #92:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/evga-geforce-rtx-3080-ti-ftw3-IDZFyMd.html",
  "title": "EVGA GeForce RTX 3080 TI FTW3"
}
```
**Семпл #93:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/msi-gtx-1060-3gb-ID10Z0C9.html",
  "title": "MSI GTX 1060 3Gb"
}
```
**Семпл #94:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/vdeokarta-nvidia-gtx-780-3gb-ID10pdkx.html",
  "title": "Відеокарта Nvidia GTX 780 3Gb"
}
```
**Семпл #95:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/vdeokarta-msi-rx5600xt-gamin-mx-IDVqcPt.html",
  "title": "Відеокарта msi rx5600xt gamin mx"
}
```
**Семпл #96:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/vdeokarta-gigabyte-geforce-rtx-2070-windforce-2x-8192mb-gv-n2070wf2-8gd-ID10Z0uy.html",
  "title": "Відеокарта Gigabyte GeForce RTX 2070 WindForce 2X 8192MB (GV-N2070WF2-8GD)"
}
```
**Семпл #97:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/videokarta-geforce-9600-gt-IDYQvM0.html",
  "title": "Видеокарта  geforce 9600 gt"
}
```
**Семпл #98:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/videokarta-gigabyte-gtx-1660-6gb-oc-ID10Z0jG.html",
  "title": "Видеокарта Gigabyte GTX 1660 6Gb OC"
}
```
**Семпл #99:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/asus-geforce-gtx-1080-rog-strix-8gb-gddr5x-strix-gtx1080-8g-gaming-ID10Z0hh.html",
  "title": "Asus GeForce GTX 1080 ROG Strix 8GB GDDR5X (STRIX-GTX1080-8G-GAMING)"
}
```
**Семпл #100:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/radeon-hd6970-2048mb-gddr5-256bit-s-defektom-IDYnmYA.html",
  "title": "Radeon HD6970 2048MB GDDR5 (256bit) с дефектом"
}
```

#### 🧠 Процесори (CPU) — Відсіяно (Показано 100 з max 100):
**Семпл #1:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/protsesor-intel-xeon-e5-2623-v4-ID10YAlp.html",
  "title": "Процесор Intel Xeon E5-2623 v4"
}
```
**Семпл #2:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/amd-ryzen-5-5500-3-6-ghz-box-am4-ID10Z0gT.html",
  "title": "AMD Ryzen 5 5500 3.6 GHz Box AM4"
}
```
**Семпл #3:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/protsesor-intel-core-ultra-5-225f-box-ID10npRM.html",
  "title": "Процесор INTEL CORE ULTRA 5 225f box"
}
```
**Семпл #4:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/s1151-set-intel-core-i5-7600k-4-2ghz-z-vdeoyadrom-plata-asus-tradein-IDYHjCD.html",
  "title": "s1151 сет Intel Core i5-7600K 4.2GHz з відеоядром +плата ASUS. TradeIN"
}
```
**Семпл #5:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/protsesor-i5-2310-IDYg2Em.html",
  "title": "Процесор i5 2310"
}
```
**Семпл #6:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Продам процесор G4400",
  "item_type": "cpu"
}
```
**Семпл #7:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Процесор AMD Athlon X4 750K (Socket FM2)",
  "item_type": "cpu"
}
```
**Семпл #8:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Intel Core i5-2430M SR04W 3GHz/3M/35W Socket G2 процесор для ноутбука",
  "item_type": "cpu"
}
```
**Семпл #9:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Процесор AMD 4800+ Малайзия и башня охлаждения",
  "item_type": "cpu"
}
```
**Семпл #10:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/amd-ryzen-5-1600-af-12nm-boksoviy-kuler-termopasta-ID10TpLp.html",
  "title": "AMD Ryzen 5 1600 AF (12nm) + боксовий кулер + термопаста"
}
```
**Семпл #11:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/amd-ryzen-5-8400f-4-2-ghz-16-mb-am5-protsessor-ID10Cuea.html",
  "title": "AMD Ryzen 5 8400F 4.2 GHz/16 MB AM5  Процессор"
}
```
**Семпл #12:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "ID-Cooling FX120 ARGB",
  "item_type": "cpu"
}
```
**Семпл #13:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/protsesor-intel-xeon-e5-2680-v4-radator-tdp-160wtr-IDYquhe.html",
  "title": "Процесор Intel Xeon E5-2680 V4 + радіатор TDP 160wtр."
}
```
**Семпл #14:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/protsesor-intel-pentium-g5600f-3-9ghz-8gt-s-4mb-s1151-box-IDT44Hq.html",
  "title": "Процесор Intel Pentium G5600F 3.9GHz/8GT/s/4MB s1151 BOX"
}
```
**Семпл #15:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/protsesor-pentium-g4400-lga-1151-ID10NzE3.html",
  "title": "Процесор Pentium G4400 LGA 1151"
}
```
**Семпл #16:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/protsesor-intel-core-i5-7500-box-IDVUHab.html",
  "title": "Процесор Intel Core i5-7500 box"
}
```
**Семпл #17:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Amd Athlon 3125GE Silver PRO",
  "item_type": "cpu"
}
```
**Семпл #18:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Кулер з процесором AMD Athlon 64 X2 4800+ - ADO4800IAA5DD",
  "item_type": "cpu"
}
```
**Семпл #19:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/protsesor-intel-core-i7-6700-ID10Z3ng.html",
  "title": "Процесор Intel Core i7 6700"
}
```
**Семпл #20:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Радіатор башеного типу для процесора материнської плати ПК",
  "item_type": "cpu"
}
```
**Семпл #21:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/protsessor-intel-celeron-g3930-IDSfxpJ.html",
  "title": "Процессор intel celeron g3930"
}
```
**Семпл #22:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Процесор AMD A8 4500M AM4500DEC44HJ 1.9-2.8GHz/4M/35W Socket FS1r2 Процесор для ноутбука",
  "item_type": "cpu"
}
```
**Семпл #23:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/amd-ryzen-7500f-am5-deepcool-ak400-digital-z-dvoma-kulerami-ID10HfAw.html",
  "title": "AMD  ryzen 7500f  am5 + deepcool ak400 digital з двома кулерами"
}
```
**Семпл #24:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/protsesori-intel-i5-6402p-6500-4-4yadra-rozprodazh-IDUEzXB.html",
  "title": "Процесори Intel  i5-6402P/6500 4/4ядра  РОЗПРОДАЖ!"
}
```
**Семпл #25:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/top-ryzen-5-9600x-zen-5-6-yader-12-potokov-5-4-ggts-IDZTpte.html",
  "title": "‼️Топ  Ryzen 5 9600x (zen 5, 6 ядер 12 потоков 5.4 ггц)"
}
```
**Семпл #26:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/intel-core-i7-8700-3-2-4-6ghz-6-yader-12-potokov-lga1151-ID10Z3jc.html",
  "title": "Intel Core I7 8700, 3.2-4.6ghz, 6 ядер, 12 потоков, LGA1151"
}
```
**Семпл #27:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/komplekt-i7-10700k-16ddr-rx5600xt-ID10Z3hi.html",
  "title": "Комплект i7 10700k 16ddr rx5600xt"
}
```
**Семпл #28:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/prodam-protsesor-intel-core-i7-11700k-3-65-0ghz-16mb-s1200-box-bx8070811700k-ID10VN5A.html",
  "title": "Продам Процесор Intel Core i7-11700K 3.6(5.0)GHz 16MB s1200 Box (BX8070811700K)"
}
```
**Семпл #29:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/protsessor-intel-core-i5-4670-IDWviEv.html",
  "title": "Процессор Intel Core i5-4670"
}
```
**Семпл #30:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/protsessor-intel-core-i7-4770-IDWvixY.html",
  "title": "Процессор Intel Core i7-4770."
}
```
**Семпл #31:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Процесор Intel Core 2 Duo T7100 (LF80537, T7100, 7720A246, SLA4A",
  "item_type": "cpu"
}
```
**Семпл #32:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Процессор intel core pentium gold f5600",
  "item_type": "cpu"
}
```
**Семпл #33:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Процессор Intel Pentium Dual Core E5200 2.50GHz/2M/800MHz",
  "item_type": "cpu"
}
```
**Семпл #34:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/amd-ryzen-7-1700-8-yader-16-potokv-IDZk6W6.html",
  "title": "AMD Ryzen 7 1700 (8 ядер/16 потоків)"
}
```
**Семпл #35:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/protsesor-intel-core-i5-9600k-3-7ghz-8gt-s-9mb-s1151-ID10Z2PZ.html",
  "title": "Процесор Intel Core i5-9600K 3.7GHz/8GT/s/9MB  s1151"
}
```
**Семпл #36:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/ryzen-9-7900x-asrock-b650-pg-lightning-ID10OTU5.html",
  "title": "Ryzen 9 7900X і Asrock B650 PG LIGHTNING"
}
```
**Семпл #37:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/cpu-intel-core-i7-10700kf-8-yader-16-potokov-lga-1200-ID10mkNI.html",
  "title": "CPU Intel Core i7-10700KF 8 ядер/ 16 потоков LGA 1200"
}
```
**Семпл #38:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/intel-core-i9-14900k-lga1700-24-yadra-32-potoka-ID10QnTF.html",
  "title": "Intel Core i9-14900K LGA1700 24 ядра / 32 потока"
}
```
**Семпл #39:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/protsesor-intel-core-i7-2700k-lga1155-ID10Z2EO.html",
  "title": "Процесор Intel Core i7 2700k LGA1155"
}
```
**Семпл #40:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Процесор для ноутбуків Intel i5 2540m SR044",
  "item_type": "cpu"
}
```
**Семпл #41:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/protsesor-intel-i5-2500k-3-3-3-7-ghz-4-yadra-4-potoka-lga-1155-IDSimYD.html",
  "title": "Процесор Intel i5-2500k | 3.3 - 3.7 GHz | 4 Ядра - 4 Потока | LGA 1155"
}
```
**Семпл #42:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Процесор AMD Athlon 64",
  "item_type": "cpu"
}
```
**Семпл #43:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Продам Процесор AMD FX-8320 3.50GHz/8M/2200MH AM3+",
  "item_type": "cpu"
}
```
**Семпл #44:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/komplekt-i5-7600k-asus-h110m-k-radiator-ID10Z2lI.html",
  "title": "Комплект I5 7600K + ASUS H110M-K + Радиатор"
}
```
**Семпл #45:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Intel Core i3-3210, сокет LGA 1155",
  "item_type": "cpu"
}
```
**Семпл #46:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Процесор",
  "item_type": "cpu"
}
```
**Семпл #47:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/protsesor-amd-a4-6300-socket-fm2-ID10Z2fg.html",
  "title": "Процесор AMD A4-6300 (Socket FM2+)"
}
```
**Семпл #48:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/protsessor-intel-i9-9900kf-ID10Z2bQ.html",
  "title": "Процессор Intel i9-9900KF"
}
```
**Семпл #49:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/igrovoy-komplekt-i7-11700f-msi-z490-tomahawk-be-quiet-ID10TiKR.html",
  "title": "Игровой Комплект - i7-11700f/MSI Z490 TOMAHAWK/be quiet!"
}
```
**Семпл #50:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/protsesor-amd-ryzen-9-7950x3d-am5-ID10WQ3Y.html",
  "title": "Процесор AMD Ryzen 9 7950X3D (AM5)"
}
```
**Семпл #51:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/intel-xeon-e5-2699a-v4-ID10Ieb2.html",
  "title": "Intel Xeon e5 2699A v4"
}
```
**Семпл #52:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/protsesor-intel-xeon-e5-2623-v4-ID10YAlp.html",
  "title": "Процесор Intel Xeon E5-2623 v4"
}
```
**Семпл #53:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/protsesor-amd-a10-5800-socket-fm2-ID10Z1UG.html",
  "title": "Процесор AMD A10-5800 (Socket FM2)"
}
```
**Семпл #54:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/protsesor-amd-athlon-64-x2-6000-125w-2-yadra-3-0-ghz-am2-tray-adx6000iaa6cz-b-u-ID10Z1Rl.html",
  "title": "Процесор AMD Athlon 64 X2 6000 125W 2 Ядра, 3.0 GHz, AM2 , Tray ( ADX6000IAA6CZ ) Б/У"
}
```
**Семпл #55:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/top-ryzen-5-9600x-zen-5-6-yader-12-potokov-5-4-ggts-IDZTpte.html",
  "title": "‼️Топ  Ryzen 5 9600x (zen 5, 6 ядер 12 потоков 5.4 ггц)"
}
```
**Семпл #56:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/cpu-pentium-g4400t-socket-lga1151-3m-cache-3-30-ghz-tdp-35w-IDRW0PW.html",
  "title": "CPU Pentium G4400T Socket LGA1151  (3M Cache, 3.30 GHz) TDP 35W"
}
```
**Семпл #57:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Кулер для процесора intel 775",
  "item_type": "cpu"
}
```
**Семпл #58:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Процесор intel pentium 5300 dual-core",
  "item_type": "cpu"
}
```
**Семпл #59:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/protsessor-amd-a4-3300-2-5ghz-1mb-4000mhz-ad3300ojgxbox-sfm1-box-IDX7gR7.html",
  "title": "Процессор AMD A4-3300 2.5GHz/1MB/4000MHz (AD3300OJGXBOX) SFM1 BOX"
}
```
**Семпл #60:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Продам процесор б/у,самовивіз",
  "item_type": "cpu"
}
```
**Семпл #61:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/protsessor-intel-core-i5-9400f-6-yader-2-9ghz-4-1ghz-8gt-s-9mb-s1151-ID10Z0YD.html",
  "title": "Процессор Intel Core i5-9400F 6 ядер/2.9GHz...4.1GHz/8GT/s/ 9MB s1151"
}
```
**Семпл #62:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/i7-13700f-16-24-30-mb-opis-ID10Tpzz.html",
  "title": "I7 13700F 16/24 30 mb (опис)"
}
```
**Семпл #63:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/intel-core-i3-9100f-4-core-4-2ghz-lga1151-ID10PozU.html",
  "title": "Intel Core i3-9100F 4-Core 4.2GHz LGA1151"
}
```
**Семпл #64:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/protsesor-amd-ryzen-9-9950x3d-am5-noviy-IDZRReu.html",
  "title": "Процесор AMD Ryzen 9 9950X3D AM5 новий"
}
```
**Семпл #65:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/protsessor-intel-pentium-g4400-sr2dc-3-30-gnz-IDW27d8.html",
  "title": "Процессор  INTEL PENTIUM G4400 SR2DC 3.30 GNZ"
}
```
**Семпл #66:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/noviy-protsesor-amd-ryzen-5-7600x-4-7ghz-32mb-sam5-box-IDZrYEr.html",
  "title": "НОВИЙ Процесор AMD Ryzen 5 7600X 4.7GHz/32MB sAM5 BOX"
}
```
**Семпл #67:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/protsesor-ryzen-5-7500f-ID10Z0IT.html",
  "title": "Процесор Ryzen 5 7500f"
}
```
**Семпл #68:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/protsessor-intel-core-i7-7700-4-yadra-8-potokov-4-2-ggts-ideal-garantiya-1151-soket-7-e-pokolenie-intel-IDZbGEX.html",
  "title": "Процессор intel core i7 7700 4 ядра 8 потоков 4.2 Ггц идеал гарантия 1151 сокет 7-е поколение интел"
}
```
**Семпл #69:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/protsessor-intel-celeron-g3900-ntelovskiy-boksoviy-kuler-ID10eF28.html",
  "title": "Процессор intel celeron g3900 + інтеловський боксовий кулер"
}
```
**Семпл #70:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/intel-core-i7-9700k-socket-1151-ID10Z0rL.html",
  "title": "Intel Core i7-9700K (Socket 1151)"
}
```
**Семпл #71:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/protsessor-core-i7-4790k-ID10Z0pd.html",
  "title": "Процессор Core i7 4790K"
}
```
**Семпл #72:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/protsesor-amd-ryzen-7-9800x3d-100-000001084-nov-zapakovan-ID10T3ir.html",
  "title": "Процесор AMD Ryzen 7 9800X3D (100-000001084) нові запаковані"
}
```
**Семпл #73:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/amd-ryzen-5-5500-3-6-ghz-box-am4-ID10Z0gT.html",
  "title": "AMD Ryzen 5 5500 3.6 GHz Box AM4"
}
```
**Семпл #74:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/protsesor-intel-xeon-e5-2690-v3-IDTm6I6.html",
  "title": "Процесор intel Xeon e5-2690 v3"
}
```
**Семпл #75:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/komplekt-ryzen-5-5500x3d-32gb-ddr4-3400mhz-groviy-monstr-na-am4-ID10e2ny.html",
  "title": "Комплект Ryzen 5 5500X3D +32gb ddr4 3400MHz ігровий монстр на ам4"
}
```
**Семпл #76:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/rozstrochka-mono-na-3-msyats-intel-core-i5-14600kf-asus-tuf-b760m-plus-id-cooling-se-206xt-topoviy-suchasniy-groviy-komplekt-ID10Xj6E.html",
  "title": "РОЗСТРОЧКА МОНО НА 3 МІСЯЦІ! Intel Core i5 14600KF, Asus TUF B760M-Plus, ID-Cooling SE-206XT топовий сучасний ігровий комплект"
}
```
**Семпл #77:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/amd-ryzen-9-7900x-ID10DKTp.html",
  "title": "AMD Ryzen 9 7900X"
}
```
**Семпл #78:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/protsessor-intel-celeron-e3400-2-60-ghz-1m-800-slgtz-malay-IDXDgYM.html",
  "title": "Процессор Intel Celeron E3400 2.60 GHz/1M/800 (SLGTZ MALAY"
}
```
**Семпл #79:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/protsessor-intel-pentium-g3220-3-00ghz-socket-1150-IDSwmbl.html",
  "title": "Процессор Intel Pentium G3220 3.00GHz socket 1150"
}
```
**Семпл #80:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Продам процесор AMD Athlon X4 (AM4) із комплектним кулером.",
  "item_type": "cpu"
}
```
**Семпл #81:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/intel-celeron-g530-s1155-i3-i5-pentium-ID10NwP5.html",
  "title": "INTEL CELERON® G530 S1155 i3 i5 Pentium"
}
```
**Семпл #82:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/intel-core-i5-10400f-2-9ghz-12mb-s1200-box-ID10YZpF.html",
  "title": "Intel Core i5-10400F 2.9GHz/12MB s1200 BOX"
}
```
**Семпл #83:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/amd-athlon-ii-x2-260-3-2-ggts-socket-am3-am2-adx2600ck23gm-ID10YZbN.html",
  "title": "AMD Athlon II X2 260 3.2 ГГц Socket AM3/AM2+ (ADX2600CK23GM)"
}
```
**Семпл #84:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/intel-core-i3-2120-3-30ghz-socket-1155-IDVqaYm.html",
  "title": "Intel Core i3-2120 3.30GHz, Socket 1155"
}
```
**Семпл #85:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/protsesor-r5-8400f-ID10YYVT.html",
  "title": "Процесор r5 8400f"
}
```
**Семпл #86:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/protsesor-amd-ryzen-5-1600-x-6-yader-12-potokv-ID101sHp.html",
  "title": "Процесор AMD Ryzen 5 1600 x 6 ядер 12 потоків"
}
```
**Семпл #87:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Процесори Amd повністю робочі",
  "item_type": "cpu"
}
```
**Семпл #88:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/komplekt-intel-core-i9-11900kf-asus-prime-z590-a-s1200-ID10yTJh.html",
  "title": "Комплект Intel Core i9 11900KF+ Asus Prime Z590 -A  s1200"
}
```
**Семпл #89:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/protsesor-intel-core-i7-6700k-4-00ghz-s1151-sr2l0-i7-6700k-IDZvF47.html",
  "title": "Процесор Intel Core i7-6700K 4.00GHz s1151 (SR2L0) / i7 6700K"
}
```
**Семпл #90:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/komplekt-i7-10700k-16ddr-rx5600xt-ID10Z3hi.html",
  "title": "Комплект i7 10700k 16ddr rx5600xt"
}
```
**Семпл #91:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/intel-core-i9-13900k-lga-1700-processor-ID10Nw3N.html",
  "title": "Intel Core i9-13900K LGA 1700 Processor"
}
```
**Семпл #92:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/amd-ryzen-9-3900x-box-ID10VI2q.html",
  "title": "AMD Ryzen 9 3900x box"
}
```
**Семпл #93:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Процессор Core 2 Quad 09300, 2.50 hz , L 333/ 05A",
  "item_type": "cpu"
}
```
**Семпл #94:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Процессор Intel Core",
  "item_type": "cpu"
}
```
**Семпл #95:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/prodam-protsessor-ryzen-5-3600-3-6hz-4-2hz-opisanie-ID10YYsE.html",
  "title": "Продам процессор ryzen 5 3600 3.6hz\\4.2hz ОПИСАНИЕ!"
}
```
**Семпл #96:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/protsesor-intel-core-ii5-3330s-i-krepezh-k-nemu-IDQEj2x.html",
  "title": "Процесор Intel Core ii5-3330S и крепеж к нему"
}
```
**Семпл #97:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Процесор та оперативна память",
  "item_type": "cpu"
}
```
**Семпл #98:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/intel-core-i3-2120-IDYr8yD.html",
  "title": "Intel Core i3-2120"
}
```
**Семпл #99:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/protsesor-amd-ryzen-5-2400g-z-kulerom-ID10qgSW.html",
  "title": "Процесор AMD Ryzen 5 2400G з кулером"
}
```
**Семпл #100:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/komplekt-do-pk-i7-6700-16-gb-ddr4-mat-plata-kuller-ID10YXVq.html",
  "title": "Комплект до пк, i7 6700, 16 gb ddr4, мат. плата, куллер"
}
```

#### 🔌 Материнські плати (Motherboard) — Відсіяно (Показано 100 з max 100):
**Семпл #1:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/materinskaya-plata-asus-prime-z370-p-1151v2-ID10Nut3.html",
  "title": "материнская плата asus prime z370-p 1151v2"
}
```
**Семпл #2:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/komplekt-qiyida-x99-k9s-xeon-e5-2699-v3-18-36-lga2011-3-ID10YQfY.html",
  "title": "Комплект QIYIDA X99 K9S + Xeon E5-2699 v3 18/36 LGA2011-3"
}
```
**Семпл #3:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/komplekt-intel-core-i9-10850k-asus-tuf-gaming-z490-plus-wi-fi-ID10O0OT.html",
  "title": "Комплект Intel Core i9 10850K + Asus TUF GAMING Z490-PLUS (WI-FI)"
}
```
**Семпл #4:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/materinski-plati-b85-ID10dHVa.html",
  "title": "Материнськи плати B85"
}
```
**Семпл #5:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/materinskaya-plata-asus-a68hm-k-prots-a8-7680-3-5-ghz-fm2-4gb-ddr3-IDXRSQF.html",
  "title": "Материнская плата ASUS A68HM-K+проц A8-7680 3.5 GHz, FM2+,  4Gb ddr3"
}
```
**Семпл #6:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/komplekt-x99-qiyida-x99-e5-a99-lga-2011-3-intel-xeon-e5-2697v3-3-6-ghz-32-gb-216-gb-pamyat-kuler-ID10Z3Gr.html",
  "title": "Комплект X99 / Qiyida X99 E5 A99 LGA 2011-3 / Intel Xeon E5-2697v3 3.6 GHz / 32 ГБ (2*16 ГБ) памяті /  Кулер"
}
```
**Семпл #7:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/materinska-plata-asus-h87-pro-intel-core-i5-4460-z-kulerom-zalman-cnps10x-ram-ddr3-12-gb-ID10Z3y4.html",
  "title": "Материнська плата Asus H87-Pro + Intel Core i5-4460 з кулером Zalman CNPS10X + RAM DDR3 12 Гб"
}
```
**Семпл #8:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Комплектуючі до пк",
  "item_type": "motherboard"
}
```
**Семпл #9:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "продам материнську плату з процесором",
  "item_type": "motherboard"
}
```
**Семпл #10:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/asus-rog-strix-b360-i-gaming-motherboard-b360-lga1151-mini-itx-ddr4-max-32gb-m-2-pci-e3-0-hdmi-for-intel-8th-9th-gen-core-cpu-ID10Z386.html",
  "title": "ASUS ROG STRIX B360-I GAMING Motherboard B360 LGA1151 Mini ITX DDR4 Max 32GB M.2 PCI-E3.0 HDMI For Intel 8th 9th Gen Core CPU"
}
```
**Семпл #11:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Продам плату бу робочу",
  "item_type": "motherboard"
}
```
**Семпл #12:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Main MS65860-ZC01-01",
  "item_type": "motherboard"
}
```
**Семпл #13:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Материнка Abit Ab9 Pro",
  "item_type": "motherboard"
}
```
**Семпл #14:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/prodam-platu-asus-tuf-z790-pro-wifi-intel-14700k-ID10YBxl.html",
  "title": "Продам плату Asus TUF Z790-PRO WIFI + Intel 14700K"
}
```
**Семпл #15:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/msi-b450m-a-pro-max-oholodzhennya-deepcool-gammaxx-300-ID10XOqA.html",
  "title": "Msi b450m-a pro max + охолодження Deepcool Gammaxx 300"
}
```
**Семпл #16:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/komplekt-gigabyte-ga-a88xm-d3h-amd-a8-7600-ID10R7dP.html",
  "title": "Комплект Gigabyte GA-A88XM-D3H + AMD A8-7600"
}
```
**Семпл #17:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Материнська плата Asus m4a78 SE",
  "item_type": "motherboard"
}
```
**Семпл #18:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/materinskaya-plata-z270-cpui5-6500-16gb-ddr4-IDVW4f3.html",
  "title": "Материнская плата Z270-CPU=I5 6500/16GB/DDR4"
}
```
**Семпл #19:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "s1155 материнська плата ASUS",
  "item_type": "motherboard"
}
```
**Семпл #20:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "HP 635 материнская плата",
  "item_type": "motherboard"
}
```
**Семпл #21:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "ASUS R101 материнская плата",
  "item_type": "motherboard"
}
```
**Семпл #22:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/materinska-plata-gigabyte-b550i-aorus-pro-ax-sam4-amd-b550-IDZEgJt.html",
  "title": "Материнська плата Gigabyte B550I AORUS PRO AX (sAM4, AMD B550)"
}
```
**Семпл #23:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Материнская плата Asrock extreme 4 1150",
  "item_type": "motherboard"
}
```
**Семпл #24:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/asrock-p67-extreme6-asus-p8z77-v-le-nerabochie-IDYeUSN.html",
  "title": "ASRock P67 Extreme6, Asus P8Z77-V LE нерабочие."
}
```
**Семпл #25:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Продам плату GSM навигатор камера",
  "item_type": "motherboard"
}
```
**Семпл #26:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Материнська плата Gigabyte GA-M61PM-S2 ( Socket AM2+,PCI-Ex16",
  "item_type": "motherboard"
}
```
**Семпл #27:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Потужный недорогие комплекты i5 + материнская плата 1150 можно с памятью ddr3",
  "item_type": "motherboard"
}
```
**Семпл #28:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/materinska-plata-asus-p8b75-m-lx-lga1155-ID10UlnM.html",
  "title": "Материнська плата Asus p8b75-M lx lga1155"
}
```
**Семпл #29:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/materinskaya-plata-asus-prime-x670e-pro-wifi-ID10BURq.html",
  "title": "Материнская плата Asus Prime X670E-PRO WiFi"
}
```
**Семпл #30:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Лот 5 ретро-процесорів Intel (775/478 сокет) + плата Pyronix",
  "item_type": "motherboard"
}
```
**Семпл #31:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Материнская плата Asus Prime Z390A",
  "item_type": "motherboard"
}
```
**Семпл #32:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/materinskaya-plata-asus-tuf-gaming-b760m-plus-2-s1700-ddr5-na-garantii-ot-brain-ID10qlSn.html",
  "title": "Материнская плата ASUS TUF GAMING B760M PLUS-2 (s1700) DDR5, на гарантии от Brain"
}
```
**Семпл #33:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/materinska-plata-asus-rog-strix-x870-a-gaming-wifi-ID10qlP7.html",
  "title": "Материнська плата ASUS ROG STRIX X870-A GAMING WIFI"
}
```
**Семпл #34:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/materinska-plata-msi-mag-z790-tomahawk-max-wifi-ddr5-IDXeb1v.html",
  "title": "Материнська плата MSI MAG Z790 TOMAHAWK MAX WIFI DDR5"
}
```
**Семпл #35:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Материнська плата MSI G41m4 +Cpu сокет775",
  "item_type": "motherboard"
}
```
**Семпл #36:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Материнські плати s1151 v1  hp",
  "item_type": "motherboard"
}
```
**Семпл #37:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Материнська плата Supermicro X10DRU-I+",
  "item_type": "motherboard"
}
```
**Семпл #38:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/materinska-plata-asus-a68hm-k-protsesor-amd-a4-6300-socket-fm-operativna-pamyat-kingston-hyperx-blu-ddr3-2gb-1600-mhz-2-sht-ID10Z24r.html",
  "title": "Материнська плата ASUS A68HM-K + процесор AMD A4-6300 (Socket FM) +   Оперативна память Kingston HyperX Blu DDR3 2GB 1600 MHz - 2 шт"
}
```
**Семпл #39:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/materinska-plata-asus-tuf-gaming-b450m-plus-ID10Z1X8.html",
  "title": "Материнська плата ASUS TUF GAMING B450M-PLUS"
}
```
**Семпл #40:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/materinska-plata-athermiter-x79-komplekt-ID10Sa7e.html",
  "title": "материнська плата athermiter x79 комплект"
}
```
**Семпл #41:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/materinska-plata-biostar-tb360-lga1151-intel-g4900-ID10MqY7.html",
  "title": "Материнська плата Biostar TB360 LGA1151 + Intel G4900"
}
```
**Семпл #42:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/komplekt-asus-tuf-z390-plus-gaming-wi-fi-i5-9600kf-bashnya-aardwolf-performa-10x-ID10U4eL.html",
  "title": "Комплект Asus TUF Z390-PLUS GAMING Wi-Fi + i5-9600KF + башня Aardwolf PERFORMA 10X"
}
```
**Семпл #43:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Комплектуючі до компʼютера",
  "item_type": "motherboard"
}
```
**Семпл #44:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/materinskaya-plata-gigabyte-ga-m68mt-d3-ID10ddiy.html",
  "title": "Материнская плата Gigabyte GA-M68MT-D3"
}
```
**Семпл #45:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/top-materinskaya-plata-asrock-b365-pro-kuller-deep-cool-IDQX0hg.html",
  "title": "Топ материнская плата   asrock  -b365 pro + куллер deep cool"
}
```
**Семпл #46:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/materinska-plata-gigabyte-z790-aorus-pro-x-wifi7-lga1700-ID10Ojw7.html",
  "title": "Материнська плата - Gigabyte Z790 AORUS PRO X WIFI7 (LGA1700)"
}
```
**Семпл #47:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/materinska-plata-asrock-fm2a75-pro4-m-protsesor-amd-a10-5800-socket-fm2-operativna-pamyat-kingston-hyperx-fury-ddr3-8gb-2h4-1600-mhz-ID10Z1HX.html",
  "title": "Материнська плата ASRock FM2A75 Pro4-M + процесор AMD A10-5800 (Socket FM2)+Оперативна память Kingston HyperX Fury DDR3 8GB (2х4) 1600 MHz"
}
```
**Семпл #48:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "комплект к  ПК плата, озу, процессор, задняя планка",
  "item_type": "motherboard"
}
```
**Семпл #49:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Продам готову збірку бюджетного пк.",
  "item_type": "motherboard"
}
```
**Семпл #50:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/materinska-plata-gigabyte-ga-h61m-ds2-rev-4-0-socket-lga-1155-ddr3-ID10Z1tU.html",
  "title": "Материнська плата Gigabyte GA-H61M-DS2 (Rev 4.0) Socket LGA 1155 DDR3"
}
```
**Семпл #51:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/materinskaya-plata-msi-h61m-e23-intel-xeon-e3-1220-v2-3-10-ghz-ID10Z1yj.html",
  "title": "материнская плата MSI H61M-E23 + Intel Xeon E3-1220 v2 (3.10 GHz)"
}
```
**Семпл #52:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Мать ,проц,опера в хорошем состоянии",
  "item_type": "motherboard"
}
```
**Семпл #53:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/ryzen-5-7500f-ddr5-32gb-6000mhz-msi-a620m-b-ID10gP6X.html",
  "title": "Ryzen 5 7500f ddr5 32gb 6000mhz msi a620m b"
}
```
**Семпл #54:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/komplekt-gigabyte-a320m-ryzen-3-1200-8gb-ddr4-ID10UIzd.html",
  "title": "Комплект: Gigabyte A320M + Ryzen 3 1200 + 8gb ddr4"
}
```
**Семпл #55:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/asus-sabertooth-z170-mark1-ID10Sz22.html",
  "title": "Asus Sabertooth Z170 Mark1"
}
```
**Семпл #56:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "материнская плата s775 Intel d101ggc + 2х ядерный процессор",
  "item_type": "motherboard"
}
```
**Семпл #57:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/asrock-a620m-pro-rs-poshkodzheniy-soket-IDVW2cU.html",
  "title": "ASROCK A620M Pro RS пошкоджений сокет"
}
```
**Семпл #58:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Материнська плата комплект",
  "item_type": "motherboard"
}
```
**Семпл #59:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Материнська плата Asus P8H61-MX s1155",
  "item_type": "motherboard"
}
```
**Семпл #60:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Двух процессорная серверная материнская плата HP proliant ml 350 g9 2011v3 сокет сервер",
  "item_type": "motherboard"
}
```
**Семпл #61:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Нові м.п Dell 7010 (Core i5 i7+E3-12**v1+v2\\4xDDR3 32GB\\SSD NVMe boot)",
  "item_type": "motherboard"
}
```
**Семпл #62:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/komplekt-intel-core-i5-9400f-asus-prime-h310m-k-r2-0-ID10XJGC.html",
  "title": "Комплект Intel Core i5-9400F + ASUS PRIME H310M-K R2.0"
}
```
**Семпл #63:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Комплект ретро заліза - материнка+проц+озу socket462",
  "item_type": "motherboard"
}
```
**Семпл #64:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Продам материнскую плату Gigabyte MZ33-AR1 SP5 для AMD EPYC 9004/9005",
  "item_type": "motherboard"
}
```
**Семпл #65:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Материнская плата бренд Hubsan модель ZINO версия PRO (Y).",
  "item_type": "motherboard"
}
```
**Семпл #66:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Платы, топы, дисплеи на различные Macbook, Imac от 2010 до 2024",
  "item_type": "motherboard"
}
```
**Семпл #67:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/opt-materinskie-platy-1155-1150-cpu-i3-i5-ddr3-4gb-8gb-ID101atg.html",
  "title": "Опт. Материнские платы 1155, 1150 CPU i3, i5.  Ddr3 4gb 8gb."
}
```
**Семпл #68:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/materinska-plata-asus-rog-crosshair-x870e-hero-btf-am5-amd-ryzen-nova-apex-aorus-IDYvNro.html",
  "title": "Материнська плата ASUS ROG CROSSHAIR X870E Hero BTF AM5 amd ryzen Нова apex aorus"
}
```
**Семпл #69:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "2 плати до  пральної машинки indesit E2SC2150",
  "item_type": "motherboard"
}
```
**Семпл #70:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/materinska-plata-asus-prime-b550-plus-ID10Z0kT.html",
  "title": "Материнська плата Asus PRIME B550-PLUS"
}
```
**Семпл #71:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Материнська плата Sony PCG-71311M",
  "item_type": "motherboard"
}
```
**Семпл #72:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/materinska-plata-gigabyte-ga-m68mt-s2p-am3-ddr3-cpu-phenom-4x-yadra-IDZ64q3.html",
  "title": "Материнська плата Gigabyte GA-M68MT-S2P AM3 DDR3 + CPU Phenom 4X ядра"
}
```
**Семпл #73:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/komplekt-gigabyte-a520m-ds3h-ryzen-5-3600-16gb-ddr4-3200mhz-ID10ejdK.html",
  "title": "Комплект Gigabyte A520M DS3H + Ryzen 5 3600 + 16gb DDR4 3200mhz"
}
```
**Семпл #74:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Материнская плата gigabyte Ga-m61pme-s2p с процессором AMD",
  "item_type": "motherboard"
}
```
**Семпл #75:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Комплектующие   для компьютера",
  "item_type": "motherboard"
}
```
**Семпл #76:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/komplekt-x99-xd3-intel-xeon-e5-2698b-v3-do-3-4-ghz-32gb-4x8gb-16-yader-32-potoki-ddr3-1866-ecc-reg-quad-channel-tpm-2-0-secure-boot-ID10WCch.html",
  "title": "Комплект X99-XD3 + Intel Xeon E5-2698B v3 до 3.4 GHz + 32GB (4x8GB), 16 ядер/32 потоки, DDR3 1866 ECC Reg quad channel, TPM 2.0, Secure Boot"
}
```
**Семпл #77:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/komplekt-materinska-plata-asus-p5qc-z-protsesorom-intel-core-2-quad-q9400-ID10YZKk.html",
  "title": "комплект: материнська плата ASUS P5QC з процесором Intel Core 2 Quad Q9400."
}
```
**Семпл #78:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/materinska-plata-asus-tug-gaming-a620m-plus-wifi-ID10YZGF.html",
  "title": "Материнська плата ASUS TUG GAMING A620M PLUS WIFI"
}
```
**Семпл #79:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/materinka-asus-z68-virtu-ID10YI1z.html",
  "title": "Материнка Asus z68 virtu"
}
```
**Семпл #80:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/komplekt-am5-platforma-ryzen-5-7500f-gigabyte-b650-kingston-fury-16-gb-ddr5-ID10Qh4w.html",
  "title": "Комплект АМ5 платформа. Ryzen 5 7500F, Gigabyte B650, kingston Fury 16 gb ddr5"
}
```
**Семпл #81:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Saturn ST LED32HD600U на запчасти",
  "item_type": "motherboard"
}
```
**Семпл #82:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/x99-xeon-e5-2650v4-16gb-ddr4-ecc-huananzhi-2682v4-2667v4-ID10YZ8p.html",
  "title": "X99  xeon e5 2650v4 16Gb ddr4 ecc huananzhi 2682v4 2667v4"
}
```
**Семпл #83:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/materinska-plata-athermiter-x79-komplekt-ID10Sa7e.html",
  "title": "материнська плата athermiter x79 комплект"
}
```
**Семпл #84:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Материнская плата main Elenberg 40df4530 HK.T.RT2936P638",
  "item_type": "motherboard"
}
```
**Семпл #85:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/materinska-plata-asus-prime-a320m-k-ne-rabochaya-ID10YZ28.html",
  "title": "Материнська плата ASUS PRIME A320M-K не рабочая"
}
```
**Семпл #86:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/komplekt-am3-am2-asrock-n68c-s-ucc-athlon-ii-x2-250-3-0-ggts-2-gb-ozu-kuler-ID10YYV4.html",
  "title": "Комплект AM3 / AM2+: ASRock N68C-S UCC + Athlon II X2 250 (3.0 ГГц) + 2 ГБ ОЗУ + кулер"
}
```
**Семпл #87:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/msi-mag-pano-m100r-pz-b650m-project-zero-IDZtZ9g.html",
  "title": "MSI MAG PANO M100R PZ + B650M Project Zero"
}
```
**Семпл #88:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/materinskaya-plata-asrock-a320m-socket-am4-ID10Uegy.html",
  "title": "Материнская плата ASRock A320M socket AM4"
}
```
**Семпл #89:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Материнська плата ASUS P8H61-MLE/USB3 + процесор + оперативка",
  "item_type": "motherboard"
}
```
**Семпл #90:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/prodam-materinskuyu-platu-asus-m4n68t-m-s-protsessorom-amd-athlon-IDUOWFV.html",
  "title": "Продам материнскую плату ASUS M4N68T-M с процессором AMD Athlon"
}
```
**Семпл #91:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/komplekt-micro-atx-h81-s1150-i3-4160-4gb-hdd-500gb-oholodzhennya-blok-zhivlennya-ID10VP1c.html",
  "title": "Комплект: Micro-ATX H81 s1150/i3 4160/4Gb/HDD 500Gb/охолодження/блок живлення"
}
```
**Семпл #92:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/komplekt-materinskaya-plata-protsessor-xeon-e3-1230-v6-4-8-yadra-i7-7700-16-gb-ddr-4-ID10TMlj.html",
  "title": "Комплект материнская плата + процессор xeon e3 1230 v6 4/8 ядра (i7 7700) + 16 gb ddr 4"
}
```
**Семпл #93:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "NM-C362, не робоча, на відновлення або запчастини",
  "item_type": "motherboard"
}
```
**Семпл #94:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/mat-plata-asrock-h81-pro-btc-r2-0-IDXlFqd.html",
  "title": "Мат. плата asrock h81 pro btc r2.0"
}
```
**Семпл #95:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "материнська плата ECS P965T-A REV 1.0",
  "item_type": "motherboard"
}
```
**Семпл #96:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/plata-asus-pbz77-v-lk-5-3570k-16-ozu-ID10ILeI.html",
  "title": "плата asus pbz77-v lk + і5 3570к+ 16 озу"
}
```
**Семпл #97:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Материнская плата BIOSTAR GeForce 6100-M7",
  "item_type": "motherboard"
}
```
**Семпл #98:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/materinskaya-plata-asus-prime-z370-p-1151v2-ID10Nut3.html",
  "title": "материнская плата asus prime z370-p 1151v2"
}
```
**Семпл #99:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/komplekt-pk-materinska-plata-dell-socket-1156-i3-cpu-530-8-gb-ddr3-oholodzhennya-ID10YY5B.html",
  "title": "Комплект ПК материнська плата Dell socket 1156 + i3 CPU 530 + 8 gb ddr3 + охолодження"
}
```
**Семпл #100:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Материнська плата для ноутбука Lenovo z50-70",
  "item_type": "motherboard"
}
```

#### ⚡ Блоки живлення (PSU) — Відсіяно (Показано 100 з max 100):
**Семпл #1:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/thermaltake-gt-snow-850w-gold-modulniy-blok-zhivlennya-ID10j294.html",
  "title": "Thermaltake GT SNOW 850W Gold | Модульний блок живлення"
}
```
**Семпл #2:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/kompyuternyy-blok-pitaniya-450w-550w-650w-750w-850w-IDUqtPm.html",
  "title": "Компютерный блок питания 450w 550w 650w 750w 850w"
}
```
**Семпл #3:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/thermaltake-smart-bm3-650w-na-plomb-80-bronze-ID10jtzp.html",
  "title": "Thermaltake Smart BM3 650W | На пломбі, 80+ Bronze"
}
```
**Семпл #4:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Блок питания Hipro HP-A2007F3\nДобавлено",
  "item_type": "psu"
}
```
**Семпл #5:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "БП Chieftec CTG-400-80P 6 пін + корпус  Winga",
  "item_type": "psu"
}
```
**Семпл #6:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Блоки живлення  SFX",
  "item_type": "psu"
}
```
**Семпл #7:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Блок питания Evga",
  "item_type": "psu"
}
```
**Семпл #8:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/premum-blok-zhivlennya-750w-be-quiet-straight-power-11-gold-trade-in-ID10FBSt.html",
  "title": "Преміум блок живлення 750W be quiet! STRAIGHT POWER 11 GOLD. Trade-in"
}
```
**Семпл #9:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Новий БЖ Gigabyte P850GM 80 Plus GOLD",
  "item_type": "psu"
}
```
**Семпл #10:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/blok-pitaniya-cooler-master-850w-rs-850-emba-IDXb8S6.html",
  "title": "Блок питания Cooler Master 850W (RS-850-EMBA)"
}
```
**Семпл #11:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Блок живлення...",
  "item_type": "psu"
}
```
**Семпл #12:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Блок живлення Segotep GP1350G",
  "item_type": "psu"
}
```
**Семпл #13:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/modulniy-blok-zhivlennya-be-quiet-system-power-9-600w-cm-ID10CsUC.html",
  "title": "Модульний! Блок живлення be quiet! System Power 9 600W CM"
}
```
**Семпл #14:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/prodam-blok-zhivlennya-chieftec-core-700w-gold-bbs-700s-chek-garantya-do-02-2027-ID10Yyt7.html",
  "title": "Продам блок живлення Chieftec Core 700W Gold (BBS-700S) + чек гарантія до 02.2027"
}
```
**Семпл #15:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/blok-pitaniya-seasonic-ss-1250xm-1250vt-ID10SXRS.html",
  "title": "Блок питания Seasonic SS-1250XM 1250Вт"
}
```
**Семпл #16:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/blok-pitaniya-chieftec-850w-ID10je7Q.html",
  "title": "Блок питания chieftec 850w"
}
```
**Семпл #17:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Блок живлення ПК, CaseCom 400 Вт, ATX, блок питания",
  "item_type": "psu"
}
```
**Семпл #18:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Блок живлення серверний HP 2250W",
  "item_type": "psu"
}
```
**Семпл #19:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Блок питания 5 В 1 Ампер, D-Link AMS47-0501000FV для роутера",
  "item_type": "psu"
}
```
**Семпл #20:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Блок живлення ПК, FSP 450 Вт, ATX, блок питания",
  "item_type": "psu"
}
```
**Семпл #21:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Блок живлення серверний Emerson 1975w",
  "item_type": "psu"
}
```
**Семпл #22:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Блок живлення ПК, Vinga 500 Вт, ATX, чорний, блок питания",
  "item_type": "psu"
}
```
**Семпл #23:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/yaksniy-blok-zhivlennya-750w-seasonic-gold-ssp-750rt-trade-in-ID10hZnI.html",
  "title": "якісний блок живлення 750W Seasonic GOLD (SSP-750RT). Trade-in"
}
```
**Семпл #24:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Блоки Живлення умовно працюючий/під відновлення/на запчастини",
  "item_type": "psu"
}
```
**Семпл #25:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/blok-zhivlennya-thermaltake-berlin-750w-ID10YlER.html",
  "title": "Блок живлення thermaltake Berlin 750w"
}
```
**Семпл #26:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Блок питания компьютера с сетевым кабелем",
  "item_type": "psu"
}
```
**Семпл #27:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Мережевий шнур Сетевой Шнур питания для ноутбука Микки Маус ОПТ,Гурт",
  "item_type": "psu"
}
```
**Семпл #28:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Кабеля  модульного БП  Chieftec A135. Be Quiet и нерабочие БП Chieftec",
  "item_type": "psu"
}
```
**Семпл #29:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/blok-pitaniya-igrovoy-hydro-g-pro-1000w-1kvt-na-garantii-80-gold-IDZQLFx.html",
  "title": "Блок питания игровой Hydro G Pro 1000w, 1квт, на гарантии 80+ gold"
}
```
**Семпл #30:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Блок живлення CHIEFTEC 500 Вт 14см вент.",
  "item_type": "psu"
}
```
**Семпл #31:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/blok-pitaniya-aerocool-vx-550-IDZE7lH.html",
  "title": "Блок питания  Aerocool vx- 550."
}
```
**Семпл #32:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/blok-pitaniya-vinga-vps-2000w-2kvt-bronze-80-IDZQKW3.html",
  "title": "Блок питания Vinga VPS 2000w, 2квт, bronze 80+"
}
```
**Семпл #33:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/nadyniy-blok-zhivlennya-dlya-sistemnika-chieftec-proton-bdf-1000c-1000w-IDZtksE.html",
  "title": "Надійний блок живлення для системника Chieftec Proton BDF-1000C 1000W"
}
```
**Семпл #34:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Блок живлення від ПК",
  "item_type": "psu"
}
```
**Семпл #35:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/blok-divlennya-azza-psaz-650w-bronze-IDZy2BD.html",
  "title": "Блок дивлення AZZA PSAZ 650w Bronze"
}
```
**Семпл #36:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/blok-pitaniya-cougar-600w-ID10UUjx.html",
  "title": "Блок питания Cougar 600w"
}
```
**Семпл #37:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/blok-zhivlennya-thermaltake-grand-rgb-850w-ID10Z1jh.html",
  "title": "Блок живлення Thermaltake Grand RGB 850W"
}
```
**Семпл #38:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "10 блоків живлення 650, 670, 750 та 835Вт до серверів одним лотом",
  "item_type": "psu"
}
```
**Семпл #39:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/blok-pitaniya-vinga-vps-2000w-2kvt-bronze-80-IDZQKW3.html",
  "title": "Блок питания Vinga VPS 2000w, 2квт, bronze 80+"
}
```
**Семпл #40:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "1 Гбіт‼️Гигабитный PoE адаптер 48В TP link инжектор блок питания живлення для камеры камери відеонагляду видеонаблюдения точки доступа доступу роутера",
  "item_type": "psu"
}
```
**Семпл #41:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/bp-bzh-750w-z-garantyu-blok-zhivlennya-blok-pitaniya-gigabyte-p750gm-750w-80-gold-ID10RkTA.html",
  "title": "БП / БЖ 750W З ГАРАНТІЄЮ / блок живлення / блок питания Gigabyte P750GM 750W 80+ gold"
}
```
**Семпл #42:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/hq-tech-hq-400-400w-silent-power-supply-IDZ4uVx.html",
  "title": "HQ-Tech HQ-400 (400W, Silent Power Supply)"
}
```
**Семпл #43:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/top-blok-zhivlennya-1000w-super-flower-platinum-gbridniy-fan-tradein-ID10I1iI.html",
  "title": "ТОП! блок живлення 1000W Super Flower PLATINUM (гібридний FAN).TradeIN"
}
```
**Семпл #44:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "DeBangSi YFY-A59",
  "item_type": "psu"
}
```
**Семпл #45:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/blok-zhivlennya-gigabyte-ultra-durable-850w-800w-900w-750w-ID10Z17g.html",
  "title": "Блок живлення Gigabyte Ultra Durable 850W 800W 900W 750W"
}
```
**Семпл #46:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/blok-zhivlennya-thermaltake-toughpower-irgb-plus-1050w-1000w-1100w-ID10Z12w.html",
  "title": "Блок живлення Thermaltake Toughpower iRGB Plus 1050W 1000W 1100W"
}
```
**Семпл #47:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/blok-zhivlennya-chieftec-vega-m-750w-ppg-750-c-ID10n8vI.html",
  "title": "Блок живлення CHIEFTEC Vega M 750W (PPG-750-C)"
}
```
**Семпл #48:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/blok-zhivlennya-thermaltake-smart-se-630w-600w-550w-650w-ID10Z0Y7.html",
  "title": "Блок живлення Thermaltake Smart SE 630W 600W 550W 650W"
}
```
**Семпл #49:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/bzh-80-gold-pd-remont-700w-850w-750w-thermaltake-gf-gt-toughpower-berlin-tr2-s-ID10Z0Pd.html",
  "title": "БЖ 80+ Gold  під ремонт 700w 850w 750w Thermaltake GF GT toughpower berlin tr2 s"
}
```
**Семпл #50:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/blok-zhivlennya-450w-thermaltake-smart-dps-g-450w-80-plus-gold-plomba-ID10Z0RW.html",
  "title": "Блок живлення 450W Thermaltake Smart DPS G 450W 80 PLUS Gold (Пломба)"
}
```
**Семпл #51:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/blok-zhivlennya-chieftec-1000w-IDUm58Y.html",
  "title": "Блок живлення CHIEFTEC 1000W"
}
```
**Семпл #52:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/blok-zhivlennya-inter-tech-sl-700-plus-700w-z-garantyu-ID10BFzb.html",
  "title": "Блок живлення Inter-Tech SL-700 Plus 700W з гарантією"
}
```
**Семпл #53:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Seasonic Prime TX-650 80 Plus Titanium (SSR-650TR) Блок живлення модульний ігровий  gtx rtx mx gt gaming rx oc",
  "item_type": "psu"
}
```
**Семпл #54:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Блок живлення Seasonic SSR-750PX (Focus PX-750 platinum)",
  "item_type": "psu"
}
```
**Семпл #55:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/blok-zhivlennya-seasonic-a851bcafh-b12-bc-850-850w-bronze-IDWhvBJ.html",
  "title": "Блок живлення Seasonic A851BCAFH (B12 BC-850) 850W Bronze"
}
```
**Семпл #56:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Продам блоки питания",
  "item_type": "psu"
}
```
**Семпл #57:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/blok-zhivlennya-na-garant-deepcool-gamer-storm-pf700x-700w-ID10Nvzo.html",
  "title": "Блок живлення на гарантії DeepCool Gamer Storm PF700X 700W"
}
```
**Семпл #58:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Блок питания Canon CA-CP200 24v-2.2A  \"Original\"",
  "item_type": "psu"
}
```
**Семпл #59:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Продаю оригінальний блок живлення для ноутбука ASUS",
  "item_type": "psu"
}
```
**Семпл #60:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Asic Antminer l3+ з блоком живлення. Херсон",
  "item_type": "psu"
}
```
**Семпл #61:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Блок живлення SeaSonic Focus Plus 1000 Gold (SSR-1000FX)",
  "item_type": "psu"
}
```
**Семпл #62:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/blok-zhivlennya-pk-kompyutera-blok-pitaniya-chieftec-600w-ID10YZOJ.html",
  "title": "Блок живлення пк компютера блок питания chieftec 600w"
}
```
**Семпл #63:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Блок живлення ENERMAX PRO82+ 385Вт",
  "item_type": "psu"
}
```
**Семпл #64:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Блоки живлення 24V 0.8A 18W, 24V 0,4А 9,12 W (MikroTik / ULLPOWER)",
  "item_type": "psu"
}
```
**Семпл #65:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/seasonic-prime-ultra-850w-titanium-ssr-850tr-titanoviy-top-modulniy-rtx-gtx-gt-mx-rx-gaming-oc-ID10PaHT.html",
  "title": "Seasonic PRIME Ultra 850W Titanium (SSR-850TR) титановий  топ Модульний rtx gtx gt mx rx gaming oc"
}
```
**Семпл #66:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/blok-pitaniya-650vat-550w-500vat-400v-450v-IDST7vx.html",
  "title": "Блок питания 650ват 550w 500ват 400в 450в"
}
```
**Семпл #67:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/b-v-brendoviy-blok-zhivlennya-hp-240w-hp-4000-4300-6200-6300-8000-8100-8300-ID10NwXY.html",
  "title": "Б/В Брендовий блок живлення HP 240W (HP 4000 4300 6200 6300 8000 8100 8300)"
}
```
**Семпл #68:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/be-quiet-dark-power-pro-12-1200w-titanium-p12-pro-1200w-topoviy-ultimativniy-rtx-gtx-rx-gt-gaming-oc-blok-zhivlennya-bzh-pitaniya-mx-ID10WB0I.html",
  "title": "be quiet! Dark Power Pro 12 1200W Titanium [P12-PRO-1200W] топовий Ультимативний RTX GTX RX gt  gaming oc блок живлення бж питания MX"
}
```
**Семпл #69:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Плата живлення DELUXE LR1204-120W 12VDC / PicoPSU / DC-ATX",
  "item_type": "psu"
}
```
**Семпл #70:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/blok-zhivlennya-enermax-maxpro-ii-400w-80-noviy-nadyniy-holodniy-ID10Atvm.html",
  "title": "Блок живлення ENERMAX MAXPRO II 400W 80+ | новий | надійний Холодний"
}
```
**Семпл #71:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Системный блок может кому нужен на запчасти",
  "item_type": "psu"
}
```
**Семпл #72:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Ретро ПК Intel Pentium II (1998)",
  "item_type": "psu"
}
```
**Семпл #73:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/blok-zhivlennya-q-dion-qd450-450w-fsp-active-pfc-ID10YZ7b.html",
  "title": "Блок живлення Q-DION QD450 450W (FSP, Active PFC)"
}
```
**Семпл #74:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Блоки живлення 3 шт",
  "item_type": "psu"
}
```
**Семпл #75:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/blok-zhivlennya-gigabyte-p650b-650w-80-bronze-ID10YZ4T.html",
  "title": "Блок живлення Gigabyte P650B 650W 80+ Bronze"
}
```
**Семпл #76:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/blok-zhivlennya-be-quiet-dark-power-bqt-p7-pro-450w-power-ID10YYYO.html",
  "title": "Блок живлення Be Quiet Dark Power BQT P7-PRO 450W Power"
}
```
**Семпл #77:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/seasonic-prime-platinum-1300w-ssr-1300pd-platinum-flagman-etalonn-testi-plomba-rtx-rx-gtx-gt-mx-gaming-oc-ID10Paim.html",
  "title": "Seasonic PRIME Platinum 1300W (SSR-1300PD) Platinum Флагман  Еталонні тести  Пломба rtx rx gtx gt mx gaming oc"
}
```
**Семпл #78:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/be-quiet-dark-power-pro-12-1200w-titanium-p12-pro-1200w-topoviy-ultimativniy-rtx-gtx-rx-gt-gaming-oc-blok-zhivlennya-bzh-pitaniya-mx-ID10WB0I.html",
  "title": "be quiet! Dark Power Pro 12 1200W Titanium [P12-PRO-1200W] топовий Ультимативний RTX GTX RX gt  gaming oc блок живлення бж питания MX"
}
```
**Семпл #79:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/blok-zhivlennya-thermaltake-berlin-750w-ID10YlER.html",
  "title": "Блок живлення thermaltake Berlin 750w"
}
```
**Семпл #80:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Продам универсальный  блок питания к ноутбуку MAXXTRO SCAC 2004",
  "item_type": "psu"
}
```
**Семпл #81:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/bloki-pitaniya-750w-850w-garantiya-opt-IDLP6qD.html",
  "title": "Блоки питания 750w 850w Гарантия Опт !"
}
```
**Семпл #82:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/kompyuternyy-blok-pitaniya-450w-550w-650w-750w-850w-IDUqtPm.html",
  "title": "Компютерный блок питания 450w 550w 650w 750w 850w"
}
```
**Семпл #83:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/blok-zhivlennya-atx-dlya-pk-350w-400w-450w-460w-500w-1600w-chieftec-cooler-master-dlya-kompyutera-IDJVQdN.html",
  "title": "Блок живлення ATX для ПК 350W, 400W, 450W, 460W, 500W, 1600W Chieftec Cooler Master, для компютера"
}
```
**Семпл #84:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Блок живлення Chiefteac A135 Series APS-600C 80 Plus",
  "item_type": "psu"
}
```
**Семпл #85:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/blok-zhivlennya-2e-master-power-750w-IDWVx98.html",
  "title": "Блок живлення 2E Master Power 750W"
}
```
**Семпл #86:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/blok-zhivlennya-corsair-rm650i-650w-na-zapchastini-ID10YY3k.html",
  "title": "Блок живлення Corsair RM650i 650W на запчастини"
}
```
**Семпл #87:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Переходник для питания wifi от павер банка",
  "item_type": "psu"
}
```
**Семпл #88:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Chieftec Proton BDF-500S ще на гарантії від Rozetka",
  "item_type": "psu"
}
```
**Семпл #89:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/blok-zhivlennya-atx-sparkman-sm-400w-IDZCdVu.html",
  "title": "Блок живлення ATX Sparkman SM-400W"
}
```
**Семпл #90:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "NEW Блоки живлення BITMAIN APW17 (APW171215c) для S21/ T21/ L9/ L11",
  "item_type": "psu"
}
```
**Семпл #91:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/blok-zhivlennya-vinga-vps-1350-be-quiet-system-power-700w-ID10QKiV.html",
  "title": "Блок живлення Vinga VPS 1350, be quiet System Power 700W"
}
```
**Семпл #92:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/blok-zhivlennya-seasonic-prime-ultra-gold-850w-ssr-850gd-2583-IDZET2U.html",
  "title": "Блок живлення Seasonic Prime Ultra Gold 850W (SSR-850GD) - 2583"
}
```
**Семпл #93:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/blok-zhivlennya-thermalright-gt-850-w-atx-3-1-pci-e-5-1-vhpwr-gold-modular-ID10YXPQ.html",
  "title": "Блок Живлення Thermalright GT-850-W ATX 3.1 PCI-E 5.1 VHPWR Gold Modular"
}
```
**Семпл #94:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Блок питания компьютера",
  "item_type": "psu"
}
```
**Семпл #95:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/blok-pitaniya-cooler-master-380w-rs-380-pmsp-ID10YXK9.html",
  "title": "Блок питания Cooler Master 380W (RS-380-PMSP)"
}
```
**Семпл #96:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Блок питания 500ват  frime glare apec led series",
  "item_type": "psu"
}
```
**Семпл #97:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "БЖ Seasonic SS-600ET, 80+ справний, гарантія",
  "item_type": "psu"
}
```
**Семпл #98:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/blok-zhivlennya-seasonic-focus-gx-750-750w-ssr-750fx-3366-IDYDB3P.html",
  "title": "Блок живлення Seasonic Focus GX-750 750W (SSR-750FX) - 3366"
}
```
**Семпл #99:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/blok-zhivlennya-tacens-600w-eco-ii-600-600w-atx-IDZVC4q.html",
  "title": "Блок живлення TACENS 600W (ECO II 600) 600W ATX"
}
```
**Семпл #100:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Блок живлення Chieftec GPE-600S Гарантія 1 місяць",
  "item_type": "psu"
}
```

#### 💾 Накопичувачі (SSD / HDD) — Відсіяно (Показано 100 з max 100):
**Семпл #1:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/zhorstkiy-disk-western-digital-wd-purple-500gb-1tb-2tb-3tb-4tb-8tv-IDTMqiX.html",
  "title": "Жорсткий диск  Western digital WD Purple 500Gb 1TB, 2TB, 3TB, 4TB, 8ТВ"
}
```
**Семпл #2:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Жорсткі диски  x2   |   SSD  диски  x2   |    Диск для ноутбука",
  "item_type": "storage"
}
```
**Семпл #3:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/zhorstkiy-disk-wd-purple-500gb-1tb-2tb-3tb-4tb-8tb-IDVoDwf.html",
  "title": "Жорсткий диск WD Purple 500Gb, 1TB, 2TB, 3TB, 4TB, 8TB"
}
```
**Семпл #4:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Продам жосткий диск вид компутера в роботом стани",
  "item_type": "storage"
}
```
**Семпл #5:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/zhorstk-diski-320gb-3-5-do-pk-dealn-IDYMClr.html",
  "title": "Жорсткі диски 320gb 3.5\" до ПК, ідеальні"
}
```
**Семпл #6:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/nakopichuvach-ssd-m-2-1tb-kingston-snv2s-1000g-noviy-IDXAUmb.html",
  "title": "Накопичувач SSD M.2 1TB Kingston (SNV2S/1000G) (НОВИЙ)"
}
```
**Семпл #7:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Продам жорсткі диски",
  "item_type": "storage"
}
```
**Семпл #8:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/samsung-hdd-1tb-seagate-hdd-2tb-ID10Z3td.html",
  "title": "Samsung HDD 1tb Seagate HDD 2tb"
}
```
**Семпл #9:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/zhorstkiy-disk-2-tb-seagate-barracuda-st2000dm008-nov-ID10bAXd.html",
  "title": "Жорсткий диск 2 TB Seagate BarraCuda (ST2000DM008), НОВІ"
}
```
**Семпл #10:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/zhorstkiy-disk-1tb-ta-500gb-IDVW4JT.html",
  "title": "Жорсткий диск 1tb та 500gb"
}
```
**Семпл #11:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Продам новий жорсткий диск для пк HDD 3.5  WD10EZRZ в заводському пакуванні!",
  "item_type": "storage"
}
```
**Семпл #12:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/noviy-ssd-m-2-nvme-pcie-4-0-256gb-samsung-pm9c1-4000-mb-s-100-health-1-god-ID10Z2JG.html",
  "title": "Новий SSD M.2 NVMe PCIe 4.0 256GB Samsung PM9C1 (4000 MB/s, 100% Health, 1 год)"
}
```
**Семпл #13:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/zhorstkiy-disk-toshiba-pc-p300-500-gb-sata-3-5-7200-ob-hv-ID10LIwz.html",
  "title": "Жорсткий диск Toshiba PC P300 500 ГБ SATA 3.5\" 7200 об/хв"
}
```
**Семпл #14:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/seagate-barracuda-pro-10tb-hdd-sata-iii-7200-rpm-ID10M8ny.html",
  "title": "Seagate BarraCuda Pro 10TB HDD SATA III 7200 RPM"
}
```
**Семпл #15:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/ssd-bestoss-2-5-sata-120-256-512gb-IDU1Wsi.html",
  "title": "Ssd Bestoss (2.5 Sata) 120,256,512gb"
}
```
**Семпл #16:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/wd-8tb-3-5-5400-rpm-v-otlichneyshem-sostoyanii-IDZK5xZ.html",
  "title": "WD 8TB 3.5\" 5400 RPM, в отличнейшем состоянии"
}
```
**Семпл #17:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/zhorstkiy-disk-hdd-wd-red-3-tb-wd30efrx-ID10Z2KF.html",
  "title": "Жорсткий диск HDD WD Red 3 TB (WD30EFRX)"
}
```
**Семпл #18:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/zhorstkiy-disk-4tb-ID10Z2Iy.html",
  "title": "Жорсткий диск 4TB"
}
```
**Семпл #19:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/zhestkiy-disk-na-500gb-ID10Z2D1.html",
  "title": "Жёсткий диск на 500GB"
}
```
**Семпл #20:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/zhorstkiy-disk-seagate-exos-x16-hdd-16tb-7200rpm-256mb-st16000nm001g-3-5-sata-iii-ID10NtDq.html",
  "title": "Жорсткий диск Seagate Exos X16 HDD 16TB 7200rpm 256MB ST16000NM001G 3.5\" SATA III"
}
```
**Семпл #21:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/zhorstkiy-disk-8tb-wd8003ffbx-ID10Z2zW.html",
  "title": "Жорсткий диск 8Tb WD8003FFBX"
}
```
**Семпл #22:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/hdd-1-tb-160-250-500gb-ssd-256-gb-ID10qlXJ.html",
  "title": "HDD 1 ТБ, 160-250-500GB, SSD 256 GB"
}
```
**Семпл #23:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Кабель подовжувач Slimline SATA (7+6 pin) для HDD/SSD/DVD/CD / Адаптер",
  "item_type": "storage"
}
```
**Семпл #24:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/zhorstkiy-disk-6tb-wd6003ffbx-ID10Z22L.html",
  "title": "Жорсткий диск 6Tb WD6003FFBX"
}
```
**Семпл #25:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/nakopichuvach-samsung-970-evo-plus-250gb-m-2-pcie-3-0-ID10Z1WE.html",
  "title": "Накопичувач Samsung 970 Evo Plus 250GB M.2 PCIe 3.0"
}
```
**Семпл #26:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/2tb-2000gb-2-5-mayzhe-nov-mala-narobotka-klkst-zovnshny-disk-smart-na-foto-narobotka-mnmalna-ID10OzRj.html",
  "title": "2tb 2000gb 2.5 майже нові мала нароботка  є кількість зовнішній  диск смарт на фото нароботка мінімальна"
}
```
**Семпл #27:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/noviy-zapakovaniy-ssd-disk-klevv-cras-c910-3d-nand-slc-1tb-m-2-ssd-1tb-ID10UOAU.html",
  "title": "Новий, запакований SSD-диск KLEVV CRAS C910 3D NAND SLC 1TB M.2. ССД 1ТБ"
}
```
**Семпл #28:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Продам новий жорсткий диск для пк HDD 3.5  WD10EZRZ в заводському пакуванні!",
  "item_type": "storage"
}
```
**Семпл #29:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/zhorstkiy-disk-8tb-hdd-western-digital-wd85purz-ID10Z1Qv.html",
  "title": "Жорсткий диск 8TB HDD Western Digital WD85PURZ"
}
```
**Семпл #30:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "HP SAS Expander Card 24-Port / Плата розширення SAS/SATA (487738-001 / 468405-002)",
  "item_type": "storage"
}
```
**Семпл #31:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/prodam-ssd-disk-samsung-480gb-ID10Z1OZ.html",
  "title": "Продам SSD Диск Samsung 480Gb"
}
```
**Семпл #32:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/zhestkiy-disk-dlya-noutbuka-250-gb-IDXlwsz.html",
  "title": "Жёсткий диск для ноутбука 250 Gb"
}
```
**Семпл #33:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/ssd-512-gb-sata-2-5-ID10Z1Kc.html",
  "title": "Ssd 512 gb sata 2.5"
}
```
**Семпл #34:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/zhorstkiy-disk-4-tb-wd4003ffbx-ID10Z1Jq.html",
  "title": "Жорсткий диск 4 Tb WD4003FFBX"
}
```
**Семпл #35:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "HBA Контролер HP H241 Smart Array 12Gb SAS/SATA (726911-001 / 750054-001)",
  "item_type": "storage"
}
```
**Семпл #36:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Western Digital WD5000LPCX",
  "item_type": "storage"
}
```
**Семпл #37:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/zhorstkiy-disk-16tb-hdd-seagate-exos-x18-st16000nm000j-ID10Z1tw.html",
  "title": "Жорсткий диск 16TB HDD Seagate Exos X18 ST16000NM000J"
}
```
**Семпл #38:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/ssd-kingston-120-gb-ID10Crjm.html",
  "title": "SSD Kingston 120 Gb"
}
```
**Семпл #39:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/ssd-nakopichuvach-crucial-bx500-2tb-sata-iii-3-roki-garant-ID10X9sy.html",
  "title": "SSD накопичувач Crucial BX500 2TB Sata III (3 роки гарантії)"
}
```
**Семпл #40:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/prodam-rostovku-novyh-ssd-diskov-64gb-4tb-priehali-vkusnyashki-IDZQCT0.html",
  "title": "Продам ростовку новых SSD дисков 64гб-4тб (приехали вкусняшки)"
}
```
**Семпл #41:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Жорсткі диски hdd 2,5” (для ноутбуків, компʼютерів)",
  "item_type": "storage"
}
```
**Семпл #42:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/disk-ssd-goodram-cx400-256gb-ID10Z1w2.html",
  "title": "диск SSD GoodRam CX400 256Gb"
}
```
**Семпл #43:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/zhorstkiy-disk-8tb-hdd-seagate-skyhawk-surveillance-st8000vx010-IDUxT2B.html",
  "title": "Жорсткий диск 8TB HDD Seagate SkyHawk Surveillance ST8000VX010"
}
```
**Семпл #44:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/disk-ssd-m-2-goodram-px500-256-gb-noviy-ID10Z1ov.html",
  "title": "диск SSD M.2 Goodram PX500 256 Gb новий"
}
```
**Семпл #45:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/320gb-500gb-vinchester-zhestkiy-disk-hdd-2-5-dlya-noutbuka-IDSwoBt.html",
  "title": "320GB, 500GB Винчестер, жесткий диск, HDD 2.5 для ноутбука"
}
```
**Семпл #46:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/ssd-kingston-m2-250gb-IDZOFWr.html",
  "title": "ssd kingston m2 250gb"
}
```
**Семпл #47:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/zhestkiy-disk-sas-2tb-seagate-ID10eDt9.html",
  "title": "Жесткий диск SAS 2TB Seagate"
}
```
**Семпл #48:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Серверний кошик HP 2.5\" SFF Caddy / Салазки HP ProLiant Gen8 Gen9 (651687-001)",
  "item_type": "storage"
}
```
**Семпл #49:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Жесткий диск Samsung",
  "item_type": "storage"
}
```
**Семпл #50:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/top-nadynst-ssd-disk-512gb-kingston-ssdnow-kc400-mlc-sata3-2-5-ID10Z0D6.html",
  "title": "ТОП надійність SSD диск 512GB Kingston SSDNow KC400 MLC (SATA3 \\ 2.5\")"
}
```
**Семпл #51:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/zhestkiy-disk-320gb-seagate-barracuda-7200-10-IDPOmQC.html",
  "title": "Жесткий диск 320GB Seagate Barracuda 7200. 10"
}
```
**Семпл #52:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/ssd-disk-2-5-sata-1tb-sandisk-ultra-ii-ID10Wg7o.html",
  "title": "SSD Диск 2.5 SATA 1TB SanDisk Ultra II"
}
```
**Семпл #53:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/ssd-m2-nvme-128-gb-250gb-480gb-1-tb-samsung-hunix-toshiba-perehdniki-do-kompyutera-pci-e-ta-operativna-pamyat-ram-ID102Fzz.html",
  "title": "SSD m2 NVME 128 Гб, 250Gb 480Gb 1 tb Samsung Hunix Toshiba, є перехідники до компютера PCI e та  оперативна память RAM"
}
```
**Семпл #54:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/ssd-wd-crucial-500gb-100-zhittya-ID10YCwb.html",
  "title": "Ssd wd crucial 500gb 100% життя"
}
```
**Семпл #55:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/nakopichuvach-disk-120gb-240gb-ID10qjG9.html",
  "title": "Накопичувач.Диск. 120GB. 240GB"
}
```
**Семпл #56:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/disk-zhestkiy-hgst-5k1000-1000-1tb-sata-iii-2-5-hts541010a9e680-ID10Nrbi.html",
  "title": "Диск жесткий hgst 5k1000-1000 1tb sata iii 2,5\" hts541010a9e680"
}
```
**Семпл #57:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/zhorstkiy-disk-hdd-3-5-toshiba-500gb-7200rpm-dt01aca050-sata-iii-ID10Z0k8.html",
  "title": "Жорсткий диск HDD 3.5 Toshiba 500GB 7200rpm (DT01ACA050) SATA III"
}
```
**Семпл #58:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/samsung-1tb-970-eva-plus-99-garantiya-30d-ID10NjLk.html",
  "title": "SAMSUNG 1TB 970 EVA Plus / 99% / Гарантия 30Д."
}
```
**Семпл #59:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/ssd-kingstone-1tb-sata-iii-ssd-disk-b-u-ID10NjN8.html",
  "title": "SSD KingStone 1TB / SATA III / SSD Диск (Б/У)"
}
```
**Семпл #60:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "DVD диски б/у для компютера",
  "item_type": "storage"
}
```
**Семпл #61:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/zhestkiy-disk-200-gb-IDKKvD0.html",
  "title": "Жёсткий диск 200 Гб"
}
```
**Семпл #62:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/prodam-ssd-nov-256gb-512gb-1tb-somnambulist-teclast-yaksn-ID10CpD9.html",
  "title": "Продам SSD нові!! 256gb, 512gb, 1tb!! Somnambulist, Teclast якісні!"
}
```
**Семпл #63:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/prodayu-ssd-240gb-adata-ID10YZW7.html",
  "title": "Продаю SSD 240GB ADATA"
}
```
**Семпл #64:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/zhorstkiy-disk-seagate-1tb-dlya-pk-ID10B9MH.html",
  "title": "жорсткий диск Seagate 1Тб для ПК"
}
```
**Семпл #65:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/ssd-crucial-p3-plus-4tb-ID10YNJp.html",
  "title": "SSD Crucial P3 Plus 4TB"
}
```
**Семпл #66:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/ssd-nakopichuvach-kingston-a400-960-gb-sa400s37-960g-ID10Y86U.html",
  "title": "SSD накопичувач Kingston A400 960 GB (SA400S37/960G)"
}
```
**Семпл #67:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/m2-nvme-ssd-512gb-netac-nv3000-3600mb-s-ID10pFbe.html",
  "title": "M2 NVMe SSD 512GB Netac NV3000 3600Mb/s"
}
```
**Семпл #68:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Кишеня для HDD у відсік DVD",
  "item_type": "storage"
}
```
**Семпл #69:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/zhorstkiy-disk-hdd-2tb-wd-p10-game-drive-wdba2w0020bbk-wesn-ID10qhi4.html",
  "title": "Жорсткий диск (HDD) 2TB WD P10 Game Drive WDBA2W0020BBK-WESN"
}
```
**Семпл #70:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Дискета большая, le Monti",
  "item_type": "storage"
}
```
**Семпл #71:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Продам жосткий диск для ПК на 2 Терабайта с гарантией от магазина",
  "item_type": "storage"
}
```
**Семпл #72:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/zhorstkiy-disk-na-3-tv-terabayta-IDZhQQV.html",
  "title": "Жорсткий диск на 3 ТВ (терабайта)"
}
```
**Семпл #73:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/prodam-zhorstkiy-disk-2-5-dlya-noutbuka-320-gb-ID10YXQT.html",
  "title": "Продам жорсткий диск 2.5 для ноутбука 320 гб"
}
```
**Семпл #74:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/nadezhnyy-hdd-400gb-hitachi-deskstar-7200rpm-16mb-sata-ii-ID10eCki.html",
  "title": "Надежный HDD 400GB Hitachi Deskstar (7200rpm, 16MB) SATA II"
}
```
**Семпл #75:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/ssd-disk-2-5-sata-1tb-sandisk-ultra-ii-ID10Wg7o.html",
  "title": "SSD Диск 2.5 SATA 1TB SanDisk Ultra II"
}
```
**Семпл #76:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/zhorstkiy-disk-hdd-1tb-2-5-seagate-ID10YXHi.html",
  "title": "Жорсткий диск HDD 1TB 2.5 Seagate"
}
```
**Семпл #77:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/m-2-ssd-disk-250gb-kingston-nv2-m-2-2280-nvme-pci-e-4-0-x4-tradein-ID10YXD0.html",
  "title": "M.2 SSD диск 250GB Kingston NV2 (M.2 2280 \\ NVMe \\ PCI-e 4.0 x4) TradeIN"
}
```
**Семпл #78:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/nakopichuvach-ssd-m-2-512gb-apacer-ID10VTXv.html",
  "title": "Накопичувач SSD M.2 512GB Apacer"
}
```
**Семпл #79:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/ssd-diski-goodram-480-512-1tb-IDXF7CU.html",
  "title": "Ssd диски Goodram 480/512/1tb."
}
```
**Семпл #80:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/noviy-ssd-m-2-nvme-pcie-4-0-256gb-samsung-pm9c1-4000-mb-s-100-health-1-god-ID10Z2JG.html",
  "title": "Новий SSD M.2 NVMe PCIe 4.0 256GB Samsung PM9C1 (4000 MB/s, 100% Health, 1 год)"
}
```
**Семпл #81:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/noutbuchnyy-zhestkiy-disk-na-320gb-v-otlichnom-sostoyanii-IDRMXuX.html",
  "title": "Ноутбучный Жёсткий диск на 320гб в отличном состоянии"
}
```
**Семпл #82:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/ssd-samsung-860evo-500gb-ID10YXvQ.html",
  "title": "SSD  Samsung 860evo 500gb"
}
```
**Семпл #83:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/zhestkiy-disk-western-digital-blue-1tb-IDVUXqd.html",
  "title": "Жесткий диск Western Digital Blue 1TB"
}
```
**Семпл #84:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/zhestkiy-disk-hd-500gb-320gb-ID10YXtF.html",
  "title": "Жёсткий диск HD 500GB, 320GB"
}
```
**Семпл #85:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/ssd-nakopichuvach-samsung-1tb-ID10YXrn.html",
  "title": "SSD накопичувач Samsung 1Tb"
}
```
**Семпл #86:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Жорсткий диск sumsung sp080n / sp0802j",
  "item_type": "storage"
}
```
**Семпл #87:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/zhorstkiy-disk-3-5-hdd-1tb-seagate-constellation-es-st1000nm0011-ID10YXao.html",
  "title": "Жорсткий диск 3,5\" HDD 1TB Seagate Constellation ES (ST1000NM0011)"
}
```
**Семпл #88:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Жорсткий диск Seagate для ПК 1 ТБ | 3,5\" | SATA III",
  "item_type": "storage"
}
```
**Семпл #89:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/nvme-1tb-samsung-wd-toshiba-sk-hynix-IDNY9hY.html",
  "title": "nvme 1Tb SAMSUNG, WD, Toshiba, SK Hynix"
}
```
**Семпл #90:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Sata SSD Amd Radeon 256 новий",
  "item_type": "storage"
}
```
**Семпл #91:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/ssd-4tb-kingston-kc3000-m-2-2280-pcie-4-0-x4-nvme-3d-tlc-ID10gKah.html",
  "title": "SSD 4TB Kingston KC3000 M.2 2280 PCIe 4.0 x4 NVMe 3D TLC"
}
```
**Семпл #92:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/ssd-m-2-nvme-1tb-netac-nv7000-t-pcie-4-0-7300-mb-s-stan-100-skrni-ID10X2ul.html",
  "title": "SSD M.2 NVMe 1TB Netac NV7000-t PCIe 4.0 (7300 MB/s) / Стан 100% / Скріни"
}
```
**Семпл #93:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/2-5-m-2-ssd-disk-128gb-250gb-500gb-crucial-samsung-hynix-wd-IDWxjls.html",
  "title": "2.5 M.2 SSD диск 128GB 250GB 500GB Crucial Samsung Hynix WD"
}
```
**Семпл #94:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Жорсткий диск Fujitsu 30 Gb",
  "item_type": "storage"
}
```
**Семпл #95:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "SSD диск Samsung 970 EVO Plus 500G 99% здоровя",
  "item_type": "storage"
}
```
**Семпл #96:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "винчестер жесткий диск АТА 40 Гб нерабочий под ремонт",
  "item_type": "storage"
}
```
**Семпл #97:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "SATA-USB 3.0 для HDD 3.5\"/2.5\"",
  "item_type": "storage"
}
```
**Семпл #98:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/zhorstkiy-disk-tandberg-data-rdx-quickstor-2tb-8731-rdx-IDYPzZK.html",
  "title": "Жорсткий диск Tandberg Data RDX QuickStor 2TB (8731-RDX)"
}
```
**Семпл #99:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Жорсткий диск hdd",
  "item_type": "storage"
}
```
**Семпл #100:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/ssd-disk-480gb-patriot-burst-sata3-2-5-trade-in-ID10B2Wd.html",
  "title": "SSD диск 480GB Patriot BURST (SATA3 \\ 2.5\"). Trade-IN"
}
```

#### 📟 Оперативна пам'ять (RAM) — Відсіяно (Показано 100 з max 100):
**Семпл #1:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/novaya-ddr3-8gb-1600mhz-12800u-intel-amd-operativnaya-pamyat-dlya-pk-IDJXL1m.html",
  "title": "НОВАЯ DDR3 8GB 1600mhz 12800U Intel/AMD оперативная память для ПК"
}
```
**Семпл #2:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Оперативна память для пк ddr2 2gb",
  "item_type": "ram"
}
```
**Семпл #3:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Оперативная память",
  "item_type": "ram"
}
```
**Семпл #4:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Kingston HyperX KHX16C9C2K2/16",
  "item_type": "ram"
}
```
**Семпл #5:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Оперативна память Goodram DDR3 2GB 1333",
  "item_type": "ram"
}
```
**Семпл #6:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/pamyat-do-pk-ddr3-2gb-4gb-IDYOK7h.html",
  "title": "Память до ПК DDR3 2Gb 4Gb"
}
```
**Семпл #7:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/prodam-dve-planki-ddr3-2x4gb-1600-IDXly7E.html",
  "title": "продам две планки ddr3 2x4gb 1600"
}
```
**Семпл #8:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/pamyat-ddr5-na-8gb-ID10Vu1Y.html",
  "title": "Память DDR5 на 8Gb"
}
```
**Семпл #9:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Память ОЗУ DDR3 PC3-8500S  2 Gb для ноутбука",
  "item_type": "ram"
}
```
**Семпл #10:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Память ОЗУ для ноутбука DDR-3 1333 CL9 2Gb",
  "item_type": "ram"
}
```
**Семпл #11:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Оперативка Viper rgb 16gb 3200mhz",
  "item_type": "ram"
}
```
**Семпл #12:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Комплект Micron DDR3L 1867MHz 16GB (8+8) 1.35V 2Rx8 PC3L-14900 [ максимальна швидкість ], оперативна память, оригінал",
  "item_type": "ram"
}
```
**Семпл #13:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/operativna-pamyat-ddr4-pc4-sodimm-16gb-2400-2666-3200mhz-ID10uiZq.html",
  "title": "Оперативна память DDR4 PC4 Sodimm 16GB,2400,2666,3200MHz"
}
```
**Семпл #14:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Память ОЗУ для  ноутбука PC3L-12800S 4Gb",
  "item_type": "ram"
}
```
**Семпл #15:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/prodam-ozp-kingston-ddr4-16gb-2x8gb-3200mhz-fury-beast-black-kf432c16bbk2-16-ID10VNew.html",
  "title": "Продам ОЗП Kingston DDR4 16GB (2x8GB) 3200Mhz FURY Beast Black (KF432C16BBK2/16)"
}
```
**Семпл #16:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "оперативна память TeamGroup Elite (модель TED34G1600C11BK),",
  "item_type": "ram"
}
```
**Семпл #17:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/hyperx-ddr4-32gb2x16gb2666mhz-amd-ryzen-5-3600-tray-ID10Z3ar.html",
  "title": "HyperX DDR4 32GB(2x16GB)2666Mhz/AMD Ryzen 5 3600 Tray"
}
```
**Семпл #18:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/modul-operativnoy-pamyati-plata-ozu-ram-dram-so-dimm-ddr4-generation-memory-offtek-uk-8gb-ID100SRE.html",
  "title": "модуль оперативной памяти плата озу ram dram so-dimm ddr4 generation memory offtek uk 8gb"
}
```
**Семпл #19:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Оперативна память ddr3",
  "item_type": "ram"
}
```
**Семпл #20:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/kingston-pamyat-ddr3-4gb-2x2-pc3-10600-1333mnz-ID10Z30O.html",
  "title": "Kingston Память DDR3 4gb (2x2) PC3-10600 (1333mnz)"
}
```
**Семпл #21:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/modul-pamyat-corsair-ddr5-32gb-2x16-6000mhz-vengeance-IDZlLu1.html",
  "title": "Модуль памяті Corsair DDR5 32GB (2x16) 6000MHz VENGEANCE"
}
```
**Семпл #22:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/g-skill-aegis-ddr4-16gb-operativnaya-pamyatt-ID10Z2WS.html",
  "title": "G.Skill Aegis DDR4 16gb оперативная памятьть"
}
```
**Семпл #23:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/moduli-pamyati-dlya-noutbuka-samsung-16gb-ddr4-c-garantiey-IDZytKp.html",
  "title": "Модули памяти для ноутбука, Samsung  16GB DDR4  .C гарантией."
}
```
**Семпл #24:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/serverna-pamyat-ddr4-32gb-4rx4-pc4-2133p-ecc-reg-2133mhz-hp-ID10QHbl.html",
  "title": "Серверна память DDR4 32Gb 4Rx4 PC4-2133P ECC REG 2133Mhz HP"
}
```
**Семпл #25:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Продам ОПТОМ оперативну память 8 gb DDR3L",
  "item_type": "ram"
}
```
**Семпл #26:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/operativna-pamyat-corsair-ddr5-5200-mhz-vengeance-96-gb-2-plashki-IDZHeIh.html",
  "title": "Оперативна память Corsair DDR5 5200 MHz Vengeance 96 GB (2 плашки)"
}
```
**Семпл #27:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/operativna-pamyat-ddr4-pc4-sodimm-16gb-2400-2666-3200mhz-ID10uiZq.html",
  "title": "Оперативна память DDR4 PC4 Sodimm 16GB,2400,2666,3200MHz"
}
```
**Семпл #28:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/operativna-pamyat-hyperx-kingston-ddr4-16gb-2x8-ID10Z2JI.html",
  "title": "Оперативна памʼять HyperX Kingston DDR4 16Gb (2x8)"
}
```
**Семпл #29:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Оперативна память Kingston DDR3 2GB 1333MHz",
  "item_type": "ram"
}
```
**Семпл #30:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Gskill Trident z 32 gb 3200mhz",
  "item_type": "ram"
}
```
**Семпл #31:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Оперативная память к ПК ddr 512mb, ddr2 512mb в рабочем состоянии",
  "item_type": "ram"
}
```
**Семпл #32:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/prodam-operativnu-pamyat-32gb-ddr4-termnovo-ID10YlHe.html",
  "title": "Продам оперативну пам’ять 32gb ddr4! Терміново!"
}
```
**Семпл #33:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "DDR1 512 Mb 256 Mb робоча ціна за дві",
  "item_type": "ram"
}
```
**Семпл #34:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/komplekt-mini-itx-intel-core-i5-14500-asus-prime-h610i-plus-d4-lga1700-ID10qlUp.html",
  "title": "Комплект Mini-ITX: Intel Core i5-14500 + ASUS Prime H610I-PLUS D4 (LGA1700)"
}
```
**Семпл #35:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/modul-pamyat-kingston-ddr3-16gb-4x4gb-hyperx-genesis-navi-edition-1600mhz-b-v-ID10Z2f5.html",
  "title": "Модуль памяті Kingston DDR3 16Gb (4x4gb) HyperX Genesis NaVi Edition 1600MHz Б/в"
}
```
**Семпл #36:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Оперативна памʼять DDR2",
  "item_type": "ram"
}
```
**Семпл #37:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/hyperx-ddr4-16gb-3200mhz-cl16-operativna-pamyat-ID10STzh.html",
  "title": "HyperX  DDR4 16GB 3200Mhz CL16 Оперативна память"
}
```
**Семпл #38:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/serverna-operativna-pamyat-rdimm-ecc-ddr3-4-4-8-16gb-1333-2666mgts-IDYVZDZ.html",
  "title": "Серверна оперативна память RDIMM ECC DDR3/4 4/8/16Gb 1333-2666Мгц"
}
```
**Семпл #39:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Серверна память SAMSUNG DDR3 32ГБ M386B4G70DM0-YK04 4Rx4",
  "item_type": "ram"
}
```
**Семпл #40:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Оперативна память ОЗУ DDR2 2Гб (2×1Гб)",
  "item_type": "ram"
}
```
**Семпл #41:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/operativna-pamyat-kingston-ddr3-8-gb-24-gb-1600-mgts-ID10Z2b0.html",
  "title": "Оперативна память Kingston DDR3 8 ГБ (2×4 ГБ) 1600 МГц"
}
```
**Семпл #42:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Оперативка, оперативная память DDR2 -4гб.",
  "item_type": "ram"
}
```
**Семпл #43:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/pamyat-dlya-noutbuka-crucial-96-gb-2x48gb-so-dimm-ddr5-5600-mhz-ct2k48g56c46s5-ID10TVjy.html",
  "title": "Память для ноутбука Crucial 96 GB (2x48GB) SO-DIMM DDR5 5600 MHz (CT2K48G56C46S5)"
}
```
**Семпл #44:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Оперативна память 1gb ddr2",
  "item_type": "ram"
}
```
**Семпл #45:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/crucial-ram-ddr5-pro-64-gb-2-x-32-gb-ID10Sd0o.html",
  "title": "Crucial RAM DDR5 Pro 64 gb (2 x 32 gb)"
}
```
**Семпл #46:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/ozp-kingston-ddr4-16gb-2x8gb-3600mhz-fury-beast-black-ID10Z1QU.html",
  "title": "ОЗП Kingston DDR4 16GB (2x8GB) 3600Mhz FURY Beast Black"
}
```
**Семпл #47:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Оперативна память ддр3 8гб пк",
  "item_type": "ram"
}
```
**Семпл #48:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/operativka-operativnaya-pamyat-ddr4-4gb-IDZRnxe.html",
  "title": "Оперативка, оперативная память ddr4-4гб."
}
```
**Семпл #49:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/kingston-fury-beast-ddr5-64gb-2x32gb-5600mhz-black-ID10VLeP.html",
  "title": "Kingston Fury Beast DDR5 64GB (2x32GB) 5600MHz Black"
}
```
**Семпл #50:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Комплект OEM ОЗУ 8 GB PC5 - 5600 для ноутбука",
  "item_type": "ram"
}
```
**Семпл #51:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/ddr4-32gb-2x16gb-3200mhz-IDZBYWJ.html",
  "title": "Ddr4 32gb 2x16gb 3200mhz"
}
```
**Семпл #52:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/ozu-corsair-ddr5-32gb-2x16gb-6000mhz-vengeance-rgb-black-ID10Xzrs.html",
  "title": "ОЗУ Corsair DDR5 32GB (2x16GB) 6000Mhz Vengeance RGB Black"
}
```
**Семпл #53:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/operativna-pamyat-kinqson-ddr3-4gb-1600mhz-sl9-IDVaUDG.html",
  "title": "Оперативна память Kinqson DDR3 4Gb 1600MHz  SL9"
}
```
**Семпл #54:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/nova-operativna-pamyat-ddr5-so-dimm-8gb-kingston-fury-impact-4800mhz-ID10NxFr.html",
  "title": "Нова оперативна память DDR5 SO-DIMM 8GB Kingston FURY Impact 4800MHz"
}
```
**Семпл #55:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Оперативна память для ноутбука, Samsung DDR 4, 4gb",
  "item_type": "ram"
}
```
**Семпл #56:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/pamyat-ddr4-16gb-kit-2x8gb-3000mhz-cl16-hp-v8-rgb-trade-in-ID10I10R.html",
  "title": "память DDR4 16GB Kit 2x8GB 3000MHz CL16 HP v8 RGB. Trade-in"
}
```
**Семпл #57:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/pamyat-ddr4-16gb-kit-2x8-3200mhz-goodram-afox-trade-in-IDZzFHN.html",
  "title": "память DDR4 16GB Kit (2x8) 3200MHz GOODRAM \\ AFOX. Trade-in"
}
```
**Семпл #58:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "DDR1 4GB  pc3200.  ддр1  4гб  400mhz",
  "item_type": "ram"
}
```
**Семпл #59:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/prodayu-operativku-ta-ssd-ddr4-16gb-8gb-ssd-sata-m-2-IDZNEbM.html",
  "title": "Продаю оперативку та SSD: , DDR4 16GB-8GB, SSD SATA - M.2"
}
```
**Семпл #60:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Продам DDR3 2gb 1333",
  "item_type": "ram"
}
```
**Семпл #61:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/ddr5-micron-4800-16gb-ID10Nxhc.html",
  "title": "Ddr5 micron 4800 16gb"
}
```
**Семпл #62:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/g-skill-trident-z-rgb-ddr4-32gb-128gb-3200-mhz-samsung-b-die-ID10yK6J.html",
  "title": "G.Skill Trident Z RGB DDR4 32GB-128GB 3200 MHz Samsung B-die."
}
```
**Семпл #63:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Samsung модуль оперативної памяті 1gb",
  "item_type": "ram"
}
```
**Семпл #64:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/operativnaya-pamyat-ddr3-4gb-1333mhz-pc3-10600-dlya-pk-IDZOFJe.html",
  "title": "Оперативная память DDR3 4GB 1333MHz (PC3-10600) для ПК"
}
```
**Семпл #65:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Оперативная память Ddr 4, 16 gb, Kingston.",
  "item_type": "ram"
}
```
**Семпл #66:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/ddr3-4-gb-pc3-8500-1066-mhz-2sht-h-2gb-intel-core-i3-370m-IDZhU9g.html",
  "title": "DDR3 4 Gb PC3-8500 1066 Mhz (2шт х 2gb) + Intel Core i3-370m"
}
```
**Семпл #67:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/64-gb-ddr4-4000-mhz-cl-18-22-22-42-g-skill-ripjawsv-ID10RIOS.html",
  "title": "64 GB DDR4 4000 mhz cl 18/22/22/42  G.SKILL RipjawsV"
}
```
**Семпл #68:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "жорсткий диск Western Digital Purple обємом 6 ТБ",
  "item_type": "ram"
}
```
**Семпл #69:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "(Ціна за всі)Планки оперативної памяті",
  "item_type": "ram"
}
```
**Семпл #70:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/operativna-pamyat-ddr3-4-gb-1600-IDV8I8Y.html",
  "title": "Оперативна память DDR3 4 GB 1600"
}
```
**Семпл #71:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/operativnaya-pamyat-geil-2x4-gb-2400-ddr4-ID10Z0CL.html",
  "title": "Оперативная память Geil 2x4 GB 2400 DDR4"
}
```
**Семпл #72:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/prodam-komplekt-operativno-pamyat-ddr4-netac-32-gb-2x16-gb-3200-mhz-ID10Z0Cl.html",
  "title": "Продам комплект оперативної памяті DDR4 Netac 32 GB (2x16 GB) 3200 MHz"
}
```
**Семпл #73:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/operativna-pamyat-dlya-serverv-hynix-reg-32-gb-ddr4-2933-mhz-ID10KNvn.html",
  "title": "Оперативна память для серверів hynix REG 32 GB DDR4 2933 MHz"
}
```
**Семпл #74:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/ryzen-5-1600-6-yad-kuler-amd-8gb-ddr4-kingston-hyperx-fury-korpus-ID100PFv.html",
  "title": "Ryzen 5 1600 6 яд + кулер AMD + 8GB DDR4 Kingston HyperX Fury + корпус"
}
```
**Семпл #75:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "оперативна память 1gb DDR2 800MHz PC2-6400 універсальна бу",
  "item_type": "ram"
}
```
**Семпл #76:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/operativna-pamyat-dlya-pk-4gb-ddr3-pc3-12800-1600mhz-bu-intel-amd-IDExmLI.html",
  "title": "Оперативна память для ПК 4Gb DDR3 PC3 12800 1600MHz бу intel amd"
}
```
**Семпл #77:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/modul-pamyat-kingston-hyperx-fury-white-ddr3-1866mhz-16gb-kit-2x8gb-xmp-hx318c10fwk2-16-ID10Z0uB.html",
  "title": "Модуль памяті KINGSTON HyperX Fury White DDR3 1866MHz 16GB kit 2x8Gb XMP (HX318C10FWK2/16)"
}
```
**Семпл #78:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/operativna-pamyat-ddr3-16gb-ID10Z0oD.html",
  "title": "Оперативна память DDR3 16GB"
}
```
**Семпл #79:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/operativna-pamyat-kingston-hyperx-predator-ddr3-2x4gb-1600mhz-cl9-IDXP9sI.html",
  "title": "Oперативна память Kingston HyperX Predator DDR3 2x4GB 1600MHz CL9"
}
```
**Семпл #80:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Оперативна память ddr2- 2gb hynix",
  "item_type": "ram"
}
```
**Семпл #81:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/operativna-pamyat-ddr5-5600-16gb-kingston-fury-ID10Z01P.html",
  "title": "Оперативна память ddr5 5600 16gb Kingston Fury"
}
```
**Семпл #82:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Комплект оперативной памяти DDR2 8GB (набор 5 шт.)",
  "item_type": "ram"
}
```
**Семпл #83:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/operativna-pamyat-ddr3-4gb-1333mhz-goodram-gr1333d364l9s-4g-ID10YZW2.html",
  "title": "Оперативна память DDR3 4GB 1333MHz GoodRAM (GR1333D364L9S/4G)"
}
```
**Семпл #84:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/grova-operativna-pamyat-u-radatorah-ddr3-4-2-4-8-16gb-1333-3200mhz-IDZcpEO.html",
  "title": "Ігрова оперативна память у радіаторах DDR3/4 2/4/8/16гб 1333-3200MHz"
}
```
**Семпл #85:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/operativna-pamyat-ddr4-32-gb2x16-3200mhz-netac-ID10VEqd.html",
  "title": "Оперативна память DDR4 32 Gb(2x16) 3200Mhz Netac"
}
```
**Семпл #86:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Два модулі DDR3 2Gb для ноутбука (pc3-10600s-9-10)",
  "item_type": "ram"
}
```
**Семпл #87:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Оперативні памяті 512мв, 1гб, 2гб, 8гб",
  "item_type": "ram"
}
```
**Семпл #88:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/ddr4-4gb-2133-2400-2666-amd-radeon-samsung-kingston-micron-hynix-IDXucWq.html",
  "title": "DDR4 4Gb 2133 2400 2666 AMD RADEON  Samsung  Kingston  Micron  Hynix"
}
```
**Семпл #89:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "1 плашка Оперативная память 1GB DDR2 Hunix 1Rx8 PC2-6400U-666-12-ZZ",
  "item_type": "ram"
}
```
**Семпл #90:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/lenovo-think-life-st-800-512gb-noviy-zapakovaniy-IDZj1e1.html",
  "title": "Lenovo Think Life ST 800 512GB. \r\nНовий запакований."
}
```
**Семпл #91:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/ddr4-serverna-8-16-32-64gb-ID10e3cI.html",
  "title": "DDR4 серверна  8,16,32,64Gb"
}
```
**Семпл #92:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/hyperx-16-gb-2x8gb-ddr3-IDSfrml.html",
  "title": "HyperX 16 GB (2x8GB) DDR3"
}
```
**Семпл #93:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Продам оперативную память",
  "item_type": "ram"
}
```
**Семпл #94:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/operativna-pamyat-amd-radeon-entertainment-series-ddr3-4gb-1600mhz-cl11-ID10YZk8.html",
  "title": "Оперативна память AMD Radeon Entertainment Series DDR3 4GB 1600MHz CL11"
}
```
**Семпл #95:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/grova-operativka-dvorangova-z-rozgonom-ta-radatorom-ddr3-g-skil-8gb-4gb-4gb-ID10A5eF.html",
  "title": "Ігрова Оперативка дворангова з розгоном,та радіатором DDR3 G-Skil 8Gb (4gb +4Гб)"
}
```
**Семпл #96:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Samsung 8x2GB DDR4 3200MHz SO-DIMM",
  "item_type": "ram"
}
```
**Семпл #97:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Оперативная память Kingston Fury DDR4-3600",
  "item_type": "ram"
}
```
**Семпл #98:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/apacer-blade-8gb-ddr4-ID10V6Np.html",
  "title": "Apacer blade 8gb ddr4"
}
```
**Семпл #99:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/ddr3-2x4gb-1600-mikron-ID10YZ9Z.html",
  "title": "Ddr3-2x4gb. 1600 Mikron"
}
```
**Семпл #100:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Оперативна память ELPIDA 2GB 2RX8 PC3-10600S-9",
  "item_type": "ram"
}
```

#### 📦 Комплекти (Bundles) — Відсіяно (Показано 0 з max 100):
_Жодного відсіяного оголошення в цій категорії._

### 🎯 Успішно розпізнані моделі заліза (по 40 прикладів для кожної категорії):
#### 🎮 Відеокарти (GPU) — Розпізнано (Показано 3 з max 40):
**Зразок #1:**
```json
{
  "raw_title": "Gtx 1060 3-6gb читайте опис",
  "matched_target": "gtx_1060_6gb",
  "item_type": "gpu",
  "detected_socket": null,
  "has_defects": false,
  "price_uah": 2500
}
```
**Зразок #2:**
```json
{
  "raw_title": "Видеокарта Gigabyte Geforce gt710 2gb",
  "matched_target": "gt_710",
  "item_type": "gpu",
  "detected_socket": null,
  "has_defects": false,
  "price_uah": 700
}
```
**Зразок #3:**
```json
{
  "raw_title": "Ігровий комплект плата Asrock+ Intel 10105F+8Gb DDR4 3200",
  "matched_target": "ram_ddr4_8gb",
  "item_type": "gpu",
  "detected_socket": null,
  "has_defects": false,
  "price_uah": 6000
}
```

#### 🧠 Процесори (CPU) — Розпізнано (Показано 5 з max 40):
**Зразок #1:**
```json
{
  "raw_title": "Процессор Intel Celeron G3930 2.9GHz, s1151",
  "matched_target": "celeron_g3930",
  "item_type": "cpu",
  "detected_socket": null,
  "has_defects": false,
  "price_uah": 300
}
```
**Зразок #2:**
```json
{
  "raw_title": "Новий Intel Core I5 12400  з кулером ( 6 ядер , з вбудованим  відео) SRL5Y / НА ГАРАНТІЇ",
  "matched_target": "i5_12400",
  "item_type": "cpu",
  "detected_socket": null,
  "has_defects": false,
  "price_uah": 7500
}
```
**Зразок #3:**
```json
{
  "raw_title": "Процесори Intel Xeon E5-2680 v4 / Intel Xeon E5 2697A v4 / Intel Xeon E5-2697 v3 / Intel Core i5-10400F",
  "matched_target": "i5_10400f",
  "item_type": "cpu",
  "detected_socket": "lga2011",
  "has_defects": false,
  "price_uah": 1000
}
```
**Зразок #4:**
```json
{
  "raw_title": "Intel core i3 2120 lga1155",
  "matched_target": "i3_2120",
  "item_type": "cpu",
  "detected_socket": "lga1155",
  "has_defects": false,
  "price_uah": 150
}
```
**Зразок #5:**
```json
{
  "raw_title": "Процесор Intel Core i3-10105T (6M Cache, up to 3.80 GHz) s1200 Tray",
  "matched_target": "i3_10105t",
  "item_type": "cpu",
  "detected_socket": "lga1200",
  "has_defects": false,
  "price_uah": 2100
}
```

#### 🔌 Материнські плати (Motherboard) — Розпізнано (Показано 4 з max 40):
**Зразок #1:**
```json
{
  "raw_title": "Intel i7-6700 4.0ghz/16gb ddr4/Материнка Мощний комплект для ПК",
  "matched_target": "i7_6700",
  "item_type": "motherboard",
  "detected_socket": null,
  "has_defects": false,
  "price_uah": 6500
}
```
**Зразок #2:**
```json
{
  "raw_title": "Intel i7-860 3.46Ghz/16gb память/материнка Комплект 4ядра 8потоків для ПК",
  "matched_target": "i7_860",
  "item_type": "motherboard",
  "detected_socket": null,
  "has_defects": false,
  "price_uah": 2600
}
```
**Зразок #3:**
```json
{
  "raw_title": "Материнська плата B650 GAMING PLUS WIFI",
  "matched_target": "b650",
  "item_type": "motherboard",
  "detected_socket": "am5",
  "has_defects": false,
  "price_uah": 5000
}
```
**Зразок #4:**
```json
{
  "raw_title": "Материнская плата Asus STRIX X870-A Gaming WiFi (AM5)",
  "matched_target": "x870",
  "item_type": "motherboard",
  "detected_socket": "am5",
  "has_defects": false,
  "price_uah": 10500
}
```

#### ⚡ Блоки живлення (PSU) — Розпізнано (Показано 1 з max 40):
**Зразок #1:**
```json
{
  "raw_title": "Блок живлення Seasonic Focus GX-650 650W (SSR-650FX) - 3743",
  "matched_target": "650w",
  "item_type": "psu",
  "detected_socket": null,
  "has_defects": false,
  "price_uah": 1950
}
```

#### 💾 Накопичувачі (SSD / HDD) — Розпізнано (Показано 2 з max 40):
**Зразок #1:**
```json
{
  "raw_title": "Жорсткий диск 3.5\" 1TB WD (WD10EZRZ)",
  "matched_target": "hdd_1tb",
  "item_type": "storage",
  "detected_socket": null,
  "has_defects": false,
  "price_uah": 2100
}
```
**Зразок #2:**
```json
{
  "raw_title": "QNAP UX-800U-RP 8-Bay SAS Storage Expansion 52TB (6×8TB + 2×2TB) Enterprise",
  "matched_target": "ssd_8tb",
  "item_type": "storage",
  "detected_socket": null,
  "has_defects": false,
  "price_uah": 30000
}
```

#### 📟 Оперативна пам'ять (RAM) — Розпізнано (Показано 22 з max 40):
**Зразок #1:**
```json
{
  "raw_title": "Серверная оперативная память DDR4 64Gb 2400Mhz",
  "matched_target": "ssd_64gb",
  "item_type": "ram",
  "detected_socket": null,
  "has_defects": false,
  "price_uah": 5800
}
```
**Зразок #2:**
```json
{
  "raw_title": "Оперативная память kingston fury  beast  2x32 gb (64gb)",
  "matched_target": "ssd_64gb",
  "item_type": "ram",
  "detected_socket": null,
  "has_defects": false,
  "price_uah": 20000
}
```
**Зразок #3:**
```json
{
  "raw_title": "Память HyperX FURY 16 GB KIT (2x8GB) DDR3 1333 1600 1866 MHz",
  "matched_target": "ram_ddr3_16gb",
  "item_type": "ram",
  "detected_socket": null,
  "has_defects": false,
  "price_uah": 3200
}
```
**Зразок #4:**
```json
{
  "raw_title": "DDR3 8GB SDRAM Samsung, Kingston, hynix",
  "matched_target": "ram_ddr3_8gb",
  "item_type": "ram",
  "detected_socket": null,
  "has_defects": false,
  "price_uah": 650
}
```
**Зразок #5:**
```json
{
  "raw_title": "Фірмова память ОЗУ RAM Memory SO-DIMM DDR4  PC-2400  2666 16GB 32ГБ",
  "matched_target": "ram_ddr4_16gb",
  "item_type": "ram",
  "detected_socket": null,
  "has_defects": false,
  "price_uah": 2390
}
```
**Зразок #6:**
```json
{
  "raw_title": "Kingston DDR4 16GB 3200Mhz CL22 SO-DIMM Оперативна память",
  "matched_target": "ram_ddr4_16gb",
  "item_type": "ram",
  "detected_socket": null,
  "has_defects": false,
  "price_uah": 2700
}
```
**Зразок #7:**
```json
{
  "raw_title": "ОЗУ HyperX DDR4 32gb (2x16)  3200MHz (Модулі оперативної памʼяті Kingston)",
  "matched_target": "ram_ddr4_32gb",
  "item_type": "ram",
  "detected_socket": null,
  "has_defects": false,
  "price_uah": 8200
}
```
**Зразок #8:**
```json
{
  "raw_title": "Crucial Ballistix RGB 16GB (2х8) 3200Mhz CL16  DDR4 Оперативна память",
  "matched_target": "ram_ddr4_16gb",
  "item_type": "ram",
  "detected_socket": null,
  "has_defects": false,
  "price_uah": 4300
}
```
**Зразок #9:**
```json
{
  "raw_title": "DDR3 4GB Hynix, Kingston, Samsung SO-DIMM 1866 1600 1333 1066 MHz",
  "matched_target": "ram_ddr3_4gb",
  "item_type": "ram",
  "detected_socket": null,
  "has_defects": false,
  "price_uah": 300
}
```
**Зразок #10:**
```json
{
  "raw_title": "DDR4 Teamgroup 16GB [8+8] 2666Mhz",
  "matched_target": "ram_ddr4_16gb",
  "item_type": "ram",
  "detected_socket": null,
  "has_defects": false,
  "price_uah": 3790
}
```
**Зразок #11:**
```json
{
  "raw_title": "Оперативная память Netac DDR4 32gb(2x16)",
  "matched_target": "ram_ddr4_32gb",
  "item_type": "ram",
  "detected_socket": null,
  "has_defects": false,
  "price_uah": 6850
}
```
**Зразок #12:**
```json
{
  "raw_title": "Оперативна память SO-DIMM DDR5 4800MHz 2x8GB (16GB)",
  "matched_target": "ram_ddr5_16gb",
  "item_type": "ram",
  "detected_socket": null,
  "has_defects": false,
  "price_uah": 6000
}
```
**Зразок #13:**
```json
{
  "raw_title": "Оперативна памʼять DDR3 8Gb",
  "matched_target": "ram_ddr3_8gb",
  "item_type": "ram",
  "detected_socket": null,
  "has_defects": false,
  "price_uah": 460
}
```
**Зразок #14:**
```json
{
  "raw_title": "Ssd m2 Kingston NV2 2Tb (відклеїв наліпку)",
  "matched_target": "ssd_2tb",
  "item_type": "ram",
  "detected_socket": null,
  "has_defects": false,
  "price_uah": 7999
}
```
**Зразок #15:**
```json
{
  "raw_title": "Оперативна память Kingston FURY Beast DDR5 64GB (2×32GB) 6000 MHz CL36 EXPO/XMP (KF560C36BBEK2-64)",
  "matched_target": "ssd_64gb",
  "item_type": "ram",
  "detected_socket": null,
  "has_defects": false,
  "price_uah": 44000
}
```
**Зразок #16:**
```json
{
  "raw_title": "DDR3 8GB (2x4GB) 1600MHz G.Skill RipjawsX CL8",
  "matched_target": "ram_ddr3_8gb",
  "item_type": "ram",
  "detected_socket": null,
  "has_defects": true,
  "price_uah": 531
}
```
**Зразок #17:**
```json
{
  "raw_title": "96GB DDR5 G.Skill Flare X5 (48x2) | CL40-40-40-89 | декілька сотень годин напрацювання",
  "matched_target": "ram_ddr5_96gb",
  "item_type": "ram",
  "detected_socket": null,
  "has_defects": false,
  "price_uah": 46999
}
```
**Зразок #18:**
```json
{
  "raw_title": "ГАРАНТІЯ | Оперативна память DDR5 32GB (2x16GB) 6000/CL30 ACER HT200 (HT200-32GB-6000-2R8-V2)",
  "matched_target": "ram_ddr5_32gb",
  "item_type": "ram",
  "detected_socket": null,
  "has_defects": false,
  "price_uah": 22699
}
```
**Зразок #19:**
```json
{
  "raw_title": "Модуль пам`ятi DDR5 2x32GB/6000 G.Skill Trident Z5 RGB",
  "matched_target": "ram_ddr5_64gb",
  "item_type": "ram",
  "detected_socket": null,
  "has_defects": false,
  "price_uah": 40000
}
```
**Зразок #20:**
```json
{
  "raw_title": "Оперативна памʼять kingston fury 16 gb 4800 ddr5",
  "matched_target": "ram_ddr5_16gb",
  "item_type": "ram",
  "detected_socket": null,
  "has_defects": false,
  "price_uah": 5200
}
```
**Зразок #21:**
```json
{
  "raw_title": "DDR1, DDR2, DDR3 оперативная память (1gb, 2gb, 4gb, 8gb)",
  "matched_target": "ram_ddr3_4gb",
  "item_type": "ram",
  "detected_socket": null,
  "has_defects": false,
  "price_uah": 49
}
```
**Зразок #22:**
```json
{
  "raw_title": "SSD Samsung 1TB PCle 5.0 PM9E1, OEM version Samsung 9100 pro",
  "matched_target": "ssd_1tb",
  "item_type": "ram",
  "detected_socket": null,
  "has_defects": false,
  "price_uah": 7199
}
```

#### 📦 Комплекти (Bundles) — Розпізнано (Показано 0 з max 40):
_Жодного оголошення з цієї категорії не розпізнано під час запуску._

============================================================

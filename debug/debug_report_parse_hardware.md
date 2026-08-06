# 🐛 ДЕБАГ-ЗВІТ ПАРСИНГУ КОМПЛЕКТУЮЧИХ OLX (GraphQL)
**Дата та час запуску:** 2026-08-07 00:16:05
**Тривалість виконання:** 497.34 сек
**Шлях до звіту:** `C:\Users\marke\OneDrive\Desktop\Operating_System\debug\debug_report_parse_hardware.md`

## 📌 1. Задача та мета коду
Основна мета: асинхронний збір свіжих оголошень комплектуючих з OLX (GraphQL API).

## 📊 2. Загальна статистика вхідних даних та відсіювання
### ⚙️ Секція: Supabase_Input
- **Завантажено URLs для дедуплікації:** 52197

### ⚙️ Секція: Parser_Config
- **Цільових моделей комплектуючих:** 37079

### ⚙️ Секція: OLX_GraphQL
- **Отримано [videokarty]:** 520
- **Отримано [protsessory]:** 520
- **Отримано [materinskie-platy]:** 520
- **Отримано [bloki-pitaniya]:** 517
- **Отримано [zhestkie-diski]:** 520
- **Отримано [moduli-pamyati]:** 516

### ⚙️ Секція: Parsing_Metrics
- **Успішно розпізнано [gpu]:** 82
- **Успішно розпізнано [cpu]:** 62
- **Успішно розпізнано [motherboard]:** 59
- **Успішно розпізнано [psu]:** 44
- **Успішно розпізнано [storage]:** 96
- **Успішно розпізнано [ram]:** 76

### ⚙️ Секція: Filtering_Rules
- **Відсіяно (Не розпізнано модель):** 1152

### ⚙️ Секція: Summary
- **Знайдено нових унікальних оголошень:** 419
- **Немає нових оголошень для відправки в DB:** 1

### ⚙️ Секція: Supabase_Output
- **Успішно збережено в DB:** 419

### ⚙️ Секція: WebSocket
- **Успішно надіслано тригер стріму:** 6

## 🔄 3. Детальні приклади даних
### 🚫 Відсіяні оголошення:
#### 🎮 Відеокарти (GPU) — Відсіяно (100):
**Семпл #1:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/holodnaya-ta-tiha-manli-gaming-rtx-3080-ti-12-gb-gddr-6-x-384-bit-magazin-compic-ID10RWv3.html",
  "title": "Холодная та тиха Manli Gaming RTX 3080 Ti 12 Gb GDDR-6 X 384 Bit магазин CompiC"
}
```
**Семпл #2:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/vdeokarta-zotac-geforce-rtx-5080-solid-core-16gb-gddr7-dlss4-magazin-compic-ID10FmyV.html",
  "title": "Відеокарта Zotac GeForce RTX 5080 Solid Core 16GB GDDR7 DLSS4 Магазин CompiC"
}
```
**Семпл #3:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Видеокарта MSI GeForce RTX 4060Ti, 8gb ( Не рабочая )"
}
```
**Семпл #4:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Видеокарта,GTX 1060,6GB,MSI OC1"
}
```
**Семпл #5:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Відеокарта Gt 1060 3gb"
}
```
**Семпл #6:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/amd-radeon-rx-5600-6gb-nova-videokarta-ID10WGvJ.html",
  "title": "AMD Radeon RX 5600 6GB НОВА видеокарта"
}
```
**Семпл #7:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Відеокарта ASUS Dual RTX 5060 Ti OC 8GB GDDR7 — гарантія"
}
```
**Семпл #8:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/msi-geforce-gtx-1080-gaming-z-8gb-ID10ZgXO.html",
  "title": "MSI GeForce GTX 1080 Gaming Z 8GB"
}
```
**Семпл #9:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "R9 Fury x 4gb водяне охолодження"
}
```
**Семпл #10:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Відеокарта рх 580 8г"
}
```
**Семпл #11:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/gtx-650-ti-videokarta-ID10F2jR.html",
  "title": "GTX 650 TI Видеокарта"
}
```
**Семпл #12:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Продам відеокарту asus r9270x - DC2T - 2GD5"
}
```
**Семпл #13:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/videokarta-rx-470-4-gb-powercolor-IDQ37Va.html",
  "title": "Видеокарта RX 470 4 GB PowerColor"
}
```
**Семпл #14:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/videokarta-rtx-4090-24-gb-msi-ID10ZV1c.html",
  "title": "Видеокарта Rtx 4090 24 gb msi"
}
```
**Семпл #15:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/vdeokarta-top-versya-rtx3090ti-24gb-msi-suprim-dealniy-stan-plomba-trade-in-ID10XiCJ.html",
  "title": "відеокарта ТОП версія RTX3090Ti 24GB MSI Suprim ідеальний стан. Пломба. Trade-IN"
}
```
**Семпл #16:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/sapphire-vega-56-pulse-8gb-ID110GiI.html",
  "title": "Sapphire Vega 56 pulse 8gb"
}
```
**Семпл #17:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Palit GTX 1060 StormX 3gb"
}
```
**Семпл #18:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/ventilyatori-asus-rog-strix-tuf-t129215su-20-60-70-80-3070-3080-3090-IDTQGpV.html",
  "title": "Вeнтилятори ASUS ROG/STRIX/TUF T129215SU 20 60/70/80 3070/3080/3090"
}
```
**Семпл #19:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/vdeokarta-rx-470-4gb-v-dealnomu-stan-IDZJSK7.html",
  "title": "відеокарта Rx 470 4gb в ідеальному стані"
}
```
**Семпл #20:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/videokarta-asus-rtx-5070-ID10ZWKf.html",
  "title": "Видеокарта Asus RTX 5070"
}
```
**Семпл #21:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/vdeokarta-radeon-r9-290-4gb-IDRJ7nK.html",
  "title": "Відеокарта \"Radeon R9 290\" 4gb"
}
```
**Семпл #22:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/rx-570-4gb-gigabite-gaming-ID110Gay.html",
  "title": "RX 570 4GB GIGABITE gaming"
}
```
**Семпл #23:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/vdeokarta-sapphire-amd-radeon-hd-6750-1gb-gddr5-ID110Ga4.html",
  "title": "Відеокарта Sapphire AMD Radeon HD 6750 1GB GDDR5"
}
```
**Семпл #24:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/nvidia-p106-100-6gb-analog-gtx-1060-6gb-otlichnoe-sostoyanie-ID110G8m.html",
  "title": "NVIDIA P106-100 6GB (аналог GTX 1060 6GB) | Отличное состояние"
}
```
**Семпл #25:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/vdeokarta-asus-geforce-gtx-550-ti-1024mb-gddr5-IDY44ZM.html",
  "title": "Відеокарта ASUS GeForce GTX 550 Ti 1024MB GDDR5"
}
```
**Семпл #26:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Відеокарточка agp 32-128 mb."
}
```
**Семпл #27:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/videokarta-nvidia-palit-gaming-pro-gtx-1650-4gb-IDZF0up.html",
  "title": "Видеокарта NVIDIA Palit GAMING PRO GTX 1650 4Gb"
}
```
**Семпл #28:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/prodam-vdeokartu-rx-550-4gb-ID110G2t.html",
  "title": "Продам відеокарту rx 550 4gb"
}
```
**Семпл #29:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/vdeokarta-msi-rx-470-8gb-garantya-velika-klkst-IDQwfj2.html",
  "title": "Відеокарта MSI RX 470 8Gb Гарантія! Велика кількість!"
}
```
**Семпл #30:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/vdeokarta-asrock-rx-7600-challenger-oc-edition-8gb-gddr6-magazin-compic-ID10VwcP.html",
  "title": "Відеокарта ASRock RX 7600 Challenger OC Edition 8GB GDDR6 Магазин CompiC"
}
```
**Семпл #31:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Asus PCI-Ex GeForce 210 512MB"
}
```
**Семпл #32:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Видеокарта Видеокарта NVIDIA Gigabyte Mini ITX GTX 1060 3Gb"
}
```
**Семпл #33:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/vdeokarta-sapphire-radeon-rx-580-8-gb-gddr5-ID110FWd.html",
  "title": "Відеокарта Sapphire Radeon RX 580 8 GB GDDR5"
}
```
**Семпл #34:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/prodam-rtx-3050-6gb-ID110FUn.html",
  "title": "Продам rtx 3050 6gb"
}
```
**Семпл #35:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/grova-vdeokarta-rtx3070-8gb-256bit-msi-ventus-3x-oc-trade-in-ID110FQS.html",
  "title": "ігрова відеокарта RTX3070 8GB 256bit MSI Ventus 3X OC. Trade-IN"
}
```
**Семпл #36:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/vdeokarta-rtx-4060-palit-dual-8gb-ID110FQf.html",
  "title": "Відеокарта RTX 4060 Palit Dual 8gb"
}
```
**Семпл #37:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/vdeokarta-nvidia-asus-tuf-rtx-3070-8gb-ID10UJZN.html",
  "title": "Відеокарта nvidia asus tuf rtx 3070 8gb"
}
```
**Семпл #38:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/grova-vdeokarta-top-versya-rtx4080-16gb-asus-tuf-gaming-trade-in-IDZQgzp.html",
  "title": "ігрова відеокарта ТОП версія RTX4080 16GB ASUS TUF Gaming. Trade-IN"
}
```
**Семпл #39:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Видиокарта.. на 1 г"
}
```
**Семпл #40:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/videokarta-amd-sapphire-hd-7750-1gb-IDZQ3yi.html",
  "title": "Видеокарта AMD Sapphire HD 7750 1Gb"
}
```
**Семпл #41:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/luchshaya-rtx-4090-asus-rog-strix-nvidia-pci-ex-geforce-24gb-ID10PVNZ.html",
  "title": "Лучшая RTX 4090 ASUS ROG Strix NVIDIA PCI-Ex GeForce 24Gb"
}
```
**Семпл #42:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Radeon VII pro 16 gb"
}
```
**Семпл #43:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/holodna-msi-geforce-gtx-1080-sea-hawk-x-z-vodyanim-oholodzhennyam-ID10t6q1.html",
  "title": "Холодна Msi GeForce GTX 1080 SEA HAWK X з Водяним Охолодженням"
}
```
**Семпл #44:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "R9 270x 2gb ddr5"
}
```
**Семпл #45:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Несправна 1660s strix"
}
```
**Семпл #46:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/msi-rtx-3060-ti-ventus-2x-ID10YqP0.html",
  "title": "Msi rtx 3060 ti ventus 2x"
}
```
**Семпл #47:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Раритет Рабочая Видеокарта, Звуковая, плата видеозахвата ISA PCI AGP , процессор"
}
```
**Семпл #48:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/vdeokarta-gigabyte-pci-ex-radeon-rx-580-gaming-8gb-gddr-ID110FI5.html",
  "title": "Відеокарта Gigabyte PCI-Ex Radeon RX 580 Gaming 8GB GDDR"
}
```
**Семпл #49:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "XpertVision Geforce 8500 gt 256mb 600mhz 1200mhz ddr3 pci ex"
}
```
**Семпл #50:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/prodam-vdeo-kartu-afox-geforce-gtx-750-ti-af750ti-4096d5h1-ID10Yqam.html",
  "title": "Продам відео карту AFOX GeForce GTX 750 Ti AF750Ti-4096D5H1"
}
```
**Семпл #51:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/video-karta-gt-630-2gb-ID10PuAu.html",
  "title": "Видео карта Gt 630 2gb"
}
```
**Семпл #52:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/2080-ti-22gb-3090-24gb-IDZXzhw.html",
  "title": "2080 ti 22gb.( 3090 24gb. )"
}
```
**Семпл #53:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "ігрова відеокарта RTX3060 12GB ASUS Dual OC на пломбі. Trade-IN"
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
  "url": "https://www.olx.ua/d/uk/obyavlenie/asus-radeon-r5-230-2gb-ddr3-hdmi-vga-dvi-standart-nizkoproflna-opt-IDZWekW.html",
  "title": "ASUS Radeon R5 230 2GB DDR3 HDMI+VGA+DVI  стандарт низкопрофільна опт"
}
```
**Семпл #56:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/garantya-sapphire-rx480-8gb-vdeokarta-rx570-rx470-i-580-IDNwUGW.html",
  "title": "Гарантія. Sapphire RX480 8GB відеокарта (rx570, rx470 и 580)"
}
```
**Семпл #57:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/vdeokarta-rx570-4gb-aorus-ID10P8WB.html",
  "title": "Відеокарта RX570 4GB Aorus"
}
```
**Семпл #58:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/vdeokarta-gigabyte-rtx-3080-ti-vision-oc-12g-ID110Ft6.html",
  "title": "Відеокарта Gigabyte RTX 3080 ti vision oc 12g"
}
```
**Семпл #59:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/hp-rtx-4070-ti-oem-12-gb-ID110FqD.html",
  "title": "HP rtx 4070 ti oem 12 gb"
}
```
**Семпл #60:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "NVidia GeForce RTX 3060 Gaming OC 12GB"
}
```
**Семпл #61:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Игровая Видеокарта, r9 380x"
}
```
**Семпл #62:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/videokarta-asus-rtx-5070-ID10ZWKf.html",
  "title": "Видеокарта Asus RTX 5070"
}
```
**Семпл #63:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/vdeokarta-msi-radeon-rx-6900-xt-gaming-x-trio-16gb-ID10To7x.html",
  "title": "Відеокарта MSI Radeon RX 6900 XT Gaming X Trio 16GB"
}
```
**Семпл #64:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/videokarta-gainward-phantom-rtx-5090-ID10WAsg.html",
  "title": "Видеокарта Gainward Phantom RTX 5090"
}
```
**Семпл #65:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/karta-hp-quadro-p6000-913197-002-24gb-gddr5x-ID10Rtrq.html",
  "title": "карта HP QUADRO P6000  913197-002 24GB GDDR5X"
}
```
**Семпл #66:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/palit-geforce-gtx-1650-4gb-ID10CrWn.html",
  "title": "Palit GeForce GTX 1650 4gb"
}
```
**Семпл #67:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/vdeokarta-msi-geforce-rtx-3080-suprim-x-10gb-gddr6x-top-ID10FYet.html",
  "title": "Відеокарта MSI GeForce RTX 3080 SUPRIM X 10GB GDDR6X топ"
}
```
**Семпл #68:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Видеокарта NVIDIA MSI GAMING X GTX 1060 3Gb"
}
```
**Семпл #69:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Видеокарта GeForce RTX 3060 GAMING Z TRIO 12G"
}
```
**Семпл #70:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Відеокарта Gigabyte GeForce RTX 4060 Ti AERO OC 8192MB (GV-N406TAERO OC-8GD)"
}
```
**Семпл #71:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Відеокарта Asus  EN9800gt"
}
```
**Семпл #72:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Відеокарта MSI GeForce N9800GT Zilent, PCI-Ex16 2.0, 1 GB, GDDR3, 256bit (На Відновлення/Запчастини)"
}
```
**Семпл #73:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/vdeokarta-evga-gtx1080ti-11gb-ID10Yj5n.html",
  "title": "Відеокарта evga Gtx1080Ti 11gb"
}
```
**Семпл #74:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/videokarta-gigabyte-rtx-4090-windforce-2-ID10WAaV.html",
  "title": "Видеокарта Gigabyte Rtx 4090 Windforce 2"
}
```
**Семпл #75:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Rtx 4060 ti срочно"
}
```
**Семпл #76:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Відеокарта Sapphire nitro R9 390X"
}
```
**Семпл #77:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/prodam-geforce-rtx-5070-ti-novaya-na-garantii-ID10ZuP3.html",
  "title": "Продам  GEFORCE RTX 5070 TI (Новая на Гарантии)"
}
```
**Семпл #78:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Відеокарти Radeon X550( ddr), Radeon НD 4350(ddr2)"
}
```
**Семпл #79:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "MSI GeForce RTX 5060 Ti 8G SHADOW  (8 ГБ GDDR7)."
}
```
**Семпл #80:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/videokarta-rx-6900-xt-16-gb-ID10YaOj.html",
  "title": "Видеокарта Rx 6900 xt 16 gb"
}
```
**Семпл #81:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/vdeokarta-msi-ventus-3x-plus-geforce-rtx-3080vdeokarta-msi-geforce-rtx-3080-ven-ID10KjOz.html",
  "title": "Відеокарта MSI Ventus 3X Plus Geforce RTX 3080\nВідеокарта MSI GeForce RTX 3080 VEN"
}
```
**Семпл #82:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/vdeokarta-grova-asus-stix-gaming-rx570-4gb-potuzhna-deal-ID10Zvqu.html",
  "title": "Відеокарта ігрова Asus Stix Gaming RX570 4GB  потужна, ідеал"
}
```
**Семпл #83:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Видеокарта NVIDIA INNO3D X2 GTX 1060 3Gb"
}
```
**Семпл #84:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/msi-gtx-1080-ti-gaming-x-rtx-11-gb-garantya-ID10qGWn.html",
  "title": "Msi GTX 1080 Ti Gaming X Rtx 11-GB Гарантія"
}
```
**Семпл #85:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/videokarta-asus-geforce-rtx-4080-16gb-gddr6x-tuf-gaming-oc-tuf-rtx4080-o16g-gaming-ID10Ma1u.html",
  "title": "Видеокарта Asus GeForce RTX 4080 16GB GDDR6X (TUF GAMING OC TUF-RTX4080-O16G-GAMING)"
}
```
**Семпл #86:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/videokarta-saphire-rx-580-8-gb-magazin-compic-v-zaporozhe-1070-1080ti-IDTJbCp.html",
  "title": "Видеокарта Saphire Rx 580 8 Gb магазин COMPiC в Запорожье 1070 1080ti"
}
```
**Семпл #87:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Відеокарта Gigabyte RTX 4060ti"
}
```
**Семпл #88:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/vdeokarta-gigabyte-pci-ex-geforce-rtx-3080-ti-eagle-oc-12g-12-gb-gddr6x-ID10JzYB.html",
  "title": "Відеокарта Gigabyte PCI-Ex GeForce RTX 3080 Ti EAGLE OC 12G 12 GB GDDR6X"
}
```
**Семпл #89:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/vdeokarta-msi-radeon-rx-6900-xt-gaming-x-trio-16gb-ID10To7x.html",
  "title": "Відеокарта MSI Radeon RX 6900 XT Gaming X Trio 16GB"
}
```
**Семпл #90:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "MSI GTX 1060 6G Gaming X"
}
```
**Семпл #91:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "RTX 5060 ti 8G MSI gaming trio"
}
```
**Семпл #92:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/vdeokarta-gt-730-ID10n3qB.html",
  "title": "Відеокарта gt 730"
}
```
**Семпл #93:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/videokarta-rx-6800-16-gb-nuzhno-proshit-bios-ID10YRQi.html",
  "title": "Видеокарта Rx 6800 16 gb Нужно прошить биос"
}
```
**Семпл #94:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/rx-580-8gb-net-izobrazheniya-ID10Z3UN.html",
  "title": "RX 580 8GB  нет изображения"
}
```
**Семпл #95:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Asus GeForce GTX 550"
}
```
**Семпл #96:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/garantya-rtx-2060-super-8gb-inno3d-twin-x2-grova-vdeokarta-tehnobro-ID10Hr1o.html",
  "title": "Гарантія! RTX 2060 Super 8GB Inno3D Twin X2 Ігрова відеокарта ТехноБро"
}
```
**Семпл #97:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Продам видео карту  1660 msi Ventus xs oc"
}
```
**Семпл #98:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/sapphire-rx-460-2gb-povniy-komplekt-ID10P59z.html",
  "title": "Sapphire RX 460 2GB повний комплект"
}
```
**Семпл #99:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Видеокарта ASUS GeForce 8800 GS 384Mb"
}
```
**Семпл #100:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Видеокарта 512M DDR4"
}
```

#### 🧠 Процесори (CPU) — Відсіяно (100):
**Семпл #1:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/protsesor-intel-core-i5-8600k-3-6-ghz-ID10XgDv.html",
  "title": "Процесор Intel Core i5-8600K 3.6 GHz"
}
```
**Семпл #2:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Процессор AMD Athlon II x4 640 3 Ghz"
}
```
**Семпл #3:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Процесор Intel Celeron Dual-Core E3200 2.40GHz LGA775"
}
```
**Семпл #4:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Процесор lga775 e6600⁸"
}
```
**Семпл #5:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/s1700-top-set-intel-core-i9-13900k-asus-rog-strix-z790-wi-fi-trade-in-IDZKK35.html",
  "title": "s1700 ТОП сет Intel Core i9-13900K+ASUS ROG STRIX Z790 Wi-Fi. Trade-in"
}
```
**Семпл #6:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Процесор AMD Athlon ii x3 450 3.2 GHz. 3 ядра/3 потока. Soket AM3."
}
```
**Семпл #7:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/protsesor-intel-core-i5-12400f-torg-ID110Gy1.html",
  "title": "процесор intel core i5 12400f є торг"
}
```
**Семпл #8:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/am4-protsesor-amd-ryzen-5-3600x-4-4ghz-6yader-12potokv-trade-in-ID10LNVq.html",
  "title": "AM4 процесор AMD Ryzen 5 3600X 4.4GHz 6ядер\\12потоків. Trade-IN"
}
```
**Семпл #9:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/protsessor-amd-ryzen-3-1200-box-4-yadra-soket-am4-v-korobke-s-kulerom-ID10E0Pg.html",
  "title": "Процессор AMD Ryzen 3 1200 BOX (4 ядра, сокет AM4), в коробке с кулером"
}
```
**Семпл #10:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Процессор Intel Core i9-7980XE Extreme Edition 18 ядер 36 потоков s2066"
}
```
**Семпл #11:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Комплект: материнська плата, процесор, водяне охолодження"
}
```
**Семпл #12:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Процессор Athlon II  2 ядра 240-250-260-270, sAM3"
}
```
**Семпл #13:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Продам процессор G4400"
}
```
**Семпл #14:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/svzhiy-s1200-set-z-vdeo-intel-pentium-g6400-4ghz-asrock-h470-m-2-ssd-i-m-2-wi-fi-IDYSzD6.html",
  "title": "свіжий s1200 сет з відео Intel Pentium G6400 4GHz + ASRock H470 M.2 SSD i M.2 Wi-Fi"
}
```
**Семпл #15:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/protsesor-intel-core-i5-6500-s1151-IDXVxbM.html",
  "title": "Процесор Intel Core i5 6500 s1151"
}
```
**Семпл #16:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/amd-ryzen-7-7800x3d-IDYEELt.html",
  "title": "AMD Ryzen 7 7800X3D"
}
```
**Семпл #17:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/intel-xeon-e5-1607-v3-3-10ghz-lga-2011-3-IDUdQZh.html",
  "title": "Intel Xeon E5-1607 v3 3.10ghz LGA 2011-3"
}
```
**Семпл #18:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/protsesor-i7-6700-3-4ghz-4-0ghz-IDX27su.html",
  "title": "Процесор I7 6700 3.4ghz-4.0ghz"
}
```
**Семпл #19:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "AMD Ryzen 2700 Tray"
}
```
**Семпл #20:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/prodayu-protsesor-amd-ryzen-3-1200-soket-am4-povnstyu-robochiy-stabl-IDZI6Uy.html",
  "title": "Продаю процесор AMD Ryzen 3 1200 (сокет AM4).\nПовністю робочий, стабіл"
}
```
**Семпл #21:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "‼️Процесор для ноутбука Intel Pentium P6100 3 МБ кеш-памяті"
}
```
**Семпл #22:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/protsesor-intel-core-i5-7400-3-00ghz-6mb-8gt-s-sr32w-s1151-tray-ID10Y1Cr.html",
  "title": "Процесор Intel Core i5-7400 3.00GHz/6MB/8GT/s (SR32W) s1151, tray"
}
```
**Семпл #23:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "AMD Ryzen 2200G + боксовий кулер + термопаста"
}
```
**Семпл #24:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/prodam-protsesor-i5-9600k-ID10L2JL.html",
  "title": "Продам процесор i5-9600k"
}
```
**Семпл #25:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "AMD Ryzen 2700X Tray"
}
```
**Семпл #26:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/prodam-protsessor-xeon-2665-IDYF8oG.html",
  "title": "Продам процессор Xeon 2665"
}
```
**Семпл #27:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/s1700-protsesor-intel-core-i5-13600k-14yader-20potokv-5-1ggts-z-vdeoyadrom-trade-in-ID10zmgh.html",
  "title": "s1700 процесор Intel Core i5-13600K 14ядер\\20потоків 5.1ГГц з відеоядром. Trade-IN"
}
```
**Семпл #28:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Продам процесор ."
}
```
**Семпл #29:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/s1151v2-protsesor-intel-core-i5-9600k-6yader-4-6ghz-trade-in-ID10XhJt.html",
  "title": "s1151v2 процесор Intel Core i5-9600K 6ядер 4.6GHz. Trade-in"
}
```
**Семпл #30:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Продам процесор Processor Intel Core i3-2330M SR04J"
}
```
**Семпл #31:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/noviy-protsesor-amd-ryzen-7-9800x3d-IDXYPam.html",
  "title": "Новий процесор AMD Ryzen 7 9800X3D"
}
```
**Семпл #32:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/s1200-protsesor-10pokolnnya-intel-pentium-gold-g6405-4-1ggts-z-grafkoyu-IDYLSXO.html",
  "title": "s1200 процесор 10покоління Intel Pentium GOLD G6405 4.1ГГц з графікою"
}
```
**Семпл #33:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/amd-ryzen-5-7500f-ID110FGA.html",
  "title": "Amd RYZEN 5 7500f"
}
```
**Семпл #34:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/s1151-set-intel-core-i5-7500-3-8ghz-z-vdeoyadrom-atx-asus-h270-trade-in-ID10HweN.html",
  "title": "s1151 сет Intel Core i5-7500 3.8GHz з відеоядром + ATX ASUS H270. Trade-IN"
}
```
**Семпл #35:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/intel-core-i3-8100-lga1151-zapasn-tri-nzhki-krplennya-dlya-kulera-ID10NtXb.html",
  "title": "Intel Core i3-8100 LGA1151 + запасні три ніжки кріплення для кулера"
}
```
**Семпл #36:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/protsessor-amd-ryzen-7-8700f-ID10XOKw.html",
  "title": "Процессор AMD Ryzen 7 8700F"
}
```
**Семпл #37:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/protsesor-intel-core-i5-14400f-box-v-idealnomu-stan-ID10YQR2.html",
  "title": "Процесор Intel Core i5-14400F Box в идеальному стані"
}
```
**Семпл #38:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/protsessor-intel-core-i3-14100-lga1700-ID108Gcc.html",
  "title": "Процессор Intel Core i3-14100 LGA1700"
}
```
**Семпл #39:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "AMD Sempron 2800+ АМ2 + BOX кулер"
}
```
**Семпл #40:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/ryzen-9-7900x-asrock-b650-pg-lightning-ID10OTU5.html",
  "title": "Ryzen 9 7900X і Asrock B650 PG LIGHTNING"
}
```
**Семпл #41:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Процесор Thesys Z80H для ZX Spectrum і не тільки, КР580ВМ80А"
}
```
**Семпл #42:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/protsesor-intel-xeon-e5-2699-v3-2-3-3-6-ghz-18yad-36pot-e5-2699v3-IDY43Be.html",
  "title": "Процесор Intel Xeon E5 2699 V3 | 2.3-3.6 GHz | 18яд.36пот. | E5-2699v3"
}
```
**Семпл #43:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/topovyy-kuler-id-cooling-frozn-a620-pro-se-argb-dlya-igrovogo-pk-ID10Ov5f.html",
  "title": "Топовый кулер ID Cooling Frozn A620 Pro SE ARGB для игрового ПК"
}
```
**Семпл #44:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/noviy-protsesor-amd-ryzen-9-9950x-9000-series-IDY32sj.html",
  "title": "Новий Процесор AMD Ryzen 9 9950X 9000 Series"
}
```
**Семпл #45:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/s1700-set-intel-core-i5-14600kf-plata-b760-ddr4-vodyanka-trade-in-ID10THhl.html",
  "title": "s1700 сет Intel Core i5-14600KF + плата B760 DDR4 + водянка. Trade-IN"
}
```
**Семпл #46:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/prodam-ryzen-3-2200g-ID110EVo.html",
  "title": "Продам Ryzen 3 2200G"
}
```
**Семпл #47:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "AMD phenom X2 550 + боксовий кулер"
}
```
**Семпл #48:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/protsesori-intel-i5-6402p-6500-4-4yadra-rozprodazh-IDUEzXB.html",
  "title": "Процесори Intel  i5-6402P/6500 4/4ядра  РОЗПРОДАЖ!"
}
```
**Семпл #49:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/protsesor-amd-ryzen-9-9950x3d-am5-noviy-IDZRReu.html",
  "title": "Процесор AMD Ryzen 9 9950X3D AM5 новий"
}
```
**Семпл #50:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/intel-xeon-e5-2640v3-ID110EHi.html",
  "title": "INTEL Xeon e5-2640v3"
}
```
**Семпл #51:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/protsesor-intel-core-i3-4150-3-5ghz-3mb-5gt-s-sr1pj-IDZC1rM.html",
  "title": "Процесор Intel Core i3-4150 3.5GHz/3MB/5GT/s (SR1PJ)"
}
```
**Семпл #52:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/protsesor-intel-core-i5-7400-3-0ghz-6mb-8gt-s-sr32w-IDZC1nO.html",
  "title": "Процесор Intel Core i5-7400 3.0GHz/6MB/8GT/s (SR32W)"
}
```
**Семпл #53:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/intel-core-i7-3610qm-2-3ghz-6144kb-socket-g2-cpu-protsessor-sr0mn-ID110Ev1.html",
  "title": "Intel Core i7-3610QM 2.3GHz 6144KB Socket G2 CPU процессор SR0MN"
}
```
**Семпл #54:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/s1200-protsesor-intel-core-i9-10850k-10yader-20potokv-5-2ggts-z-grafkoyu-trade-in-ID10TGIm.html",
  "title": "s1200 процесор Intel Core i9-10850K 10ядер\\20потоків 5.2ГГц з графікою. Trade-IN"
}
```
**Семпл #55:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/potuzhniy-set-intel-core-i9-10850k-10yader-20pot-5-2ggts-z-vdeo-plata-asus-z490-trade-in-ID10TGI8.html",
  "title": "потужний сет Intel Core i9-10850K 10ядер\\20пот 5.2ГГц з відео + плата ASUS Z490. Trade-in"
}
```
**Семпл #56:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Процы со старых ноутов"
}
```
**Семпл #57:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Процесор 450/512/100/2.0V S1 SECC2"
}
```
**Семпл #58:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Процесор для ноутбука Intel Pentium P6200 Socket G1 PGA988"
}
```
**Семпл #59:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/komplekt-intel-core-i9-11900kf-asus-prime-z590-a-s1200-ID10yTJh.html",
  "title": "Комплект Intel Core i9 11900KF+ Asus Prime Z590 -A  s1200"
}
```
**Семпл #60:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/protsesor-intel-core-i7-6700k-4-00ghz-s1151-sr2l0-i7-6700k-IDZvF47.html",
  "title": "Процесор Intel Core i7-6700K 4.00GHz s1151 (SR2L0) / i7 6700K"
}
```
**Семпл #61:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Процесор Phenom II 1055T"
}
```
**Семпл #62:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Intel Xeon X7560 2.26GHz 8 ядер 16 потоків 24MB L3 LGA1567"
}
```
**Семпл #63:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "I3-1105f.        ."
}
```
**Семпл #64:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Процесори до ретро ПК"
}
```
**Семпл #65:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Intel Core 2 Quad Q9500 сокет 775 процессоры"
}
```
**Семпл #66:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/amd-ryzen-5-1600af-v-neizvestnom-sostoyanii-ID10YiRh.html",
  "title": "AMD Ryzen 5 1600AF в неизвестном состоянии"
}
```
**Семпл #67:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Рідинне охолодження corsair icue h150i elite capellix з лед підсвіткою"
}
```
**Семпл #68:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/protsesor-intel-core-i5-9500-8500-8400-7400-7600k-6500-ID10SLfT.html",
  "title": "Процесор intel core i5 9500/8500/8400/7400/7600k/6500"
}
```
**Семпл #69:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Процессор AMD Athlon II X4 640 AM3 / AM3+ (4 ядра)"
}
```
**Семпл #70:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Комплект Материнская плата Asus H-170 pro и i5-6500 с видео ядром"
}
```
**Семпл #71:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Xeon E5-2640v4 процессор CPU"
}
```
**Семпл #72:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Xeon x5650 (12M Cache)"
}
```
**Семпл #73:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/intel-core-5-6500-s-1151-sky-lake-IDUNmuC.html",
  "title": "Intel Core і5 -6500 -s.1151 Sky lake"
}
```
**Семпл #74:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/protsesor-ryzen-5-5600-ID10ZRzk.html",
  "title": "Процесор Ryzen 5 5600"
}
```
**Семпл #75:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/amd-ryzen-9-7900-box-kuler-v-komplekt-yak-noviy-ID10Sp1b.html",
  "title": "AMD Ryzen 9 7900 BOX (кулер в комплекті) | як новий"
}
```
**Семпл #76:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/prodam-protsessor-intel-i5-8600k-ID10MUxa.html",
  "title": "Продам процессор Intel I5-8600k"
}
```
**Семпл #77:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/intel-core-i9-14900k-lga1700-24-yadra-32-potoka-ID10QnTF.html",
  "title": "Intel Core i9-14900K LGA1700 24 ядра / 32 потока"
}
```
**Семпл #78:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/protsesor-intel-core-2-quad-q6600-4x2-4ghz-8mb-cache-1066mhz-bu-s775-pk-IDDusy5.html",
  "title": "Процесор Intel Core 2 Quad Q6600 4x2.4GHz 8mb cache 1066MHz бу s775 пк"
}
```
**Семпл #79:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Процессор 2 ядра Intel core  3.3 Ghz"
}
```
**Семпл #80:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Процесори intel celeron, pentium, 2 duo"
}
```
**Семпл #81:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/komplekt-materinska-plata-asus-rog-strix-z690-e-gaming-wifi-intel-core-i5-13600k-ID110vfX.html",
  "title": "Комплект: материнська плата Asus ROG Strix Z690-E Gaming WiFi + Intel Core i5-13600K"
}
```
**Семпл #82:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Процессор Core 2 Duo E6550"
}
```
**Семпл #83:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/protsesori-intel-i5-9500t-9500-9600k-s1151-rozprodazh-ID10jMiu.html",
  "title": "Процесори Intel i5 9500T/9500/9600K s1151. Розпродаж!"
}
```
**Семпл #84:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "‼️Топова повітряна система охолодження для CPU Scythe Ashura (SCASR-1000)"
}
```
**Семпл #85:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/komplekt-do-pk-i7-6700-16-gb-ddr4-mat-plata-kuller-ID10YXVq.html",
  "title": "Комплект до пк, i7 6700, 16 gb ddr4, мат. плата, куллер"
}
```
**Семпл #86:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "AMD Athlon II  робочій"
}
```
**Семпл #87:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Кулер для процесора Thermalright AXP120-X67 Black ARGB (новий, AM4 / Intel)"
}
```
**Семпл #88:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Процесор Intel Core 2 Duo E4500 2.20 GHz / 2 M / 800 (SLA95) s775"
}
```
**Семпл #89:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Процесор Intel Pentium G5600 3,9GHz"
}
```
**Семпл #90:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/protsesor-intel-xeon-e5-2623-v4-ID10YAlp.html",
  "title": "Процесор Intel Xeon E5-2623 v4"
}
```
**Семпл #91:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Процесор amd ryzen 7600х"
}
```
**Семпл #92:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "ПРОДАМ процессор AMD 5 7500F"
}
```
**Семпл #93:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "AMD Athlon II X3 460. Intel Pentium B960. Система охлаждения Samsung 300V3A/300V4A/300V5A"
}
```
**Семпл #94:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Комплект: материнська плата, процесор, водяне охолодження"
}
```
**Семпл #95:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Процессор AMD Ryzen 3 2200"
}
```
**Семпл #96:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Кулер вентилятор процессора Intel LGA775 для Core2 Duo, Quad"
}
```
**Семпл #97:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/5-8500-intel-core-3-00-ghz-protsesor-ID10TG6y.html",
  "title": "і5-8500 Intel Core 3.00 ghz процесор"
}
```
**Семпл #98:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/prodam-ryzen-3-2200g-ID110EVo.html",
  "title": "Продам Ryzen 3 2200G"
}
```
**Семпл #99:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/rozstrochka-mono-na-3-msyats-intel-core-i5-14600kf-asus-tuf-b760m-plus-id-cooling-se-206xt-topoviy-suchasniy-groviy-komplekt-ID10Xj6E.html",
  "title": "РОЗСТРОЧКА МОНО НА 3 МІСЯЦІ! Intel Core i5 14600KF, Asus TUF B760M-Plus, ID-Cooling SE-206XT топовий сучасний ігровий комплект"
}
```
**Семпл #100:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Боксовые кулера Intel и AMD"
}
```

#### 🔌 Материнські плати — Відсіяно (100):
**Семпл #1:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/materinska-plata-gigabyte-z790-ud-s1700-intel-z790-pci-ex16-ID10QMt2.html",
  "title": "Материнська плата Gigabyte Z790 UD (s1700, Intel Z790, PCI-Ex16)"
}
```
**Семпл #2:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/materinska-plata-asrock-b850m-steel-legend-wifi-oftsyna-garantya-ID1101qq.html",
  "title": "Материнська плата ASRock B850M Steel Legend WiFi (Офіційна гарантія)"
}
```
**Семпл #3:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/materinska-plata-gigabyte-x870-eagle-wifi7-ID10AZhe.html",
  "title": "Материнська плата GIGABYTE X870 EAGLE WIFI7"
}
```
**Семпл #4:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Gigabyte GA G33M-S2"
}
```
**Семпл #5:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Материнську плату ASRock з процесором AMD Athlon"
}
```
**Семпл #6:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Матиринка m5a97 plus"
}
```
**Семпл #7:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Материнские платы 1155 сокет. 1151 сокет. Топовые и бюджетные."
}
```
**Семпл #8:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Потужный недорогие комплекты i5 + материнская плата 1150 можно с памятью ddr3"
}
```
**Семпл #9:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/komplekt-asrock-x370-pro4-ta-ryzen-5-1600-ID110Gcn.html",
  "title": "Комплект Asrock x370 pro4 та ryzen 5 1600"
}
```
**Семпл #10:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "ASUS Prime X399-A + Ryzen Threadripper 1920X + кулер"
}
```
**Семпл #11:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Материнская плата Asus P4P800SE"
}
```
**Семпл #12:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "s1200 mini-ITX материнка Z490i AORUS ULTRA Wi-Fi BT (10\\11покоління)"
}
```
**Семпл #13:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/rozstrochka-3-msyats-vd-mono-ryzen-7-7700-gigabyte-b850-eagle-wifi6e-be-quiet-pure-rock-3lx-topoviy-groviy-komplekt-am5-ID10WKqz.html",
  "title": "РОЗСТРОЧКА 3 МІСЯЦІ ВІД МОНО! Ryzen 7 7700, Gigabyte B850 Eagle WiFi6E, Be Quiet! Pure Rock 3LX топовий ігровий комплект АМ5"
}
```
**Семпл #14:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/asus-tuf-gaming-x670e-plus-wifi-IDYG43k.html",
  "title": "Asus TUF Gaming X670E-Plus WiFi"
}
```
**Семпл #15:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/materinka-asus-z68-virtu-ID10YI1z.html",
  "title": "Материнка Asus z68 virtu"
}
```
**Семпл #16:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Материнська плата am2, am3. Ddr2"
}
```
**Семпл #17:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Материнская плата"
}
```
**Семпл #18:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "комплектація материнська плата"
}
```
**Семпл #19:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Продам компютерні запчастини"
}
```
**Семпл #20:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/mat-plata-asrock-h110m-dgs-lga1151-ddr4-IDZQDBC.html",
  "title": "Мат плата Asrock h110m dgs Lga1151 ddr4"
}
```
**Семпл #21:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/materinskaya-plata-gigabyte-z370-hd3-ID110Gha.html",
  "title": "Материнская плата GIGABYTE Z370 HD3"
}
```
**Семпл #22:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Материнська плата до ноутбука читати оголошення"
}
```
**Семпл #23:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/komplekt-intel-core-i3-8100-gigabyte-b365m-aorus-elite-16gb-ddr4-ID10P9O3.html",
  "title": "Комплект Intel Core i3-8100 + Gigabyte B365M Aorus Elite + 16GB DDR4"
}
```
**Семпл #24:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Мат плата Asus 760GM p21 fx+процесор 4 ядра amd athlon 2 adx64"
}
```
**Семпл #25:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Продам  материнскую плату"
}
```
**Семпл #26:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/komplekt-gigabyte-ga-b85m-ds3h-a-intel-core-i3-4160-ozp-16gb-ddr3-ID10R2yg.html",
  "title": "Комплект Gigabyte GA-B85M-DS3H-A + Intel Core i3-4160 + ОЗП 16GB DDR3"
}
```
**Семпл #27:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Материнская плата Intel DG965RY S775 965 4×DDR2"
}
```
**Семпл #28:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Материнская плата Новые AM4,1151v2,1200,1700"
}
```
**Семпл #29:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Материнська плата+проц+опертивка"
}
```
**Семпл #30:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Материнская плата"
}
```
**Семпл #31:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Gigabyte GA-73VM-S2 системная плата на базе чипсета GeForce 7050 S775"
}
```
**Семпл #32:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Asus k8n системная плата на базе чипсета nVIDIA nForce 3 250 S754"
}
```
**Семпл #33:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "MSI K9NGM-L системная плата на базе чипсета NVIDIA GeForce 6100 AM2"
}
```
**Семпл #34:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/materinskaya-plata-asrock-870-extreme-3-IDXnBUM.html",
  "title": "Материнская плата ASRock - 870 EXTREME 3"
}
```
**Семпл #35:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Срочно. Материнская плата  asus A68HM-K"
}
```
**Семпл #36:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Материнская плата Asrock extreme 4 1150 +ЦП и куллер"
}
```
**Семпл #37:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/komplekt-1150-asrock-h81-r2-0-intel-core-i5-4670k-8gb-ddr3-ID10WrTG.html",
  "title": "Комплект 1150 ASRock H81 R2.0 + Intel Core i5-4670K + 8GB DDR3"
}
```
**Семпл #38:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/materinska-plata-asus-rog-crosshair-x870e-hero-btf-am5-amd-ryzen-nova-apex-aorus-IDYvNro.html",
  "title": "Материнська плата ASUS ROG CROSSHAIR X870E Hero BTF AM5 amd ryzen Нова apex aorus"
}
```
**Семпл #39:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Материнська плата під ремонт / донорство + (куллер, I/O планка, CMOS батарейка)"
}
```
**Семпл #40:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Материнська плата GIGABYTE GA-970A-DS3 (rev. 1.1) Socket AM3 plus."
}
```
**Семпл #41:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Материнська плата Asus P5VD2-MX"
}
```
**Семпл #42:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Материнські плати"
}
```
**Семпл #43:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Материнська плата комплект"
}
```
**Семпл #44:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Мануал материнки Asus M2N-X plus"
}
```
**Семпл #45:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Gigabyte GA-78LMT-S2P (sAM3+, AMD FX, Phenom)"
}
```
**Семпл #46:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/materinska-plata-msi-mag-tomahawk-b550-ID10DCYo.html",
  "title": "Материнська плата MSI MAG tomahawk b550"
}
```
**Семпл #47:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/materinska-plata-asus-prime-b350m-e-IDZO63v.html",
  "title": "Материнська плата ASUS PRIME B350M-E"
}
```
**Семпл #48:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "материнська плата комплект NF61S Micro AM2 SE +ОЗУ + проц+ БП в бонус"
}
```
**Семпл #49:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/materinka-asus-v-zbor-i3-ddr3-4-gb-ID10ZkKM.html",
  "title": "Материнка Asus (в зборі) + i3 + DDR3 4 ГБ"
}
```
**Семпл #50:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/komplekt-soyo-x99-d4-tpm-2-0-e5-2643-v3-16gb-intel-xeon-lga-2011-3-x99-ddr4-zeon-kseon-ID10S2vz.html",
  "title": "Комплект SOYO X99 D4 TPM 2.0 / E5 2643 v3 / 16GB intel xeon lga 2011-3 x99 ddr4 зеон ксеон"
}
```
**Семпл #51:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/materinska-plata-m5a78l-m-le-16gb-kuler-IDTH7BB.html",
  "title": "Материньська плата m5a78l m le + 16gb + кулер"
}
```
**Семпл #52:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Материнка і комплектуючі"
}
```
**Семпл #53:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/i7-8700k-asus-rog-strix-z370-e-gaming-be-quiet-ID10ETmR.html",
  "title": "i7-8700K + ASUS ROG Strix Z370-E Gaming + be quiet!"
}
```
**Семпл #54:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Материнская плата для компьютера Jetway M2GTA-4VP (Socket AM2)"
}
```
**Семпл #55:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "комплект майнинг ферма для начинающих"
}
```
**Семпл #56:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/materinska-plata-asus-prime-h270m-plus-ID110Ej4.html",
  "title": "Материнська плата  ASUS PRIME h270m- plus"
}
```
**Семпл #57:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "PCI Riser HP Compaq плата розширення"
}
```
**Семпл #58:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Материнська плата Asrock Rack Z690D4U"
}
```
**Семпл #59:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Нова NZXT N9 Z890 LGA 1851 ATX Gaming Motherboard White pcie 5.0"
}
```
**Семпл #60:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Asrock b650pg lightning на ремонт/запчастини"
}
```
**Семпл #61:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Материнская плата Asrock extreme 4 1150 +ЦП и куллер"
}
```
**Семпл #62:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Материнська плата"
}
```
**Семпл #63:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Материнські плати ASRock, ASUS,GIGABITE,MSI. (Ретро)"
}
```
**Семпл #64:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/komplekt-intel-i3-9100f-msi-h310m-pro-vd-plus-ID10Yo85.html",
  "title": "Комплект Intel i3-9100F + MSI H310M PRO-VD PLUS"
}
```
**Семпл #65:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Продам материнську плату ASUS P5G-MX"
}
```
**Семпл #66:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Материнська плата Acer Q5WT6 LA-8531P"
}
```
**Семпл #67:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Материнська плата GIGABYTE GA-M61PME-S2 разом з процесором"
}
```
**Семпл #68:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Продаю БУ комплект материнскую плату 1155 + процесор intel Core 9 2600 + кулер и оперативная память 16 гб"
}
```
**Семпл #69:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Материнська Плата Б/У Є ВИБІР s1156 1155,AM3, AM3+, Am2, FM1, FM2 s775"
}
```
**Семпл #70:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/prodam-platu-asus-tuf-z790-pro-wifi-intel-14700k-ID10YBxl.html",
  "title": "Продам плату Asus TUF Z790-PRO WIFI + Intel 14700K"
}
```
**Семпл #71:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/igrovoy-komplekt-msi-a520m-a-pro-ryzen-5-3500x-amd-amd-rayzen-5-am4-IDXhfMs.html",
  "title": "Игровой комплект MSI A520M A PRO Ryzen 5 3500X амд amd райзен 5 am4"
}
```
**Семпл #72:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/asus-rog-strix-b760-f-gaming-wi-fis1700-intel-b760-na-garantii-ID10NY07.html",
  "title": "Asus ROG STRIX B760-F Gaming Wi-Fi(s1700, Intel B760) на гарантии"
}
```
**Семпл #73:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Материнка Z600 с адаптером под ATX БП"
}
```
**Семпл #74:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/asus-tuf-gaming-x670e-plus-wifi-IDYG43k.html",
  "title": "Asus TUF Gaming X670E-Plus WiFi"
}
```
**Семпл #75:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Материнская плата Foxconn G31MXP"
}
```
**Семпл #76:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Материнская плата GIGABYTE GA-990XA-UD3 (AM3+)"
}
```
**Семпл #77:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/komplekt-qiyida-x99-k9s-xeon-e5-2699-v3-18-36-lga2011-3-ID10YQfY.html",
  "title": "Комплект QIYIDA X99 K9S + Xeon E5-2699 v3 18/36 LGA2011-3"
}
```
**Семпл #78:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "АКЦІЯ! Материнська плата Asus Prime N100I-D D4, Intel N100 Quad-Core 2.0GHz 1×Ddr4 Sodimm, VGA/HDMI/DP mITX"
}
```
**Семпл #79:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Материнская плата Asus P5GC"
}
```
**Семпл #80:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Процесор та материнська плата"
}
```
**Семпл #81:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Материнская плата ,Процессор ,Оперативная память"
}
```
**Семпл #82:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Материнська плата сокет AM3+"
}
```
**Семпл #83:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Компютерне залізо одним лотом. (Xeon X3440, Athlon 64 x2, FSP, DDR4. DDR3. DDR2). Торг"
}
```
**Семпл #84:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Мат. плата ASUS P5PL2"
}
```
**Семпл #85:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/groviy-komplekt-ryzen-7-2700-biostar-b350-kuler-ID10s0TY.html",
  "title": "Ігровий комплект Ryzen 7 2700 Biostar B350 кулер"
}
```
**Семпл #86:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/asus-rog-strix-b760-f-gaming-wi-fis1700-intel-b760-na-garantii-ID10NY07.html",
  "title": "Asus ROG STRIX B760-F Gaming Wi-Fi(s1700, Intel B760) на гарантии"
}
```
**Семпл #87:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/msi-mpg-b650i-edge-wifi-povniy-komplekt-z-rdnoyu-korobkoyu-ID10SrvR.html",
  "title": "MSI MPG B650I EDGE WIFI | повний комплект з рідною коробкою"
}
```
**Семпл #88:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/materinska-plata-biostar-tb360-lga1151-intel-g4900-ID10MqY7.html",
  "title": "Материнська плата Biostar TB360 LGA1151 + Intel G4900"
}
```
**Семпл #89:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Psp материнські плати не робочі"
}
```
**Семпл #90:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "материнська плата GA-H67MA-USB3-B3 сокет 1155, ОЗУ макс 32гб; сата-6шт"
}
```
**Семпл #91:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Комплект Intel 6 ядер / 24 Gb озу материнка + проц +кулер + озу Evga x"
}
```
**Семпл #92:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Материнская плата ASUS P5G41T-M LX2/GB/LPT"
}
```
**Семпл #93:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Материнская плата для часов Samsung gear sport, под ремонт"
}
```
**Семпл #94:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/igrovoy-komplekt-rayzen-msi-a520m-ryzen-5-3600-amd-amd-ryzen-am4-ID108kGa.html",
  "title": "Игровой комплект райзен MSI A520M Ryzen 5 3600 амд amd ryzen am4"
}
```
**Семпл #95:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/komplekt-intel-i3-9100f-msi-h310m-pro-vd-plus-ID10Yo85.html",
  "title": "Комплект Intel i3-9100F + MSI H310M PRO-VD PLUS"
}
```
**Семпл #96:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "EPoX EP-7KXA Slot A + AMD Athlon 650MHz - комплект для коллекции"
}
```
**Семпл #97:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Материнська плата Foxconn N15235 Socket AM2 + AMD Athlon 64 X2 + 2 ГБ RAM"
}
```
**Семпл #98:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Материнська плата NFORCE4M-A V3.0"
}
```
**Семпл #99:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Материнская плата комплект Asus P4B533-X"
}
```
**Семпл #100:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Материнские платы 1155 сокет. 1151 сокет. Топовые и бюджетные."
}
```

#### ⚡ Блоки живлення — Відсіяно (100):
**Семпл #1:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/bloki-zhivlennya-fsp-hp-fujitsu-200-850w-IDVRYdh.html",
  "title": "Блоки живлення FSP HP FUJITSU 200-850W"
}
```
**Семпл #2:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/bloki-zhivlennya-dlya-grovih-pk-be-quiet-thermaltake-300-850w-6-8pin-gpu-IDVRY8d.html",
  "title": "Блоки живлення для ігрових ПК Be quiet Thermaltake 300-850W 6/8pin GPU"
}
```
**Семпл #3:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Блок живлення SeaSonic Focus Plus 1000 Gold (SSR-1000FX)"
}
```
**Семпл #4:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Блок живлення LED jinbo 150вт"
}
```
**Семпл #5:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Продається 2 блока живлення і 2 кулера"
}
```
**Семпл #6:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/top-blok-zhivlennya-850w-seasonic-prime-px-850-platinum-trade-in-ID10LNMs.html",
  "title": "ТОП блок живлення 850W Seasonic PRIME PX-850 PLATINUM. Trade-in"
}
```
**Семпл #7:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Chieftec Proton BDF-500S Блок живлення"
}
```
**Семпл #8:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/atx-blok-zhivlennya-550w-qube-bronze-trade-in-ID10zmzV.html",
  "title": "ATX блок живлення 550W QUBE (bronze). Trade-IN"
}
```
**Семпл #9:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/svzhiy-blok-zhivlennya-700w-qube-bronze-4-4-cpu-4x6-2-gpu-trade-in-IDZDvwx.html",
  "title": "свіжий блок живлення 700W QUBE Bronze (4+4 CPU. 4x6+2 GPU). Trade-IN"
}
```
**Семпл #10:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/blok-zhivlennya-300w-dlya-pk-ID102CkF.html",
  "title": "Блок живлення 300W для ПК"
}
```
**Семпл #11:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Блок питания High Power 370w"
}
```
**Семпл #12:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "NEW Блоки живлення BITMAIN APW12 (APW121417b) для S19/ T19/ L7/ K7"
}
```
**Семпл #13:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Нові Блоки живлення BITMAIN APW12 14-17v (B) для S19 (xp), K7, L7, KS3"
}
```
**Семпл #14:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/blok-pitaniya-zalman-zm1200-arx-1200w-acrux-series-ID10p6Cd.html",
  "title": "Блок питания Zalman ZM1200-ARX 1200w Acrux Series"
}
```
**Семпл #15:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Блок питания  Q-dion QD400"
}
```
**Семпл #16:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Блок живлення Seasonic SSR-1300GB (Prime 1300 Gold)"
}
```
**Семпл #17:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Блок живлення Seasonic SSR-850GD (PRIME 850 Gold)"
}
```
**Семпл #18:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/svzhiy-yaksniy-blok-zhivlennya-750w-corsair-rm750-gold-trade-in-ID110FKu.html",
  "title": "свіжий якісний блок живлення 750W Corsair RM750 GOLD. Trade-IN"
}
```
**Семпл #19:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "БУ блоки питания в полностью рабочем состоянии ATX"
}
```
**Семпл #20:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/blok-zhivlennya-na-pk-500w-ID10DZMh.html",
  "title": "Блок Живлення на ПК, 500w"
}
```
**Семпл #21:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/blok-zhivlennya-thermaltake-tr2-420w-IDYgHp6.html",
  "title": "Блок живлення Thermaltake TR2-420w"
}
```
**Семпл #22:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/blok-zhivlennya-thermaltake-smart-rgb-500w-ID110FvQ.html",
  "title": "Блок живлення Thermaltake Smart RGB 500W"
}
```
**Семпл #23:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Продам блок живлення"
}
```
**Семпл #24:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/850w-750w-650w-550w-450w-yaksn-brendov-bloki-zhivlennya-protestovan-povnstyu-roboch-stan-garniy-ID10KwGv.html",
  "title": "850W 750W 650W 550W 450W Якісні брендові блоки живлення Протестовані повністю робочі Стан гарний"
}
```
**Семпл #25:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/blok-zhivlennya-chieftec-600w-IDVekcH.html",
  "title": "Блок живлення Chieftec 600W"
}
```
**Семпл #26:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Блок питания для стационарного компьютера Б/У"
}
```
**Семпл #27:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Блок питания Cougar CMX 1200 Вт 80 PLUS Bronze"
}
```
**Семпл #28:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/blok-zhivlennya-vinga-vps-750w-gold-IDZwysV.html",
  "title": "Блок живлення Vinga VPS 750W Gold"
}
```
**Семпл #29:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/blok-zhivlennya-fsp-2000w-fsp2000-a0agpbi-IDPVxsH.html",
  "title": "Блок живлення FSP 2000W (FSP2000-A0AGPBI)"
}
```
**Семпл #30:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Блок питания с радио завода"
}
```
**Семпл #31:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Потужний Блок Живлення( пускозарядний пристрій для машин) AC 220v-DC 1"
}
```
**Семпл #32:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/blok-zhivlennya-be-quiet-straight-power-12-1000w-bn338-80-plus-platinum-garantya-sche-9-rokv-ID10VhVs.html",
  "title": "Блок живлення be quiet! Straight Power 12 1000W (BN338), 80 PLUS Platinum — гарантія ще 9 років"
}
```
**Семпл #33:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/blok-zhivlennya-vinga-vps-1650-v2-mining-edition-ID110EH3.html",
  "title": "Блок живлення Vinga VPS 1650 V2 Mining edition"
}
```
**Семпл #34:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/blok-zhivlennya-polaris-1250w-ID10HuWO.html",
  "title": "Блок живлення Polaris 1250W"
}
```
**Семпл #35:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Блок живлення комп\"ютерний, від акумуляторної бат. DC/DC 32-72V"
}
```
**Семпл #36:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/thermaltake-gt-snow-850w-gold-modulniy-blok-zhivlennya-ID10j294.html",
  "title": "Thermaltake GT SNOW 850W Gold | Модульний блок живлення"
}
```
**Семпл #37:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "NEW Блоки живлення BITMAIN APW12 (APW121215F) для S19/ T19/ L7/ K7"
}
```
**Семпл #38:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/blok-zhivlennya-dlya-pk-650w-750w-850w-yak-nov-garantya-servs-IDX27KE.html",
  "title": "Блок живлення для Пк 650w 750w 850w як нові ,гарантія, сервіс !"
}
```
**Семпл #39:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Блок живлення для монітора ADS-40NP-19-1, 19030E - 19V 1.58A 30W 5.5x2.5mm"
}
```
**Семпл #40:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Блок живлення HPC-500-H12S"
}
```
**Семпл #41:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Блок живлення Corsair CS650M"
}
```
**Семпл #42:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/cooler-master-v850-sfx-gold-850w-mpy-8501-sfhagv-ID10NaC1.html",
  "title": "Cooler Master V850 SFX Gold 850W (MPY-8501-SFHAGV)"
}
```
**Семпл #43:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Адаптер(блок питания) HP 24V, 500mA, 12W, 6.5mm x 3.0 ..."
}
```
**Семпл #44:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/blok-zhivlennya-dlya-pk-650w-750w-850w-gurt-rozdrb-garantya-IDX24Vz.html",
  "title": "Блок живлення для Пк 650w 750w 850w гурт роздріб гарантія!"
}
```
**Семпл #45:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Новий блок живлення"
}
```
**Семпл #46:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/blok-zhivlennya-aerocool-vx-700w-IDZQeIa.html",
  "title": "Блок живлення Aerocool VX-700W"
}
```
**Семпл #47:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Серверний блок живлення Emerson 1975W (IBM / Lenovo)"
}
```
**Семпл #48:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Оригінальні кабелі до компютерних блоків живлення Asus"
}
```
**Семпл #49:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/seasonic-prime-ultra-850w-titanium-ssr-850tr-titanoviy-top-modulniy-rtx-gtx-gt-mx-rx-gaming-oc-ID10PaHT.html",
  "title": "Seasonic PRIME Ultra 850W Titanium (SSR-850TR) титановий  топ Модульний rtx gtx gt mx rx gaming oc"
}
```
**Семпл #50:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/blok-zhivlennya-seasonic-focus-gx-650-650w-ssr-650fx-3743-IDZOMso.html",
  "title": "Блок живлення Seasonic Focus GX-650 650W (SSR-650FX) - 3743"
}
```
**Семпл #51:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/blok-pitaniya-hpc-350-102-350w-ID10DXAj.html",
  "title": "Блок питания HPC 350-102 (350W)"
}
```
**Семпл #52:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/bloki-zhivlennya-600w-chieftec-gps-600ab-ta-aerocool-vx-plus-ID110DT2.html",
  "title": "Блоки живлення 600W Chieftec GPS-600AB та AeroCool VX PLUS"
}
```
**Семпл #53:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Блоки живлення для компютера"
}
```
**Семпл #54:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Блок живлення ATX GAMEMAX GM-500"
}
```
**Семпл #55:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Без гарантій віддам"
}
```
**Семпл #56:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Блок питания"
}
```
**Семпл #57:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Блок живлення chieftec iarena 450 gpa 450s8"
}
```
**Семпл #58:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Блок живлення до компьютера CHIFTEC GPS 600A8 Новий!"
}
```
**Семпл #59:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Блок живлення Full Energy BGM-125Pro"
}
```
**Семпл #60:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "NEW Блоки живлення BITMAIN APW17 (APW171215c) для S21/ T21/ L9/ L11"
}
```
**Семпл #61:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/blok-zhivlennya-seasonic-prime-titanium-650w-ssr-650td-3734-IDYkaM6.html",
  "title": "Блок живлення Seasonic Prime Titanium 650W (SSR-650TD) - 3734"
}
```
**Семпл #62:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/blok-zhivlennya-msi-mpg-pcie5-1000-vt-80-gold-ID10Sr77.html",
  "title": "Блок живлення MSI MPG PCIE5 1000 Вт 80+ Gold"
}
```
**Семпл #63:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Блок живлення на 12 вольт KENWOOD"
}
```
**Семпл #64:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Зарядка для телефона зарядка для стареньких тл"
}
```
**Семпл #65:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Блок живлення Chieftec 2009 рік"
}
```
**Семпл #66:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Компьютерный блок питания CHIEFTEC GPS-1250C 80+GOLD"
}
```
**Семпл #67:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Продам блок питания Fortron FSP-250-60-GTA (б/у)"
}
```
**Семпл #68:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Corsair RM850x 80 Plus Gold 2020 рік Блок живлення ігровий модульний gtx rtx gt rx mx gaming oc"
}
```
**Семпл #69:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Зарядка Блок живлення HP 45W 90W 4530 4.5x3.0 Blue pin Blue tip ОРИГІНАЛ"
}
```
**Семпл #70:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/phanteks-amp-750w-80-plus-gold-seasonic-platforma-blok-zhivlennya-modulniy-groviy-bzh-bp-rtx-rx-gtx-gt-gaming-oc-ID10UoVz.html",
  "title": "Phanteks AMP 750W 80 Plus Gold (Seasonic платформа) Блок живлення модульний ігровий бж БП rtx rx gtx gt gaming oc"
}
```
**Семпл #71:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/blok-pitaniya-be-quiet-dark-power-pro-1500w-ID10ZRi8.html",
  "title": "Блок питания Be Quiet Dark Power Pro 1500w"
}
```
**Семпл #72:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Блок живлення D-Link Chassi 16slot Media conv 19\" (DMC-1000)"
}
```
**Семпл #73:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Блок живлення для компютера"
}
```
**Семпл #74:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Блок живлення 9 В, 4 А"
}
```
**Семпл #75:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/blok-pitaniya-cougar-600w-ID10UUjx.html",
  "title": "Блок питания Cougar 600w"
}
```
**Семпл #76:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/blok-zhivlennya-seasonic-prime-ultra-gold-850w-ssr-850gd-2583-IDZET2U.html",
  "title": "Блок живлення Seasonic Prime Ultra Gold 850W (SSR-850GD) - 2583"
}
```
**Семпл #77:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Seasonic Prime PX-650 80 Plus Platinum (SSR-650PD) модульний блок живлення Рідна пломба  гарний стан Ультимативний rtx gtx gt gaming oc rx"
}
```
**Семпл #78:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Блок живлення Frime Micro-ATX FPMO-400-8Z"
}
```
**Семпл #79:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/blok-pitaniya-thermaltake-850w-gold-otlichnyy-ID10mlXH.html",
  "title": "Блок питания Thermaltake 850w gold. Отличный"
}
```
**Семпл #80:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "SATA-кабель для модульного блока питания"
}
```
**Семпл #81:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Блок  питания 48 вольт"
}
```
**Семпл #82:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/blok-zhivlennya-thermaltake-berlin-750w-ID10YlER.html",
  "title": "Блок живлення thermaltake Berlin 750w"
}
```
**Семпл #83:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Компьютерный блок питания."
}
```
**Семпл #84:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Блок живлення та інші запчастини  series x"
}
```
**Семпл #85:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Оригінальні кабелі до компютерних блоків живлення Asus"
}
```
**Семпл #86:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "NEW Блоки живлення BITMAIN APW11 для S19/ S21+/ XP Hydro"
}
```
**Семпл #87:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Блок живлення Q-DION QD450 450Вт"
}
```
**Семпл #88:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/blok-zhivlennya-be-quiet-power-zone-2-850w-ID10OxIf.html",
  "title": "Блок живлення Be quiet! Power zone 2 850w"
}
```
**Семпл #89:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Блок живлення Блок питания 3В-24В (1-40А). Адаптер 5V 6V 9V 12V 18V 24V для роутера, LED стрічки. Опт/роздріб"
}
```
**Семпл #90:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "ОПТ Блоки живлення Блок Питания 3В-24В (1-40А). Адаптери 5V 6V 9V 12V 18V 24V. Від 10 шт!"
}
```
**Семпл #91:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Адаптер питания 65W, 90W, 150W. для монитора  Apple Cinema display"
}
```
**Семпл #92:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Блок питания Corsair CX750M 80plus Bronze. Полумодельный блок. Полностью рабочий"
}
```
**Семпл #93:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Блок живлення Q-dion"
}
```
**Семпл #94:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/blok-pitaniya-cougar-600w-ID10UUjx.html",
  "title": "Блок питания Cougar 600w"
}
```
**Семпл #95:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Б/в блок живлення від ПК Frontier ATX-400F (не працює)"
}
```
**Семпл #96:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Блок питания Corsair AX1500 80 Plus Titanium"
}
```
**Семпл #97:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/bzh-80-gold-pd-remont-700w-850w-750w-thermaltake-gf-gt-toughpower-berlin-tr2-s-ID10Z0Pd.html",
  "title": "БЖ 80+ Gold  під ремонт 700w 850w 750w Thermaltake GF GT toughpower berlin tr2 s"
}
```
**Семпл #98:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Кабеля  модульного БП  Chieftec A135. Be Quiet и нерабочие БП Chieftec"
}
```
**Семпл #99:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Блок питания серверный HP HSTNS-PR49 80PLUS PLATINUM 2650W"
}
```
**Семпл #100:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Продаю блок питания"
}
```

#### 💾 Накопичувачі — Відсіяно (100):
**Семпл #1:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/ssd-disk-m-2-agi-512gb-ID10uvtc.html",
  "title": "SSD диск M.2 Agi 512gb"
}
```
**Семпл #2:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/seagate-exos-x20-st16000nm000d-3pc101-16tb-sata-3-5-hdd-ID10B9Q1.html",
  "title": "Seagate Exos X20 / ST16000NM000D-3PC101 16TB SATA 3.5 HDD"
}
```
**Семпл #3:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/ssd-m2-nvme-2280-samsung-256gb-nvme-2280-512gb-sk-hynix-nvme-western-digital-2230-dlya-pk-noutbuka-IDZPAa7.html",
  "title": "ssd m2 nvme 2280 SAMSUNG 256GB нвме 2280 512gb SK hynix nvme Western Digital 2230 для пк ноутбука"
}
```
**Семпл #4:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Жесткие Диски для ПК/Ноутбука"
}
```
**Семпл #5:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/zhestkie-diski-500gb-500gig-hdd-dlya-pk-3-5-2-5-ID10P8bN.html",
  "title": "Жёсткие диски 500gb 500гиг. HDD для ПК 3.5, 2.5"
}
```
**Семпл #6:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "мережеве обладнання різне Catalyst 3750  комутатори cisco розпродаж"
}
```
**Семпл #7:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "SSD диск з програмами для діагностики авто"
}
```
**Семпл #8:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/ssd-disk-240gb-apacer-panther-as340-sata3-2-5-trade-in-IDZQgQm.html",
  "title": "SSD диск 240GB Apacer PANTHER AS340 (SATA3 \\ 2.5\"). Trade-in"
}
```
**Семпл #9:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/m-2-ssd-disk-500gb-kingston-nv2-nvme-pci-e-4-0-x4-trade-in-IDZQgLc.html",
  "title": "M.2 SSD диск 500GB Kingston NV2 (NVMe\\PCI-e 4.0 x4). Trade-IN"
}
```
**Семпл #10:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Старые, раритетные жесткие диски HDD"
}
```
**Семпл #11:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/servern-zhorstk-diski-hgst-ultrastar-4tb-3-5-7200rpm-sas-12gb-s-hus726040al5210-ID10P5kY.html",
  "title": "Серверні жорсткі диски HGST Ultrastar 4TB 3.5\" 7200rpm SAS 12Gb/s (HUS726040AL5210)."
}
```
**Семпл #12:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/zhorstkiy-disk-western-digital-black-500gb-7200rpm-32mb-wd5000lplx-2-5-sata-iii-ID10LKBP.html",
  "title": "Жорсткий диск Western Digital Black 500GB 7200rpm 32MB WD5000LPLX 2.5 SATA III"
}
```
**Семпл #13:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/ssd-grucial-p3-plus-4tb-ID10ZgyS.html",
  "title": "SSD Grucial P3 Plus 4TB"
}
```
**Семпл #14:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/toshiba-mq04abf100-1-tb-5400-rpm-sata-iii-ID110Gcr.html",
  "title": "Toshiba mq04abf100 (1 tb,5400 rpm,sata III)"
}
```
**Семпл #15:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/top-vibr-m-2-ssd-disk-1tb-samsung-970-evo-plus-pci-e-3-0-x4-nvme-trade-in-ID10pEqg.html",
  "title": "ТОП вибір M.2 SSD диск 1TB Samsung 970 EVO PLUS (PCI-e 3.0 x4. NVMe). Trade-in"
}
```
**Семпл #16:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Жорсткий диск.  .Ціна за два"
}
```
**Семпл #17:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/zhorstkiy-disk-2-5-hitachi-500gb-travelstar-5k750-hts547550a9e384-ID10E09Z.html",
  "title": "Жорсткий диск 2.5\" Hitachi 500GB Travelstar 5K750 HTS547550A9E384"
}
```
**Семпл #18:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "HDD Western Digital WD5003ABYX"
}
```
**Семпл #19:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/zhorstkiy-disk-toshiba-mk3252gsx-320gb-2-5-sata-ID110FRN.html",
  "title": "Жорсткий диск Toshiba MK3252GSX 320GB 2.5\" SATA"
}
```
**Семпл #20:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/ssd-kingston-a400-480-gb-ID110FPC.html",
  "title": "SSD Kingston A400 480 gb"
}
```
**Семпл #21:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/ssd-2-5-120gb-kingston-sa400s37-120g-ID110FPZ.html",
  "title": "SSD 2.5\" 120GB Kingston (SA400S37/120G)"
}
```
**Семпл #22:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/seagate-expansion-desktop-8tb-IDUuDJp.html",
  "title": "Seagate Expansion Desktop 8TB"
}
```
**Семпл #23:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/vinchester-3-5-wd-caviar-blue-wd3200aajs-320-gb-sata300-7200-IDNOFh5.html",
  "title": "Винчестер 3.5 WD Caviar Blue wd3200aajs 320 gb sata300 7200"
}
```
**Семпл #24:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/ssd-gigabyte-nvme-512gb-model-gp-gsm2ne3512gntd-ID1010UO.html",
  "title": "SSD Gigabyte NVMe 512GB (модель GP-GSM2NE3512GNTD)"
}
```
**Семпл #25:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/ssd-kingston-fury-renegade-2tb-u-vdmnnomu-stan-ID10xKcw.html",
  "title": "SSD Kingston FURY Renegade 2TB у відмінному стані"
}
```
**Семпл #26:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/ssd-m-2-1tb-nvme-micron-3500-2280-r-do-7000-mb-s-w-do-6900-mb-s-mtfdkba1t0tgd-pcie-4-0-x4-oem-noviy-klkst-garantya-ID10KLEN.html",
  "title": "SSD M.2 1Tb NVMe Micron 3500 2280 R: до 7000 MB/s, W: до 6900 MB/s  (MTFDKBA1T0TGD) PCIe 4.0 x4 OEM Новий! Є кількість + Гарантія"
}
```
**Семпл #27:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/hhd-500gb-seagate-ID110FAr.html",
  "title": "Hhd 500gb Seagate"
}
```
**Семпл #28:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/komplekthdd-sata-250gb-3-5-120gb-2-5-pod-vosstanovlenie-zapchasti-ID102Bfx.html",
  "title": "КомплектHDD SATA 250GB (3.5\")+120GB (2.5\") под восстановление/запчасти"
}
```
**Семпл #29:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/zhestkiy-disk-western-digital-320-gb-ID102B8b.html",
  "title": "Жесткий диск Western Digital 320 GB"
}
```
**Семпл #30:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/zhorstkiy-disk-hitachi-2-5-500gb-wdc-hgst-hts725050a7e630-IDUPr8V.html",
  "title": "Жорсткий диск Hitachi 2.5\" 500GB WDC HGST (HTS725050A7E630)"
}
```
**Семпл #31:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/zhorstkiy-disk-seagate-1tb-barracuda-5400rpm-128mb-st2000lm015-sataiii-IDUPrpd.html",
  "title": "Жорсткий диск Seagate 1ТB Barracuda 5400rpm 128MB ST2000LM015 SATAIII"
}
```
**Семпл #32:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/top-vibr-ssd-disk-500gb-samsung-860-evo-sata3-2-5-trade-in-ID10dZqd.html",
  "title": "ТОП вибір! SSD диск 500GB Samsung 860 EVO (SATA3 \\ 2.5\"). Trade-in"
}
```
**Семпл #33:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Жорстиюкий диск hdd 256 gb"
}
```
**Семпл #34:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Seagate Momentus 5400.6 ST9500325AS"
}
```
**Семпл #35:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Жесткий диск Seagate Barracuda"
}
```
**Семпл #36:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/ssd-samsung-990-pro-2tb-m-2-nvme-noviy-100-resurs-ID10Z7em.html",
  "title": "SSD Samsung 990 PRO 2TB M.2 NVMe - новий, 100% ресурс"
}
```
**Семпл #37:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Жорсткий диск Hitachi 100Gb"
}
```
**Семпл #38:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/shvidksniy-ssd-m-2-nvme-500gb-ediloca-en760-pcie-4-0-z-radatorom-dlya-pk-ps5-noutbuk-shvidka-vdpravka-ID110F9i.html",
  "title": "Швидкісний SSD M.2 NVMe 500GB Ediloca EN760 PCIe 4.0 з радіатором (для ПК / PS5 / Ноутбук) Швидка відправка"
}
```
**Семпл #39:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Жесткий диск для компютера"
}
```
**Семпл #40:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/prodam-hdd-wd5003abyz-500gb-64mb-7200-3-5-ID104Z0Q.html",
  "title": "Продам HDD WD5003ABYZ 500GB/64mb 7200 3.5\""
}
```
**Семпл #41:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/m-2-ssd-disk-1tb-msi-spatium-m371-pci-e-3-0-x4-nvme-ID10g2xr.html",
  "title": "M.2 SSD диск 1TB MSI Spatium M371 (PCI-e 3.0 x4. NVMe)"
}
```
**Семпл #42:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/zhorstkiy-disk-western-digital-80gb-7200rpm-8mb-3-5-sataii-IDYsKkG.html",
  "title": "Жорсткий диск Western Digital 80Gb 7200rpm 8MB  3.5\" SATAII"
}
```
**Семпл #43:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/ssd-m-2-1tb-nvme-micron-3500-2280-r-do-7000-mb-s-w-do-6900-mb-s-mtfdkba1t0tgd-pcie-4-0-x4-oem-noviy-klkst-garantya-ID10KLEN.html",
  "title": "SSD M.2 1Tb NVMe Micron 3500 2280 R: до 7000 MB/s, W: до 6900 MB/s  (MTFDKBA1T0TGD) PCIe 4.0 x4 OEM Новий! Є кількість + Гарантія"
}
```
**Семпл #44:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Sata диски по 1 терабайту"
}
```
**Семпл #45:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/portativniy-nakopichuvach-4tb-usb-3-0-hdd-toshiba-ID10pfOg.html",
  "title": "Портативний накопичувач 4TB USB 3.0 HDD Toshiba"
}
```
**Семпл #46:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "накопичувач Samsung SSD M2 NVMe 970 EVO Plus"
}
```
**Семпл #47:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/ssd-micron-2280-m2-nvme-pcie-1000-1024-gb-1tb-ID10HRAh.html",
  "title": "SSD Micron 2280 m2 NVMe PCie 1000/1024 Gb 1Tb"
}
```
**Семпл #48:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/nakopitel-ssd-m-2-sata-1tb-razmery-22h42-100-zdorovya-ID10Qy7r.html",
  "title": "Накопитель SSD M.2 SATA-1TB. Размеры 22х42. 100% здоровья."
}
```
**Семпл #49:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Жорсткий диск для ПК 3,5\" HDD 1Тб SATA III"
}
```
**Семпл #50:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/groviy-nadyniy-shvidkiy-wd-blue-azlx-3-5-hdd-500gb-7200prm-32mb-sataiii-stan-novogo-levada-IDZahez.html",
  "title": "Ігровий надійний швидкий WD BLUE AZLX 3,5\" HDD 500Gb 7200prm 32Mb SATAIII - стан нового - Левада"
}
```
**Семпл #51:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/zhorstkiy-disk-hdd-western-digital-wd-green-500gb-sata-iii-wd5000aads-ID110E9f.html",
  "title": "Жорсткий диск HDD Western Digital WD Green 500GB SATA III WD5000AADS"
}
```
**Семпл #52:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Винчестер FUJITSU"
}
```
**Семпл #53:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/zhestkiy-disk-ssd-120gb-hdd-1-5tb-500-320gb-ID10YoN8.html",
  "title": "Жёсткий диск SSD 120Gb  HDD 1.5Tb 500 320Gb"
}
```
**Семпл #54:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/new-ssd-samsung-micron-480gb-sm883-sm863a-rm881-5300max-IDYNQbo.html",
  "title": "NEW! SSD Samsung, Micron 480Gb (SM883, SM863a, РМ881, 5300Max)"
}
```
**Семпл #55:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Ретро HDD 3.5 IDE Western Digital 44MB 1990 р. Раритет"
}
```
**Семпл #56:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/zhorstkiy-disk-western-digital-wd-purple-1tb-dlya-vdeosposterezhennya-IDXJWkI.html",
  "title": "Жорсткий диск Western Digital WD Purple 1TB для відеоспостереження"
}
```
**Семпл #57:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/ssd-samsung-870-qvo-8-tb-sostoyanie-100-v-nalichii-3-shtuki-ID101JdG.html",
  "title": "SSD Samsung 870 QVO 8 TB, состояние 100% (в наличии 3 штуки)"
}
```
**Семпл #58:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "HDD диск та інше"
}
```
**Семпл #59:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Жорсткий, жесткий диск Seagate, Western Digital"
}
```
**Семпл #60:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Ssd диски Kingston разных объемов."
}
```
**Семпл #61:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Жорсткий диск HDD 3,5\" 750Gb SATA3 Western Digital Black WD7501AALS 7200rpm/32Mb"
}
```
**Семпл #62:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/prodam-rostovku-novyh-ssd-diskov-64gb-4tb-priehali-vkusnyashki-IDZQCT0.html",
  "title": "Продам ростовку новых SSD дисков 64гб-4тб (приехали вкусняшки)"
}
```
**Семпл #63:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/zhorstkiy-disk-wd-purple-500gb-1tb-2tb-3tb-4tb-8tb-IDVoDwf.html",
  "title": "Жорсткий диск WD Purple 500Gb, 1TB, 2TB, 3TB, 4TB, 8TB"
}
```
**Семпл #64:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/ssd-nakopichuvach-kingston-a400-960-gb-sa400s37-960g-ID10Y86U.html",
  "title": "SSD накопичувач Kingston A400 960 GB (SA400S37/960G)"
}
```
**Семпл #65:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Одно колесо б/у . MICHELIN . 205/55R16. 91H."
}
```
**Семпл #66:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/ssd-disk-m-2-nvme-sk-hynix-pc711-512gb-perevreniy-vdmnniy-stan-ID10XFaa.html",
  "title": "SSD диск M.2 NVMe SK hynix PC711 512GB – перевірений, відмінний стан"
}
```
**Семпл #67:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/ssd-m2-nvme-128-gb-250gb-480gb-1-tb-samsung-hunix-toshiba-perehdniki-do-kompyutera-pci-e-ta-operativna-pamyat-ram-ID102Fzz.html",
  "title": "SSD m2 NVME 128 Гб, 250Gb 480Gb 1 tb Samsung Hunix Toshiba, є перехідники до компютера PCI e та  оперативна память RAM"
}
```
**Семпл #68:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/ssd-bestoss-2-5-sata-120-256-512gb-IDU1Wsi.html",
  "title": "Ssd Bestoss (2.5 Sata) 120,256,512gb"
}
```
**Семпл #69:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/ssd-samsung-850-pro-512gb-hdd-wd-1tb-green-IDZqWyC.html",
  "title": "SSD Samsung 850 Pro 512GB,  HDD WD 1TB Green"
}
```
**Семпл #70:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Ретро жорсткий диск IBM Deskstar IC35L020AVER07-0 на 20гб"
}
```
**Семпл #71:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Продається ретро жорсткий диск Samsung WN310820A, на 1.8  ГБ."
}
```
**Семпл #72:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Ретро жесткий диск MFM Miniscribe M8425"
}
```
**Семпл #73:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/zhorstkiy-disk-seagate-skyhawk-surveillance-8tb-st8000vx0022-IDYvNMe.html",
  "title": "Жорсткий диск Seagate SkyHawk Surveillance 8TB - ST8000VX0022"
}
```
**Семпл #74:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Жорсткий диск Тoshiba X300 (HDD) - HDWR180XZSTA"
}
```
**Семпл #75:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/zhorstk-diski-3-5-6tb-hp-enterprise-7200rpm-sata3-ID10TFBD.html",
  "title": "Жорсткі диски 3.5’ 6TB HP Enterprise 7200RPM SATA3"
}
```
**Семпл #76:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/zhorstkiy-disk-seagate-ironwolf-pro-14tb-7200rpm-st14000ne0008-ctan-novogo-ID10Rk25.html",
  "title": "Жорсткий диск Seagate IronWolf Pro 14TB 7200rpm (ST14000NE0008) Cтан нового"
}
```
**Семпл #77:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/prodam-zhestkiy-disk-8-tb-IDWMt2H.html",
  "title": "Продам жесткий диск 8 тб"
}
```
**Семпл #78:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Жорсткий диск Seagate 40 gb"
}
```
**Семпл #79:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "750гб вінчестер для ноута"
}
```
**Семпл #80:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Продам жорсткий диск"
}
```
**Семпл #81:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/zhestkiy-disk-ssd-120gb-hdd-1-5tb-500-320gb-ID10YoN8.html",
  "title": "Жёсткий диск SSD 120Gb  HDD 1.5Tb 500 320Gb"
}
```
**Семпл #82:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/seagate-barracuda-pro-10tb-hdd-sata-iii-7200-rpm-ID10M8ny.html",
  "title": "Seagate BarraCuda Pro 10TB HDD SATA III 7200 RPM"
}
```
**Семпл #83:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/m-2-ssd-disk-512gb-micron-2300-z-buferom-nvme-pci-e-3-0-x4-trade-in-ID108oiC.html",
  "title": "M.2 SSD диск 512GB Micron 2300 з буфером (NVMe\\PCI-e 3.0 x4). Trade-IN"
}
```
**Семпл #84:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Жорсткий диск Western Digital Purple 4 ТБ"
}
```
**Семпл #85:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/ssd-samsung-sm863-1-9tb-2tb-nadyn-ssd-diski-IDZTlD6.html",
  "title": "Ssd Samsung SM863 1.9tb 2tb Надійні ssd диски"
}
```
**Семпл #86:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "АКЦІЯ!!! Кабель SATA 3.0 ОПТ !!"
}
```
**Семпл #87:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/ssd-nakopichuvach-crucial-bx500-2tb-sata-iii-3-roki-garant-ID10X9sy.html",
  "title": "SSD накопичувач Crucial BX500 2TB Sata III (3 роки гарантії)"
}
```
**Семпл #88:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Жесткий диск HDD 2,0Tb TOSHIBA 64Mb"
}
```
**Семпл #89:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/ssd-goodram-px500-gen-3-nvme-m-2-2280-512gb-z-garantyu-36-msyatsv-ID10T5vw.html",
  "title": "SSD GOODRAM PX500 Gen.3 NVMe M.2 2280 512GB із гарантією 36 місяців"
}
```
**Семпл #90:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/ssd-sk-hynix-pc711-1tb-nvme-m-2-gen3x4-ID110CTN.html",
  "title": "SSD SK Hynix PC711 1Tb NVMe M.2 Gen3x4"
}
```
**Семпл #91:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Жорсткий диск 3.5\" TOSHIBA, SAMSUNG, ST, WDC"
}
```
**Семпл #92:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/ssd-kingston-nv3-1tb-m-2-97-ID10WvQV.html",
  "title": "SSD Kingston NV3 1TB M.2  (97%)"
}
```
**Семпл #93:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Вінчестери HDD SATA"
}
```
**Семпл #94:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/zhorstkiy-disk-toshiba-pc-p300-500-gb-sata-3-5-7200-ob-hv-ID10LIwz.html",
  "title": "Жорсткий диск Toshiba PC P300 500 ГБ SATA 3.5\" 7200 об/хв"
}
```
**Семпл #95:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Жесткий диск HDD Toshiba 3 ТБ в кармане USB 3.0"
}
```
**Семпл #96:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/ssd-samsung-sm863-1-9tb-2tb-nadyn-ssd-diski-IDZTlD6.html",
  "title": "Ssd Samsung SM863 1.9tb 2tb Надійні ssd диски"
}
```
**Семпл #97:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Внешний жёсткий диск wd elements 1.5 Тб. Хорошее состояние."
}
```
**Семпл #98:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/m-2-ssd-disk-1tb-adata-legend-850-5000mb-s-nvme-trade-in-ID10LCct.html",
  "title": "M.2 SSD диск 1TB ADATA Legend 850 (5000MB\\s. NVMe). Trade-IN"
}
```
**Семпл #99:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/tihiy-zhorstkiy-disk-6tb-wd-purple-wd60purz-sata3-5400rpm-64mb-kesh-ID10LC1R.html",
  "title": "тихий Жорсткий диск 6TB WD Purple WD60PURZ SATA3\\5400RPM\\64MB кеш"
}
```
**Семпл #100:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Жорсткі диски hdd 2,5” (для ноутбуків, компʼютерів)"
}
```

#### 📟 Оперативна пам'ять — Відсіяно (100):
**Семпл #1:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/operativna-pamyat-g-skill-trident-z5-neo-rgb-ddr5-6000-32gb-f5-6000j3038f16gx2-tz5nr-ID10Xs9y.html",
  "title": "Оперативна память G.Skill Trident Z5 Neo RGB DDR5-6000 32GB (F5-6000J3038F16GX2-TZ5NR)"
}
```
**Семпл #2:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/operativna-pamyat-samsung-m425r1gb4pb0-8gb-so-dimm-ddr5-5600mhz-nova-oem-klkst-garantya-ID10TEHV.html",
  "title": "Оперативна память Samsung M425R1GB4PB0 8GB SO-DIMM DDR5 5600MHz НОВА OEM (є кількість) + Гарантія"
}
```
**Семпл #3:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Kingston furry 32gb 3200 LED"
}
```
**Семпл #4:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/operativnaya-pamyat-ddr3-8gb-4gb-2gb-ddr2-IDWr1oC.html",
  "title": "оперативная память DDR3 8гб 4Gb 2гб DDR2"
}
```
**Семпл #5:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "SSD Patriot 1T NEW"
}
```
**Семпл #6:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "DDR3 2GB 1600 MHz (PC3-12800) Kingston HyperX KHX1600C9D3K2/4GX"
}
```
**Семпл #7:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Нова оперативна память на чипах Hynix 16gb (2×8)  DDR 4"
}
```
**Семпл #8:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/operativna-pamyat-kingston-hyperx-32-gb-ddr4-ID110GBz.html",
  "title": "Оперативна память Kingston і HyperX 32 gb ddr4"
}
```
**Семпл #9:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/48gb-ddr5-6000mhz-cl30-ID110Gzv.html",
  "title": "48gb ddr5 6000mhz cl30"
}
```
**Семпл #10:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/g-skill-trident-z5-rgb-ddr5-7200-32gb-2x16gb-cl34-ID10b8CF.html",
  "title": "G.SKILL Trident Z5 RGB DDR5 -7200 32GB (2x16GB) CL34"
}
```
**Семпл #11:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/teamgroup-rgb-ddr4-16gb-2x8-2666mhz-cl15-operativna-pamyat-ID10STtD.html",
  "title": "TeamGroup RGB DDR4 16GB (2X8) 2666Mhz CL15 Оперативна память"
}
```
**Семпл #12:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Оперативная память для ПК"
}
```
**Семпл #13:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Оперативна паметь"
}
```
**Семпл #14:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/operativna-pamyat-ddr3-g-skill-sniper-8gb-2x4gb-1600mhz-IDYF8yG.html",
  "title": "Оперативна память DDR3 G.Skill Sniper 8Gb (2x4gb) 1600MHz"
}
```
**Семпл #15:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "память DDR2 - 1 GB, 800Mh для ПК"
}
```
**Семпл #16:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Оперативна память"
}
```
**Семпл #17:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Оперативная память OCZ DDR2 2 Gb"
}
```
**Семпл #18:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Kingston Fury Renegade NVMe M.2  на 1тб"
}
```
**Семпл #19:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "оперативна память"
}
```
**Семпл #20:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/goodram-8gb-ddr3-ID110FYP.html",
  "title": "GoodRam 8gb ddr3"
}
```
**Семпл #21:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/operativna-pamyat-z-rgb-pdsvtkoyu-adata-xpg-spectrix-d35g-rgb-ddr4-16gb-3600mhz-cl18-stan-novo-ID10Sd7r.html",
  "title": "Оперативна память  з RGB підсвіткою ADATA XPG Spectrix D35G RGB DDR4 16GB 3600MHz CL18 Стан нової"
}
```
**Семпл #22:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/grova-operativna-pamyat-xpg-ddr4-32gb-2x16gb-tsna-vkazana-za-2-shtuki-3200mhz-ID100565.html",
  "title": "Ігрова Оперативна память XPG DDR4 32GB 2x16GB ціна вказана за 2 штуки. 3200MHz"
}
```
**Семпл #23:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Оперативна память (hynix 2gb 1Rx8 PC3) і (Kingston 2Gb DDR3 1333 Mhz)"
}
```
**Семпл #24:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/kingston-fury-impact-32gb-ddr4-kf426s15ib1k2-32-ID10P9rk.html",
  "title": "Kingston FURY Impact 32Gb DDR4  KF426S15IB1K2/32"
}
```
**Семпл #25:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/pamyat-ddr5-dlya-pk-64gb-2x32-5600mhz-exceleram-trade-in-ID10e0ew.html",
  "title": "память DDR5 для ПК 64GB (2x32) 5600MHz EXCELERAM. Trade-IN"
}
```
**Семпл #26:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Оперативна память Crucial Ballistix 16 GB (2x8 GB) 3600 MHz"
}
```
**Семпл #27:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/kingston-ddr4-32gb-216gb-ID110FAS.html",
  "title": "Kingston DDR4 32GB (2×16GB)"
}
```
**Семпл #28:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/corsair-ddr3-xms-3-4gb-1600mhz-IDZwzlp.html",
  "title": "Corsair DDR3 XMS 3 4Gb 1600Mhz"
}
```
**Семпл #29:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Оперативна память DDR2 NANYA 1GB 1Rx8 PC2-6400U-666-13-D1.800"
}
```
**Семпл #30:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/ozu-takems-8gb-ddr3-1-2-1333-mgts-ID110FsC.html",
  "title": "ОЗУ-TakeMS 8gb ddr3 1/2 1333 МГц"
}
```
**Семпл #31:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/crucial-ddr4-16gb-28gb-ID110Fpt.html",
  "title": "Crucial DDR4 16GB (2×8GB)"
}
```
**Семпл #32:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/operativna-pamyat-netac-shadow-iii-ddr4-16gb-2x8gb-3200mhz-cl16-nova-ID10Yu0S.html",
  "title": "Оперативна память Netac Shadow III DDR4 16GB (2x8GB) 3200MHz CL16. Нова."
}
```
**Семпл #33:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/operativna-pamyat-ddr4-16gb-2x8gb-ID10OEAz.html",
  "title": "Оперативна память DDR4 16GB 2x8GB"
}
```
**Семпл #34:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/ddr1-ddr2-ddr3-operativnaya-pamyat-1gb-2gb-4gb-8gb-IDQDZVb.html",
  "title": "DDR1, DDR2, DDR3 оперативная память (1gb, 2gb, 4gb, 8gb)"
}
```
**Семпл #35:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Оперативна память DDR 2"
}
```
**Семпл #36:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/serverna-operativna-pamyat-rdimm-ecc-ddr3-4-4-8-16gb-1333-2666mgts-IDYVZDZ.html",
  "title": "Серверна оперативна память RDIMM ECC DDR3/4 4/8/16Gb 1333-2666Мгц"
}
```
**Семпл #37:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/fusion-io-drive-320gb-ssd-ID110FfZ.html",
  "title": "Fusion - io Drive 320Gb ssd"
}
```
**Семпл #38:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Sandisk 1300 ioMemory"
}
```
**Семпл #39:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/modul-pamyat-dlya-noutbuka-sodimm-ddr4-64gb-2x32gb-3200-mhz-fury-impact-kingston-fury-ex-hyperx-kf432s20ibk2-64-nova-ID10S233.html",
  "title": "Модуль памяті для ноутбука SoDIMM DDR4 64GB (2x32GB) 3200 MHz Fury Impact Kingston Fury (ex.HyperX) (KF432S20IBK2/64) (Нова)"
}
```
**Семпл #40:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/pamyat-ddr4-32gb-2x16gb-3200mhz-g-skill-ripjaws-v-odna-planka-ne-pratsyu-trade-in-ID10s76C.html",
  "title": "память DDR4 32GB (2x16GB) 3200MHz G.Skill RipJaws V одна планка не працює. Trade-IN"
}
```
**Семпл #41:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/sk-hynix-16gb-ecc-ddr4-2400-pc4-19200r-reg-serverna-IDZElTJ.html",
  "title": "SK hynix 16GB ECC DDR4 2400 PC4-19200R Reg серверна"
}
```
**Семпл #42:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/novaya-g-skill-tridentz-rgb-32gb-4x8gb-ddr4-3200-f4-3200c16q-32gtzr-olx-dostavka-v-tsene-ID102Abp.html",
  "title": "Новая G.Skill TridentZ RGB 32GB (4x8GB) DDR4-3200 F4-3200C16Q-32GTZR, OLX доставка в цене!"
}
```
**Семпл #43:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/g-skill-ddr5-6000-96-gb-kit-of-2x49152-ID10QXag.html",
  "title": "G.Skill DDR5-6000 96 GB (Kit of 2x49152)"
}
```
**Семпл #44:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/novaya-ddr3-8gb-1600mhz-12800u-intel-amd-operativnaya-pamyat-dlya-pk-IDJXL1m.html",
  "title": "НОВАЯ DDR3 8GB 1600mhz 12800U Intel/AMD оперативная память для ПК"
}
```
**Семпл #45:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/modul-pamyat-kingston-fury-32gb-2x16gb-ddr4-3600-mhz-beast-rgb-ID10OHI2.html",
  "title": "Модуль памяті Kingston FURY 32Gb (2x16Gb) DDR4 3600 MHz Beast RGB"
}
```
**Семпл #46:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/operativna-pamyat-ozu-ram-kingston-ddr4-16gb-2400mhz-ID10r3Yd.html",
  "title": "Оперативна память ОЗУ RAM Kingston DDR4 16GB 2400Mhz"
}
```
**Семпл #47:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/prodam-ssd-1tb-2tb-4tb-8tb-ssd-m2-2tb-IDYYVJs.html",
  "title": "Продам  SSD 1TB / 2TB / 4TB /  8TB  |      SSD M2   2TB"
}
```
**Семпл #48:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Оперативная память  PC3 4gb"
}
```
**Семпл #49:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/operativnaya-pamyat-16gb-odna-plashka-ddr4-2666mhz-ID110Exd.html",
  "title": "Оперативная память 16gb , одна плашка ddr4 2666mhz"
}
```
**Семпл #50:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Оперативна память Kingston HyperX 8 GB (2x4GB) KHX24C11T1K2/8X"
}
```
**Семпл #51:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Продам оперативну пам’ять G.Skill 16 ГБ (2×8 ГБ)"
}
```
**Семпл #52:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Опиративная память. ОЗУ DDR 4.   4 Gb"
}
```
**Семпл #53:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Оперативна памʼять 8 ГБ дд4"
}
```
**Семпл #54:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Оперативная память TeamGroup 2888mhz"
}
```
**Семпл #55:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Оперативная память"
}
```
**Семпл #56:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Kingston Fury Renegade NVMe M.2  на 1тб"
}
```
**Семпл #57:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/prodam-operativnu-pamyat-32gb-ddr4-termnovo-ID10YlHe.html",
  "title": "Продам оперативну пам’ять 32gb ddr4! Терміново!"
}
```
**Семпл #58:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Память ОЗУ 2GB Adata"
}
```
**Семпл #59:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/operativna-pamyat-ddr3-1-2-4-8gb-1333-1600-1866mhz-IDVCVuF.html",
  "title": "Оперативна память DDR3 1/2/4/8Gb 1333/1600/1866MHz"
}
```
**Семпл #60:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Ddr 3  SODIMM 4gb для ноутбука комплект"
}
```
**Семпл #61:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Серверна память SAMSUNG DDR3 32ГБ M386B4G70DM0-YK04 4Rx4"
}
```
**Семпл #62:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Память DDR 3 4 gb 1600"
}
```
**Семпл #63:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Память оперативная 2 Гб pc3-10600s-9-10-b10"
}
```
**Семпл #64:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Kingston Fury Beast White ddr 5 2x16gb cl32-39-39"
}
```
**Семпл #65:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Модуль памяті 1 Gb.,ddr 2"
}
```
**Семпл #66:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Диск 1 Тбайт чистый"
}
```
**Семпл #67:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "оперативна памʼять PATRIOT 16GB (2x8) 3200Mhz (PV416G320C6K)"
}
```
**Семпл #68:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/operativna-pamyat-transcend-ddr5-64gb-2x32gb-5600mhz-ID10YNFp.html",
  "title": "Оперативна память Transcend DDR5 64GB (2x32GB) 5600MHz"
}
```
**Семпл #69:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/amd-radeon-ddr4-16gb-2400-mhz-operativna-pamyat-ID10G4Mo.html",
  "title": "AMD RADEON DDR4 16GB  2400 Mhz Оперативна память"
}
```
**Семпл #70:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/operativnaya-pamyat-kingston-fury-beast-2x32-gb-64gb-ID10Z3WB.html",
  "title": "Оперативная память kingston fury  beast  2x32 gb (64gb)"
}
```
**Семпл #71:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Оперативна память для ноутбука Kingston ddr4 3200mhz cl20"
}
```
**Семпл #72:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Оперативна пам‘ять память 1 гб 1 gb"
}
```
**Семпл #73:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/operativna-pamyat-samsung-m425r1gb4pb0-8gb-so-dimm-ddr5-5600mhz-nova-oem-klkst-garantya-ID10TEHV.html",
  "title": "Оперативна память Samsung M425R1GB4PB0 8GB SO-DIMM DDR5 5600MHz НОВА OEM (є кількість) + Гарантія"
}
```
**Семпл #74:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Память для сервера ddr2 HYNIX 1Gb 2Rx8 PC2-5300F-555-11"
}
```
**Семпл #75:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/operativna-pamyat-ddr4-16-8gb-corsair-vengeance-hyperx-komplekti-ta-poshtuchno-ID10l3vS.html",
  "title": "Оперативна память DDR4- 16/8gb Corsair Vengeance / HyperX (Комплекти та поштучно)"
}
```
**Семпл #76:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "ОЗУ DDR 4 8гб so-dimm для ноутбука"
}
```
**Семпл #77:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Оперативна память в ноутбук DDR2"
}
```
**Семпл #78:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Оперативна память Kingston Fury DDR4-3200 65536 MB PC4-25600 (Kit of 2x32768) Beast Black (KF432C16BBK2/64)"
}
```
**Семпл #79:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "4 шт. серверна/powermac оперетивня память ddr2 PC2 4gb"
}
```
**Семпл #80:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/servernaya-pamyat-32gb-2rx4-ddr4-pc4-2133p-ecc-reg-ID10vzRS.html",
  "title": "Серверная память 32Gb 2Rx4 DDR4 PC4-2133P ECC REG"
}
```
**Семпл #81:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/ddr4-32gb-16-16-2400-mhz-cl16-amd-radeon-memory-ID10Zicq.html",
  "title": "DDR4 32GB [16+16] 2400 Mhz CL16 AMD Radeon Memory"
}
```
**Семпл #82:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Оперативна память Samsung DDR5 5600"
}
```
**Семпл #83:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/kingston-ddr4-16gb-2h8-3200mhz-cl22-so-dimm-operativna-pamyat-ID10Rp5T.html",
  "title": "Kingston DDR4 16GB (2х8) 3200Mhz CL22 SO-DIMM Оперативна память"
}
```
**Семпл #84:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "DDR 5 5600 32 GB"
}
```
**Семпл #85:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Оперативна память Kingston fury beast 3200, 2по 8GB,"
}
```
**Семпл #86:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Продам планку оперативної пам’яті DDR3 1333 MHz 1.5V 240pinKingstek4GB"
}
```
**Семпл #87:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/ssd-disk-msi-spatium-m371-500gb-nvme-m-2-2280-z-garantyu-5-rokv-ID10ZhNf.html",
  "title": "SSD диск MSI Spatium M371 500GB NVMe M.2 2280 з гарантією 5 років"
}
```
**Семпл #88:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/modul-pamyat-operativna-pamyat-dlya-kompyutera-ddr4-32gb-2x16gb-3600-mhz-fury-renegade-black-kingston-fury-ex-hyperx-kf436c16rb12k2-32-ID10Yqw6.html",
  "title": "Модуль памяті (оперативна памʼять) для компютера DDR4 32GB (2x16GB) 3600 MHz Fury Renegade Black Kingston Fury (ex.HyperX) (KF436C16RB12K2/32)"
}
```
**Семпл #89:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/serverna-pamyat-ddr5-64gb-2rx4-pc5-5600b-ecc-reg-5600mhz-ID10Xc45.html",
  "title": "Серверна память DDR5 64Gb 2Rx4 PC5-5600B ECC REG 5600Mhz"
}
```
**Семпл #90:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/prodam-operativnu-pamyat-32gb-ddr4-termnovo-ID10YlHe.html",
  "title": "Продам оперативну пам’ять 32gb ddr4! Терміново!"
}
```
**Семпл #91:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Продам оперативную память DDR 3 4X2"
}
```
**Семпл #92:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Оперативна память для пк ddr2 2gb"
}
```
**Семпл #93:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/komplektuyuch-dlya-pk-osnova-dlya-kompyutera-pd-podalshu-zbrku-montor-intel-i5-10600kf-32gb-ddr4-hyperx-3200mhz-groviy-pk-kompyuter-kompyuter-ID10YkXP.html",
  "title": "Комплектуючі для пк, основа для компютера під подальшу збірку + монітор. intel i5-10600KF 32ГБ DDR4 HyperX 3200MHz, ігровий пк, компютер, компютер"
}
```
**Семпл #94:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Оперативная память для ноутбука SODIMM"
}
```
**Семпл #95:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/ozp-kingston-ddr4-16gb-2x8gb-3600mhz-fury-beast-black-ID10Z1QU.html",
  "title": "ОЗП Kingston DDR4 16GB (2x8GB) 3600Mhz FURY Beast Black"
}
```
**Семпл #96:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/top-pamyat-ddr4-32gb-2x16-4400mhz-g-skill-tridentz-rgb-trade-in-IDZWXYH.html",
  "title": "ТОП память DDR4 32GB (2x16) 4400MHz G.Skill TridentZ RGB. Trade-in"
}
```
**Семпл #97:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/g-skill-ddr5-6000-96-gb-kit-of-2x49152-ID10QXag.html",
  "title": "G.Skill DDR5-6000 96 GB (Kit of 2x49152)"
}
```
**Семпл #98:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Продам оперативну память GLOWAY DDR5 24GB (2x12GB) 5600 MT/s Біла (Б/В)"
}
```
**Семпл #99:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/operativna-pamyat-g-skill-trident-z-rgb-ddr4-4266-mhz-16-gb-2-x-8-gb-samsung-b-die-intel-ryzen-operativka-kingston-ID10QJZ3.html",
  "title": "Оперативна память G.skill Trident Z Rgb DDR4 4266 Mhz 16 Gb 2 x 8 gb Samsung b-die Intel ryzen оперативка kingston"
}
```
**Семпл #100:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Оперативная память Kingston HX318C10FBK2/8"
}
```

#### 📦 Комплекти — Відсіяно (0):

### 🎯 Успішно розпізнані моделі:
#### 🎮 Відеокарти (GPU) — Розпізнано (82):
**Зразок #1:**
```json
{
  "raw_title": "Відеокарта Inno3D GeForce RTX 2060 Super 8GB GDDR6",
  "matched_target": "rtx_2060_super",
  "price_uah": 7000
}
```
**Зразок #2:**
```json
{
  "raw_title": "Відеокарта AFOX PCI-E GeForce GT 710 2048 MB DDR3",
  "matched_target": "gt_710",
  "price_uah": 805
}
```
**Зразок #3:**
```json
{
  "raw_title": "Radeon rx580 8gb red devil",
  "matched_target": "rx_580",
  "price_uah": 2699
}
```
**Зразок #4:**
```json
{
  "raw_title": "(НЕ РОБОЧА)Відеокарта hd 7850 2 gb gddr5",
  "matched_target": "hd_7850",
  "price_uah": 300
}
```
**Зразок #5:**
```json
{
  "raw_title": "Комплект ASUS 750ti + M5A7BL-M LX3 +AMD FX 4300 под восстановление",
  "matched_target": "bundle_fx_4300_gtx_750_ti",
  "price_uah": 444
}
```
**Зразок #6:**
```json
{
  "raw_title": "Видеокарта,Rx5700,ASUS DUAL OC",
  "matched_target": "rx_5700",
  "price_uah": 6000
}
```
**Зразок #7:**
```json
{
  "raw_title": "Відеокарта Rx 580",
  "matched_target": "rx_580",
  "price_uah": 4000
}
```
**Зразок #8:**
```json
{
  "raw_title": "Видеокарта Rx5700XT,Gigabyte oc",
  "matched_target": "rx_5700_xt",
  "price_uah": 6000
}
```
**Зразок #9:**
```json
{
  "raw_title": "Відеокарта GIGABYTE GeForce RTX4060 8Gb EAGLE OC (GV-N4060EAGLE OC-8GD)",
  "matched_target": "rtx_4060",
  "price_uah": 14000
}
```
**Зразок #10:**
```json
{
  "raw_title": "Видеокарта XFX PCI-Ex Radeon RX 6600 Speedster SWFT 210 8GB GDDR6 (128bit) (1626/14000) (HDMI, 3 x DisplayPort) (RX-66XL8LFDQ)",
  "matched_target": "rx_6600",
  "price_uah": 7500
}
```
**Зразок #11:**
```json
{
  "raw_title": "MSI GTX 1650 SUPER Gaming X 4GB GDDR6 GeForce",
  "matched_target": "gtx_1650_super",
  "price_uah": 4499
}
```
**Зразок #12:**
```json
{
  "raw_title": "Видеокарта MSI GeForce GTX 970 Gaming 4GB GDDR5 (256bit) PCI-E 3.0",
  "matched_target": "gtx_970",
  "price_uah": 2800
}
```
**Зразок #13:**
```json
{
  "raw_title": "GTX560TI 1GB GDDR5 в хорошому стані",
  "matched_target": "gtx_560_ti",
  "price_uah": 550
}
```
**Зразок #14:**
```json
{
  "raw_title": "MSI AMD Radeon RX 5700 MECH OC 8GB GDDR6 Робоча",
  "matched_target": "rx_5700",
  "price_uah": 6500
}
```
**Зразок #15:**
```json
{
  "raw_title": "Sapphire Radeon RX 570 8GB",
  "matched_target": "rx_570",
  "price_uah": 2550
}
```
**Зразок #16:**
```json
{
  "raw_title": "Видеокарта GeForce GT 1030 2GB MSI Aero ITX OC DDR5",
  "matched_target": "gt_1030",
  "price_uah": 1800
}
```
**Зразок #17:**
```json
{
  "raw_title": "Видеокарта NVIDIA MSI GTX 950 2Gb",
  "matched_target": "gtx_950",
  "price_uah": 2399
}
```
**Зразок #18:**
```json
{
  "raw_title": "Видеокарта AMD Asus HD 6870 1Gb",
  "matched_target": "hd_6870",
  "price_uah": 1299
}
```
**Зразок #19:**
```json
{
  "raw_title": "Видеокарта Asus PCI-Ex Radeon RX550 2GB, рабочая",
  "matched_target": "rx_550",
  "price_uah": 1700
}
```
**Зразок #20:**
```json
{
  "raw_title": "запчасти / Донор / Охлаждение GeForce RTX 4090 GAMING X SLIM 24G",
  "matched_target": "rtx_4090",
  "price_uah": 8500
}
```
**Зразок #21:**
```json
{
  "raw_title": "Видеокарты Radeon HD7470 2Gb Gigabyte GeForce 8600 GT Inno3D FX5200",
  "matched_target": "bundle_fx_5200_fx_5200",
  "price_uah": 200
}
```
**Зразок #22:**
```json
{
  "raw_title": "Відеокарта  gt1030 4GB",
  "matched_target": "gt_1030",
  "price_uah": 4500
}
```
**Зразок #23:**
```json
{
  "raw_title": "Відеокарта ASUS PCI-Ex GeForce RTX 5070 Dual OC Edition 12GB GDDR7 (192bit) (2572/28000) (HDMI, 3 x DisplayPort) (DUAL-RTX5070-O12G)",
  "matched_target": "rtx_5070",
  "price_uah": 31600
}
```
**Зразок #24:**
```json
{
  "raw_title": "Відеокарта sapphire RX480 8GB",
  "matched_target": "rx_480",
  "price_uah": 3000
}
```
**Зразок #25:**
```json
{
  "raw_title": "Asus TUF RTX 3070 Gaming OC",
  "matched_target": "rtx_3070",
  "price_uah": 13500
}
```
**Зразок #26:**
```json
{
  "raw_title": "Відеокарта MSI RX 6600 XT",
  "matched_target": "rx_6600_xt",
  "price_uah": 9300
}
```
**Зразок #27:**
```json
{
  "raw_title": "Відеокарта MSI GeForce RTX 3090 VENTUS 3X OC 24GB GDDR6X (384bit) (HDMI, 3 x DisplayPort) Магазин CompiC",
  "matched_target": "rtx_3090",
  "price_uah": 42000
}
```
**Зразок #28:**
```json
{
  "raw_title": "Видеокарта Gtx 1050Ti",
  "matched_target": "gtx_1050_ti",
  "price_uah": 2984
}
```
**Зразок #29:**
```json
{
  "raw_title": "Відеокарта nvidia gtx  670 GIGABYTE",
  "matched_target": "gtx_670",
  "price_uah": 600
}
```
**Зразок #30:**
```json
{
  "raw_title": "Видеокарта AURUS GTX 1080 Ti 11 Gb Любые тесты! Магазин COMPiC",
  "matched_target": "gtx_1080_ti",
  "price_uah": 7400
}
```
**Зразок #31:**
```json
{
  "raw_title": "RTX 2070 MSI Ventus Несправна",
  "matched_target": "rtx_2070",
  "price_uah": 3000
}
```
**Зразок #32:**
```json
{
  "raw_title": "Відеокарта RTX3050 8gb Asus",
  "matched_target": "rtx_3050",
  "price_uah": 8500
}
```
**Зразок #33:**
```json
{
  "raw_title": "Відеокарта MSI GeForce GT 740 2GB DDR3 (N740-2GD3) Робоча",
  "matched_target": "gt_740",
  "price_uah": 800
}
```
**Зразок #34:**
```json
{
  "raw_title": "Відеокарта R5 230 afox 2gb gddr3 робоча",
  "matched_target": "r5_230",
  "price_uah": 1000
}
```
**Зразок #35:**
```json
{
  "raw_title": "Відеокарта - NVIDIA GeForce GTX 1070 8 ГБ GDDR5",
  "matched_target": "gtx_1070",
  "price_uah": 4899
}
```
**Зразок #36:**
```json
{
  "raw_title": "Продам Rtx 3050 6gb",
  "matched_target": "rtx_3050",
  "price_uah": 11000
}
```
**Зразок #37:**
```json
{
  "raw_title": "RTX 3080 TI zotac",
  "matched_target": "rtx_3080_ti",
  "price_uah": 19999
}
```
**Зразок #38:**
```json
{
  "raw_title": "Відееарта gtx  1660super 6gb 192bit від PALIT",
  "matched_target": "gtx_1660_super",
  "price_uah": 5700
}
```
**Зразок #39:**
```json
{
  "raw_title": "Відеокарта GTX 1650",
  "matched_target": "gtx_1650",
  "price_uah": 3500
}
```
**Зразок #40:**
```json
{
  "raw_title": "Відеокарта - AMD Radeon RX 6600 XT 8 ГБ GDDR6",
  "matched_target": "rx_6600_xt",
  "price_uah": 7199
}
```
**Зразок #41:**
```json
{
  "raw_title": "Radeon R9 280 3GB GDDR5 — Повний комплект (Box)під відновлення/ремонт",
  "matched_target": "r9_280",
  "price_uah": 970
}
```
**Зразок #42:**
```json
{
  "raw_title": "Відеокарта Asus GTX650 2Gb GDDR5",
  "matched_target": "gtx_650",
  "price_uah": 1400
}
```
**Зразок #43:**
```json
{
  "raw_title": "Видеокарта Asus Gtx780 3gb",
  "matched_target": "gtx_780",
  "price_uah": 1000
}
```
**Зразок #44:**
```json
{
  "raw_title": "Відеокарта Galax GeForce GTX950 2Gb GDDR5 DVI HDMI OEM",
  "matched_target": "gtx_950",
  "price_uah": 2300
}
```
**Зразок #45:**
```json
{
  "raw_title": "Відеокарта - AMD Radeon RX 5700 XT 8 ГБ GDDR6",
  "matched_target": "rx_5700_xt",
  "price_uah": 6299
}
```
**Зразок #46:**
```json
{
  "raw_title": "ASUS ROG Strix GeForce RTX 3090 24GB",
  "matched_target": "rtx_3090",
  "price_uah": 41499
}
```
**Зразок #47:**
```json
{
  "raw_title": "Радиатор с кулером Radeon R9 390 Gigabyte",
  "matched_target": "r9_390",
  "price_uah": 531
}
```
**Зразок #48:**
```json
{
  "raw_title": "RTX 6070 видеокарта/відеокарта",
  "matched_target": "rtx_6070",
  "price_uah": 67000
}
```
**Зразок #49:**
```json
{
  "raw_title": "Відеокарта HD7750 2048MB, б/у",
  "matched_target": "hd_7750",
  "price_uah": 799
}
```
**Зразок #50:**
```json
{
  "raw_title": "Продам коробку от видеокарты MSI RADEON RX 480 4GB",
  "matched_target": "rx_480",
  "price_uah": 99
}
```
**Зразок #51:**
```json
{
  "raw_title": "Відеокарта - NVIDIA GeForce RTX 4060 8 ГБ GDDR6",
  "matched_target": "rtx_4060",
  "price_uah": 11999
}
```
**Зразок #52:**
```json
{
  "raw_title": "ASUS Rog Strix GTX 1070 8GB",
  "matched_target": "gtx_1070",
  "price_uah": 4612
}
```
**Зразок #53:**
```json
{
  "raw_title": "AMD Radeon RX 7900 XTX 24GB GDDR6 — потужна відеокарта для 2K/4K",
  "matched_target": "rx_7900_xtx",
  "price_uah": 32500
}
```
**Зразок #54:**
```json
{
  "raw_title": "Palit GeForce RTX 4070 Ti SUPER GamingPro OC",
  "matched_target": "rtx_4070_ti_super",
  "price_uah": 23700
}
```
**Зразок #55:**
```json
{
  "raw_title": "Asus GeForce GTX 650",
  "matched_target": "gtx_650",
  "price_uah": 400
}
```
**Зразок #56:**
```json
{
  "raw_title": "Видеокарта GTX 1080ti",
  "matched_target": "gtx_1080_ti",
  "price_uah": 5500
}
```
**Зразок #57:**
```json
{
  "raw_title": "PowerColor Hellhound AMD Radeon RX 7900 XT 20GB",
  "matched_target": "rx_7900_xt",
  "price_uah": 28500
}
```
**Зразок #58:**
```json
{
  "raw_title": "GeForce 960 GTX 4gb",
  "matched_target": "gtx_960",
  "price_uah": 2500
}
```
**Зразок #59:**
```json
{
  "raw_title": "Gigabyte RTX 4060 WINDFORCE OC 8G",
  "matched_target": "rtx_4060",
  "price_uah": 11700
}
```
**Зразок #60:**
```json
{
  "raw_title": "Видеокарта Radeon Sapphire RX470 8GB Samsung! (Много)",
  "matched_target": "rx_470",
  "price_uah": 2999
}
```
**Зразок #61:**
```json
{
  "raw_title": "MSI RTX 5070 Ventus 3X OC",
  "matched_target": "rtx_5070",
  "price_uah": 31500
}
```
**Зразок #62:**
```json
{
  "raw_title": "Видеокарта Gtx 760 2g msi рабочая",
  "matched_target": "gtx_760",
  "price_uah": 999
}
```
**Зразок #63:**
```json
{
  "raw_title": "Видеокарта Palit GeForce GTS 250 green 512 мб DDR3",
  "matched_target": "gts_250",
  "price_uah": 300
}
```
**Зразок #64:**
```json
{
  "raw_title": "Обмен Prime RTX 5080 на ПК",
  "matched_target": "rtx_5080",
  "price_uah": 0
}
```
**Зразок #65:**
```json
{
  "raw_title": "RX 570 4 gb Gigabyte",
  "matched_target": "rx_570",
  "price_uah": 1780
}
```
**Зразок #66:**
```json
{
  "raw_title": "Nvidia GeForce RTX 2070 8GB GDDR6",
  "matched_target": "rtx_2070",
  "price_uah": 15000
}
```
**Зразок #67:**
```json
{
  "raw_title": "Дві карти - ASUS ROG STRIX GTX 1070Ti 8Gb",
  "matched_target": "gtx_1070_ti",
  "price_uah": 8500
}
```
**Зразок #68:**
```json
{
  "raw_title": "GeForce GTX 750 Ti 2GB GDDR5 Inno3D",
  "matched_target": "gtx_750_ti",
  "price_uah": 900
}
```
**Зразок #69:**
```json
{
  "raw_title": "Продам відеокарту ASUS  Rog-Strix GeForceGTX1070Ті 1070 Ti",
  "matched_target": "gtx_1070_ti",
  "price_uah": 5500
}
```
**Зразок #70:**
```json
{
  "raw_title": "Відеокарта MSI Radeon RX 480 GAMING X 8G Б/в + Гарантія 3 місяці!",
  "matched_target": "rx_480",
  "price_uah": 3325
}
```
**Зразок #71:**
```json
{
  "raw_title": "Відеокарта GIGABYTE GeForce GTX1050 Ti 4096Mb",
  "matched_target": "gtx_1050_ti",
  "price_uah": 3500
}
```
**Зразок #72:**
```json
{
  "raw_title": "Відеокарта Sapphire Pure Radeon RX 9070 XT",
  "matched_target": "rx_9070_xt",
  "price_uah": 34000
}
```
**Зразок #73:**
```json
{
  "raw_title": "відеокарта rx 470 4gb",
  "matched_target": "rx_470",
  "price_uah": 500
}
```
**Зразок #74:**
```json
{
  "raw_title": "Nvidia GeForce RTX 3070 Founders Edition 8GB",
  "matched_target": "rtx_3070",
  "price_uah": 12800
}
```
**Зразок #75:**
```json
{
  "raw_title": "Rx 550 lp  4 gb red dragon",
  "matched_target": "rx_550",
  "price_uah": 3000
}
```
**Зразок #76:**
```json
{
  "raw_title": "AMD Radeon 1GB HD8350 64bit активное охлаждение.",
  "matched_target": "hd_8350",
  "price_uah": 690
}
```
**Зразок #77:**
```json
{
  "raw_title": "Відеокарта EVGA GeForce GTX 770 SC ACX",
  "matched_target": "bundle_770_gtx_770",
  "price_uah": 600
}
```
**Зразок #78:**
```json
{
  "raw_title": "Відеокарта Gainward GeForce GTX 650 Ti GS (Golden Sample) 1GB GDDR5",
  "matched_target": "gtx_650_ti",
  "price_uah": 700
}
```
**Зразок #79:**
```json
{
  "raw_title": "Відеокарта ASUS Prime OC RTX 5070 Ti 16GB з коробкою",
  "matched_target": "rtx_5070_ti",
  "price_uah": 46000
}
```
**Зразок #80:**
```json
{
  "raw_title": "Rx 550 (2gb) Asus",
  "matched_target": "rx_550",
  "price_uah": 1800
}
```
**Зразок #81:**
```json
{
  "raw_title": "Відеокарта ASUS Dual Radeon RX 6750 XT OC 12GB",
  "matched_target": "rx_6750_xt",
  "price_uah": 11500
}
```
**Зразок #82:**
```json
{
  "raw_title": "Відеокарта EVGA RTX 3090 24GB FTW3 ultra ТОП Монстр іі та 4К ігор. ТОП виробник EVGA, топ модель.",
  "matched_target": "rtx_3090",
  "price_uah": 45000
}
```

#### 🧠 Процесори (CPU) — Розпізнано (62):
**Зразок #1:**
```json
{
  "raw_title": "Комплект: материнська плата Asus ROG Strix Z690-E Gaming WiFi + Intel Core i5-13600K",
  "matched_target": "bundle_i5_13600k_z690",
  "price_uah": 15000
}
```
**Зразок #2:**
```json
{
  "raw_title": "Процессор AMD Ryzen 9 9900X 4.4 GHz/64MB Socket AM5",
  "matched_target": "ryzen_9_9900x",
  "price_uah": 14000
}
```
**Зразок #3:**
```json
{
  "raw_title": "Игоровой комплет на пк AMD Ryzen 7 5700X3D",
  "matched_target": "ryzen_7_5700x3d",
  "price_uah": 23000
}
```
**Зразок #4:**
```json
{
  "raw_title": "Процесор Ryzen 5 5600X 3.7(4.6)GHz 32MB sAM4 tray",
  "matched_target": "ryzen_5_5600x",
  "price_uah": 5600
}
```
**Зразок #5:**
```json
{
  "raw_title": "Процесор Ryzen 5 5600",
  "matched_target": "ryzen_5_5600",
  "price_uah": 3950
}
```
**Зразок #6:**
```json
{
  "raw_title": "Xeon 2670 v3 + материнка и башня DDR4",
  "matched_target": "xeon_e5_2670_v3",
  "price_uah": 3000
}
```
**Зразок #7:**
```json
{
  "raw_title": "Процесор Intel Core i5 3330",
  "matched_target": "i5_3330",
  "price_uah": 350
}
```
**Зразок #8:**
```json
{
  "raw_title": "Процессор AMD Ryzen 5 7500F Socket AM5 6 ядрер 5.0 ГГц можно с материнкой",
  "matched_target": "ryzen_5_7500f",
  "price_uah": 4700
}
```
**Зразок #9:**
```json
{
  "raw_title": "Процессор Intel Celeron G530 (LGA socket 1155)",
  "matched_target": "celeron_g530",
  "price_uah": 70
}
```
**Зразок #10:**
```json
{
  "raw_title": "Процессор Intel Pentium G3460 s1150",
  "matched_target": "pentium_g3460",
  "price_uah": 200
}
```
**Зразок #11:**
```json
{
  "raw_title": "Процесор AMD Ryzen 7 5800X (AM4)",
  "matched_target": "ryzen_7_5800x",
  "price_uah": 6900
}
```
**Зразок #12:**
```json
{
  "raw_title": "Intel Celeron G1840",
  "matched_target": "celeron_g1840",
  "price_uah": 120
}
```
**Зразок #13:**
```json
{
  "raw_title": "Intel Core i7-870 сокет 1156 процессоры",
  "matched_target": "bundle_i7_870_870",
  "price_uah": 599
}
```
**Зразок #14:**
```json
{
  "raw_title": "Продам i3 6100 Б/У",
  "matched_target": "i3_6100",
  "price_uah": 200
}
```
**Зразок #15:**
```json
{
  "raw_title": "Процессор Intel Celeron G1610",
  "matched_target": "celeron_g1610",
  "price_uah": 100
}
```
**Зразок #16:**
```json
{
  "raw_title": "Процесор Intel Core i5-11600K 3.9-4.9GHz 12MB LGA1200 (Box)",
  "matched_target": "i5_11600k",
  "price_uah": 5799
}
```
**Зразок #17:**
```json
{
  "raw_title": "AMD Ryzen 5 1600 процесор 6 ядер/12 потоків",
  "matched_target": "ryzen_5_1600",
  "price_uah": 2100
}
```
**Зразок #18:**
```json
{
  "raw_title": "Intel Xeon E5-2678 v3 SR20Z",
  "matched_target": "xeon_e5_2678_v3",
  "price_uah": 1000
}
```
**Зразок #19:**
```json
{
  "raw_title": "Процессор Fx-6300",
  "matched_target": "bundle_fx_6300_fx_6300",
  "price_uah": 550
}
```
**Зразок #20:**
```json
{
  "raw_title": "Intel core i5 9400f",
  "matched_target": "i5_9400f",
  "price_uah": 1990
}
```
**Зразок #21:**
```json
{
  "raw_title": "Fx4320 ам3+ ам3.",
  "matched_target": "bundle_fx_4320_fx_4320",
  "price_uah": 600
}
```
**Зразок #22:**
```json
{
  "raw_title": "Xeon E3 1240 v2 тот же i7 3770 и i7 3770K .Будет мощнее i7 2600K",
  "matched_target": "i7_3770",
  "price_uah": 1450
}
```
**Зразок #23:**
```json
{
  "raw_title": "Intel Core i5 7400 4x 3.5Ghz Socket 1151 Kaby Lake",
  "matched_target": "i5_7400",
  "price_uah": 850
}
```
**Зразок #24:**
```json
{
  "raw_title": "і5-8500 Intel Core 3.00 ghz процесор",
  "matched_target": "i5_8500",
  "price_uah": 1550
}
```
**Зразок #25:**
```json
{
  "raw_title": "Процесор AMD A8-3800 Series",
  "matched_target": "a8_3800",
  "price_uah": 1000
}
```
**Зразок #26:**
```json
{
  "raw_title": "Процессор Intel Core i5-14600Kf",
  "matched_target": "i5_14600kf",
  "price_uah": 10700
}
```
**Зразок #27:**
```json
{
  "raw_title": "Процесор Intel Core i5-7500 (сокет 1151)",
  "matched_target": "i5_7500",
  "price_uah": 1070
}
```
**Зразок #28:**
```json
{
  "raw_title": "Процессор Intel Core i7-8700 3,2GHz (Socket 1151 v2) Гарантия 1 год",
  "matched_target": "i7_8700",
  "price_uah": 3400
}
```
**Зразок #29:**
```json
{
  "raw_title": "Ryzen 7 5700x soyo b550 ddr4 16gb",
  "matched_target": "bundle_ryzen_7_5700x_b550",
  "price_uah": 11000
}
```
**Зразок #30:**
```json
{
  "raw_title": "Процесор Intel Pentium G4560 + Боксовий кулер",
  "matched_target": "pentium_g4560",
  "price_uah": 200
}
```
**Зразок #31:**
```json
{
  "raw_title": "Intel Haswell i7 4790 1150 (4770)",
  "matched_target": "i7_4790",
  "price_uah": 2000
}
```
**Зразок #32:**
```json
{
  "raw_title": "Топ Процессор на АМ4 Ryzen 7 5800X3D, рабочий. На гарантии",
  "matched_target": "ryzen_7_5800x3d",
  "price_uah": 15000
}
```
**Зразок #33:**
```json
{
  "raw_title": "Процессор - AMD A4-6300",
  "matched_target": "a4_6300",
  "price_uah": 350
}
```
**Зразок #34:**
```json
{
  "raw_title": "Продам Pentium G4560",
  "matched_target": "pentium_g4560",
  "price_uah": 300
}
```
**Зразок #35:**
```json
{
  "raw_title": "Процессоры:AMD Athlon II x2 250 и fm1-AMD A4-3300",
  "matched_target": "athlon_ii_x2_250",
  "price_uah": 130
}
```
**Зразок #36:**
```json
{
  "raw_title": "Intel Core i3-12100F (LGA1700)",
  "matched_target": "i3_12100f",
  "price_uah": 3100
}
```
**Зразок #37:**
```json
{
  "raw_title": "Процессор s1150 Intel® Core™ i3-4170 Processor\n3M Cache, 3.70 GHz",
  "matched_target": "i3_4170",
  "price_uah": 100
}
```
**Зразок #38:**
```json
{
  "raw_title": "Процесор AMD Ryzen 7 - 9800x3D | Нові",
  "matched_target": "ryzen_7_9800x3d",
  "price_uah": 17900
}
```
**Зразок #39:**
```json
{
  "raw_title": "Продам процесор  i7  7700",
  "matched_target": "i7_7700",
  "price_uah": 3200
}
```
**Зразок #40:**
```json
{
  "raw_title": "Amd ryzen 3 2200g",
  "matched_target": "ryzen_3_2200g",
  "price_uah": 700
}
```
**Зразок #41:**
```json
{
  "raw_title": "Сore i3 10105f - Сore i3 8100",
  "matched_target": "i3_10105f",
  "price_uah": 0
}
```
**Зразок #42:**
```json
{
  "raw_title": "Intel  i5-2310\n Процессор",
  "matched_target": "i5_2310",
  "price_uah": 600
}
```
**Зразок #43:**
```json
{
  "raw_title": "Процессор Intel Core i5-3470 4ядра 3.2-3.6GHz lga 1155 socket",
  "matched_target": "i5_3470",
  "price_uah": 680
}
```
**Зразок #44:**
```json
{
  "raw_title": "Процессор Intel Core i7-4790 (Socket LGA1150)",
  "matched_target": "i7_4790",
  "price_uah": 1700
}
```
**Зразок #45:**
```json
{
  "raw_title": "Процесор intel core i5 3470",
  "matched_target": "i5_3470",
  "price_uah": 1000
}
```
**Зразок #46:**
```json
{
  "raw_title": "Amd Ryzen 5 1600",
  "matched_target": "ryzen_5_1600",
  "price_uah": 1000
}
```
**Зразок #47:**
```json
{
  "raw_title": "Комплект: Intel Core i5-10400F + Asus PRIME H510M-A + Deepcool GAMMAXX 400K",
  "matched_target": "i5_10400f",
  "price_uah": 7500
}
```
**Зразок #48:**
```json
{
  "raw_title": "Ryzen 5 5500 використовувався 3 місяці не розганявся",
  "matched_target": "ryzen_5_5500",
  "price_uah": 2300
}
```
**Зразок #49:**
```json
{
  "raw_title": "Процессор Intel Celeron G1840 б.у. (Сокет 1150)",
  "matched_target": "celeron_g1840",
  "price_uah": 122
}
```
**Зразок #50:**
```json
{
  "raw_title": "Ryzen 3 1200 BOX",
  "matched_target": "ryzen_3_1200",
  "price_uah": 500
}
```
**Зразок #51:**
```json
{
  "raw_title": "Процессор Intel Core i7-6700K 4,0GHz (Socket 1151) Гарантия 1 год",
  "matched_target": "i7_6700k",
  "price_uah": 2700
}
```
**Зразок #52:**
```json
{
  "raw_title": "Процессор Intel Core i3-3220 3.30GHz  (SR0RG) s1155, сокет 1155",
  "matched_target": "i3_3220",
  "price_uah": 240
}
```
**Зразок #53:**
```json
{
  "raw_title": "Продам процесор з кулером AMD Ryzen 7 2700X",
  "matched_target": "ryzen_7_2700x",
  "price_uah": 2000
}
```
**Зразок #54:**
```json
{
  "raw_title": "Процесор Ryzen 5 3500x",
  "matched_target": "ryzen_5_3500x",
  "price_uah": 2600
}
```
**Зразок #55:**
```json
{
  "raw_title": "Процесор AMD Athlon X4 970 (Socket AM4) 3.8-4.0 GHz",
  "matched_target": "athlon_x4_970",
  "price_uah": 300
}
```
**Зразок #56:**
```json
{
  "raw_title": "Процесор Intel i3-4330",
  "matched_target": "i3_4330",
  "price_uah": 300
}
```
**Зразок #57:**
```json
{
  "raw_title": "Intel core i5 7600",
  "matched_target": "i5_7600",
  "price_uah": 1700
}
```
**Зразок #58:**
```json
{
  "raw_title": "Intel Celeron G1840 SR1VK 2.80GHZ VN",
  "matched_target": "celeron_g1840",
  "price_uah": 400
}
```
**Зразок #59:**
```json
{
  "raw_title": "Производительный Процессор AMD A4-3300",
  "matched_target": "a4_3300",
  "price_uah": 200
}
```
**Зразок #60:**
```json
{
  "raw_title": "Процесор AMD Ryzen 7 5700G 3.8GHz/16MB sAM4",
  "matched_target": "ryzen_7_5700g",
  "price_uah": 6200
}
```
**Зразок #61:**
```json
{
  "raw_title": "Процессор AMD ryzen 5 1600AF (2600)",
  "matched_target": "ryzen_5_1600af",
  "price_uah": 1200
}
```
**Зразок #62:**
```json
{
  "raw_title": "Процессор AMD Ryzen 9 7950X3D  sAM5 Box",
  "matched_target": "ryzen_9_7950x3d",
  "price_uah": 18300
}
```

#### 🔌 Материнські плати — Розпізнано (59):
**Зразок #1:**
```json
{
  "raw_title": "Комплект материнська плата GIGABYTE B450 GAMING X + RYZEN 5 3600",
  "matched_target": "bundle_ryzen_5_3600_b450",
  "price_uah": 9900
}
```
**Зразок #2:**
```json
{
  "raw_title": "Материнская плата MSI X79A-GD45 + Intel Core i7-4930K 3,4GHz + кулер (Socket 2011) Гарантия 1 год",
  "matched_target": "i7_4930k",
  "price_uah": 3100
}
```
**Зразок #3:**
```json
{
  "raw_title": "MSI B150M PRO-VH(сокет 1151v1) + Core i5-6500 3.2GHz + кулер",
  "matched_target": "i5_6500",
  "price_uah": 1567
}
```
**Зразок #4:**
```json
{
  "raw_title": "Материнська плата ASUS TUF GAMING A620M PLUS WIFI",
  "matched_target": "a620",
  "price_uah": 4500
}
```
**Зразок #5:**
```json
{
  "raw_title": "Материнская плата рабочей станции Lenovo ThinkStation S30 + Xeon E5-1650 3,2GHz + кулер (Socket 2011) Гарантия 1 год",
  "matched_target": "xeon_e5_1650",
  "price_uah": 3000
}
```
**Зразок #6:**
```json
{
  "raw_title": "Gigabyte B850 AORUS Elite WiFi7",
  "matched_target": "b850",
  "price_uah": 8300
}
```
**Зразок #7:**
```json
{
  "raw_title": "Материнка Gigabyte GA-H81M-S2V",
  "matched_target": "h81_btc",
  "price_uah": 1000
}
```
**Зразок #8:**
```json
{
  "raw_title": "Материнська плата ASUS m5a78l-m lx3 PLUS Socket am3+ ddr3 OEM Bulk",
  "matched_target": "760g",
  "price_uah": 1500
}
```
**Зразок #9:**
```json
{
  "raw_title": "I3 10105f + asus prime H510M-A (Wifi)",
  "matched_target": "i3_10105f",
  "price_uah": 5500
}
```
**Зразок #10:**
```json
{
  "raw_title": "Материнка AM5 Gigabyte X870E AORUS ELITE WIFI7",
  "matched_target": "x870e",
  "price_uah": 14200
}
```
**Зразок #11:**
```json
{
  "raw_title": "Комплект MSI Z87-G41 + i5-4670 + 4GB DDR3 LGA1150",
  "matched_target": "bundle_i5_4670_z87",
  "price_uah": 1999
}
```
**Зразок #12:**
```json
{
  "raw_title": "Gigabyte GA-78LMT-USB3 + AMD FX-6300 + 8 ГБ DDR3 (комплект)",
  "matched_target": "bundle_fx_6300_fx_6300",
  "price_uah": 1250
}
```
**Зразок #13:**
```json
{
  "raw_title": "Продам комплект для пк на сокеті LGA 1700 материнська плата b660 + процесор intel core i7 13700f 16/24",
  "matched_target": "bundle_i7_13700f_b660",
  "price_uah": 9000
}
```
**Зразок #14:**
```json
{
  "raw_title": "Материнська плата Asus P5KPL-E (Socket LGA775, Intel G31, ATX)",
  "matched_target": "g31",
  "price_uah": 300
}
```
**Зразок #15:**
```json
{
  "raw_title": "Персональний Компютер для Ігор Та роботи Core i9 9900k  512 Гб NVME SSD",
  "matched_target": "i9_9900k",
  "price_uah": 12500
}
```
**Зразок #16:**
```json
{
  "raw_title": "Продам комплект ASUS M4A78LT LE + AMD Phenom II X2 555 Black Edition + 4 ГБ DDR3 + кулер",
  "matched_target": "760g",
  "price_uah": 910
}
```
**Зразок #17:**
```json
{
  "raw_title": "Материнка MSI H61M-P21 s1155 + процессор G620 + 4Gb память",
  "matched_target": "h61",
  "price_uah": 950
}
```
**Зразок #18:**
```json
{
  "raw_title": "Комплект s1151, DDR4 8GB, SSD 128GB, HDD 500GB,H110M-K, 400W PSU",
  "matched_target": "400w",
  "price_uah": 2500
}
```
**Зразок #19:**
```json
{
  "raw_title": "Gigabyte GA-A320M-S2H V2 материнська плата AMD AM4",
  "matched_target": "a320",
  "price_uah": 2600
}
```
**Зразок #20:**
```json
{
  "raw_title": "Продам комплект ga-f2a68hm-s1 cpu a4-4000 box+",
  "matched_target": "a4_4000",
  "price_uah": 900
}
```
**Зразок #21:**
```json
{
  "raw_title": "Комплект X99 / Xeon E5-2666 v3 / 32GB DDR4 / Zalman Optima",
  "matched_target": "bundle_xeon_e5_2666_v3_x99",
  "price_uah": 7300
}
```
**Зразок #22:**
```json
{
  "raw_title": "B75usb_btc_1.1 + i5 2400 (box) + DDR3 4GB",
  "matched_target": "i5_2400",
  "price_uah": 950
}
```
**Зразок #23:**
```json
{
  "raw_title": "материнська плата ASRock h110m dgs",
  "matched_target": "h110",
  "price_uah": 200
}
```
**Зразок #24:**
```json
{
  "raw_title": "Комплект MSI Z270-A Pro + i5 7500 (сокет 1151)",
  "matched_target": "bundle_i5_7500_z270",
  "price_uah": 2790
}
```
**Зразок #25:**
```json
{
  "raw_title": "asrock b650m-hdv/m.2",
  "matched_target": "b650e",
  "price_uah": 3300
}
```
**Зразок #26:**
```json
{
  "raw_title": "Материнська плата MSI Z270-A Pro (сокет 1151), під 6-те та 7-ме покоління intel",
  "matched_target": "z270",
  "price_uah": 1960
}
```
**Зразок #27:**
```json
{
  "raw_title": "материнська плата gigabyte h110m s2pv",
  "matched_target": "h110",
  "price_uah": 700
}
```
**Зразок #28:**
```json
{
  "raw_title": "материнська плата ASRock b150m pro4s",
  "matched_target": "b150",
  "price_uah": 1000
}
```
**Зразок #29:**
```json
{
  "raw_title": "Материнська плата MSI PRO B760M-P DDR4 s1700",
  "matched_target": "b760",
  "price_uah": 3400
}
```
**Зразок #30:**
```json
{
  "raw_title": "Комплект s1151 MSI B150M-S01 + i7-6700 материнка і процесор",
  "matched_target": "i7_6700",
  "price_uah": 3150
}
```
**Зразок #31:**
```json
{
  "raw_title": "Комплект s1151 Asus Prime B250M-C + i5-7400 материнка і процесор",
  "matched_target": "i5_7400",
  "price_uah": 2455
}
```
**Зразок #32:**
```json
{
  "raw_title": "Материнська плата MSI G41M-P33 Combo MS-7592 REV: 7.1, Intel g41",
  "matched_target": "g41",
  "price_uah": 300
}
```
**Зразок #33:**
```json
{
  "raw_title": "Материнська плата з процесором gigabyte ga-p55-us3l",
  "matched_target": "p55",
  "price_uah": 939
}
```
**Зразок #34:**
```json
{
  "raw_title": "Материнская плата Asrock z77 extreme 3\\под восстановление\\.",
  "matched_target": "z77",
  "price_uah": 230
}
```
**Зразок #35:**
```json
{
  "raw_title": "Материнская плата Z87-Pro в комплекте процессор intel I5-4670K , 16 Гб оперативная память.",
  "matched_target": "bundle_i5_4670k_z87",
  "price_uah": 4500
}
```
**Зразок #36:**
```json
{
  "raw_title": "msi z97 gaming 3 (MS-7918) 1150 intel haswell",
  "matched_target": "z97",
  "price_uah": 2500
}
```
**Зразок #37:**
```json
{
  "raw_title": "Материнська плата asus z270-p",
  "matched_target": "z270",
  "price_uah": 1000
}
```
**Зразок #38:**
```json
{
  "raw_title": "Продам материнську Msi Z17O gaming 5m+Процесор I7 6700k +Башня з кулером",
  "matched_target": "i7_6700k",
  "price_uah": 4500
}
```
**Зразок #39:**
```json
{
  "raw_title": "Ryzen 5 5500 B450M-A PRO MAX",
  "matched_target": "ryzen_5_5500",
  "price_uah": 5100
}
```
**Зразок #40:**
```json
{
  "raw_title": "Комплект i5 2400",
  "matched_target": "i5_2400",
  "price_uah": 2000
}
```
**Зразок #41:**
```json
{
  "raw_title": "материнская плата asus LGA 1155 PCIe 3.0 , 16 gb ОЗУ ddr 3 1600 мгг , процессор i5 3570 + кулер intel",
  "matched_target": "i5_3570",
  "price_uah": 2200
}
```
**Зразок #42:**
```json
{
  "raw_title": "Материнська плата MSI X570-A Pro (sAM4, AMD X570, PCI-Ex16)",
  "matched_target": "x570",
  "price_uah": 3700
}
```
**Зразок #43:**
```json
{
  "raw_title": "Материнська плата комплект MSI H110M PRO-VD + проц Intel Celeron G3930 2.9 Ghz",
  "matched_target": "celeron_g3930",
  "price_uah": 947
}
```
**Зразок #44:**
```json
{
  "raw_title": "Комплект ASUS PRIME H310M-R R2.0 + Intel Core i3-9100F + Кулер",
  "matched_target": "i3_9100f",
  "price_uah": 2000
}
```
**Зразок #45:**
```json
{
  "raw_title": "Материнська плата Gigabyte x670 aorus elite ax  am5 ddr5 wifi",
  "matched_target": "x670",
  "price_uah": 6000
}
```
**Зразок #46:**
```json
{
  "raw_title": "Материнська плата ASROCK X470 MASTER SLI/AC нова",
  "matched_target": "x470",
  "price_uah": 4900
}
```
**Зразок #47:**
```json
{
  "raw_title": "Материнська плата Btc H250 + intel i3 6100",
  "matched_target": "i3_6100",
  "price_uah": 1100
}
```
**Зразок #48:**
```json
{
  "raw_title": "Материнська плата ASUS P7H55-M LX  + процесор Intel Core i3 - 550",
  "matched_target": "i3_550",
  "price_uah": 450
}
```
**Зразок #49:**
```json
{
  "raw_title": "Комплект ASUS H110M-CS + Pentium G4400 + БП Game Max 450W",
  "matched_target": "pentium_g4400",
  "price_uah": 1000
}
```
**Зразок #50:**
```json
{
  "raw_title": "Материнська плата MSI H81M-P33",
  "matched_target": "h81_btc",
  "price_uah": 250
}
```
**Зразок #51:**
```json
{
  "raw_title": "Maxsun H610 ITX + Wi-Fi материнская плата s1700",
  "matched_target": "h610",
  "price_uah": 4200
}
```
**Зразок #52:**
```json
{
  "raw_title": "Комплект i3 12100F + Asus Prime H610M-K D4 +  башта",
  "matched_target": "i3_12100f",
  "price_uah": 5800
}
```
**Зразок #53:**
```json
{
  "raw_title": "mb Intel s775 Asus P5KPL-AM SE (G31/DDR2/int. video GMA3100) в ідеальному стані",
  "matched_target": "g31",
  "price_uah": 499
}
```
**Зразок #54:**
```json
{
  "raw_title": "Мать A68MDE+ проц А4 4000",
  "matched_target": "a4_4000",
  "price_uah": 700
}
```
**Зразок #55:**
```json
{
  "raw_title": "Материнська плата ASUS TUF GAMING A520M-PLUS II AM4",
  "matched_target": "a520",
  "price_uah": 2600
}
```
**Зразок #56:**
```json
{
  "raw_title": "Материнская плата s1200 ASUS B460TUF Gaming Plus с i5-10400F DeepCool 300",
  "matched_target": "i5_10400f",
  "price_uah": 6500
}
```
**Зразок #57:**
```json
{
  "raw_title": "Комплект intel i5 10400F / H510MХ/E 2.0 / Кулер ZE Gaming",
  "matched_target": "i5_10400f",
  "price_uah": 5900
}
```
**Зразок #58:**
```json
{
  "raw_title": "Msi z790 tomahawk max wifi ddr5",
  "matched_target": "z790",
  "price_uah": 4300
}
```
**Зразок #59:**
```json
{
  "raw_title": "Материнська плата Asus TUF Gaming X870-PLUS WIFI",
  "matched_target": "x870",
  "price_uah": 11000
}
```

#### ⚡ Блоки живлення — Розпізнано (44):
**Зразок #1:**
```json
{
  "raw_title": "Блок живлення 650W модульный Seasonic Core GM-650 gold",
  "matched_target": "650w",
  "price_uah": 1200
}
```
**Зразок #2:**
```json
{
  "raw_title": "Блок живлення BTC H450ATX 450W",
  "matched_target": "450w",
  "price_uah": 310
}
```
**Зразок #3:**
```json
{
  "raw_title": "DeepCool DQ750ST 750W 80 Plus Gold, хороший стан",
  "matched_target": "750w",
  "price_uah": 2000
}
```
**Зразок #4:**
```json
{
  "raw_title": "Блок живлення 400W Golden Field ATX-S460",
  "matched_target": "400w",
  "price_uah": 350
}
```
**Зразок #5:**
```json
{
  "raw_title": "Блок живлення Gigabyte P450B 450W 80+ Bronze",
  "matched_target": "450w",
  "price_uah": 999
}
```
**Зразок #6:**
```json
{
  "raw_title": "Блок живлення 750W Seasonic Focus PX-750 Platinum SSR-750PX",
  "matched_target": "750w",
  "price_uah": 2499
}
```
**Зразок #7:**
```json
{
  "raw_title": "Блок питания Chieftec PowerUP 750w",
  "matched_target": "750w",
  "price_uah": 2300
}
```
**Зразок #8:**
```json
{
  "raw_title": "Блок живлення для ПК Cooler Master 460W (RS-460-PCAP-A3)",
  "matched_target": "460w",
  "price_uah": 399
}
```
**Зразок #9:**
```json
{
  "raw_title": "Блок  питания Chieftec 500 w",
  "matched_target": "500w",
  "price_uah": 530
}
```
**Зразок #10:**
```json
{
  "raw_title": "Продам  компьютерный блок питания  Thermaltake 1500w",
  "matched_target": "1500w",
  "price_uah": 5000
}
```
**Зразок #11:**
```json
{
  "raw_title": "be quiet! Dark Power 12 850W Titanium [P12--850W] топовий Ультимативний RTX GTX RX gt  gaming oc блок живлення бж питания MX",
  "matched_target": "850w",
  "price_uah": 4999
}
```
**Зразок #12:**
```json
{
  "raw_title": "Блок живлення 700W Chieftec GPC-700S (купувався в  Elmir)",
  "matched_target": "700w",
  "price_uah": 1390
}
```
**Зразок #13:**
```json
{
  "raw_title": "Блок живлення Seasonic Prime TX-1000 1000W Titanium (SSR-1000TR) - 5468",
  "matched_target": "1000w",
  "price_uah": 7099
}
```
**Зразок #14:**
```json
{
  "raw_title": "Блок живлення Chieftec Chieftronic PowerPlay Platinum GPU-1050FC 1050W",
  "matched_target": "1050w",
  "price_uah": 4700
}
```
**Зразок #15:**
```json
{
  "raw_title": "Блоки питания Delux,Fsp,Gembird,microlab 360w,400w",
  "matched_target": "400w",
  "price_uah": 250
}
```
**Зразок #16:**
```json
{
  "raw_title": "EVGA SuperNOVA 850 GA 850W 80 Plus Gold 2021 рік  Топовий бж    rtx rx gtx mx gt gaming oc",
  "matched_target": "850w",
  "price_uah": 3900
}
```
**Зразок #17:**
```json
{
  "raw_title": "Блок живлення Gigabyte UD850GM PG5 850W Gold (Гарантія Rozetka до 2030)",
  "matched_target": "850w",
  "price_uah": 2800
}
```
**Зразок #18:**
```json
{
  "raw_title": "be quiet straight power 11 550w gold",
  "matched_target": "550w",
  "price_uah": 3000
}
```
**Зразок #19:**
```json
{
  "raw_title": "Блок питания для ПК MSI MAG 500w полностью рабочий",
  "matched_target": "500w",
  "price_uah": 600
}
```
**Зразок #20:**
```json
{
  "raw_title": "Блок питания Thermaltake ATX Smart 650w 80 plus bronze. Полностью рабочий блок",
  "matched_target": "650w",
  "price_uah": 1300
}
```
**Зразок #21:**
```json
{
  "raw_title": "Брендовий блок живлення Chieftec APS-700C 700W(модульний) Тест ОК",
  "matched_target": "700w",
  "price_uah": 1999
}
```
**Зразок #22:**
```json
{
  "raw_title": "Thermaltake Toughpower GF 550W Gold | Модульний блок живлення",
  "matched_target": "550w",
  "price_uah": 1150
}
```
**Зразок #23:**
```json
{
  "raw_title": "Chieftec Nitro 2 850W",
  "matched_target": "850w",
  "price_uah": 2499
}
```
**Зразок #24:**
```json
{
  "raw_title": "Блок питания Gamemax 450W (GM-450B) Новый",
  "matched_target": "450w",
  "price_uah": 650
}
```
**Зразок #25:**
```json
{
  "raw_title": "Блок живлення для ПК Gamemax ATX 700W 80 plus bronze",
  "matched_target": "700w",
  "price_uah": 1600
}
```
**Зразок #26:**
```json
{
  "raw_title": "Блок живлення Corsair CX750 750W (на запчастини / під відновлення)",
  "matched_target": "750w",
  "price_uah": 500
}
```
**Зразок #27:**
```json
{
  "raw_title": "Блок живлення HP-D2402E0 240W HP 200 210 220 240 4000 5800 6200 6300 8100 8200 8300",
  "matched_target": "240w",
  "price_uah": 650
}
```
**Зразок #28:**
```json
{
  "raw_title": "Блок живлення Thermaltake Toughpower GF1 1000W Modular 80+Gold (PS-TPD-1000FNFAGE-1)",
  "matched_target": "1000w",
  "price_uah": 4400
}
```
**Зразок #29:**
```json
{
  "raw_title": "Блок живлення LC-Power Super Silent Modular 1000W 80 PLUS Gold",
  "matched_target": "1000w",
  "price_uah": 3900
}
```
**Зразок #30:**
```json
{
  "raw_title": "Блок живленя для пк Chieftec 700w",
  "matched_target": "700w",
  "price_uah": 1300
}
```
**Зразок #31:**
```json
{
  "raw_title": "Блок живлення AeroCool Mirage Gold 850W 80 Plus Gold з ефектом Infinity Mirror та RGB",
  "matched_target": "850w",
  "price_uah": 2800
}
```
**Зразок #32:**
```json
{
  "raw_title": "Блок Живлення  400 W GAMEMAX для пк",
  "matched_target": "400w",
  "price_uah": 600
}
```
**Зразок #33:**
```json
{
  "raw_title": "Блок питания Thermaltake Smart Pro RGB 850W",
  "matched_target": "850w",
  "price_uah": 2780
}
```
**Зразок #34:**
```json
{
  "raw_title": "Asus ROG Thor 1200W Platinum",
  "matched_target": "1200w",
  "price_uah": 13500
}
```
**Зразок #35:**
```json
{
  "raw_title": "Блок живлення 750W CHIEFTEC ProTon 80 PLUS bronze",
  "matched_target": "750w",
  "price_uah": 1700
}
```
**Зразок #36:**
```json
{
  "raw_title": "Блок живлення для ПК MACRON 250W",
  "matched_target": "250w",
  "price_uah": 150
}
```
**Зразок #37:**
```json
{
  "raw_title": "Блок питания 400w для пк",
  "matched_target": "400w",
  "price_uah": 350
}
```
**Зразок #38:**
```json
{
  "raw_title": "Блок живлення CHIEFTEC Polaris 850W",
  "matched_target": "850w",
  "price_uah": 1500
}
```
**Зразок #39:**
```json
{
  "raw_title": "БП Chieftec 600w",
  "matched_target": "600w",
  "price_uah": 1500
}
```
**Зразок #40:**
```json
{
  "raw_title": "Блок живлення enermax revolution d.f. 2 1050w 80+ gold",
  "matched_target": "1050w",
  "price_uah": 3400
}
```
**Зразок #41:**
```json
{
  "raw_title": "Блок живлення UNYKAch SFX 300 w сріблястий(300 Вт, 100-240 В) GPU-6PIN",
  "matched_target": "300w",
  "price_uah": 800
}
```
**Зразок #42:**
```json
{
  "raw_title": "Блок живлення AeroCool KCAS Plus 800W (80 Plus Bronze)",
  "matched_target": "800w",
  "price_uah": 1600
}
```
**Зразок #43:**
```json
{
  "raw_title": "Блок живлення Cooler Master RS-460-PCAP-A3 Б/в",
  "matched_target": "460w",
  "price_uah": 750
}
```
**Зразок #44:**
```json
{
  "raw_title": "БУ оригинальный блок питания HP 503376-001 240W для системников Pro 6000 6005 6200 Elite 8000 8100 8200 SFF",
  "matched_target": "240w",
  "price_uah": 500
}
```

#### 💾 Накопичувачі — Розпізнано (96):
**Зразок #1:**
```json
{
  "raw_title": "Жорсткий диск Iomega Prestige Desktop Hard Drive. 500Гб",
  "matched_target": "ssd_500gb",
  "price_uah": 700
}
```
**Зразок #2:**
```json
{
  "raw_title": "Комплект з 4 штук.Топові Швидкі SSD  M.2 NVMe Samsung PM991a 256GB PCIe 3.0 x4 (100% здоровя)",
  "matched_target": "ssd_256gb",
  "price_uah": 2061
}
```
**Зразок #3:**
```json
{
  "raw_title": "Жорсткий диск Seagate SkyHawk Surveillance 8TB - ST8000VX0022",
  "matched_target": "hdd_8tb",
  "price_uah": 12600
}
```
**Зразок #4:**
```json
{
  "raw_title": "Жесткий диск Seagate 500 Gb SATA",
  "matched_target": "hdd_500gb",
  "price_uah": 250
}
```
**Зразок #5:**
```json
{
  "raw_title": "SSD Kingston NV1 1TB NVMe M.2 2280 PCIe 3.0 x4",
  "matched_target": "ssd_1tb",
  "price_uah": 5000
}
```
**Зразок #6:**
```json
{
  "raw_title": "SSD-накопичувач Samsung 990 PRO 2 TB",
  "matched_target": "ssd_2tb",
  "price_uah": 15900
}
```
**Зразок #7:**
```json
{
  "raw_title": "Kingston A400 SSD SATA (SA400S37) 480 GB",
  "matched_target": "ssd_480gb",
  "price_uah": 2500
}
```
**Зразок #8:**
```json
{
  "raw_title": "NVMe 1tb 1024gb Micron SSD M2 накопичувач аналог KC3000 Samsung evo",
  "matched_target": "ssd_1tb",
  "price_uah": 6200
}
```
**Зразок #9:**
```json
{
  "raw_title": "M2 nvme SSD 240-512gb !!!",
  "matched_target": "ssd_512gb",
  "price_uah": 2980
}
```
**Зразок #10:**
```json
{
  "raw_title": "Жорсткi  диски Western Digital ,  Seagаte , Hitachi - 80GB, 120GB, 160GB, 320GB  до ретро ПК.",
  "matched_target": "hdd_80gb",
  "price_uah": 122
}
```
**Зразок #11:**
```json
{
  "raw_title": "Жорсткий диск WD Red Plus NAS  2 TB, 4 TB, 6TB 8TB 10TB 12TB  CMR / SMR",
  "matched_target": "hdd_2tb",
  "price_uah": 4999
}
```
**Зразок #12:**
```json
{
  "raw_title": "SSD GOODRAM 256 Gb, б/в.",
  "matched_target": "ssd_256gb",
  "price_uah": 960
}
```
**Зразок #13:**
```json
{
  "raw_title": "M2 SSD nvme 1-2tb !!!",
  "matched_target": "ssd_2tb",
  "price_uah": 5850
}
```
**Зразок #14:**
```json
{
  "raw_title": "SSD wd_black SN850X 4TB — NVMe SSD",
  "matched_target": "ssd_4tb",
  "price_uah": 17999
}
```
**Зразок #15:**
```json
{
  "raw_title": "Ssd Kingcell 240gb",
  "matched_target": "ssd_240gb",
  "price_uah": 600
}
```
**Зразок #16:**
```json
{
  "raw_title": "Жесткие диски 3tb",
  "matched_target": "hdd_3tb",
  "price_uah": 1500
}
```
**Зразок #17:**
```json
{
  "raw_title": "SSD SK Hynix PC711 1Tb NVMe M.2 Gen3x4",
  "matched_target": "ssd_1tb",
  "price_uah": 5000
}
```
**Зразок #18:**
```json
{
  "raw_title": "Western Digital 1TB ідеальний стан",
  "matched_target": "hdd_1tb",
  "price_uah": 1499
}
```
**Зразок #19:**
```json
{
  "raw_title": "Продам Жорсткий диск  4TB Seagate",
  "matched_target": "hdd_4tb",
  "price_uah": 6700
}
```
**Зразок #20:**
```json
{
  "raw_title": "SSD Samsung 1 TB 990 Pro with HeatSink",
  "matched_target": "ssd_1tb",
  "price_uah": 9000
}
```
**Зразок #21:**
```json
{
  "raw_title": "SSD Kingston SQ500S37 480Gb SQ500S37/480G TLC, 87-98%",
  "matched_target": "ssd_480gb",
  "price_uah": 1855
}
```
**Зразок #22:**
```json
{
  "raw_title": "Жорсткий Диск Western Digital Black 10TB SATA III (WD102FZBX)",
  "matched_target": "hdd_10tb",
  "price_uah": 22399
}
```
**Зразок #23:**
```json
{
  "raw_title": "SSD Samsung 860 evo 250gb 840 pro 256gb",
  "matched_target": "ssd_250gb",
  "price_uah": 1500
}
```
**Зразок #24:**
```json
{
  "raw_title": "SSD Kingston 240gb хороший стан",
  "matched_target": "ssd_240gb",
  "price_uah": 1150
}
```
**Зразок #25:**
```json
{
  "raw_title": "Жесткий диск HDD 8TB SATA 3.5\" HGST Ultrastar He8 (Dell) 7200RPM Enterprise | 100% Health Гарантия!!!",
  "matched_target": "hdd_8tb",
  "price_uah": 4950
}
```
**Зразок #26:**
```json
{
  "raw_title": "HDD 2.5 500gb , 320gb, Seagate, Toshiba",
  "matched_target": "hdd_500gb",
  "price_uah": 600
}
```
**Зразок #27:**
```json
{
  "raw_title": "жоский диск hdd seagate barracuda 250GB",
  "matched_target": "hdd_250gb",
  "price_uah": 200
}
```
**Зразок #28:**
```json
{
  "raw_title": "SSD Silicon Power A55 2TB SATA III 2.5\" – швидкий, справний",
  "matched_target": "a55",
  "price_uah": 5000
}
```
**Зразок #29:**
```json
{
  "raw_title": "Жорсткий диск Toshiba NAS N300 8Tb",
  "matched_target": "hdd_8tb",
  "price_uah": 11200
}
```
**Зразок #30:**
```json
{
  "raw_title": "Жёсткий диск 2 TB Toshiba PC P300",
  "matched_target": "hdd_2tb",
  "price_uah": 2878
}
```
**Зразок #31:**
```json
{
  "raw_title": "Ssd nvme 2 TB Samsung 990 Pro / Patriot p300 2000 ГБ",
  "matched_target": "ssd_2tb",
  "price_uah": 10999
}
```
**Зразок #32:**
```json
{
  "raw_title": "SSD диск Transcend 250S 4TB NVMe M.2 2280 PCIe 4.0 x4 3D NAND TLC",
  "matched_target": "ssd_4tb",
  "price_uah": 19400
}
```
**Зразок #33:**
```json
{
  "raw_title": "SSD-диск GoodRAM CX400 Gen.2 3D NAND TLC 512GB 2.5",
  "matched_target": "ssd_512gb",
  "price_uah": 2100
}
```
**Зразок #34:**
```json
{
  "raw_title": "Жорсткий диск 2.5\" Seagate Mobile HDD 1TB (ST1000LM035) — стан нового (51 год)",
  "matched_target": "hdd_1tb",
  "price_uah": 1100
}
```
**Зразок #35:**
```json
{
  "raw_title": "HDD 250GB Seagate Barracuda 7200.10",
  "matched_target": "hdd_250gb",
  "price_uah": 250
}
```
**Зразок #36:**
```json
{
  "raw_title": "Продам SSD Fusion SX300 6.4tb",
  "matched_target": "ssd_4tb",
  "price_uah": 23900
}
```
**Зразок #37:**
```json
{
  "raw_title": "SSD диск Samsung 860 Evo-Series 250GB 2.5\" SATA III V-NAND (MLC)",
  "matched_target": "ssd_250gb",
  "price_uah": 1551
}
```
**Зразок #38:**
```json
{
  "raw_title": "Жорсткий диск 3.5\" WD Seagate Samsung 160Gb, 80Gb",
  "matched_target": "hdd_160gb",
  "price_uah": 122
}
```
**Зразок #39:**
```json
{
  "raw_title": "Жорсткий диск HDD 1TB Toshiba P300 (7200 rpm / 64MB) SATA III",
  "matched_target": "hdd_1tb",
  "price_uah": 736
}
```
**Зразок #40:**
```json
{
  "raw_title": "Жесткий диск 160 Гб",
  "matched_target": "ssd_160gb",
  "price_uah": 250
}
```
**Зразок #41:**
```json
{
  "raw_title": "Жесткий диск Seagate 10tb",
  "matched_target": "hdd_10tb",
  "price_uah": 9000
}
```
**Зразок #42:**
```json
{
  "raw_title": "Жорсткий диск Western Digital на 14 ТВ",
  "matched_target": "hdd_14tb",
  "price_uah": 8000
}
```
**Зразок #43:**
```json
{
  "raw_title": "SSD диск KingSpec 128Gb , новий ,2.5\" SATA3",
  "matched_target": "ssd_128gb",
  "price_uah": 749
}
```
**Зразок #44:**
```json
{
  "raw_title": "Жорсткий диск Seagate BarraCuda 1 TB ST1000DM010, НОВІ",
  "matched_target": "hdd_1tb",
  "price_uah": 2599
}
```
**Зразок #45:**
```json
{
  "raw_title": "Жорсткий диск Samsung 80GB 7200rpm 8MB (HD082GJ) SATA-II",
  "matched_target": "hdd_80gb",
  "price_uah": 100
}
```
**Зразок #46:**
```json
{
  "raw_title": "HDD 1Tb, з bed секторами",
  "matched_target": "hdd_1tb",
  "price_uah": 327
}
```
**Зразок #47:**
```json
{
  "raw_title": "Жорсткі диски HDD 320GB + 250GB | Ціна ЗА 2 ДИСКИ",
  "matched_target": "hdd_320gb",
  "price_uah": 380
}
```
**Зразок #48:**
```json
{
  "raw_title": "SSD накопичувач Lexar NQ790 2Tb M.2 2280 NVMe PCIe Gen4x4 (LNQ790X002T)",
  "matched_target": "ssd_2tb",
  "price_uah": 14000
}
```
**Зразок #49:**
```json
{
  "raw_title": "Seagate Barracuda 7200.12 160GB",
  "matched_target": "hdd_160gb",
  "price_uah": 250
}
```
**Зразок #50:**
```json
{
  "raw_title": "Жорсткий диск Western Digital WD Red Pro 2TB FFSX NAS",
  "matched_target": "ssd_2tb",
  "price_uah": 4100
}
```
**Зразок #51:**
```json
{
  "raw_title": "HDD Samsung SP2504C 250GB",
  "matched_target": "hdd_250gb",
  "price_uah": 300
}
```
**Зразок #52:**
```json
{
  "raw_title": "Б\\в 2.5\" ССД 120 ГБ протестований. SSD 120 GB 2.5\" SATA III (6Gb/s) для Пк та Ноутбука",
  "matched_target": "ssd_120gb",
  "price_uah": 633
}
```
**Зразок #53:**
```json
{
  "raw_title": "WD Purple 2TB (на фото) - Жорсткий диск!",
  "matched_target": "hdd_2tb",
  "price_uah": 4200
}
```
**Зразок #54:**
```json
{
  "raw_title": "Жёсткий диск HDD Seagate 1TB (2.5\")",
  "matched_target": "hdd_1tb",
  "price_uah": 900
}
```
**Зразок #55:**
```json
{
  "raw_title": "Жорсткий диск HDD 12TB 7200rpm",
  "matched_target": "hdd_12tb",
  "price_uah": 9000
}
```
**Зразок #56:**
```json
{
  "raw_title": "!СРОЧНО! Kingston KC3000 ( 2TB ) M.2 NVMe PCIe 4.0 SSD — до 7000 МБ/с, идеальное состояние",
  "matched_target": "ssd_2tb",
  "price_uah": 9800
}
```
**Зразок #57:**
```json
{
  "raw_title": "Продам Жорсткий диск Seagate ST1000DM003 1Tb",
  "matched_target": "hdd_1tb",
  "price_uah": 850
}
```
**Зразок #58:**
```json
{
  "raw_title": "Toshiba BG3 (модель KBG30ZMV256G) обємом 256 ГБ стандарту M.2 2280 NVMe PCIe Gen3 x2.",
  "matched_target": "ssd_256gb",
  "price_uah": 1350
}
```
**Зразок #59:**
```json
{
  "raw_title": "SSD накопичувач MSI 240 Gb",
  "matched_target": "ssd_240gb",
  "price_uah": 1950
}
```
**Зразок #60:**
```json
{
  "raw_title": "Ідеальний HDD_1 TB samsung",
  "matched_target": "hdd_1tb",
  "price_uah": 1000
}
```
**Зразок #61:**
```json
{
  "raw_title": "SSD диск Samsung 980 Pro 1TB M.2 PCIe 4.0 x4 V-NAND БУ отличное сост.",
  "matched_target": "ssd_1tb",
  "price_uah": 7000
}
```
**Зразок #62:**
```json
{
  "raw_title": "Жесткий диск Toshiba PC P300 2TB НА ГАРАНТИИ",
  "matched_target": "hdd_2tb",
  "price_uah": 2500
}
```
**Зразок #63:**
```json
{
  "raw_title": "Жорсткий  диск HDD 2,5\"  Seagate 320Гб",
  "matched_target": "hdd_320gb",
  "price_uah": 300
}
```
**Зразок #64:**
```json
{
  "raw_title": "Продам жорсткі диски HDD 500 gb",
  "matched_target": "hdd_500gb",
  "price_uah": 350
}
```
**Зразок #65:**
```json
{
  "raw_title": "SSD диск PNY CS900 1TB 6G SATA III 2.5\"",
  "matched_target": "ssd_1tb",
  "price_uah": 4500
}
```
**Зразок #66:**
```json
{
  "raw_title": "Диск SSD 128 Samsung 240 Гб HDD 2,5\" Gb: 320 , 500 , 750 Windows",
  "matched_target": "ssd_240gb",
  "price_uah": 1650
}
```
**Зразок #67:**
```json
{
  "raw_title": "SSD NVME 1000 gb Kingston / Wibrand 1 TB/ 1 ТБ ССД НВМЕ",
  "matched_target": "ssd_1tb",
  "price_uah": 5950
}
```
**Зразок #68:**
```json
{
  "raw_title": "Hdd 8Tb WD85PURZ SATA 6gb/s",
  "matched_target": "hdd_8tb",
  "price_uah": 9000
}
```
**Зразок #69:**
```json
{
  "raw_title": "Запаковани Новий SSD на 1tb Goodram CX400 Gen2 1Tb SATA 2.5 (SSDPR-CX400-01T-G2) ССД на 1 тб",
  "matched_target": "ssd_1tb",
  "price_uah": 4898
}
```
**Зразок #70:**
```json
{
  "raw_title": "Samsung HD160JJ 160Gb/7200rpm/8Mb",
  "matched_target": "ssd_160gb",
  "price_uah": 140
}
```
**Зразок #71:**
```json
{
  "raw_title": "Samsung 990 pro 1tb + зовнішній кейс для нього",
  "matched_target": "ssd_1tb",
  "price_uah": 6300
}
```
**Зразок #72:**
```json
{
  "raw_title": "Накопичувач зовнішній USB NVMe NGFF M.2 SSD 2TB",
  "matched_target": "ssd_2tb",
  "price_uah": 2370
}
```
**Зразок #73:**
```json
{
  "raw_title": "жёсткий диск Seagate barracuda 500 Gb",
  "matched_target": "hdd_500gb",
  "price_uah": 400
}
```
**Зразок #74:**
```json
{
  "raw_title": "Жесткий диск 320 ГБ Samsung HM320JI 2.5 SATA все тесты скину",
  "matched_target": "ssd_320gb",
  "price_uah": 200
}
```
**Зразок #75:**
```json
{
  "raw_title": "Продам жорсткий диск hitachi 160 gb",
  "matched_target": "hdd_160gb",
  "price_uah": 200
}
```
**Зразок #76:**
```json
{
  "raw_title": "SSD  Kingston  240 Gb  (SUV400S37/240G)",
  "matched_target": "ssd_240gb",
  "price_uah": 1300
}
```
**Зразок #77:**
```json
{
  "raw_title": "SSD диск  Crucial T700 2Tb PCIe 5.0 x4 NVMe 2.0 (12400 МБ/с)",
  "matched_target": "ssd_2tb",
  "price_uah": 14999
}
```
**Зразок #78:**
```json
{
  "raw_title": "WD My Cloud / Western Digital NAS на 8 TB.",
  "matched_target": "hdd_8tb",
  "price_uah": 6000
}
```
**Зразок #79:**
```json
{
  "raw_title": "LaCie 1tb 1000GB Якісні зовнішні ударостійкі диски Мала нароботка майже нові Стан гарний",
  "matched_target": "ssd_1tb",
  "price_uah": 2500
}
```
**Зразок #80:**
```json
{
  "raw_title": "Жорсткі диски 80Gb",
  "matched_target": "hdd_80gb",
  "price_uah": 90
}
```
**Зразок #81:**
```json
{
  "raw_title": "Жорсткий диск Toshiba 320 Gb",
  "matched_target": "hdd_320gb",
  "price_uah": 260
}
```
**Зразок #82:**
```json
{
  "raw_title": "SSD Crucial 240 Gb",
  "matched_target": "ssd_240gb",
  "price_uah": 1300
}
```
**Зразок #83:**
```json
{
  "raw_title": "Goodram CX400 Gen.2 512 GB",
  "matched_target": "ssd_512gb",
  "price_uah": 2350
}
```
**Зразок #84:**
```json
{
  "raw_title": "Samsung 850 PRO 256GB (Здоровя 93–96%) Відмінний стан",
  "matched_target": "ssd_256gb",
  "price_uah": 1500
}
```
**Зразок #85:**
```json
{
  "raw_title": "Накопичувач HDD SATA 500GB Toshiba P300 7200rpm 64MB",
  "matched_target": "hdd_500gb",
  "price_uah": 225
}
```
**Зразок #86:**
```json
{
  "raw_title": "Жорстки диск Toshiba PC P300 2TB новий",
  "matched_target": "hdd_2tb",
  "price_uah": 4000
}
```
**Зразок #87:**
```json
{
  "raw_title": "SSD 512Gb 2,5\" SATA-3 в ідеальному стані",
  "matched_target": "ssd_512gb",
  "price_uah": 2000
}
```
**Зразок #88:**
```json
{
  "raw_title": "Продам Жесткий диск 2.5\" Toshiba 500GB SATAIII (MQ01ABF050) для ноутбука",
  "matched_target": "hdd_500gb",
  "price_uah": 400
}
```
**Зразок #89:**
```json
{
  "raw_title": "Жорсткий диск 3.5 6TB WD (WD62PURZ) (WD64PURZ)",
  "matched_target": "hdd_6tb",
  "price_uah": 13000
}
```
**Зразок #90:**
```json
{
  "raw_title": "Ssd SATA 2.5” 1 ТБ (1000 ГБ) нова, запакована",
  "matched_target": "ssd_1tb",
  "price_uah": 3500
}
```
**Зразок #91:**
```json
{
  "raw_title": "SSD диск Samsung 870 Evo-Series 2TB 2.5",
  "matched_target": "870",
  "price_uah": 14000
}
```
**Зразок #92:**
```json
{
  "raw_title": "Серверний Накопичувач SSD Seagate 960GB SATA 6Gbps Haden 2.5",
  "matched_target": "ssd_960gb",
  "price_uah": 10000
}
```
**Зразок #93:**
```json
{
  "raw_title": "SSD диск - Apacer AS350X 512GB (Новий)",
  "matched_target": "ssd_512gb",
  "price_uah": 3000
}
```
**Зразок #94:**
```json
{
  "raw_title": "ssd 240Gb , 960Gb sata брендові",
  "matched_target": "ssd_240gb",
  "price_uah": 999
}
```
**Зразок #95:**
```json
{
  "raw_title": "SSD накопичувач Kingston FURY Renegade 4 TB (SFYRD/4000G)",
  "matched_target": "ssd_4tb",
  "price_uah": 29999
}
```
**Зразок #96:**
```json
{
  "raw_title": "Накопичувач 97% SSD 240GB Kingston (ФОТО КРІСТАЛ ДИСК)",
  "matched_target": "ssd_240gb",
  "price_uah": 1080
}
```

#### 📟 Оперативна пам'ять — Розпізнано (76):
**Зразок #1:**
```json
{
  "raw_title": "Оперативна памʼять G.Skill DDR5 32GB (2x16GB) 6400Mhz Trident Z5 Neo RGB Black (F5-6400J3239G16GX2-TZ5NR)",
  "matched_target": "ram_ddr5_32gb",
  "price_uah": 24500
}
```
**Зразок #2:**
```json
{
  "raw_title": "память DDR5 для ПК 64GB (2x32) 5600MHz Corsair Vengeance RGB. TradeIN",
  "matched_target": "ssd_64gb",
  "price_uah": 30500
}
```
**Зразок #3:**
```json
{
  "raw_title": "Оперативная память DDR3 8GB 1600 MHz Dato",
  "matched_target": "ram_ddr3_8gb",
  "price_uah": 600
}
```
**Зразок #4:**
```json
{
  "raw_title": "память швидка DDR4 32GB Kit (2x16) 4000MHz Patriot VIPER. Trade-in",
  "matched_target": "ram_ddr4_32gb",
  "price_uah": 9200
}
```
**Зразок #5:**
```json
{
  "raw_title": "SSD Kingston NV3 1TB M.2 2280 NVMe PCIe 4.0 x4 3D NAND",
  "matched_target": "ssd_1tb",
  "price_uah": 4900
}
```
**Зразок #6:**
```json
{
  "raw_title": "Kingston DDR4 16GB (2х8) 3200Mhz CL22 SO-DIMM Оперативна память",
  "matched_target": "ram_ddr4_16gb",
  "price_uah": 2700
}
```
**Зразок #7:**
```json
{
  "raw_title": "Продам планки памяти DDR3 на 4gb",
  "matched_target": "ram_ddr3_4gb",
  "price_uah": 130
}
```
**Зразок #8:**
```json
{
  "raw_title": "Комплектуючі для пк, основа для компютера під подальшу збірку + монітор. intel i5-10600KF 32ГБ DDR4 HyperX 3200MHz, ігровий пк, компютер, компютер",
  "matched_target": "i5_10600kf",
  "price_uah": 15000
}
```
**Зразок #9:**
```json
{
  "raw_title": "Модуль оперативної памяті Kingston FURY Beast (ex. HyperX) DDR4 16GB (2×8GB) 3200 MHz (KF432C16BBK2/16WP)",
  "matched_target": "ram_ddr4_16gb",
  "price_uah": 7350
}
```
**Зразок #10:**
```json
{
  "raw_title": "ОЗП Kingston DDR4 2х8GB 3600Mhz FURY Beast RGB Black",
  "matched_target": "ram_ddr4_16gb",
  "price_uah": 6900
}
```
**Зразок #11:**
```json
{
  "raw_title": "Серверна оперативна пам’ять DDR3 ECC Registered 4GB PC3-10600R 1333MHz Samsung / Hynix",
  "matched_target": "ram_ddr3_4gb",
  "price_uah": 250
}
```
**Зразок #12:**
```json
{
  "raw_title": "ОЗУ 2 плашки по 8гб ddr3",
  "matched_target": "ram_ddr3_8gb",
  "price_uah": 150
}
```
**Зразок #13:**
```json
{
  "raw_title": "Оперативна памʼять Patriot DDR4-2666 2*8GB",
  "matched_target": "ram_ddr4_16gb",
  "price_uah": 2400
}
```
**Зразок #14:**
```json
{
  "raw_title": "модулі оперативної памяті INTELIGENTES DDR3 16GB (2 по 8GB)1600 MHz",
  "matched_target": "ram_ddr3_16gb",
  "price_uah": 500
}
```
**Зразок #15:**
```json
{
  "raw_title": "DDR3 4 gb оперативная память",
  "matched_target": "ram_ddr3_4gb",
  "price_uah": 170
}
```
**Зразок #16:**
```json
{
  "raw_title": "kingston fury ddr4 8gb 2666MHz",
  "matched_target": "ram_ddr4_8gb",
  "price_uah": 1199
}
```
**Зразок #17:**
```json
{
  "raw_title": "Память 4Gb DDR4 DIMM разный бренд на выбор",
  "matched_target": "ram_ddr4_4gb",
  "price_uah": 750
}
```
**Зразок #18:**
```json
{
  "raw_title": "Серверна оперативна память DDR3 REG ECC 16gb і 32gb частота 1333 1600  1866мгц",
  "matched_target": "ram_ddr3_16gb",
  "price_uah": 390
}
```
**Зразок #19:**
```json
{
  "raw_title": "Вживане/ГАРАНТІЯ | Оперативна память DDR5 32GB [2x16GB] 6400/CL44 Kingston FURY Alienware Легко працює на 6000/CL30-36-36-76 (X668G8-HYA-A)",
  "matched_target": "ram_ddr5_32gb",
  "price_uah": 22999
}
```
**Зразок #20:**
```json
{
  "raw_title": "SSD диск Apacer 512GB \nh",
  "matched_target": "ssd_512gb",
  "price_uah": 2600
}
```
**Зразок #21:**
```json
{
  "raw_title": "Модуль памяті для компютера DDR4 8GB 3200 MHz Goodram",
  "matched_target": "ram_ddr4_8gb",
  "price_uah": 1900
}
```
**Зразок #22:**
```json
{
  "raw_title": "Crucial 32 GB (2 по 16gb) DDR4 2666 MHZ CT16G4DFRA266.18FD1 оперативная память ОЗУ",
  "matched_target": "ram_ddr4_32gb",
  "price_uah": 4100
}
```
**Зразок #23:**
```json
{
  "raw_title": "Опереативна память 4x2 8 gb ddr3  1600mhz ddr 5 8x2 16 gb 5600",
  "matched_target": "ram_ddr3_8gb",
  "price_uah": 5199
}
```
**Зразок #24:**
```json
{
  "raw_title": "G.Skill 16 GB (4x4GB) DDR4 2800 MHz (F4-2800C16Q-16GRK)",
  "matched_target": "ram_ddr4_16gb",
  "price_uah": 3850
}
```
**Зразок #25:**
```json
{
  "raw_title": "Оперативна памʼять до ноутбука ddr4 16gb",
  "matched_target": "ram_ddr4_16gb",
  "price_uah": 2500
}
```
**Зразок #26:**
```json
{
  "raw_title": "HyperX Fury DDR4 16GB (2×8GB)",
  "matched_target": "ram_ddr4_16gb",
  "price_uah": 3000
}
```
**Зразок #27:**
```json
{
  "raw_title": "Оперативная память 32Gb 3200Mhz DDR4 HyperX",
  "matched_target": "ram_ddr4_32gb",
  "price_uah": 4900
}
```
**Зразок #28:**
```json
{
  "raw_title": "Оперативка DDR3 16GB (4x4GB) Corsair та TeamGroup Elite+",
  "matched_target": "ram_ddr3_16gb",
  "price_uah": 850
}
```
**Зразок #29:**
```json
{
  "raw_title": "Оперативна память SK hynix SO-DIMM DDR5 16GB 5600MHz",
  "matched_target": "ram_ddr5_16gb",
  "price_uah": 12000
}
```
**Зразок #30:**
```json
{
  "raw_title": "Оперативна Память Samsung 16GB (2x8GB) DDR4  3200MHz (M378A1G44AB0-CWE)",
  "matched_target": "ram_ddr4_16gb",
  "price_uah": 3400
}
```
**Зразок #31:**
```json
{
  "raw_title": "Оперативна память ddr5 sodimm 16gb 1rx16 pc5-4800b-sco-1010 xt",
  "matched_target": "ram_ddr5_16gb",
  "price_uah": 6000
}
```
**Зразок #32:**
```json
{
  "raw_title": "Ddr4 16gb kingston",
  "matched_target": "ram_ddr4_16gb",
  "price_uah": 4000
}
```
**Зразок #33:**
```json
{
  "raw_title": "Оперативна память 32gb (2x16gb) ddr4",
  "matched_target": "ram_ddr4_32gb",
  "price_uah": 8500
}
```
**Зразок #34:**
```json
{
  "raw_title": "Оперативна памʼять Kingston Fury SODIMM DDR5-5600 16ГБ",
  "matched_target": "ram_ddr5_16gb",
  "price_uah": 7599
}
```
**Зразок #35:**
```json
{
  "raw_title": "HDD Maxtor DiamondMax 22 500 gb",
  "matched_target": "hdd_500gb",
  "price_uah": 200
}
```
**Зразок #36:**
```json
{
  "raw_title": "DDR4 4GB 2666mhz Crucial",
  "matched_target": "ram_ddr4_4gb",
  "price_uah": 400
}
```
**Зразок #37:**
```json
{
  "raw_title": "Продам б\\в ОЗП Corsair DDR4 32GB (2x16GB) 3600Mhz Vengeance RGB Pro SL White",
  "matched_target": "ram_ddr4_32gb",
  "price_uah": 8600
}
```
**Зразок #38:**
```json
{
  "raw_title": "SSD диск Gigabyte 256GB M.2 2280 NVMe PCIe 3.0 x4 NAND TLC (GP-GSM2NE3",
  "matched_target": "ssd_256gb",
  "price_uah": 2200
}
```
**Зразок #39:**
```json
{
  "raw_title": "RAM G.SKILL AEGIS DDR4 2x8gb (16gb) 3000mhz cl16",
  "matched_target": "ram_ddr4_16gb",
  "price_uah": 3388
}
```
**Зразок #40:**
```json
{
  "raw_title": "Оперативная память ОЗУ DDR4 16gb 2*8gb",
  "matched_target": "ram_ddr4_16gb",
  "price_uah": 2800
}
```
**Зразок #41:**
```json
{
  "raw_title": "Ореративна пам ять ddr4 32 gb 4x8",
  "matched_target": "ram_ddr4_32gb",
  "price_uah": 7000
}
```
**Зразок #42:**
```json
{
  "raw_title": "Оперативна пам’ять ОЗУ  DDR4 JAZER 8GB 3200MHz",
  "matched_target": "ram_ddr4_8gb",
  "price_uah": 1755
}
```
**Зразок #43:**
```json
{
  "raw_title": "Оперативна пам’ять Kingston FURY (ex. HyperX) Beast Black DDR5 16GB (KF552C36BBEK2)",
  "matched_target": "ram_ddr5_16gb",
  "price_uah": 10300
}
```
**Зразок #44:**
```json
{
  "raw_title": "Crucial DDR5 64GB (2x32GB) 5600, CL46,  протестована",
  "matched_target": "ssd_64gb",
  "price_uah": 28995
}
```
**Зразок #45:**
```json
{
  "raw_title": "продам оперативную память DDR3 8GB 1600",
  "matched_target": "ram_ddr3_8gb",
  "price_uah": 633
}
```
**Зразок #46:**
```json
{
  "raw_title": "Продам оперативку DDR3 4Gb 1333Mhz Patriot",
  "matched_target": "ram_ddr3_4gb",
  "price_uah": 400
}
```
**Зразок #47:**
```json
{
  "raw_title": "Оперативна память GEIL 8GB DDR4-2666",
  "matched_target": "ram_ddr4_8gb",
  "price_uah": 1100
}
```
**Зразок #48:**
```json
{
  "raw_title": "Продам оперативну память ноутбука ddr4 2x8 3200MHz",
  "matched_target": "ram_ddr4_16gb",
  "price_uah": 3000
}
```
**Зразок #49:**
```json
{
  "raw_title": "Оперативна память GOOD RAM   DDR3    4Gb",
  "matched_target": "ram_ddr3_4gb",
  "price_uah": 150
}
```
**Зразок #50:**
```json
{
  "raw_title": "Оперативна память 4gb ddr4",
  "matched_target": "ram_ddr4_4gb",
  "price_uah": 350
}
```
**Зразок #51:**
```json
{
  "raw_title": "Оперативная Память DDR3 1600 (2x8)",
  "matched_target": "ram_ddr3_16gb",
  "price_uah": 1200
}
```
**Зразок #52:**
```json
{
  "raw_title": "RAM DDR4 2666 PATRIOT PVE432G266C6KBL 16gb CL16 1.2V (1х16Gb)",
  "matched_target": "ram_ddr4_16gb",
  "price_uah": 2450
}
```
**Зразок #53:**
```json
{
  "raw_title": "Оперативна память Exceleram DDR3 8GB.1600 МГц",
  "matched_target": "ram_ddr3_8gb",
  "price_uah": 800
}
```
**Зразок #54:**
```json
{
  "raw_title": "Оперативна пʼмять DDR3 8gb 1600mhz AMD Radeon",
  "matched_target": "ram_ddr3_8gb",
  "price_uah": 650
}
```
**Зразок #55:**
```json
{
  "raw_title": "Оперативна память Kingston Fury Beast Black DDR5 2x16GB 4800MHz CL38  - 32GB",
  "matched_target": "ram_ddr5_32gb",
  "price_uah": 26999
}
```
**Зразок #56:**
```json
{
  "raw_title": "Оперативна память AORUS 8GB DDR4-3333",
  "matched_target": "ram_ddr4_8gb",
  "price_uah": 1650
}
```
**Зразок #57:**
```json
{
  "raw_title": "SSD M.2 Samsung 970 EVO Plus 1TB 1 ТБ NVMe PCIe MZ-V7S1T0BW",
  "matched_target": "ssd_1tb",
  "price_uah": 7500
}
```
**Зразок #58:**
```json
{
  "raw_title": "Оперативная память G.Skill DDR4-3000 16gb (2x8)Aegis",
  "matched_target": "ram_ddr4_16gb",
  "price_uah": 2950
}
```
**Зразок #59:**
```json
{
  "raw_title": "Оперативна памʼять RAM ОЗУ G.SKILL Trident Z RGB 64GB 2x32 DDR4 3600 CL18",
  "matched_target": "ssd_64gb",
  "price_uah": 14999
}
```
**Зразок #60:**
```json
{
  "raw_title": "Оперативная память - HyperX DDR4-3200-CL16/16gb/(8+8)",
  "matched_target": "ram_ddr4_16gb",
  "price_uah": 5000
}
```
**Зразок #61:**
```json
{
  "raw_title": "Оперативна памаять(ОЗП): Kingston DDR4 16GB (2x8GB) 3200Mhz FURY Beast Black",
  "matched_target": "ram_ddr4_16gb",
  "price_uah": 6000
}
```
**Зразок #62:**
```json
{
  "raw_title": "Оперативна память SK hynix 16GB DDR3 ECC REG 1333MHz сервер Xeon X79",
  "matched_target": "x79",
  "price_uah": 645
}
```
**Зразок #63:**
```json
{
  "raw_title": "Оперативная память Samsung 8GB DDR3 1Rx4 PC3L-12800R  M393B1G70BH0-YK0",
  "matched_target": "ram_ddr3_8gb",
  "price_uah": 800
}
```
**Зразок #64:**
```json
{
  "raw_title": "Оперативная плашка ddr4 3200mhz g.skill ripjaws 8gb",
  "matched_target": "ram_ddr4_8gb",
  "price_uah": 2500
}
```
**Зразок #65:**
```json
{
  "raw_title": "Оперативная память Samsung DDR3 4gb 1333 MHz",
  "matched_target": "ram_ddr3_4gb",
  "price_uah": 550
}
```
**Зразок #66:**
```json
{
  "raw_title": "Оперативная память ddr4 kingston fury hyperx  16gb 2 по 8 3200mhz",
  "matched_target": "ram_ddr4_16gb",
  "price_uah": 4500
}
```
**Зразок #67:**
```json
{
  "raw_title": "Оперативная память Samsung 96GB RDIMM DDR5 4800 MHz (M321RYGA0BB0-CQK)",
  "matched_target": "ram_ddr5_96gb",
  "price_uah": 129900
}
```
**Зразок #68:**
```json
{
  "raw_title": "Kingston Beast Black DDR4 16GB",
  "matched_target": "ram_ddr4_16gb",
  "price_uah": 5000
}
```
**Зразок #69:**
```json
{
  "raw_title": "Модуль RAM Kingston DDR4 8GB 3200MT/s SODIMM",
  "matched_target": "ram_ddr4_8gb",
  "price_uah": 1500
}
```
**Зразок #70:**
```json
{
  "raw_title": "Оперативная память corsair vengeance ddr4 16gb 2 по 8 3000mhz(3200mhz)",
  "matched_target": "ram_ddr4_16gb",
  "price_uah": 4000
}
```
**Зразок #71:**
```json
{
  "raw_title": "Память reg ddr4 64gb 2933 серверна",
  "matched_target": "ssd_64gb",
  "price_uah": 6500
}
```
**Зразок #72:**
```json
{
  "raw_title": "KLLISRE DDR4 16гб 2666мгц",
  "matched_target": "ram_ddr4_16gb",
  "price_uah": 2750
}
```
**Зразок #73:**
```json
{
  "raw_title": "Нова‼️Оперативна пам’ять Netac DDR4 32GB 2×16GB 3200MHz CL16",
  "matched_target": "ram_ddr4_32gb",
  "price_uah": 7499
}
```
**Зразок #74:**
```json
{
  "raw_title": "Goodram DDR3 4gb PC3, 15000 DIMM",
  "matched_target": "ram_ddr3_4gb",
  "price_uah": 290
}
```
**Зразок #75:**
```json
{
  "raw_title": "Модуль памяті для компютера DDR4 8GB 3200 MHz Aegis G.Skill",
  "matched_target": "ram_ddr4_8gb",
  "price_uah": 2000
}
```
**Зразок #76:**
```json
{
  "raw_title": "Оперативна память в ПК Corsair 16GB (2*8GB) DDR4 2666mhz CL16",
  "matched_target": "ram_ddr4_16gb",
  "price_uah": 3500
}
```

#### 📦 Комплекти — Розпізнано (0):

# 🐛 ДЕБАГ-ЗВІТ ПАРСИНГУ КОМПЛЕКТУЮЧИХ OLX (GraphQL)
**Дата та час запуску:** 2026-08-07 22:23:35
**Тривалість виконання:** 347.25 сек
**Шлях до звіту:** `C:\Users\marke\OneDrive\Desktop\Operating_System\debug\debug_report_parse_hardware.md`

## 📌 1. Задача та мета коду
Основна мета: асинхронний збір свіжих оголошень комплектуючих з OLX (GraphQL API).

## 📊 2. Загальна статистика вхідних даних та відсіювання
### ⚙️ Секція: Supabase_Input
- **Завантажено URLs для дедуплікації:** 52621

### ⚙️ Секція: Parser_Config
- **Цільових моделей комплектуючих:** 31782

### ⚙️ Секція: OLX_GraphQL
- **Отримано [videokarty]:** 463
- **Отримано [protsessory]:** 467
- **Отримано [materinskie-platy]:** 467
- **Отримано [bloki-pitaniya]:** 467
- **Отримано [zhestkie-diski]:** 358
- **Отримано [moduli-pamyati]:** 414

### ⚙️ Секція: Filtering_Rules
- **Відсіяно (Не розпізнано модель):** 751

### ⚙️ Секція: Parsing_Metrics
- **Успішно розпізнано [gpu]:** 4
- **Успішно розпізнано [cpu]:** 1
- **Успішно розпізнано [storage]:** 1
- **Успішно розпізнано [ram]:** 3
- **Успішно розпізнано [psu]:** 1

### ⚙️ Секція: Summary
- **Знайдено нових унікальних оголошень:** 10
- **Немає нових оголошень для відправки в DB:** 2

### ⚙️ Секція: Supabase_Output
- **Успішно збережено в DB:** 10

### ⚙️ Секція: WebSocket
- **Успішно надіслано тригер стріму:** 4

## 🔄 3. Детальні приклади даних
### 🚫 Відсіяні оголошення:
#### 🎮 Відеокарти (GPU) — Відсіяно (100):
**Семпл #1:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/vdeokarta-xfx-radeon-rx-7900-gre-gaming-oem-ID10SdK7.html",
  "title": "Відеокарта XFX Radeon RX 7900 GRE Gaming OEM"
}
```
**Семпл #2:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/hp-rtx-4070-ti-oem-12-gb-ID110FqD.html",
  "title": "HP rtx 4070 ti oem 12 gb"
}
```
**Семпл #3:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Відеокарта Gigabyte RTX 4060ti"
}
```
**Семпл #4:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Radeon hd 7000 series"
}
```
**Семпл #5:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Gigabyte gtx1060 super 6gb"
}
```
**Семпл #6:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/gtx-1070ti-8gb-evga-ID11105W.html",
  "title": "gtx 1070ti 8gb evga"
}
```
**Семпл #7:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/rx470-4gb-256bit-gaming-x-4g-ID1111GB.html",
  "title": "rx470 4gb 256bit GAMING X 4G"
}
```
**Семпл #8:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/prodam-videokartu-rx-470-miner-4g-ID1111FO.html",
  "title": "Продам видеокарту Rx 470 Miner 4g"
}
```
**Семпл #9:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "EN  8600 gt 512 mb"
}
```
**Семпл #10:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/videokarta-nvidia-asus-gtx-950-2gb-ID1111Ee.html",
  "title": "Видеокарта NVIDIA Asus GTX 950 2Gb"
}
```
**Семпл #11:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "MSI PCI-Ex Radeon HD5750 1024MB GDDR5 (128bit)"
}
```
**Семпл #12:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/vdeokarta-nvidia-geforce-gtx-1070-8gb-gddr5-256-bit-1920-cuda-b-v-ID10Fbnu.html",
  "title": "Відеокарта Nvidia GeForce GTX 1070 (8Gb / GDDR5 / 256 bit / 1920 CUDA) - Б/В"
}
```
**Семпл #13:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/vdeokarta-palit-dual-rtx-3060-12gb-povniy-komplekt-ID10YRMg.html",
  "title": "Відеокарта Palit Dual RTX 3060 12Gb (повний комплект)"
}
```
**Семпл #14:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/kompyuter-lenovo-legion-tower-7i-gen-10-90y6003wus-ultra-9-285k-rtx-5080-32gb-2tb-nov-zapakovan-ID10ekXL.html",
  "title": "Компютер Lenovo Legion Tower 7i Gen 10 (90Y6003WUS) Ultra 9 285k/RTX 5080/32Gb/2Tb Нові - запаковані!"
}
```
**Семпл #15:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/videokarta-gigabyte-geforce-rtx-2070-super-8gb-ID1111zB.html",
  "title": "Видеокарта Gigabyte GeForce RTX 2070 SUPER 8GB"
}
```
**Семпл #16:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/hp-rtx-4070-ti-oem-12-gb-ID110FqD.html",
  "title": "HP rtx 4070 ti oem 12 gb"
}
```
**Семпл #17:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Відео карта GeForce 1 Gb"
}
```
**Семпл #18:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/vdeokarta-rx570-4gb-gigabyte-IDZtSlk.html",
  "title": "Відеокарта rx570 4gb gigabyte"
}
```
**Семпл #19:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/geforce-gt-730-2gb-ID1111m9.html",
  "title": "GeForce GT 730 2gb"
}
```
**Семпл #20:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Продам видеокарту 10-50"
}
```
**Семпл #21:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/rtx-2060-super-palit-dual-ID10EqeJ.html",
  "title": "Rtx 2060 super Palit dual"
}
```
**Семпл #22:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/vdeokarta-1060-3-gb-gigabyte-ID11119b.html",
  "title": "Відеокарта 1060 3 гб gigabyte"
}
```
**Семпл #23:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/vdeokarta-grova-asus-stix-gaming-rx570-4gb-potuzhna-deal-ID10Zvqu.html",
  "title": "Відеокарта ігрова Asus Stix Gaming RX570 4GB  потужна, ідеал"
}
```
**Семпл #24:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/asus-strix-gtx-960-2gb-ID10p6DY.html",
  "title": "Asus Strix GTX 960 2gb"
}
```
**Семпл #25:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/vdeokarta-sapphire-nitro-amd-radeon-rx-6800-xt-special-edition-ID10XwdR.html",
  "title": "Відеокарта Sapphire NITRO+ AMD Radeon RX 6800 XT Special Edition."
}
```
**Семпл #26:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/vdeokarta-msi-ventus-3x-plus-geforce-rtx-3080vdeokarta-msi-geforce-rtx-3080-ven-ID10KjOz.html",
  "title": "Відеокарта MSI Ventus 3X Plus Geforce RTX 3080\nВідеокарта MSI GeForce RTX 3080 VEN"
}
```
**Семпл #27:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/vdeokarta-gigabyte-rtx-2070-8gb-gaming-ID10YDlv.html",
  "title": "Відеокарта Gigabyte RTX 2070 8Gb Gaming"
}
```
**Семпл #28:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/vdeokarta-asus-rog-strix-gtx-1080-ti-11gb-gddr5x-ID10YXAx.html",
  "title": "Відеокарта ASUS ROG Strix GTX 1080 Ti 11GB GDDR5X"
}
```
**Семпл #29:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/vdeokarta-geforce-gtx-1080-ti-msi-ID10BbOS.html",
  "title": "Відеокарта Geforce GTX 1080 Ti MSI"
}
```
**Семпл #30:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/videokarta-nvidia-geforce-gtx-1080-ti-11gb-ID10aLo1.html",
  "title": "Видеокарта NVIDIA GeForce GTX 1080 Ti 11GB"
}
```
**Семпл #31:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/vdeokarta-asus-pci-ex-geforce-rtx-5060-ti-dual-oc-edition-16gb-gddr7-128bit-2632-28000-hdmi-3-x-displayport-dual-rtx5060ti-o16g-ID10EpZO.html",
  "title": "Відеокарта ASUS PCI-Ex GeForce RTX 5060 Ti Dual OC Edition 16GB GDDR7 (128bit) (2632/28000) (HDMI, 3 x DisplayPort) (DUAL-RTX5060TI-O16G)"
}
```
**Семпл #32:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/vdeokarta-gigabyte-geforce-gtx-1070-g1-gaming-8g-ID1035yq.html",
  "title": "Відеокарта Gigabyte GeForce GTX 1070 G1 Gaming 8G"
}
```
**Семпл #33:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Відеокарта Gigabyte Radeon HD5570 1Gb"
}
```
**Семпл #34:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Видеокарта radeon HD 7770 1gd"
}
```
**Семпл #35:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/protsessor-amd-ryzen-7-1800x-8-16-am4-ID1110VF.html",
  "title": "Процессор Amd Ryzen 7 1800x 8/16 am4"
}
```
**Семпл #36:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/1060-3gb-vdeokarta-ID1110OH.html",
  "title": "1060 3gb відеокарта"
}
```
**Семпл #37:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/vdeokarta-msi-rtx-4060-8gb-ddr6-ID1110Nn.html",
  "title": "Відеокарта MSI RTX 4060 8GB DDR6"
}
```
**Семпл #38:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/rx-470-480-570-garantya-6ms-stan-praktichno-yak-nov-IDZyKgo.html",
  "title": "RX 470/480/570|Гарантія 6міс|Стан практично як нові"
}
```
**Семпл #39:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/2080-ti-msi-gamingx-trio-ID10YXP2.html",
  "title": "2080 Ti MSI GamingX trio"
}
```
**Семпл #40:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/vdeokarta-asrock-radeon-rx-9060-xt-challenger-oc-16gb-IDZP5RR.html",
  "title": "Відеокарта ASRock Radeon RX 9060 XT Challenger OC 16GB"
}
```
**Семпл #41:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/videokarta-gigabyte-geforce-gt710-ne-rabochaya-IDTp6Pc.html",
  "title": "Видеокарта GIGABYTE GeForce GT710 не рабочая"
}
```
**Семпл #42:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/vdeokarta-gigabyte-rtx-3060-eagle-oc-12-gb-gvn3060eagle-oc12gd-20-ID1110KG.html",
  "title": "Відеокарта Gigabyte RTX 3060 Eagle OC 12 GB (GVN3060EAGLE_OC12GD_20)"
}
```
**Семпл #43:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/vdeokarta-nvidia-gt-530-2gb-potuzhnsha-za-gt-520-ID10Pv8F.html",
  "title": "Відеокарта Nvidia GT 530 2GB (Потужніша за GT 520)"
}
```
**Семпл #44:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/vdeokarta-gigabyte-geforce-gtx-1660-ti-oc-6g-ID1110F9.html",
  "title": "Відеокарта Gigabyte GeForce GTX 1660 Ti OC 6G"
}
```
**Семпл #45:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/prodam-vdeokartu-1080ti-ID1034M9.html",
  "title": "Продам відеокарту 1080Ti"
}
```
**Семпл #46:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/vdeokarta-amd-radeon-rx-480-8gb-sapphire-d5-21260-00-b-v-ID1110v1.html",
  "title": "Відеокарта AMD Radeon RX 480 8GB Sapphire D5 (21260-00) Б/В"
}
```
**Семпл #47:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/50-sapphire-pulse-radeon-rx-570-8g-gddr5-oc-stan-garniy-ID1110mN.html",
  "title": "(~50$) Sapphire PULSE Radeon RX 570 8G GDDR5 OC • стан гарний"
}
```
**Семпл #48:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/videokarta-nvidia-quadro-p400-ID10WUPM.html",
  "title": "Видеокарта Nvidia Quadro P400."
}
```
**Семпл #49:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/videokarta-1650gtx-4-gb-ID1110cG.html",
  "title": "Видеокарта 1650gtx 4 gb"
}
```
**Семпл #50:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/prodam-gigabyte-gtx-1080-windforce-oc-8gb-ID10Awpp.html",
  "title": "Продам Gigabyte GTX 1080 Windforce OC 8GB"
}
```
**Семпл #51:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/videokarta-nvidia-rtx-5070-asus-oc-dual-IDZNIKH.html",
  "title": "Видеокарта nvidia rtx 5070 asus oc dual"
}
```
**Семпл #52:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/palit-geforce-gtx-1650-4gb-ID10CrWn.html",
  "title": "Palit GeForce GTX 1650 4gb"
}
```
**Семпл #53:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/vdeokarta-msi-rtx-3060-gaming-trio-z-12-gb-ID1110az.html",
  "title": "Відеокарта MSI RTX 3060 Gaming Trio Z 12 Gb"
}
```
**Семпл #54:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/sapphire-radeon-rx-6600-pulse-ID10KXwO.html",
  "title": "Sapphire Radeon rx 6600 pulse"
}
```
**Семпл #55:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/videokarta-b-u-asus-strix-rx580-8gb-top-sostoyanie-i-drugie-IDUsqD4.html",
  "title": "Видеокарта б\\у ASUS STRIX RX580 8GB ТОП СОСТОЯНИЕ и другие"
}
```
**Семпл #56:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Відеокарта Palit GeForce 8400 GS 256MB DDR2 HDMI DVI VGA"
}
```
**Семпл #57:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/videokarta-kak-novaya-asus-tuf-rtx-3080-10gb-gaming-na-plombe-obmen-IDTD2m4.html",
  "title": "Видеокарта КАК НОВАЯ ASUS TUF RTX 3080  10Gb GAMING на пломбе, ОБМЕН"
}
```
**Семпл #58:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Msi 1030 відеокарта"
}
```
**Семпл #59:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/nvidia-cmp-170hx-8gb-64gb-hbm2e-ga100-4096-bit-ID110ZWX.html",
  "title": "NVIDIA CMP 170HX 8GB (64GB) HBM2e GA100 4096-bit"
}
```
**Семпл #60:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/vdeo-karta-geforce-gtx-1660-super-nvidia-ID110ZQy.html",
  "title": "Відео карта GEFORCE GTX 1660 SUPER nvidia"
}
```
**Семпл #61:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/asus-nvidia-geforce-gtx-1050-ti-ID1033pL.html",
  "title": "Asus NVIDIA GeForce GTX 1050 Ti"
}
```
**Семпл #62:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/videokarta-asus-pci-ex-radeon-rx-580-mining-8gb-gddr5-ID10Po87.html",
  "title": "Видеокарта Asus PCI-Ex Radeon RX 580 Mining 8GB GDDR5"
}
```
**Семпл #63:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/hd6790-1-gb-ddr5-robocha-vdkokarta-6770-650-460-ID10XV1B.html",
  "title": "HD6790 1 Gb DDR5 робоча відкокарта 6770 650 460"
}
```
**Семпл #64:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/acer-nitro-radeon-rx-9070-xt-oc-16gb-ID10WYbb.html",
  "title": "Acer Nitro Radeon RX 9070 XT OC 16GB"
}
```
**Семпл #65:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/msi-geforce-gtx-1080-gaming-z-8gb-ID10ZgXO.html",
  "title": "MSI GeForce GTX 1080 Gaming Z 8GB"
}
```
**Семпл #66:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/rx-5700-xt-asus-tuf-gaming-ID110ZyT.html",
  "title": "RX 5700 XT Asus tuf gaming"
}
```
**Семпл #67:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/videokarta-sapphire-radeon-rx-580-4gb-ddd5-nitro-otlichnoe-sost-IDZPyDz.html",
  "title": "Видеокарта Sapphire Radeon RX 580 4Gb DDD5 NITRO+ отличное сост."
}
```
**Семпл #68:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/vdeokarta-1660ti-starogo-vipusku-vida-na-zobrazhenn-artefakti-ID10srwX.html",
  "title": "Відеокарта 1660ti  старого випуску видає на зображенні артефакти"
}
```
**Семпл #69:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/video-karta-rh-570-8-gb-i-drugie-komponenty-IDZQyPD.html",
  "title": "видео карта рх 570 8 гб, и другие компоненты"
}
```
**Семпл #70:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/vdeokarta-p106-100-6gb-gurtom-znizhka-analog-gtx-1060-IDZYY5a.html",
  "title": "Відеокарта P106-100 6GB гуртом знижка aнaлoг GTX 1060"
}
```
**Семпл #71:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Відеокарта Nvidia GeForce 9600 GT"
}
```
**Семпл #72:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/vdeokarta-asus-rx570-4gbgb-IDZjwCk.html",
  "title": "Відеокарта Asus rx570 4gb(гб)"
}
```
**Семпл #73:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/gigabyte-1060-3gb-ID10hqpq.html",
  "title": "gigabyte 1060 3gb"
}
```
**Семпл #74:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/videokarta-gigabyte-gaming-oc-rtx-3080-10gb-msi-lhr-i-drugie-karty-IDRs7yn.html",
  "title": "Видеокарта GIGABYTE GAMING OC   RTX 3080 10Gb MSI..LHR и другие карты"
}
```
**Семпл #75:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/prodam-vdeo-kartu-afox-geforce-gtx-750-ti-af750ti-4096d5h1-ID10Yqam.html",
  "title": "Продам відео карту AFOX GeForce GTX 750 Ti AF750Ti-4096D5H1"
}
```
**Семпл #76:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/videokarta-gigabyte-rtx-4090-windforce-2-ID10WAaV.html",
  "title": "Видеокарта Gigabyte Rtx 4090 Windforce 2"
}
```
**Семпл #77:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/dell-nvidia-geforce-rtx-3080-10gb-gddr6x-ID10MgM6.html",
  "title": "Dell NVIDIA GeForce RTX 3080 10GB GDDR6X"
}
```
**Семпл #78:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/videokarta-rx9070-xt-red-devil-na-garantii-ID10ThRg.html",
  "title": "Видеокарта RX9070 XT Red Devil (на гарантии)"
}
```
**Семпл #79:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/vdeokarta-evga-rtx-3080-10gb-pd-vdnovlennya-ID110YXR.html",
  "title": "Відеокарта Evga rtx 3080 10gb (під відновлення)"
}
```
**Семпл #80:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Radeon R9 280X IceQ 3gb"
}
```
**Семпл #81:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Видеокарта Asus EAH3730/HTDI/1G/A"
}
```
**Семпл #82:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/nvidia-gtx-1070-8gb-ID110YQD.html",
  "title": "Nvidia GTX 1070 8gb"
}
```
**Семпл #83:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/gigabyte-geforce-gt-730-2048mb-gddr5-IDYt3mY.html",
  "title": "Gigabyte geforce gt 730 2048mb gddr5"
}
```
**Семпл #84:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Видеокарта NVIDIA NVS 300/NVIDIA Quadro 512Mb в идеальном состоянии!"
}
```
**Семпл #85:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/prodam-videokartu-nvidia-geforce-gt440-IDZQybk.html",
  "title": "Продам видеокарту Nvidia Geforce GT440"
}
```
**Семпл #86:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/videokarta-rtx-2060-super-8gb-inno3d-ID110YEO.html",
  "title": "Видеокарта RTX 2060 SUPER 8gb inno3D"
}
```
**Семпл #87:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/vdeokarta-gtx660-2gb-r7240-4gb-gt710-2gb-ID10FhsO.html",
  "title": "Відеокарта GTX660 2Гб, R7240 4Гб, GT710 2Гб"
}
```
**Семпл #88:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/videokarta-rtx-4090-24-gb-msi-ID10ZV1c.html",
  "title": "Видеокарта Rtx 4090 24 gb msi"
}
```
**Семпл #89:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/vdeokarta-asus-rog-strix-geforce-gtx-1070-ti-8gb-garantya-magazin-pro-pc-ID1109nB.html",
  "title": "Відеокарта ASUS ROG STRIX GeForce GTX 1070 Ti 8GB | Гарантія | Магазин | Pro PC"
}
```
**Семпл #90:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/vdeokarta-radeon-rx-470-ID10POZO.html",
  "title": "відеокарта Radeon RX 470."
}
```
**Семпл #91:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/vdeokarta-asus-dual-amd-radeon-rx-6600-ID110fM6.html",
  "title": "Відеокарта Asus Dual AMD Radeon RX 6600"
}
```
**Семпл #92:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/palit-geforce-rtx-4070-ti-super-gamingpro-oc-ID110Ypn.html",
  "title": "Palit GeForce RTX 4070 Ti SUPER GamingPro OC"
}
```
**Семпл #93:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/msi-gtx-1650-super-gaming-x-4gb-gddr6-geforce-ID10U6xd.html",
  "title": "MSI GTX 1650 SUPER Gaming X 4GB GDDR6 GeForce"
}
```
**Семпл #94:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/vdeokarta-radeon-rx470-4gb-ID110YrH.html",
  "title": "Відеокарта Radeon rx470 4gb"
}
```
**Семпл #95:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/gigabyte-gtx-1650-4gb-ID110Yq2.html",
  "title": "Gigabyte GTX 1650 4gb"
}
```
**Семпл #96:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Видеокарта gf 210"
}
```
**Семпл #97:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/xfx-rx-580-8gb-vdeokarta-ID110YeJ.html",
  "title": "XFX rx 580 8gb відеокарта"
}
```
**Семпл #98:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/vdeokarta-rtx-5070-ti-ID10CgQ5.html",
  "title": "Відеокарта RTX 5070 Ti"
}
```
**Семпл #99:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/vdeokarta-gigabyte-geforce-gt-740-1gb-gddr5-gv-n740d5oc-1gi-ID110YaG.html",
  "title": "Відеокарта Gigabyte GeForce GT 740 1GB GDDR5 GV-N740D5OC-1GI"
}
```
**Семпл #100:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Видеокарта 1Gb 2Gb DDR3 DDR5"
}
```

#### 🧠 Процесори (CPU) — Відсіяно (100):
**Семпл #1:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/intel-core-i3-9100f-4-core-4-2ghz-lga1151-ID10PozU.html",
  "title": "Intel Core i3-9100F 4-Core 4.2GHz LGA1151"
}
```
**Семпл #2:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/ryzen7-5700x3d-tuf-gaming-b450-plus-ii-ozu-16gb-samsung-ID10VaPq.html",
  "title": "Ryzen7 5700x3d+TUF GAMING B450-PLUS II+ озу 16gb Samsung"
}
```
**Семпл #3:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/5-8500-intel-core-3-00-ghz-protsesor-ID10TG6y.html",
  "title": "і5-8500 Intel Core 3.00 ghz процесор"
}
```
**Семпл #4:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Процесор AMD Athlon II X3 455 3.3GHz/1.5MB/4000MHz AM3"
}
```
**Семпл #5:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Процессор Turion 64 X2  TL58 1.9GHz TMDTL58HAX5DC Socket S1"
}
```
**Семпл #6:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/set-intel-core-i7-12700kf-12yader-5ghz-plata-gigabyte-wi-fi-trade-in-ID10va1d.html",
  "title": "сет Intel Core i7-12700KF 12ядер 5GHz + плата Gigabyte Wi-Fi. Trade-IN"
}
```
**Семпл #7:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/protsessor-amd-a4-3400-2-7-ghz-1mb-IDUenXB.html",
  "title": "Процессор AMD A4-3400 2.7 GHz/1MB"
}
```
**Семпл #8:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/ryzen5600x-noviy-IDZRaVB.html",
  "title": "Ryzen5600x новий"
}
```
**Семпл #9:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Процесор Intel E7500"
}
```
**Семпл #10:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Intel Core i3-2310M"
}
```
**Семпл #11:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "звуковой процессор MSP3465G C12 160579.001.JCMHF"
}
```
**Семпл #12:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/intel-core-i3-9100f-ID1111gV.html",
  "title": "Intel Core i3-9100F"
}
```
**Семпл #13:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/intel-core-i5-4690k-top-z-lnyki-5-chetvertogo-pokolnnya-IDSii9D.html",
  "title": "Intel core i5 4690k - TOP з лінійки і5 четвертого покоління"
}
```
**Семпл #14:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/komplekt-xeon-698x-86yader-do-4-8ggts-256gb-ddr5-8800mhz-asus-w890-sage-se-lga4710-ws-ID10zQyf.html",
  "title": "Комплект Xeon 698x 86ядер до 4.8Ггц + 256GB DDR5 8800MHz + Asus w890 SAGE SE LGA4710 WS"
}
```
**Семпл #15:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/prodam-zapakovaniy-protsesor-amd-ryzen-5600x-ID10ytKe.html",
  "title": "Продам запакований процесор AMD Ryzen 5600x"
}
```
**Семпл #16:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/intel-core-i9-14900k-lga1700-24-yadra-32-potoka-ID10QnTF.html",
  "title": "Intel Core i9-14900K LGA1700 24 ядра / 32 потока"
}
```
**Семпл #17:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/intel-core-i3-6320-ID10EqaZ.html",
  "title": "intel core i3 6320"
}
```
**Семпл #18:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Процессор AMD Ryzen 5 PRO 1600. Бу."
}
```
**Семпл #19:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Процессор AMD Athlon 3000G 3.5GHz,4MB,35W,AM4 TRAY"
}
```
**Семпл #20:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Процессор 3яд AMD Atlon 2 3300гц"
}
```
**Семпл #21:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/amd-ryzen-7-7700-am5-protsesor-v-dealnomu-stan-ID10Zv2Z.html",
  "title": "AMD Ryzen 7 7700 AM5 процесор, в ідеальному стані"
}
```
**Семпл #22:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/s1700-protsesor-intel-core-i5-12500-4-6ghz-z-vdeoyadrom-trade-in-IDYYtQs.html",
  "title": "s1700 процесор Intel Core i5-12500 4.6GHz з відеоядром. Trade-in"
}
```
**Семпл #23:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Кулер Noctua D14 Intel AMD AM2 AM3 AM4 s1155/ s1151/ s1200/ s1700/ s2011/ s775/ s1150/ s1156"
}
```
**Семпл #24:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Процессор AMD Athlon II X2 340 3.2GHz/2000MHz/1MB  sFM2"
}
```
**Семпл #25:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/ryzen-3-1200-polnostyu-robochiy-ID1110K0.html",
  "title": "Ryzen 3 1200, полностью робочий"
}
```
**Семпл #26:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/protsesor-intel-core-i5-8600k-3-6-ghz-ID10XgDv.html",
  "title": "Процесор Intel Core i5-8600K 3.6 GHz"
}
```
**Семпл #27:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/noviy-protsesor-amd-ryzen-9-9950x-9000-series-IDY32sj.html",
  "title": "Новий Процесор AMD Ryzen 9 9950X 9000 Series"
}
```
**Семпл #28:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/protsessor-amd-ryzen-5-7500f-socket-am5-6-yadrer-5-0-ggts-mozhno-s-materinkoy-ID10WxE3.html",
  "title": "Процессор AMD Ryzen 5 7500F Socket AM5 6 ядрер 5.0 ГГц можно с материнкой"
}
```
**Семпл #29:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/prodam-protsessor-intel-i5-8600k-ID10MUxa.html",
  "title": "Продам процессор Intel I5-8600k"
}
```
**Семпл #30:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/set-am4-ryzen-5-2600-z-kulerom-plata-gigabyte-a520-m-2-trade-in-ID10L81S.html",
  "title": "сет AM4 Ryzen 5 2600 з кулером + плата Gigabyte A520 M.2. Trade-IN"
}
```
**Семпл #31:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Процесор процессор CPU AMD Athlon 2"
}
```
**Семпл #32:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/i7-6700-intel-core-3-40ghz-protsesor-ID10TFUd.html",
  "title": "i7-6700 Intel Core 3.40ghz процесор"
}
```
**Семпл #33:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/27-protsesor-ryzen-5-2600-tray-stan-garniy-ID1110t4.html",
  "title": "(~27$) процесор Ryzen 5 2600 • TRAY • стан гарний"
}
```
**Семпл #34:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/intel-i7-9700kf-asrock-z370pro4-ID1110pj.html",
  "title": "Intel I7-9700KF + ASROCK Z370pro4"
}
```
**Семпл #35:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/protsesor-i39100f-ID1110kv.html",
  "title": "Процесор i39100f"
}
```
**Семпл #36:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/protsessor-intel-core-i3-9100f-2-9ghz-4-yader-8gt-s-9mb-s1151-IDZnTcS.html",
  "title": "Процессор Intel Core i3-9100F 2.9GHz- 4 ядер  / 8GT / s / 9MB s1151"
}
```
**Семпл #37:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/protsessor-amd-ryzen-3-1200-s-ohlazhdeniem-ID10gPdQ.html",
  "title": "Процессор AMD RYZEN 3 1200 с охлаждением"
}
```
**Семпл #38:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Процессор Athlon x3 445, sAM3"
}
```
**Семпл #39:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/protsessor-quadcore-intel-core-i3-8100-3600-mhz-s1151-v2-IDZlp6D.html",
  "title": "Процессор QuadCore Intel Core i3-8100, 3600 MHz , s1151 V2"
}
```
**Семпл #40:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Рідинне охолодження corsair icue h150i elite capellix з лед підсвіткою"
}
```
**Семпл #41:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/prodam-protsesor-i5-9600k-ID10L2JL.html",
  "title": "Продам процесор i5-9600k"
}
```
**Семпл #42:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/prodam-ryzen-3-2200g-ID110EVo.html",
  "title": "Продам Ryzen 3 2200G"
}
```
**Семпл #43:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "процесор G3258 3.2 ghz 3MB Cache LGA1150 s1150"
}
```
**Семпл #44:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/protsesor-intel-xeon-e5-2620-v2-6-yader-12-potokv-lga2011-ID10J0Ll.html",
  "title": "Процесор Intel Xeon E5-2620 v2 6 ядер 12 потоків LGA2011"
}
```
**Семпл #45:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/i5-11400-asus-prime-b560m-k-ID11101l.html",
  "title": "i5 11400 + Asus Prime b560m-k"
}
```
**Семпл #46:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/prodam-protsessor-intel-i5-8600k-ID10MUxa.html",
  "title": "Продам процессор Intel I5-8600k"
}
```
**Семпл #47:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/rozstrochka-mono-na-3-msyats-intel-core-i5-14600kf-asus-tuf-b760m-plus-id-cooling-se-206xt-topoviy-suchasniy-groviy-komplekt-ID10Xj6E.html",
  "title": "РОЗСТРОЧКА МОНО НА 3 МІСЯЦІ! Intel Core i5 14600KF, Asus TUF B760M-Plus, ID-Cooling SE-206XT топовий сучасний ігровий комплект"
}
```
**Семпл #48:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/protsesor-i3-6100-povnstyu-robochiy-ID10EnX4.html",
  "title": "процесор i3 6100 повністю робочий"
}
```
**Семпл #49:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Процесор  INTEL Core Ultra 9 285 (BX80768285) Новий! open box"
}
```
**Семпл #50:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Процессор АMD Athlon II X4 640"
}
```
**Семпл #51:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Процессор Intel Pentium Dual-Core P6200"
}
```
**Семпл #52:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/prodam-protsesor-i3-9100f-ID110YZh.html",
  "title": "продам процесор i3 9100F"
}
```
**Семпл #53:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/protsesor-intel-xeon-e5-2623-v4-ID10YAlp.html",
  "title": "Процесор Intel Xeon E5-2623 v4"
}
```
**Семпл #54:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/protsesor-intel-core-i7-6700-s1151-IDY7dY4.html",
  "title": "Процесор Intel Core i7 6700 s1151"
}
```
**Семпл #55:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/protsesor-intel-core-i5-14400f-box-v-idealnomu-stan-ID10YQR2.html",
  "title": "Процесор Intel Core i5-14400F Box в идеальному стані"
}
```
**Семпл #56:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/protsessor-intel-pentium-e5400-IDSpTSf.html",
  "title": "Процессор Intel Pentium Е5400"
}
```
**Семпл #57:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Процессор Intel Core 2 Duo E4500 2.2 GHz s775, tray"
}
```
**Семпл #58:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Продам процессор intel core 2 duo"
}
```
**Семпл #59:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/protsessory-i5-13400-i7-13700-11700k-9700-ID110YMa.html",
  "title": "Процессоры i5 13400, i7 13700, 11700k, 9700"
}
```
**Семпл #60:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/amd-ryzen-9-9900x-nov-zapakovan-ID10T3iR.html",
  "title": "AMD Ryzen 9 9900X нові-запаковані"
}
```
**Семпл #61:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/protsessor-amd-a8-9600-am4-IDY4uAj.html",
  "title": "Процессор AMD A8-9600 AM4"
}
```
**Семпл #62:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/9700k-z390-asrock-IDZQxWw.html",
  "title": "9700к + z390 asrock"
}
```
**Семпл #63:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/prodam-protsessor-intel-core-i5-6600-3-30ghz-ID10gN1B.html",
  "title": "Продам процессор intel core i5-6600 3,30ghz"
}
```
**Семпл #64:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Процессор Intel Core 2 Quad Q9300 2.5GHz/6M/1033 (SLACQ) s775"
}
```
**Семпл #65:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/protsesor-intel-xeon-e5-2667-2-9-3-5-ghz-lga2011-130w-b-v-ID110Ycs.html",
  "title": "Процесор Intel Xeon e5-2667 2.9-3.5 GHz, LGA2011 130W Б/В"
}
```
**Семпл #66:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "ПРОДАМ процессор AMD 5 7500F"
}
```
**Семпл #67:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/protsessor-intel-core-i9-7980xe-extreme-edition-18-yader-36-potokov-s2066-ID10Pkv4.html",
  "title": "Процессор Intel Core i9-7980XE Extreme Edition 18 ядер 36 потоков s2066"
}
```
**Семпл #68:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/protsesor-amd-ryzen-7-9800x3d-nov-ID10W1uk.html",
  "title": "Процесор AMD Ryzen 7 - 9800x3D | Нові"
}
```
**Семпл #69:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/komplekt-intel-core-i5-10400f-msi-b560m-pro-e-16-gb-apacer-ddr4-ID110YbI.html",
  "title": "комплект Intel Core i5-10400F + MSI B560M PRO-E + 16 ГБ Apacer DDR4"
}
```
**Семпл #70:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/intel-core-i7-3770-3-4ghz-IDZBs5p.html",
  "title": "Intel Core i7 3770 3.4Ghz"
}
```
**Семпл #71:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/protstsesor-r5-3600-ID10ElKe.html",
  "title": "проццесор r5 3600"
}
```
**Семпл #72:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Материнсеая плата"
}
```
**Семпл #73:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "•ТОП•Куллер/Башня/Охолодження для процесору•Am3+• Не 1155 1150 775 Ам4,2011 1151,2011•Cooler Master,OSZ AMD/Intel НЕ:Gamemax Deep Cool MSI Asus•"
}
```
**Семпл #74:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/ryzen-7-7700-3-80ghz-max-5-30ghz-8c-16t-l3-32mb-ID102Zut.html",
  "title": "ryzen 7 7700 3.80Ghz/Max 5.30Ghz    8c/16T  L3-32mb"
}
```
**Семпл #75:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/amd-athlon-ii-x2-250-ID10gLKa.html",
  "title": "AMD Athlon II x2 250"
}
```
**Семпл #76:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/intel-core-i5-12400f-box-garantiya-ID110VXP.html",
  "title": "Intel Core i5-12400F BOX Гарантия!"
}
```
**Семпл #77:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Продам процесор Intel Celeron D 326 (Socket LGA775) б/в"
}
```
**Семпл #78:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "‼️Топова повітряна система охолодження для CPU Scythe Ashura (SCASR-1000)"
}
```
**Семпл #79:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/protsesor-intel-core-i5-9500-8500-8400-7400-7600k-6500-ID10SLfT.html",
  "title": "Процесор intel core i5 9500/8500/8400/7400/7600k/6500"
}
```
**Семпл #80:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "‼️Топова повітряна система охолодження для CPU Scythe Ashura (SCASR-1000)"
}
```
**Семпл #81:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/amd-ryzen-7-7700-am5-protsesor-v-dealnomu-stan-ID10Zv2Z.html",
  "title": "AMD Ryzen 7 7700 AM5 процесор, в ідеальному стані"
}
```
**Семпл #82:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "AMD Wraith Stealth (базовий кулер)"
}
```
**Семпл #83:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/amd-ryzen-7-7700-7500f-IDXRrGD.html",
  "title": "AMD Ryzen 7 7700, 7500f"
}
```
**Семпл #84:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "AMD Ryzen Threadripper Pro 7945wx"
}
```
**Семпл #85:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/protsessor-amd-ryzen-5-5500-b-u-idealnoe-sostoyanie-ID110W1C.html",
  "title": "Процессор AMD Ryzen 5 5500 (Б/у, идеальное состояние)"
}
```
**Семпл #86:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Б\\У Процесор Intel Celeron T3500, SLGJV"
}
```
**Семпл #87:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/protsessor-intel-celeron-g1830-2-8ghz-5gt-s-2mb-bx80646g1830-s1150-ID10gKWc.html",
  "title": "Процессор Intel Celeron G1830 2.8GHz/5GT/s/2MB (BX80646G1830) s1150"
}
```
**Семпл #88:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Процесор Xeon x5460 3.16 під 775 сокет"
}
```
**Семпл #89:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/protsesor-intel-xeon-5160-3-00ghz-4m-1333-slag9-para-IDTPtUe.html",
  "title": "Процесор Intel Xeon 5160 3.00GHz/4M/1333 SLAG9 є пара"
}
```
**Семпл #90:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/intel-pentium-g4400-ID102XWi.html",
  "title": "Intel Pentium G4400"
}
```
**Семпл #91:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/protsessor-intel-pentium-g4560-IDSUzJn.html",
  "title": "Процессор INTEL Pentium G4560"
}
```
**Семпл #92:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Продаю процесор Xeon"
}
```
**Семпл #93:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/amd-ryzen-2200g-boksoviy-kuler-termopasta-ID10TpLp.html",
  "title": "AMD Ryzen 2200G + боксовий кулер + термопаста"
}
```
**Семпл #94:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/protsessor-amd-ryzen-5-5500-b-u-idealnoe-sostoyanie-ID110W1C.html",
  "title": "Процессор AMD Ryzen 5 5500 (Б/у, идеальное состояние)"
}
```
**Семпл #95:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Процеcор Intel Core 2 Duo E8400 3,0GHz 6MB s775 лот 50 шт."
}
```
**Семпл #96:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/serverniy-protsesor-intel-xeon-e5-2695-v3-ID10FlYv.html",
  "title": "Серверний процесор Intel Xeon E5-2695 V3"
}
```
**Семпл #97:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/amd-ryzen-7-7700-ID110WxO.html",
  "title": "AMD Ryzen 7 7700"
}
```
**Семпл #98:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/prodam-svy-ryzen-3-2200g-ID10QaEB.html",
  "title": "Продам свій Ryzen 3 2200G"
}
```
**Семпл #99:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/protsessor-intel-core-i5-10600kf-ID10Pqfd.html",
  "title": "Процессор Intel core i5 10600kf"
}
```
**Семпл #100:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/protsesor-amd-ryzen-5-3500x-3-6ghz-32m-100-000000158-sam4-ID110WuU.html",
  "title": "Процесор AMD Ryzen 5 3500X 3.6GHz/32M (100-000000158) sAM4"
}
```

#### 🔌 Материнські плати — Відсіяно (100):
**Семпл #1:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/materinskaya-plata-asus-strix-x870-a-gaming-wifi-am5-ID10YxFv.html",
  "title": "Материнская плата Asus STRIX X870-A Gaming WiFi (AM5)"
}
```
**Семпл #2:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/asrock-b650pg-lightning-na-remont-zapchastini-ID10xPyc.html",
  "title": "Asrock b650pg lightning на ремонт/запчастини"
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
  "url": "https://www.olx.ua/d/uk/obyavlenie/gigabyte-h310m-s2h-g5400-ID1111NL.html",
  "title": "Gigabyte H310M S2H + G5400"
}
```
**Семпл #5:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/maxan-challenger-b650-ID1111LH.html",
  "title": "Maxan Challenger b650"
}
```
**Семпл #6:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/prodam-komplekt-materinka-huanahzi-x79-2-49-deluxe-e5-2689-16gb-IDX9JhI.html",
  "title": "Продам комплект,  материнка huanahzi x79 2.49 deluxe + e5 2689 +16gb"
}
```
**Семпл #7:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Материнская плата+процессор+память"
}
```
**Семпл #8:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Материнська плата M848A v5.0, РОЗЄМ 462, 2x DDR AGP, PCI"
}
```
**Семпл #9:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/materinska-plata-asus-tuf-gaming-b650m-plus-wi-fi-protsesor-amd-ryzen-5-7600-bez-ssd-ta-operativno-pamyat-ID10PxfD.html",
  "title": "Материнська плата Asus TUF Gaming B650M-Plus Wi-Fi, процесор AMD Ryzen 5 7600 (без SSD та оперативної памяті)"
}
```
**Семпл #10:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Продам кулер AVC для процессора, рабочее состояние"
}
```
**Семпл #11:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Материнская плата с комплектуюшуми"
}
```
**Семпл #12:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/materinskie-platy-asrock-775dual-915gl-asus-p5g-mx-asrock-n68c-gs-fx-ID10Ex3R.html",
  "title": "Материнские платы ASRock 775Dual-915GL. Asus P5G-MX.  ASRock N68C-GS FX."
}
```
**Семпл #13:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/komplekt-x99-xd3-intel-xeon-e5-2698b-v3-do-3-4-ghz-32gb-4x8gb-16-yader-32-potoki-ddr3-1866-mhz-ecc-reg-quad-channel-tpm-2-0-secure-boot-ID10WCch.html",
  "title": "Комплект X99-XD3 + Intel Xeon E5-2698B v3 до 3.4 GHz + 32GB (4x8GB), 16 ядер/32 потоки, DDR3 1866 MHz ECC Reg quad channel, TPM 2.0, Secure Boot"
}
```
**Семпл #14:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "ASUS Prime X399-A + Ryzen Threadripper 1920X + кулер"
}
```
**Семпл #15:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/asus-sabertooth-z170-mark1-ID10Sz22.html",
  "title": "Asus Sabertooth Z170 Mark1"
}
```
**Семпл #16:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/komplekt-gigabyte-ga-b85m-ds3h-a-intel-core-i3-4160-ozp-16gb-ddr3-ID10R2yg.html",
  "title": "Комплект Gigabyte GA-B85M-DS3H-A + Intel Core i3-4160 + ОЗП 16GB DDR3"
}
```
**Семпл #17:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/komplekt-i5-10400f-asus-prime-h510m-a-pccooler-gi-x4sd-ID10PvZu.html",
  "title": "Комплект i5-10400F + Asus Prime H510M-A + PcCooler GI-X4SD"
}
```
**Семпл #18:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/materinska-plata-gigabyte-ga-a320m-h-kuler-dlya-tsp-ID1111g4.html",
  "title": "Материнська плата GIGABYTE GA-A320M-H + кулер для ЦП"
}
```
**Семпл #19:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/groviy-komplekt-materinska-plata-asus-prime-b450m-a-ryzen-5-3600-ssd-samsung-kuler-vinga-ID1111eT.html",
  "title": "Ігровий комплект: Материнська плата ASUS Prime B450M-A + Ryzen 5 3600 + SSD Samsung + Кулер Vinga"
}
```
**Семпл #20:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Материнская плата Sony VAIO VPCF1 в сборе, рабочая, с процессором и видеокартой"
}
```
**Семпл #21:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Материнська плата Asus P5QL-PRO  + intel core 2  Duo  E8500  3.16 Ghz  + 4GB RAM DDR2"
}
```
**Семпл #22:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Комплект gigabyte ga-f2a68hm-s1 + CPU +RAM"
}
```
**Семпл #23:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/prodam-materinskuyu-platu-msi-7600gm-p21-vmeste-s-protsessorom-amd-fx-4100-ID10E9Eg.html",
  "title": "Продам материнскую плату MSI 7600GM-P21 вместе с процессором Amd FX 4100."
}
```
**Семпл #24:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/komplekt-materinska-colorful-c-h81a-btc-v20-prots-operativka-4gb-IDTkbQR.html",
  "title": "комплект материнска colorful c.h81a-btc v20 проц ,оперативка 4гб"
}
```
**Семпл #25:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "материнская плата Meizu M2 Note"
}
```
**Семпл #26:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "комплектующие материнская плата + процессор + озу"
}
```
**Семпл #27:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Заглушки для материнських плат I/O Shields"
}
```
**Семпл #28:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Материнские платы 1155 сокет. 1151 сокет. Топовые и бюджетные."
}
```
**Семпл #29:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/komplekt-asus-tuf-z390-plus-gaming-wi-fi-i5-9600kf-bashnya-aardwolf-performa-10x-ID10U4eL.html",
  "title": "Комплект Asus TUF Z390-PLUS GAMING Wi-Fi + i5-9600KF + башня Aardwolf PERFORMA 10X"
}
```
**Семпл #30:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/hexacore-intel-i5-9600-4-6ghz-16gb-ddr4-materinka-moschniy-komplekt-dlyapk-ID10gPE6.html",
  "title": "HexaCore Intel i5-9600 4.6Ghz/16gb ddr4/Материнка  Мощний комплект дляПК"
}
```
**Семпл #31:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/intel-i7-6700-4-0ghz-16gb-ddr4-materinka-komplekt-soket1151-dlya-sistemnogo-bloka-ID10gOMl.html",
  "title": "Intel i7-6700 4.0Ghz+16gb ddr4+Материнка  комплект сокет1151 для системного блока"
}
```
**Семпл #32:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/hexacore-intel-i5-9600-4-6ghz-asus-h310m-k-oholodzhennya-moschniy-komplekt-6yader-IDZQ3xl.html",
  "title": "HexaCore Intel i5-9600 4.6Ghz+ASUS H310M-K/охолодження Мощний комплект 6ядер"
}
```
**Семпл #33:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/intel-i7-950-3-3-3ghz-ohlad-materinka-komplekt-8potokv-dlya-pk-ID102Zhl.html",
  "title": "Intel i7-950 3-3.3Ghz/охлад/Материнка Комплект 8потоків для ПК"
}
```
**Семпл #34:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/i7-4820k-3-9ghz-gigabyte-x79-ohlad-moschniy-komplekt-8potokv-ID1030mQ.html",
  "title": "i7-4820K 3.9Ghz/Gigabyte X79/охлад Мощний комплект 8потоків"
}
```
**Семпл #35:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/intel-i5-7500-3-4-3-8ghz-materinka-h270-ohlad-moschniy-bistriy-komplekt-s1151-dlyapk-ID10gPjj.html",
  "title": "Intel i5-7500 3.4-3.8ghz/Материнка H270/охлад Мощний бистрий комплект s1151 дляПК"
}
```
**Семпл #36:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/nova-materinska-plata-jginyue-b850m-pro-am5-ID1110Pk.html",
  "title": "Нова Материнська плата JGINYUE B850M PRO AM5"
}
```
**Семпл #37:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Материнская плата ASUS M4A78"
}
```
**Семпл #38:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/mat-plata-msi-b450a-pro-amd-am4-ryzen-IDZQyCN.html",
  "title": "Мат плата MSI B450A-Pro AMD AM4 Ryzen"
}
```
**Семпл #39:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Плата материнська,,Asus M2M  E+процесор"
}
```
**Семпл #40:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/msi-h81m-p33-soc-1150-usb3-dvi-intel-core-i3-4150-IDXfPlV.html",
  "title": "MSI H81M-P33 (soc 1150, USB3, DVI)+Intel Core i3-4150"
}
```
**Семпл #41:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/msi-b150m-pro-vhsoket-1151v1-core-i5-6500-3-2ghz-kuler-IDYLQyj.html",
  "title": "MSI B150M PRO-VH(сокет 1151v1) + Core i5-6500 3.2GHz + кулер"
}
```
**Семпл #42:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/komplekt-x99-xd3-intel-xeon-e5-2698b-v3-do-3-4-ghz-32gb-4x8gb-16-yader-32-potoki-ddr3-1866-mhz-ecc-reg-quad-channel-tpm-2-0-secure-boot-ID10WCch.html",
  "title": "Комплект X99-XD3 + Intel Xeon E5-2698B v3 до 3.4 GHz + 32GB (4x8GB), 16 ядер/32 потоки, DDR3 1866 MHz ECC Reg quad channel, TPM 2.0, Secure Boot"
}
```
**Семпл #43:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/kompyuternaya-sborka-asrock-g41m-vs3-i-xeon-e5430-IDWKdxF.html",
  "title": "Компьютерная сборка Asrock g41m-vs3 и Xeon e5430"
}
```
**Семпл #44:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/biostar-a58ml-ver-7-6-soket-fm2-i-drugie-pod-remont-zapchasti-IDUIquJ.html",
  "title": "BIOSTAR A58ML ver 7.6 (Сокет FM2+) и другие под РЕМОНТ \\ ЗАПЧАСТИ"
}
```
**Семпл #45:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Материнська плата MSI 970A-G46 (sAM3+, AMD970, PCI-E 2.0x16)"
}
```
**Семпл #46:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/materinska-plata-asus-prime-b365m-a-IDYCUHx.html",
  "title": "Материнська плата Asus Prime B365M-A"
}
```
**Семпл #47:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Материнська плата m2a480vp-pb jetway"
}
```
**Семпл #48:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/personalniy-kompyuter-dlya-gor-ta-roboti-core-i9-9900k-512-gb-nvme-ssd-ID10tEPt.html",
  "title": "Персональний Компютер для Ігор Та роботи Core i9 9900k  512 Гб NVME SSD"
}
```
**Семпл #49:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/komplekt-am3-8gb-ddr3-ID110PD8.html",
  "title": "Комплект AM3+ 8GB DDR3"
}
```
**Семпл #50:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/intel-i7-6700-4-0ghz-kuler-materinka-asus-bistriy-moschniy-komplekt-s1151-IDZQ3nF.html",
  "title": "Intel i7-6700 4.0ghz +кулер+ материнка ASUS  Бистрий мощний комплект s1151"
}
```
**Семпл #51:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/intel-i5-6600-3-9ghz-ohlad-materinka-s1151-komplektdlya-sistemnogo-bloka-IDZOsOh.html",
  "title": "intel i5-6600 3.9Ghz+охлад+Материнка s1151 Комплектдля системного блока"
}
```
**Семпл #52:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Материнская плата Gigabyte Ga-H11OM-S2H+проц"
}
```
**Семпл #53:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Комплект контроллеров Danfoss (EKC 302B + EKC 202D1 + модуль EKA 178A)"
}
```
**Семпл #54:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/igrovoy-komplekt-msi-a520m-a-pro-ryzen-5-3500x-amd-amd-rayzen-5-am4-IDXhfMs.html",
  "title": "Игровой комплект MSI A520M A PRO Ryzen 5 3500X амд amd райзен 5 am4"
}
```
**Семпл #55:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/materinska-plata-socket-am4-a320m-asrock-a320m-hdv-rev-4-02-ddr4-m-2-nvme-ID110XMl.html",
  "title": "Материнська плата Socket AM4 A320M / ASRock A320M-HDV / REV. 4.02 / DDR4 / M.2 NVMe"
}
```
**Семпл #56:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/materinska-plata-asus-prime-a320m-k-sam4-amd-a320-IDYNAc7.html",
  "title": "Материнська плата Asus Prime A320M-K (sAM4, AMD A320 )"
}
```
**Семпл #57:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/materinska-plata-gigabyte-ga-h270-hd3-s1151-g6-7-intel-h270-4ddr4-ID10ssEk.html",
  "title": "Материнська плата Gigabyte GA-H270-HD3 s1151 g6-7 Intel H270 4*DDR4"
}
```
**Семпл #58:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Материнські плати, процесори, ретро"
}
```
**Семпл #59:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/materinskaya-plata-msi-b350-ryzen-5-1600-3-2ghz-sam4-IDYKrg3.html",
  "title": "Материнская плата MSI B350 + Ryzen 5 1600 3.2GHz, sAM4"
}
```
**Семпл #60:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/materinskaya-plata-asus-prime-b350-plus-sam4-ID10AQBJ.html",
  "title": "Материнская плата ASUS PRIME B350 -PLUS , sAM4"
}
```
**Семпл #61:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/materinska-plata-msi-h110m-pro-d-s1151-intel-h110-IDZ8nwW.html",
  "title": "Материнська плата MSI H110M PRO-D (s1151, Intel H110)"
}
```
**Семпл #62:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/materinskaya-plata-asus-z170-pro-gaming-s-protsessorom-intel-core-i5-6600k-ID10PwxP.html",
  "title": "Материнская плата asus z170 pro gaming с процессором intel core i5 6600k"
}
```
**Семпл #63:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/xeon-e5-2650v3-materinskaya-plata-ID11109l.html",
  "title": "Xeon e5 2650v3 + материнская плата"
}
```
**Семпл #64:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/prodam-materinskuyu-platu-supermicro-a2sdi-4c-hln4f-intel-atom-c3558-64gb-ecc-ram-ID10EnAj.html",
  "title": "Продам материнскую плату Supermicro A2SDI-4C-HLN4F Intel Atom C3558 + 64gb ecc ram"
}
```
**Семпл #65:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/rozstrochka-3-msyats-vd-mono-ryzen-7-7700-gigabyte-b850-eagle-wifi6e-be-quiet-pure-rock-3lx-topoviy-groviy-komplekt-am5-ID10WKqz.html",
  "title": "РОЗСТРОЧКА 3 МІСЯЦІ ВІД МОНО! Ryzen 7 7700, Gigabyte B850 Eagle WiFi6E, Be Quiet! Pure Rock 3LX топовий ігровий комплект АМ5"
}
```
**Семпл #66:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/komplekt-intel-core-i5-9400f-asus-prime-h310m-k-r2-0-ID10XJGC.html",
  "title": "Комплект Intel Core i5-9400F + ASUS PRIME H310M-K R2.0"
}
```
**Семпл #67:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/komplekt-materinskaya-plata-protsessor-xeon-e3-1230-v6-4-8-yadra-i7-7700-16-gb-ddr-4-ID10TMlj.html",
  "title": "Комплект материнская плата + процессор xeon e3 1230 v6 4/8 ядра (i7 7700) + 16 gb ddr 4"
}
```
**Семпл #68:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Нова NZXT N9 Z890 LGA 1851 ATX Gaming Motherboard White pcie 5.0"
}
```
**Семпл #69:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/materinskaya-plata-socket-1151-b250a-btc-ne-rabochaya-ID10PnWT.html",
  "title": "Материнская плата Socket 1151 B250A-BTC не рабочая!"
}
```
**Семпл #70:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/klka-shtuk-s1200-materinka-gigabyte-h410m-s2h-v2-dlya-10-pokolnnya-IDZDOnt.html",
  "title": "Є кілька штук. s1200 материнка Gigabyte H410M S2H V2 для 10 покоління"
}
```
**Семпл #71:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Biostar P31B-A7 + Celeron 3.06 + DDR2"
}
```
**Семпл #72:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/materinskaya-plata-gigabyte-ga-z68p-ds3-i3-3240-8gb-ddr3-IDPsJQk.html",
  "title": "Материнская плата Gigabyte GA-Z68P-DS3 i3-3240 + 8GB DDR3"
}
```
**Семпл #73:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/materinskaya-plata-h55itx-a-e-wifi-i3-560-IDPsJGH.html",
  "title": "Материнская плата H55ITX-A-E WIFI i3-560"
}
```
**Семпл #74:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/materinskaya-plata-gigabyte-ga-h61m-d2h-usb3-rev1-0-lga1155-ID110DP1.html",
  "title": "Материнская плата Gigabyte GA-H61M-D2H-USB3 rev1.0 LGA1155"
}
```
**Семпл #75:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Материнська плата AN515-57 N20C1  3050ti i5- 11400H\n\nПроцес"
}
```
**Семпл #76:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Корпус до персонального компютера"
}
```
**Семпл #77:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Материнская плата gigabyte GA-MA69VM-S2"
}
```
**Семпл #78:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/asus-prime-b250-plus-ID10hpXL.html",
  "title": "asus prime B250-PLUS"
}
```
**Семпл #79:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/materinskaya-plata-msi-x79a-gd45-intel-core-i7-4930k-3-4ghz-kuler-socket-2011-garantiya-1-god-ID10c0yt.html",
  "title": "Материнская плата MSI X79A-GD45 + Intel Core i7-4930K 3,4GHz + кулер (Socket 2011) Гарантия 1 год"
}
```
**Семпл #80:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/materinskaya-plata-gigabyte-b450m-s2h-am4-ID10ZVOH.html",
  "title": "Материнская плата Gigabyte B450M S2H AM4"
}
```
**Семпл #81:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/groviy-komplekt-asus-tuf-b450m-pro-gaming-amd-ryzen-5-5600-ID10Z98t.html",
  "title": "Ігровий комплект Asus Tuf B450M-PRO Gaming + AMD Ryzen 5 5600"
}
```
**Семпл #82:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Материнська плата MSI MS-6507"
}
```
**Семпл #83:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Материнська плата DELL MT3804"
}
```
**Семпл #84:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Продаю материнську плату відразу з чіпом"
}
```
**Семпл #85:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/materinskaya-plata-gigabyte-ga-g31m-es2-s775-IDTBWLz.html",
  "title": "Материнская плата Gigabyte GA-G31M-ES2/ s775"
}
```
**Семпл #86:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/msi-h81m-p33-soc-1150-usb3-dvi-intel-core-i3-4150-IDXfPlV.html",
  "title": "MSI H81M-P33 (soc 1150, USB3, DVI)+Intel Core i3-4150"
}
```
**Семпл #87:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Материнская плата"
}
```
**Семпл #88:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/komplekt-materinska-plata-msi-h310-pro-vdh-plus-i3-9100f-4-2ggts-kuler-deepcool-gammaxx-300-vse-spravne-ID110YQH.html",
  "title": "Комплект материнська плата MSI H310 PRO VDH PLUS + i3 9100F 4.2Ггц + кулер DeepCool GAMMAXX 300, все справне"
}
```
**Семпл #89:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/igrovoy-komplekt-msi-a520m-a-pro-ryzen-5-3500x-amd-amd-rayzen-5-am4-IDXhfMs.html",
  "title": "Игровой комплект MSI A520M A PRO Ryzen 5 3500X амд amd райзен 5 am4"
}
```
**Семпл #90:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Материнская плата Asus F80CR"
}
```
**Семпл #91:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Майн плата Філіпс 42PFL4208T/12 під ремонт"
}
```
**Семпл #92:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/materinska-plata-gigabyte-b850-aorus-elite-wi-fi7-ice-ID10YIvb.html",
  "title": "Материнська плата GIGABYTE B850 AORUS ELITE WI-FI7 ICE"
}
```
**Семпл #93:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/komplekt-gigabyte-ga-a88xm-d3h-amd-a8-7600-ID10R7dP.html",
  "title": "Комплект Gigabyte GA-A88XM-D3H + AMD A8-7600"
}
```
**Семпл #94:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/materinskaya-plata-asus-h110m-k-intel-pentium-g4400-ID10WbKR.html",
  "title": "Материнская плата Asus h110m-k + intel pentium g4400"
}
```
**Семпл #95:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/prodam-komplektom-asrock-b760-pro-rs-intel-i7-14700k-ID10xnSV.html",
  "title": "Продам комплектом asrock b760 pro rs і Intel i7 14700k"
}
```
**Семпл #96:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Материнская плата ASUS P5Q, процессор и оперативная память"
}
```
**Семпл #97:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Asus p7p55d deluxe s1156+подарунок)"
}
```
**Семпл #98:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/komplekt-asrock-n68c-gs-prots-amd-fx-6300-6-yader-pamyat-4gb-kuler-ID10gN6X.html",
  "title": "Комплект AsRock N68C-GS + проц amd fx 6300 (6 ядер) + память 4гб + Кулер"
}
```
**Семпл #99:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/prodam-platu-micro-itx-onda-b650plus-itx-am5-ddr5-IDZEs1t.html",
  "title": "Продам плату Micro ITX ONDA B650PLUS-ITX AM5 DDR5."
}
```
**Семпл #100:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Комплект старих комплектуючих ПК: Foxconn Socket 775, відеокарти, кулери, DVD-приводи"
}
```

#### ⚡ Блоки живлення — Відсіяно (100):
**Семпл #1:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/polumodulnyy-blok-pitaniya-be-quiet-dark-power-pro-550w-gold-garantiya-1-god-ID10VM7s.html",
  "title": "Полумодульный блок питания Be quiet Dark Power PRO 550w GOLD Гарантия 1 год"
}
```
**Семпл #2:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/blok-zhivlennya-vinga-vps-1350-1350vt-ID110Kdf.html",
  "title": "Блок живлення Vinga VPS-1350 1350Вт"
}
```
**Семпл #3:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/blok-zhivlennya-dlya-pk-650w-750w-850w-yak-nov-garantya-servs-IDX27KE.html",
  "title": "Блок живлення для Пк 650w 750w 850w як нові ,гарантія, сервіс !"
}
```
**Семпл #4:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/blok-zhivlennya-500w-vinga-vps-500apfc-4-4-cpu-6-2-gpu-trade-in-ID10nH3u.html",
  "title": "блок живлення 500W VINGA VPS-500APFC (4+4 CPU \\ 6+2 GPU). Trade-IN"
}
```
**Семпл #5:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/be-quiet-system-power-10-650w-80-bronze-ID1111I5.html",
  "title": "be quiet! System Power 10 650w 80+ Bronze"
}
```
**Семпл #6:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/blok-zhivlennya-atng-ata-800fb-b-800w-ID1111DS.html",
  "title": "Блок живлення ATNG ATA-800FB-B 800W"
}
```
**Семпл #7:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Кабелі живлення для блоку живлення PCI-E, SATA"
}
```
**Семпл #8:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/blok-zhivlennya-griffon-400-w-IDY4yKD.html",
  "title": "Блок живлення Griffon 400 w"
}
```
**Семпл #9:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/blok-zhivlennya-850w-thermaltake-rgb-IDXCFoc.html",
  "title": "Блок живлення 850W Thermaltake RGB"
}
```
**Семпл #10:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/blok-zhivlennya-na-750w-vd-cooler-master-gold-ID11118Q.html",
  "title": "Блок живлення на 750W від Cooler Master (Gold)"
}
```
**Семпл #11:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/corsair-rm1000-shift-blok-zhivlennya-ID10PvH7.html",
  "title": "Corsair RM1000 SHIFT блок живлення"
}
```
**Семпл #12:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/blok-pitanie-gamemax-modelgm-700b-700w-ID11114I.html",
  "title": "Блок питание GameMax MODEL:GM- 700B, 700w"
}
```
**Семпл #13:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/modulniy-blok-zhivlennya-650w-chieftec-a80-ctg-650c-trade-in-ID10nFRY.html",
  "title": "модульний блок живлення 650W Chieftec A80 CTG-650C. Trade-IN"
}
```
**Семпл #14:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/blok-zhivlennya-msi-mpg-pcie5-1000-vt-80-gold-ID10Sr77.html",
  "title": "Блок живлення MSI MPG PCIE5 1000 Вт 80+ Gold"
}
```
**Семпл #15:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Перехідник  процесору CPU/відеокарти GPU (4-8, 6-8, 4-6 pin)/MOLEX"
}
```
**Семпл #16:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/blok-zhivlennya-seasonic-focus-gx-750-750w-ssr-750fx-3366-IDYDB3P.html",
  "title": "Блок живлення Seasonic Focus GX-750 750W (SSR-750FX) - 3366"
}
```
**Семпл #17:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/blok-zhivlennya-650w-chieftec-ctb-650s-2x6-2pin-gpu-IDYbjoT.html",
  "title": "Блок живлення 650W Chieftec CTB-650S 2x6+2pin GPU"
}
```
**Семпл #18:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/blok-zhivlennya-380w-acbel-pc9045-za1g-IDYbiMi.html",
  "title": "Блок живлення 380W AcBel PC9045-ZA1G"
}
```
**Семпл #19:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/blok-zhivlennya-700w-bequiet-system-power-bqt-s6-sys-ua-700w-80-IDZM23Y.html",
  "title": "Блок живлення 700W beQuiet! System Power BQT S6-SYS-UA-700W 80+"
}
```
**Семпл #20:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Блок живлення для компютера"
}
```
**Семпл #21:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Блок живлення Paptoxx RAP-PRO-450"
}
```
**Семпл #22:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Блок питания YP20106P"
}
```
**Семпл #23:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/blok-zhivlennya-chieftec-gpa-500s8-500w-IDY3gVf.html",
  "title": "Блок живлення Chieftec GPA-500S8 500W"
}
```
**Семпл #24:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Кулера разные на U , диаметр , обороты"
}
```
**Семпл #25:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Модульные провода белого цвета комплектом для блока питания."
}
```
**Семпл #26:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/blok-zhivlennya-chieftec-a-135-1000w-atx-80-plus-bronze-IDZQA5r.html",
  "title": "Блок живлення Chieftec A-135 1000W ATX 80 PLUS Bronze"
}
```
**Семпл #27:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/bloki-zhivlennya-dlya-grovih-pk-be-quiet-thermaltake-300-850w-6-8pin-gpu-IDVRY8d.html",
  "title": "Блоки живлення для ігрових ПК Be quiet Thermaltake 300-850W 6/8pin GPU"
}
```
**Семпл #28:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/corsair-tx850-850w-IDYTNK9.html",
  "title": "Corsair TX850 850W"
}
```
**Семпл #29:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Corsair RM850x 80 Plus Gold 2020 рік Блок живлення ігровий модульний gtx rtx gt rx mx gaming oc"
}
```
**Семпл #30:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Блок живлення APW9"
}
```
**Семпл #31:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/blok-zhivlennya-chieftec-gpa-500s-500w-ID10PwsP.html",
  "title": "Блок живлення Chieftec GPA-500S 500W"
}
```
**Семпл #32:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Блок живлення для компютера"
}
```
**Семпл #33:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/blok-pitaniya-chieftec-a80-ctg-650c-modulnyy-650-vatt-ID10srUx.html",
  "title": "Блок питания Chieftec  A80 CTG-650C  (Модульный)  650 Ватт"
}
```
**Семпл #34:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/bp-axes-400-vatt-ID10Eo0u.html",
  "title": "БП Axes 400 ватт"
}
```
**Семпл #35:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/blok-zhivlennya-chieftec-850w-80-bronze-povnstyu-spravniy-ID110Zte.html",
  "title": "Блок живлення Chieftec 850W 80+ Bronze – повністю справний"
}
```
**Семпл #36:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/blok-pitaniya-chieftec-400w-IDZLgmh.html",
  "title": "Блок питания Chieftec 400w"
}
```
**Семпл #37:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/blok-zhivlennya-seasonic-atx-750w-black-v-dealnomu-stan-z-garantyu-ID10YS18.html",
  "title": "Блок живлення SEASONIC ATX 750W Black в ідеальному стані з гарантією"
}
```
**Семпл #38:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/prodam-blok-pitaniya-aerocool-vx-400-plus-ID10EnJX.html",
  "title": "Продам блок питания  Aerocool VX-400 PLUS"
}
```
**Семпл #39:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Переходник с MOLEX на SATA POWER"
}
```
**Семпл #40:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Блок питание оригенальный HP"
}
```
**Семпл #41:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/blok-pitaniya-chieftec-850w-ID10je7Q.html",
  "title": "Блок питания chieftec 850w"
}
```
**Семпл #42:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/blok-pitaniya-chieftec-powerup-750w-ID10ZRL3.html",
  "title": "Блок питания Chieftec PowerUP 750w"
}
```
**Семпл #43:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Блок живлення Thermalright Ag-750"
}
```
**Семпл #44:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/kenweiipc-kw-1600wpf-90-plus-gold-1600w-btc-mining-ai-ii-IDZjWrN.html",
  "title": "Kenweiipc KW-1600WPF - 90 PLUS GOLD | 1600W, BTC, MINING, AI, ИИ"
}
```
**Семпл #45:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/blok-zhivlennya-dlya-kompyutera-400-vat-IDW5pGZ.html",
  "title": "Блок живлення для компютера 400 Ват"
}
```
**Семпл #46:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Блок живлення Seasonic FOCUS PX-550"
}
```
**Семпл #47:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/blok-zhivlennya-corsair-cs750m-750w-napvmodulniy-ID10KI7E.html",
  "title": "Блок живлення Corsair CS750M 750W — напівмодульний"
}
```
**Семпл #48:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/blok-zhivlennya-t-f-skywindintl-tf-2000w-IDXmcrF.html",
  "title": "Блок живлення T.F.SKYWINDINTL TF-2000W"
}
```
**Семпл #49:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/prodam-bloki-zhivlennya-400-500vt-IDVVT1J.html",
  "title": "Продам Блоки живлення - 400-500Вт"
}
```
**Семпл #50:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/blok-pitaniya-frontier-atx-400-IDYt2QQ.html",
  "title": "Блок питания Frontier atx-400"
}
```
**Семпл #51:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/blok-zhivlennya-dell-6mvjh-250w-24-pin-IDVSQjl.html",
  "title": "Блок живлення Dell 6MVJH / 250W / 24-Pin"
}
```
**Семпл #52:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Компютерний блок живлення."
}
```
**Семпл #53:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Нові Блоки живлення BITMAIN APW12 14-17v (B) для S19 (xp), K7, L7, KS3"
}
```
**Семпл #54:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/850w-750w-650w-550w-450w-yaksn-brendov-bloki-zhivlennya-protestovan-povnstyu-roboch-stan-garniy-ID10KwGv.html",
  "title": "850W 750W 650W 550W 450W Якісні брендові блоки живлення Протестовані повністю робочі Стан гарний"
}
```
**Семпл #55:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/blok-zhivlennya-enermax-revolution-d-f-2-1050w-80-gold-ID10PRWt.html",
  "title": "Блок живлення enermax revolution d.f. 2 1050w 80+ gold"
}
```
**Семпл #56:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/12v-800w-serverniy-blok-zhivlennya-hp-80-platinum-hstns-pl41-pd41-g9-10-IDT13N0.html",
  "title": "12V 800W серверний блок живлення HP 80+ Platinum HSTNS-PL41 PD41 G9-10"
}
```
**Семпл #57:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/blok-zhivlennya-gamemax-gp-450w-IDVwvnv.html",
  "title": "Блок живлення GameMax GP 450w"
}
```
**Семпл #58:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Блок живлення GameMax GP 750B WH"
}
```
**Семпл #59:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/sistemniy-blok-phenom-x6-3-2-ghz-8gb-ram-1tb-120gb-rom-radeon-290-4gb-IDZOKLe.html",
  "title": "Системний блок Phenom X6 3.2 GHz/8GB RAM/1Tb+120Gb ROM/Radeon 290 4GB"
}
```
**Семпл #60:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Продаю 2 бп, блока питания"
}
```
**Семпл #61:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Оригінальний кабель живлення Samsung \n- 3903-001130\n- 3 m\n- гарантія 3"
}
```
**Семпл #62:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/zalman-megamax-zm700-txii-700w-IDY4tDN.html",
  "title": "Zalman MegaMax ZM700-TXII 700W"
}
```
**Семпл #63:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Адаптер живлення AD 12/1A RH48-1201000dg LYNKSYS"
}
```
**Семпл #64:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Блок питания ATX Gigabyte P850GM живлення"
}
```
**Семпл #65:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Блок живлення    POWER LW1600PG ,"
}
```
**Семпл #66:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/blok-zhivlennya-premalniy-groviy-topoviy-chieftec-navitas-1250w-sertifkat-gold-plomba-stan-novogo-potuzhniy-ID10suls.html",
  "title": "Блок живлення преміальний,ігровий топовий Chieftec Navitas 1250W сертифікат Gold,пломба , стан нового, потужний"
}
```
**Семпл #67:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/blok-zhivlennya-seasonic-vertex-gx-1200-1200w-gold-12122-gxafs-5475-IDYEgkT.html",
  "title": "Блок живлення Seasonic Vertex GX-1200 1200W Gold (12122 GXAFS) - 5475"
}
```
**Семпл #68:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/blok-pitaniya-be-quiet-dark-power-pro-1500w-ID10ZRi8.html",
  "title": "Блок питания Be Quiet Dark Power Pro 1500w"
}
```
**Семпл #69:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/blok-pitaniya-1stplayer-ps-500fk-500w-IDVG8u3.html",
  "title": "Блок питания 1stplayer ps-500fk 500w"
}
```
**Семпл #70:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/blok-zhivlennya-thermaltake-smart-700w-rgb-garantya-6-msyatsv-ID110XvP.html",
  "title": "Блок живлення Thermaltake Smart 700W RGB Гарантія 6 Місяців"
}
```
**Семпл #71:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Блок питания на 230 вольт"
}
```
**Семпл #72:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Блок живлення - зарядний пристрій DELTA ESR-48/30d 1800W"
}
```
**Семпл #73:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/bloki-pitaniya-chieftec-500vt-IDZNQAT.html",
  "title": "Блоки  питания Chieftec 500вт."
}
```
**Семпл #74:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Блок питания G.C.I. 230W Блок живлення 230 Вт"
}
```
**Семпл #75:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Продам блок питания монитора и трансформаторы."
}
```
**Семпл #76:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/blok-pitaniya-1600w-formata-atx-standartnyy-IDXoFpV.html",
  "title": "Блок питания 1600w формата ATX (стандартный)"
}
```
**Семпл #77:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/blok-pitaniya-1250w-gold-otlichnyy-ID10lHQ9.html",
  "title": "Блок питания 1250w Gold отличный"
}
```
**Семпл #78:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Блок питания Emerson 1975w майнинг"
}
```
**Семпл #79:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "NEW Блоки живлення BITMAIN APW12 (APW121215a) для S19/ T19/ L7/ K7"
}
```
**Семпл #80:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/seasonic-prime-platinum-1300w-ssr-1300pd-platinum-flagman-etalonn-testi-plomba-rtx-rx-gtx-gt-mx-gaming-oc-ID10Paim.html",
  "title": "Seasonic PRIME Platinum 1300W (SSR-1300PD) Platinum Флагман  Еталонні тести  Пломба rtx rx gtx gt mx gaming oc"
}
```
**Семпл #81:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/blok-zhivlennya-seasonic-prime-tx-1000-1000w-titanium-ssr-1000tr-5468-ID10UXPk.html",
  "title": "Блок живлення Seasonic Prime TX-1000 1000W Titanium (SSR-1000TR) - 5468"
}
```
**Семпл #82:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/blok-zhivlennya-gamemax-ge-700-700w-ID10MiIC.html",
  "title": "Блок живлення GameMax GE-700 700W"
}
```
**Семпл #83:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/blok-zhivlennya-chieftec-ctg-500-80p-IDXCykJ.html",
  "title": "Блок живлення CHIEFTEC CTG-500-80P"
}
```
**Семпл #84:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Блок живлення IBM ASTEC AA23920L 2880W"
}
```
**Семпл #85:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Блок питания для пк"
}
```
**Семпл #86:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Блоки живлення із моніторів. Ціна за все"
}
```
**Семпл #87:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/super-flower-combat-sfx-750w-80-gold-atx-3-1-blok-zhivlennya-noviy-ID110VIA.html",
  "title": "Super Flower Combat SFX 750w (80+ Gold,ATX 3.1) Блок живлення новий"
}
```
**Семпл #88:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Блок питания ASUS ADP-90SB bb оригинальный с сетевым кабелем."
}
```
**Семпл #89:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Блок питания Emerson 3500 w, роспайка 8pin+6pin+Pico"
}
```
**Семпл #90:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/blok-zhivlennya-1150w-aerocool-imperator-templarius-ID110VpJ.html",
  "title": "Блок живлення 1150w Aerocool Imperator Templarius"
}
```
**Семпл #91:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/prodam-blok-zhivlennya-chieftec-i-arena-400w-ID10gKWJ.html",
  "title": "Продам блок живлення Chieftec i-arena 400w"
}
```
**Семпл #92:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/blok-zhivlennya-vinga-vps-1350-be-quiet-system-power-700w-ID10QKiV.html",
  "title": "Блок живлення Vinga VPS 1350, be quiet System Power 700W"
}
```
**Семпл #93:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Кабеля  модульного БП  Chieftec A135. Be Quiet и нерабочие БП Chieftec"
}
```
**Семпл #94:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Seasonic Prime PX-650 80 Plus Platinum (SSR-650PD) модульний блок живлення Рідна пломба  гарний стан Ультимативний rtx gtx gt gaming oc rx"
}
```
**Семпл #95:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/bp-pccooler-hw600-np-600w-ID110V6p.html",
  "title": "Бп PcCooler HW600-NP 600w"
}
```
**Семпл #96:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/blok-zhivlennya-vinga-vps-1350w-80-bronze-IDXjXmI.html",
  "title": "Блок живлення Vinga VPS 1350W 80+ Bronze"
}
```
**Семпл #97:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Msi mpg A850G PCIE5"
}
```
**Семпл #98:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Блок живлення Gigabyte P650b"
}
```
**Семпл #99:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/thermaltake-650w-ID110V0X.html",
  "title": "Thermaltake 650w"
}
```
**Семпл #100:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/blok-zhivlennya-na-400-vt-IDUee0k.html",
  "title": "Блок живлення на 400 вт"
}
```

#### 💾 Накопичувачі — Відсіяно (100):
**Семпл #1:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/nakopitel-ssd-m-2-sata-1tb-razmery-22h42-100-zdorovya-ID10Qy7r.html",
  "title": "Накопитель SSD M.2 SATA-1TB. Размеры 22х42. 100% здоровья."
}
```
**Семпл #2:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/zhorstkiy-disk-western-digital-black-500gb-7200rpm-32mb-wd5000lplx-2-5-sata-iii-ID10LKBP.html",
  "title": "Жорсткий диск Western Digital Black 500GB 7200rpm 32MB WD5000LPLX 2.5 SATA III"
}
```
**Семпл #3:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/ssd-crucial-p3-plus-4tb-ID10YNJp.html",
  "title": "SSD Crucial P3 Plus 4TB"
}
```
**Семпл #4:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Продам диски SSD и HDD"
}
```
**Семпл #5:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/ssd-disk-rgb-adata-xpg-spectrix-s20g-1tb-m-2-nvme-pcie-3-0-x4-3d-nand-ID10skZB.html",
  "title": "SSD диск rgb adata XPG SPECTRIX S20G 1TB M.2 nvme PCIe 3.0 x4 3D NAND"
}
```
**Семпл #6:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/zhorstkiy-disk-hdd-toshiba-500gb-3-5-sata-iii-7200-rpm-2-sht-ID10Pn6E.html",
  "title": "Жорсткий диск HDD Toshiba 500GB 3.5\" SATA III 7200 RPM. Є 2 шт."
}
```
**Семпл #7:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/ssd-disk-samsung-870-evo-series-500gb-2-5-sata-iii-v-nand-3bit-mlc-tlc-mz-77e500bw-mz-77e500b-eu-ID10Pn3F.html",
  "title": "SSD диск Samsung 870 Evo-Series 500GB 2.5\" SATA III V-NAND 3bit MLC (TLC) (MZ-77E500BW/MZ-77E500B/EU)"
}
```
**Семпл #8:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/nakopitel-ssd-2-5-256gb-as350-panther-apacer-ID110S6Y.html",
  "title": "Накопитель SSD 2.5\" 256GB AS350 PANTHER Apacer"
}
```
**Семпл #9:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/nakopitel-ssd-wd-green-240-gb-IDZQrT7.html",
  "title": "Накопитель SSD WD Green 240 Gb"
}
```
**Семпл #10:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/hdd-500gb-hgst-tayland-IDYSPTr.html",
  "title": "HDD 500gb HGST Тайланд"
}
```
**Семпл #11:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Жорсткий диск HDD 1T TOSHIBA"
}
```
**Семпл #12:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/zhorstkiy-disk-wd-purple-4tb-wd40purz-u-nayavnost-10-sht-ID10SFsT.html",
  "title": "Жорсткий диск WD Purple 4TB WD40PURZ — у наявності 10 шт."
}
```
**Семпл #13:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Продам жорсткий диск"
}
```
**Семпл #14:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/ssd-disk-nakopichuvach-samsung-evo-860-250gb-ID10mcNn.html",
  "title": "SSD диск накопичувач Samsung EVO 860 250гб"
}
```
**Семпл #15:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/lacie-1tb-1000gb-yaksn-zovnshn-udarostyk-diski-mala-narobotka-mayzhe-nov-stan-garniy-ID10UrPo.html",
  "title": "LaCie 1tb 1000GB Якісні зовнішні ударостійкі диски Мала нароботка майже нові Стан гарний"
}
```
**Семпл #16:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/ssd-samsung-960-pro-512-gb-b-u-ID10sk0m.html",
  "title": "SSD Samsung 960 PRO 512 GB б/у"
}
```
**Семпл #17:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/wd-blue-500gb-wd5000azlx-dealniy-stan-ID10sjYn.html",
  "title": "WD Blue 500GB (WD5000AZLX) — Ідеальний стан"
}
```
**Семпл #18:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Жорсткий диск Western Digital Blue 640GB 3.5\" SATA II (WD6400AAKS)"
}
```
**Семпл #19:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/prodam-nerobochiy-ssd-disk-m2-nvme-xraydisk-pro-1tb-ID110QR2.html",
  "title": "Продам неробочий ssd диск m2 nvme xraydisk pro 1tb"
}
```
**Семпл #20:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/vinchester-zhestkiy-disk-1tb-western-digital-wd-black-wd1003fzex-bystraya-seriya-rabochiy-IDYsFBI.html",
  "title": "Винчестер жесткий диск 1Tb Western Digital WD Black WD1003FZEX быстрая серия рабочий"
}
```
**Семпл #21:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Жорсткий диск для ПК 3,5\" HDD 1Тб SATA III"
}
```
**Семпл #22:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Комплект раритет! Жёсткие диски HDD"
}
```
**Семпл #23:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "‼️кабель-перехідник USB на SATA або IDE для HDD або SSD"
}
```
**Семпл #24:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/ssd-disk-m-2-agi-512gb-ID10uvtc.html",
  "title": "SSD диск M.2 Agi 512gb"
}
```
**Семпл #25:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Переходник USB 3.0 - SATA + адаптер питания для SSD и HDD 2.5 / 3.5"
}
```
**Семпл #26:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/ssd-disk-m-2-agi-512gb-ID10uvtc.html",
  "title": "SSD диск M.2 Agi 512gb"
}
```
**Семпл #27:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/zhorstkiy-disk-3-5-hdd-3-4-6tb-IDR6xAr.html",
  "title": "Жорсткий диск 3.5 HDD 3-4-6TB"
}
```
**Семпл #28:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/qnap-ux-800u-rp-8-bay-sas-storage-expansion-52tb-68tb-22tb-enterprise-ID10QJoD.html",
  "title": "QNAP UX-800U-RP 8-Bay SAS Storage Expansion 52TB (6×8TB + 2×2TB) Enterprise"
}
```
**Семпл #29:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Винчестер (жёсткий диск) Seagate ST-4096."
}
```
**Семпл #30:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/sandisk-optimus-gx-pro-8100-4tb-ID110Q4y.html",
  "title": "SANDISK Optimus GX PRO 8100 4tb"
}
```
**Семпл #31:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/samsung-9100-pro-2-tb-mz-vap2t0b-am-ID10ZILO.html",
  "title": "Samsung 9100 PRO 2 TB MZ-VAP2T0B/AM"
}
```
**Семпл #32:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/samsung-pm991a-512gb-nvme-pcie-m-2-2242-2280-ID110PBq.html",
  "title": "Samsung PM991a 512Gb NVMe PCIe M.2 2242/2280"
}
```
**Семпл #33:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/ssd-disk-bestoss-gm888-m-2-ssd-7100-6000mb-s-1tb-pcie-4-0x4-m-2-2280-nvme-ID10DXqn.html",
  "title": "SSD диск Bestoss GM888 M.2 SSD 7100/6000MB/s 1TB PCIe 4.0x4 M.2 2280 NVMe"
}
```
**Семпл #34:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "SSD диск 1.92TB SSD Intel D3-S4610-series"
}
```
**Семпл #35:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Bestoss S202 M.2 SATA NGFF.512/1t"
}
```
**Семпл #36:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/zhorstkiy-disk-hd-disk-500gb-ID10aRpG.html",
  "title": "Жорсткий диск HD Disk 500GB"
}
```
**Семпл #37:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/ssd-1tb-m2-nvme-pci-e-4-0-2280-samsung-ssd-disk-ID110PoB.html",
  "title": "SSD 1TB M2 NVMe PCI-E 4.0 2280 Samsung ссд диск"
}
```
**Семпл #38:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Раритетный жесткий диск Seagate ST343113A 4ГБ"
}
```
**Семпл #39:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/zhestkiy-disk-hdd-8tb-sata-3-5-hgst-ultrastar-he8-dell-7200rpm-enterprise-100-health-garantiya-ID10mSuL.html",
  "title": "Жесткий диск HDD 8TB SATA 3.5\" HGST Ultrastar He8 (Dell) 7200RPM Enterprise | 100% Health Гарантия!!!"
}
```
**Семпл #40:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/kingston-kc3000-4tb-m-2-2280-nvme-pcie-gen-4-0-x4-3d-tlc-nand-skc3000d-4096g-ID10QxaL.html",
  "title": "Kingston KC3000 4TB M.2 2280 NVMe PCIe Gen 4.0 x4 3D TLC NAND (SKC3000D/4096G)"
}
```
**Семпл #41:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/ssd-gigabyte-nvme-512gb-model-gp-gsm2ne3512gntd-ID1010UO.html",
  "title": "SSD Gigabyte NVMe 512GB (модель GP-GSM2NE3512GNTD)"
}
```
**Семпл #42:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/zhorstkiy-disk-toshiba-pc-p300-500-gb-sata-3-5-7200-ob-hv-ID10LIwz.html",
  "title": "Жорсткий диск Toshiba PC P300 500 ГБ SATA 3.5\" 7200 об/хв"
}
```
**Семпл #43:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/ssd-grucial-p3-plus-4tb-ID10ZgyS.html",
  "title": "SSD Grucial P3 Plus 4TB"
}
```
**Семпл #44:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/zhestkiy-disk-hitachi-deskstar-250-gb-IDLr9n8.html",
  "title": "Жесткий диск Hitachi Deskstar 250 gb"
}
```
**Семпл #45:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/ssd-disk-patriot-burst-elite-480gb-2-5-sataiii-tlc-pbe480gs25ssdr-ID110OMQ.html",
  "title": "SSD диск Patriot Burst Elite 480GB 2.5\" SATAIII TLC (PBE480GS25SSDR)"
}
```
**Семпл #46:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/zhorstkiy-disk-seagate-500-gb-IDJdQ2c.html",
  "title": "Жорсткий диск Seagate 500 GB"
}
```
**Семпл #47:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/zhorstk-diski-3-5-6tb-hp-enterprise-7200rpm-sata3-ID10TFBD.html",
  "title": "Жорсткі диски 3.5’ 6TB HP Enterprise 7200RPM SATA3"
}
```
**Семпл #48:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/ssd-disk-goodram-px600-1tb-m-2-2280-pcie-4-0-x4-nvme-3d-nand-qlc-ID110OHk.html",
  "title": "SSD диск Goodram PX600 1TB M.2 2280 PCIe 4.0 x4 NVMe 3D NAND QLC"
}
```
**Семпл #49:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/ssd-m-2-nvme-1tb-netac-nv7000-t-pcie-4-0-7300-mb-s-stan-100-ID110OEl.html",
  "title": "SSD M.2 NVMe 1TB Netac NV7000-t PCIe 4.0 (7300 MB/s) / Стан 100%"
}
```
**Семпл #50:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/disk-ssd-nakopitel-kingston-a400-240gb-sataiii-3d-tlc-sa400s37-240g-96-ID110ODJ.html",
  "title": "Диск SSD накопитель Kingston A400 240GB SATAIII 3D TLC (SA400S37/240G) 96%"
}
```
**Семпл #51:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/nakopichuvach-ssd-256gb-intel-545s-2-5-sataiii-tlc-ssdsc2kw256g8l-ID110Os8.html",
  "title": "Накопичувач SSD 256GB Intel 545s 2.5\" SATAIII TLC (SSDSC2KW256G8L)"
}
```
**Семпл #52:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/prodam-rostovku-novyh-ssd-diskov-64gb-4tb-priehali-vkusnyashki-IDZQCT0.html",
  "title": "Продам ростовку новых SSD дисков 64гб-4тб (приехали вкусняшки)"
}
```
**Семпл #53:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/zhorstk-diski-3-5-6tb-hp-enterprise-7200rpm-sata3-ID10TFBD.html",
  "title": "Жорсткі диски 3.5’ 6TB HP Enterprise 7200RPM SATA3"
}
```
**Семпл #54:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/16tb-gely-wd-wuh721816ale6l4-nas-sata-6gb-s-dc-hc550-synology-nas-b-u-IDZufyC.html",
  "title": "16TB Гелій WD WUH721816ALE6L4 Nas SATA 6Gb/s DC HC550 synology nas Б/у"
}
```
**Семпл #55:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "HDD 2.5\" Жесткие диски Toshiba Hitachi 160/320/500 Sata"
}
```
**Семпл #56:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/zhestkiy-disk-fujitsu-200gb-5400rpm-8mb-mhy2200bh-2-5-sata-IDYgRPY.html",
  "title": "Жесткий диск Fujitsu 200GB 5400rpm 8MB MHY2200BH 2.5 SATA"
}
```
**Семпл #57:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/western-digital-pasport-1-tb-ID10PoIH.html",
  "title": "Western digital pasport 1 tb"
}
```
**Семпл #58:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/zhestkiy-disk-wd-160gb-5400rpm-8mb-wd1600bevs-2-5-sata-IDYgRKQ.html",
  "title": "Жесткий диск WD 160GB 5400rpm 8MB WD1600BEVS 2.5 SATA"
}
```
**Семпл #59:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Жорсткий Диск DG146BB976 HP Enterprise 146GB 10K 2,5\" SAS"
}
```
**Семпл #60:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Жесткий диск i.norys"
}
```
**Семпл #61:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "SSD Patriot Viper VP4300 Lite M.2 на 1Т"
}
```
**Семпл #62:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Кабель SATA-USB, адаптер жесткого диска USB 3.0-SATA III"
}
```
**Семпл #63:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Память xbox 4GB оригинал"
}
```
**Семпл #64:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/termnovo-zhorstkiy-disk-western-digital-purple-pro-10tb-wd102purp-ID10RmuV.html",
  "title": "Терміново!!!Жорсткий диск Western Digital Purple Pro 10TB (WD102PURP)"
}
```
**Семпл #65:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/ssd-micron-2280-m2-nvme-pcie-1000-1024-gb-1tb-ID10HRAh.html",
  "title": "SSD Micron 2280 m2 NVMe PCie 1000/1024 Gb 1Tb"
}
```
**Семпл #66:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/ssd-samsung-pm871b-256gb-m-2-sata-iii-ID10STnR.html",
  "title": "SSD Samsung PM871b 256GB M.2 SATA III"
}
```
**Семпл #67:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/zhorstkiy-disk-wd-purple-4tb-wd40purz-u-nayavnost-10-sht-ID10SFsT.html",
  "title": "Жорсткий диск WD Purple 4TB WD40PURZ — у наявності 10 шт."
}
```
**Семпл #68:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/zhorstkiy-disk-wd-purple-500gb-1tb-2tb-3tb-4tb-8tb-IDVoDwf.html",
  "title": "Жорсткий диск WD Purple 500Gb, 1TB, 2TB, 3TB, 4TB, 8TB"
}
```
**Семпл #69:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Шлейф Sata 2.5 HDD/SSD для Acer Nitro 5  и Predator Helios 300."
}
```
**Семпл #70:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/goodram-cx400-128gb-ssd-sataiii-97-zhittya-550-mb-s-460-mb-s-ID110MJj.html",
  "title": "Goodram CX400 128Gb SSD SATAIII 97% життя (550 МБ/с, 460 МБ/с)"
}
```
**Семпл #71:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "SSD 128 жорсткий диск"
}
```
**Семпл #72:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/zhestkiy-disk-western-digital-wd3200aajs-320gb-ID10E8u6.html",
  "title": "Жесткий диск - Western digital wd3200aajs 320gb"
}
```
**Семпл #73:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/seagate-ironwolf-pro-14tb-st14000ne0008-nas-vdmnniy-stan-smart-ok-ID10RPke.html",
  "title": "Seagate IronWolf Pro 14TB ST14000NE0008 • NAS • Відмінний стан • SMART OK"
}
```
**Семпл #74:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/samsung-pm863a-240gb-ssd-sata-2-5-99-zhittya-mz-7lm240n-mz7lm240hmhq-v-nand-3d-tlc-sata-6-gb-s-plp-metaleviy-korpus-ID110MwO.html",
  "title": "Samsung PM863a 240Gb  SSD SATA 2.5 99% \"життя\" (MZ-7LM240N / MZ7LM240HMHQ) (V-NAND 3D TLC, SATA 6 Гб/с, PLP, металевий корпус)"
}
```
**Семпл #75:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/kingston-fury-renegade-2tb-nvme-gen-4-ID10PgMT.html",
  "title": "Kingston Fury Renegade 2TB NVMe (Gen 4)"
}
```
**Семпл #76:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "3.5\" Samsung sv1021h 10.2 Gb, sv0431d 4.3 Gb ATA"
}
```
**Семпл #77:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Адаптер-перехідник M.2 NVMe PCI-E 4.0/3.0 (M.2 SSD до PCI-E X1)"
}
```
**Семпл #78:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/zhorstkiy-disk-seagate-barracuda-2-5-st2000lm015-2tb-hdd-ID10Bwv3.html",
  "title": "Жорсткий диск Seagate BarraCuda 2,5\" (ST2000LM015) 2Tb HDD"
}
```
**Семпл #79:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/ssd-samsung-990-pro-2tb-m-2-nvme-noviy-100-resurs-ID10Z7em.html",
  "title": "SSD Samsung 990 PRO 2TB M.2 NVMe - новий, 100% ресурс"
}
```
**Семпл #80:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/ssd-samsung-850-pro-512gb-hdd-wd-1tb-green-IDZqWyC.html",
  "title": "SSD Samsung 850 Pro 512GB,  HDD WD 1TB Green"
}
```
**Семпл #81:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/zhestkiy-disk-1tb-western-digital-ID110LRd.html",
  "title": "Жесткий диск 1Tb Western Digital"
}
```
**Семпл #82:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Жорсткі диски. HDD 2,5\". Умовно працюючі."
}
```
**Семпл #83:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/16tb-gely-wd-wuh721816ale6l4-nas-sata-6gb-s-dc-hc550-synology-nas-b-u-IDZufyC.html",
  "title": "16TB Гелій WD WUH721816ALE6L4 Nas SATA 6Gb/s DC HC550 synology nas Б/у"
}
```
**Семпл #84:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Жорсткий диск HTC426020G7CE10 20 ГБ Travelstar 4200 об/хв 08K153"
}
```
**Семпл #85:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/3tb-western-digital-wd-sata-nas-IDZ639w.html",
  "title": "3TB western digital WD  SATA NAS"
}
```
**Семпл #86:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Жеский диск на терабайт"
}
```
**Семпл #87:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/zhostkiy-disk-80-gb-IDToJAT.html",
  "title": "Жосткий диск 80 Гб"
}
```
**Семпл #88:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Внутрішній жорсткий диск"
}
```
**Семпл #89:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/ssd-teamgroup-t2535t120g0c101-120gb-shvidkiy-ta-nadyniy-nakopichuvach-dlya-pk-noutbukv-ID110LbS.html",
  "title": "SSD TeamGroup T2535T120G0C101 120GB — швидкий та надійний накопичувач для ПК-Ноутбуків"
}
```
**Семпл #90:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/ssd-samsung-860-evo-mz-76e250-250gb-shvidkiy-ta-nadyniy-nakopichuvach-dlya-pk-noutbkv-ID110LnA.html",
  "title": "SSD Samsung 860 EVO (MZ-76E250) 250GB — швидкий та надійний накопичувач для ПК-Ноутбіків"
}
```
**Семпл #91:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/ssd-kingston-nv3-1tb-m-2-97-ID10WvQV.html",
  "title": "SSD Kingston NV3 1TB M.2  (97%)"
}
```
**Семпл #92:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/ssd-sk-hynix-pc711-1tb-nvme-m-2-gen3x4-ID110CTN.html",
  "title": "SSD SK Hynix PC711 1Tb NVMe M.2 Gen3x4"
}
```
**Семпл #93:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/goodram-cx400-gen-2-512-gb-ssd-ID110hvB.html",
  "title": "Goodram CX400 Gen.2 512 GB SSD"
}
```
**Семпл #94:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/ssd-kingston-kc-s44256-6f-256gb-shvidkiy-ta-nadyniy-nakopichuvach-dlya-pk-noutbukv-ID110Lhn.html",
  "title": "SSD Kingston KC-S44256-6F 256GB — швидкий та надійний накопичувач для ПК-Ноутбуків"
}
```
**Семпл #95:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/ssd-disk-nvme-256gb-ne-rabochiy-ID110Lms.html",
  "title": "SSD диск NVMe 256Gb - не рабочий"
}
```
**Семпл #96:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/zhorstkiy-disk-seagate-barracuda-2-5-st2000lm015-2tb-hdd-ID10Bwv3.html",
  "title": "Жорсткий диск Seagate BarraCuda 2,5\" (ST2000LM015) 2Tb HDD"
}
```
**Семпл #97:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/disk-ssd-sata3-256-512gb-2-5-nov-IDZwW6p.html",
  "title": "Диск SSD SATA3 256-512Gb 2.5 Нові!"
}
```
**Семпл #98:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Hdd 1000g WD 10ezex 3.5\""
}
```
**Семпл #99:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Розпродаж! Жорсткі диски на запчастини або під ремонт!"
}
```
**Семпл #100:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/hdd-1tb-2-5-7200-ID10E6v2.html",
  "title": "HDD 1Tb 2.5 7200"
}
```

#### 📟 Оперативна пам'ять — Відсіяно (100):
**Семпл #1:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/operativna-pamyat-samsung-16gb-ddr4-ecc-reg-rdimm-2133mhz-m393a2g40db0-cpb2q-x99-xeon-ID10Nrkr.html",
  "title": "Оперативна память Samsung 16GB DDR4 ECC REG RDIMM 2133MHz M393A2G40DB0-CPB2Q X99 Xeon"
}
```
**Семпл #2:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/operativna-pamyat-g-skill-trident-z-rgb-ddr4-4266-mhz-16-gb-2-x-8-gb-samsung-b-die-intel-ryzen-operativka-kingston-ID10QJZ3.html",
  "title": "Оперативна память G.skill Trident Z Rgb DDR4 4266 Mhz 16 Gb 2 x 8 gb Samsung b-die Intel ryzen оперативка kingston"
}
```
**Семпл #3:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/operativna-pamyat-kingston-ddr4-3200mhz-32gb-cl16-ID110gnC.html",
  "title": "Оперативна память kingston ddr4 3200mhz 32gb cl16"
}
```
**Семпл #4:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/operativna-pamyat-ddr5-32gb-4800-ID1111Hc.html",
  "title": "Оперативна память ddr5 32gb 4800"
}
```
**Семпл #5:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Оперативна память DDR 4 16 гб"
}
```
**Семпл #6:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Память оперативная ОЗУ RAM Hynix DDR2 256mb PC2-4200"
}
```
**Семпл #7:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/servernaya-ddr3-4gb-8gb-16gb-32gb-1333-1600mgts-pc3-10600-pamyat-ecc-reg-IDPrjdj.html",
  "title": "Серверная DDR3 4GB/8Gb/16GB/32GB 1333/1600мгц PC3-10600 память ECC REG"
}
```
**Семпл #8:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/novaya-ddr3-8gb-1600mhz-12800u-intel-amd-operativnaya-pamyat-dlya-pk-IDJXL1m.html",
  "title": "НОВАЯ DDR3 8GB 1600mhz 12800U Intel/AMD оперативная память для ПК"
}
```
**Семпл #9:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/samsung-ddr4-8gb-sostoyanie-otlichnoe-polnostyu-rabochiy-lyubye-testy-proverki-ID10Nkxu.html",
  "title": "Samsung ddr4 8gb состояние отличное полностью рабочий любые тесты проверки"
}
```
**Семпл #10:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/ddr1-ddr2-ddr3-operativnaya-pamyat-1gb-2gb-4gb-8gb-IDQDZVb.html",
  "title": "DDR1, DDR2, DDR3 оперативная память (1gb, 2gb, 4gb, 8gb)"
}
```
**Семпл #11:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Продам оперативну память GLOWAY DDR5 24GB (2x12GB) 5600 MT/s Біла (Б/В)"
}
```
**Семпл #12:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Модуль памяті для компютера Hynix DDR2 4Gb (4x1Gb)"
}
```
**Семпл #13:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Оперативна память 4gb"
}
```
**Семпл #14:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/ddr4-32gb-2x16gb-3200mhz-IDZBYWJ.html",
  "title": "Ddr4 32gb 2x16gb 3200mhz"
}
```
**Семпл #15:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/operativna-pamyat-crucial-ballistix-tactical-ddr3-8gb-1600mhz-cl8-blt8g3d1608dt1tx0-ID10fpus.html",
  "title": "Оперативна память Crucial Ballistix Tactical DDR3 8GB 1600MHz CL8 (BLT8G3D1608DT1TX0)"
}
```
**Семпл #16:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/serverna-operativna-pamyat-ddr3-reg-ecc-16gb-32gb-chastota-1333-1600-1866mgts-ID10mbGc.html",
  "title": "Серверна оперативна память DDR3 REG ECC 16gb і 32gb частота 1333 1600  1866мгц"
}
```
**Семпл #17:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Оперативная память Kingston DDR3-1333"
}
```
**Семпл #18:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Оперативная память DDR3 2GB/1333 Team Elite"
}
```
**Семпл #19:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Оперативная память DDR3L DDR2 GB RAM SDRAM SODIMM"
}
```
**Семпл #20:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/operativnaya-pamyat-ddr3-4gb-1600mhz-ddr3-4gb-dlya-pk-IDTZ6Gs.html",
  "title": "Оперативная память DDR3 4Gb 1600Mhz ДДР3 4Гб  для ПК"
}
```
**Семпл #21:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/pamyat-ddr4-16gb-kit-2x8-2400mhz-team-trade-in-ID10rinK.html",
  "title": "память DDR4 16GB Kit (2x8) 2400MHz Team. Trade-in"
}
```
**Семпл #22:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/ddr5-32gb-kit-patriot-viper-elite-5-ID10ZQDr.html",
  "title": "Ddr5 32gb kit patriot viper elite 5"
}
```
**Семпл #23:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Оперативная память DDR3 2"
}
```
**Семпл #24:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Память  DDR 400  2 шт х 256mb"
}
```
**Семпл #25:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Оперативна память Team Group 1/32gb 4800МГц"
}
```
**Семпл #26:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/serverna-pamyat-ddr4-32gb-4rx4-pc4-2133p-ecc-reg-2133mhz-hp-ID10QHbl.html",
  "title": "Серверна память DDR4 32Gb 4Rx4 PC4-2133P ECC REG 2133Mhz HP"
}
```
**Семпл #27:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/operativna-pamyat-ddr5-sodimm-16gb-1rx16-pc5-4800b-sco-1010-xt-IDZTv6C.html",
  "title": "Оперативна память ddr5 sodimm 16gb 1rx16 pc5-4800b-sco-1010 xt"
}
```
**Семпл #28:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/ozp-kingston-ddr4-2h8gb-3600mhz-fury-beast-rgb-black-ID10BDpD.html",
  "title": "ОЗП Kingston DDR4 2х8GB 3600Mhz FURY Beast RGB Black"
}
```
**Семпл #29:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/ssd-samsung-860-evo-500gb-ID10STzh.html",
  "title": "SSD Samsung 860 EVO 500GB"
}
```
**Семпл #30:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/operativna-pamyat-ddr4-8gb-ddr-3-8gb-IDZFVGh.html",
  "title": "Оперативна память ddr4 8gb ddr 3 8gb"
}
```
**Семпл #31:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Продам оперативную память ddr2 2×1g 800"
}
```
**Семпл #32:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/operativna-pamyat-dlya-noutbuka-4gb-ddr3-ID10ssWQ.html",
  "title": "Оперативна память для ноутбука 4GB DDR3"
}
```
**Семпл #33:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Оперативна память g.skill trident z 2x8 3200mhz"
}
```
**Семпл #34:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "ОЗУ DDR2 Kingston"
}
```
**Семпл #35:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Для ноутбука 16GB 2*8GB DDR3L 1600MHz Samsung PC3L 12800S 2Rx8 RAM Оперативна память"
}
```
**Семпл #36:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/operativna-pamyat-kingston-ddr3-8gb-4gb-4gb-ID10Ep3t.html",
  "title": "Оперативна память Kingston DDR3 8Gb (4Gb +4Gb)"
}
```
**Семпл #37:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/operativna-pamyat-g-skill-trident-z5-neo-rgb-ddr5-6000-32gb-f5-6000j3038f16gx2-tz5nr-ID10Xs9y.html",
  "title": "Оперативна память G.Skill Trident Z5 Neo RGB DDR5-6000 32GB (F5-6000J3038F16GX2-TZ5NR)"
}
```
**Семпл #38:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Kingston 1x16 GB ⤵️ DDR4 | FURY Beast Black | Оперативна память | Кількість!"
}
```
**Семпл #39:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Комплект Micron DDR3L 1867MHz 16GB (8+8) 1.35V 2Rx8 PC3L-14900 [ максимальна швидкість ], оперативна память, оригінал"
}
```
**Семпл #40:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/operativna-pamyat-g-skill-ddr5-32gb-2x16gb-6400mhz-trident-z5-neo-rgb-black-f5-6400j3239g16gx2-tz5nr-ID10Nx92.html",
  "title": "Оперативна памʼять G.Skill DDR5 32GB (2x16GB) 6400Mhz Trident Z5 Neo RGB Black (F5-6400J3239G16GX2-TZ5NR)"
}
```
**Семпл #41:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/prodam-pamyat-dlya-noutbukov-ddr4-16-8-4-2gb-ddr3-8-4gb-ddr2-2gb-ID10Qznq.html",
  "title": "Продам память для ноутбуков. DDR4-16-8-4-2GB/DDR3-8-4GB/DDR2-2GB."
}
```
**Семпл #42:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/operativna-pamyat-ddr4-16gb-hyperx-fury-black-2x8gb-ID1110ci.html",
  "title": "Оперативна память DDR4 16GB HyperX Fury Black 2x8GB"
}
```
**Семпл #43:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Оперативна Память Samsung 512MB 1Rx8 PC2-5300U-555-12-ZZ (Для ПК)"
}
```
**Семпл #44:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/operativna-pamyat-kingston-ddr3-2400-16-gb-4h4-gb-pc3-19200-cl-11-hyperx-predator-khx24c11t2k2-ID10PN3C.html",
  "title": "Оперативна память Kingston DDR3-2400 16 Гб (4х4 Гб), PC3-19200, CL 11, HyperX Predator (KHX24C11T2K2)"
}
```
**Семпл #45:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Оперативная память DDR3 32 GB !6+16 для сервера"
}
```
**Семпл #46:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/4-gb-operativna-pamyat-ddr3-noutbuchna-ID10jRPM.html",
  "title": "4 Гб оперативна память ddr3 ноутбучна"
}
```
**Семпл #47:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Материнська плата, процесор, блок живлення, память"
}
```
**Семпл #48:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Оперативна память Kingston DDR2 SDRAM (PC2-4200U) - 512 MB"
}
```
**Семпл #49:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Карта оперативной памяти"
}
```
**Семпл #50:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/dva-absolyutno-nov-modul-pamyat-crucial-ddr4-po-8-gb-ID110ZO6.html",
  "title": "Два абсолютно нові модулі памяті \"crucial\" ddr4 по 8 GB"
}
```
**Семпл #51:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/corsair-vengeance-lpx-ddr4-16gb-28gb-ID110ZMd.html",
  "title": "Corsair Vengeance LPX DDR4 16GB (2×8GB)"
}
```
**Семпл #52:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Kingston Fury Renegade NVMe M.2  на 1тб"
}
```
**Семпл #53:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/g-skill-trident-z5-rgb-ddr5-7200-32gb-2x16gb-cl34-ID10b8CF.html",
  "title": "G.SKILL Trident Z5 RGB DDR5 -7200 32GB (2x16GB) CL34"
}
```
**Семпл #54:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/nove-garantya-operativna-pamyat-ddr5-64gb-2x32gb-6000-cl30-g-skill-trident-z5-rgb-black-f5-6000j3040g32gx2-tz5rk-IDZOpsT.html",
  "title": "Нове/ГАРАНТІЯ | Оперативна память DDR5 64GB (2x32GB) 6000/CL30 G.SKILL Trident Z5 RGB Black (F5-6000J3040G32GX2-TZ5RK)"
}
```
**Семпл #55:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Samsung RAM 1GB 1Rx8 PC3-10600U-09-10-ZZZ"
}
```
**Семпл #56:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/operativnaya-pamyat-samsung-8gb-ddr5-4800-pc5-4800-IDZoSxx.html",
  "title": "Оперативная пам`ять Samsung 8GB DDR5 4800 PC5-4800"
}
```
**Семпл #57:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Оперативная память"
}
```
**Семпл #58:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Оперативна память 2GB DDR3L 1600MHz SODIMM SK Hynix для ноутбука"
}
```
**Семпл #59:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/ddr3-kingstone-4gb-2x2-dvokanal-IDYt1W6.html",
  "title": "ddr3 kingstone 4gb (2x2) двоканал"
}
```
**Семпл #60:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Оперативна память ddr3 дві по 4."
}
```
**Семпл #61:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/operativna-pamyat-dlya-pk-ddr3-4-8gb-1333-1600-IDZT6oM.html",
  "title": "Оперативна память для ПК DDR3 4-8Gb 1333-1600"
}
```
**Семпл #62:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Память DDR2 800 1 GB"
}
```
**Семпл #63:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/nova-g-skill-ripjaws-v-ddr4-32gb-2x16gb-3600mhz-cl18-22-22-42-1-35v-artikul-f4-3600c18d-32gvk-ID10Ps5v.html",
  "title": "Нова (G.SKILL Ripjaws V DDR4 32GB (2x16GB) 3600MHz CL18-22-22-42 1.35V (артикул F4-3600C18D-32GVK)"
}
```
**Семпл #64:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/crucial-ddr4-2666-sodimm-operativna-pamyat-dlya-noutbuka-8gb2x4gb-IDWbGdP.html",
  "title": "Crucial DDR4 - 2666 Sodimm оперативна памʼять для ноутбука 8gb(2x4gb)"
}
```
**Семпл #65:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/operativna-pamyat-ozu-ram-ddr4-samsung-kingston-sk-hynix-16gbx2-32gb-dlya-pk-ID10za2i.html",
  "title": "Оперативна памʼять ОЗУ RAM DDR4 Samsung, Kingston, SK Hynix 16Gbx2 (32gb) для ПК"
}
```
**Семпл #66:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Оперативна память ддр4 4гб пк"
}
```
**Семпл #67:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/novaoperativna-pamyat-netac-ddr4-32gb-216gb-3200mhz-cl16-ID10YASZ.html",
  "title": "Нова‼️Оперативна пам’ять Netac DDR4 32GB 2×16GB 3200MHz CL16"
}
```
**Семпл #68:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/operativna-pamyat-samsung-ddr4-8gb-3200mhz-ID110X7h.html",
  "title": "Оперативна память Samsung DDR4 8GB 3200MHz"
}
```
**Семпл #69:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/operativna-pamyat-dlya-noutbuka-so-dimm-ddr4-8-gb-3-200mhz-ID10spb5.html",
  "title": "Оперативна память для ноутбука so-dimm ddr4 8 gb 3.200mhz"
}
```
**Семпл #70:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/operativna-pamyat-kllisre-4gb-ddr3-1600mhz-2x4gb-IDXXMVb.html",
  "title": "Оперативна пам’ять Kllisre 4GB DDR3 1600MHz (2x4GB)"
}
```
**Семпл #71:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/operativnaya-pamyat-kingston-hyperx-fury-ddr4-16gb-3466mhz-ID10EkSi.html",
  "title": "Оперативная память Kingston HyperX Fury DDR4 16GB 3466MHz"
}
```
**Семпл #72:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/operativna-pamyat-ddr4-netac-3200-3600mgts-16gb-28-ID110VMD.html",
  "title": "Оперативна память DDR4  Netac 3200, 3600мгц 16гб (2*8)"
}
```
**Семпл #73:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/plashka-apirativno-pamyat-g-skill-aegismodel-f3-1333c9d-8gisobm-4-gbtip-ddr3-1333-pc3-10600taymngi-cl9napruga-1-5-v-ID10Pn79.html",
  "title": "Плашка апиративної памяті G.Skill Aegis\nМодель: F3-1333C9D-8GIS\nОбєм: 4 ГБ\nТип: DDR3-1333 (PC3-10600)\nТаймінги: CL9\nНапруга: 1.5 В"
}
```
**Семпл #74:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Оперативна память samsung"
}
```
**Семпл #75:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/grova-pamyat-g-skill-sniper-xmp-ddr3-2x4gb-1600mhz-pc3-1280-IDZwSf5.html",
  "title": "Ігрова память G.Skill Sniper XMP DDR3  2x4Gb 1600MHz PC3-1280"
}
```
**Семпл #76:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/operativnaya-pamyat-ddr3-mhz-1333-4gb-1plashkabu-v-gar-stan-za-1sht-IDVeypg.html",
  "title": "Оперативная память DDR3 MHZ 1333,4GB (1плашка)бу в гар стані, за 1шт"
}
```
**Семпл #77:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/operativna-pamyat-hynix-ddr4-16-gb-2rx4-pc4-2133p-ra0-10-hma42gr7mfr4n-tf-t1-ab-1514-ID110VwJ.html",
  "title": "Оперативна памʼять Hynix DDR4 16 GB 2RX4 PC4-2133P-RA0-10  HMA42GR7MFR4N-TF T1 AB 1514"
}
```
**Семпл #78:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "DDR4 Crucial Ballistix Black CL16 2x8G 3200mhzB"
}
```
**Семпл #79:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/operativna-pamyat-kingston-fury-ex-hyperx-beast-black-ddr5-2x16gb-kf552c36bbek2-32-ID10PDzA.html",
  "title": "Оперативна пам’ять Kingston FURY (ex. HyperX) Beast Black DDR5 2x16GB (KF552C36BBEK2-32)"
}
```
**Семпл #80:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/ssd-kingston-nv3-1tb-m-2-2280-nvme-pcie-4-0-x4-3d-nand-ID10ZHuF.html",
  "title": "SSD Kingston NV3 1TB M.2 2280 NVMe PCIe 4.0 x4 3D NAND"
}
```
**Семпл #81:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/ozp-g-skill-ddr4-3200mhz-trident-z-neo-16gb-2x8gb-abo-32gb-4x8gb-ID10EkgL.html",
  "title": "ОЗП G.Skill DDR4 3200Mhz Trident Z Neo 16GB 2x8GB або 32GB 4x8GB"
}
```
**Семпл #82:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/prodam-disk-ssd-m2-patriot-480gb-na-garant-1-5-roki-ID10InB4.html",
  "title": "продам диск ssd m2 patriot 480GB на гарантії 1.5 роки"
}
```
**Семпл #83:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Оригинал ОЗУ HyperX DDR3-1866 8192MB PC3-14900 Fury Black HX318C10FB/8"
}
```
**Семпл #84:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/operativno-pamyat-gtl-ddr4-8gb-udimm-dlya-domashnogo-kompyutera-ID110VeX.html",
  "title": "Оперативної памяті GTL DDR4 8Gb UDIMM для домашнього компютера"
}
```
**Семпл #85:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Память серверная регистровая Hynix 4Gb PC2-3200R DDR2-400 2Rx4 ECC буф"
}
```
**Семпл #86:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/operativna-pamyat-ddr4-16gb-hyperx-fury-black-2x8gb-ID105KUB.html",
  "title": "Оперативна память DDR4 16GB HyperX Fury Black 2x8GB"
}
```
**Семпл #87:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Модуль памяти Hynix HP 4GB PC3-10600"
}
```
**Семпл #88:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/operativna-pamyat-ddr4-4gb-samsung-so-dimm-dlya-noutbuka-3200mhz-ID10NpSJ.html",
  "title": "Оперативна память DDR4 4GB Samsung SO-DIMM для ноутбука (3200MHz)"
}
```
**Семпл #89:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Продам оперативную память Kingston 4/4 ddr3"
}
```
**Семпл #90:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Память DDR2 для компютера 2Гб PC2-6400U 800MHz Adata 2Gb ДДР2 800МГц"
}
```
**Семпл #91:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/kingston-fury-beast-ddr4-8gb-2666mhz-black-ID10ZhnK.html",
  "title": "Kingston FURY Beast DDR4 8GB 2666MHz Black"
}
```
**Семпл #92:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/operativna-pamyat-ddr4-3600-3200-3000-2133mhz-16-8gb-corsair-vengeance-hyperx-komplekti-ta-poshtuchno-ID10l3vS.html",
  "title": "Оперативна память DDR4- 3600/3200/3000/2133mhZ - 16/8gb Corsair Vengeance / HyperX (Комплекти та поштучно)"
}
```
**Семпл #93:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/crucial-ram-ddr5-pro-64-gb-2-x-32-gb-ID10Sd0o.html",
  "title": "Crucial RAM DDR5 Pro 64 gb (2 x 32 gb)"
}
```
**Семпл #94:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/operativna-pamyat-crucial-ballistix-tactical-ddr3-8gb-1600mhz-cl8-blt8g3d1608dt1tx0-ID10fpus.html",
  "title": "Оперативна память Crucial Ballistix Tactical DDR3 8GB 1600MHz CL8 (BLT8G3D1608DT1TX0)"
}
```
**Семпл #95:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/operativna-pamyat-4sht-8gb-ddr3-IDR4RyC.html",
  "title": "Оперативна пам’ять (4шт) 8gb ddr3"
}
```
**Семпл #96:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/novaoperativna-pamyat-netac-ddr4-32gb-216gb-3200mhz-cl16-ID10YASZ.html",
  "title": "Нова‼️Оперативна пам’ять Netac DDR4 32GB 2×16GB 3200MHz CL16"
}
```
**Семпл #97:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Оперативна пам\"ять ddr1234 пк комплекти на всі сокети Левада"
}
```
**Семпл #98:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/operativna-pamyat-ddr3-na-4-gb-IDYSUtP.html",
  "title": "Оперативна память DDR3 на 4 гб"
}
```
**Семпл #99:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "G. Skill Trident Z 3600mhz cl16-16-16-36 b-die"
}
```
**Семпл #100:**
```json
{
  "reason": "no_hardware_target_matched",
  "title": "Оперативна память DDR2 mushkin XP-2 8500 4x2Gb"
}
```

#### 📦 Комплекти — Відсіяно (0):

### 🎯 Успішно розпізнані моделі:
#### 🎮 Відеокарти (GPU) — Розпізнано (4):
**Зразок #1:**
```json
{
  "raw_title": "Відеокарта XFX RX 6600XT Quick 308 Black",
  "matched_target": "rx_6600_xt",
  "price_uah": 9000
}
```
**Зразок #2:**
```json
{
  "raw_title": "AORUS GeForce® GTX 1660 Ti 6G",
  "matched_target": "gtx_1660_ti",
  "price_uah": 7200
}
```
**Зразок #3:**
```json
{
  "raw_title": "Відеокарта MSI GeForce RTX5080 16GB INSPIRE 3X OC (RTX 5080 16G INSPIRE 3X OC) На Гарантії",
  "matched_target": "rtx_5080",
  "price_uah": 68000
}
```
**Зразок #4:**
```json
{
  "raw_title": "видеокарта Gigabyte GeForce GT 730",
  "matched_target": "gt_730",
  "price_uah": 1000
}
```

#### 🧠 Процесори (CPU) — Розпізнано (1):
**Зразок #1:**
```json
{
  "raw_title": "Процесор intel pentium g3220, картридер ST Lab, оперативна память 4 гб",
  "matched_target": "pentium_g3220",
  "price_uah": 200
}
```

#### 🔌 Материнські плати — Розпізнано (0):

#### ⚡ Блоки живлення — Розпізнано (1):
**Зразок #1:**
```json
{
  "raw_title": "Блок живлення Chieftec 700W",
  "matched_target": "700w",
  "price_uah": 1100
}
```

#### 💾 Накопичувачі — Розпізнано (1):
**Зразок #1:**
```json
{
  "raw_title": "M.2 SSD диск 256GB Samsung PM991 (PCIe 3.0 x4. NVMe). Trade-in",
  "matched_target": "ssd_256gb",
  "price_uah": 2500
}
```

#### 📟 Оперативна пам'ять — Розпізнано (3):
**Зразок #1:**
```json
{
  "raw_title": "Нова оперативна память Patriot DDR4 4GB 2666MHz (PSD44G266682) для ПК",
  "matched_target": "ram_ddr4_4gb",
  "price_uah": 599
}
```
**Зразок #2:**
```json
{
  "raw_title": "память DDR5 для ПК 64GB (2x32) 6000MHz PATRIOT Viper RGB. TradeIN",
  "matched_target": "ssd_64gb",
  "price_uah": 32500
}
```
**Зразок #3:**
```json
{
  "raw_title": "Оперативна память Kingston FURY Beast DDR5 32GB (2x16GB) 6000MHz CL40",
  "matched_target": "ram_ddr5_32gb",
  "price_uah": 15000
}
```

#### 📦 Комплекти — Розпізнано (0):

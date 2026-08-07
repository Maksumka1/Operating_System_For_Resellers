# 🐛 ДЕБАГ-ЗВІТ ПАРСИНГУ ГОТОВИХ ПК (OLX Category 78)
**Дата та час запуску:** 2026-08-07 22:23:35
**Тривалість виконання:** 340.17 сек
**Шлях до звіту:** `C:\Users\marke\OneDrive\Desktop\Operating_System\debug\debug_report_parse_pc.md`

## 📌 1. Задача та мета коду
Основна мета: асинхронний збір оголошень готових ПК та системних блоків з OLX GraphQL API.

## 📊 2. Загальна статистика вхідних даних та відсіювання
### ⚙️ Секція: Supabase_Input
- **Завантажено URLs для дедуплікації:** 52621

### ⚙️ Секція: OLX_GraphQL
- **Отримано сирих оголошень ПК:** 468

### ⚙️ Секція: Filtering_Rules
- **Відсіяно if (Дублікат URL в DB):** 446
- **Відсіяно if (Спрацював фільтр is_real_pc):** 11

### ⚙️ Секція: Parsing_Metrics
- **Успішно розпаршено ПК:** 11

### ⚙️ Секція: Summary
- **Знайдено нових ПК:** 11
- **Пропущено дублікатів:** 446
- **Немає нових лотів для відправки:** 2

### ⚙️ Секція: Supabase_Output
- **Успішно збережено в DB:** 11

### ⚙️ Секція: WebSocket
- **Успішно тригернуто живий стрім:** 4

## 🔄 3. Детальні приклади даних
### 🔹 Відсіяні оголошення (запчастини, окремі комплектуючі, дублікати) (Показано 100 з max 100):
**Семпл #1:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/nayavnst-new-asic-bitmain-antminer-t21-190-th-cv1835-miner-garantya-IDW5PJR.html",
  "title": "НАЯВНІСТЬ! NEW Asic Bitmain Antminer T21 190 Th CV1835 miner +Гарантія"
}
```
**Семпл #2:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/kompyuter-pk-server-dell-optiplex-3060-i5-8500t-16gb-ID10ZbRV.html",
  "title": "Компʼютер ПК Сервер Dell OptiPlex 3060 i5-8500T/16GB"
}
```
**Семпл #3:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/srochno-suchasniy-mn-groviy-pk-ID10IVEr.html",
  "title": "!СРОЧНО! Сучасний Міні Ігровий ПК |"
}
```
**Семпл #4:**
```json
{
  "reason": "banned_word_without_pc_indicator: видеокарта",
  "title": "Сборка ASUS M4A77TD, AMD Phenom II, Crucial DDR3 4GB, видеокарта asus"
}
```
**Семпл #5:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/serverniy-pk-dual-xeon-e5-2697-v4-rtx-3060-128gb-ecc-ID10V4SX.html",
  "title": "Серверний ПК Dual Xeon E5-2697 v4 | RTX 3060 | 128GB ECC"
}
```
**Семпл #6:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/prodam-pk-ryzen-5-1600-16gb-gtx-1050-ti-b450m-IDZZZtA.html",
  "title": "Продам ПК Ryzen 5 1600 / 16GB / GTX 1050 Ti / B450M"
}
```
**Семпл #7:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/byudzhetniy-groviy-pk-ID10Ogj9.html",
  "title": "Бюджетний ігровий пк"
}
```
**Семпл #8:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/prodam-pk-na-baze-protsessora-intel-i5-2300-ID1111Kh.html",
  "title": "Продам ПК на базе процессора Intel i5-2300"
}
```
**Семпл #9:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/prodam-personalniy-kompyuter-IDWZ9fW.html",
  "title": "Продам персональний комп'ютер"
}
```
**Семпл #10:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/odnoplatnyy-kompyuter-raspberry-pi-4-model-b-komplekt-s-kabelyami-ID10PqCB.html",
  "title": "Одноплатный компьютер Raspberry Pi 4 Model B. Комплект с кабелями"
}
```
**Семпл #11:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/kompyutery-pk-acer-veriton-x2611-2610-g-s1150-optom-s-garantiey-deshevo-IDCiscD.html",
  "title": "Компьютеры ПК Acer veriton X2611 2610 G s1150 оптом с гарантией дешево"
}
```
**Семпл #12:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/pk-sistemn-bloki-fujitsu-esprimo-q920-mini-i5-4570t-8gb-128ssd-gurt-IDXQhBu.html",
  "title": "ПК системні блоки Fujitsu Esprimo Q920 Mini i5-4570t/8GB/128SSD Гурт"
}
```
**Семпл #13:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/antminer-asic-s19-82-th-novb-garantya-ask-mayner-na-btc-xilinx-ID103DjF.html",
  "title": "ANTMINER Asic S19 82 Th, новіб, Гарантія, асік, майнер, на BTC, Xilinx"
}
```
**Семпл #14:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/kompyuter-amd-ryzen-5-3600-gtx-1050-ti-32gb-ID10VtTH.html",
  "title": "Компьютер AMD Ryzen 5 3600 / GTX 1050 Ti / 32GB"
}
```
**Семпл #15:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/sistemniy-blok-radeon-x470-ID10ZwpC.html",
  "title": "Системний блок Radeon X470"
}
```
**Семпл #16:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/sterodniy-malyuk-ryzen-9-9950x3d-rtx-5080-16gb-ddr5-64gb-m-2-ssd-2tb-robocha-stantsya-groviy-kompyuter-igrovoy-pk-rabochaya-stantsiya-ID10DhHt.html",
  "title": "Стероїдний Малюк! Ryzen 9 9950X3D+RTX 5080 16GB+DDR5 64GB+M.2 SSD 2TB –  Робоча станція ігровий комп'ютер игровой ПК рабочая станция"
}
```
**Семпл #17:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/hp-pavilion-wave-desktop-pc-IDJ0NnL.html",
  "title": "hp pavilion Wave Desktop PC"
}
```
**Семпл #18:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/kompyutery-pk-lenovo-thinkcentre-m71-m72e-sff-i5-8gb-120ssd-opt-b-n-IDSFIP7.html",
  "title": "Компьютеры ПК Lenovo ThinkCentre M71 M72е SFF i5/8ГБ/120SSD ОПТ!Б/Н"
}
```
**Семпл #19:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/kompyuteri-pk-hp-prodesk-600-g3-sff-i3-7100-8-120-ssd-s1151-gurt-b-g-IDTCTCm.html",
  "title": "Комп'ютери ПК HP ProDesk 600 G3 SFF i3 7100/8/120 SSD s1151 ГУРТ!Б/Г‼️"
}
```
**Семпл #20:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/prodam-kompyuter-ID1111E6.html",
  "title": "Продам комп'ютер"
}
```
**Семпл #21:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/potuzhniy-groviy-pk-dlya-navchannya-ta-rozvag-ID10gQLO.html",
  "title": "Потужний ігровий ПК для навчання та розваг"
}
```
**Семпл #22:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/suchasniy-komp-yuter-sistemniy-blok-ID10ssO3.html",
  "title": "Сучасний комп\"ютер/системний блок."
}
```
**Семпл #23:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/personalnyy-kompyuter-pk-pc-ID10C4uj.html",
  "title": "Персональный компьютер. ПК. PC"
}
```
**Семпл #24:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/robocha-stantsya-hp-z800-IDZ70VQ.html",
  "title": "Робоча станція HP Z800"
}
```
**Семпл #25:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/groviy-robochiy-pk-xeon-e5-2660-gtx-1660-6gb-16gb-ram-x79-ID1111w3.html",
  "title": "Ігровий / робочий ПК Xeon E5-2660 / GTX 1660 6GB / 16GB RAM / X79"
}
```
**Семпл #26:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/mayneri-new-asic-antminer-l9-16-gh-v-nayavnost-xilinx-garantya-IDZyMdZ.html",
  "title": "Майнери NEW Asic Antminer L9 16 Gh в наявності, Xilinx, Гарантія"
}
```
**Семпл #27:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/monoblok-asus-all-in-one-a6421-fullhd-ips-21-5-intel-4gb-ddr4-500gb-hdd-ID10qjGP.html",
  "title": "Моноблок Asus All in one A6421 (FullHD, IPS, 21,5\") Intel / 4gb DDR4 / 500gb HDD"
}
```
**Семпл #28:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/prodam-igrovoy-kompyuter-ID10TJ4r.html",
  "title": "Продам игровой компьютер"
}
```
**Семпл #29:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/gtx1660s-kompyuter-IDZ1GzT.html",
  "title": "gtx1660s компʼютер"
}
```
**Семпл #30:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/horosho-yakost-noutbuk-acer-aspire-5349-ekran-15-6-dyuymv-protsesori-dvoyadern-intel-celeron-1-5ghz-operativna-pamyat-ddr3-ma-obm-8gb-wi-fi-hdmi-ID1111uq.html",
  "title": "Хорошої якості ноутбук Acer Aspire 5349/Екран 15.6 дюймів /Процесори двоядерні Intel Celeron  1.5GHz/Оперативна пам'ять DDR3 має об'єм 8GB/Wi-Fi,HDMI"
}
```
**Семпл #31:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/prodam-sistemniy-blok-pentium-dyal-core-e6500-3666-mhz-IDVWS1w.html",
  "title": "Продам системний блок. Pentium Dyal Core E6500 3666 MHz."
}
```
**Семпл #32:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/rx-570-xeon-e3-1270-v3-core-i7-4770-monitor-v-podarok-ID1111tn.html",
  "title": "RX 570 + Xeon E3-1270 v3 (Core i7-4770) монитор в подарок"
}
```
**Семпл #33:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/buntar-i7-14700kf-rtx-4080-super-16gb-ddr5-32gb-m-2-ssd-1tb-robocha-stantsya-groviy-kompyuter-igrovoy-pk-rabochaya-stantsiya-ID10EqBr.html",
  "title": "БУНТАР! i7-14700KF+RTX 4080 Super 16GB+DDR5 32GB+M.2 SSD 1TB –  Робоча станція ігровий комп'ютер игровой ПК рабочая станция"
}
```
**Семпл #34:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/mnpk-acer-veriton-n4660g-core-i3-i5-i7-8-9-pokolnnya-wi-fi-gurt-fop-IDZlh4y.html",
  "title": "МініПК Acer Veriton N4660G Core i3 i5 i7 8-9 покоління Wi-Fi Гурт ФОП"
}
```
**Семпл #35:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/kompyuter-nvidia-gtx-770-intel-core-i5-IDX9II5.html",
  "title": "Компьютер Nvidia gtx 770, Intel core i5"
}
```
**Семпл #36:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/kompyuter-apple-macpro-5-1-6-core-intel-xeon-os-high-sierra-IDSoOJz.html",
  "title": "Компьютер Apple MacPro 5.1 (6-Core Intel Xeon ) OS High Sierra"
}
```
**Семпл #37:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/mnpk-fujitsu-esprimo-q958-mini-i3-i5-9500t-8-16gb-ssd128-256-512gb-ID10i6ty.html",
  "title": "МініПК Fujitsu Esprimo Q958 Mini i3 i5-9500T 8-16GB SSD128-256-512GB"
}
```
**Семпл #38:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/macmini-m4-garantya-stantsya-ID1111ri.html",
  "title": "MacMini M4 + Гарантія + Станція"
}
```
**Семпл #39:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/prodam-pk-v-sbore-deepcool-8-16-32ram-ssd-rx480-8gb-ID10ZAgw.html",
  "title": "Продам ПК в сборе Deepcool 8/16-32ram-ssd-rx480 8gb"
}
```
**Семпл #40:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/1230-mayner-bitmain-antminer-s19xp-279t-hydro-supertsna-garantya-IDXXwas.html",
  "title": "1230$! Майнер BITMAIN ANTMINER S19XP+ 279T HYDRO (Суперціна+Гарантія"
}
```
**Семпл #41:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/sistemniy-blok-pk-lenovo-v520s-sff-s1151-i3-7100-8gb-ssd128-gb-gurt-IDYf8t8.html",
  "title": "Системний блок ПК Lenovo V520S SFF s1151 i3-7100/8GB/SSD128 GB Гурт"
}
```
**Семпл #42:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/hp-640-intel-xeon-e5-2670-v3-turbo-boost-ddr-4-16-gb-quadro-k2200-IDNyVfq.html",
  "title": "HP 640 Intel Xeon E5 -2670  V3 Turbo Boost  DDR 4 16 gb Quadro K2200"
}
```
**Семпл #43:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/sistemniy-blok-hp-i3-6100-8-ram-120-ssd-IDZFFtv.html",
  "title": "Системний блок Hp i3-6100/8 ram/120 ssd"
}
```
**Семпл #44:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/sistemn-bloki-pk-mat-plata-gigabyte-asus-protsesora-cpu-ryzen-ID1036b9.html",
  "title": "Системні блоки - ПК - Мат. плата Gigabyte Asus - Процесора CPU Ryzen"
}
```
**Семпл #45:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/vazhlivo-shanovn-ID1111lY.html",
  "title": "Важливо шановні!"
}
```
**Семпл #46:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/kompyuter-evolve-pk-rtx-4070-12gb-i5-13500-32gb-ddr5-1tb-ssd-ID1111lR.html",
  "title": "Комп'ютер EVOLVE ПК \\ RTX 4070 12GB \\ i5-13500 \\ 32GB DDR5 \\ 1TB SSD"
}
```
**Семпл #47:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/prodayu-komplekt-do-pk-IDZQBfX.html",
  "title": "Продаю комплект до пк"
}
```
**Семпл #48:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/monobloki-dell-v-ofs-doma-kompyuter-i3-i5-i7-ssd-256-480-m2-optom-IDUkHBM.html",
  "title": "Моноблоки Dell в Офіс дома Комп'ютер i3, i5, i7, SSD 256, 480 M2 ОПТОМ"
}
```
**Семпл #49:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/prodam-pk-IDTHOCA.html",
  "title": "Продам пк"
}
```
**Семпл #50:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/groviy-kopyuter-ID10gQli.html",
  "title": "Ігровий Коп'ютер"
}
```
**Семпл #51:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/titan-ryzen-9-7950x-rtx-3090-24gb-ddr5-64gb-m-2-ssd-1tb-robocha-stantsya-groviy-kompyuter-igrovoy-pk-rabochaya-stantsiya-ID10Eqg8.html",
  "title": "ТИТАН! Ryzen 9 7950X+RTX 3090 24GB+DDR5 64GB+M.2 SSD 1TB –  Робоча станція ігровий комп'ютер игровой ПК рабочая станция"
}
```
**Семпл #52:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/sistemniy-blok-pk-lenovo-v520s-sff-s1151-i3-7100-8gb-ssd128-gb-gurt-IDYf8t8.html",
  "title": "Системний блок ПК Lenovo V520S SFF s1151 i3-7100/8GB/SSD128 GB Гурт"
}
```
**Семпл #53:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/raspberry-pi-touch-display-2-IDYor3j.html",
  "title": "Raspberry Pi Touch Display 2"
}
```
**Семпл #54:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/prodam-pk-dlya-shkoli-ta-domu-v-povnomu-nabor-IDZ6MbQ.html",
  "title": "Продам ПК для школи та дому в повному наборі"
}
```
**Семпл #55:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/kompyuter-intel-core-i3-8100-8gb-ssd-240gb-hdd-1tb-montor-lg-ID10PQFX.html",
  "title": "Комп'ютер Intel Core i3-8100 / 8GB / SSD 240GB + HDD 1TB / Монітор LG"
}
```
**Семпл #56:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/apple-mac-studio-m2-max-12-30-yader-32-gb-512-ssd-povniy-komplekt-ID10YpFp.html",
  "title": "Apple Mac Studio M2 Max 12/30 ядер · 32 ГБ · 512 SSD · повний комплект"
}
```
**Семпл #57:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/mn-pk-wintel-box-w8-pro-4-64-gb-windows-10-ID1111al.html",
  "title": "Міні-ПК Wintel Box W8 Pro 4/64 ГБ (Windows 10)"
}
```
**Семпл #58:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/prodam-sistemnyy-blok-na-s-am3-s-novym-ssd-diskom-IDZXFVH.html",
  "title": "Продам системный блок на S AM3, с новым ссд диском."
}
```
**Семпл #59:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/igrovoy-kompyuter-IDWDjh2.html",
  "title": "Игровой компьютер"
}
```
**Семпл #60:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/igrovoy-pk-i7-10700f-rx5700xt-ID10U428.html",
  "title": "Игровой Пк  I7-10700f/Rx5700Xt"
}
```
**Семпл #61:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/mac-mini-2018-i7-64gb-1tb-ID10r4ao.html",
  "title": "Mac Mini 2018 i7 / 64GB / 1TB"
}
```
**Семпл #62:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/prodam-kompyuter-ID11117J.html",
  "title": "Продам комп'ютер"
}
```
**Семпл #63:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/dzherelo-bezperebynogo-zhivlennya-luxeon-1500zd-ID10OhUG.html",
  "title": "Джерело безперебійного живлення Luxeon 1500zd"
}
```
**Семпл #64:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/prodam-komp-yutern-aktivn-kolonki-ID10qjuY.html",
  "title": "Продам комп\"ютерні активні колонки"
}
```
**Семпл #65:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/igrovoy-pk-dlya-ks-rast-doty-maynkrafta-ID10ZRaM.html",
  "title": "Игровой пк для кс/раст/доты/майнкрафта"
}
```
**Семпл #66:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/groviy-pk-ryzen-5-7500f-rtx-5070-12gb-ddr5-am5-ID110ZTv.html",
  "title": "Ігровий ПК Ryzen 5 7500F RTX 5070 12GB DDR5 AM5"
}
```
**Семпл #67:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/prodayu-pk-garniy-setap-ID1106Jm.html",
  "title": "Продаю ПК , гарний сетап"
}
```
**Семпл #68:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/prodam-sistemniy-blok-montor-22-i5-4670k-gtx-1050-ti-4gb-ID10O9xa.html",
  "title": "Продам системний блок + Монітор 22\" (i5-4670K / GTX 1050 Ti 4GB)"
}
```
**Семпл #69:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/bliskavka-rx-5700-12-yader-32gb-ram-ssd-120gb-groviy-kompyuter-pk-dlya-gor-geymerskiy-igrovoy-kompyuter-ID10DgYE.html",
  "title": "Блискавка! RX 5700+12 ядер+32GB RAM+SSD 120GB –  Ігровий комп'ютер ПК для ігор геймерський игровой компьютер"
}
```
**Семпл #70:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/groviy-pk-rtx-4070-12gb-i5-11400f-32gb-ram-1-5tb-ssd-ID10DfsU.html",
  "title": "Ігровий ПК RTX 4070 12GB / i5-11400F / 32GB RAM / 1.5TB SSD"
}
```
**Семпл #71:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/robochiy-sistemniy-blok-pk-na-intel-core-duo-e8400-4gb-ram-250gb-IDZCuNb.html",
  "title": "Робочий системний блок ПК на Intel Core Duo E8400, 4Gb Ram, 250Gb"
}
```
**Семпл #72:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/moschnyy-mini-pk-na-i7-8700-IDZhUzD.html",
  "title": "Мощный мини ПК на i7 8700"
}
```
**Семпл #73:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/kompyuter-komplekt-IDWZ8ms.html",
  "title": "Компютер комплект"
}
```
**Семпл #74:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/prodam-kompyuter-monitor-ID10Zvec.html",
  "title": "Продам компьютер + монитор"
}
```
**Семпл #75:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/pk-lenovo-think-centre-m92p-ta-m82opt-ID10jPv7.html",
  "title": "ПК Lenovo Think Centre M92p та М82(опт)"
}
```
**Семпл #76:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/kompyuter-pk-hp-elitedesk-705-g4-sff-ryzen-3-2200g-8gb-ddr4-ssd-256gb-IDZ4a2M.html",
  "title": "Комп'ютер ПК HP EliteDesk 705 G4 SFF Ryzen 3 2200G 8Gb DDR4 SSD 256Gb"
}
```
**Семпл #77:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/kompyuter-dell-optiplex-3020-sff-i3-4130-8gb-ddr3-128gb-ssd-garantya-IDYVhyz.html",
  "title": "Комп'ютер Dell Optiplex 3020 SFF i3-4130 8Gb DDR3 128Gb SSD Гарантія"
}
```
**Семпл #78:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/noviy-suchasniy-groviy-pk-sistemnyy-blok-igrovoy-kompyuter-IDZyNWE.html",
  "title": "• Новий! Сучасний! Ігровий ПК! Системный блок ! Игровой компьютер!"
}
```
**Семпл #79:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/kompyuteri-dell-3050-3090-7050-mini-sistemn-bloki-optom-sklad-IDYS9kv.html",
  "title": "‼️Комп’ютери Dell 3050|3090|7050 Mini | системні блоки оптом |СКЛАД"
}
```
**Семпл #80:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/potuzhniy-groviy-pk-i7-13700k-rtx-3070-ti-ddr5-32-gb-ID10UQfZ.html",
  "title": "Потужний ігровий ПК i7-13700K / RTX 3070 Ti / DDR5 32 ГБ"
}
```
**Семпл #81:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/groviy-pk-kompyuter-i5-12400f-rtx-3070-32gb-ddr4-512gb-nvme-IDYS67J.html",
  "title": "Ігровий ПК комп'ютер i5-12400f RTX 3070 32Gb DDR4 512Gb NVMe"
}
```
**Семпл #82:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/kompyuter-dell-optiplex-3040-sff-i5-6400-8gb-ssd-120gb-garantya-12-ms-IDVyVUK.html",
  "title": "Комп'ютер Dell Optiplex 3040 SFF i5-6400 8Gb SSD 120Gb Гарантія 12 міс"
}
```
**Семпл #83:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/pk-z-rx-580-8-gb-ID1110VO.html",
  "title": "Пк з  Rx 580 8 gb"
}
```
**Семпл #84:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/groviy-personalniy-kompyuter-ID10EpSI.html",
  "title": "Ігровий персональний комп'ютер"
}
```
**Семпл #85:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/kompyuter-acer-aspire-tc-100-z-montorom-samsung-ID10EpPQ.html",
  "title": "Комп'ютер Acer Aspire TC-100 з монітором SAMSUNG"
}
```
**Семпл #86:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/mn-pk-nuc7i3bhn-i3-7100u-mn-kompyuter-intel-nuc-IDYfzTx.html",
  "title": "Міні ПК NUC7i3BHN, i3-7100U Міні-комп'ютер Intel NUC"
}
```
**Семпл #87:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/pk-ryzen-5-5500-rtx-4060-ID1110RW.html",
  "title": "ПК Ryzen 5 5500 / RTX 4060"
}
```
**Семпл #88:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/pk-ryzen-5-7500f-rtx-4060-32gb-1tb-ID10Pvm3.html",
  "title": "ПК  Ryzen 5 7500F / RTX 4060 / 32GB / 1TB"
}
```
**Семпл #89:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/prodayu-potuzhniy-pk-z-garantyu-ID10cA6F.html",
  "title": "Продаю потужний ПК з гарантією"
}
```
**Семпл #90:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/prodam-sistemniy-blok-bez-vdeokarti-IDWleal.html",
  "title": "Продам системний блок без відеокарти"
}
```
**Семпл #91:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/nayavnst-b-v-mayneri-asic-bitmain-antminer-s19-90-th-3150vt-garantya-IDX1f3s.html",
  "title": "Наявність!Б/в Майнери Asic Bitmain Antminer S19 90 Th 3150Вт +Гарантія"
}
```
**Семпл #92:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/2025r-monoblok-lenovo-ideacentre-3-27irh9-i5-13420h-16gb-512gb-fhd-27-ID10mhvZ.html",
  "title": "2025р. Моноблок Lenovo IdeaCentre 3 27IRH9/i5-13420H/16GB/512GB/FHD/27"
}
```
**Семпл #93:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/igrovoy-pk-rtx5060-ozu-32gb-ryzen-5-5600x-1tb-ssdna-garantii-novyy-ID10Z8Ww.html",
  "title": "Игровой ПК RTX5060 ОЗУ 32гб Ryzen 5 5600x 1TB SSDна гарантии новый"
}
```
**Семпл #94:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/sistemnyy-blok-kompyuter-IDR88ZW.html",
  "title": "Системный блок компьютер"
}
```
**Семпл #95:**
```json
{
  "reason": "starts_with_banned_word: відеокарта",
  "title": "Відеокарта Apple iMac 27\" ATI Radeon HD 6970M 2GB MXM 109-C29657-10"
}
```
**Семпл #96:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/prodam-pk-montor-klavatura-mishka-IDY4xHi.html",
  "title": "Продам (ПК, Монітор, клавіатура, мишка)"
}
```
**Семпл #97:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/pk-i5-9400f-rtx-2060rtx-2060-ventus-xs-6g-oc16gb-ddr4-2666mhz-ID10gPLe.html",
  "title": "Пк i5-9400F rtx 2060\nRtx 2060 Ventus xs 6g oc\n16gb ddr4 2666mhz"
}
```
**Семпл #98:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/pk-gtx-1660-super-intel-i5-11400f-ID1110Jz.html",
  "title": "ПК GTX 1660 Super,intel-i5 11400F"
}
```
**Семпл #99:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/stil-rtx-4080-super-16gb-ryzen-7-7800x3d-ddr5-32gb-m-2-ssd-1tb-groviy-kompyuter-pk-dlya-gor-geymerskiy-igrovoy-kompyuter-ID10DgAc.html",
  "title": "СТИЛЬ! RTX 4080 Super 16GB+Ryzen 7 7800X3D+DDR5 32GB+M.2 SSD 1TB –  Ігровий комп'ютер ПК для ігор геймерський игровой компьютер"
}
```
**Семпл #100:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/sistemniy-blok-asus-artline-gaming-IDZfvxQ.html",
  "title": "Системний блок Asus ARTLINE Gaming"
}
```

### 🔹 Валідовані оголошення ПК (пройшли перевірку is_real_pc) (Показано 11 з max 100):
**Семпл #1:**
```json
{
  "ad_id": 925770117,
  "title": "Игровой ПК новый",
  "status": "passed_is_real_pc"
}
```
**Семпл #2:**
```json
{
  "ad_id": 931007469,
  "title": "iMac 21.5 4K Retina (ТОП: i5 3.4GHz / 16GB / Radeon 560 4GB)",
  "status": "passed_is_real_pc"
}
```
**Семпл #3:**
```json
{
  "ad_id": 929735907,
  "title": "ігровий ПК Steam Deck від компанії Valve512 гб",
  "status": "passed_is_real_pc"
}
```
**Семпл #4:**
```json
{
  "ad_id": 924740873,
  "title": "ІГРОВИЙ ПК ElitePC Sensei! Ryzen 9800X3D / RTX 5080 16Gb / DDR5 64Gb 6000 CL30 / 11000MB/s Pcie 5.0 1Tb / MSI PRO X870E WIFI7",
  "status": "passed_is_real_pc"
}
```
**Семпл #5:**
```json
{
  "ad_id": 909300866,
  "title": "Продам компютер / системний блок / монітор ПК / ASUS / Phillips / intel/ Windows",
  "status": "passed_is_real_pc"
}
```
**Семпл #6:**
```json
{
  "ad_id": 920172180,
  "title": "Акція! Fujitsu Esprimo P957 E94+ Intel i5-6500 8GB/  ( DDR4 m2 NVME)— Компактний і швидкий",
  "status": "passed_is_real_pc"
}
```
**Семпл #7:**
```json
{
  "ad_id": 930912965,
  "title": "Ігровий ПК GTX 1660 Super i3-8100 cmp30hx",
  "status": "passed_is_real_pc"
}
```
**Семпл #8:**
```json
{
  "ad_id": 927243221,
  "title": "Компьютер ASGARD Ryzen 5 9600X, 32ГБ DDR5, GeForce RTX 5060, 1TB SSD на водянке",
  "status": "passed_is_real_pc"
}
```
**Семпл #9:**
```json
{
  "ad_id": 839258249,
  "title": "Персональний компютер",
  "status": "passed_is_real_pc"
}
```
**Семпл #10:**
```json
{
  "ad_id": 780620407,
  "title": "Компьютер Системный блок",
  "status": "passed_is_real_pc"
}
```
**Семпл #11:**
```json
{
  "ad_id": 924323068,
  "title": "Компютер i5 9400f ,gtx 1650",
  "status": "passed_is_real_pc"
}
```

============================================================

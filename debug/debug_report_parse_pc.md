# 🐛 ДЕБАГ-ЗВІТ ПАРСИНГУ ГОТОВИХ ПК (OLX Category 78)
**Дата та час запуску:** 2026-08-07 00:16:05
**Тривалість виконання:** 489.23 сек
**Шлях до звіту:** `C:\Users\marke\OneDrive\Desktop\Operating_System\debug\debug_report_parse_pc.md`

## 📌 1. Задача та мета коду
Основна мета: асинхронний збір оголошень готових ПК та системних блоків з OLX GraphQL API.

## 📊 2. Загальна статистика вхідних даних та відсіювання
### ⚙️ Секція: Supabase_Input
- **Завантажено URLs для дедуплікації:** 52197

### ⚙️ Секція: OLX_GraphQL
- **Отримано сирих оголошень ПК:** 520

### ⚙️ Секція: Parsing_Metrics
- **Успішно розпаршено ПК:** 121

### ⚙️ Секція: Filtering_Rules
- **Відсіяно if (Дублікат URL в DB):** 387
- **Відсіяно if (Спрацював фільтр is_real_pc):** 12

### ⚙️ Секція: Summary
- **Знайдено нових ПК:** 121
- **Пропущено дублікатів:** 387
- **Немає нових лотів для відправки:** 4

### ⚙️ Секція: Supabase_Output
- **Успішно збережено в DB:** 121

### ⚙️ Секція: WebSocket
- **Успішно тригернуто живий стрім:** 3

## 🔄 3. Детальні приклади даних
### 🔹 Відсіяні оголошення (запчастини, окремі комплектуючі, дублікати) (Показано 100 з max 100):
**Семпл #1:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/kompyuter-fx4100-rx5604gb-ID10c1LF.html",
  "title": "Компютер Fx4100/rx560(4GB)"
}
```
**Семпл #2:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/l7-9050-gh-s-asic-bitmain-doge-ltc-antminer-ID10gSTJ.html",
  "title": "L7- 9050 gh/s Asic, Bitmain, DOGE, LTC, Antminer"
}
```
**Семпл #3:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/pk-korpus-ta-komplektuyuch-vdeokarti-tsp-bloki-zhivlennya-ssd-ddr2-ddr3-ID10AQEP.html",
  "title": "ПК корпус та комплектуючі, відеокарти, цп, блоки живлення, ssd, ddr2 ddr3"
}
```
**Семпл #4:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/kompyuteri-fujitsu-sff-s1151-55-sistemn-bloki-i3-i5-i7-pk-ssd120-250-IDRHxnN.html",
  "title": "Комп'ютери Fujitsu SFF s1151/55 Системні блоки i3/i5/i7 ПК SSD120/250"
}
```
**Семпл #5:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/mayner-s19-bitmain-asik-antminer-s19j-pro-120t-garantya-b-v-430-ID10kCRS.html",
  "title": "Майнер S19! Bitmain asik antminer S19j pro+ 120T + Гарантія (Б/В 430$)"
}
```
**Семпл #6:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/new-asic-antminer-s21-hydro-335-th-miner-mayner-bitmain-servs-IDXp9RC.html",
  "title": "NEW Asic Antminer S21 Hydro 335 Th miner Майнер Bitmain + Сервіс"
}
```
**Семпл #7:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/mini-kompyutery-dell-kompyuter-nettop-sistemnye-bloki-optom-skladpk-IDWcMnM.html",
  "title": "Мини Компьютеры Dell компьютер неттоп системные блоки оптом складпк"
}
```
**Семпл #8:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/igrovoy-kompyuter-pk-gtx-1070-8-gb-ID10eHjc.html",
  "title": "Игровой компьютер, ПК, GTX 1070 8 ГБ"
}
```
**Семпл #9:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/moshnyy-igrovoy-pk-pc-i5-10400f-16ram-ssd-hdd-ID10I5ne.html",
  "title": "Мошный игровой пк/PC/i5 10400f /16RAM/SSD+HDD!"
}
```
**Семпл #10:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/igrovoy-pk-kompyuter-rx470-videokarta-garantiya-ID10xZ1r.html",
  "title": "Игровой ПК, компьютер,  RX470 видеокарта Гарантия"
}
```
**Семпл #11:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/kompyuter-pk-komplekti-sistemniy-blok-protsesori-opt-beznal-usdt-IDYFdNB.html",
  "title": "Компʼютер ПК Комплекти, Системний блок, Процесори  Опт, БЕЗНАЛ, USDT"
}
```
**Семпл #12:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/kompyuter-dell-7050-micro-i5-75003-9ghz-4yadra-8gb-ssd256gb-nvme-wi-fi-IDPHXbA.html",
  "title": "Комп’ютер Dell  7050 micro i5-7500(3.9GHz) (4ядра),8гб, SSD256GB nvme, WI-FI"
}
```
**Семпл #13:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/groviy-pk-rx-5700-xt-kompyuter-ram-16gb-sistemnik-i5-7500-ssd-hdd-1tb-ID101RtK.html",
  "title": "Ігровий ПК RX 5700 XT Комп'ютер RAM 16GB Системник i5-7500 ssd+hdd 1TB"
}
```
**Семпл #14:**
```json
{
  "reason": "banned_word_without_pc_indicator: ram",
  "title": "LLMки в шоці! RTX 3090 24GB+24 ядра+128GB RAM+M.2 SSD 1TB –"
}
```
**Семпл #15:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/kompyuter-ryzen-3600-16gb-1070-ID10Z1PG.html",
  "title": "Комп'ютер Ryzen 3600/16gb/1070"
}
```
**Семпл #16:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/kompyuteri-dell-optiplex-7010-sff-pk-i5-8gb-ssd128gb-opt-IDSQAaP.html",
  "title": "Комп’ютери Dell Optiplex 7010 SFF ПК i5, 8GB SSD128GB ОПТ"
}
```
**Семпл #17:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/groviy-kompyuter-z-grovim-montorom-ID10p93t.html",
  "title": "Ігровий компютер з ігровим монітором"
}
```
**Семпл #18:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/groviy-kompyuter-ID110GEJ.html",
  "title": "ігровий компютер"
}
```
**Семпл #19:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/groviy-pk-12-yaderxeon-2640v3-16gb-rx-570-4gb-ssd-m2-128-hdd-500-IDYUSSJ.html",
  "title": "Ігровий ПК 12 ядер:Xeon 2640v3/16Gb/RX 570 4gb/SSD M2 128+HDD 500"
}
```
**Семпл #20:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/pk-po-komplektuyuchim-r5-7500f-3060-ti-ddr5-ID110GCt.html",
  "title": "Пк по комплектуючим R5 7500F 3060 ti ддр5"
}
```
**Семпл #21:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/fantastiks-24-yadra-gtx-1070-16gb-ram-ssd-120gb-robocha-stantsya-groviy-kompyuter-igrovoy-pk-rabochaya-stantsiya-ID10E10W.html",
  "title": "ФАНТАСТИКС! 24 ядра+GTX 1070+16GB RAM+SSD 120GB –  Робоча станція ігровий комп'ютер игровой ПК рабочая станция"
}
```
**Семпл #22:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/imac-g3-aplle-retro-ID10Paeu.html",
  "title": "Imac G3 Aplle ретро"
}
```
**Семпл #23:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/personalniy-kompyuter-IDUJ87O.html",
  "title": "Персональний комп'ютер"
}
```
**Семпл #24:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/monoblok-apple-imac-a2438-24-retina-4-5k-256-8-apple-m1-dealniy-ID1032pV.html",
  "title": "Моноблок Apple iMac A2438/24\"/Retina/4.5K/256/8/Apple M1/ІДЕАЛЬНИЙ"
}
```
**Семпл #25:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/kompyuter-sistemniy-blok-komplekt-pk-kompyuter-beznal-usdt-IDXRraY.html",
  "title": "Компʼютер. Системний блок, Комплект ПК  Компютер БЕЗНАЛ/ USDT"
}
```
**Семпл #26:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/sistemniy-blok-ultra-5-245kf-rtx-5070-ti-16gb-ssd-nvme-1tb-32gb-ddr5-6400mhz-garantya-12ms-ID10BD6D.html",
  "title": "Системний блок / Ultra 5 245KF / RTX 5070 Ti 16gb / SSD NVMe 1tb / 32gb - DDR5 6400Mhz / ГАРАНТІЯ 12міс"
}
```
**Семпл #27:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/prodam-monoblok-archos-vision-215-ID110Gpn.html",
  "title": "Продам моноблок ARCHOS Vision 215"
}
```
**Семпл #28:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/kompyuter-povniy-komplekt-pk-montor-klavatura-mishka-ID10g4LF.html",
  "title": "Комп’ютер повний комплект: ПК + монітор + клавіатура + мишка"
}
```
**Семпл #29:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/komplekt-kompyuter-ID10rbej.html",
  "title": "Комплект, компьютер"
}
```
**Семпл #30:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/kompyuter-hp-600b-series-sistemniy-blok-ID10gw0N.html",
  "title": "Комп'ютер HP 600B Series системний блок"
}
```
**Семпл #31:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/kompyuter-ryzen-3600-16gb-1070-ID10Z1PG.html",
  "title": "Комп'ютер Ryzen 3600/16gb/1070"
}
```
**Семпл #32:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/sistemniy-blok-intel-core-2-duo-IDLXwvC.html",
  "title": "Системний блок Intel core 2 duo."
}
```
**Семпл #33:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/igrovoy-pk-ryzen-7-7800x3d-rtx-3080-10gb-32gb-ddr5-6000-ID110Glw.html",
  "title": "Игровой ПК Ryzen 7 7800X3D, RTX 3080 10gb , 32gb DDR5 6000"
}
```
**Семпл #34:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/prodam-igrovoy-pk-ID10OlYg.html",
  "title": "Продам игровой ПК"
}
```
**Семпл #35:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/igrovoy-pk-ryzen-5-7500f-rx-6700-xt-12gb-32gb-ddr5-am5-otlichnoe-sostoyanie-ID10Yrzm.html",
  "title": "Игровой ПК Ryzen 5 7500F / RX 6700 XT 12GB / 32GB DDR5 / AM5 — Отличное состояние"
}
```
**Семпл #36:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/anomalya-rtx-4060-i3-12100f-ddr4-16gb-ssd-240gb-groviy-kompyuter-pk-dlya-gor-geymerskiy-igrovoy-kompyuter-ID10CVEz.html",
  "title": "АНОМАЛІЯ! RTX 4060+i3-12100f+DDR4 16GB+SSD 240GB –  Ігровий комп'ютер ПК для ігор геймерський игровой компьютер"
}
```
**Семпл #37:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/groviy-pk-gtx-1060-kompyuter-4-yadra-16gb-ram-sistemniy-blok-500gb-ID10odpw.html",
  "title": "Ігровий ПК GTX 1060 Комп'ютер 4 ядра / 16GB RAM Системний блок 500GB"
}
```
**Семпл #38:**
```json
{
  "reason": "banned_word_without_pc_indicator: ssd",
  "title": "Продам сервер / робочу станцію  Xeon E5-2680 v4 / 32GB ECC / SSD / 650W Gold"
}
```
**Семпл #39:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/potuzhniy-groviy-pk-rx-7900-xt-20gb-i5-12400-32gb-ssd-1tb-ID10ZWPa.html",
  "title": "Потужний ігровий ПК — RX 7900 XT 20GB / i5-12400 / 32GB / SSD 1TB"
}
```
**Семпл #40:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/groviy-sistemniy-blok-u-novomu-korpus-ID110Gea.html",
  "title": "Ігровий системний блок у новому корпусі"
}
```
**Семпл #41:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/pk-i-komplektuyuschie-b-u-ID10s8wQ.html",
  "title": "ПК и комплектующие б/у"
}
```
**Семпл #42:**
```json
{
  "reason": "banned_word_without_pc_indicator: озу",
  "title": "‼️ТОП Игровой (Ryzen 7 7700, RX 6900Xt 16gb, 32 ОЗУ, 1tb SSD,am5  b850)"
}
```
**Семпл #43:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/prodam-apple-imac-24-b-IDX9UAp.html",
  "title": "Продам Apple Imac 24\" b"
}
```
**Семпл #44:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/prodam-sistemn-bloki-IDUMOxF.html",
  "title": "Продам системні блоки"
}
```
**Семпл #45:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/fujitsu-esprimo-d556-e85-ID10guJu.html",
  "title": "Fujitsu esprimo d556/e85+"
}
```
**Семпл #46:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/sistemniy-blok-amd-kompyuter-pc-IDY44ZK.html",
  "title": "системний блок amd компютер pc"
}
```
**Семпл #47:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/lot-kompyuterna-mishka-klavatura-150-grn-mozhna-okremo-100-grn-sven-a4tech-hp-acme-fujitsu-ID10P6bM.html",
  "title": "(Лот - комп'ютерна мишка + клавіатура - 150 грн (можна окремо - 100 грн)  SVEN / A4Tech / HP / Acme / Fujitsu"
}
```
**Семпл #48:**
```json
{
  "reason": "banned_word_without_pc_indicator: відеокарта",
  "title": "Dell optiplex 755 ноутбук Леново  і відеокарта gt730"
}
```
**Семпл #49:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/nayavnst-antminer-l7-9050-mh-3450-vt-asic-garantya-IDXBbd4.html",
  "title": "НАЯВНІСТЬ! Antminer L7 9050 Mh 3450 Вт ASIC + Гарантія"
}
```
**Семпл #50:**
```json
{
  "reason": "banned_word_without_pc_indicator: озу",
  "title": "‼️ІГРОВА МАШИНА‼️+ Клавіатура + Мишка • Nvidia GTX 1650 • ОЗУ: 24GB • Процесор: intel Core"
}
```
**Семпл #51:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/prodam-kompyuter-groviy-setap-ID10Xm8c.html",
  "title": "Продам Компютер ігровий сетап"
}
```
**Семпл #52:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/pk-kompyuter-groviy-xeon-2680-580-8gb-32ozu-ddr4-dealniy-dlya-svogo-byudzhetu-ID110G7B.html",
  "title": "Пк Компютер Ігровий Xeon 2680, 580 8gb 32озу ддр4 ідеальний для свого бюджету"
}
```
**Семпл #53:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/kompyuter-1050ti-ID10OASC.html",
  "title": "Компьютер 1050ti"
}
```
**Семпл #54:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/asus-eee-top-monoblok-et1602c-IDZjB13.html",
  "title": "Asus Eее Top моноблок ET1602C"
}
```
**Семпл #55:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/prodam-igrovoy-kompyuter-ID10TJ4r.html",
  "title": "Продам игровой компьютер"
}
```
**Семпл #56:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/groviy-pk-i7-4790-gtx1080-8gb-ID10TtOX.html",
  "title": "Ігровий ПК i7-4790, GTX1080 8Gb"
}
```
**Семпл #57:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/pk-dlya-gor-ryzen-5-5500-gtx-1080-ti-11gb-16gb-ddr4-win-10-win-11-ID10P9Ei.html",
  "title": "Пк для ігор Ryzen 5 5500 | GTX 1080 ti 11GB | 16GB DDR4 | Win 10 / Win 11"
}
```
**Семпл #58:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/komplekt-komplektuyuchihnih-dlya-kompyutera-IDRAMBX.html",
  "title": "Комплект комплектуючихних для комп'ютера"
}
```
**Семпл #59:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/korpus-pk-sistemnyy-blok-kompyuter-IDYSzrB.html",
  "title": "Корпус пк системный блок компьютер"
}
```
**Семпл #60:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/byudzhetniy-groviy-pk-i5-4460-nvidia-gtx-960-ssd-240-ID110G0Q.html",
  "title": "Бюджетний ігровий ПК | i5-4460 • Nvidia GTX 960 • SSD 240"
}
```
**Семпл #61:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/pk-kompyuter-sff-core-i5-13500-b760m-32gb-512gb-nvme-1tb-hdd-ID10SqDU.html",
  "title": "ПК компютер SFF (core i5-13500/B760M/32gb/512gb nvme+1tb hdd)"
}
```
**Семпл #62:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/hp-prodesk-405-g8-ryzen-5-pro-5650ge-8-256-gb-displayport-hdmi-wifi-bt-1312-IDXq3rQ.html",
  "title": "HP ProDesk 405 G8 RYZEN 5 PRO 5650GE 8/256 GB DisplayPort HDMI WiFi+BT #1312"
}
```
**Семпл #63:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/pk-monitor-v-polnom-komplekte-IDV90YU.html",
  "title": "ПК+Монитор в полном комплекте"
}
```
**Семпл #64:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/onyx-rtx-5060-ti-8gb-ryzen-7-7700-ddr5-32gb-m-2-ssd-500gb-groviy-kompyuter-pk-dlya-gor-geymerskiy-igrovoy-kompyuter-ID10E0gz.html",
  "title": "ONYX! RTX 5060 Ti 8GB+Ryzen 7 7700+DDR5 32GB+M.2 SSD 500GB –  Ігровий комп'ютер ПК для ігор геймерський игровой компьютер"
}
```
**Семпл #65:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/kompyuter-v-rabochem-sostoyanii-IDYEyuw.html",
  "title": "Компьютер в рабочем состоянии"
}
```
**Семпл #66:**
```json
{
  "reason": "banned_word_without_pc_indicator: hdd",
  "title": "Intel core I7, DDR4 32 гб, 512 SDD, 512 HDD"
}
```
**Семпл #67:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/byudzhetniy-groviy-pk-sistemniy-blok-i5-12gb-gtx-1060-6gb-analog-ID10xQnp.html",
  "title": "Бюджетний ігровий ПК / Системний блок (i5 / 12GB / GTX 1060 6GB аналог)"
}
```
**Семпл #68:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/groviy-kompyuter-r5-5500-16gb-ddr4-rx-5700-xt-8gb-ssd-ID10YqRa.html",
  "title": "Ігровий комп'ютер R5 5500 / 16GB DDR4 / RX 5700 XT 8gb / ssd"
}
```
**Семпл #69:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/lenovo-loq-15iax9i-ID10DAWg.html",
  "title": "Lenovo LOQ 15IAX9I"
}
```
**Семпл #70:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/groviy-kompyuter-r5-3600-16gb-ddr4-rx-5700-xt-8gb-ssd-ID10YqLw.html",
  "title": "Ігровий комп'ютер R5 3600 / 16GB DDR4 / RX 5700 XT 8gb / ssd"
}
```
**Семпл #71:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/igrovoy-pk-pc-rayzen-5-rtx-3060ti-32ram-ssd-hdd-rog-strix-tuf-gaming-ID10YqHD.html",
  "title": "Игровой пк/PC/Rayzen 5/RTX 3060ti/32RAM/SSD+HDD/ROG STRIX/TUF GAMING !"
}
```
**Семпл #72:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/bliy-lev-rtx-5060-ti-8gb-ryzen-5-9600-ddr5-16gb-m-2-ssd-500gb-groviy-kompyuter-pk-dlya-gor-geymerskiy-igrovoy-kompyuter-ID10CWP2.html",
  "title": "Білий Лев! RTX 5060 Ti 8GB+Ryzen 5 9600+DDR5 16GB+M.2 SSD 500GB –  Ігровий комп'ютер ПК для ігор геймерський игровой компьютер"
}
```
**Семпл #73:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/potuzhniy-groviy-kompyuter-5060ti-16gb-ryzen-5500x3d-ID10QydY.html",
  "title": "Потужний ігровий комп'ютер (5060ti 16GB, ryzen 5500x3d)"
}
```
**Семпл #74:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/mn-pk-nettopi-sistemn-bloki-dell-i3-i5-i7-s1151-v2-1150-11-IDY5o6y.html",
  "title": "Міні-ПК / Неттопи / Системні блоки Dell i3 i5 i7 (s1151-V2 / 1150 / 11"
}
```
**Семпл #75:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/groviy-kompyuter-r3-1300x-12gb-ddr4-gtx-1050-ti-4gb-ssd-ID10Yqzb.html",
  "title": "Ігровий комп'ютер R3 1300x / 12GB DDR4 / GTX 1050 Ti 4gb / ssd"
}
```
**Семпл #76:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/sistemniy-blok-dell-optiplex-7010-sff-intel-core-i3-3220-4gb-hdd500gb-kompyuter-IDWKrdU.html",
  "title": "Системний блок Dell OptiPlex 7010 SFF Intel Core i3-3220,4гб,hdd500гб комп'ютер"
}
```
**Семпл #77:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/sistemniy-blok-prodesk-400g5-mini-i5-9500t6yader-8gb-ssd256-IDX0XM6.html",
  "title": "Системний блок ProDesk 400G5 mini i5-9500T(6ядер)/8gb/ssd256"
}
```
**Семпл #78:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/prodam-kompyuter-s-monitorom-ID10YoGn.html",
  "title": "Продам компьютер с монитором!"
}
```
**Семпл #79:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/pk-ryzen-7-5700x-rtx-3060-12gb-32gb-ram-ssd-2tb-periferya-ID10UPk8.html",
  "title": "ПК Ryzen 7 5700X, RTX 3060 12GB, 32GB RAM, SSD 2TB + периферія"
}
```
**Семпл #80:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/v-nayavnost-asic-bitmain-antminer-l7-9050-mh-3400-vt-IDXBbfW.html",
  "title": "В наявності Asic Bitmain Antminer L7 9050 Mh 3400 Вт"
}
```
**Семпл #81:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/topoviy-pk-ryzen-9-9950x3d-asus-rog-astral-rtx-5090-oc-64gb128gb-4tb-m2-ID10Rtnn.html",
  "title": "Топовий ПК Ryzen 9 9950X3D / ASUS ROG Astral RTX 5090 OC / 64GB(128GB) / 4TB M2"
}
```
**Семпл #82:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/igrovoy-pk-ryzen-5-7500f-rx-6700-xt-12gb-32gb-ddr5-am5-otlichnoe-sostoyanie-ID10Yrzm.html",
  "title": "Игровой ПК Ryzen 5 7500F / RX 6700 XT 12GB / 32GB DDR5 / AM5 — Отличное состояние"
}
```
**Семпл #83:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/byudzhetniy-groviy-setap-i5-6400-rx-570-16gb-ddr4-z-montorom-24-ta-pereferyu-ID10LNyN.html",
  "title": "Бюджетний ігровий сетап i5-6400/RX 570/16GB DDR4 з монітором 24\" та переферією"
}
```
**Семпл #84:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/ho-ultra-9-285k-rtx-5080-16gb-ddr5-32gb-m-2-ssd-2tb-robocha-stantsya-groviy-kompyuter-igrovoy-pk-rabochaya-stantsiya-ID10CWqW.html",
  "title": "H²O! Ultra 9 285K+RTX 5080 16GB+DDR5 32GB+M.2 SSD 2TB –  Робоча станція ігровий комп'ютер игровой ПК рабочая станция"
}
```
**Семпл #85:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/fenks-rtx-2060-ryzen-5-3600-ddr4-16gb-m-2-ssd-240gb-groviy-pk-kompyuter-dlya-gor-IDFBQNd.html",
  "title": "ФЕНІКС! RTX 2060+Ryzen 5 3600+DDR4 16GB+M.2 SSD 240GB – ігровий ПК комп'ютер для ігор"
}
```
**Семпл #86:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/300hz-monstr-gtx-1080-ti-i5-12400f-ddr4-16gb-ssd-480gb-groviy-pk-kompyuter-dlya-gor-IDIGaqT.html",
  "title": "300Hz МОНСТР! GTX 1080 Ti+i5-12400f+DDR4 16GB+SSD 480GB – ігровий ПК комп'ютер для ігор"
}
```
**Семпл #87:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/kompyuter-v-zbor-sistemniy-blok-montor-ID10T0eO.html",
  "title": "Комп'ютер в зборі (Системний блок+Монітор)"
}
```
**Семпл #88:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/garantiya-na-vse-komplektuyuschie-5070-12gb-amd-7-5700x-32gb-ddr4-1tb-ssd-ID10eHf1.html",
  "title": "Гарантия на все комплектующие!5070 12GB/AMD 7 5700X/32GB ddr4/1TB SSD"
}
```
**Семпл #89:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/potuzhniy-groviy-pk-rtx-3070-8gb-i5-10600kf-16gb-rgb-ssd-m-2-512gb-ID10KAD1.html",
  "title": "Потужний Ігровий ПК / RTX 3070 8GB / i5-10600KF / 16GB RGB / SSD M.2 512GB"
}
```
**Семпл #90:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/kompyuter-z-vropi-pk-hp-600-g4-sff-s1151-sistemniy-blok-i3-i5-i7-IDVjyEY.html",
  "title": "Комп'ютер із Європи ПК HP 600 G4 SFF s1151 системний блок i3/i5/i7"
}
```
**Семпл #91:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/apple-mac-studio-m2-max-12-30-yader-32-gb-512-ssd-povniy-komplekt-ID10YpFp.html",
  "title": "Apple Mac Studio M2 Max 12/30 ядер · 32 ГБ · 512 SSD · повний комплект"
}
```
**Семпл #92:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/kompyuter-byudzhetniy-groviy-ryzen-5600-32-ddr-1-5tb-m2-rtx-3060-12gb-IDSvaOS.html",
  "title": "Компьютер Бюджетний Ігровий Ryzen 5600+32 ddr+1.5тб м2+RTX 3060 12gb"
}
```
**Семпл #93:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/kompyuter-fx4100-rx5604gb-ID10c1LF.html",
  "title": "Компютер Fx4100/rx560(4GB)"
}
```
**Семпл #94:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/mayner-s19-bitmain-asik-antminer-s19j-pro-120t-garantya-b-v-430-ID10kCRS.html",
  "title": "Майнер S19! Bitmain asik antminer S19j pro+ 120T + Гарантія (Б/В 430$)"
}
```
**Семпл #95:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/igrovoy-pk-core-i5-6600-gtx-1060-6gb-16gb-ram-ssd-hdd-lyubye-testy-ID110Hd2.html",
  "title": "Игровой ПК Core i5 6600 / GTX 1060 6GB / 16GB RAM / SSD + HDD (Любые тесты)"
}
```
**Семпл #96:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/prodam-sistemniy-blok-ID10E1yQ.html",
  "title": "Продам системний блок"
}
```
**Семпл #97:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/l7-9050-gh-s-asic-bitmain-doge-ltc-antminer-ID10gSTJ.html",
  "title": "L7- 9050 gh/s Asic, Bitmain, DOGE, LTC, Antminer"
}
```
**Семпл #98:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/pk-korpus-ta-komplektuyuch-vdeokarti-tsp-bloki-zhivlennya-ssd-ddr2-ddr3-ID10AQEP.html",
  "title": "ПК корпус та комплектуючі, відеокарти, цп, блоки живлення, ssd, ddr2 ddr3"
}
```
**Семпл #99:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/kompyuteri-fujitsu-sff-s1151-55-sistemn-bloki-i3-i5-i7-pk-ssd120-250-IDRHxnN.html",
  "title": "Комп'ютери Fujitsu SFF s1151/55 Системні блоки i3/i5/i7 ПК SSD120/250"
}
```
**Семпл #100:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/kompyuter-fx6300-rx560-ID102DYH.html",
  "title": "Комп'ютер FX6300 + RX560"
}
```

### 🔹 Валідовані оголошення ПК (пройшли перевірку is_real_pc) (Показано 100 з max 100):
**Семпл #1:**
```json
{
  "ad_id": 805590234,
  "title": "Компьютер Бюджетний Ігровий Ryzen 5600+32 ddr+1.5тб м2+RTX 3060 12gb",
  "status": "passed_is_real_pc"
}
```
**Семпл #2:**
```json
{
  "ad_id": 931066333,
  "title": "Игровой ПК 1660 ti oc",
  "status": "passed_is_real_pc"
}
```
**Семпл #3:**
```json
{
  "ad_id": 931075268,
  "title": "Игровой ПК Core i5 6600 / GTX 1060 6GB / 16GB RAM / SSD + HDD (Любые тесты)",
  "status": "passed_is_real_pc"
}
```
**Семпл #4:**
```json
{
  "ad_id": 925671956,
  "title": "Продам системний блок",
  "status": "passed_is_real_pc"
}
```
**Семпл #5:**
```json
{
  "ad_id": 916763167,
  "title": "Компютер FX6300 + RX560",
  "status": "passed_is_real_pc"
}
```
**Семпл #6:**
```json
{
  "ad_id": 931074830,
  "title": "Продам комьютер, в хорошем состоянии",
  "status": "passed_is_real_pc"
}
```
**Семпл #7:**
```json
{
  "ad_id": 920068205,
  "title": "Системный блок Atlon FM-1 AMD A8-3870K /ASRock A75 Pro4/MVP/ DDR3-16Gb (1866) / HDD-500Gb / 400 Watt",
  "status": "passed_is_real_pc"
}
```
**Семпл #8:**
```json
{
  "ad_id": 925417853,
  "title": "Медуза! 44 ядра+RTX 3080 Ti 12GB+DDR4 64GB+M.2 SSD 500GB –  Робоча станція ігровий компютер игровой ПК рабочая станция",
  "status": "passed_is_real_pc"
}
```
**Семпл #9:**
```json
{
  "ad_id": 929699822,
  "title": "Ігровий Компьютер",
  "status": "passed_is_real_pc"
}
```
**Семпл #10:**
```json
{
  "ad_id": 930882252,
  "title": "Ігровий ПК GTX 1060 (P106-100) i5-7400 (МОЖЛИВИЙ ОПТ)",
  "status": "passed_is_real_pc"
}
```
**Семпл #11:**
```json
{
  "ad_id": 907314417,
  "title": "Ігровий ПК. INTEL CORE I7, 16Gb ОЗУ, RX 560 , SSD 120 GB, HDD 1000GB",
  "status": "passed_is_real_pc"
}
```
**Семпл #12:**
```json
{
  "ad_id": 890567286,
  "title": "Потужний ігровий ПК RTX 3080 / i7 / 32GB / NVMe — готовий до будь-яких задач",
  "status": "passed_is_real_pc"
}
```
**Семпл #13:**
```json
{
  "ad_id": 931074531,
  "title": "Компютер на 1060",
  "status": "passed_is_real_pc"
}
```
**Семпл #14:**
```json
{
  "ad_id": 867656469,
  "title": "HP EliteDesk 800 G2 SFF Business PC(ssd 256gb,intel core i5,ddr4 8gb)",
  "status": "passed_is_real_pc"
}
```
**Семпл #15:**
```json
{
  "ad_id": 874014591,
  "title": "продам компьютер",
  "status": "passed_is_real_pc"
}
```
**Семпл #16:**
```json
{
  "ad_id": 915737786,
  "title": "Продам ПК ryzen7 3700x/3070ti/32gb/512gb ssd + 2TBssd",
  "status": "passed_is_real_pc"
}
```
**Семпл #17:**
```json
{
  "ad_id": 931074250,
  "title": "Продам свій ігровий компютер",
  "status": "passed_is_real_pc"
}
```
**Семпл #18:**
```json
{
  "ad_id": 930803930,
  "title": "Продажа среднего пк(описание)",
  "status": "passed_is_real_pc"
}
```
**Семпл #19:**
```json
{
  "ad_id": 931074180,
  "title": "ПК для геймерів (новий)",
  "status": "passed_is_real_pc"
}
```
**Семпл #20:**
```json
{
  "ad_id": 929594144,
  "title": "Пк, системний блок",
  "status": "passed_is_real_pc"
}
```
**Семпл #21:**
```json
{
  "ad_id": 925417202,
  "title": "МОНОЛІТ! RX 570 4GB+Ryzen 5 1600+DDR4 16GB+SSD 120GB –  Ігровий компютер ПК для ігор геймерський игровой компьютер",
  "status": "passed_is_real_pc"
}
```
**Семпл #22:**
```json
{
  "ad_id": 911287952,
  "title": "Матплата HP EliteDesk 800 G6 DM USFF L79218-002 L86387-601 L86387-001",
  "status": "passed_is_real_pc"
}
```
**Семпл #23:**
```json
{
  "ad_id": 928233730,
  "title": "Ігровий ПК! RTX5060 | Ryzen 7 5700x | 32gb DDR4 | 1tb SSD | 850w | B550",
  "status": "passed_is_real_pc"
}
```
**Семпл #24:**
```json
{
  "ad_id": 920336648,
  "title": "Компютер Dell 3070mff i3-9100t 16gb 256gb ssd+adapter+cable в наявності",
  "status": "passed_is_real_pc"
}
```
**Семпл #25:**
```json
{
  "ad_id": 931073954,
  "title": "пк, игровой,на 11 винде",
  "status": "passed_is_real_pc"
}
```
**Семпл #26:**
```json
{
  "ad_id": 927443310,
  "title": "Міні ПК 10ген Dell 3090mff i5-10400t 6x3,6GHz 16gb 512gb ssd+adapter+cable в наявності",
  "status": "passed_is_real_pc"
}
```
**Семпл #27:**
```json
{
  "ad_id": 907882351,
  "title": "Продам ПК на FM2+",
  "status": "passed_is_real_pc"
}
```
**Семпл #28:**
```json
{
  "ad_id": 359518014,
  "title": "Компютер системний блок Dell packard bell",
  "status": "passed_is_real_pc"
}
```
**Семпл #29:**
```json
{
  "ad_id": 930703789,
  "title": "Бюджетний ПК для навчання та роботи / ПК для работы и учебы",
  "status": "passed_is_real_pc"
}
```
**Семпл #30:**
```json
{
  "ad_id": 839114415,
  "title": "Anritsu MP1590B аналізатор сигналів",
  "status": "passed_is_real_pc"
}
```
**Семпл #31:**
```json
{
  "ad_id": 924742733,
  "title": "HP Compaq 8000 Elite CMT PC",
  "status": "passed_is_real_pc"
}
```
**Семпл #32:**
```json
{
  "ad_id": 916761096,
  "title": "Apple Imac 21.5\" ssd 256 Стан нового.",
  "status": "passed_is_real_pc"
}
```
**Семпл #33:**
```json
{
  "ad_id": 931073525,
  "title": "Продам компьютер",
  "status": "passed_is_real_pc"
}
```
**Семпл #34:**
```json
{
  "ad_id": 789684322,
  "title": "Системний блок в гарному стані",
  "status": "passed_is_real_pc"
}
```
**Семпл #35:**
```json
{
  "ad_id": 843432820,
  "title": "Моноблок (блок)",
  "status": "passed_is_real_pc"
}
```
**Семпл #36:**
```json
{
  "ad_id": 924638452,
  "title": "Продам компютер + монітор",
  "status": "passed_is_real_pc"
}
```
**Семпл #37:**
```json
{
  "ad_id": 910751548,
  "title": "Джистік havic для ПК",
  "status": "passed_is_real_pc"
}
```
**Семпл #38:**
```json
{
  "ad_id": 931073345,
  "title": "Стаціонарний ПК Acer AX5950 core i5, Radeon HD 5570, озу 4Gb",
  "status": "passed_is_real_pc"
}
```
**Семпл #39:**
```json
{
  "ad_id": 928327427,
  "title": "Продам игровий пк без видиокарти",
  "status": "passed_is_real_pc"
}
```
**Семпл #40:**
```json
{
  "ad_id": 931073027,
  "title": "Игровой комп на 1070 ti | ryzen 7-1700 | 32 ggb",
  "status": "passed_is_real_pc"
}
```
**Семпл #41:**
```json
{
  "ad_id": 930894358,
  "title": "Ігровий ПК/Ryzen 5/ASUS ROG Strix RX5700xt/16OZU",
  "status": "passed_is_real_pc"
}
```
**Семпл #42:**
```json
{
  "ad_id": 931072950,
  "title": "Продаю компьютер.",
  "status": "passed_is_real_pc"
}
```
**Семпл #43:**
```json
{
  "ad_id": 925707864,
  "title": "Игровой ПК i3-10100F / 32GB DDR4 / GTX 1660 Super 6GB / SSD+HDD",
  "status": "passed_is_real_pc"
}
```
**Семпл #44:**
```json
{
  "ad_id": 930596933,
  "title": "Игровой ПК i5-9500F / RX 590 8GB / 16GB RAM / SSD",
  "status": "passed_is_real_pc"
}
```
**Семпл #45:**
```json
{
  "ad_id": 929793789,
  "title": "Продам свой игровой компьютер + монитор 27 дюймов Samsung",
  "status": "passed_is_real_pc"
}
```
**Семпл #46:**
```json
{
  "ad_id": 920063117,
  "title": "ПК і Вайфай модуль",
  "status": "passed_is_real_pc"
}
```
**Семпл #47:**
```json
{
  "ad_id": 906026170,
  "title": "Ідеальний компютер для ігор",
  "status": "passed_is_real_pc"
}
```
**Семпл #48:**
```json
{
  "ad_id": 922824527,
  "title": "PC | Компактний системний блок (i5-9600K\\8GB DDR4\\256GB NVMe\\1TB HDD)",
  "status": "passed_is_real_pc"
}
```
**Семпл #49:**
```json
{
  "ad_id": 761092972,
  "title": "Продам компютер",
  "status": "passed_is_real_pc"
}
```
**Семпл #50:**
```json
{
  "ad_id": 679654226,
  "title": "Компютер Dell Inspiron 3650",
  "status": "passed_is_real_pc"
}
```
**Семпл #51:**
```json
{
  "ad_id": 929242046,
  "title": "Мікрокомпютер Raspberry Pi 5  2GB",
  "status": "passed_is_real_pc"
}
```
**Семпл #52:**
```json
{
  "ad_id": 930700722,
  "title": "Компютер 13700k / MSI B660M Mortar DDR4 / 32Gb / Gigabyte 1000W",
  "status": "passed_is_real_pc"
}
```
**Семпл #53:**
```json
{
  "ad_id": 930864519,
  "title": "Продам ігровий пк.Компютер.x3d",
  "status": "passed_is_real_pc"
}
```
**Семпл #54:**
```json
{
  "ad_id": 899585112,
  "title": "Apple Mac Mini M1 A2348 3.2\\16\\512 iСloud lock неттоп міні пк",
  "status": "passed_is_real_pc"
}
```
**Семпл #55:**
```json
{
  "ad_id": 819132425,
  "title": "Компактный системный блок ZOTAC ZBOX - ID41 - E, FCBGA559",
  "status": "passed_is_real_pc"
}
```
**Семпл #56:**
```json
{
  "ad_id": 931069915,
  "title": "Потужна база для ПК без відеокарти | Ryzen 5 3600 / 32GB RAM / 1.5TB SSD / 700W",
  "status": "passed_is_real_pc"
}
```
**Семпл #57:**
```json
{
  "ad_id": 930699972,
  "title": "Игровой Компьютер,ПК/Ryzen 5 5600X,DDR4 32GB 3200Mhz,RTX 3070TI,M2 1TB/Ігровий ПК",
  "status": "passed_is_real_pc"
}
```
**Семпл #58:**
```json
{
  "ad_id": 873454026,
  "title": "Продам игровой компьютер",
  "status": "passed_is_real_pc"
}
```
**Семпл #59:**
```json
{
  "ad_id": 922836748,
  "title": "Продам килимки для мишки",
  "status": "passed_is_real_pc"
}
```
**Семпл #60:**
```json
{
  "ad_id": 920750849,
  "title": "Продам потужний ігровий ПК | Ryzen 5 5600 + RTX 5060 | Готовий до ігор",
  "status": "passed_is_real_pc"
}
```
**Семпл #61:**
```json
{
  "ad_id": 911282195,
  "title": "Продам компьютер в полном комплекте",
  "status": "passed_is_real_pc"
}
```
**Семпл #62:**
```json
{
  "ad_id": 931055730,
  "title": "Ігровий компʼютер rtx 4060/i5-12400f/ddr4 32gb",
  "status": "passed_is_real_pc"
}
```
**Семпл #63:**
```json
{
  "ad_id": 929235312,
  "title": "Ігровий ПК | RTX 3060 12GB | Ryzen 5500 | 16GB | M.2 SSD | Компʼютер",
  "status": "passed_is_real_pc"
}
```
**Семпл #64:**
```json
{
  "ad_id": 898437989,
  "title": "Lenovo ThinkCentre M75Q RYZEN 5 PRO 3400GE 8/256GB HDMI DP WiFi #8731",
  "status": "passed_is_real_pc"
}
```
**Семпл #65:**
```json
{
  "ad_id": 931069618,
  "title": "Системный блок старенький в",
  "status": "passed_is_real_pc"
}
```
**Семпл #66:**
```json
{
  "ad_id": 913251037,
  "title": "Компютерні колонки Gemix",
  "status": "passed_is_real_pc"
}
```
**Семпл #67:**
```json
{
  "ad_id": 769775453,
  "title": "Срочно Компьютер BRAVO",
  "status": "passed_is_real_pc"
}
```
**Семпл #68:**
```json
{
  "ad_id": 917769860,
  "title": "Персональний Компютер Ryzen 7 5700g, 64gb ram ddr4",
  "status": "passed_is_real_pc"
}
```
**Семпл #69:**
```json
{
  "ad_id": 911281449,
  "title": "Збірка ПК під ключ.",
  "status": "passed_is_real_pc"
}
```
**Семпл #70:**
```json
{
  "ad_id": 930697957,
  "title": "моноблок Dell inspiron 5459 all-in-one",
  "status": "passed_is_real_pc"
}
```
**Семпл #71:**
```json
{
  "ad_id": 776941796,
  "title": "Системный блок + монітор",
  "status": "passed_is_real_pc"
}
```
**Семпл #72:**
```json
{
  "ad_id": 930901318,
  "title": "Продам компютер fx6300+1050ti ОЗУ 16 гб",
  "status": "passed_is_real_pc"
}
```
**Семпл #73:**
```json
{
  "ad_id": 763293662,
  "title": "компютер компьютер системний блок",
  "status": "passed_is_real_pc"
}
```
**Семпл #74:**
```json
{
  "ad_id": 930391237,
  "title": "Моноблок Lenovo m93z All-in-One 23\"",
  "status": "passed_is_real_pc"
}
```
**Семпл #75:**
```json
{
  "ad_id": 856720361,
  "title": "Компьютер з ліцензованим windows",
  "status": "passed_is_real_pc"
}
```
**Семпл #76:**
```json
{
  "ad_id": 776941580,
  "title": "Комп’ютер системний блок",
  "status": "passed_is_real_pc"
}
```
**Семпл #77:**
```json
{
  "ad_id": 899583655,
  "title": "Компютер Intel NUC 13 Pro Kit,",
  "status": "passed_is_real_pc"
}
```
**Семпл #78:**
```json
{
  "ad_id": 931068946,
  "title": "ПК GT 1030 2 GB GDDR5 +INTEL I3 8100 8 GBDDR4",
  "status": "passed_is_real_pc"
}
```
**Семпл #79:**
```json
{
  "ad_id": 774251746,
  "title": "Компютер з монітором та клавіатурою куплений у Німеччині",
  "status": "passed_is_real_pc"
}
```
**Семпл #80:**
```json
{
  "ad_id": 931068862,
  "title": "Intel NUC NUC6i7KYK Skull Canyon, Core i7, 32GB DDR4, WD NVMe SSD, Компактний Mini PC",
  "status": "passed_is_real_pc"
}
```
**Семпл #81:**
```json
{
  "ad_id": 931068742,
  "title": "Важливо шановні!",
  "status": "passed_is_real_pc"
}
```
**Семпл #82:**
```json
{
  "ad_id": 563924433,
  "title": "Компьютер Amd системный блок",
  "status": "passed_is_real_pc"
}
```
**Семпл #83:**
```json
{
  "ad_id": 931068603,
  "title": "Ігровий ПК i5-3570 RX470 4GB",
  "status": "passed_is_real_pc"
}
```
**Семпл #84:**
```json
{
  "ad_id": 927968915,
  "title": "ПК ryzen 7 5700x3d rtx3060ti",
  "status": "passed_is_real_pc"
}
```
**Семпл #85:**
```json
{
  "ad_id": 871090220,
  "title": "Потужний ігровий системний блок Dell Precision T3610",
  "status": "passed_is_real_pc"
}
```
**Семпл #86:**
```json
{
  "ad_id": 922835319,
  "title": "Пк на 1080ti 32 ОЗУ 3600МГц",
  "status": "passed_is_real_pc"
}
```
**Семпл #87:**
```json
{
  "ad_id": 920060491,
  "title": "Комп\"ютер (ПК, персональний коп\"ютер)",
  "status": "passed_is_real_pc"
}
```
**Семпл #88:**
```json
{
  "ad_id": 762818002,
  "title": "Apple Mac Mini A1176 Desktop - 1.83/2x512/80/COMBO/AP/BT",
  "status": "passed_is_real_pc"
}
```
**Семпл #89:**
```json
{
  "ad_id": 927247437,
  "title": "Продам ігровий пк",
  "status": "passed_is_real_pc"
}
```
**Семпл #90:**
```json
{
  "ad_id": 928321200,
  "title": "Продам копʼютер LG",
  "status": "passed_is_real_pc"
}
```
**Семпл #91:**
```json
{
  "ad_id": 765177855,
  "title": "Продам / соберу ПК в отличном состоянии",
  "status": "passed_is_real_pc"
}
```
**Семпл #92:**
```json
{
  "ad_id": 931067966,
  "title": "мощный игровой ПК в сборе. razyn 5 5600 & rtx 2060 super & RAM 16 + монитор 144 hz , клавиатура, мышка superlite, кранштейн , стол, коврик, наушники",
  "status": "passed_is_real_pc"
}
```
**Семпл #93:**
```json
{
  "ad_id": 931068072,
  "title": "Ігровий ПК. Повний комплект. і5, 16гб. DDR4, RX580 8GB, SSD",
  "status": "passed_is_real_pc"
}
```
**Семпл #94:**
```json
{
  "ad_id": 930888645,
  "title": "Игровой ПК MSI RTX 3050 8GB / Intel Core i3-10105F / 16GB RAM / SSD + HDD",
  "status": "passed_is_real_pc"
}
```
**Семпл #95:**
```json
{
  "ad_id": 569954730,
  "title": "Продам системный блок",
  "status": "passed_is_real_pc"
}
```
**Семпл #96:**
```json
{
  "ad_id": 873047298,
  "title": "Продаю потужний ігровий ПК! Ідеальний  для геймерів та ентузіастів!",
  "status": "passed_is_real_pc"
}
```
**Семпл #97:**
```json
{
  "ad_id": 931067901,
  "title": "Пк полностю рабочие детали не запускаться в описание",
  "status": "passed_is_real_pc"
}
```
**Семпл #98:**
```json
{
  "ad_id": 931067885,
  "title": "Продам  настольний компʼютер MSI ms 7680 з монітором Asus ml238h",
  "status": "passed_is_real_pc"
}
```
**Семпл #99:**
```json
{
  "ad_id": 931067855,
  "title": "Продам ігровий пк!!!",
  "status": "passed_is_real_pc"
}
```
**Семпл #100:**
```json
{
  "ad_id": 928429294,
  "title": "Системний блок для cs, wot з відеокартою 8Gb",
  "status": "passed_is_real_pc"
}
```

============================================================

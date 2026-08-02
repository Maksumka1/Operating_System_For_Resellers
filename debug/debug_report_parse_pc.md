# 🐛 ДЕБАГ-ЗВІТ ПАРСИНГУ ГОТОВИХ ПК (OLX Category 78)
**Дата та час запуску:** 2026-08-02 19:28:14
**Тривалість виконання:** 127.43 сек
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
- **Завантажено URLs для дедуплікації:** 10255

### ⚙️ Секція: OLX_GraphQL
- **Отримано сирих оголошень ПК:** 260

### ⚙️ Секція: Parsing_Metrics
- **Успішно розпаршено ПК:** 34

### ⚙️ Секція: Filtering_Rules
- **Відсіяно if (Дублікат URL в DB):** 218
- **Відсіяно if (Спрацював фільтр запчастин is_real_pc):** 8

### ⚙️ Секція: Summary
- **Знайдено нових ПК:** 34
- **Пропущено дублікатів:** 218
- **Немає нових лотів для відправки:** 1

### ⚙️ Секція: Supabase_Output
- **Успішно збережено в DB:** 34

### ⚙️ Секція: WebSocket
- **Успішно тригернуто живий стрім:** 1

## 🔄 3. Детальні приклади даних
### 🔹 Відсіяні оголошення (запчастини, окремі комплектуючі, дублікати) (Показано 100 з max 100):
**Семпл #1:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/new-antminer-l9-17-gh-plata-7007-miner-asic-bitmain-mayner-garantya-IDXpmX7.html",
  "title": "NEW Antminer L9 17 Gh плата 7007 miner Asic Bitmain, Майнер + Гарантія"
}
```
**Семпл #2:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/bliskavka-rx-5700-xt-12-yader-32gb-ram-ssd-120gb-groviy-kompyuter-pk-dlya-gor-geymerskiy-igrovoy-kompyuter-ID10FWnr.html",
  "title": "Блискавка! RX 5700 XT+12 ядер+32GB RAM+SSD 120GB –  Ігровий комп'ютер ПК для ігор геймерський игровой компьютер"
}
```
**Семпл #3:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/groviy-kompyuter-pk-rtx-3060-i5-10400f-16-ddr4-ssd-120-hdd-500-gb-ID10B7lf.html",
  "title": "Ігровий компʼютер/пк RTX 3060 i5-10400f 16 ddr4 ssd 120/hdd 500 GB"
}
```
**Семпл #4:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/monoblok-lenovo-yoga-a940-27-4k-i7-8700-3-20ghz-32gb-512gb-ssd-1tb-hdd-radeon-rx-560x-sensornyy-ID10RJxw.html",
  "title": "Моноблок Lenovo Yoga A940 27\" 4K i7-8700 3.20GHz 32GB 512GB SSD/1TB HDD Radeon RX 560X Сенсорный"
}
```
**Семпл #5:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/navchannya-gri-ta-robota-gtx1060-6gb-i5-groviy-pk-igrovoy-kompyuter-IDZ80uf.html",
  "title": "Навчання, ігри та робота! GTX1060 6GB+i5 ігровий ПК игровой комп'ютер"
}
```
**Семпл #6:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/igrovoy-kompyuter-igrovoy-pk-wot-cs2-kompyuter-dlya-igor-kompyuter-dlya-igry-pk-dlya-igor-pk-dlya-igry-ID10IRj9.html",
  "title": "Игровой компьютер, игровой пк, WoT CS2 компьютер для игор компьютер для игры  ПК для Игор, ПК для игры"
}
```
**Семпл #7:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/kompyuter-fujitsu-esprimo-d756-sff-i3-6100-8gb-ddr4-hdd-500gb-z-mozhlivstyu-apgreyda-klkst-garantya-12-msyatsv-ID10PS0N.html",
  "title": "Комп'ютер Fujitsu Esprimo D756 SFF i3-6100 8GB DDR4 HDD 500GB з можливістю апгрейда (є кількість) + Гарантія 12 місяців"
}
```
**Семпл #8:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/groviy-pk-ryzen-5-7500f-rtx-5060-ti-ddr5-am5-ID10XocF.html",
  "title": "Ігровий ПК Ryzen 5 7500F RTX 5060 Ti DDR5 AM5"
}
```
**Семпл #9:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/robochiy-personalniy-kompyuter-pk-u-zbor-chieftec-giga-gx-01sl-IDVFElD.html",
  "title": "робочий персональний комп'ютер ПК у зборі Chieftec Giga GX-01SL"
}
```
**Семпл #10:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/sistemn-bloki-ddr3-ddr4-ID10b6Ys.html",
  "title": "Системні блоки DDR3 DDR4"
}
```
**Семпл #11:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/groviy-pk-rtx-4060-i3-12100f-24gb-ID10Z3Od.html",
  "title": "Ігровий ПК RTX 4060 / i3-12100F / 24GB"
}
```
**Семпл #12:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/titan-ryzen-9-5950x-rtx-3080-ti-12gb-ddr4-64gb-m-2-ssd-1tb-robocha-stantsya-groviy-kompyuter-igrovoy-pk-rabochaya-stantsiya-ID10FW5E.html",
  "title": "ТИТАН! Ryzen 9 5950X+RTX 3080 Ti 12GB+DDR4 64GB+M.2 SSD 1TB –  Робоча станція ігровий комп'ютер игровой ПК рабочая станция"
}
```
**Семпл #13:**
```json
{
  "reason": "banned_word_without_pc_indicator: озу",
  "title": "HP-i5/12GB-ОЗУ/120-ССД."
}
```
**Семпл #14:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/monoblok-apple-imac-21-1-apple-m1-8gb-256gb-24-4-5k-2021-rk-blue-ID102UKO.html",
  "title": "Моноблок Apple iMac 21,1/Apple M1/8GB/256GB/24\"/4.5K/2021 рік/Blue"
}
```
**Семпл #15:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/kompyuter-sistemn-bloki-3-5-komplekti-pk-montori-kompyuter-IDXP9cJ.html",
  "title": "Компʼютер, системні блоки і3 і5 , Комплекти ПК ,+ Монітори. Компютер"
}
```
**Семпл #16:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/igrovoy-pk-komplekt-xeon-e5-2680v4-32-gb-ddr-4-ID10OG1g.html",
  "title": "Игровой ПК  комплект xeon e5 2680v4 32 gb ddr 4"
}
```
**Семпл #17:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/prodam-pk-v-robochomu-stan-ID10YEsw.html",
  "title": "Продам ПК в робочому стані."
}
```
**Семпл #18:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/asic-antminer-t21-IDZOIIr.html",
  "title": "ASIC AntMiner t21"
}
```
**Семпл #19:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/prodam-sistemnyy-blok-dell-990-ID10Z3Ii.html",
  "title": "Продам системный блок dell 990"
}
```
**Семпл #20:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/prodam-osobistiy-sistemniy-blok-IDTmc1d.html",
  "title": "Продам особистий системний блок"
}
```
**Семпл #21:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/prodayu-svy-domashny-setap-groviy-pk-montor-klava-mishka-v-podarunok-ID10VNgZ.html",
  "title": "Продаю свій домашній \"сетап\" - ігровий пк + монітор + клава (мишка в подарунок)"
}
```
**Семпл #22:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/samouchitel-pk-s-uchetom-noveyshih-programm-ID10Z3Dv.html",
  "title": "Самоучитель ПК с учетом новейших программ"
}
```
**Семпл #23:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/pk-i5-12400f-4060-ti-16gb-ddr4-mini-itx-formatu-ID10Z3CH.html",
  "title": "ПК i5-12400f, 4060 ti, 16gb ddr4, mini-itx формату"
}
```
**Семпл #24:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/kompyuter-dlya-roboti-domu-ta-rozvag-kompyuter-IDXly1v.html",
  "title": "Компʼютер для роботи, дому та розваг компютер"
}
```
**Семпл #25:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/prodam-pk-geforce-rtx-3060-obmn-na-makbuk-ID10Z3BN.html",
  "title": "Продам ПК Geforce Rtx 3060 обмін на макбук"
}
```
**Семпл #26:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/groviy-pk-ryzen-5-5600-rtx-4060-8gb-ID10VpX6.html",
  "title": "Ігровий ПК Ryzen 5 5600, RTX 4060 8gb"
}
```
**Семпл #27:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/pk-fujitsu-esprimo-p7010n-mt-s1200-i3-i5-i7-8-16gb-128-256-512gb-nvme-ID10i6on.html",
  "title": "ПК Fujitsu Esprimo P7010n MT s1200 i3 i5 i7 8 16GB 128 256 512GB NVMe"
}
```
**Семпл #28:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/groviy-pk-rtx-3060-12gb-i512400f-faktichno-noviy-ID10VhGs.html",
  "title": "Ігровий ПК: RTX 3060 12GB + i5‑12400F | фактично новий"
}
```
**Семпл #29:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/prodam-sistemnyy-blok-ID10Z3zq.html",
  "title": "Продам системный блок"
}
```
**Семпл #30:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/sistemniy-blok-pk-dell-t1500-5-kompyuter-IDXjBeP.html",
  "title": "Системний блок пк  Dell T1500 і5 комп'ютер"
}
```
**Семпл #31:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/pk-4770k-ozu-16gb-rx580-8gb-bp-750vt-ID10Okcd.html",
  "title": "ПК 4770К, ОЗУ 16Gb, RX580 8GB, БП 750Вт"
}
```
**Семпл #32:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/monoblok-hp-proone-440-g5-IDTV5xD.html",
  "title": "Моноблок hp ProOne 440 g5"
}
```
**Семпл #33:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/kompyuter-samsung-IDWvj84.html",
  "title": "Компьютер самсунг"
}
```
**Семпл #34:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/groviy-byudzhetniy-pk-5-4570-16gb-ssd-120-hdd-500gb-gtx-1060-6gb-top-tsna-ID10NCQE.html",
  "title": "Ігровий б'юджетний  Пк І5 4570, 16gb, Ssd 120, Hdd 500gb, Gtx 1060 6gb !!!Топ ціна!!!"
}
```
**Семпл #35:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/sistemnyy-blok-tihiy-bezshumniy-pentium-j2900-IDT44DM.html",
  "title": "Системный блок тихий безшумний Pentium J2900"
}
```
**Семпл #36:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/vodoblok-ek-fc1080-gtx-ti-gtx-ftw3-fullcover-IDX6ryO.html",
  "title": "Водоблок EK-FC1080 GTX Ti GTX FTW3 (FullCover)"
}
```
**Семпл #37:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/kompyutery-i3-i5-i7-sistemnye-bloki-dell-pk-s775-1155-1150-opt-ssd-IDSPQYE.html",
  "title": "Компьютеры, (i3 i5 i7) Системные блоки Dell ПК s775 1155 1150 ОПТ SSD"
}
```
**Семпл #38:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/kompyuteri-i3-i5-i7-pk-1151-50-55-z-vropi-optom-garantya-bezgotvk-IDYqWY9.html",
  "title": "Комп'ютери i3, i5, i7, ПК 1151 50 55 з Європи оптом гарантія Безготівк"
}
```
**Семпл #39:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/kompyuteri-dlya-ofsu-ta-domu-nedorogo-dell-fujitsu-hp-lenovo-pk1155-50-IDSVF2Q.html",
  "title": "Комп'ютери для Офісу та Дому Недорого Dell Fujitsu HP Lenovo ПК1155/50"
}
```
**Семпл #40:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/sistemniy-blok-asus-ozu-8-gb-vdeokarta-2-gb-IDYXJgr.html",
  "title": "Системний блок ASUS: ОЗУ 8 ГБ/відеокарта 2 ГБ"
}
```
**Семпл #41:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/groviy-pk-ryzen-5-gtx1080-8gb-ddr4-16gb-ssd-hdd-argb-ID10YmCT.html",
  "title": "Ігровий пк Ryzen 5/GTX1080 8gb/ DDR4 16gb/ssd+hdd/ARGB"
}
```
**Семпл #42:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/pk-prodam-robochiy-ID10NMpE.html",
  "title": "ПК. Продам робочий"
}
```
**Семпл #43:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/groviy-kompyuter-dlya-bud-yakih-gor-ID10bh6N.html",
  "title": "Ігровий комп'ютер для будь-яких ігор"
}
```
**Семпл #44:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/prodam-kompyuter-IDX4bJT.html",
  "title": "Продам комп'ютер"
}
```
**Семпл #45:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/groviy-sistemnik-i3-10100f-16g-ddr4-gtx-1660-6g-ssd-480gb-ID10Z3mP.html",
  "title": "Ігровий системник i3-10100F 16g ddr4 GTX 1660 6g SSD 480GB"
}
```
**Семпл #46:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/garniy-groviy-pk-rx-580-8-gb-i-4771-16gb-ram-ID10Z3mj.html",
  "title": "Гарний ігровий пк (RX 580 8 gb, i-4771 16gb RAM)"
}
```
**Семпл #47:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/kompyuter-byudzhetniy-u-novomu-kompaktnomu-korpus-z-8-yadernim-protsesorom-ID10V9Yu.html",
  "title": "Компьютер бюджетний у новому компактному корпусі з 8-ядерним процесором"
}
```
**Семпл #48:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/prodam-termnovo-kompyuter-samsung-v-m-hust-IDX2J2J.html",
  "title": "Продам терміново комп'ютер Samsung в м.Хуст"
}
```
**Семпл #49:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/moshnyy-igrovoy-pk-pc-i5-10400f-16ram-ssd-hdd-ID10I5ne.html",
  "title": "Мошный игровой пк/PC/i5 10400f /16RAM/SSD+HDD!"
}
```
**Семпл #50:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/b-v-mayneri-asic-bitmain-antminer-s19-90-th-3250vt-garantya-IDX4E7v.html",
  "title": "Б/в Майнери Asic Bitmain Antminer S19 90 Th 3250Вт + Гарантія"
}
```
**Семпл #51:**
```json
{
  "reason": "banned_word_without_pc_indicator: ram",
  "title": "Ryzen 5900x + RTX 3090 + 64GB RAM"
}
```
**Семпл #52:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/groviy-pk-komplekt-z-montorom-periferya-v-podarunok-benq-gtx-1060-core-i7-16gb-2xssd-500gb-hdd-ID10Qvq8.html",
  "title": "Ігровий ПК комплект з монітором. Периферія в подарунок. BenQ / GTX 1060 / Core i7 / 16GB / 2xSSD 500gb + HDD"
}
```
**Семпл #53:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/fujitsu-futro-s720-slim-IDUYPoH.html",
  "title": "Fujitsu Futro S720 slim"
}
```
**Семпл #54:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/legkiy-kompyuter-ID10qmSC.html",
  "title": "Легкий комп‘ютер"
}
```
**Семпл #55:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/prodam-groviy-pk-gtx-1660s-xeon-e5-2670-v3-komplektom-abo-okremo-ID10Z3jn.html",
  "title": "Продам ігровий ПК (GTX 1660S / Xeon E5-2670 v3) – комплектом або окремо"
}
```
**Семпл #56:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/raspberry-pi-4b-4g-ID10Z3io.html",
  "title": "Raspberry pi 4b 4g"
}
```
**Семпл #57:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/kompyuter-sistemniy-blok-fujitsu-p720-core-i3-4160-3-6-ddr3-8gb-intel-hd-graphics-4400-ID10eI5t.html",
  "title": "Комп'ютер системний блок Fujitsu P720 Core i3-4160 3,6  DDR3 8Gb  Intel HD Graphics 4400"
}
```
**Семпл #58:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/sistemniy-blok-dell-optiplex-3040-micro-usff-core-i3-6100t-8-gb-128-gb-ssd-kompyuter-nettop-ID10nZuS.html",
  "title": "Системний блок Dell OptiPlex 3040 Micro USFF Core i3-6100T 8 GB  128 GB SSD  комп'ютер неттоп"
}
```
**Семпл #59:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/kompyuter-sistemnik-amd-athlon-5000-320gb-hdd-4gb-nvidia-geforce-gt240-horoshaya-tsena-ID10NzlQ.html",
  "title": "Компьютер системник AMD Athlon 5000+ / 320Gb HDD / 4Gb / Nvidia Geforce GT240 / хорошая цена"
}
```
**Семпл #60:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/pc-kompyuter-monitor-samsung-IDPj3si.html",
  "title": "Pc компьютер+монитор Samsung"
}
```
**Семпл #61:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/kompyuter-pk-razen-7-5700x-rx5600xt2060-16gb-ddr4-ID10Vpn1.html",
  "title": "компьютер ПК Razen 7 5700x RX5600XT(2060) 16GB DDR4"
}
```
**Семпл #62:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/kompyuter-lenovo-thinkcentre-m720s-sff-i5-8400-8gb-ddr4-nvme-256gb-IDXlb2O.html",
  "title": "Комп'ютер Lenovo ThinkCentre M720s SFF i5-8400 8Gb DDR4 NVMe 256Gb"
}
```
**Семпл #63:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/mnkompyuteri-dell-sff-s1151-s1200-sistemn-bloki-i5-i7-pk-ssd120-250-IDZnIvr.html",
  "title": "МІНІКомп'ютери DELL SFF s1151/s1200 Системні блоки i5/i7 ПК SSD120/250"
}
```
**Семпл #64:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/pk-u-komplekt-z-montorom-ta-aksesuarami-ID10f0cI.html",
  "title": "ПК у комплекті з монітором та аксесуарами"
}
```
**Семпл #65:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/lodovichok-rtx-5080-16gb-i5-14400f-ddr4-32gb-m-2-ssd-1tb-groviy-kompyuter-pk-dlya-gor-geymerskiy-igrovoy-kompyuter-ID10FUxS.html",
  "title": "Льодовичок! RTX 5080 16GB+i5-14400F+DDR4 32GB+M.2 SSD 1TB –  Ігровий комп'ютер ПК для ігор геймерський игровой компьютер"
}
```
**Семпл #66:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/pk-na-i5-ta-rx-380-IDZE8ML.html",
  "title": "Пк на i5 та rx 380"
}
```
**Семпл #67:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/prodam-sistemnyy-blok-IDVffpa.html",
  "title": "Продам системный блок"
}
```
**Семпл #68:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/moschnyy-igrovoy-pk-rabochaya-stantsiya-ryzen-7-5800x-rx-6600-32gb-sostoyanie-novogo-tsena-dogovornaya-ID10YmoU.html",
  "title": "Мощный игровой ПК / Рабочая станция (Ryzen 7 5800X + RX 6600 + 32GB) (Состояние нового) Цена договорная"
}
```
**Семпл #69:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/potuzhniy-nastlniy-kompyuter-dlya-gor-ID10qmGw.html",
  "title": "Потужний настільний комп'ютер для ігор"
}
```
**Семпл #70:**
```json
{
  "reason": "banned_word_without_pc_indicator: ssd",
  "title": "Xeon e2186m(i7 8700) 8ddr4 ssd m2 256gb p106-100 6gb"
}
```
**Семпл #71:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/kompyuter-sistemniy-blok-montor-soket-775-IDZZpfy.html",
  "title": "Комп'ютер: системний блок, монітор, сокет 775."
}
```
**Семпл #72:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/rgb-terminator-gtx-1080-ti-16-yader-32gb-ozu-ssd-480gb-groviy-pk-kompyuter-dlya-gor-IDG0HQ4.html",
  "title": "RGB Терминатор! GTX 1080 Ti+16 ядер+32GB ОЗУ+SSD 480GB – ігровий ПК комп'ютер для ігор"
}
```
**Семпл #73:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/potuzhniy-groviy-pk-komplekt-am5-ddr5-ryzen-8400f-rx-6750-xt-12gb-montor-2k-klavatura-garantya-ID10YkzT.html",
  "title": "Потужний ігровий ПК Комплект (AM5, DDR5): Ryzen 8400F + RX 6750 XT 12GB + Монітор 2К + Клавіатура (Гарантія)"
}
```
**Семпл #74:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/kompyuter-sistemniy-blok-ID10YGtY.html",
  "title": "Комп'ютер системний блок"
}
```
**Семпл #75:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/groviy-pk-5060-ti-16gb-32-ddr5-asgard-muninn-a75f-32-s10-56t16-10027-IDZPYBr.html",
  "title": "Ігровий ПК 5060 ti 16GB/32 DDR5/ASGARD Muninn (A75F.32.S10.56T16.10027)"
}
```
**Семпл #76:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/igrovoy-kompyuter-ID10Z2YO.html",
  "title": "Игровой компьютер"
}
```
**Семпл #77:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/pk-dlya-raboty-i-videoigr-IDGrvks.html",
  "title": "ПК для работы и видеоигр"
}
```
**Семпл #78:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/monoblok-hp-proone-400-g2-aio-20-ID10PMON.html",
  "title": "Моноблок HP ProOne 400 G2 AiO 20\""
}
```
**Семпл #79:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/groviy-pk-intel-core-i5-6500-16gb-ddr4-nvidia-gtx-1070-ti-8gb-ssd-500gb-w11-ID10Se2c.html",
  "title": "Ігровий ПК Intel Core i5-6500 | 16GB DDR4 | Nvidia GTX 1070 Ti 8GB | SSD 500GB | W11"
}
```
**Семпл #80:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/pkmaterinka-ozu-zhestkiy-disk-protsessor-blok-pitaniya-korpus-IDZE8t1.html",
  "title": "пк(материнка, озу, жёсткий диск, процессор, блок питания, корпус"
}
```
**Семпл #81:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/igrovoy-kompyuter-ryzen-5-8400f-16gb-ddr5-rx-5700-xt-ID10VUKG.html",
  "title": "Игровой компьютер ryzen 5 8400f, 16gb ddr5, rx 5700 xt."
}
```
**Семпл #82:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/sistemniy-blok-prodesk-400g5-mini-i5-9500t6yader-8gb-ssd256-IDX0XM6.html",
  "title": "Системний блок ProDesk 400G5 mini i5-9500T(6ядер)/8gb/ssd256"
}
```
**Семпл #83:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/pk-sborka-komyuter-ID10Nz0u.html",
  "title": "ПК сборка, Комʼютер"
}
```
**Семпл #84:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/moschnyy-igrovoy-rabochiy-pk-ryzen9-5900x-rtx3080-32gb-ID10yXVe.html",
  "title": "Мощный игровой / рабочий ПК/Ryzen9/5900x/Rtx3080/32gb"
}
```
**Семпл #85:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/sistemniy-blok-i5-4590-8gb-ram-128gb-ssd-1tb-hdd-gtx1060-6gb-IDWt8M3.html",
  "title": "Системний блок i5-4590 / 8Gb RAM / 128Gb SSD / 1Tb HDD / GTX1060 6Gb"
}
```
**Семпл #86:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/prodam-kompyuter-koplektom-ID10oWxt.html",
  "title": "Продам Компютер Коплектом"
}
```
**Семпл #87:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/groviy-pk-z-montorom-IDXYdKc.html",
  "title": "Ігровий ПК з монітором"
}
```
**Семпл #88:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/i7-2600k-i-i5-3770-soket-1155-ID10Z2Nh.html",
  "title": "I7 2600k и i5 3770 сокет 1155"
}
```
**Семпл #89:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/moschnyy-igrovoy-pk-idealnoe-sostoyanie-ID10Z2L8.html",
  "title": "Мощный игровой ПК / Идеальное состояние"
}
```
**Семпл #90:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/moschnyy-igrovoy-pk-12600kf-rtx-5060-32gb-ddr5-ID10VMOw.html",
  "title": "Мощный игровой ПК 12600kf rtx 5060 32gb ddr5"
}
```
**Семпл #91:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/sistemnyy-blok-IDRHpkl.html",
  "title": "Системный блок"
}
```
**Семпл #92:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/kompyuter-mishka-klavatura-ID10qmbc.html",
  "title": "Компʼютер + мишка + клавіатура"
}
```
**Семпл #93:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/pk-i5-8gb-ssd-zbrka-2026-pk-dlya-ofsu-personalniy-kompyuter-IDZVAYw.html",
  "title": "ПК i5 | 8GB | SSD | Збірка 2026 ПК для офісу персональний компʼютер"
}
```
**Семпл #94:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/groviy-pk-xeon-e3-1230-v2-gtx-1060-6gb-ozu-16gb-ddr3-ssd-480gb-ID10Z2z7.html",
  "title": "ІГРОВИЙ ПК: Xeon E3 1230 V2, GTX 1060 6gb, ОЗУ 16gb DDR3, SSD 480gb"
}
```
**Семпл #95:**
```json
{
  "reason": "starts_with_banned_word: відеокарта",
  "title": "Відеокарта MSI GeForce GTX 1070 Ti GAMING X 8G GDDR5 256bit"
}
```
**Семпл #96:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/noviy-mayner-antminer-l9-15-gh-amlogic-miner-asic-bitmain-garantya-IDX9tjm.html",
  "title": "Новий Майнер! Antminer L9 15 Gh Amlogic miner Asic Bitmain + Гарантія"
}
```
**Семпл #97:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/pk-dlya-roboti-ta-navchannyaya-ID10XVVN.html",
  "title": "ПК для роботи та навчанняя"
}
```
**Семпл #98:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/groviy-pk-ryzen-7-3700x-rtx-2060-6gb-16gb-ram-ssd-240gb-hdd-1tb-ID10Nigg.html",
  "title": "Ігровий ПК | Ryzen 7 3700X | RTX 2060 6GB | 16GB RAM | SSD 240GB + HDD 1TB"
}
```
**Семпл #99:**
```json
{
  "reason": "duplicate_url_already_in_db",
  "url": "https://www.olx.ua/d/uk/obyavlenie/sistemniy-blok-ryzen-3-1200-8-gb-gtx-650-ti-ssd-128-gb-ID10JnKG.html",
  "title": "Системний блок Ryzen 3 1200, 8 ГБ, GTX 650 Ti, SSD 128 ГБ"
}
```
**Семпл #100:**
```json
{
  "reason": "banned_word_without_pc_indicator: hdd",
  "title": "Lenovo ThinkCentre • E8400 • 4GB DDR3 • HDD 200GB • вбудоване відео"
}
```

### 🔹 Валідовані оголошення ПК (пройшли перевірку is_real_pc) (Показано 34 з max 100):
**Семпл #1:**
```json
{
  "ad_id": 893404805,
  "title": "Продам ПК, 2 ноутбука.  AMD Ryzen 3 2200g, 8 GB ОЗУ, Ноутбук ASUS K53T, ноутбук, LENOVO B50-30",
  "status": "passed_is_real_pc"
}
```
**Семпл #2:**
```json
{
  "ad_id": 916046872,
  "title": "Игровой Компьютер | Ддр 3 32 Gb | GTX 980 | SSD |",
  "status": "passed_is_real_pc"
}
```
**Семпл #3:**
```json
{
  "ad_id": 930686688,
  "title": "iMac 27 Mid 2011 A1312 i7 / 8GB / 1TB / Radeon 6970M",
  "status": "passed_is_real_pc"
}
```
**Семпл #4:**
```json
{
  "ad_id": 902454333,
  "title": "Компютер Ryzen 5 5500 , GTX 1060(3gb), 16gb RAM",
  "status": "passed_is_real_pc"
}
```
**Семпл #5:**
```json
{
  "ad_id": 929456110,
  "title": "Игровой ПК RX 6700 XT, Ryzen5 5600x, 16gb, SSD 500gb",
  "status": "passed_is_real_pc"
}
```
**Семпл #6:**
```json
{
  "ad_id": 930686283,
  "title": "компютер ний комплект asus p5kpl/epu",
  "status": "passed_is_real_pc"
}
```
**Семпл #7:**
```json
{
  "ad_id": 930686206,
  "title": "Міні-ПК Bosgame P1 / Cybergeek Nano L1 / Ryzen 7 5700U / 16-32GB / 512GB-1TB",
  "status": "passed_is_real_pc"
}
```
**Семпл #8:**
```json
{
  "ad_id": 902453892,
  "title": "Корпус Чехол Raspberry Pi 3 Малинка",
  "status": "passed_is_real_pc"
}
```
**Семпл #9:**
```json
{
  "ad_id": 930686076,
  "title": "Продам Ігровий компʼютер",
  "status": "passed_is_real_pc"
}
```
**Семпл #10:**
```json
{
  "ad_id": 863288838,
  "title": "Продаж ігрового ПК (Б/у)",
  "status": "passed_is_real_pc"
}
```
**Семпл #11:**
```json
{
  "ad_id": 930521400,
  "title": "Игровой ПК Ryzen 7 5700X / RTX 3070 Ti STRIX / 64GB RGB / 2.5TB SSD | Возможен комплект",
  "status": "passed_is_real_pc"
}
```
**Семпл #12:**
```json
{
  "ad_id": 858673619,
  "title": "Гарантия! Ryzen 5 DDR4 GTX1070   купить игровой пк компьютер",
  "status": "passed_is_real_pc"
}
```
**Семпл #13:**
```json
{
  "ad_id": 925303862,
  "title": "Старый рабочий ПК для ретро-игр, Windows XP, HDD 120 ГБ. Продаётся как есть.",
  "status": "passed_is_real_pc"
}
```
**Семпл #14:**
```json
{
  "ad_id": 930685530,
  "title": "Продам системный блок dell 790",
  "status": "passed_is_real_pc"
}
```
**Семпл #15:**
```json
{
  "ad_id": 928243830,
  "title": "Системний блок ПК Dell Inspiron 3020s SFF Intel Core i5-13400\\16GB RAM\\256Gb SSD",
  "status": "passed_is_real_pc"
}
```
**Семпл #16:**
```json
{
  "ad_id": 924089462,
  "title": "Продам ігровий компютер з монітором б/в",
  "status": "passed_is_real_pc"
}
```
**Семпл #17:**
```json
{
  "ad_id": 929370009,
  "title": "Сист.блок Ryzen 3, 8gb DDR4, ssd 120 gb",
  "status": "passed_is_real_pc"
}
```
**Семпл #18:**
```json
{
  "ad_id": 899460575,
  "title": "Asik L9 - Майнер Bitmain Antminer L9 Hyd-27G 2U 6900$ (Найнижча ціна)",
  "status": "passed_is_real_pc"
}
```
**Семпл #19:**
```json
{
  "ad_id": 920486827,
  "title": "Акція! Fujitsu Esprimo P957 i5-6500 — Готовий до апгрейду: NVMe + багато слотів + Німеччина",
  "status": "passed_is_real_pc"
}
```
**Семпл #20:**
```json
{
  "ad_id": 917004334,
  "title": "НАЯВНІСТЬ! NEW Asic Avalon Q 90 Th, Майнер, Асік + Гарантія, 7007",
  "status": "passed_is_real_pc"
}
```
**Семпл #21:**
```json
{
  "ad_id": 888507283,
  "title": "РОЗПРОДАЖ Комп’ютерів Dell Optiplex 7010 SFF ПК i5-3 8GB 240 SSD ОПТ‼️",
  "status": "passed_is_real_pc"
}
```
**Семпл #22:**
```json
{
  "ad_id": 929264066,
  "title": "ІГРОВИЙ ПК!! RTX 3080, Ryzen 5 5500, ОЗУ DDR4 16gb, SSD 512gb",
  "status": "passed_is_real_pc"
}
```
**Семпл #23:**
```json
{
  "ad_id": 930585636,
  "title": "Компьютер AMD Ryzen 7 9800X3D|RTX 5070 TI|32 GB DDR5 Cl 28|SSD 2TB|850W| NEW!",
  "status": "passed_is_real_pc"
}
```
**Семпл #24:**
```json
{
  "ad_id": 925809556,
  "title": "DELL INSPIRON 3020  Intel core I5-13400/256GB/8GB",
  "status": "passed_is_real_pc"
}
```
**Семпл #25:**
```json
{
  "ad_id": 927324141,
  "title": "Продам топовый игровой компьютер на максималках (Ryzen 7 8700, Radeon 6800XT 16GB)",
  "status": "passed_is_real_pc"
}
```
**Семпл #26:**
```json
{
  "ad_id": 917005708,
  "title": "Під замовлення! ASIC Antminer S21+ Hydro 395 Th, асік, Майнер Bitmain",
  "status": "passed_is_real_pc"
}
```
**Семпл #27:**
```json
{
  "ad_id": 923059407,
  "title": "Компютер:8GB Відеокарта /I7 процесор потужний комплект пк з монітором",
  "status": "passed_is_real_pc"
}
```
**Семпл #28:**
```json
{
  "ad_id": 930470864,
  "title": "Продам игровой ПК",
  "status": "passed_is_real_pc"
}
```
**Семпл #29:**
```json
{
  "ad_id": 928880459,
  "title": "MacBook pro 2017 i5",
  "status": "passed_is_real_pc"
}
```
**Семпл #30:**
```json
{
  "ad_id": 882501734,
  "title": "Micro міні Комп’ютер Dell Optiplex 3060 mini ПК i3 i5 i7 s1151 DDR4SSD",
  "status": "passed_is_real_pc"
}
```
**Семпл #31:**
```json
{
  "ad_id": 917018230,
  "title": "80шт.ПК Lenovo V520S SFF s1151 (Core i5-7500/8GB/SSD256GB ОПТ КИЇВ)‼️",
  "status": "passed_is_real_pc"
}
```
**Семпл #32:**
```json
{
  "ad_id": 930285721,
  "title": "Mac mini m1 8/512",
  "status": "passed_is_real_pc"
}
```
**Семпл #33:**
```json
{
  "ad_id": 930475469,
  "title": "Продам игровой пк",
  "status": "passed_is_real_pc"
}
```
**Семпл #34:**
```json
{
  "ad_id": 924977907,
  "title": "Моноблок HP ProOne 400 G2/i5-6500T/8GB/256GB/FHD/20\"/IPS/Бюджетний Зручний Компактний ОПТ Роздріб По перерахунку",
  "status": "passed_is_real_pc"
}
```

============================================================

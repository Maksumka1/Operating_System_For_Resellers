# 🐛 ДЕБАГ-ЗВІТ АНАЛІЗУ РИНКУ ТА КОНКУРЕНТІВ
**Дата та час запуску:** 2026-07-31 21:32:21
**Тривалість виконання:** 27.15 сек

## 📌 1. Задача та мета коду
Основна мета: автоматизована оцінка ринкової вартості та вигоди оголошень в Supabase.
1. Викачування активних лотів комплектуючих та готових ПК.
2. Зіставлення з базою чесних цін `component_prices` або розрахунок медіани.
3. Кластеризація ПК за зв'язкою `CPU + GPU` та аналіз цін конкурентів.
4. Обчислення `deal_status`, `saving_percent`, `saving_uah` та пачкове оновлення в DB.

## 📊 2. Загальна статистика вхідних даних та відсіювання
### ⚙️ Категорія: Hardware_Input
- **Завантажено записів з component_prices:** 264
- **Отримано активних оголошень комплектуючих:** 548

### ⚙️ Категорія: Hardware_Pipeline
- **Згруповано унікальних моделей комплектуючих:** 183
- **Відсіяно if (fair_price <= 0):** 38

### ⚙️ Категорія: Hardware_Price_Calc
- **Відсіяно if (менше 3 валідних цін > 100 грн):** 122

### ⚙️ Категорія: Updates_DB
- **Успішно оновлено лотів у базі:** 703
- **Помилки оновлення (Exception): <ConnectionTerminated error_code:1, last:** 4
- **Помилки оновлення (Exception): [WinError 10035] A non-blocking socket o:** 25

### ⚙️ Категорія: PC_Input
- **Отримано активних ПК з DB:** 677

### ⚙️ Категорія: PC_Pipeline
- **Відсіяно if ('unknown' у назвах GPU/CPU):** 455
- **Сформовано унікальних збірок (CPU+GPU):** 199

## 🔄 3. Детальні приклади даних (по 20 семплів на етап)
### 🔹 Вхідні цінові орієнтири з `component_prices` (Показано 20 з max 20):
**Семпл #1:**
```json
{
  "component_name": "ryzen_5_7500f",
  "price": 4490
}
```
**Семпл #2:**
```json
{
  "component_name": "z170",
  "price": 2100
}
```
**Семпл #3:**
```json
{
  "component_name": "b650",
  "price": 4000
}
```
**Семпл #4:**
```json
{
  "component_name": "hdd_500gb",
  "price": 450
}
```
**Семпл #5:**
```json
{
  "component_name": "h110",
  "price": 1000
}
```
**Семпл #6:**
```json
{
  "component_name": "rtx_3050",
  "price": 7900
}
```
**Семпл #7:**
```json
{
  "component_name": "gtx_1080",
  "price": 8000
}
```
**Семпл #8:**
```json
{
  "component_name": "rx_570",
  "price": 1375
}
```
**Семпл #9:**
```json
{
  "component_name": "ssd_500gb",
  "price": 2800
}
```
**Семпл #10:**
```json
{
  "component_name": "ssd_1tb",
  "price": 4500
}
```
**Семпл #11:**
```json
{
  "component_name": "450w",
  "price": 750
}
```
**Семпл #12:**
```json
{
  "component_name": "gtx_1660_super",
  "price": 5700
}
```
**Семпл #13:**
```json
{
  "component_name": "i5_3470",
  "price": 425
}
```
**Семпл #14:**
```json
{
  "component_name": "rtx_3060",
  "price": 13999
}
```
**Семпл #15:**
```json
{
  "component_name": "ryzen_7_5700",
  "price": 6900
}
```
**Семпл #16:**
```json
{
  "component_name": "ssd_512gb",
  "price": 2800
}
```
**Семпл #17:**
```json
{
  "component_name": "1000w",
  "price": 4000
}
```
**Семпл #18:**
```json
{
  "component_name": "rtx_3070",
  "price": 12500
}
```
**Семпл #19:**
```json
{
  "component_name": "hdd_2tb",
  "price": 2000
}
```
**Семпл #20:**
```json
{
  "component_name": "gtx_1080_ti",
  "price": 8750
}
```

### 🔹 Вхідні оголошення комплектуючих з `ads` (Показано 20 з max 20):
**Семпл #1:**
```json
{
  "id": 832,
  "component_name": "i7_6700",
  "price": 1800
}
```
**Семпл #2:**
```json
{
  "id": 4297,
  "component_name": "gtx_1660_super",
  "price": 5700
}
```
**Семпл #3:**
```json
{
  "id": 514,
  "component_name": "1000w",
  "price": 7700
}
```
**Семпл #4:**
```json
{
  "id": 371,
  "component_name": "i7_10700kf",
  "price": 7500
}
```
**Семпл #5:**
```json
{
  "id": 6812,
  "component_name": "x870",
  "price": 9402
}
```
**Семпл #6:**
```json
{
  "id": 6698,
  "component_name": "i5_8400",
  "price": 3800
}
```
**Семпл #7:**
```json
{
  "id": 6673,
  "component_name": "rtx_3070",
  "price": 10735
}
```
**Семпл #8:**
```json
{
  "id": 237,
  "component_name": "rtx_2060_super",
  "price": 8750
}
```
**Семпл #9:**
```json
{
  "id": 439,
  "component_name": "h110",
  "price": 800
}
```
**Семпл #10:**
```json
{
  "id": 328,
  "component_name": "ryzen_7_7800x3d",
  "price": 14300
}
```
**Семпл #11:**
```json
{
  "id": 506,
  "component_name": "h310",
  "price": 3850
}
```
**Семпл #12:**
```json
{
  "id": 4478,
  "component_name": "hdd_2tb",
  "price": 3000
}
```
**Семпл #13:**
```json
{
  "id": 238,
  "component_name": "rtx_3050",
  "price": 7999
}
```
**Семпл #14:**
```json
{
  "id": 559,
  "component_name": "1050w",
  "price": 4600
}
```
**Семпл #15:**
```json
{
  "id": 6597,
  "component_name": "gtx_1080_ti",
  "price": 8750
}
```
**Семпл #16:**
```json
{
  "id": 5908,
  "component_name": "gtx_1050_ti",
  "price": 2800
}
```
**Семпл #17:**
```json
{
  "id": 6264,
  "component_name": "rtx_3060_ti",
  "price": 12000
}
```
**Семпл #18:**
```json
{
  "id": 6713,
  "component_name": "i7_3770k",
  "price": 750
}
```
**Семпл #19:**
```json
{
  "id": 389,
  "component_name": "i5_9500t",
  "price": 1899
}
```
**Семпл #20:**
```json
{
  "id": 203,
  "component_name": "rx_470",
  "price": 1600
}
```

### 🔹 Проміжні обчислення та фінальний payload для комплектуючих (Показано 20 з max 20):
**Семпл #1:**
```json
{
  "component_model": "i7_6700",
  "total_listings_in_group": 2,
  "calculated_market_price": 0,
  "fair_price_source": "component_prices",
  "input_ad": {
    "id": 832,
    "seller_price": 1800
  },
  "output_payload_for_db": {
    "competitor_price": 1800,
    "estimated_fair_price": 1800,
    "saving_uah": 0,
    "saving_percent": 0,
    "deal_status": "regular"
  }
}
```
**Семпл #2:**
```json
{
  "component_model": "i7_6700",
  "total_listings_in_group": 2,
  "calculated_market_price": 0,
  "fair_price_source": "component_prices",
  "input_ad": {
    "id": 15839,
    "seller_price": 2100
  },
  "output_payload_for_db": {
    "competitor_price": 1800,
    "estimated_fair_price": 1800,
    "saving_uah": -300,
    "saving_percent": -17,
    "deal_status": "❌ OVERPRICED"
  }
}
```
**Семпл #3:**
```json
{
  "component_model": "gtx_1660_super",
  "total_listings_in_group": 3,
  "calculated_market_price": 5700,
  "fair_price_source": "component_prices",
  "input_ad": {
    "id": 4297,
    "seller_price": 5700
  },
  "output_payload_for_db": {
    "competitor_price": 5700,
    "estimated_fair_price": 6500,
    "saving_uah": 800,
    "saving_percent": 12,
    "deal_status": "⭐ GOOD DEAL"
  }
}
```
**Семпл #4:**
```json
{
  "component_model": "gtx_1660_super",
  "total_listings_in_group": 3,
  "calculated_market_price": 5700,
  "fair_price_source": "component_prices",
  "input_ad": {
    "id": 256,
    "seller_price": 6500
  },
  "output_payload_for_db": {
    "competitor_price": 5700,
    "estimated_fair_price": 6500,
    "saving_uah": 0,
    "saving_percent": 0,
    "deal_status": "regular"
  }
}
```
**Семпл #5:**
```json
{
  "component_model": "gtx_1660_super",
  "total_listings_in_group": 3,
  "calculated_market_price": 5700,
  "fair_price_source": "component_prices",
  "input_ad": {
    "id": 9684,
    "seller_price": 5500
  },
  "output_payload_for_db": {
    "competitor_price": 5700,
    "estimated_fair_price": 6500,
    "saving_uah": 1000,
    "saving_percent": 15,
    "deal_status": "⭐ GOOD DEAL"
  }
}
```
**Семпл #6:**
```json
{
  "component_model": "1000w",
  "total_listings_in_group": 6,
  "calculated_market_price": 5150,
  "fair_price_source": "component_prices",
  "input_ad": {
    "id": 514,
    "seller_price": 7700
  },
  "output_payload_for_db": {
    "competitor_price": 5150,
    "estimated_fair_price": 3200,
    "saving_uah": -4500,
    "saving_percent": -100,
    "deal_status": "❌ OVERPRICED"
  }
}
```
**Семпл #7:**
```json
{
  "component_model": "1000w",
  "total_listings_in_group": 6,
  "calculated_market_price": 5150,
  "fair_price_source": "component_prices",
  "input_ad": {
    "id": 6865,
    "seller_price": 5500
  },
  "output_payload_for_db": {
    "competitor_price": 5150,
    "estimated_fair_price": 3200,
    "saving_uah": -2300,
    "saving_percent": -72,
    "deal_status": "❌ OVERPRICED"
  }
}
```
**Семпл #8:**
```json
{
  "component_model": "1000w",
  "total_listings_in_group": 6,
  "calculated_market_price": 5150,
  "fair_price_source": "component_prices",
  "input_ad": {
    "id": 19018,
    "seller_price": 6400
  },
  "output_payload_for_db": {
    "competitor_price": 5150,
    "estimated_fair_price": 3200,
    "saving_uah": -3200,
    "saving_percent": -100,
    "deal_status": "❌ OVERPRICED"
  }
}
```
**Семпл #9:**
```json
{
  "component_model": "1000w",
  "total_listings_in_group": 6,
  "calculated_market_price": 5150,
  "fair_price_source": "component_prices",
  "input_ad": {
    "id": 9443,
    "seller_price": 4800
  },
  "output_payload_for_db": {
    "competitor_price": 5150,
    "estimated_fair_price": 3200,
    "saving_uah": -1600,
    "saving_percent": -50,
    "deal_status": "❌ OVERPRICED"
  }
}
```
**Семпл #10:**
```json
{
  "component_model": "1000w",
  "total_listings_in_group": 6,
  "calculated_market_price": 5150,
  "fair_price_source": "component_prices",
  "input_ad": {
    "id": 19013,
    "seller_price": 4000
  },
  "output_payload_for_db": {
    "competitor_price": 5150,
    "estimated_fair_price": 3200,
    "saving_uah": -800,
    "saving_percent": -25,
    "deal_status": "❌ OVERPRICED"
  }
}
```
**Семпл #11:**
```json
{
  "component_model": "1000w",
  "total_listings_in_group": 6,
  "calculated_market_price": 5150,
  "fair_price_source": "component_prices",
  "input_ad": {
    "id": 571,
    "seller_price": 3200
  },
  "output_payload_for_db": {
    "competitor_price": 5150,
    "estimated_fair_price": 3200,
    "saving_uah": 0,
    "saving_percent": 0,
    "deal_status": "regular"
  }
}
```
**Семпл #12:**
```json
{
  "component_model": "i7_10700kf",
  "total_listings_in_group": 1,
  "calculated_market_price": 0,
  "fair_price_source": "component_prices",
  "input_ad": {
    "id": 371,
    "seller_price": 7500
  },
  "output_payload_for_db": {
    "competitor_price": 7500,
    "estimated_fair_price": 7500,
    "saving_uah": 0,
    "saving_percent": 0,
    "deal_status": "regular"
  }
}
```
**Семпл #13:**
```json
{
  "component_model": "rtx_3070",
  "total_listings_in_group": 7,
  "calculated_market_price": 13000,
  "fair_price_source": "component_prices",
  "input_ad": {
    "id": 6673,
    "seller_price": 10735
  },
  "output_payload_for_db": {
    "competitor_price": 13000,
    "estimated_fair_price": 14000,
    "saving_uah": 3265,
    "saving_percent": 23,
    "deal_status": "🔥 SUPER DEAL"
  }
}
```
**Семпл #14:**
```json
{
  "component_model": "rtx_3070",
  "total_listings_in_group": 7,
  "calculated_market_price": 13000,
  "fair_price_source": "component_prices",
  "input_ad": {
    "id": 6677,
    "seller_price": 12500
  },
  "output_payload_for_db": {
    "competitor_price": 13000,
    "estimated_fair_price": 14000,
    "saving_uah": 1500,
    "saving_percent": 11,
    "deal_status": "⭐ GOOD DEAL"
  }
}
```
**Семпл #15:**
```json
{
  "component_model": "rtx_3070",
  "total_listings_in_group": 7,
  "calculated_market_price": 13000,
  "fair_price_source": "component_prices",
  "input_ad": {
    "id": 258,
    "seller_price": 14000
  },
  "output_payload_for_db": {
    "competitor_price": 13000,
    "estimated_fair_price": 14000,
    "saving_uah": 0,
    "saving_percent": 0,
    "deal_status": "regular"
  }
}
```
**Семпл #16:**
```json
{
  "component_model": "rtx_3070",
  "total_listings_in_group": 7,
  "calculated_market_price": 13000,
  "fair_price_source": "component_prices",
  "input_ad": {
    "id": 5614,
    "seller_price": 15000
  },
  "output_payload_for_db": {
    "competitor_price": 13000,
    "estimated_fair_price": 14000,
    "saving_uah": -1000,
    "saving_percent": -7,
    "deal_status": "regular"
  }
}
```
**Семпл #17:**
```json
{
  "component_model": "rtx_3070",
  "total_listings_in_group": 7,
  "calculated_market_price": 13000,
  "fair_price_source": "component_prices",
  "input_ad": {
    "id": 201,
    "seller_price": 13000
  },
  "output_payload_for_db": {
    "competitor_price": 13000,
    "estimated_fair_price": 14000,
    "saving_uah": 1000,
    "saving_percent": 7,
    "deal_status": "regular"
  }
}
```
**Семпл #18:**
```json
{
  "component_model": "rtx_3070",
  "total_listings_in_group": 7,
  "calculated_market_price": 13000,
  "fair_price_source": "component_prices",
  "input_ad": {
    "id": 6689,
    "seller_price": 12500
  },
  "output_payload_for_db": {
    "competitor_price": 13000,
    "estimated_fair_price": 14000,
    "saving_uah": 1500,
    "saving_percent": 11,
    "deal_status": "⭐ GOOD DEAL"
  }
}
```
**Семпл #19:**
```json
{
  "component_model": "rtx_3070",
  "total_listings_in_group": 7,
  "calculated_market_price": 13000,
  "fair_price_source": "component_prices",
  "input_ad": {
    "id": 6688,
    "seller_price": 14750
  },
  "output_payload_for_db": {
    "competitor_price": 13000,
    "estimated_fair_price": 14000,
    "saving_uah": -750,
    "saving_percent": -5,
    "deal_status": "regular"
  }
}
```
**Семпл #20:**
```json
{
  "component_model": "rtx_2060_super",
  "total_listings_in_group": 2,
  "calculated_market_price": 0,
  "fair_price_source": "component_prices",
  "input_ad": {
    "id": 237,
    "seller_price": 8750
  },
  "output_payload_for_db": {
    "competitor_price": 8750,
    "estimated_fair_price": 8750,
    "saving_uah": 0,
    "saving_percent": 0,
    "deal_status": "regular"
  }
}
```

### 🔹 Вхідні оголошення ПК з `ads` (Показано 20 з max 20):
**Семпл #1:**
```json
{
  "id": 3958,
  "gpu_detected": "Unknown GPU",
  "cpu_detected": "Unknown CPU",
  "price": 35000
}
```
**Семпл #2:**
```json
{
  "id": 3326,
  "gpu_detected": "Unknown GPU",
  "cpu_detected": "Unknown CPU",
  "price": 3100
}
```
**Семпл #3:**
```json
{
  "id": 1057,
  "gpu_detected": "Unknown GPU",
  "cpu_detected": "Unknown CPU",
  "price": 6000
}
```
**Семпл #4:**
```json
{
  "id": 1386,
  "gpu_detected": "Unknown GPU",
  "cpu_detected": "Unknown CPU",
  "price": 3000
}
```
**Семпл #5:**
```json
{
  "id": 24,
  "gpu_detected": "Unknown GPU",
  "cpu_detected": "i5_3470",
  "price": 3200
}
```
**Семпл #6:**
```json
{
  "id": 9473,
  "gpu_detected": "Unknown GPU",
  "cpu_detected": "Unknown CPU",
  "price": 45499
}
```
**Семпл #7:**
```json
{
  "id": 25,
  "gpu_detected": "Unknown GPU",
  "cpu_detected": "Unknown CPU",
  "price": 2800
}
```
**Семпл #8:**
```json
{
  "id": 1364,
  "gpu_detected": "Unknown GPU",
  "cpu_detected": "Unknown CPU",
  "price": 50050
}
```
**Семпл #9:**
```json
{
  "id": 9475,
  "gpu_detected": "Unknown GPU",
  "cpu_detected": "Unknown CPU",
  "price": 41999
}
```
**Семпл #10:**
```json
{
  "id": 1069,
  "gpu_detected": "Unknown GPU",
  "cpu_detected": "i5_10500t",
  "price": 13400
}
```
**Семпл #11:**
```json
{
  "id": 1212,
  "gpu_detected": "Unknown GPU",
  "cpu_detected": "Unknown CPU",
  "price": 35000
}
```
**Семпл #12:**
```json
{
  "id": 2826,
  "gpu_detected": "Unknown GPU",
  "cpu_detected": "ryzen_3_2200g",
  "price": 1800
}
```
**Семпл #13:**
```json
{
  "id": 2925,
  "gpu_detected": "gtx_1660",
  "cpu_detected": "Unknown CPU",
  "price": 15500
}
```
**Семпл #14:**
```json
{
  "id": 19,
  "gpu_detected": "Unknown GPU",
  "cpu_detected": "Unknown CPU",
  "price": 2700
}
```
**Семпл #15:**
```json
{
  "id": 178,
  "gpu_detected": "Unknown GPU",
  "cpu_detected": "i5_8400",
  "price": 9200
}
```
**Семпл #16:**
```json
{
  "id": 49,
  "gpu_detected": "Unknown GPU",
  "cpu_detected": "i3_6100",
  "price": 6477
}
```
**Семпл #17:**
```json
{
  "id": 123,
  "gpu_detected": "Unknown GPU",
  "cpu_detected": "Unknown CPU",
  "price": 2500
}
```
**Семпл #18:**
```json
{
  "id": 1847,
  "gpu_detected": "Unknown GPU",
  "cpu_detected": "Unknown CPU",
  "price": 13000
}
```
**Семпл #19:**
```json
{
  "id": 5864,
  "gpu_detected": "Unknown GPU",
  "cpu_detected": "Unknown CPU",
  "price": 2500
}
```
**Семпл #20:**
```json
{
  "id": 1355,
  "gpu_detected": "Unknown GPU",
  "cpu_detected": "Unknown CPU",
  "price": 199000
}
```

### 🔹 Проміжні обчислення та фінальний payload для ПК (Показано 20 з max 20):
**Семпл #1:**
```json
{
  "build_key": "rx_570_ryzen_5_4500",
  "input_pc_ad": {
    "id": 6590,
    "price": 20000
  },
  "other_competitors_count": 0,
  "other_competitors_prices": [],
  "output_payload_for_db": {
    "competitor_price": 20000
  }
}
```
**Семпл #2:**
```json
{
  "build_key": "quadro_p2200_xeon_e3_1220",
  "input_pc_ad": {
    "id": 1665,
    "price": 4100
  },
  "other_competitors_count": 0,
  "other_competitors_prices": [],
  "output_payload_for_db": {
    "competitor_price": 4100
  }
}
```
**Семпл #3:**
```json
{
  "build_key": "gtx_1060_i5_7400",
  "input_pc_ad": {
    "id": 18747,
    "price": 25000
  },
  "other_competitors_count": 0,
  "other_competitors_prices": [],
  "output_payload_for_db": {
    "competitor_price": 25000
  }
}
```
**Семпл #4:**
```json
{
  "build_key": "gtx_1060_i5_7500",
  "input_pc_ad": {
    "id": 1219,
    "price": 13000
  },
  "other_competitors_count": 0,
  "other_competitors_prices": [],
  "output_payload_for_db": {
    "competitor_price": 13000
  }
}
```
**Семпл #5:**
```json
{
  "build_key": "gtx_1660_ti_ryzen_5_3600",
  "input_pc_ad": {
    "id": 1256,
    "price": 12800
  },
  "other_competitors_count": 4,
  "other_competitors_prices": [
    12750,
    12800,
    12750,
    12700
  ],
  "output_payload_for_db": {
    "competitor_price": 12750
  }
}
```
**Семпл #6:**
```json
{
  "build_key": "gtx_1660_ti_ryzen_5_3600",
  "input_pc_ad": {
    "id": 1301,
    "price": 12750
  },
  "other_competitors_count": 4,
  "other_competitors_prices": [
    12800,
    12800,
    12750,
    12700
  ],
  "output_payload_for_db": {
    "competitor_price": 12762
  }
}
```
**Семпл #7:**
```json
{
  "build_key": "gtx_1660_ti_ryzen_5_3600",
  "input_pc_ad": {
    "id": 2176,
    "price": 12800
  },
  "other_competitors_count": 4,
  "other_competitors_prices": [
    12800,
    12750,
    12750,
    12700
  ],
  "output_payload_for_db": {
    "competitor_price": 12750
  }
}
```
**Семпл #8:**
```json
{
  "build_key": "gtx_1660_ti_ryzen_5_3600",
  "input_pc_ad": {
    "id": 5546,
    "price": 12750
  },
  "other_competitors_count": 4,
  "other_competitors_prices": [
    12800,
    12750,
    12800,
    12700
  ],
  "output_payload_for_db": {
    "competitor_price": 12762
  }
}
```
**Семпл #9:**
```json
{
  "build_key": "gtx_1660_ti_ryzen_5_3600",
  "input_pc_ad": {
    "id": 6584,
    "price": 12700
  },
  "other_competitors_count": 4,
  "other_competitors_prices": [
    12800,
    12750,
    12800,
    12750
  ],
  "output_payload_for_db": {
    "competitor_price": 12775
  }
}
```
**Семпл #10:**
```json
{
  "build_key": "rtx_3070_i9_10900k",
  "input_pc_ad": {
    "id": 9523,
    "price": 44500
  },
  "other_competitors_count": 0,
  "other_competitors_prices": [],
  "output_payload_for_db": {
    "competitor_price": 44500
  }
}
```
**Семпл #11:**
```json
{
  "build_key": "rtx_3080_i5_14400f",
  "input_pc_ad": {
    "id": 9250,
    "price": 60700
  },
  "other_competitors_count": 0,
  "other_competitors_prices": [],
  "output_payload_for_db": {
    "competitor_price": 60700
  }
}
```
**Семпл #12:**
```json
{
  "build_key": "rtx_3080_ryzen_7_5700x",
  "input_pc_ad": {
    "id": 4124,
    "price": 52000
  },
  "other_competitors_count": 1,
  "other_competitors_prices": [
    50395
  ],
  "output_payload_for_db": {
    "competitor_price": 50395
  }
}
```
**Семпл #13:**
```json
{
  "build_key": "rtx_3080_ryzen_7_5700x",
  "input_pc_ad": {
    "id": 6454,
    "price": 50395
  },
  "other_competitors_count": 1,
  "other_competitors_prices": [
    52000
  ],
  "output_payload_for_db": {
    "competitor_price": 52000
  }
}
```
**Семпл #14:**
```json
{
  "build_key": "gtx_1650_i5_8400",
  "input_pc_ad": {
    "id": 1193,
    "price": 8000
  },
  "other_competitors_count": 0,
  "other_competitors_prices": [],
  "output_payload_for_db": {
    "competitor_price": 8000
  }
}
```
**Семпл #15:**
```json
{
  "build_key": "rtx_2070_super_ryzen_5_3600",
  "input_pc_ad": {
    "id": 20156,
    "price": 21300
  },
  "other_competitors_count": 0,
  "other_competitors_prices": [],
  "output_payload_for_db": {
    "competitor_price": 21300
  }
}
```
**Семпл #16:**
```json
{
  "build_key": "rx_470_xeon_e3_1270_v3",
  "input_pc_ad": {
    "id": 1673,
    "price": 6000
  },
  "other_competitors_count": 0,
  "other_competitors_prices": [],
  "output_payload_for_db": {
    "competitor_price": 6000
  }
}
```
**Семпл #17:**
```json
{
  "build_key": "gt_710_i5_7400",
  "input_pc_ad": {
    "id": 18715,
    "price": 4600
  },
  "other_competitors_count": 0,
  "other_competitors_prices": [],
  "output_payload_for_db": {
    "competitor_price": 4600
  }
}
```
**Семпл #18:**
```json
{
  "build_key": "gtx_1060_3gb_i5_4570",
  "input_pc_ad": {
    "id": 133,
    "price": 12499
  },
  "other_competitors_count": 0,
  "other_competitors_prices": [],
  "output_payload_for_db": {
    "competitor_price": 12499
  }
}
```
**Семпл #19:**
```json
{
  "build_key": "rx_570_i3_10100f",
  "input_pc_ad": {
    "id": 1723,
    "price": 18000
  },
  "other_competitors_count": 0,
  "other_competitors_prices": [],
  "output_payload_for_db": {
    "competitor_price": 18000
  }
}
```
**Семпл #20:**
```json
{
  "build_key": "rx_580_i7_6700t",
  "input_pc_ad": {
    "id": 2164,
    "price": 12200
  },
  "other_competitors_count": 1,
  "other_competitors_prices": [
    12300
  ],
  "output_payload_for_db": {
    "competitor_price": 12300
  }
}
```

============================================================

import json

# Наша розширена база даних
pc_market = {
    "cpu_intel": {
        "i3_6100": {"price": 250, "score": 1.0},
        "i5_6500": {"price": 800, "score": 3.5},
        "i7_6700": {"price": 2200, "score": 4.0},
        "i3_8100": {"price": 800, "score": 4.2},
        "i5_8400": {"price": 1500, "score": 5.5},
        "i7_8700": {"price": 3800, "score": 6.8},
        "i3_9100f": {"price": 1900, "score": 4.8},
        "i5_9400f": {"price": 1900, "score": 6.0},
        "i7_9700f": {"price": 4500, "score": 7.2},
        "i3_10100f": {"price": 2300, "score": 6.5},
        "i5_10400f": {"price": 3500, "score": 7.8},
        "i7_10700f": {"price": 5800, "score": 8.5},
        "i3_12100f": {"price": 3200, "score": 8.0},
        "i5_12400f": {"price": 4900, "score": 9.2},
        "i5_13400f": {"price": 6800, "score": 9.4},
        "i5_14400f": {"price": 7800, "score": 9.5},
        "i7_12700f": {"price": 8500, "score": 9.3},
        "i7_13700f": {"price": 12000, "score": 9.6},
        "i7_14700f": {"price": 14500, "score": 9.7},
        "i9_14900k": {"price": 22000, "score": 9.9}
    },
    "cpu_ryzen": {
        "ryzen_3_1200": {"price": 1000, "score": 2.5},
        "ryzen_5_1600": {"price": 1600, "score": 4.5},
        "ryzen_7_1700": {"price": 2000, "score": 4.8},
        "ryzen_3_3100": {"price": 1900, "score": 5.2},
        "ryzen_5_2600": {"price": 2100, "score": 5.8},
        "ryzen_7_2700x": {"price": 3000, "score": 6.2},
        "ryzen_3_4100": {"price": 2200, "score": 5.5},
        "ryzen_5_3500x": {"price": 2600, "score": 6.5},
        "ryzen_5_3600": {"price": 2900, "score": 7.8},
        "ryzen_7_3700x": {"price": 4200, "score": 8.0},
        "ryzen_5_4500": {"price": 2700, "score": 7.0},
        "ryzen_5_5500": {"price": 3400, "score": 8.5},
        "ryzen_5_5600": {"price": 4300, "score": 9.3},
        "ryzen_7_5700x": {"price": 6200, "score": 9.4},
        "ryzen_7_5800x3d": {"price": 9500, "score": 9.7},
        "ryzen_5_7500f": {"price": 6000, "score": 9.5},
        "ryzen_5_7600": {"price": 7500, "score": 9.6},
        "ryzen_7_7700x": {"price": 11000, "score": 9.6},
        "ryzen_7_7800x3d": {"price": 16500, "score": 9.9},
        "ryzen_9_7950x": {"price": 21000, "score": 9.8}
    },
    "mobo_intel": {
        "H-чіпсет (Basic)": {"price": 1200, "score": 4.0},
        "B-чіпсет (Medium)": {"price": 2400, "score": 7.0},
        "Z-чіпсет (Premium)": {"price": 4500, "score": 9.5}
    },
    "mobo_ryzen": {
        "A-чіпсет (Basic)": {"price": 1300, "score": 4.0},
        "B-чіпсет (Medium)": {"price": 2600, "score": 7.5},
        "X-чіпсет (Premium)": {"price": 5000, "score": 9.5}
    },
    "gpu": {
        "gtx_750_ti": {"price": 1200, "score": 1.5},
        "gtx_960": {"price": 1600, "score": 2.2},
        "gtx_1050_ti": {"price": 2000, "score": 2.8},
        "rx_470_4gb": {"price": 1800, "score": 4.0},
        "rx_580_8gb": {"price": 2500, "score": 5.5},
        "gtx_1060_3gb": {"price": 2400, "score": 4.2},
        "gtx_1060_6gb": {"price": 3100, "score": 5.0},
        "gtx_1650_super": {"price": 3300, "score": 5.2},
        "gtx_1660_super": {"price": 4200, "score": 6.8},
        "rtx_2060_super": {"price": 6000, "score": 7.5},
        "rx_6600": {"price": 7200, "score": 8.5},
        "rtx_3060_12gb": {"price": 9500, "score": 8.7},
        "rx_6700_xt": {"price": 11000, "score": 9.2},
        "rtx_4060": {"price": 12500, "score": 9.0},
        "rtx_3070": {"price": 13000, "score": 9.1},
        "rtx_4060_ti": {"price": 16000, "score": 9.2},
        "rx_7700_xt": {"price": 17500, "score": 9.4},
        "rtx_4070_super": {"price": 26000, "score": 9.7},
        "rtx_4080_super": {"price": 46000, "score": 9.8},
        "rtx_4090": {"price": 85000, "score": 10.0}
    },
    "ram": {
        "8gb_ddr4": {"price": 700, "score": 4.0},
        "16gb_ddr4": {"price": 1300, "score": 7.5},
        "32gb_ddr4": {"price": 2600, "score": 9.5}
    },
    "storage": {
        "ssd_240gb": {"price": 600, "score": 4.0},
        "ssd_480gb": {"price": 1100, "score": 7.0},
        "ssd_1tb": {"price": 2000, "score": 9.5}
    },
    "psu": {
        "400W_v1": {"price": 800, "score": 3.5},
        "500W_v2": {"price": 1200, "score": 6.5},
        "600W_v3": {"price": 1800, "score": 8.5}
    },
    "case": {
        "Простий_офісний": {"price": 500, "score": 3.0},
        "Ігровий_з_акрилом": {"price": 1200, "score": 6.5},
        "Mesh_продувний": {"price": 1700, "score": 8.5}
    }
}

def build_best_pc_weighted(market_data: dict, budget: float) -> dict:
    
    def optimize_for_platform(platform_name: str) -> dict:
        best_build = None
        max_score = -1
        
        cpus = market_data.get(f"cpu_{platform_name}", {})
        mobos = market_data.get(f"mobo_{platform_name}", {})
        gpus = market_data.get("gpu", {})
        rams = market_data.get("ram", {})
        storages = market_data.get("storage", {})
        psus = market_data.get("psu", {})
        cases = market_data.get("case", {})
        
        for cpu_name, cpu_info in cpus.items():
            if cpu_info["price"] > budget: continue
            for mobo_name, mobo_info in mobos.items():
                if cpu_info["price"] + mobo_info["price"] > budget: continue
                for gpu_name, gpu_info in gpus.items():
                    
                    base_cost = cpu_info["price"] + mobo_info["price"] + gpu_info["price"]
                    if base_cost > budget: continue
                    
                    for ram_name, ram_info in rams.items():
                        for storage_name, storage_info in storages.items():
                            for psu_name, psu_info in psus.items():
                                for case_name, case_info in cases.items():
                                    
                                    total_price = base_cost + ram_info["price"] + storage_info["price"] + psu_info["price"] + case_info["price"]
                                    
                                    if total_price > budget:
                                        continue
                                    
                                    # --- ОСЬ ТУТ МИ ВПРОВАДЖУЄМО КРИТЕРІЇ ВАЖЛИВОСТІ Комплектуючих ---
                                    weighted_score = (
                                        cpu_info["score"] * 2.5 +      # Процесор
                                        mobo_info["score"] * 1.0 +     # Материнка
                                        gpu_info["score"] * 3.5 +      # Відеокарта (найвищий пріоритет)
                                        ram_info["score"] * 1.5 +      # ОЗУ
                                        storage_info["score"] * 1.0 +  # Накопичувач
                                        psu_info["score"] * 1.2 +      # Блок живлення
                                        case_info["score"] * 0.5       # Корпус (найменший пріоритет)
                                    )
                                    
                                    # Сума коефіцієнтів = 2.5 + 1.0 + 3.5 + 1.5 + 1.0 + 1.2 + 0.5 = 11.2
                                    
                                    if weighted_score > max_score:
                                        max_score = weighted_score
                                        best_build = {
                                            "components": {
                                                "Процесор": cpu_name,
                                                "Материнська плата": mobo_name,
                                                "Відеокарта": gpu_name,
                                                "Оперативна пам'ять": ram_name,
                                                "Накопичувач": storage_name,
                                                "Блок живлення": psu_name,
                                                "Корпус": case_name
                                            },                      
                                            "total_price": total_price,                     
                                            # Рахуємо фінальну збалансовану оцінку від 1 до 10                      
                                            "final_rating": round(weighted_score / 11.2, 2)                     
                                        }                       
                                        
        return best_build

    results = {}
    for platform in ["intel", "ryzen"]:
        build = optimize_for_platform(platform)
        results[f"{platform.capitalize()} Platform"] = build if build else f"Недостатньо бюджету для мінімальної збірки на {platform.capitalize()}"
        
    return results

# Запускаємо тест на бюджеті 8000 грн
my_budget = 6000
final_builds = build_best_pc_weighted(pc_market, my_budget)

print(json.dumps(final_builds, indent=4, ensure_ascii=False))
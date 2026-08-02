import re
from pathlib import Path
from hardware_matchers import normalize_title

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

DB_FILE = DATA_DIR / "hardware.db"
STATS_FILE = DATA_DIR / "stats.json"
CLEANED_STATE_FILE = DATA_DIR / "cleaned_state.json"
HTML_FILE = DATA_DIR / "olx_page_source.html"

PARSER_SETTINGS = {
    "request_delay": 2.0,
    "analyzer_delay": 0.5,
    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

BANNED_KEYWORDS = [
    "куплю", "обмін", "оренда", "шукаю", "несправна", "на запчастини", 
    "прогріта", "після майнінгу", "відвал", "артефакти", "копія"
]

VIDEOCARDS = [
    "gt_430", "gt_440", "gt_450", "gt_520", "gt_530", "gt_540", "gt_550_ti", "gt_560", "gt_560_ti", "gt_570", "gt_580",
    "gtx_660", "gtx_650", "gtx_650_ti", "gtx_660_ti", "gtx_670", "gtx_680", "gtx_690",
    "gtx_260", "8800_gts", "gts_8800","9600_gt", "gt_9600","hd_2600_pro","w6600", "rx_w6600",
    "fx_5200", "fx_5500", "fx_5700", "fx_5900", "en6600", "a9600_pro",
    "8600", "8800_gt", "8800_gts", "8800_gtx", "8800_ultra", "9500gt", "9600gt", "9800gt", "9800gtx",
    "gts_250", "gtx_275", "gt_440", "gts_450", "gtx_465", "gtx_470", "gt_520", "gtx_550_ti", "gtx_570",
    "hd_2600_xt", "hd_4670", "hd_4870", "hd_5670", "hd_5770", "hd_5800",
    "hd_6450", "hd_6570", "hd_6670", "hd_6750", "hd_6770", "hd_6790", "hd_6850", "hd_6870", "hd_6950", "hd_6970",
    "hd_7730", "hd_7750", "hd_7770", "hd_7850", "hd_7870", "hd_7950", "hd_7970",
    "r5_340", "r7_250x", "r7_265", "r7_360", "r9_270x", "r9_290", "r9_290x", "r9_380",
    "rx_vega_56", "rx_vega_64", "arc_a770", "firepro_v5800", "cmp_90hx",
    "gt_610", "gt_710", "gt_720", "gt_730", "gt_740", "gt_1030", 
    "gtx_650_ti", "gtx_670", "gtx_745", "gtx_750_ti", "gtx_750", "gtx_760_ti", "gtx_760", "gtx_770", "gtx_780_ti", "gtx_780", 
    "gtx_950", "gtx_960", "gtx_970", "gtx_980_ti", "gtx_980", 
    "gtx_1050_ti", "gtx_1050", "gtx_1060_3gb", "gtx_1060_6gb", "gtx_1060", "gtx_1070_ti", "gtx_1070", "gtx_1080_ti", "gtx_1080",
    "gtx_1630", "gtx_1650_super", "gtx_1650", "gtx_1660_super", "gtx_1660_ti", "gtx_1660", 
    "rtx_2060_super", "rtx_2060", "rtx_2070_super", "rtx_2070", "rtx_2080_ti", "rtx_2080_super", "rtx_2080", 
    "rtx_3050_6gb", "rtx_3050", "rtx_3060_12gb", "rtx_3060_8gb", "rtx_3060_ti", "rtx_3060", "rtx_3070_ti", "rtx_3070", 
    "rtx_3080_12gb", "rtx_3080_10gb", "rtx_3080_ti", "rtx_3080", "rtx_3090_ti", "rtx_3090", 
    "rtx_4060_ti", "rtx_4060", "rtx_4070_ti_super", "rtx_4070_ti", "rtx_4070_super", "rtx_4070", "rtx_4080_super", "rtx_4080", "rtx_4090", 
    "rtx_5090", "rtx_5080", "rtx_5070_ti", "rtx_5070", "rtx_5060_ti", "rtx_5060", "rtx_5050", 
    "rx_460", "rx_470_4gb", "rx_470_8gb", "rx_470", "rx_480_4gb", "rx_480_8gb", "rx_480", 
    "rx_550", "rx_560", "rx_570_4gb", "rx_570_8gb", "rx_570", "rx_580_4gb", "rx_580_8gb", "rx_580", "rx_590",  
    "rx_5300", "rx_5500_xt", "rx_5500", "rx_5600_xt", "rx_5600", "rx_5700_xt", "rx_5700", 
    "rx_6400", "rx_6500_xt", "rx_6600", "rx_6600_xt", "rx_6650_xt", "rx_6700", "rx_6700_xt", "rx_6750_xt", "rx_6800", "rx_6800_xt", "rx_6900_xt", "rx_6950_xt", 
    "rx_7600", "rx_7600_xt", "rx_7700_xt", "rx_7800_xt", "rx_7900_gre", "rx_7900_xt", "rx_7900_xtx", 
    "rx_9060_xt", "rx_9070", "rx_9070_xt",
    "p106_090", "p106_100", "p104_100", "p102_100_10gb", "p102_100", "cmp_30hx", "cmp_40hx", "cmp_50hx", "cmp_90hx", "cmp_170hx",
    "tesla_k20x", "tesla_k20xm", "tesla_v100",
    "quadro_2000", "quadro_p400", "quadro_p620", "quadro_p1000", "quadro_p2000", "quadro_p2200", "quadro_p4000", "quadro_p5000", "quadro_p6000",
    "quadro_k420", "quadro_k600", "quadro_k620", "quadro_k1200", "quadro_k2000", "quadro_k2200", "quadro_k4000", "quadro_k4200", "quadro_k5000", "quadro_k5200", "quadro_k6000",
    "quadro_m2000", "quadro_m4000", "quadro_m5000", "quadro_m6000",
    "quadro_rtx_3000", "quadro_rtx_4000", "quadro_rtx_5000", "quadro_rtx_6000"
]

INTEL_CPUS = [
    "i5_3330s", "pentium_g4400t", "pentium_g5420t", "pentium_g5400", "pentium_g530", "celeron_g530", "pentium_g3220", "celeron_g5905", 
    "celeron_e3400", "celeron_560", "core_2_quad_q8200""core_2_duo_e8400", "core_2_duo_e8500", "core_2_duo_e7400", "core_2_duo_e7500",
    "core_2_quad_q8300", "core_2_quad_q9400", "core_2_quad_q9550",
    "intel_n95", "intel_n100", "intel_n200", "intel_n300", "intel_n305",
    "pentium_iii_800", "pentium_d945", "core_2_duo_e6550", "core_2_quad_q6600",
    "pentium_e2140", "pentium_e5200", "pentium_p6200", "pentium_g645", "pentium_g850",
    "celeron_g1620", "celeron_g1820", "celeron_g1840", "celeron_g3900", "celeron_g3930", 
    "celeron_g4900t", "celeron_g4900", "pentium_g2020", "pentium_g2030", "pentium_g2130", 
    "pentium_g3258", "pentium_g3260", "pentium_g3420", "pentium_g4400", "pentium_g4500", "pentium_g4560", "pentium_g4620", 
    "pentium_g5420", "pentium_g5600f", "pentium_g6405",
    "i3_380m", "i3_330m", "i3_530", "i3_540", "i3_550", 
    "i3_2100", "i3_2120", "i3_2348m", "i3_3120m", "i3_3240", "i3_4130", "i3_4150", "i3_4160",
    "i3_6098p", "i3_6100t", "i3_6100", "i3_6300t", "i3_6300", "i3_6320", 
    "i3_7100t", "i3_7100", "i3_7300t", "i3_7300", "i3_7320", 
    "i3_8100t", "i3_8100", "i3_8300t", "i3_8300", "i3_8350k", 
    "i3_9100f", "i3_9100t", "i3_9100", "i3_9350k", 
    "i3_10100t", "i3_10100f", "i3_10100", "i3_10105f", "i3_10105t", "i3_10105", "i3_10300t", "i3_10300", "i3_10320", 
    "i3_12100f", "i3_12100t", "i3_12100", "i3_12300f", "i3_12300t", "i3_12300", 
    "i3_13100f", "i3_13100t", "i3_13100", "i3_14100f", "i3_14100t", "i3_14100", 
    "i5_650", "i5_750", "i5_760", 
    "i5_2300", "i5_2310", "i5_2320", "i5_2400", "i5_2500k", "i5_2500", 
    "i5_3330", "i5_3340", "i5_3450", "i5_3470", "i5_3550", "i5_3570k", "i5_3570", 
    "i5_4430", "i5_4440", "i5_4460", "i5_4570", "i5_4590", "i5_4670k", "i5_4670", "i5_4690k", "i5_4690", 
    "i5_6400t", "i5_6400", "i5_6402p", "i5_6500t", "i5_6500", "i5_6600t", "i5_6600k", "i5_6600", "i5_5675c",
    "i5_7400t", "i5_7400", "i5_7500t", "i5_7500", "i5_7600t", "i5_7600k", "i5_7600", 
    "i5_8400t", "i5_8400", "i5_8500t", "i5_8500", "i5_8600t", "i5_8600k", "i5_8600", 
    "i5_9400t", "i5_9400f", "i5_9400", "i5_9500f", "i5_9500t", "i5_9500", "i5_9600kf", "i5_9600t", "i5_9600k", "i5_9600", 
    "i5_10400f", "i5_10400t", "i5_10400", "i5_10500t", "i5_10500", "i5_10600kf", "i5_10600k", "i5_10600t", "i5_10600", 
    "i5_11400f", "i5_11400t", "i5_11400", "i5_11500t", "i5_11500", "i5_11600kf", "i5_11600k", "i5_11600f", "i5_11600t", "i5_11600", 
    "i5_12400f", "i5_12400t", "i5_12400", "i5_12500t", "i5_12500", "i5_12600kf", "i5_12600k", "i5_12600t", "i5_12600", 
    "i5_13400f", "i5_13400t", "i5_13400", "i5_13500t", "i5_13500", "i5_13600kf", "i5_13600k", "i5_13600f", "i5_13600t", "i5_13600", 
    "i5_14400f", "i5_14400t", "i5_14400", "i5_14500t", "i5_14500", "i5_14600kf", "i5_14600k", "i5_14600f", "i5_14600t", "i5_14600", 
    "i7_860", "i7_920", "i7_2600k", "i7_2600", "i7_2670qm", "i7_2700k", "i7_3770k", "i7_3770", "i7_5775c",
    "i7_4702mq", "i7_4770k", "i7_4770", "i7_4790k", "i7_4790", "i7_4980hq",
    "i7_6700k", "i7_6700t", "i7_6700", "i7_7700k", "i7_7700t", "i7_7700", 
    "i7_8086k", "i7_8700k", "i7_8700t", "i7_8700", "i7_6800k", "i7_7800x",
    "i7_9700kf", "i7_9700k", "i7_9700f", "i7_9700t", "i7_9700", 
    "i7_10700kf", "i7_10700k", "i7_10700f", "i7_10700t", "i7_10700", 
    "i7_11700kf", "i7_11700k", "i7_11700f", "i7_11700t", "i7_11700", 
    "i7_12700kf", "i7_12700k", "i7_12700f", "i7_12700t", "i7_12700", 
    "i7_13700kf", "i7_13700k", "i7_13700f", "i7_13700t", "i7_13700", 
    "i7_14700kf", "i7_14700k", "i7_14700f", "i7_14700t", "i7_14700", 
    "i9_9900kf", "i9_9900f", "i9_9900t", "i9_9900k", "i9_9900", 
    "i9_10850k", "i9_10900kf", "i9_10900f", "i9_10900t", "i9_10900k", "i9_10900",
    "i9_11900kf", "i9_11900f", "i9_11900t", "i9_11900k", "i9_11900", "i9_7900x", "i9_9900x", "i9_10900x",
    "i9_12900kf", "i9_12900f", "i9_12900t", "i9_12900k", "i9_12900", 
    "i9_13900kf", "i9_13900f", "i9_13900t", "i9_13900k", "i9_13900", 
    "i9_14900kf", "i9_14900f", "i9_14900t", "i9_14900k", "i9_14900",
    "core_ultra_5_225f", "core_ultra_5_230f", "core_ultra_5_245kf",
    "core_ultra_7_265k", "core_ultra_7_265kf", "core_ultra_7_265f",
    "core_ultra_9_285k","core_ultra_5_245t", "core_ultra_7_265t", "core_ultra_9_285t"
]

AMD_CPUS = [
    "a4_6300", "a10_5800", "a4_3300", "fx_4300", "fx_6100", "fx_8350","athlon_64_x2_6000", "athlon_64_x2_5400", "athlon_200ge",
    "athlon_x4_640", "phenom_ii_x4_b60""athlon_64_x2_5000", "athlon_ii_x2_250", "athlon_ii_x2_260", 
    "athlon_ii_x4_631", "athlon_ii_x4_640", "athlon_x4_860k", "athlon_x4_870k", 
    "a8_5600k", "phenom_x3_8600", "phenom_ii_n850", "phenom_ii_x4_840", "phenom_ii_x4", 
    "fx_6200", "fx_6300", "fx_8300", "epyc_7402",
    "ryzen_3_1200", "ryzen_3_1300x", "ryzen_3_2200ge", "ryzen_3_2200g", "ryzen_3_2300x", 
    "ryzen_3_3100", "ryzen_3_3200g", "ryzen_3_3300x", "ryzen_3_4300ge", "ryzen_3_4300g", 
    "ryzen_3_5300ge", "ryzen_3_5300g", "ryzen_3_7300x", "ryzen_3_7300", "ryzen_3_8300ge", "ryzen_3_8300g", 
    "ryzen_5_1400", "ryzen_5_1500x", "ryzen_5_1600af", "ryzen_5_1600x", "ryzen_5_1600", 
    "ryzen_5_2400ge", "ryzen_5_2400g", "ryzen_5_2500x", "ryzen_5_2600x", "ryzen_5_2600", 
    "ryzen_5_3400ge", "ryzen_5_3400g", "ryzen_5_3500x", "ryzen_5_3500", "ryzen_5_3600xt", "ryzen_5_3600x", "ryzen_5_3600", 
    "ryzen_5_4500", "ryzen_5_4600g", 
    "ryzen_5_5500", "ryzen_5_5500gt", "ryzen_5_5500x3d", "ryzen_5_5600g", "ryzen_5_5600gt", "ryzen_5_5600x", "ryzen_5_5600xt", "ryzen_5_5600", "ryzen_5_5700g", 
    "ryzen_5_7500f", "ryzen_5_7600x", "ryzen_5_7600", "ryzen_5_8400f", "ryzen_5_9600x",
    "ryzen_7_1700x", "ryzen_7_1700", "ryzen_7_1800x", "ryzen_7_2700x", "ryzen_7_2700", 
    "ryzen_7_3700x", "ryzen_7_3800xt", "ryzen_7_3800x", "ryzen_7_4700g", 
    "ryzen_7_5700g", "ryzen_7_5700x3d", "ryzen_7_5700x", "ryzen_7_5700", "ryzen_7_5800x3d", "ryzen_7_5800x", "ryzen_7_5800", 
    "ryzen_7_7700x", "ryzen_7_7700", "ryzen_7_7800x3d", "ryzen_7_8700f", "ryzen_7_9800x3d",
    "ryzen_9_3900x", "ryzen_9_3900", "ryzen_9_3950x", "ryzen_9_5900x", "ryzen_9_5900", "ryzen_9_5950x", 
    "ryzen_9_7900x3d", "ryzen_9_7900x", "ryzen_9_7900", "ryzen_9_7950x3d", "ryzen_9_7950x", 
    "ryzen_9_9900x3d", "ryzen_9_9900x", "ryzen_9_9950x3d", "ryzen_9_9950x"
]

XEON_CPUS = [
    "xeon_e5_2623_v4", "xeon_e5_2667", "xeon_e5_2430",
    "xeon_e3_1220_v2", "xeon_e3_1220_v3", "xeon_e3_1220_v5", "xeon_e3_1220_v6", "xeon_e3_1220", 
    "xeon_e3_1230_v2", "xeon_e3_1230_v3", "xeon_e3_1230_v5", "xeon_e3_1230_v6", "xeon_e3_1230", 
    "xeon_e3_1240_v2", "xeon_e3_1240_v3", "xeon_e3_1240_v5", "xeon_e3_1240_v6", "xeon_e3_1240", 
    "xeon_e3_1270_v2", "xeon_e3_1270_v3", "xeon_e3_1270_v5", "xeon_e3_1270_v6", "xeon_e3_1270", 
    "xeon_e3_1280_v2", "xeon_e3_1280_v3", "xeon_e3_1280", "xeon_e3_1290_v2", "xeon_e3_1290",
    "xeon_e5_1620", "xeon_e5_2620_v2", "xeon_e5_2620_v3", "xeon_e5_2620_v4", "xeon_e5_2620", 
    "xeon_e5_2630_v2", "xeon_e5_2630_v3", "xeon_e5_2630_v4", "xeon_e5_2630", 
    "xeon_e5_2640_v2", "xeon_e5_2640_v3", "xeon_e5_2640_v4", "xeon_e5_2640", 
    "xeon_e5_2650_v2", "xeon_e5_2650_v3", "xeon_e5_2650_v4", "xeon_e5_2650",
    "xeon_e5_2660_v2", "xeon_e5_2660_v3", "xeon_e5_2660_v4", "xeon_e5_2660", 
    "xeon_e5_2670_v2", "xeon_e5_2670_v3", "xeon_e5_2670_v4", "xeon_e5_2670", 
    "xeon_e5_2680_v2", "xeon_e5_2680_v3", "xeon_e5_2680_v4", "xeon_e5_2680", 
    "xeon_e5_2682_v4", "xeon_e5_2689", "xeon_e5_2690_v2", "xeon_e5_2690_v3", "xeon_e5_2690_v4", "xeon_e5_2690",
    "xeon_e5_2699a_v4", "xeon_e5420", "xeon_e5440", "xeon_e5450","xeon_x5550", "xeon_e5_2609_v3",
]

MOTHERBOARDS = [
    "p55", "p45", "p35", "p965", "g41", "g31", "n68", "tb360",
    "h81_btc", "g6100", "k9ngm3", "m5a78l", "k10n78", "a99", "x99_bd3",
    "h61", "b65", "q65", "q67", "h67", "p67", "z68", "b75", "q75", "q77", "h77", "z75", "z77",
    "h81", "b85", "q85", "q87", "h87", "z87", "h97", "z97",
    "h110", "b150", "q150", "h170", "q170", "z170",
    "b250", "h270", "z270", "h310", "b360", "b365", "h370", "q370", "z370", "z390",
    "h410", "b460", "h470", "q470", "z490", "h510", "b560", "h570", "q570", "z590",
    "h610", "b660", "h670", "q670", "z690", "b760", "h770", "z790",
    "x58", "x79", "x99", "x299",
    "c202", "c204", "c206", "c222", "c224", "c226", "c232", "c236", "c242", "c246", "c621", "c622", "c741", "c742",
    "w480", "w580", "w680",
    "760g", "770", "780g", "785g", "790x", "790fx", "870", "880g", "890gx", "890fx", "970", "990x", "990fx",
    "a55", "a58", "a68h", "a75", "a78", "a85x", "a88x",
    "a320", "b350", "x370", "b450", "x470", "a520", "b550", "x570",
    "a620", "b650", "b650e", "x670", "x670e", "b840", "b850", "x870", "x870e"
]

SOCKETS = [
    "lga775", "lga1150", "lga1151", "lga1151v2", "lga1155", "lga1156", "lga1200", "lga1700", "lga1851",
    "lga1356", "lga1366", "lga1567", "lga2011", "lga2011-3", "lga2066", "lga3647", "lga4189", "lga4677",
    "socket775", "socket1150", "socket1151", "socket1155", "socket1156", "socket1200", "socket1700", "socket1851",
    "socket1366", "socket2011", "socket2011-3", "socket2066",
    "am2", "am2+", "am3", "am3+", "am4", "am5", "fm1", "fm2", "fm2+",
    "swrx8", "str4", "trx4", "strx4"
]

CHIPSET_TO_SOCKET = {
    "p45": "lga775", "g41": "lga775", "p35": "lga775",
    "h61": "lga1155", "b75": "lga1155", "z77": "lga1155", "h77": "lga1155", "z68": "lga1155", "p67": "lga1155",
    "h81": "lga1150", "b85": "lga1150", "z87": "lga1150", "z97": "lga1150", "h97": "lga1150",
    "h110": "lga1151", "b150": "lga1151", "b250": "lga1151", "z170": "lga1151", "z270": "lga1151",
    "h310": "lga1151v2", "b360": "lga1151v2", "b365": "lga1151v2", "z370": "lga1151v2", "z390": "lga1151v2",
    "h410": "lga1200", "b460": "lga1200", "z490": "lga1200", "h510": "lga1200", "b560": "lga1200", "z590": "lga1200",
    "h610": "lga1700", "b660": "lga1700", "h670": "lga1700", "z690": "lga1700", "b760": "lga1700", "z790": "lga1700",
    "x79": "lga2011", "x99": "lga2011-3", "x299": "lga2066", "x58": "lga1366",
    "760g": "am3+", "970": "am3+", "990fx": "am3+",
    "a55": "fm2", "a58": "fm2", "a68h": "fm2+", "a88x": "fm2+",
    "a320": "am4", "b350": "am4", "x370": "am4", "b450": "am4", "x470": "am4", "a520": "am4", "b550": "am4", "x570": "am4",
    "a620": "am5", "b650": "am5", "b650e": "am5", "x670": "am5", "x670e": "am5", "b840": "am5", "b850": "am5", "x870": "am5", "x870e": "am5"
}

PSUS = [
    "200w", "240w", "250w", "300w", "350w", "380w", "385w", "400w", "420w", "430w", 
    "450w", "460w", "500w", "520w", "530w", "550w", "600w", "620w", "650w", "700w", 
    "750w", "800w", "850w", "1000w", "1050w", "1100w", "1150w", "1200w", "1250w", 
    "1300w", "1350w", "1400w", "1500w", "1600w", "1650w", "2000w"
]

STORAGES = [
    "ssd_60gb", "ssd_64gb", "ssd_120gb", "ssd_128gb", "ssd_160gb", "ssd_200gb", "ssd_240gb", "ssd_250gb", "ssd_256gb", 
    "ssd_300gb", "ssd_320gb", "ssd_400gb", "ssd_480gb", "ssd_500gb", "ssd_512gb", "ssd_960gb", "ssd_1tb", "ssd_2tb", 
    "ssd_4tb", "ssd_8tb",
    "hdd_80gb", "hdd_120gb", "hdd_160gb", "hdd_200gb", "hdd_250gb", "hdd_300gb", "hdd_320gb", "hdd_400gb", "hdd_500gb", 
    "hdd_1tb", "hdd_2tb", "hdd_3tb", "hdd_4tb", "hdd_6tb", "hdd_8tb", "hdd_10tb", "hdd_12tb", "hdd_14tb", "hdd_16tb", 
    "hdd_18tb", "hdd_20tb"
]


RAMS = [
    # DDR3
    "ram_ddr3_4gb", "ram_ddr3_8gb", "ram_ddr3_16gb",
    # DDR4
    "ram_ddr4_4gb", "ram_ddr4_8gb", "ram_ddr4_16gb", "ram_ddr4_32gb", "ram_ddr4_64gb",
    # DDR5
    "ram_ddr5_8gb", "ram_ddr5_16gb", "ram_ddr5_32gb", "ram_ddr5_48gb", "ram_ddr5_64gb", "ram_ddr5_96gb"
]

# Генератори ключів для підтримуваних стародрукованих типів
def generate_mb_keywords(mb_code: str) -> list[str]:
    variants = set()
    raw = mb_code.replace("_", " ")
    dash = mb_code.replace("_", "-")
    joined = mb_code.replace("_", "")
    for base in [raw, dash, joined]:
        variants.add(base)
        match = re.match(r"^([a-z]+)(\d+)(.*)$", base, re.IGNORECASE)
        if match:
            letter, num, rest = match.groups()
            variants.update([
                f"{letter} {num}{rest}", f"{letter} {num} {rest}", f"{letter}{num} {rest}",
                f"{letter}{num}m", f"{letter} {num}m", f"{letter}{num} m",
            ])
    return list(variants)

def generate_psu_keywords(psu_code: str) -> list[str]:
    variants = set()
    num = re.sub(r"\D", "", psu_code)
    for unit in ["w", "вт", "ват", "watt", "wt", "в"]:
        variants.add(f"{num}{unit}")
        variants.add(f"{num} {unit}")
        variants.add(f"{num}{unit}.")
        variants.add(f"{num} {unit}.")
    return list(variants)

def generate_storage_keywords(st_code: str) -> list[str]:
    variants = set()
    st_type, cap = st_code.split("_")
    cap_num = re.sub(r"\D", "", cap)
    unit = "tb" if "tb" in cap else "gb"
    unit_ukr = "тб" if unit == "tb" else "гб"
    type_variants = ["ssd", "ссд", "nvme"] if st_type == "ssd" else ["hdd", "хдд", "жорсткий диск", "жесткий диск", "винчестер"]
    for t in type_variants:
        variants.add(f"{t} {cap_num}{unit}")
        variants.add(f"{t} {cap_num} {unit}")
        variants.add(f"{t} {cap_num}{unit_ukr}")
        variants.add(f"{t} {cap_num} {unit_ukr}")
        variants.add(f"{cap_num}{unit} {t}")
        variants.add(f"{cap_num} {unit} {t}")
    return list(variants)

# --- СЛОВНИК СІТКИ ТОВАРІВ ---
HARDWARE_TARGETS = {}

def _register_simple(items_list: list[str], item_type: str, subcategory: str):
    """Швидка реєстрація моделей GPU / CPU для Direct Lookup (O(1))."""
    for item in items_list:
        HARDWARE_TARGETS[item] = {
            "item_type": item_type,
            "subcategory": subcategory,
        }

def _register_legacy_targets(items_list: list[str], item_type: str, subcategory: str, kw_generator):
    """Реєстрація категорій, де поки використовується створювана картотека регулярних виразів."""
    for item in items_list:
        keywords = kw_generator(item)
        keywords_sorted = sorted(set(keywords), key=len, reverse=True)
        escaped_kws = [re.escape(kw.strip().lower()) for kw in keywords_sorted if kw.strip()]
        pattern_str = r"(?<![a-zA-Z0-9а-яА-ЯіІїЇєЄґҐ])(?:" + "|".join(escaped_kws) + r")(?![a-zA-Z0-9а-яА-ЯіІїЇєЄґҐ])"
        HARDWARE_TARGETS[item] = {
            "item_type": item_type,
            "subcategory": subcategory,
            "compiled_pattern": re.compile(pattern_str, re.IGNORECASE)
        }

# Реєстрація нових компонентів (O(1))
_register_simple(VIDEOCARDS, "gpu", "videokarty")
_register_simple(INTEL_CPUS, "cpu", "protsessory")
_register_simple(AMD_CPUS, "cpu", "protsessory")
_register_simple(XEON_CPUS, "cpu", "protsessory")
_register_simple(RAMS, "ram", "operativnaya-pamyat")

# Реєстрація старого механізму для Motherboards, PSU, Storage
_register_legacy_targets(MOTHERBOARDS, "motherboard", "materinskie-platy", generate_mb_keywords)
_register_legacy_targets(PSUS, "psu", "bloki-pitaniya", generate_psu_keywords)
_register_legacy_targets(STORAGES, "storage", "zhestkie-diski", generate_storage_keywords)

# Для відкатних категорій (Motherboards, Storage, PSU)
LEGACY_PRE_SORTED_TARGETS = [
    (k, v) for k, v in HARDWARE_TARGETS.items() if "compiled_pattern" in v
]
LEGACY_PRE_SORTED_TARGETS.sort(key=lambda x: (len(x[0]), "_" in x[0]), reverse=True)
import json
import requests

# 1. Заголовки (Cookie залишено мінімальні, більшість не потрібні)
headers = {
    "accept": "application/json",
    "accept-language": "uk",
    "content-type": "application/json",
    "origin": "https://www.olx.ua",
    "referer": "https://www.olx.ua/uk/elektronika/kompyutery-i-komplektuyuschie/komplektuyuschie-i-aksesuary/q-%D0%B2%D1%96%D0%B4%D0%B5%D0%BE%D0%BA%D0%B0%D1%80%D1%82%D0%B0/?currency=UAH&search%5Border%5D=filter_float_price:asc",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "x-client": "DESKTOP",
}

# 2. GraphQL Payload з вашого запиту
json_data = {
    "query": """query ListingSearchQuery(
  $searchParameters: [SearchParameter!] = []
  $fetchPayAndShip: Boolean = false
  $searchOptions: SearchOptions
) {
  clientCompatibleListings(searchParameters: $searchParameters, searchOptions: $searchOptions) {
    __typename
    ... on ListingSuccess {
      __typename
      data {
        _nodeId
        id
        title
        status
        url
        created_time
        valid_to_time
        last_refresh_time
        omnibus_pushup_time
        description
        business
        offer_type
        external_url
        protect_phone
        isGpsrAvailable
        location {
          city { id name normalized_name _nodeId }
          district { id name normalized_name _nodeId }
          region { id name normalized_name _nodeId }
        }
        delivery {
          rock { active mode offer_id }
        }
        category { id type _nodeId }
        contact { courier chat name negotiation phone }
        photos { link height rotation width }
        promotion {
          highlighted top_ad options premium_ad_page urgent b2c_ad_page seller_badge_x_years_with_olx
        }
        shop { subdomain }
        user {
          id uuid _nodeId about b2c_business_page banner_desktop banner_mobile company_name created is_online last_seen logo logo_ad_page name other_ads_enabled photo seller_type social_network_account_type verification { status }
        }
        params {
          key name type
          value {
            __typename
            ... on GenericParam { key label }
            ... on CheckboxesParam { label checkboxParamKey: key }
            ... on PriceParam { value type negotiable label currency converted_value converted_currency arranged budget }
            ... on SalaryParam { from to arranged converted_currency converted_from converted_to currency gross type }
          }
        }
        partner { code }
        map { lat lon radius show_detailed zoom }
        safedeal { allowed_quantity weight_grams }
        payAndShip @include(if: $fetchPayAndShip) { sellerPaidDeliveryEnabled }
      }
      metadata {
        total_elements
        visible_total_count
        search_id
      }
    }
  }
}""",
    "variables": {
        "searchParameters": [
            {"key": "offset", "value": "0"},
            {"key": "limit", "value": "40"},
            {"key": "query", "value": "відеокарта"},
            {"key": "category_id", "value": "458"},
            {"key": "currency", "value": "UAH"},
            {"key": "sort_by", "value": "filter_float_price:asc"},
        ],
        "fetchPayAndShip": True,
        "searchOptions": None,
    },
}

print("📡 Відправляємо запит до GraphQL API OLX...")
response = requests.post("https://www.olx.ua/apigateway/graphql", headers=headers, json=json_data)

if response.status_code != 200:
    print(f"❌ Помилка запиту: {response.status_code}")
    print(response.text[:500])
    exit()

res_json = response.json()
listings_data = res_json.get("data", {}).get("clientCompatibleListings", {})

if listings_data.get("__typename") != "ListingSuccess":
    print("❌ Помилка отримання оголошень з API")
    exit()

items = listings_data.get("data", [])
metadata = listings_data.get("metadata", {})

print(f"✅ Знайдено оголошень у вибірці: {len(items)} (Всього у пошуку: {metadata.get('total_elements')})\n")

if not items:
    print("Немає даних для відображення.")
    exit()

# -------------------------------------------------------------
# Роздруківка ВСІХ можливих полів для ПЕРШОГО оголошення
# -------------------------------------------------------------
sample_ad = items[0]

print("=" * 70)
print("📌 ПОВНА СТРУКТУРА ДАНИХ ОГОЛОШЕННЯ (ПРИКЛАД 1-ГО ТОВАРУ):")
print("=" * 70)

# Основні атрибути
print(f"🔹 ID оголошення (int):          {sample_ad.get('id')}")
print(f"🔹 Заголовок (str):              {sample_ad.get('title')}")
print(f"🔹 Пряме посилання URL (str):    {sample_ad.get('url')}")
print(f"🔹 Статус (str):                 {sample_ad.get('status')}")
print(f"🔹 Дата створення (str/ISO):     {sample_ad.get('created_time')}")
print(f"🔹 Дійсне до (str/ISO):          {sample_ad.get('valid_to_time')}")
print(f"🔹 Останнє оновлення (str/ISO):  {sample_ad.get('last_refresh_time')}")
print(f"🔹 Бізнес чи приватне (bool):   {sample_ad.get('business')}")
print(f"🔹 Повний опис HTML (str):      {sample_ad.get('description', '')[:100]}... (всього {len(sample_ad.get('description', ''))} символів)")

# Локація
loc = sample_ad.get("location", {})
city = loc.get("city", {}).get("name") if loc.get("city") else "Невідомо"
region = loc.get("region", {}).get("name") if loc.get("region") else "Невідомо"
district = loc.get("district", {}).get("name") if loc.get("district") else "Немає"
print(f"\n📍 ЛОКАЦІЯ:")
print(f"   ├─ Область:  {region}")
print(f"   ├─ Місто:    {city}")
print(f"   └─ Район:   {district}")

# Координати на карті
map_data = sample_ad.get("map", {})
if map_data:
    print(f"🗺️ КООРДИНАТИ НА КАРТІ: Lat: {map_data.get('lat')}, Lon: {map_data.get('lon')}")

# Ціна та специфічні параметри
print(f"\n⚙️ ПАРАМЕТРИ ТА ЦІНА (Params):")
for param in sample_ad.get("params", []):
    p_key = param.get("key")
    p_name = param.get("name")
    p_val = param.get("value")
    
    if p_key == "price":
        val_amount = p_val.get("value")
        currency = p_val.get("currency")
        label = p_val.get("label")
        negotiable = p_val.get("negotiable")
        print(f"   💲 [ЦІНА] {label} (Число: {val_amount} {currency}, Договірна: {negotiable})")
    else:
        label = p_val.get("label") if isinstance(p_val, dict) else p_val
        print(f"   ├─ {p_name} ({p_key}): {label}")

# Контакти та Доставка
contact = sample_ad.get("contact", {})
delivery = sample_ad.get("delivery", {}).get("rock", {})
print(f"\n📞 КОНТАКТИ ТА ДОСТАВКА:")
print(f"   ├─ Ім'я продавця:      {contact.get('name')}")
print(f"   ├─ Можливість чату:    {contact.get('chat')}")
print(f"   ├─ Телефон доступний:  {contact.get('phone')}")
print(f"   └─ OLX Доставка:       {delivery.get('active')}")

# Інформація про Продавця (User)
user = sample_ad.get("user", {})
if user:
    print(f"\n👤 ПРОДАВЕЦЬ (User):")
    print(f"   ├─ User ID:           {user.get('id')}")
    print(f"   ├─ Назва/Ім'я:        {user.get('name')}")
    print(f"   ├─ Дата реєстрації:   {user.get('created')}")
    print(f"   ├─ Останній візит:    {user.get('last_seen')}")
    print(f"   └─ Онлайн зараз:      {user.get('is_online')}")

# Фотографії
photos = sample_ad.get("photos", [])
print(f"\n🖼️ ФОТОГРАФІЇ (Всього: {len(photos)}):")
if photos:
    print(f"   └─ Головне фото: {photos[0].get('link')}")

# Промоція / Реклама
promo = sample_ad.get("promotion", {})
print(f"\n🚀 РЕКЛАМНІ ОПЦІЇ (Promotion):")
print(f"   ├─ TOP оголошення:   {promo.get('top_ad')}")
print(f"   └─ Виділено кольором: {promo.get('highlighted')}")

print("\n" + "=" * 70)
print("💡 Якщо хочете зберегти повний JSON першого оголошення у файл для детального перегляду:")
with open("sample_ad_full.json", "w", encoding="utf-8") as f:
    json.dump(sample_ad, f, ensure_ascii=False, indent=2)
print("Файл 'sample_ad_full.json' успішно створено!")
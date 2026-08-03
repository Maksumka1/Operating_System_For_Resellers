import asyncio
import json
from curl_cffi.requests import AsyncSession

# 🎯 Вкажіть ID одного ТОЧНО АКТИВНОГО оголошення для тесту
TEST_AD_ID = "784649471"

HEADERS = {
    "accept": "application/json",
    "accept-language": "uk",
    "content-type": "application/json",
    "origin": "https://www.olx.ua",
    "referer": "https://www.olx.ua/",
    "sec-ch-ua": '"Not;A=Brand";v="8", "Chromium";v="124", "Google Chrome";v="124"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "x-client": "DESKTOP",
}

# Ваша робоча GraphQL Query з другого файлу
GRAPHQL_QUERY = """query ListingSearchQuery($searchParameters: [SearchParameter!] = []) {
  clientCompatibleListings(searchParameters: $searchParameters) {
    ... on ListingSuccess {
      data {
        id
        title
        status
      }
    }
  }
}"""

async def test_id_filters():
    async with AsyncSession(headers=HEADERS, impersonate="chrome124") as session:
        print("🔥 Прогріваємо сесію...")
        await session.get("https://www.olx.ua/uk/elektronika/", timeout=10)

        # ------------------------------------------------------------------
        # ТЕСТ 1: filter_refers_to_ad_id[0]
        # ------------------------------------------------------------------
        print(f"\n--- 🧪 ТЕСТ 1: filter_refers_to_ad_id[0] = {TEST_AD_ID} ---")
        p1 = {
            "query": GRAPHQL_QUERY,
            "variables": {
                "searchParameters": [
                    {"key": "filter_refers_to_ad_id[0]", "value": str(TEST_AD_ID)}
                ]
            }
        }
        r1 = await session.post("https://www.olx.ua/apigateway/graphql", json=p1)
        res1 = r1.json().get("data", {}).get("clientCompatibleListings", {}).get("data", [])
        print(f"Знайдено оголошень: {len(res1)}")
        if res1:
            print(f"Перший результат ID: {res1[0].get('id')} | Title: {res1[0].get('title')[:40]}")

        # ------------------------------------------------------------------
        # ТЕСТ 2: filter_enum_id[0]
        # ------------------------------------------------------------------
        print(f"\n--- 🧪 ТЕСТ 2: filter_enum_id[0] = {TEST_AD_ID} ---")
        p2 = {
            "query": GRAPHQL_QUERY,
            "variables": {
                "searchParameters": [
                    {"key": "filter_enum_id[0]", "value": str(TEST_AD_ID)}
                ]
            }
        }
        r2 = await session.post("https://www.olx.ua/apigateway/graphql", json=p2)
        res2 = r2.json().get("data", {}).get("clientCompatibleListings", {}).get("data", [])
        print(f"Знайдено оголошень: {len(res2)}")
        if res2:
            print(f"Перший результат ID: {res2[0].get('id')} | Title: {res2[0].get('title')[:40]}")

        # ------------------------------------------------------------------
        # ТЕСТ 3: filter_float_id:from / filter_float_id:to (точний діапазон)
        # ------------------------------------------------------------------
        print(f"\n--- 🧪 ТЕСТ 3: filter_float_id:from/to = {TEST_AD_ID} ---")
        p3 = {
            "query": GRAPHQL_QUERY,
            "variables": {
                "searchParameters": [
                    {"key": "filter_float_id:from", "value": str(TEST_AD_ID)},
                    {"key": "filter_float_id:to", "value": str(TEST_AD_ID)}
                ]
            }
        }
        r3 = await session.post("https://www.olx.ua/apigateway/graphql", json=p3)
        res3 = r3.json().get("data", {}).get("clientCompatibleListings", {}).get("data", [])
        print(f"Знайдено оголошень: {len(res3)}")
        if res3:
            print(f"Перший результат ID: {res3[0].get('id')} | Title: {res3[0].get('title')[:40]}")

if __name__ == "__main__":
    asyncio.run(test_id_filters())
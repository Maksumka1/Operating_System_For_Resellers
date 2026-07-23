import asyncio
import json
from curl_cffi.requests import AsyncSession

# Точні заголовки з вашого cURL (без прив'язки до особистих куків)
HEADERS = {
    "accept": "application/json",
    "accept-language": "uk",
    "content-type": "application/json",
    "origin": "https://www.olx.ua",
    "priority": "u=1, i",
    "referer": "https://www.olx.ua/",
    "sec-ch-ua": '"Not;A=Brand";v="8", "Chromium";v="124", "Google Chrome";v="124"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "x-client": "DESKTOP",  # 👈 КРИТИЧНО ВАЖЛИВИЙ ХЕДЕР
}

GRAPHQL_PAYLOAD = {
    "query": """query ListingSearchQuery($searchParameters: [SearchParameter!] = []) {
      clientCompatibleListings(searchParameters: $searchParameters) {
        ... on ListingSuccess {
          data {
            id
            title
            status
            url
            user { id name created }
          }
        }
      }
    }""",
    "variables": {
        "searchParameters": [
            {"key": "offset", "value": "0"},
            {"key": "limit", "value": "10"},
            {"key": "query", "value": "ссд диски"},
        ]
    },
}

async def test_graphql_request():
    async with AsyncSession(headers=HEADERS, impersonate="chrome124") as session:
        # Крок 1: Ініціалізація сесії та отримання початкових DataDome / OLX куків
        print("1. Отримуємо початкові cookies...")
        resp_init = await session.get("https://www.olx.ua/uk/elektronika/", timeout=10)
        print(f"Головна сторінка: status {resp_init.status_code}")

        # Крок 2: Відправка GraphQL запиту з правильним хедром x-client
        print("2. Відправляємо GraphQL запит...")
        resp = await session.post(
            "https://www.olx.ua/apigateway/graphql",
            json=GRAPHQL_PAYLOAD,
            timeout=15,
        )

        print(f"GraphQL Status: {resp.status_code}")
        if resp.status_code == 200:
            print("Успіх! Отримано JSON:")
            print(json.dumps(resp.json(), indent=2, ensure_ascii=False)[:500])
        else:
            print("Помилка response text:", resp.text[:300])

if __name__ == "__main__":
    asyncio.run(test_graphql_request())
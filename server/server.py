import sys
import sqlite3
import json
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
if not (PROJECT_ROOT / "config.py").exists():
    PROJECT_ROOT = PROJECT_ROOT.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from config import DB_FILE

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        print(f"📡 [WS] Нове підключення! Активних клієнтів: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        print(f"🛑 [WS] Клієнт відключився. Залишилось: {len(self.active_connections)}")

    async def broadcast(self, message: dict):
        print(f"📢 [WS BROADCAST] Розкидаємо лот через сокет: {message.get('title', 'Без назви')[:40]}...")
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception as e:
                print(f"❌ [WS ERROR] Помилка відправки клієнту: {e}")
                pass

manager = ConnectionManager()

class NewAdModel(BaseModel):
    id: int  # 🔥 Додали id в модель для реалтайму
    url: str
    title: str
    description: str | None = None
    price: int
    item_type: str
    city: str | None = None
    created_at_olx: str | None = None
    photo_url: str | None = None
    seller_name: str | None = None
    seller_created_at: str | None = None
    seller_successful_deals: int | None = 0
    seller_rating: str | None = None
    seller_risk: str | None = "neutral"
    estimated_fair_price: int | None = None
    competitor_price: int | None = None
    saving_uah: int | None = None
    saving_percent: int | None = None
    evaluated_at: str | None = None


@app.get("/api/ads")
def get_ads():
    print("\n🔍 [API GET] Запит бази даних від фронтенду...")
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # 🔥 ФІКС ТУТ: Додали початкове поле 'id' у SELECT запит
    cursor.execute("""
        SELECT 
            id, url, title, description, price, item_type, city, created_at_olx, photo_url,
            seller_name, seller_created_at, seller_successful_deals, seller_rating, seller_risk_score,
            estimated_fair_price, competitor_price, saving_uah, saving_percent, evaluated_at
        FROM ads 
        WHERE status = 'active'
        ORDER BY id DESC
    """)
    rows = cursor.fetchall()
    conn.close()
    
    print(f"📊 [API GET] Знайдено активних лотів у SQLite: {len(rows)}")
    
    # Виведемо в консоль бекенду лог по i5-8400, щоб ти бачив, що вони дістаються
    i5_count = 0
    for r in rows:
        if "i5-8400" in str(r[2]).lower() or "i5 8400" in str(r[2]).lower() or "i5-8400" in str(r[1]).lower():
            i5_count += 1
            print(f"   └─ [Знайдено в БД] ID: {r[0]} | Title: {r[2][:30]}... | Price: {r[4]} UAH | Risk: {r[13]}")
    
    print(f"🎯 [DEBUG INFO] Всього процесорів i5-8400 у вибірці з бази: {i5_count}")

    # Зсуваємо індекси масиву r на +1, бо r[0] тепер це id
    return [
        {
"id": r[0],
            "url": r[1],
            "title": r[2],
            "description": r[3],
            "price": r[4],
            "item_type": r[5], 
            "city": r[6],
            "created_at_olx": r[7],
            "photo_url": r[8],
            "seller_name": r[9],
            "seller_created_at": r[10],
            "seller_successful_deals": r[11] or 0,
            "seller_rating": r[12] or "немає оцінок",
            "seller_risk": r[13] or "neutral",
            "estimated_fair_price": r[14],
            "competitor_price": r[15], 
            "saving_uah": r[16],
            "saving_percent": r[17],
            "evaluated_at": r[18]
        }
        for r in rows
    ]


@app.post("/api/trigger-new-ad")
async def trigger_new_ad(ad: NewAdModel):
    print(f"📥 [API POST] Отримано новий лот від парсера: {ad.title}")
    await manager.broadcast(ad.dict())
    return {"status": "broadcasted"}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)
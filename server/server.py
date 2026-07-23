import sys
import sqlite3
from typing import List, Union
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Body, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
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

# 🔍 Гнучка модель: ціни та відсотки приймають float / int / None
class NewAdModel(BaseModel):
    id: int
    url: str
    title: str
    description: str | None = None
    price: float | int | None = 0
    item_type: str | None = "unknown"
    city: str | None = None
    created_at_olx: str | None = None
    photo_url: str | None = None
    seller_name: str | None = None
    seller_created_at: str | None = None
    seller_successful_deals: int | None = 0
    seller_rating: str | None = None
    seller_risk: str | None = "neutral"
    estimated_fair_price: float | int | None = None
    competitor_price: float | int | None = None
    saving_uah: float | int | None = None
    saving_percent: float | int | None = None
    evaluated_at: str | None = None


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        print(f"📡 [WS] Нове підключення! Активних клієнтів: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
            print(f"🛑 [WS] Клієнт відключився. Залишилось: {len(self.active_connections)}")

    async def broadcast(self, message: dict):
        print(f"📢 [WS BROADCAST] Розкидаємо лот: {message.get('title', 'Без назви')[:40]}...")
        for connection in list(self.active_connections):
            try:
                await connection.send_json(message)
            except Exception as e:
                print(f"❌ [WS ERROR] Помилка відправки клієнту: {e}")

manager = ConnectionManager()


# 🐛 Обробник помилок валідації (виводить у консоль exact причину, якщо щось не так)
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    print("❌ [VALIDATION ERROR 422]:", exc.errors())
    return JSONResponse(status_code=422, content={"detail": exc.errors()})


@app.get("/api/ads")
def get_ads():
    print("\n🔍 [API GET] Запит бази даних від фронтенду...")
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
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
async def trigger_new_ad(payload: Union[List[NewAdModel], NewAdModel] = Body(...)):
    if isinstance(payload, list):
        print(f"📥 [API POST] Отримано пачку з {len(payload)} лотів від парсера!")
        for ad in payload:
            await manager.broadcast(ad.model_dump())
    else:
        print(f"📥 [API POST] Отримано лот: {payload.title}")
        await manager.broadcast(payload.model_dump())
        
    return {"status": "broadcasted"}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)
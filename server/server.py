import os
import sys
from typing import List, Union
from pathlib import Path

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Body, Request, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from supabase import create_client, Client

# --- ПІДКТЮЧЕННЯ ДО SUPABASE ---
SUPABASE_URL = os.getenv("SUPABASE_URL", "https://nfhtmfhckctuyhfolhou.supabase.co")
# Використовуємо SERVICE_ROLE_KEY або PUBLISHABLE_KEY із змінних середовища
SUPABASE_KEY = os.getenv("SUPABASE_SECRET_KEY") or os.getenv("SUPABASE_PUBLISHABLE_KEY")

if not SUPABASE_KEY:
    print("⚠️ [УВАГА] Не знайдено SUPABASE_SECRET_KEY або SUPABASE_PUBLISHABLE_KEY у змінних середовища!")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY or "")

# Схема перевірки Bearer токена в заголовках Authorization
security = HTTPBearer()

app = FastAPI(title="Edge.Feed API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Для продакшну замінити на конкретний домен Vercel
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- МІДЛВЕРА ДЛЯ ПЕРЕВІРКИ АВТОРИЗАЦІЇ КОРИСТУВАЧА ---
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Перевіряє JWT-токен, надісланий з React-фронтенду через Supabase Auth."""
    token = credentials.credentials
    try:
        # Звертаємося до Supabase, щоб валідувати токен
        user_response = supabase.auth.get_user(token)
        if not user_response or not user_response.user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Невалідний або протермінований сесійний токен"
            )
        return user_response.user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Помилка авторизації: {str(e)}"
        )


# --- PYDANTIC МОДЕЛЬ ДАНИХ ---
class NewAdModel(BaseModel):
    id: int | None = None
    ad_id: int | None = None
    url: str
    title: str
    description: str | None = None
    price: float | int | None = 0
    seller_price_clean: float | int | None = None
    item_type: str | None = "unknown"
    component_name: str | None = None
    socket: str | None = None
    city: str | None = None
    created_at_olx: str | None = None
    last_refresh_time: str | None = None
    photo_url: str | None = None
    photos: str | None = None
    all_photos: str | None = None
    has_defects: int | None = 0
    pc_category: str | None = "uncategorized"
    seller_id: str | None = None
    seller_name: str | None = None
    seller_created_at: str | None = None
    seller_successful_deals: int | None = 0
    seller_rating: str | None = "немає оцінок"
    seller_type: str | None = "private_person"
    seller_risk_score: str | None = "neutral"
    gpu_detected: str | None = None
    cpu_detected: str | None = None
    gpu_market_price: float | int | None = None
    cpu_market_price: float | int | None = None
    estimated_fair_price: float | int | None = None
    competitor_price: float | int | None = None
    saving_uah: float | int | None = None
    saving_percent: float | int | None = None
    deal_status: str | None = "regular"
    evaluated_at: str | None = None


# --- WEBSOCKET МЕНЕДЖЕР З'ЄДНАНЬ ---
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


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    print("❌ [VALIDATION ERROR 422]:", exc.errors())
    return JSONResponse(status_code=422, content={"detail": exc.errors()})


# --- ЕНДПОІНТИ API ---

@app.get("/api/ads")
def get_ads(current_user = Depends(get_current_user)):
    """
    Повертає список активних оголошень з бази Supabase.
    Доступ дозволено ТІЛЬКИ авторизованим користувачам.
    """
    print(f"\n🔍 [API GET] Запит бази від користувача: {current_user.email}")
    
    try:
        # Запит до таблиці 'ads' у Supabase
        response = (
            supabase.table("ads")
            .select("*")
            .eq("status", "active")
            .order("id", desc=True)
            .execute()
        )
        rows = response.data or []
    except Exception as e:
        print(f"❌ [SUPABASE ERROR]: {e}")
        raise HTTPException(status_code=500, detail="Помилка читання з бази даних Supabase")
    
    print(f"📊 [API GET] Віддаємо {len(rows)} повних лотів для фронтенду.")

    # Обробка та подвійна страховка фолбеків для фронтенду
    result = []
    for ad_dict in rows:
        ad_dict["seller_successful_deals"] = ad_dict.get("seller_successful_deals") or 0
        ad_dict["seller_rating"] = ad_dict.get("seller_rating") or "немає оцінок"
        ad_dict["seller_risk_score"] = ad_dict.get("seller_risk_score") or "neutral"
        ad_dict["deal_status"] = ad_dict.get("deal_status") or "regular"
        result.append(ad_dict)

    return result


@app.post("/api/trigger-new-ad")
async def trigger_new_ad(payload: Union[List[NewAdModel], NewAdModel] = Body(...)):
    """Приймає нові лоти від парсера і транслює їх підключеним клієнтам через WebSocket."""
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
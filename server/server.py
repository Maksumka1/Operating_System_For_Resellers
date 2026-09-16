"""
Edge.Feed API Server — Production Ready (Single-Instance / 1 Worker)
Запуск: uvicorn server:app --host 0.0.0.0 --port 8000 --workers 1
"""

from __future__ import annotations

import asyncio
import json
import logging
import os
import re
import secrets
import httpx
from datetime import datetime, timedelta, timezone
from typing import Any, List, Union

import jwt
from dotenv import load_dotenv
from fastapi import (
    BackgroundTasks,
    Body,
    Depends,
    FastAPI,
    Header,
    HTTPException,
    Query,
    Request,
    WebSocket,
    WebSocketDisconnect,
    status,
)
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel, Field
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from supabase import Client, create_client
from services.telegram_notifier import TelegramNotifierService, handle_category_toggle

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("server")

# --- КОНФІГУРАЦІЯ ТА СЕКРЕТИ ---
ENVIRONMENT = os.getenv("ENVIRONMENT", "production").strip().lower()
SUPABASE_URL = os.getenv("SUPABASE_URL", "").strip()
SUPABASE_KEY = os.getenv("SUPABASE_SECRET_KEY", "").strip()
SUPABASE_JWT_SECRET = os.getenv("SUPABASE_JWT_SECRET", "").strip()
INTERNAL_SECRET_KEY = os.getenv("INTERNAL_SECRET_KEY", "").strip()

MONOBANK_TOKEN = os.getenv("MONOBANK_TOKEN", "").strip()
APP_PUBLIC_URL = os.getenv("APP_PUBLIC_URL", "http://localhost:8000").strip().rstrip("/")
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173").strip().rstrip("/")

tg_service = TelegramNotifierService(os.getenv("TELEGRAM_BOT_TOKEN", ""))

ALLOWED_ORIGINS_RAW = os.getenv(
    "ALLOWED_ORIGINS", 
    "http://localhost:8080,http://localhost:3000,http://localhost:5173"
).strip()


if not SUPABASE_URL:
    raise RuntimeError("❌ Відсутній SUPABASE_URL у .env")
if not SUPABASE_KEY:
    raise RuntimeError("❌ Відсутній SUPABASE_SECRET_KEY у .env")
if not INTERNAL_SECRET_KEY:
    raise RuntimeError("❌ Відсутній INTERNAL_SECRET_KEY у .env")

ALLOWED_ORIGINS = [origin.strip() for origin in ALLOWED_ORIGINS_RAW.split(",") if origin.strip()]
MAX_WS_CONNECTIONS = 500

PLANS = {
    "month_1": {
        "title": "Підписка Edge.Feed — 1 місяць",
        "amount_kop": 64900, # 649 грн
        "days": 30,
    },
    "month_6": {
        "title": "Підписка Edge.Feed — 6 місяців",
        "amount_kop": 295000, # 2 950 грн
        "days": 180,
    },
}

PUBLIC_AD_COLUMNS = (
    "id,ad_id,url,title,description,price,seller_price_clean,item_type,component_name,"
    "socket,city,created_at_olx,photo_url,all_photos,has_defects,pc_category,seller_name,"
    "seller_rating,seller_successful_deals,seller_risk_score,estimated_fair_price,"
    "competitor_price,saving_uah,saving_percent,deal_status,evaluated_at,"
    "gpu_detected,cpu_detected,mb_detected,motherboard_detected,ram_detected,psu_detected,"
    "storage_detected,ssd_detected,gpu_market_price,cpu_market_price,mb_market_price,"
    "motherboard_market_price,ram_market_price,psu_market_price,storage_market_price,ssd_market_price"
)

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
security = HTTPBearer()

limiter = Limiter(key_func=get_remote_address)
app = FastAPI(
    title="Edge.Feed API",
    docs_url="/api/docs" if ENVIRONMENT == "development" else None,
    redoc_url=None,
    openapi_url="/api/openapi.json" if ENVIRONMENT == "development" else None,
)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class CreateInvoiceRequest(BaseModel):
    plan_type: str = Field(pattern=r"^(month_1|month_6)$")


# --- АВТОРИЗАЦІЯ ТА ПЕРЕВІРКА ПІДПИСКИ ---
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict[str, Any]:
    token = credentials.credentials

    if SUPABASE_JWT_SECRET:
        try:
            payload = jwt.decode(
                token,
                SUPABASE_JWT_SECRET,
                algorithms=["HS256"],
                audience="authenticated",
            )
            user_id = payload.get("sub")
            if not user_id:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Невалідний ідентифікатор сесії")
            return {"id": user_id, "email": payload.get("email"), "role": payload.get("role")}
        except jwt.PyJWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Невалідний або протермінований токен")

    try:
        user_response = await asyncio.to_thread(supabase.auth.get_user, token)
        if not user_response or not user_response.user or not user_response.user.id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Сесія недійсна")
        return {"id": user_response.user.id, "email": user_response.user.email}
    except HTTPException:
        raise
    except Exception as exc:
        logger.warning(f"Помилка перевірки автентифікації: {exc}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Помилка авторизації")


async def verify_active_subscription(
    current_user: dict = Depends(get_current_user),
) -> dict[str, Any]:
    """Перевіряє, чи є у користувача активний тріал або діюча платна підписка."""
    user_id = current_user.get("id")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Неавторизований користувач")

    def _fetch_sub():
        res = (
            supabase.table("subscriptions")
            .select("status, plan_type, trial_end, subscription_end")
            .eq("user_id", user_id)
            .limit(1)
            .execute()
        )
        return res.data[0] if res.data else None

    try:
        sub = await asyncio.to_thread(_fetch_sub)
    except Exception as exc:
        logger.error(f"Помилка перевірки підписки для {user_id}: {exc}")
        raise HTTPException(status_code=500, detail="Помилка перевірки доступу")

    if not sub:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="subscription_required")

    now = datetime.now(timezone.utc)
    has_access = False

    # 1. Перевірка 3-денного тріалу
    trial_end_raw = sub.get("trial_end")
    if trial_end_raw:
        try:
            trial_end = datetime.fromisoformat(trial_end_raw.replace("Z", "+00:00"))
            if now <= trial_end:
                has_access = True
        except Exception:
            pass

    # 2. Перевірка платної підписки
    sub_end_raw = sub.get("subscription_end")
    if sub_end_raw and not has_access:
        try:
            sub_end = datetime.fromisoformat(sub_end_raw.replace("Z", "+00:00"))
            if now <= sub_end:
                has_access = True
        except Exception:
            pass

    if not has_access:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="subscription_expired",
        )

    return current_user


def verify_internal_secret(x_internal_secret: str = Header(None, alias="X-Internal-Secret")) -> None:
    if not x_internal_secret or not secrets.compare_digest(x_internal_secret, INTERNAL_SECRET_KEY):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Доступ заборонено")


# --- МОДЕЛІ ДАНИХ ---
class NewAdModel(BaseModel):
    id: Union[int, str, None] = None
    ad_id: Union[int, str, None] = None
    url: str = Field(..., max_length=4096)
    title: str = Field(..., max_length=2000)
    description: str | None = Field(default="", max_length=20000)
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

    seller_name: str | None = None
    seller_created_at: str | None = None
    seller_successful_deals: int | None = 0
    seller_rating: str | None = "немає оцінок"
    seller_type: str | None = "private_person"
    seller_risk_score: str | None = "neutral"

    gpu_detected: str | None = None
    cpu_detected: str | None = None
    mb_detected: str | None = None
    motherboard_detected: str | None = None
    ram_detected: str | None = None
    psu_detected: str | None = None
    storage_detected: str | None = None
    ssd_detected: str | None = None

    gpu_market_price: float | int | None = None
    cpu_market_price: float | int | None = None
    mb_market_price: float | int | None = None
    motherboard_market_price: float | int | None = None
    ram_market_price: float | int | None = None
    psu_market_price: float | int | None = None
    storage_market_price: float | int | None = None
    ssd_market_price: float | int | None = None

    estimated_fair_price: float | int | None = None
    competitor_price: float | int | None = None
    competitors_ids: Any = None
    saving_uah: float | int | None = None
    saving_percent: float | int | None = None
    deal_status: str | None = "regular"
    evaluated_at: str | None = None


# --- МЕНЕДЖЕР WEBSOCKET ---
class ConnectionManager:
    def __init__(self, max_connections: int = MAX_WS_CONNECTIONS) -> None:
        self.active_connections: set[WebSocket] = set()
        self.max_connections = max_connections
        self._lock = asyncio.Lock()

    async def try_connect(self, websocket: WebSocket) -> bool:
        async with self._lock:
            if len(self.active_connections) >= self.max_connections:
                return False
            self.active_connections.add(websocket)
            return True

    async def disconnect(self, websocket: WebSocket) -> None:
        async with self._lock:
            self.active_connections.discard(websocket)

    async def broadcast(self, message: dict) -> None:
        async with self._lock:
            targets = list(self.active_connections)

        if not targets:
            return

        dead_connections = []
        for connection in targets:
            try:
                await connection.send_json(message)
            except Exception:
                dead_connections.append(connection)

        if dead_connections:
            async with self._lock:
                for dead in dead_connections:
                    self.active_connections.discard(dead)


manager = ConnectionManager()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": "Помилка валідації параметрів запиту"},
    )


# --- API ЕНДПОІНТИ ---

@app.get("/api/subscription/me")
@limiter.limit("60/minute")
async def get_my_subscription(
    request: Request,
    current_user: dict = Depends(get_current_user),
) -> dict[str, Any]:
    """Повертає поточний статус тріалу / підписки користувача."""
    user_id = current_user.get("id")

    def _fetch_sub():
        res = (
            supabase.table("subscriptions")
            .select("status, plan_type, trial_end, subscription_end")
            .eq("user_id", user_id)
            .limit(1)
            .execute()
        )
        return res.data[0] if res.data else None

    sub = await asyncio.to_thread(_fetch_sub)
    if not sub:
        return {"has_access": False, "status": "none", "days_left": 0}

    now = datetime.now(timezone.utc)
    days_left = 0
    has_access = False
    effective_status = "expired"

    # Перевірка тріалу
    if sub.get("trial_end"):
        t_end = datetime.fromisoformat(sub["trial_end"].replace("Z", "+00:00"))
        if now <= t_end:
            has_access = True
            effective_status = "trial"
            days_left = max(1, (t_end - now).days + 1)

    # Перевірка платної підписки
    if sub.get("subscription_end"):
        s_end = datetime.fromisoformat(sub["subscription_end"].replace("Z", "+00:00"))
        if now <= s_end:
            has_access = True
            effective_status = sub.get("plan_type", "active")
            days_left = max(1, (s_end - now).days + 1)

    return {
        "has_access": has_access,
        "status": effective_status,
        "days_left": days_left,
        "trial_end": sub.get("trial_end"),
        "subscription_end": sub.get("subscription_end"),
    }

# --- КЛАВІАТУРИ РОЗШИРЕНИХ ФІЛЬТРІВ ---

def get_filters_dashboard_keyboard():
    """Головне меню керування всіма фільтрами."""
    return {
        "inline_keyboard": [
            [
                {"text": "📉 Знижка (%)", "callback_data": "menu_discount"},
                {"text": "💰 Ціна (грн)", "callback_data": "menu_price"}
            ],
            [
                {"text": "🔌 Сокети CPU", "callback_data": "menu_sockets"},
                {"text": "🏷️ Моделі / Слова", "callback_data": "menu_keywords"}
            ],
            [
                {"text": "🎮 Мін. VRAM", "callback_data": "menu_vram"},
                {"text": "🧠 Мін. ядер", "callback_data": "menu_cores"}
            ],
            [
                {"text": "🔧 Змінити категорії", "callback_data": "open_categories"},
                {"text": "🔄 Скинути фільтри", "callback_data": "reset_all_filters"}
            ],
            [
                {"text": "✅ Закрити меню", "callback_data": "close_filters_view"}
            ]
        ]
    }

def get_discount_inline_keyboard(current_pct: int):
    options = [10, 15, 20, 25, 30]
    row = [
        {"text": f"{'✅ ' if current_pct == p else ''}{p}%+", "callback_data": f"set_discount_{p}"}
        for p in options
    ]
    return {
        "inline_keyboard": [
            row,
            [{"text": "⬅️ Назад до фільтрів", "callback_data": "back_to_filters_menu"}]
        ]
    }

def get_sockets_inline_keyboard(active_sockets: list[str]):
    popular_sockets = ["am4", "am5", "lga1700", "lga1200", "lga1151", "lga2011-3"]
    clean_active = [s.lower().strip() for s in active_sockets]
    
    rows = []
    curr_row = []
    for s in popular_sockets:
        checked = "✅ " if s in clean_active else "▫️ "
        curr_row.append({"text": f"{checked}{s.upper()}", "callback_data": f"toggle_socket_{s}"})
        if len(curr_row) == 2:
            rows.append(curr_row)
            curr_row = []
    if curr_row:
        rows.append(curr_row)

    rows.append([
        {"text": "🗑️ Очистити сокети", "callback_data": "clear_sockets"},
        {"text": "⬅️ Назад", "callback_data": "back_to_filters_menu"}
    ])
    return {"inline_keyboard": rows}

def get_vram_inline_keyboard(current_vram: float):
    options = [(0, "Будь-яка"), (6, "6GB+"), (8, "8GB+"), (12, "12GB+"), (16, "16GB+")]
    row = [
        {"text": f"{'✅ ' if current_vram == v else ''}{label}", "callback_data": f"set_vram_{v}"}
        for v, label in options
    ]
    return {
        "inline_keyboard": [
            row[:3],
            row[3:],
            [{"text": "⬅️ Назад до фільтрів", "callback_data": "back_to_filters_menu"}]
        ]
    }

def get_cores_inline_keyboard(current_cores: int):
    options = [(0, "Всі"), (4, "4+"), (6, "6+"), (8, "8+"), (12, "12+")]
    row = [
        {"text": f"{'✅ ' if current_cores == c else ''}{label}", "callback_data": f"set_cores_{c}"}
        for c, label in options
    ]
    return {
        "inline_keyboard": [
            row,
            [{"text": "⬅️ Назад до фільтрів", "callback_data": "back_to_filters_menu"}]
        ]
    }


def format_user_filters_view(sub: dict[str, Any]) -> str:
    cats = ", ".join([c.upper() for c in (sub.get("categories") or ["gpu", "cpu", "pc"])])
    discount = sub.get("min_saving_percent") or 10
    min_p = sub.get("min_price") or 0
    max_p = sub.get("max_price") or 1000000
    price_str = f"від {min_p:,} до {max_p:,} грн".replace(",", " ") if (min_p > 0 or max_p < 1000000) else "Будь-яка"

    sockets = sub.get("target_sockets") or []
    sockets_str = ", ".join([s.upper() for s in sockets]) if sockets else "Всі платформи"

    keywords = sub.get("target_brands") or []
    keywords_str = ", ".join(keywords) if keywords else "Не задано (всі моделі)"

    vram = sub.get("min_vram_gb")
    vram_str = f"від {int(vram)} GB" if vram and float(vram) > 0 else "Будь-який"

    cores = sub.get("min_cores")
    cores_str = f"від {cores} ядер" if cores and int(cores) > 0 else "Будь-яка кількість"

    return (
        "<b>📋 Ваші персональні параметри пошуку:</b>\n\n"
        f"• <b>Категорії:</b> <code>{cats}</code>\n"
        f"• <b>Мін. дисконт:</b> <code>від {discount}%</code>\n"
        f"• <b>Ціновий діапазон:</b> <code>{price_str}</code>\n"
        f"• <b>Сокети CPU:</b> <code>{sockets_str}</code>\n"
        f"• <b>Фільтр за назвами/моделями:</b> <code>{keywords_str}</code>\n"
        f"• <b>Відеопам'ять GPU:</b> <code>{vram_str}</code>\n"
        f"• <b>Кількість ядер CPU:</b> <code>{cores_str}</code>\n"
        f"• <b>Статус моніторингу:</b> Активний 🟢\n\n"
        "<i>Використовуйте кнопки нижче або текстові команди (напр. <code>/price 5000 20000</code>, <code>/keywords ryzen 5600, rtx 3060</code>):</i>"
    )


def get_main_menu_keyboard():
    """Постійна клавіатура головного меню бота."""
    return {
        "keyboard": [
            [{"text": "⚙️ Мої фільтри"}, {"text": "🔧 Змінити категорії"}],
            [{"text": "ℹ️ Що робить бот?"}, {"text": "🌐 Мій кабінет"}]
        ],
        "resize_keyboard": True,
        "is_persistent": True
    }


def get_categories_inline_keyboard(active_cats: list[str]):
    """Інлайн-клавіатура з вибором категорій та навігацією."""
    return {
        "inline_keyboard": [
            [
                {"text": f"{'✅' if 'gpu' in active_cats else '▫️'} GPU", "callback_data": "toggle_gpu"},
                {"text": f"{'✅' if 'cpu' in active_cats else '▫️'} CPU", "callback_data": "toggle_cpu"},
            ],
            [
                {"text": f"{'✅' if 'ram' in active_cats else '▫️'} RAM", "callback_data": "toggle_ram"},
                {"text": f"{'✅' if 'storage' in active_cats else '▫️'} SSD/HDD", "callback_data": "toggle_storage"},
            ],
            [
                {"text": f"{'✅' if 'pc' in active_cats else '▫️'} Готові ПК", "callback_data": "toggle_pc"},
                {"text": f"{'✅' if 'psu' in active_cats else '▫️'} БЖ", "callback_data": "toggle_psu"},
            ],
            [
                {"text": "💾 Зберегти", "callback_data": "close_categories"},
                {"text": "⬅️ До всіх фільтрів", "callback_data": "back_to_filters_menu"}
            ]
        ]
    }


async def check_telegram_subscriber_access(chat_id: int) -> dict[str, Any]:
    """Перевіряє доступ до бота без виклику потенційно відсутніх колонок."""
    def _fetch():
        try:
            sub_res = supabase.table("telegram_subscribers").select("user_id, categories").eq("chat_id", chat_id).execute()
            if not sub_res.data or not sub_res.data[0].get("user_id"):
                return None, None

            user_id = sub_res.data[0]["user_id"]
            plan_res = supabase.table("subscriptions").select("status, trial_end, subscription_end").eq("user_id", user_id).limit(1).execute()
            plan = plan_res.data[0] if plan_res.data else None
            return sub_res.data[0], plan
        except Exception as e:
            logger.error(f"Помилка check_telegram_subscriber_access (chat_id: {chat_id}): {e}")
            return None, None

    subscriber, plan = await asyncio.to_thread(_fetch)
    if not subscriber or not plan:
        return {"allowed": False, "reason": "unauthorized", "subscriber": None}

    now = datetime.now(timezone.utc)
    has_access = False

    if plan.get("trial_end"):
        try:
            t_end = datetime.fromisoformat(plan["trial_end"].replace("Z", "+00:00"))
            if now <= t_end:
                has_access = True
        except Exception:
            pass

    if plan.get("subscription_end") and not has_access:
        try:
            s_end = datetime.fromisoformat(plan["subscription_end"].replace("Z", "+00:00"))
            if now <= s_end:
                has_access = True
        except Exception:
            pass

    return {
        "allowed": has_access,
        "reason": "active" if has_access else "expired",
        "subscriber": subscriber,
    }


async def process_telegram_update(data: dict):
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
    if not bot_token:
        logger.error("❌ [TG] TELEGRAM_BOT_TOKEN відсутній у змінних оточення!")
        return

    # 1. ОБРОБКА CALLBACK QUERY
    if "callback_query" in data:
        cq = data["callback_query"]
        cq_id = cq["id"]
        chat_id = cq["from"]["id"]
        cb_data = cq.get("data", "")
        message_id = cq.get("message", {}).get("message_id")
        logger.info(f"🔘 [TG Callback] chat_id={chat_id}, data={cb_data}")

        async with httpx.AsyncClient(timeout=10.0) as client:
            access = await check_telegram_subscriber_access(chat_id)
            logger.info(f"🔑 [TG Access] chat_id={chat_id}, allowed={access['allowed']}, reason={access.get('reason')}")

            if not access["allowed"]:
                await client.post(
                    f"https://api.telegram.org/bot{bot_token}/answerCallbackQuery",
                    json={"callback_query_id": cq_id, "text": "🔒 Потрібна активна підписка на сайті!", "show_alert": True}
                )
                return

            # ВІДКРИТТЯ МЕНЮ КАТЕГОРІЙ ІЗ ДАШБОРДУ ФІЛЬТРІВ (FIX)
            if cb_data == "open_categories":
                sub_fresh = (await asyncio.to_thread(lambda: supabase.table("telegram_subscribers").select("categories").eq("chat_id", chat_id).execute())).data
                active_cats = sub_fresh[0].get("categories") if sub_fresh else ["gpu", "cpu", "pc"]
                await client.post(
                    f"https://api.telegram.org/bot{bot_token}/editMessageText",
                    json={
                        "chat_id": chat_id,
                        "message_id": message_id,
                        "text": "<b>Оберіть категорії комплектуючих для сповіщень:</b>\n<i>(Натискайте на кнопки для ввімкнення / вимкнення)</i>",
                        "parse_mode": "HTML",
                        "reply_markup": get_categories_inline_keyboard(active_cats)
                    }
                )
                await client.post(f"https://api.telegram.org/bot{bot_token}/answerCallbackQuery", json={"callback_query_id": cq_id})
                return

            # ЗБЕРЕЖЕННЯ КАТЕГОРІЙ (FIX СВІЖИХ ДАНИХ)
            if cb_data == "close_categories":
                sub_fresh = (await asyncio.to_thread(lambda: supabase.table("telegram_subscribers").select("categories").eq("chat_id", chat_id).execute())).data
                cats = sub_fresh[0].get("categories") if sub_fresh else ["gpu", "cpu", "pc"]
                cats_str = ", ".join(c.upper() for c in cats)
                await client.post(
                    f"https://api.telegram.org/bot{bot_token}/answerCallbackQuery",
                    json={"callback_query_id": cq_id, "text": "✅ Категорії збережено!"}
                )
                if message_id:
                    await client.post(
                        f"https://api.telegram.org/bot{bot_token}/editMessageText",
                        json={
                            "chat_id": chat_id,
                            "message_id": message_id,
                            "text": f"✅ <b>Налаштування збережено!</b>\n\nАктивні категорії: <code>{cats_str}</code>",
                            "parse_mode": "HTML"
                        }
                    )
                return

            # Навігація меню фільтрів
            if cb_data == "back_to_filters_menu":
                res = (await asyncio.to_thread(lambda: supabase.table("telegram_subscribers").select("*").eq("chat_id", chat_id).execute())).data
                sub_fresh = res[0] if res else access["subscriber"]
                await client.post(
                    f"https://api.telegram.org/bot{bot_token}/editMessageText",
                    json={
                        "chat_id": chat_id,
                        "message_id": message_id,
                        "text": format_user_filters_view(sub_fresh),
                        "parse_mode": "HTML",
                        "reply_markup": get_filters_dashboard_keyboard()
                    }
                )
                await client.post(f"https://api.telegram.org/bot{bot_token}/answerCallbackQuery", json={"callback_query_id": cq_id})
                return

            if cb_data == "menu_discount":
                curr_d = (access["subscriber"] or {}).get("min_saving_percent") or 10
                await client.post(
                    f"https://api.telegram.org/bot{bot_token}/editMessageText",
                    json={
                        "chat_id": chat_id,
                        "message_id": message_id,
                        "text": "<b>Оберіть мінімальний відсоток вигоди від ринку:</b>",
                        "parse_mode": "HTML",
                        "reply_markup": get_discount_inline_keyboard(curr_d)
                    }
                )
                await client.post(f"https://api.telegram.org/bot{bot_token}/answerCallbackQuery", json={"callback_query_id": cq_id})
                return

            if cb_data.startswith("set_discount_"):
                new_val = int(cb_data.replace("set_discount_", ""))
                await asyncio.to_thread(lambda: supabase.table("telegram_subscribers").update({"min_saving_percent": new_val}).eq("chat_id", chat_id).execute())
                await client.post(f"https://api.telegram.org/bot{bot_token}/answerCallbackQuery", json={"callback_query_id": cq_id, "text": f"Знижку встановлено: від {new_val}%"})
                res = (await asyncio.to_thread(lambda: supabase.table("telegram_subscribers").select("*").eq("chat_id", chat_id).execute())).data
                sub_fresh = res[0] if res else access["subscriber"]
                await client.post(
                    f"https://api.telegram.org/bot{bot_token}/editMessageText",
                    json={"chat_id": chat_id, "message_id": message_id, "text": format_user_filters_view(sub_fresh), "parse_mode": "HTML", "reply_markup": get_filters_dashboard_keyboard()}
                )
                return

            if cb_data == "menu_sockets":
                curr_socks = (access["subscriber"] or {}).get("target_sockets") or []
                await client.post(
                    f"https://api.telegram.org/bot{bot_token}/editMessageText",
                    json={"chat_id": chat_id, "message_id": message_id, "text": "<b>Оберіть сокети процесора для сповіщень:</b>", "parse_mode": "HTML", "reply_markup": get_sockets_inline_keyboard(curr_socks)}
                )
                await client.post(f"https://api.telegram.org/bot{bot_token}/answerCallbackQuery", json={"callback_query_id": cq_id})
                return

            if cb_data.startswith("toggle_socket_"):
                target_s = cb_data.replace("toggle_socket_", "").lower()
                curr_socks = list((access["subscriber"] or {}).get("target_sockets") or [])
                if target_s in curr_socks:
                    curr_socks.remove(target_s)
                else:
                    curr_socks.append(target_s)
                await asyncio.to_thread(lambda: supabase.table("telegram_subscribers").update({"target_sockets": curr_socks}).eq("chat_id", chat_id).execute())
                await client.post(
                    f"https://api.telegram.org/bot{bot_token}/editMessageReplyMarkup",
                    json={"chat_id": chat_id, "message_id": message_id, "reply_markup": get_sockets_inline_keyboard(curr_socks)}
                )
                await client.post(f"https://api.telegram.org/bot{bot_token}/answerCallbackQuery", json={"callback_query_id": cq_id, "text": f"Сокет: {target_s.upper()}"})
                return

            if cb_data == "clear_sockets":
                await asyncio.to_thread(lambda: supabase.table("telegram_subscribers").update({"target_sockets": []}).eq("chat_id", chat_id).execute())
                await client.post(f"https://api.telegram.org/bot{bot_token}/answerCallbackQuery", json={"callback_query_id": cq_id, "text": "Сокети скинуто (всі)"})
                await client.post(
                    f"https://api.telegram.org/bot{bot_token}/editMessageReplyMarkup",
                    json={"chat_id": chat_id, "message_id": message_id, "reply_markup": get_sockets_inline_keyboard([])}
                )
                return

            if cb_data == "menu_vram":
                curr_v = float((access["subscriber"] or {}).get("min_vram_gb") or 0)
                await client.post(
                    f"https://api.telegram.org/bot{bot_token}/editMessageText",
                    json={"chat_id": chat_id, "message_id": message_id, "text": "<b>Оберіть мінімальний обсяг VRAM відеокарти:</b>", "parse_mode": "HTML", "reply_markup": get_vram_inline_keyboard(curr_v)}
                )
                await client.post(f"https://api.telegram.org/bot{bot_token}/answerCallbackQuery", json={"callback_query_id": cq_id})
                return

            if cb_data.startswith("set_vram_"):
                new_vram = float(cb_data.replace("set_vram_", ""))
                await asyncio.to_thread(lambda: supabase.table("telegram_subscribers").update({"min_vram_gb": new_vram}).eq("chat_id", chat_id).execute())
                await client.post(f"https://api.telegram.org/bot{bot_token}/answerCallbackQuery", json={"callback_query_id": cq_id, "text": f"VRAM: {int(new_vram)}GB+" if new_vram > 0 else "Будь-який"})
                res = (await asyncio.to_thread(lambda: supabase.table("telegram_subscribers").select("*").eq("chat_id", chat_id).execute())).data
                sub_fresh = res[0] if res else access["subscriber"]
                await client.post(
                    f"https://api.telegram.org/bot{bot_token}/editMessageText",
                    json={"chat_id": chat_id, "message_id": message_id, "text": format_user_filters_view(sub_fresh), "parse_mode": "HTML", "reply_markup": get_filters_dashboard_keyboard()}
                )
                return

            if cb_data == "menu_cores":
                curr_c = int((access["subscriber"] or {}).get("min_cores") or 0)
                await client.post(
                    f"https://api.telegram.org/bot{bot_token}/editMessageText",
                    json={"chat_id": chat_id, "message_id": message_id, "text": "<b>Оберіть мінімальну кількість ядер CPU:</b>", "parse_mode": "HTML", "reply_markup": get_cores_inline_keyboard(curr_c)}
                )
                await client.post(f"https://api.telegram.org/bot{bot_token}/answerCallbackQuery", json={"callback_query_id": cq_id})
                return

            if cb_data.startswith("set_cores_"):
                new_c = int(cb_data.replace("set_cores_", ""))
                await asyncio.to_thread(lambda: supabase.table("telegram_subscribers").update({"min_cores": new_c}).eq("chat_id", chat_id).execute())
                await client.post(f"https://api.telegram.org/bot{bot_token}/answerCallbackQuery", json={"callback_query_id": cq_id, "text": f"Ядер: {new_c}+" if new_c > 0 else "Всі"})
                res = (await asyncio.to_thread(lambda: supabase.table("telegram_subscribers").select("*").eq("chat_id", chat_id).execute())).data
                sub_fresh = res[0] if res else access["subscriber"]
                await client.post(
                    f"https://api.telegram.org/bot{bot_token}/editMessageText",
                    json={"chat_id": chat_id, "message_id": message_id, "text": format_user_filters_view(sub_fresh), "parse_mode": "HTML", "reply_markup": get_filters_dashboard_keyboard()}
                )
                return

            if cb_data == "reset_all_filters":
                await asyncio.to_thread(lambda: supabase.table("telegram_subscribers").update({
                    "min_saving_percent": 10,
                    "min_price": 0,
                    "max_price": 1000000,
                    "target_sockets": [],
                    "target_brands": [],
                    "min_vram_gb": 0,
                    "min_cores": 0,
                    "categories": ["gpu", "cpu", "pc"]
                }).eq("chat_id", chat_id).execute())
                await client.post(f"https://api.telegram.org/bot{bot_token}/answerCallbackQuery", json={"callback_query_id": cq_id, "text": "Усі фільтри скинуто до стандартних!"})
                res = (await asyncio.to_thread(lambda: supabase.table("telegram_subscribers").select("*").eq("chat_id", chat_id).execute())).data
                sub_fresh = res[0] if res else access["subscriber"]
                await client.post(
                    f"https://api.telegram.org/bot{bot_token}/editMessageText",
                    json={"chat_id": chat_id, "message_id": message_id, "text": format_user_filters_view(sub_fresh), "parse_mode": "HTML", "reply_markup": get_filters_dashboard_keyboard()}
                )
                return

            if cb_data == "close_filters_view":
                await client.post(
                    f"https://api.telegram.org/bot{bot_token}/editMessageText",
                    json={"chat_id": chat_id, "message_id": message_id, "text": "✅ <b>Панель фільтрів закрито.</b>\nСповіщення надходитимуть за збереженими правилами.", "parse_mode": "HTML"}
                )
                await client.post(f"https://api.telegram.org/bot{bot_token}/answerCallbackQuery", json={"callback_query_id": cq_id})
                return
        return

    # 2. ОБРОБКА ПОВІДОМЛЕНЬ
    message = data.get("message", {})
    chat_id = message.get("chat", {}).get("id")
    text = (message.get("text") or "").strip()

    if not chat_id:
        logger.warning(f"⚠️ [TG] Оновлення не містить chat_id: {data}")
        return

    logger.info(f"💬 [TG Message] chat_id={chat_id}, text='{text}'")

    async with httpx.AsyncClient(timeout=10.0) as client:
        # АВТОРИЗАЦІЯ: /start auth_<token>
        if text.startswith("/start auth_"):
            token = text.replace("/start auth_", "").strip()
            logger.info(f"🔐 [TG Auth] Спроба споживання токена: {token[:8]}... для chat_id={chat_id}")

            def _consume():
                return supabase.rpc("consume_telegram_token", {"target_token": token}).execute()

            try:
                rpc_res = await asyncio.to_thread(_consume)
                user_id = rpc_res.data
                logger.info(f"🎯 [TG Auth RPC Result] user_id={user_id}")
            except Exception as exc:
                logger.error(f"❌ [TG Auth RPC ERROR]: {exc}", exc_info=True)
                user_id = None

            if not user_id:
                # Перевіряємо чи chat_id вже прив'язаний
                existing = await asyncio.to_thread(
                    lambda: supabase.table("telegram_subscribers").select("user_id").eq("chat_id", chat_id).execute()
                )
                if existing.data and existing.data[0].get("user_id"):
                    logger.info(f"ℹ️ [TG Auth] chat_id={chat_id} вже був прив'язаний раніше.")
                    resp = await client.post(
                        f"https://api.telegram.org/bot{bot_token}/sendMessage",
                        json={
                            "chat_id": chat_id,
                            "text": "✅ <b>Ваш акаунт вже успішно підключено до HuntingSmarter!</b>",
                            "parse_mode": "HTML",
                            "reply_markup": get_main_menu_keyboard()
                        }
                    )
                    logger.info(f"📤 [TG Send] статус відповіді бота: {resp.status_code}")
                    return

                logger.warning(f"⚠️ [TG Auth] Невалідний або прострочений токен: {token}")
                resp = await client.post(
                    f"https://api.telegram.org/bot{bot_token}/sendMessage",
                    json={
                        "chat_id": chat_id,
                        "text": "❌ <b>Посилання застаріло або вже використане.</b>\n\nЗгенеруйте нове посилання в кабінеті на сайті.",
                        "parse_mode": "HTML"
                    }
                )
                logger.info(f"📤 [TG Send Error Msg] статус: {resp.status_code}")
                return

            # Атомарна прив'язка 1:1
            def _link_sub():
                supabase.table("telegram_subscribers").delete().eq("user_id", user_id).neq("chat_id", chat_id).execute()
                supabase.table("telegram_subscribers").upsert({
                    "chat_id": chat_id,
                    "user_id": user_id,
                    "is_active": True,
                    "categories": ["gpu", "cpu", "pc"],
                    "updated_at": datetime.now(timezone.utc).isoformat()
                }, on_conflict="chat_id").execute()

                try:
                    supabase.table("profiles").update({
                        "telegram_connected": True,
                        "updated_at": datetime.now(timezone.utc).isoformat()
                    }).eq("id", user_id).execute()
                except Exception as e:
                    logger.warning(f"Не вдалося оновити profiles.telegram_connected: {e}")

            try:
                await asyncio.to_thread(_link_sub)
                logger.info(f"✅ [TG DB] Успішно записано в telegram_subscribers: user_id={user_id}, chat_id={chat_id}")
            except Exception as dberr:
                logger.error(f"❌ [TG DB INSERT ERROR]: {dberr}", exc_info=True)

            welcome_text = (
                "<b>✅ Акаунт успішно прив'язано до HuntingSmarter!</b>\n\n"
                "Бот активовано. Ви отримуватимете найвигідніші пропозиції заліза з дисконтом у реальному часі.\n\n"
                "Керуйте сповіщеннями за допомогою меню нижче:"
            )
            resp = await client.post(
                f"https://api.telegram.org/bot{bot_token}/sendMessage",
                json={
                    "chat_id": chat_id,
                    "text": welcome_text,
                    "parse_mode": "HTML",
                    "reply_markup": get_main_menu_keyboard()
                }
            )
            logger.info(f"📤 [TG Send Welcome] статус відповіді Telegram API: {resp.status_code}, тіло: {resp.text}")
            return

        # ПЕРЕВІРКА ПІДПИСКИ
        access = await check_telegram_subscriber_access(chat_id)
        logger.info(f"🔑 [TG Message Access] chat_id={chat_id}, allowed={access['allowed']}, reason={access.get('reason')}")

        if not access["allowed"]:
            if access["reason"] == "unauthorized":
                msg = (
                    "<b>🔒 Доступ обмежено</b>\n\n"
                    "Цей бот працює для авторизованих користувачів сервісу <b>HuntingSmarter</b>.\n\n"
                    "Увійдіть у свій Профіль на сайті та натисніть кнопку <b>«Під'єднати Telegram»</b>."
                )
            else:
                msg = (
                    "<b>⚠️ Термін дії підписки або тріалу завершився</b>\n\n"
                    "Щоб відновити отримання сповіщень та керування фільтрами, продовжіть підписку в особистому кабінеті."
                )
            resp = await client.post(
                f"https://api.telegram.org/bot{bot_token}/sendMessage",
                json={"chat_id": chat_id, "text": msg, "parse_mode": "HTML"}
            )
            logger.info(f"📤 [TG Denied Msg] статус: {resp.status_code}")
            return
        

        # КОМАНДИ
        if text in ("/help", "ℹ️ Що робить бот?"):
            help_text = (
                "<b>🤖 Що робить HuntingSmarter Bot?</b>\n\n"
                "• <b>24/7 Сканування:</b> Моніторить нові оголошення OLX кожні 3–5 секунд.\n"
                "• <b>Fair Price:</b> Розраховує справедливу ринкову ціну комплектуючих та ПК.\n"
                "• <b>Фільтрація:</b> Відсікає переоцінені лоти та ненадійних продавців.\n"
                "• <b>Миттєвий пуш:</b> Надсилає картку товару з прямою кнопкою купівлі."
            )
            resp = await client.post(
                f"https://api.telegram.org/bot{bot_token}/sendMessage",
                json={
                    "chat_id": chat_id,
                    "text": help_text,
                    "parse_mode": "HTML",
                    "reply_markup": get_main_menu_keyboard()
                }
            )
            logger.info(f"📤 [TG Help] статус: {resp.status_code}")
            return

        # ОБРОБКА ТЕКСТОВОЇ КОМАНДИ /price
        if text.startswith("/price"):
            parts = text.replace("/price", "").strip().split()
            if len(parts) >= 2 and parts[0].isdigit() and parts[1].isdigit():
                p_min = int(parts[0])
                p_max = int(parts[1])
                if p_max == 0:
                    p_max = 1000000
                if p_min > p_max:
                    p_min, p_max = p_max, p_min
                await asyncio.to_thread(lambda: supabase.table("telegram_subscribers").update({"min_price": p_min, "max_price": p_max}).eq("chat_id", chat_id).execute())
                await client.post(
                    f"https://api.telegram.org/bot{bot_token}/sendMessage",
                    json={"chat_id": chat_id, "text": f"✅ <b>Діапазон цін оновлено:</b> від {p_min:,} до {p_max:,} грн.".replace(",", " "), "parse_mode": "HTML"}
                )
            else:
                await client.post(
                    f"https://api.telegram.org/bot{bot_token}/sendMessage",
                    json={"chat_id": chat_id, "text": "⚠️ <b>Формат:</b> <code>/price 5000 25000</code>", "parse_mode": "HTML"}
                )
            return

        # ОБРОБКА ТЕКСТОВОЇ КОМАНДИ /keywords
        if text.startswith("/keywords"):
            kw_raw = text.replace("/keywords", "").strip()
            if not kw_raw or kw_raw.lower() in ("clear", "скинути", "reset", "none"):
                new_keywords = []
                msg = "✅ <b>Фільтр за моделями очищено!</b> Сповіщення надходитимуть по всіх моделях обраних категорій."
            else:
                new_keywords = [k.strip().lower() for k in kw_raw.split(",") if k.strip()]
                kw_list_str = ", ".join(new_keywords)
                msg = f"✅ <b>Встановлено фільтр моделей:</b> <code>{kw_list_str}</code>\nБот надсилатиме тільки лоти, що містять ці слова."

            await asyncio.to_thread(lambda: supabase.table("telegram_subscribers").update({"target_brands": new_keywords}).eq("chat_id", chat_id).execute())
            await client.post(
                f"https://api.telegram.org/bot{bot_token}/sendMessage",
                json={"chat_id": chat_id, "text": msg, "parse_mode": "HTML"}
            )
            return

        # КНОПКА: Мої фільтри (Виводимо повний інтерактивний дашборд)
        if text in ("/status", "⚙️ Мої фільтри"):
            sub_res = await asyncio.to_thread(lambda: supabase.table("telegram_subscribers").select("*").eq("chat_id", chat_id).execute())
            sub_data = sub_res.data[0] if sub_res.data else access["subscriber"]
            status_text = format_user_filters_view(sub_data)
            await client.post(
                f"https://api.telegram.org/bot{bot_token}/sendMessage",
                json={
                    "chat_id": chat_id,
                    "text": status_text,
                    "parse_mode": "HTML",
                    "reply_markup": get_filters_dashboard_keyboard()
                }
            )
            return

        if text in ("/categories", "🔧 Змінити категорії"):
            sub = access["subscriber"]
            active_cats = sub.get("categories") or ["gpu", "cpu", "pc"]
            resp = await client.post(
                f"https://api.telegram.org/bot{bot_token}/sendMessage",
                json={
                    "chat_id": chat_id,
                    "text": "<b>Оберіть категорії комплектуючих для сповіщень:</b>\n<i>(Натискайте на кнопки для ввімкнення / вимкнення)</i>",
                    "parse_mode": "HTML",
                    "reply_markup": get_categories_inline_keyboard(active_cats)
                }
            )
            logger.info(f"📤 [TG Categories] статус: {resp.status_code}")
            return

        # ДЕФОЛТ / /start
        profile_url = f"{FRONTEND_URL}/profile"
        resp = await client.post(
            f"https://api.telegram.org/bot{bot_token}/sendMessage",
            json={
                "chat_id": chat_id,
                "text": f"Головне меню активно. Оберіть дію на клавіатурі нижче або відкрийте <a href=\"{profile_url}\">особистий кабінет</a>:",
                "parse_mode": "HTML",
                "reply_markup": get_main_menu_keyboard()
            }
        )
        logger.info(f"📤 [TG Default / Menu] статус: {resp.status_code}")


# --- TELEGRAM LINK GENERATION ---
@app.post("/api/telegram/generate-link")
@limiter.limit("10/minute")
async def generate_telegram_link(
    request: Request,
    current_user: dict = Depends(get_current_user),
) -> dict[str, str]:
    """Генерує одноразовий токен (15 хв) для авторизації Telegram бота."""
    user_id = current_user.get("id")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Неавторизований користувач")

    token = secrets.token_urlsafe(32)
    expires_at = (datetime.now(timezone.utc) + timedelta(minutes=15)).isoformat()

    def _save_token():
        supabase.table("telegram_link_tokens").insert({
            "token": token,
            "user_id": user_id,
            "expires_at": expires_at,
        }).execute()

    try:
        await asyncio.to_thread(_save_token)
    except Exception as exc:
        logger.error(f"Помилка збереження токена для {user_id}: {exc}")
        raise HTTPException(status_code=500, detail="Не вдалося згенерувати токен підключення")

    bot_username = os.getenv("TELEGRAM_BOT_USERNAME", "HuntingSmarterBot").lstrip("@")
    return {"link": f"https://t.me/{bot_username}?start=auth_{token}"}



@app.post("/api/telegram/webhook")
async def telegram_webhook(request: Request):
    """Приймає оновлення від Telegram та логує кожен крок."""
    try:
        data = await request.json()
    except Exception as err:
        logger.error(f"❌ [TG Webhook] Помилка парсингу JSON: {err}")
        return {"ok": False}

    logger.info(f"📩 [TG Webhook INCOMING]: {data}")

    try:
        await process_telegram_update(data)
    except Exception as exc:
        logger.error(f"❌ [TG Webhook CRITICAL ERROR]: {exc}", exc_info=True)

    return {"ok": True}



@app.get("/api/ads")
@limiter.limit("60/minute")
async def get_ads(
    request: Request,
    limit: int = Query(default=40, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    category: str = Query(default="all"),
    min_price: float = Query(default=0),
    max_price: float = Query(default=100000),
    min_profit: float = Query(default=-10000),
    max_profit: float = Query(default=30000),
    city: str = Query(default=""),
    condition: str = Query(default="all"),
    seller_type: str = Query(default="all"),
    max_age_sec: int = Query(default=0),
    search_query: str = Query(default=""),
    pc_categories: str = Query(default=""),
    deal_statuses: str = Query(default=""),
    seller_risks: str = Query(default=""),
    min_seller_deals: int = Query(default=0),
    min_seller_rating: float = Query(default=0),
    min_account_age_years: int = Query(default=0),
    gpu_detected: str = Query(default=""),
    cpu_detected: str = Query(default=""),
    exclude_keywords: str = Query(default=""),
    current_user: dict = Depends(verify_active_subscription),
) -> dict[str, Any]:
    def _fetch():
        query = (
            supabase.table("ads")
            .select(PUBLIC_AD_COLUMNS, count="exact")
            .eq("status", "active")
        )

        if category != "all":
            query = query.eq("item_type", category)

        if min_price > 0:
            query = query.gte("price", min_price)
        if max_price < 100000:
            query = query.lte("price", max_price)

        if min_profit > -10000:
            query = query.gte("saving_uah", min_profit)
        if max_profit < 30000:
            query = query.lte("saving_uah", max_profit)

        if city.strip():
            query = query.ilike("city", f"%{city.strip()}%")

        if condition == "clean":
            query = query.eq("has_defects", 0)
        elif condition == "defects":
            query = query.gt("has_defects", 0)

        if seller_type != "all":
            query = query.eq("seller_type", seller_type)

        if max_age_sec > 0:
            threshold = (datetime.now(timezone.utc) - timedelta(seconds=max_age_sec)).isoformat()
            query = query.gte("created_at_olx", threshold)

        if search_query.strip():
            raw_sq = search_query.strip().lower()
            sq = re.sub(r"[\s\-]+", "_", raw_sq)

            is_gpu_code = bool(re.match(r"^(?:rx|rtx|gtx|arc|gt|hd|r[579]|vega)_\w+", sq))
            is_cpu_code = bool(re.match(r"^(?:i[3579]|ryzen_[3579]|r[3579]|core_ultra|xeon|fx|athlon)_\w+", sq))
            is_component_code = is_gpu_code or is_cpu_code or bool(re.match(r"^(?:b\d{3}|z\d{3}|x\d{3}|h\d{3}|a\d{3}|ram_\w+|ssd_\w+|hdd_\w+)", sq))

            if is_component_code:
                conditions = [
                    f"component_name.eq.{sq}",
                ]
                
                if category in ("pc", "all"):
                    if is_gpu_code:
                        conditions.append(f"gpu_detected.eq.{sq}")
                    if is_cpu_code:
                        conditions.append(f"cpu_detected.eq.{sq}")

                # Якщо вказано конкретний тип заліза (наприклад, category='gpu'), ПК взагалі відсікаються
                query = query.or_(",".join(conditions))
            else:
                # Звичайний текстовий пошук по словах
                query = query.ilike("title", f"%{search_query.strip()}%")



        if min_seller_deals > 0:
            query = query.gte("seller_successful_deals", min_seller_deals)

        if gpu_detected.strip():
            query = query.ilike("gpu_detected", f"%{gpu_detected.strip()}%")
        if cpu_detected.strip():
            query = query.ilike("cpu_detected", f"%{cpu_detected.strip()}%")

        if exclude_keywords.strip():
            keywords = [k.strip() for k in exclude_keywords.split(",") if k.strip()]
            for kw in keywords[:5]:
                query = query.not_.ilike("title", f"%{kw}%")

        if min_seller_rating > 0:
            rating_prefix = f"{float(min_seller_rating):.1f}"
            query = query.neq("seller_rating", "немає оцінок").gte("seller_rating", rating_prefix)

        if min_account_age_years > 0:
            current_year = datetime.now(timezone.utc).year
            max_allowed_year = str(current_year - min_account_age_years)
            query = query.neq("seller_created_at", "").lte("seller_created_at", max_allowed_year)

        if category == "pc" and pc_categories.strip():
            try:
                pc_map = json.loads(pc_categories)
                inc = [k for k, v in pc_map.items() if v == "include"]
                exc = [k for k, v in pc_map.items() if v == "exclude"]
                if inc:
                    query = query.in_("pc_category", inc)
                for item in exc:
                    query = query.neq("pc_category", item)
            except Exception:
                pass

        if deal_statuses.strip():
            try:
                deal_map = json.loads(deal_statuses)
                inc = [k for k, v in deal_map.items() if v == "include"]
                exc = [k for k, v in deal_map.items() if v == "exclude"]
                if inc:
                    query = query.in_("deal_status", inc)
                for item in exc:
                    query = query.neq("deal_status", item)
            except Exception:
                pass

        if seller_risks.strip():
            try:
                risk_map = json.loads(seller_risks)
                inc = [k for k, v in risk_map.items() if v == "include"]
                exc = [k for k, v in risk_map.items() if v == "exclude"]
                if inc:
                    query = query.in_("seller_risk_score", inc)
                for item in exc:
                    query = query.neq("seller_risk_score", item)
            except Exception:
                pass

        return (
            query.order("created_at_olx", desc=True, nullsfirst=False)
            .range(offset, offset + limit - 1)
            .execute()
        )

    try:
        response = await asyncio.to_thread(_fetch)
        rows = response.data or []
        total = response.count or 0
    except Exception as exc:
        logger.error(f"Помилка читання ads: {exc}")
        raise HTTPException(status_code=500, detail="Помилка завантаження оголошень")

    for ad in rows:
        ad.setdefault("seller_successful_deals", 0)
        ad.setdefault("seller_rating", "немає оцінок")
        ad.setdefault("seller_risk_score", "neutral")
        ad.setdefault("deal_status", "regular")

    return {
        "items": rows,
        "total_count": total,
        "limit": limit,
        "offset": offset,
    }


@app.get("/api/stats")
@limiter.limit("30/minute")
async def get_stats(
    request: Request,
    current_user: dict = Depends(verify_active_subscription),
) -> dict[str, Any]:
    today_start = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0).isoformat()

    def _fetch_stats():
        scanned = supabase.table("ads").select("id", count="exact").gte("created_at_olx", today_start).execute()
        deals = supabase.table("ads").select("id", count="exact").eq("status", "active").neq("deal_status", "regular").execute()
        return scanned.count or 0, deals.count or 0

    try:
        scanned_count, deals_count = await asyncio.to_thread(_fetch_stats)
    except Exception as exc:
        logger.error(f"Помилка читання статистики: {exc}")
        scanned_count, deals_count = 0, 0

    return {
        "scanned": scanned_count,
        "deals": deals_count,
        "avgDetectionSec": 3.1,
        "activeUsers": len(manager.active_connections),
    }


@app.get("/api/ads/{ad_id}")
@limiter.limit("60/minute")
async def get_single_ad(
    request: Request,
    ad_id: str,
    current_user: dict = Depends(verify_active_subscription),
) -> dict:
    clean_id = ad_id.strip()

    def _fetch_single():
        if clean_id.isdigit():
            target_id = int(clean_id)
            return supabase.table("ads").select(PUBLIC_AD_COLUMNS).or_(f"id.eq.{target_id},ad_id.eq.{target_id}").limit(1).execute()
        return supabase.table("ads").select(PUBLIC_AD_COLUMNS).eq("id", clean_id).limit(1).execute()

    try:
        response = await asyncio.to_thread(_fetch_single)
        rows = response.data or []
    except Exception as exc:
        logger.error(f"Помилка отримання лоту {clean_id}: {exc}")
        raise HTTPException(status_code=500, detail="Помилка завантаження лоту")

    if not rows:
        raise HTTPException(status_code=404, detail="Товар не знайдено")

    ad = rows[0]
    ad.setdefault("seller_successful_deals", 0)
    ad.setdefault("seller_rating", "немає оцінок")
    ad.setdefault("seller_risk_score", "neutral")
    ad.setdefault("deal_status", "regular")
    return ad


@app.get("/api/components/{name}/competitors")
@limiter.limit("40/minute")
async def get_component_competitors(
    request: Request,
    name: str,
    current_user: dict = Depends(verify_active_subscription),
) -> dict[str, Any]:
    clean_name = name.strip().lower()[:80]

    try:
        def _fetch_competitor_data():
            price_res = (
                supabase.table("component_prices")
                .select("id, component_name, price, competitor_ids, date")
                .ilike("component_name", f"%{clean_name}%")
                .order("date", desc=True)
                .order("id", desc=True)
                .limit(1)
                .execute()
            )
            price_rows = price_res.data or []
            fair_price, target_ids, date_calc = None, [], None

            if price_rows:
                latest = price_rows[0]
                fair_price = latest.get("price")
                date_calc = latest.get("date")
                raw_ids = latest.get("competitor_ids")
                if isinstance(raw_ids, str):
                    try:
                        raw_ids = json.loads(raw_ids)
                    except Exception:
                        raw_ids = []
                if isinstance(raw_ids, list):
                    target_ids = [int(str(i)) for i in raw_ids if str(i).strip().isdigit()][:10]

            if target_ids:
                ads_res = supabase.table("ads").select(PUBLIC_AD_COLUMNS).in_("ad_id", target_ids).limit(10).execute()
                return fair_price, date_calc, ads_res.data or []

            fallback_res = (
                supabase.table("ads")
                .select(PUBLIC_AD_COLUMNS)
                .ilike("component_name", f"%{clean_name}%")
                .order("price", desc=False)
                .limit(10)
                .execute()
            )
            return fair_price, date_calc, fallback_res.data or []

        fair_price, date_calc, competitors = await asyncio.to_thread(_fetch_competitor_data)

        return {
            "component_name": clean_name,
            "fair_price": fair_price,
            "date_calculated": date_calc,
            "count": len(competitors),
            "competitors": competitors,
        }
    except Exception as exc:
        logger.error(f"Помилка аналітики конкурентів: {exc}")
        raise HTTPException(status_code=500, detail="Помилка розрахунку ринкових цін")


@app.post("/api/trigger-new-ad", dependencies=[Depends(verify_internal_secret)])
@limiter.limit("300/minute")
async def trigger_new_ad(
    request: Request,
    payload: Union[List[NewAdModel], NewAdModel] = Body(...),
) -> dict[str, str]:
    if isinstance(payload, list):
        for ad in payload:
            await manager.broadcast(ad.model_dump())
    else:
        await manager.broadcast(payload.model_dump())

    return {"status": "broadcasted"}



@app.post("/api/payments/create-invoice")
@limiter.limit("10/minute")
async def create_payment_invoice(
    request: Request,
    payload: CreateInvoiceRequest,
    current_user: dict = Depends(get_current_user),
) -> dict[str, Any]:
    user_id = current_user.get("id")
    plan = PLANS.get(payload.plan_type)
    if not plan:
        raise HTTPException(status_code=400, detail="Невірний тарифний план")

    if not MONOBANK_TOKEN:
        raise HTTPException(status_code=500, detail="Monobank токен не налаштовано на сервері")

    mono_payload = {
        "amount": plan["amount_kop"],
        "ccy": 980, # UAH
        "merchantPaymInfo": {
            "reference": f"sub_{user_id}_{int(datetime.now(timezone.utc).timestamp())}",
            "destination": plan["title"],
            "basketOrder": [
                {
                    "name": plan["title"],
                    "qty": 1,
                    "sum": plan["amount_kop"],
                    "unit": "шт.",
                }
            ],
        },
        "redirectUrl": f"{FRONTEND_URL}/dashboard?payment=success",
        "webHookUrl": f"{APP_PUBLIC_URL}/api/payments/monobank-webhook",
        "validity": 3600,
        "paymentType": "debit",
    }

    headers = {"X-Token": MONOBANK_TOKEN}

    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                "https://api.monobank.ua/api/merchant/invoice/create",
                json=mono_payload,
                headers=headers,
                timeout=10.0,
            )
            if resp.status_code != 200:
                logger.error(f"Mono create invoice error: {resp.text}")
                raise HTTPException(status_code=502, detail="Помилка платіжного шлюзу Monobank")
            
            mono_data = resp.json()
            invoice_id = mono_data.get("invoiceId")
            page_url = mono_data.get("pageUrl")
    except HTTPException:
        raise
    except Exception as exc:
        logger.error(f"Помилка створення інвойсу: {exc}")
        raise HTTPException(status_code=500, detail="Не вдалося створити платіж")

    # Зберігаємо інвойс у БД
    def _save_payment():
        supabase.table("payments").insert({
            "user_id": user_id,
            "invoice_id": invoice_id,
            "plan_type": payload.plan_type,
            "amount_kop": plan["amount_kop"],
            "status": "created",
            "page_url": page_url,
        }).execute()

    await asyncio.to_thread(_save_payment)

    return {"invoice_id": invoice_id, "page_url": page_url}


@app.post("/api/payments/monobank-webhook")
async def monobank_webhook(request: Request) -> dict[str, str]:
    """Приймає статус оплати від Monobank та активує підписку."""
    try:
        data = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON")

    invoice_id = data.get("invoiceId")
    status_mono = data.get("status") # 'success', 'failure', 'reversed', etc.

    if not invoice_id:
        return {"status": "ignored"}

    logger.info(f"💳 [Mono Webhook]: Invoice {invoice_id} status={status_mono}")

    def _process_payment():
        # 1. Знаходимо запис платежу
        res = supabase.table("payments").select("*").eq("invoice_id", invoice_id).limit(1).execute()
        if not res.data:
            return None
        payment = res.data[0]
        
        # Оновлюємо статус платежу
        supabase.table("payments").update({
            "status": status_mono,
            "updated_at": datetime.now(timezone.utc).isoformat(),
        }).eq("invoice_id", invoice_id).execute()

        if status_mono == "success":
            user_id = payment["user_id"]
            plan_type = payment["plan_type"]
            days_to_add = PLANS.get(plan_type, {}).get("days", 30)

            # Отримуємо поточну підписку користувача
            sub_res = supabase.table("subscriptions").select("*").eq("user_id", user_id).limit(1).execute()
            now = datetime.now(timezone.utc)
            base_date = now

            if sub_res.data:
                current_sub = sub_res.data[0]
                current_sub_end = current_sub.get("subscription_end")
                if current_sub_end:
                    parsed_end = datetime.fromisoformat(current_sub_end.replace("Z", "+00:00"))
                    if parsed_end > now:
                        base_date = parsed_end # продовжуємо існуючу, якщо вона ще активна

            new_sub_end = base_date + timedelta(days=days_to_add)

            supabase.table("subscriptions").upsert({
                "user_id": user_id,
                "plan_type": plan_type,
                "status": "active",
                "subscription_end": new_sub_end.isoformat(),
                "updated_at": now.isoformat(),
            }, on_conflict="user_id").execute()
            logger.info(f"✅ Підписку користувача {user_id} активовано/продовжено до {new_sub_end}")

        return True

    try:
        await asyncio.to_thread(_process_payment)
    except Exception as exc:
        logger.error(f"Помилка обробки вебхука Mono: {exc}")
        return {"status": "error"}

    return {"status": "ok"}



# --- WEBSOCKET ЕНДПОІНТ ---
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, token: str = Query(None)):
    if not token:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    user_id = None
    if SUPABASE_JWT_SECRET:
        try:
            payload = jwt.decode(token, SUPABASE_JWT_SECRET, algorithms=["HS256"], audience="authenticated")
            user_id = payload.get("sub")
        except jwt.PyJWTError:
            user_id = None
    else:
        try:
            user_response = await asyncio.to_thread(supabase.auth.get_user, token)
            if user_response and user_response.user and user_response.user.id:
                user_id = user_response.user.id
        except Exception:
            user_id = None

    if not user_id:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    # Перевірка підписки для WebSocket клієнта
    def _check_ws_sub():
        res = (
            supabase.table("subscriptions")
            .select("status, trial_end, subscription_end")
            .eq("user_id", user_id)
            .limit(1)
            .execute()
        )
        return res.data[0] if res.data else None

    try:
        sub = await asyncio.to_thread(_check_ws_sub)
        now = datetime.now(timezone.utc)
        has_access = False

        if sub:
            if sub.get("trial_end"):
                t_end = datetime.fromisoformat(sub["trial_end"].replace("Z", "+00:00"))
                if now <= t_end:
                    has_access = True
            if sub.get("subscription_end") and not has_access:
                s_end = datetime.fromisoformat(sub["subscription_end"].replace("Z", "+00:00"))
                if now <= s_end:
                    has_access = True

        if not has_access:
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            return
    except Exception:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    # Атомарна перевірка та реєстрація з'єднання
    if not await manager.try_connect(websocket):
        await websocket.close(code=status.WS_1013_TRY_AGAIN_LATER)
        return

    await websocket.accept()
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        await manager.disconnect(websocket)
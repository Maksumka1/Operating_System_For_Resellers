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
    "competitor_price,saving_uah,saving_percent,deal_status,evaluated_at"
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
    url: str = Field(..., max_length=2048)
    title: str = Field(..., max_length=500)
    description: str | None = Field(default="", max_length=10000)
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
            sq = search_query.strip().lower().replace("-", "_").replace(" ", "_")
            
            # Якщо користувач шукає конкретну модель (наприклад rx_6600, rtx_3060, i7_7700)
            is_hardware_code = bool(re.match(r"^(?:rx|rtx|gtx|i[3579]|ryzen|r[3579])_\w+", sq))
            
            if is_hardware_code:
                query = query.or_(
                    f"gpu_detected.eq.{sq},"
                    f"cpu_detected.eq.{sq},"
                    f"component_name.eq.{sq},"
                    f"title.ilike.% {search_query.strip()} %,"
                    f"title.ilike.{search_query.strip()} %,"
                    f"title.ilike.% {search_query.strip()}"
                )
            else:
                # Звичайний текстовий пошук по тайтлу
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
    payload: Union[List[NewAdModel], NewAdModel] = Body(..., max_length=500),
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
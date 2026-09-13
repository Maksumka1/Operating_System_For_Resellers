"""
services/telegram_notifier.py — Сервіс сповіщень та взаємодії Telegram Bot
"""

from __future__ import annotations

import asyncio
import html
import logging
import os
from datetime import datetime, timezone
from typing import Any, List
import httpx
from dotenv import load_dotenv
from supabase import Client, create_client

logger = logging.getLogger("telegram_notifier")

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
SUPABASE_URL = os.getenv("SUPABASE_URL", "").strip()
SUPABASE_KEY = os.getenv("SUPABASE_SECRET_KEY", "").strip()

supabase: Client | None = None
if SUPABASE_URL and SUPABASE_KEY:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


class TelegramNotifierService:
    def __init__(self, bot_token: str, client: Client | None = supabase) -> None:
        self.bot_token = bot_token
        self.api_url = f"https://api.telegram.org/bot{bot_token}"
        self._client = client

    def format_deal_message(self, ad: dict[str, Any]) -> str:
        # 1. Базові поля
        title = ad.get("title") or ad.get("component_name") or "Товар"
        price = f"{int(ad.get('price', 0)):,}".replace(",", " ")
        
        fair_price_raw = ad.get("estimated_fair_price") or ad.get("competitor_price") or 0
        fair_price = f"{int(fair_price_raw):,}".replace(",", " ")
        
        saving_pct = ad.get("saving_percent") or 0
        url = ad.get("url") or "https://www.olx.ua"
        seller_name = ad.get("seller_name") or "Приватна особа"
        deals = ad.get("seller_successful_deals") or 0

        # 2. Розрахунок часу публікації (⏱ Опубліковано)
        time_since_post = "тільки що"
        created_at_raw = ad.get("created_at_olx")
        if created_at_raw:
            try:
                dt = datetime.fromisoformat(created_at_raw.replace("Z", "+00:00"))
                now = datetime.now(timezone.utc)
                diff_sec = int((now - dt).total_seconds())
                if diff_sec < 60:
                    time_since_post = f"{max(1, diff_sec)} сек тому"
                elif diff_sec < 3600:
                    time_since_post = f"{diff_sec // 60} хв тому"
                elif diff_sec < 86400:
                    time_since_post = f"{diff_sec // 3600} год тому"
                else:
                    time_since_post = f"{diff_sec // 86400} дн тому"
            except Exception:
                time_since_post = "нещодавно"

        # 3. Онлайн продавця (береться з last_refresh_time або дефолт)
        last_seen = "нещодавно"
        refresh_raw = ad.get("last_refresh_time")
        if refresh_raw:
            try:
                dt_ref = datetime.fromisoformat(refresh_raw.replace("Z", "+00:00"))
                diff_ref_sec = int((datetime.now(timezone.utc) - dt_ref).total_seconds())
                if diff_ref_sec < 3600:
                    last_seen = f"{max(1, diff_ref_sec // 60)} хв тому"
                elif diff_ref_sec < 86400:
                    last_seen = f"{diff_ref_sec // 3600} год тому"
                else:
                    last_seen = f"{diff_ref_sec // 86400} дн тому"
            except Exception:
                last_seen = "нещодавно"

        # 4. Оцінка безпеки та технічний стан
        is_safe = ad.get("seller_risk_score") == "safe"
        is_broken = int(ad.get("has_defects") or 0) > 0

        # 5. Рекомендація на основі deal_status та відсотка економії
        deal_status = ad.get("deal_status") or "regular"
        if is_broken:
            verdict = "⚠️ Обережно (є дефекти)"
        elif deal_status == "🔥 SUPER DEAL" or saving_pct >= 20:
            verdict = "🚀 Забирати негайно (Super Deal)"
        elif deal_status == "⭐ GOOD DEAL" or saving_pct >= 10:
            verdict = "👍 Хороша ціна (Варто уваги)"
        elif deal_status == "❌ OVERPRICED" or saving_pct < 0:
            verdict = "❌ Дорого (Переплата)"
        else:
            verdict = "⚖️ Середня ринкова ціна"

        # 6. Збирання повідомлення
        msg = (
            f"🔥 <b>{html.escape(title)}</b>\n"
            f"💰 Ціна: <b>{price} грн</b>  |  📊 Ринкова: <b>{fair_price} грн</b>\n"
            f"📉 Вигідно на: <b>{saving_pct}%</b>  |  ⏱ Опубліковано: {time_since_post}\n"
            f"👤 Продавець: {html.escape(seller_name)}\n"
            f"   • Угод: {deals}  |  • Онлайн: {last_seen}\n"
            f"   • Оцінка: {'🟢 Безпечний' if is_safe else '🔴 Ризик'}\n"
            f"⚠️ Стан: {'🔧 Неробочий' if is_broken else '✅ Робочий'}\n"
            f"🎯 Рекомендація: <b>{verdict}</b>\n"
            f"🔗 <a href='{url}'>Відкрити оголошення</a>"
        )
        return msg

    async def fetch_subscribers_for_deal(self, item_type: str, saving_percent: int) -> List[int]:
        """Отримує chat_id активних користувачів з валідною підпискою та відповідними фільтрами."""
        if not self._client:
            return []

        def _query() -> List[int]:
            # Перевіряємо активних підписників, у кого обрана дана категорія та підходить поріг вигоди
            res = (
                self._client.table("telegram_subscribers")
                .select("chat_id, user_id, min_saving_percent, categories")
                .eq("is_active", True)
                .lte("min_saving_percent", saving_percent)
                .contains("categories", [item_type])
                .execute()
            )
            data = res.data or []
            if not data:
                return []

            # Фільтруємо за наявністю активної підписки/тріалу в subscriptions
            user_ids = [row["user_id"] for row in data if row.get("user_id")]
            if not user_ids:
                return [row["chat_id"] for row in data]

            sub_res = (
                self._client.table("subscriptions")
                .select("user_id, status, trial_end, subscription_end")
                .in_("user_id", user_ids)
                .execute()
            )
            # Дозволяємо надсилати користувачам з активною підпискою
            allowed_users = {
                s["user_id"] for s in (sub_res.data or [])
                if s.get("status") in ("trial", "month_1", "month_6", "active")
            }
            return [row["chat_id"] for row in data if row.get("user_id") in allowed_users]

        return await asyncio.to_thread(_query)

    async def send_notification(self, chat_id: int, text: str, http_client: httpx.AsyncClient) -> bool:
        """Надсилає повідомлення конкретному chat_id."""
        url = f"{self.api_url}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "HTML",
            "disable_web_page_preview": False,
        }
        try:
            resp = await http_client.post(url, json=payload, timeout=5.0)
            return resp.status_code == 200
        except Exception as e:
            logger.warning(f"Помилка надсилання в Telegram ({chat_id}): {e}")
            return False

    async def broadcast_deals(self, ads: List[dict[str, Any]]) -> int:
        """Фільтрує вигідні лоти та масово розсилає підписникам."""
        if not self.bot_token or not ads:
            return 0

        sent_count = 0
        async with httpx.AsyncClient() as http_client:
            for ad in ads:
                saving_pct = ad.get("saving_percent") or 0
                item_type = (ad.get("item_type") or "").lower()

                # Сповіщаємо тільки про реальні вигідні пропозиції (від 10% економії або deal_status)
                if saving_pct < 10 and ad.get("deal_status") not in ("🔥 SUPER DEAL", "⭐ GOOD DEAL"):
                    continue

                recipients = await self.fetch_subscribers_for_deal(item_type, saving_pct)
                if not recipients:
                    continue

                message_text = self.format_deal_message(ad)
                for chat_id in recipients:
                    success = await self.send_notification(chat_id, message_text, http_client)
                    if success:
                        sent_count += 1
                    # Захист від Telegram Rate Limit (макс 30 msg/sec)
                    await asyncio.sleep(0.04)

        return sent_count


# Інтерфейс для зміни категорій через кнопки бота
async def handle_category_toggle(chat_id: int, category: str) -> list[str]:
    """Перемикає категорію у підписника в базі."""
    if not supabase:
        return []

    def _db_op():
        res = supabase.table("telegram_subscribers").select("categories").eq("chat_id", chat_id).execute()
        current = res.data[0]["categories"] if res.data else ["gpu", "cpu", "pc"]
        
        if category in current:
            current.remove(category)
        else:
            current.append(category)

        supabase.table("telegram_subscribers").upsert({
            "chat_id": chat_id,
            "categories": current,
            "is_active": True
        }, on_conflict="chat_id").execute()
        return current

    return await asyncio.to_thread(_db_op)
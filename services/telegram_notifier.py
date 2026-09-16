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
        # 1. Назва товару (єдиний жирний заголовок)
        title = ad.get("title") or ad.get("component_name") or "Товар"
        clean_title = html.escape(title.strip())

        # 2. Ціна, ринкова вартість та відсоток економії
        price = f"{int(ad.get('price', 0)):,}".replace(",", " ")
        fair_price_raw = ad.get("estimated_fair_price") or ad.get("competitor_price") or 0
        fair_price = f"{int(fair_price_raw):,}".replace(",", " ")
        saving_pct = int(ad.get("saving_percent") or 0)
        
        pct_sign = "−" if saving_pct >= 0 else "+"
        price_line = f"<b>{price} грн</b> · ринок {fair_price} грн · {pct_sign}{abs(saving_pct)}%"

        # 3. Онлайн продавця (парсинг last_refresh_time)
        last_seen = "щойно"
        refresh_raw = ad.get("last_refresh_time")
        if refresh_raw:
            try:
                dt_ref = datetime.fromisoformat(refresh_raw.replace("Z", "+00:00"))
                diff_ref_sec = int((datetime.now(timezone.utc) - dt_ref).total_seconds())
                if diff_ref_sec < 60:
                    last_seen = "щойно"
                elif diff_ref_sec < 3600:
                    last_seen = f"{diff_ref_sec // 60} хв тому"
                elif diff_ref_sec < 86400:
                    last_seen = f"{diff_ref_sec // 3600} год тому"
                else:
                    last_seen = f"{diff_ref_sec // 86400} дн тому"
            except Exception:
                last_seen = "нещодавно"

        seller_name = html.escape(ad.get("seller_name") or "Приватна особа")
        deals = ad.get("seller_successful_deals") or 0
        seller_line = f"{seller_name} · угод {deals} · онлайн {last_seen}"

        # 4. Єдиний сигнал-вердикт
        is_safe = ad.get("seller_risk_score") == "safe"
        is_broken = int(ad.get("has_defects") or 0) > 0
        deal_status = ad.get("deal_status") or "regular"

        if is_broken:
            verdict = "🔧 Потребує ремонту"
        elif not is_safe or deals == 0:
            verdict = "⚠️ Ризик продавця"
        elif deal_status == "🔥 SUPER DEAL" or saving_pct >= 20:
            verdict = "🔥 Брати негайно"
        elif deal_status == "⭐ GOOD DEAL" or saving_pct >= 10:
            verdict = "👍 Варто уваги"
        else:
            verdict = "🔹 Звичайна ціна"

        # 5. Посилання внизу
        url = ad.get("url") or "https://www.olx.ua"
        link_line = f'<a href="{url}">Відкрити</a>'

        return f"<b>{clean_title}</b>\n\n{price_line}\n\n{seller_line}\n\n{verdict}\n\n{link_line}"

    async def fetch_subscribers_for_deal(self, item_type: str, saving_percent: int) -> List[int]:
        """Отримує chat_id активних користувачів з валідною підпискою та відповідними фільтрами."""
        if not self._client:
            return []

        def _query() -> List[int]:
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

            user_ids = [row["user_id"] for row in data if row.get("user_id")]
            if not user_ids:
                return [row["chat_id"] for row in data]

            sub_res = (
                self._client.table("subscriptions")
                .select("user_id, status, trial_end, subscription_end")
                .in_("user_id", user_ids)
                .execute()
            )
            allowed_users = {
                s["user_id"]
                for s in (sub_res.data or [])
                if s.get("status") in ("trial", "month_1", "month_6", "active")
            }
            return [row["chat_id"] for row in data if row.get("user_id") in allowed_users]

        return await asyncio.to_thread(_query)

    async def send_notification(
        self,
        chat_id: int,
        text: str,
        http_client: httpx.AsyncClient,
        photo_url: str | None = None
    ) -> bool:
        """Надсилає картку з фото (sendPhoto) або резервне текстове повідомлення (sendMessage)."""
        # Спроба відправити фотографію з підписом
        if photo_url:
            try:
                photo_payload = {
                    "chat_id": chat_id,
                    "photo": photo_url,
                    "caption": text,
                    "parse_mode": "HTML",
                }
                resp = await http_client.post(
                    f"{self.api_url}/sendPhoto",
                    json=photo_payload,
                    timeout=8.0
                )
                if resp.status_code == 200:
                    return True
                logger.warning(f"sendPhoto failed ({resp.status_code}): {resp.text}. Спроба fallback на sendMessage.")
            except Exception as e:
                logger.warning(f"Помилка відправки фото: {e}. Спроба fallback на sendMessage.")

        # Fallback: звичайне повідомлення без фото
        try:
            msg_payload = {
                "chat_id": chat_id,
                "text": text,
                "parse_mode": "HTML",
                "disable_web_page_preview": False,
            }
            resp = await http_client.post(
                f"{self.api_url}/sendMessage",
                json=msg_payload,
                timeout=5.0
            )
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

                if saving_pct < 10 and ad.get("deal_status") not in ("🔥 SUPER DEAL", "⭐ GOOD DEAL"):
                    continue

                recipients = await self.fetch_subscribers_for_deal(item_type, saving_pct)
                if not recipients:
                    continue

                message_text = self.format_deal_message(ad)
                
                # Отримання фото з полів оголошення
                photos_list = ad.get("photos") or []
                photo_url = ad.get("photo_url") or (photos_list[0] if photos_list else None)

                for chat_id in recipients:
                    success = await self.send_notification(
                        chat_id=chat_id,
                        text=message_text,
                        http_client=http_client,
                        photo_url=photo_url
                    )
                    if success:
                        sent_count += 1
                    # Telegram Rate Limit: до 30 повідомлень/сек
                    await asyncio.sleep(0.04)

        return sent_count


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
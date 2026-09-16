"""
services/telegram_notifier.py — Сервіс сповіщень та взаємодії Telegram Bot
Повністю захищена від падінь та адаптована до суворих вимог Telegram API версія.
"""

from __future__ import annotations

import asyncio
import html
import logging
import os
import re
from datetime import datetime, timezone
from typing import Any, List, Optional
from urllib.parse import urlparse

import httpx
from dotenv import load_dotenv
from supabase import Client, create_client

logger = logging.getLogger("telegram_notifier")

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
SUPABASE_URL = os.getenv("SUPABASE_URL", "").strip()
SUPABASE_KEY = os.getenv("SUPABASE_SECRET_KEY", "").strip()
FRONTEND_URL = os.getenv("FRONTEND_URL", "https://huntingsmarter.com").strip().rstrip("/")


def _safe_html(val: Any) -> str:
    """Безпечне перетворення будь-якого значення на екранований HTML-рядок."""
    if val is None:
        return ""
    return html.escape(str(val).strip(), quote=True)


def _strip_html_tags(text: str) -> str:
    """Видаляє всі HTML теги для аварійного fallback-надсилання."""
    return re.sub(r"<[^>]+>", "", text)


def _normalize_url(raw_url: Optional[str]) -> str:
    """Гарантує абсолютний валідний HTTP/HTTPS URL для Telegram Inline кнопок."""
    if not raw_url:
        return "https://www.olx.ua"
    url = str(raw_url).strip()
    if url.startswith("//"):
        url = f"https:{url}"
    elif not url.startswith("http://") and not url.startswith("https://"):
        if url.startswith("/"):
            url = f"https://www.olx.ua{url}"
        else:
            url = f"https://www.olx.ua/{url}"
    try:
        parsed = urlparse(url)
        if parsed.scheme in ("http", "https") and parsed.netloc:
            return url
    except Exception:
        pass
    return "https://www.olx.ua"


class TelegramNotifierService:
    def __init__(self, bot_token: str, client: Client | None = None) -> None:
        self.bot_token = bot_token.strip()
        self.api_url = f"https://api.telegram.org/bot{self.bot_token}"
        self._client = client
        if not self._client and SUPABASE_URL and SUPABASE_KEY:
            self._client = create_client(SUPABASE_URL, SUPABASE_KEY)

    def format_deal_message(self, ad: dict[str, Any]) -> str:
        # 1. Заголовок
        title = ad.get("title") or ad.get("component_name") or "Товар"
        clean_title = _safe_html(title)
        item_type = _safe_html(ad.get("item_type") or "hardware").upper()

        # 2. Ціни та розрахунок економії
        try:
            price_val = int(ad.get("price") or 0)
        except (ValueError, TypeError):
            price_val = 0
        price_str = f"{price_val:,}".replace(",", " ")

        fair_price_raw = ad.get("estimated_fair_price") or ad.get("competitor_price") or 0
        try:
            fair_price_val = int(fair_price_raw)
        except (ValueError, TypeError):
            fair_price_val = 0
        fair_price_str = f"{fair_price_val:,}".replace(",", " ")

        try:
            saving_pct = int(ad.get("saving_percent") or 0)
        except (ValueError, TypeError):
            saving_pct = 0

        try:
            saving_uah = int(ad.get("saving_uah") or (fair_price_val - price_val if fair_price_val > 0 else 0))
        except (ValueError, TypeError):
            saving_uah = fair_price_val - price_val if fair_price_val > 0 else 0

        saving_sign = "−" if saving_pct >= 0 else "+"

        # 3. Вердикт
        deal_status = str(ad.get("deal_status") or "")
        is_broken = int(ad.get("has_defects") or 0) > 0
        seller_risk = str(ad.get("seller_risk_score") or "neutral").lower()

        if is_broken:
            verdict_badge = "🔧 <b>Потребує ремонту / Дефекти</b>"
        elif seller_risk == "suspicious":
            verdict_badge = "⚠️ <b>Ризик продавця (новий або без відгуків)</b>"
        elif "SUPER" in deal_status or saving_pct >= 20:
            verdict_badge = "🔥 <b>SUPER DEAL — Гаряча пропозиція!</b>"
        elif "GOOD" in deal_status or saving_pct >= 10:
            verdict_badge = "⭐ <b>GOOD DEAL — Вигідна ціна</b>"
        else:
            verdict_badge = "🔹 <b>Звичайна ринкова ціна</b>"

        # 4. Специфікація заліза
        specs_lines: list[str] = []
        if ad.get("item_type") == "pc":
            for label, field in [
                ("CPU", "cpu_detected"),
                ("GPU", "gpu_detected"),
                ("RAM", "ram_detected"),
                ("Диск", "storage_detected"),
            ]:
                val = ad.get(field) or (ad.get("ssd_detected") if field == "storage_detected" else None)
                if val and str(val).strip().lower() not in ("unknown", "none", "null"):
                    specs_lines.append(f"  • {label}: <code>{_safe_html(val)}</code>")
        else:
            comp_name = ad.get("component_name")
            socket = ad.get("socket")
            if comp_name:
                specs_lines.append(f"  • Модель: <code>{_safe_html(comp_name)}</code>")
            if socket:
                specs_lines.append(f"  • Сокет: <code>{_safe_html(socket)}</code>")

        specs_block = ""
        if specs_lines:
            specs_block = "<b>Характеристики:</b>\n" + "\n".join(specs_lines) + "\n\n"

        # 5. Дані продавця та локація
        seller_name = _safe_html(ad.get("seller_name") or "Приватна особа")
        try:
            deals_count = int(ad.get("seller_successful_deals") or 0)
        except (ValueError, TypeError):
            deals_count = 0
        rating_str = _safe_html(ad.get("seller_rating") or "немає оцінок")

        last_seen = "щойно"
        refresh_raw = ad.get("last_refresh_time")
        if refresh_raw:
            try:
                dt_ref = datetime.fromisoformat(str(refresh_raw).replace("Z", "+00:00"))
                diff_sec = int((datetime.now(timezone.utc) - dt_ref).total_seconds())
                if diff_sec < 60:
                    last_seen = "щойно"
                elif diff_sec < 3600:
                    last_seen = f"{diff_sec // 60} хв тому"
                elif diff_sec < 86400:
                    last_seen = f"{diff_sec // 3600} год тому"
                else:
                    last_seen = f"{diff_sec // 86400} дн тому"
            except Exception:
                last_seen = "нещодавно"

        city = _safe_html(ad.get("city") or "Україна")
        saving_formatted = f"{saving_uah:,}".replace(",", " ")

        return (
            f"<b>[{item_type}]</b> <b>{clean_title}</b>\n\n"
            f"💰 <b>{price_str} грн</b>  (Ринок: {fair_price_str} грн)\n"
            f"📈 Профіт: <b>+{saving_formatted} грн</b> ({saving_sign}{abs(saving_pct)}%)\n\n"
            f"{verdict_badge}\n\n"
            f"{specs_block}"
            f"📍 {city} | 👤 {seller_name}\n"
            f"📦 OLX Угод: <b>{deals_count}</b> | Рейтинг: {rating_str}\n"
            f"🕒 Активність: {last_seen}"
        )

    def build_deal_keyboard(self, ad: dict[str, Any]) -> dict[str, Any]:
        target_url = _normalize_url(ad.get("url"))
        ad_id = ad.get("id") or ad.get("ad_id")
        web_link = _normalize_url(f"{FRONTEND_URL}/dashboard?ad={ad_id}" if ad_id else f"{FRONTEND_URL}/dashboard")

        buttons = [{"text": "🔗 Відкрити на OLX", "url": target_url}]
        if FRONTEND_URL and FRONTEND_URL.startswith("http"):
            buttons.append({"text": "📊 Деталі на сервісі", "url": web_link})

        return {"inline_keyboard": [buttons]}

    async def fetch_subscribers_for_deal(self, item_type: str, saving_percent: int) -> List[int]:
        if not self._client:
            return []

        def _query() -> List[int]:
            try:
                res = (
                    self._client.table("telegram_subscribers")
                    .select("chat_id, user_id, min_saving_percent, categories")
                    .eq("is_active", True)
                    .lte("min_saving_percent", saving_percent)
                    .contains("categories", [item_type])
                    .execute()
                )
            except Exception as e:
                logger.error(f"Помилка вибірки підписників: {e}")
                return []

            data = res.data or []
            if not data:
                return []

            user_ids = [row["user_id"] for row in data if row.get("user_id")]
            if not user_ids:
                return [row["chat_id"] for row in data]

            try:
                sub_res = (
                    self._client.table("subscriptions")
                    .select("user_id, status, trial_end, subscription_end")
                    .in_("user_id", user_ids)
                    .execute()
                )
                now = datetime.now(timezone.utc)
                allowed_users = set()
                for s in (sub_res.data or []):
                    u_id = s.get("user_id")
                    st = s.get("status")
                    t_end = s.get("trial_end")
                    s_end = s.get("subscription_end")

                    is_valid = False
                    if t_end:
                        try:
                            if now <= datetime.fromisoformat(t_end.replace("Z", "+00:00")):
                                is_valid = True
                        except Exception:
                            pass
                    if s_end and not is_valid:
                        try:
                            if now <= datetime.fromisoformat(s_end.replace("Z", "+00:00")):
                                is_valid = True
                        except Exception:
                            pass
                    if not t_end and not s_end and st in ("active", "trial", "month_1", "month_6"):
                        is_valid = True

                    if is_valid and u_id:
                        allowed_users.add(u_id)

                return [row["chat_id"] for row in data if row.get("user_id") in allowed_users]
            except Exception as e:
                logger.error(f"Помилка перевірки підписок для розсилки: {e}")
                return [row["chat_id"] for row in data]

        return await asyncio.to_thread(_query)

    async def send_notification(
        self,
        chat_id: int,
        text: str,
        http_client: httpx.AsyncClient,
        photo_url: str | None = None,
        reply_markup: dict[str, Any] | None = None,
    ) -> bool:
        """Надсилає повідомлення з дворівневим fallback на випадок збою розмітки Telegram."""
        # 1. Спроба відправити фото
        if photo_url and photo_url.startswith("http"):
            photo_payload: dict[str, Any] = {
                "chat_id": chat_id,
                "photo": photo_url,
                "caption": text,
                "parse_mode": "HTML",
            }
            if reply_markup:
                photo_payload["reply_markup"] = reply_markup

            try:
                resp = await http_client.post(f"{self.api_url}/sendPhoto", json=photo_payload, timeout=8.0)
                if resp.status_code == 200:
                    return True
                # Якщо помилка в HTML-сутностях, пробуємо без HTML
                if "can't parse entities" in resp.text:
                    photo_payload["caption"] = _strip_html_tags(text)
                    photo_payload.pop("parse_mode", None)
                    retry_resp = await http_client.post(f"{self.api_url}/sendPhoto", json=photo_payload, timeout=8.0)
                    if retry_resp.status_code == 200:
                        return True
            except Exception as e:
                logger.warning(f"sendPhoto error ({chat_id}): {e}")

        # 2. Fallback: текстове повідомлення
        msg_payload: dict[str, Any] = {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "HTML",
            "disable_web_page_preview": False,
        }
        if reply_markup:
            msg_payload["reply_markup"] = reply_markup

        try:
            resp = await http_client.post(f"{self.api_url}/sendMessage", json=msg_payload, timeout=6.0)
            if resp.status_code == 200:
                return True
            # Аварійний ретрай чистим текстом
            if "can't parse entities" in resp.text:
                msg_payload["text"] = _strip_html_tags(text)
                msg_payload.pop("parse_mode", None)
                retry_resp = await http_client.post(f"{self.api_url}/sendMessage", json=msg_payload, timeout=6.0)
                return retry_resp.status_code == 200
            return False
        except Exception as e:
            logger.warning(f"sendMessage error ({chat_id}): {e}")
            return False

    async def broadcast_deals(self, ads: List[dict[str, Any]]) -> int:
        if not self.bot_token or not ads:
            return 0

        sent_count = 0
        async with httpx.AsyncClient(timeout=10.0) as http_client:
            for ad in ads:
                try:
                    saving_pct = int(ad.get("saving_percent") or 0)
                except (ValueError, TypeError):
                    saving_pct = 0

                item_type = str(ad.get("item_type") or "").lower()

                if saving_pct < 10 and ad.get("deal_status") not in ("🔥 SUPER DEAL", "⭐ GOOD DEAL"):
                    continue

                recipients = await self.fetch_subscribers_for_deal(item_type, saving_pct)
                if not recipients:
                    continue

                message_text = self.format_deal_message(ad)
                keyboard = self.build_deal_keyboard(ad)

                photos_list = ad.get("photos") or []
                photo_url = ad.get("photo_url") or (photos_list[0] if photos_list else None)

                for chat_id in recipients:
                    success = await self.send_notification(
                        chat_id=chat_id,
                        text=message_text,
                        http_client=http_client,
                        photo_url=photo_url,
                        reply_markup=keyboard,
                    )
                    if success:
                        sent_count += 1
                    await asyncio.sleep(0.04)

        return sent_count


async def handle_category_toggle(chat_id: int, category: str, client: Optional[Client] = None) -> list[str]:
    """Атомарне та безпечне перемикання списку категорій."""
    db = client or create_client(SUPABASE_URL, SUPABASE_KEY) if SUPABASE_URL and SUPABASE_KEY else None
    if not db:
        return ["gpu", "cpu", "pc"]

    allowed_categories = {"gpu", "cpu", "ram", "storage", "pc", "psu"}
    if category not in allowed_categories:
        return ["gpu", "cpu", "pc"]

    def _db_op():
        try:
            res = db.table("telegram_subscribers").select("categories").eq("chat_id", chat_id).execute()
            current = res.data[0].get("categories") if res.data and res.data[0].get("categories") else ["gpu", "cpu", "pc"]

            if category in current:
                current.remove(category)
            else:
                current.append(category)

            db.table("telegram_subscribers").update({
                "categories": current,
                "is_active": True,
                "updated_at": datetime.now(timezone.utc).isoformat(),
            }).eq("chat_id", chat_id).execute()
            return current
        except Exception as e:
            logger.error(f"Помилка handle_category_toggle: {e}")
            return ["gpu", "cpu", "pc"]

    return await asyncio.to_thread(_db_op)
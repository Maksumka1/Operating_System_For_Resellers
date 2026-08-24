"""
core/competitor_finder.py — Швидкий виклик SQL RPC перерахунку конкурентів ПК
"""

import os
import sys
import asyncio
import logging
from pathlib import Path
from typing import Any, Optional
from dotenv import load_dotenv
from supabase import create_client

logger = logging.getLogger("orchestrator.competitor_finder")

project_root = Path(__file__).resolve().parent
if not (project_root / ".env").exists():
    project_root = project_root.parent
load_dotenv(project_root / ".env")

SUPABASE_URL = os.getenv("SUPABASE_URL", "").strip()
SUPABASE_KEY = os.getenv("SUPABASE_SECRET_KEY", "").strip()

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("Відсутні SUPABASE_URL або SUPABASE_SECRET_KEY у .env")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


async def main_async(db_lock: Optional[asyncio.Lock] = None, **kwargs: Any) -> int:
    """Викликає швидкий RPC-перерахунок конкурентів у PostgreSQL."""
    def _execute_rpc() -> int:
        res = supabase.rpc("recalculate_pc_competitors").execute()
        return int(res.data) if res.data is not None else 0

    try:
        if db_lock:
            async with db_lock:
                updated_count = await asyncio.to_thread(_execute_rpc)
        else:
            updated_count = await asyncio.to_thread(_execute_rpc)

        return updated_count

    except Exception as e:
        logger.error(f"Помилка виконання recalculate_pc_competitors RPC: {e}")
        raise


run = main_async


def main():
    if sys.platform == "win32":
        res = asyncio.run(main_async(), loop_factory=asyncio.SelectorEventLoop)
    else:
        res = asyncio.run(main_async())
    print(f"✅ Оновлено записів: {res}")


if __name__ == "__main__":
    main()
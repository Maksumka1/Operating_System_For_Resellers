"""
Component Price Analyzer — SQL In-Database Processing
"""

import os
import sys
import asyncio
import logging
from pathlib import Path
from typing import Any, Optional
from dotenv import load_dotenv
from supabase import create_client

logger = logging.getLogger("price_hardware")

project_root = Path(__file__).resolve().parent
if not (project_root / ".env").exists():
    project_root = project_root.parent
load_dotenv(project_root / ".env")

SUPABASE_URL = os.getenv("SUPABASE_URL", "").strip()
SUPABASE_KEY = os.getenv("SUPABASE_SECRET_KEY", "").strip()

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("Відсутні SUPABASE_URL або SUPABASE_SECRET_KEY у .env")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


async def main_async(db_lock: Optional[asyncio.Lock] = None, **kwargs: Any) -> list[dict]:
    """Викликає швидкий розрахунок ринкових цін на рівні БД через RPC."""
    def _execute_rpc() -> int:
        res = supabase.rpc("calculate_component_market_prices").execute()
        return res.data if res.data is not None else 0

    if db_lock:
        async with db_lock:
            updated_count = await asyncio.to_thread(_execute_rpc)
    else:
        updated_count = await asyncio.to_thread(_execute_rpc)

    logger.info(f"Оновлено/розраховано ринкових цін комплектуючих: {updated_count}")
    return [{"calculated_count": updated_count}]


def main() -> list[dict]:
    if sys.platform == "win32":
        return asyncio.run(main_async(), loop_factory=asyncio.SelectorEventLoop)
    return asyncio.run(main_async())


if __name__ == "__main__":
    main()
"""
Hardware Evaluator — SQL In-Database Evaluation
"""

import os
import sys
import asyncio
import logging
from pathlib import Path
from typing import Any, Optional
from dotenv import load_dotenv
from supabase import create_client

logger = logging.getLogger("hardware_evaluator")

project_root = Path(__file__).resolve().parent
if not (project_root / ".env").exists():
    project_root = project_root.parent
load_dotenv(project_root / ".env")

SUPABASE_URL = os.getenv("SUPABASE_URL", "").strip()
SUPABASE_KEY = os.getenv("SUPABASE_SECRET_KEY", "").strip()

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("Відсутні SUPABASE_URL або SUPABASE_SECRET_KEY у .env")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


async def main_async(db_lock: Optional[asyncio.Lock] = None, limit: int = 300, **kwargs: Any) -> list[int]:
    """Оцінює неоцінені комплектуючі через SQL RPC функцію."""
    def _execute_rpc() -> int:
        res = supabase.rpc("evaluate_hardware_deals_rpc", {"p_limit": limit}).execute()
        return res.data if res.data is not None else 0

    if db_lock:
        async with db_lock:
            updated_count = await asyncio.to_thread(_execute_rpc)
    else:
        updated_count = await asyncio.to_thread(_execute_rpc)

    logger.info(f"Оцінено комплектуючих за ітерацію: {updated_count}")
    return [1] * updated_count


def main() -> list[int]:
    if sys.platform == "win32":
        return asyncio.run(main_async(), loop_factory=asyncio.SelectorEventLoop)
    return asyncio.run(main_async())


if __name__ == "__main__":
    main()
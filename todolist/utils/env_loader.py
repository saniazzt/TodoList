from __future__ import annotations

import os
from dotenv import load_dotenv

load_dotenv()


def get_env_int(key: str, default: int) -> int:
    val = os.getenv(key)
    if val is None:
        return default
    try:
        return int(val)
    except ValueError:
        return default
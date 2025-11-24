from __future__ import annotations
import os
from dotenv import load_dotenv

load_dotenv()

def get_env(key: str, default: str | None = None) -> str | None:
    return os.getenv(key, default)

def get_env_int(key: str, default: int) -> int:
    v = os.getenv(key)
    if v is None:
        return default
    try:
        return int(v)
    except ValueError:
        return default
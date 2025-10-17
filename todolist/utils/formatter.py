from __future__ import annotations

from typing import Any


def success(msg: str) -> str:
    return f"[OK] {msg}"


def error(msg: str) -> str:
    return f"[ERROR] {msg}"


def info(msg: str) -> str:
    return f"[INFO] {msg}"


def format_entity(entity: Any) -> str:
    if hasattr(entity, "id") and hasattr(entity, "name"):
        return f"{entity.id} - {entity.name}"
    return str(entity)
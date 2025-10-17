from __future__ import annotations

from typing import Optional

from todolist.core.exceptions.invalid_entity import InvalidEntityError
from todolist.core.exceptions.limit_exceeded import LimitExceededError
from todolist.utils.env_loader import get_env_int
from todolist.storage.memory_storage import MemoryStorage


MAX_PROJECTS = get_env_int("MAX_NUMBER_OF_PROJECT", 10)


def validate_project_name(name: str, exclude_project_id: Optional[str] = None) -> None:
    if not name or len(name.strip()) == 0:
        raise InvalidEntityError("Project name cannot be empty.")
    if len(name) > 30:
        raise InvalidEntityError("Project name must be <= 30 characters.")
    storage = MemoryStorageSingleton.get_instance()
    existing = storage.find_project_by_name(name)
    if existing and existing.id != exclude_project_id:
        raise InvalidEntityError("Project name must be unique.")


def validate_project_limits() -> None:
    storage = MemoryStorageSingleton.get_instance()
    if len(storage.get_all_projects()) >= MAX_PROJECTS:
        raise LimitExceededError("Maximum number of projects reached.")


class MemoryStorageSingleton:
    _instance: MemoryStorage | None = None

    @classmethod
    def get_instance(cls) -> MemoryStorage:
        if cls._instance is None:
            cls._instance = MemoryStorage()
        return cls._instance
from __future__ import annotations

from typing import List, Optional

from todolist.core.entities.project import Project
from todolist.core.exceptions.invalid_entity import InvalidEntityError
from todolist.core.exceptions.limit_exceeded import LimitExceededError
from todolist.core.validators.project_validator import validate_project_name, validate_project_limits, MemoryStorageSingleton
from todolist.storage.memory_storage import MemoryStorage


class ProjectService:
    def __init__(self, storage: Optional[MemoryStorage] = None) -> None:
        self.storage = storage or MemoryStorageSingleton.get_instance()

    def create_project(self, name: str, description: str) -> Project:
        validate_project_name(name)
        validate_project_limits()
        proj = Project.create(name=name, description=description)
        self.storage.add_project(proj)
        return proj
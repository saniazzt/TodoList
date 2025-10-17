from __future__ import annotations

from datetime import date
from typing import Optional, List

from todolist.core.entities.task import Task
from todolist.core.exceptions.invalid_entity import InvalidEntityError
from todolist.core.validators.task_validator import (
    validate_task_title,
    validate_task_description,
    validate_status,
    validate_deadline,
)
from todolist.core.validators.project_validator import MemoryStorageSingleton
from todolist.storage.memory_storage import MemoryStorage


class TaskService:
    def __init__(self, storage: Optional[MemoryStorage] = None) -> None:
        self.storage = storage or MemoryStorageSingleton.get_instance()

    def add_task(self, project_id: str, title: str, description: str, deadline: Optional[date] = None) -> Task:
        validate_task_title(title)
        validate_task_description(description)
        validate_deadline(deadline)

        proj = self.storage.get_project(project_id)
        if proj is None:
            raise InvalidEntityError("Project not found.")

        task = Task.create(title=title, description=description, deadline=deadline)
        proj.add_task(task)
        return task

    
from __future__ import annotations

from datetime import date
from typing import Optional

from todolist.core.exceptions.invalid_entity import InvalidEntityError
from todolist.core.exceptions.limit_exceeded import LimitExceededError
from todolist.utils.env_loader import get_env_int
from todolist.storage.memory_storage import MemoryStorage


MAX_TASKS = get_env_int("MAX_NUMBER_OF_TASK", 100)
VALID_STATUSES = {"todo", "doing", "done"}


def validate_task_title(title: str) -> None:
    if not title or len(title.strip()) == 0:
        raise InvalidEntityError("Task title cannot be empty.")
    if len(title) > 30:
        raise InvalidEntityError("Task title must be <= 30 characters.")


def validate_task_description(description: str) -> None:
    if description is not None and len(description) > 150:
        raise InvalidEntityError("Task description must be <= 150 characters.")


def validate_status(status: str) -> None:
    if status not in VALID_STATUSES:
        raise InvalidEntityError(f"Status must be one of {VALID_STATUSES}.")


def validate_deadline(deadline: Optional[date]) -> None:
    if deadline is not None and not isinstance(deadline, date):
        raise InvalidEntityError("Deadline must be a date object.")


def validate_task_limits(project_id: str) -> None:
    storage = MemoryStorage()
    proj = storage.get_project(project_id)
    if proj and len(proj.tasks) >= MAX_TASKS:
        raise LimitExceededError("Maximum number of tasks for this project reached.")

from __future__ import annotations
from datetime import date
from todolist.exceptions.invalid_entity import InvalidEntityError
from todolist.exceptions.limit_exceeded import LimitExceededError
from todolist.repositories.abstract import TaskRepositoryInterface
from todolist.utils.env_loader import get_env_int

MAX_TASKS = get_env_int("MAX_NUMBER_OF_TASK", 100)
VALID_STATUSES = {"todo", "doing", "done"}


def validate_task_title(title: str) -> None:
    if not title or not title.strip():
        raise InvalidEntityError("Task title cannot be empty.")
    if len(title) > 30:
        raise InvalidEntityError("Task title must be <= 30 characters.")


def validate_task_description(description: str) -> None:
    if description is not None and len(description) > 150:
        raise InvalidEntityError("Task description must be <= 150 characters.")


def validate_task_status(status: str) -> None:
    if status not in VALID_STATUSES:
        raise InvalidEntityError(f"Invalid status '{status}'. Must be one of {VALID_STATUSES}.")


def validate_task_deadline(deadline: date | None) -> None:
    if deadline is not None and not isinstance(deadline, date):
        raise InvalidEntityError("Deadline must be a date object.")


def validate_task_limit(repo: TaskRepositoryInterface, project_id: int) -> None:
    tasks = repo.list_by_project(project_id)
    if len(tasks) >= MAX_TASKS:
        raise LimitExceededError("Maximum number of tasks for this project has been reached.")
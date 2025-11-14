from __future__ import annotations
from todolist.exceptions.invalid_entity import InvalidEntityError
from todolist.exceptions.limit_exceeded import LimitExceededError
from todolist.repositories.abstract import ProjectRepositoryInterface
from todolist.utils.env_loader import get_env_int

MAX_PROJECTS = get_env_int("MAX_NUMBER_OF_PROJECT", 10)


def validate_project_name(name: str) -> None:
    if not name or not name.strip():
        raise InvalidEntityError("Project name cannot be empty.")
    if len(name) > 30:
        raise InvalidEntityError("Project name must be <= 30 characters.")


def validate_project_uniqueness(repo: ProjectRepositoryInterface, name: str, exclude_project_id: int | None = None) -> None:
    existing = repo.find_by_name(name)
    if existing and existing.id != exclude_project_id:
        raise InvalidEntityError("Project name must be unique.")


def validate_project_limit(repo: ProjectRepositoryInterface) -> None:
    projects = repo.list()
    if len(projects) >= MAX_PROJECTS:
        raise LimitExceededError("Maximum number of projects reached.")
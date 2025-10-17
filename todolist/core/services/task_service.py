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
    
    def edit_task(
        self,
        project_id: str,
        task_id: str,
        title: Optional[str] = None,
        description: Optional[str] = None,
        status: Optional[str] = None,
        deadline: Optional[date] = None,
    ) -> Task:
        proj = self.storage.get_project(project_id)
        if proj is None:
            raise InvalidEntityError("Project not found.")
        task = proj.get_task(task_id)
        if task is None:
            raise InvalidEntityError("Task not found.")

        if title is not None:
            validate_task_title(title)
            task.title = title
        if description is not None:
            validate_task_description(description)
            task.description = description
        if status is not None:
            validate_status(status)
            task.status = status
        if deadline is not None:
            validate_deadline(deadline)
            task.deadline = deadline

        return task
    
    def delete_task(self, project_id: str, task_id: str) -> bool:
        proj = self.storage.get_project(project_id)
        if proj is None:
            raise InvalidEntityError("Project not found.")
        return proj.remove_task(task_id)
    
    def change_status(self, project_id: str, task_id: str, new_status: str) -> Task:
        proj = self.storage.get_project(project_id)
        if proj is None:
            raise InvalidEntityError("Project not found.")
        task = proj.get_task(task_id)
        if task is None:
            raise InvalidEntityError("Task not found.")
        validate_status(new_status)
        task.status = new_status
        return task

    
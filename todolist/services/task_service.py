from __future__ import annotations
from datetime import date, datetime
from typing import Optional, List
from todolist.repositories.abstract import TaskRepositoryInterface
from todolist.models.task import Task, TaskStatus
from todolist.models.project import Project
from todolist.validators.task_validator import (
    validate_task_title,
    validate_task_description,
    validate_task_status,
    validate_task_deadline,
    validate_task_limit,
)
from todolist.exceptions.not_found import NotFoundError


class TaskService:
    def __init__(self, repo: TaskRepositoryInterface):
        self.repo = repo

    def list_tasks(self, project: Project) -> List[Task]:
        return self.repo.list_by_project(project.id)

    def add_task(self, project: Project, title: str, description: str, deadline) -> Task:
        if not project:
            raise NotFoundError("Project not found.")

        validate_task_title(title)
        validate_task_description(description)
        validate_task_deadline(deadline)
        validate_task_limit(self.repo, project.id)

        task = Task(
            project_id=project.id,
            title=title,
            description=description,
            deadline=deadline,
            status=TaskStatus.todo,
        )
        return self.repo.add(task)

    def edit_task(
        self,
        project: Project,
        task_id: int,
        title: Optional[str],
        description: Optional[str],
        status: Optional[str],
        deadline,
    ) -> Task:
        if not project:
            raise NotFoundError("Project not found.")

        task = self.repo.get(task_id)
        if not task or task.project_id != project.id:
            raise NotFoundError("Task not found in this project.")

        if title is not None:
            validate_task_title(title)
            task.title = title

        if description is not None:
            validate_task_description(description)
            task.description = description

        if status is not None:
            validate_task_status(status)
            task.status = TaskStatus(status)
            if task.status == TaskStatus.done:
                task.closed_at = datetime.utcnow()

        if deadline is not None:
            validate_task_deadline(deadline)
            task.deadline = deadline

        return self.repo.update(task)

    def delete_task(self, project: Project, task_id: int) -> bool:
        if not project:
            raise NotFoundError("Project not found.")

        task = self.repo.get(task_id)
        if not task or task.project_id != project.id:
            return False

        return self.repo.delete(task_id)

    def change_status(self, project: Project, task_id: int, new_status: str) -> Task:
        if not project:
            raise NotFoundError("Project not found.")

        task = self.repo.get(task_id)
        if not task or task.project_id != project.id:
            raise NotFoundError("Task not found.")

        validate_task_status(new_status)

        task.status = TaskStatus(new_status)
        if task.status == TaskStatus.done:
            task.closed_at = datetime.utcnow()

        return self.repo.update(task)

    def autoclose_overdue(self) -> int:
        today = date.today()

        overdue_tasks = self.repo.db.query(Task).filter(Task.deadline < today, Task.status != "done").all()

        if not overdue_tasks:
            return 0

        for task in overdue_tasks:
            task.status = TaskStatus.done
            task.closed_at = datetime.utcnow()
            self.repo.update(task)

        return len(overdue_tasks)

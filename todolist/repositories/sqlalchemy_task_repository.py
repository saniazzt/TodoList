from __future__ import annotations
from datetime import date
from typing import List, Optional
from sqlalchemy.orm import Session
from todolist.models.task import Task, TaskStatus

class SqlAlchemyTaskRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def add(self, task: Task) -> Task:
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task

    def get(self, task_id: int) -> Optional[Task]:
        return self.db.get(Task, task_id)

    def list_by_project(self, project_id: int) -> List[Task]:
        return self.db.query(Task).filter(Task.project_id == project_id).order_by(Task.id).all()

    def delete(self, task_id: int) -> bool:
        obj = self.get(task_id)
        if not obj:
            return False
        self.db.delete(obj)
        self.db.commit()
        return True

    def update(self, task: Task) -> Task:
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task

    def list_overdue(self) -> List[Task]:
        today = date.today()
        return (
            self.db.query(Task)
            .filter(Task.deadline != None)
            .filter(Task.deadline < today)
            .filter(Task.status != TaskStatus.done)
            .all()
        )
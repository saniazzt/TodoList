from __future__ import annotations

from dataclasses import dataclass, field
from typing import List
import uuid
from todolist.core.entities.task import Task


@dataclass
class Project:
    id: str
    name: str
    description: str
    tasks: List[Task] = field(default_factory=list)

    @classmethod
    def create(cls, name: str, description: str) -> "Project":
        short_id = uuid.uuid4().hex[:4]
        return cls(id=short_id, name=name, description=description)
    
    def add_task(self, task: Task) -> None:
        self.tasks.append(task)

    def remove_task(self, task_id: str) -> bool:
        before = len(self.tasks)
        self.tasks = [t for t in self.tasks if t.id != task_id]
        return len(self.tasks) < before

    def get_task(self, task_id: str) -> Task | None:
        for t in self.tasks:
            if t.id == task_id:
                return t
        return None
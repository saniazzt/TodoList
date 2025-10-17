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

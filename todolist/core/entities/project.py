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
        return cls(id=str(uuid.uuid4()), name=name, description=description)

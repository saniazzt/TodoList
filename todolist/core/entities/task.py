from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Optional
import uuid


@dataclass
class Task:
    id: str
    title: str
    description: str
    status: str = "todo"
    deadline: Optional[date] = None

    @classmethod
    def create(
        cls,
        title: str,
        description: str,
        status: str = "todo",
        deadline: Optional[date] = None,
    ) -> "Task":
        short_id = uuid.uuid4().hex[:4]
        return cls(id=short_id, title=title, description=description, status=status, deadline=deadline)

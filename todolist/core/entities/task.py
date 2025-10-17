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
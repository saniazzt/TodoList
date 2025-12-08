from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime


class TaskResponse(BaseModel):
    id: int
    project_id: int
    title: str
    description: Optional[str]
    status: str
    deadline: Optional[date]
    closed_at: Optional[datetime]
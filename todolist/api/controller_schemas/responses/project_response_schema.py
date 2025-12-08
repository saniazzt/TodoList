from pydantic import BaseModel
from typing import Optional

class ProjectResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    tasks_count: int

from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

class TaskCreateRequest(BaseModel):
    title: str = Field(..., max_length=30)
    description: Optional[str] = Field(None, max_length=150)
    deadline: Optional[date] = None

class TaskEditRequest(BaseModel):
    title: Optional[str] = Field(None, max_length=30)
    description: Optional[str] = Field(None, max_length=150)
    status: Optional[str] = None
    deadline: Optional[date] = None

class TaskStatusRequest(BaseModel):
    status: str
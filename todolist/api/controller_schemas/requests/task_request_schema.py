from pydantic import BaseModel, Field
from typing import Optional
from datetime import date


class TaskCreateRequest(BaseModel):
    """Schema for creating a new task within a project."""

    title: str = Field(..., max_length=30, description="Task title (max 30 characters)")
    description: Optional[str] = Field(None, max_length=150, description="Task description (max 150 characters)")
    deadline: Optional[date] = Field(None, description="Task deadline in YYYY-MM-DD format")

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "Design mockups",
                "description": "Create high-fidelity mockups for the new landing page",
                "deadline": "2025-12-15",
            }
        }
    }


class TaskEditRequest(BaseModel):
    """Schema for editing an existing task."""

    title: Optional[str] = Field(None, max_length=30, description="Updated task title (max 30 characters)")
    description: Optional[str] = Field(None, max_length=150, description="Updated task description (max 150 characters)")
    status: Optional[str] = Field(None, description="Task status: 'todo', 'doing', or 'done'")
    deadline: Optional[date] = Field(None, description="Updated deadline in YYYY-MM-DD format")

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "Design mockups v2",
                "status": "doing",
                "deadline": "2025-12-20",
            }
        }
    }


class TaskStatusRequest(BaseModel):
    """Schema for changing a task's status."""

    status: str = Field(..., description="Task status: 'todo', 'doing', or 'done'")

    model_config = {
        "json_schema_extra": {
            "example": {
                "status": "done",
            }
        }
    }
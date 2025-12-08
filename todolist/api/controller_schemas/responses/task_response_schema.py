from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, datetime


class TaskResponse(BaseModel):
    """Response schema for a task."""

    id: int = Field(..., description="Unique task identifier")
    project_id: int = Field(..., description="ID of the project this task belongs to")
    title: str = Field(..., description="Task title")
    description: Optional[str] = Field(None, description="Task description")
    status: str = Field(..., description="Task status: 'todo', 'doing', or 'done'")
    deadline: Optional[date] = Field(None, description="Task deadline date in YYYY-MM-DD format")
    closed_at: Optional[datetime] = Field(None, description="ISO 8601 timestamp when task was marked as done")

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 1,
                "project_id": 1,
                "title": "Design mockups",
                "description": "Create high-fidelity mockups for the new landing page",
                "status": "done",
                "deadline": "2025-12-15",
                "closed_at": "2025-12-10T14:30:00",
            }
        }
    }
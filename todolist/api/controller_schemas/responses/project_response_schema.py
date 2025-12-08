from pydantic import BaseModel, Field
from typing import Optional


class ProjectResponse(BaseModel):
    """Response schema for a project."""

    id: int = Field(..., description="Unique project identifier")
    name: str = Field(..., description="Project name")
    description: Optional[str] = Field(None, description="Project description")
    tasks_count: int = Field(..., description="Number of tasks in the project")

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 1,
                "name": "Website Redesign",
                "description": "Complete redesign of the company website",
                "tasks_count": 5,
            }
        }
    }

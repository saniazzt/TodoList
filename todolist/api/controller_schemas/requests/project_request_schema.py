from pydantic import BaseModel, Field
from typing import Optional


class ProjectCreateRequest(BaseModel):
    """Schema for creating a new project."""

    name: str = Field(..., max_length=30, description="Project name (max 30 characters)")
    description: Optional[str] = Field(None, max_length=150, description="Project description (max 150 characters)")

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "Website Redesign",
                "description": "Complete redesign of the company website",
            }
        }
    }


class ProjectEditRequest(BaseModel):
    """Schema for editing an existing project."""

    name: str = Field(..., max_length=30, description="Updated project name (max 30 characters)")
    description: Optional[str] = Field(None, max_length=150, description="Updated project description (max 150 characters)")

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "Website Redesign v2",
                "description": "Redesign with improved UX and performance",
            }
        }
    }

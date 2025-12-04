from pydantic import BaseModel, Field
from typing import Optional

class ProjectCreateRequest(BaseModel):
    name: str = Field(..., max_length=30)
    description: Optional[str] = Field(None, max_length=150)

class ProjectEditRequest(BaseModel):
    name: str = Field(..., max_length=30)
    description: Optional[str] = Field(None, max_length=150)

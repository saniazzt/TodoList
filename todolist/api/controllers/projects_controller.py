from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from todolist.api.controller_schemas.requests.project_request_schema import ProjectCreateRequest, ProjectEditRequest
from todolist.api.controller_schemas.responses.project_response_schema import ProjectResponse
from todolist.db.session import SessionLocal
from todolist.repositories.sqlalchemy_project_repository import SqlAlchemyProjectRepository
from todolist.services.project_service import ProjectService

router = APIRouter(prefix="/api/projects", tags=["projects"])

def get_project_service():
    db = SessionLocal()
    try:
        repo = SqlAlchemyProjectRepository(db)
        svc = ProjectService(repo)
        yield svc
    finally:
        db.close()

@router.get("/", response_model=List[ProjectResponse])
def list_projects(svc: ProjectService = Depends(get_project_service)):
    """
    Retrieve all projects.

    Returns a list of all projects with their task counts.
    """
    projects = svc.list_projects()
    return [ProjectResponse(id=p.id, name=p.name, description=p.description, tasks_count=len(p.tasks)) for p in projects]

@router.post("/", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
def create_project(payload: ProjectCreateRequest, svc: ProjectService = Depends(get_project_service)):
    """
    Create a new project.

    - **name**: Project name (required, max 30 characters)
    - **description**: Optional project description (max 150 characters)

    Returns the created project with its ID and initial task count (0).
    """
    try:
        p = svc.create_project(payload.name, payload.description or "")
        return ProjectResponse(id=p.id, name=p.name, description=p.description, tasks_count=len(p.tasks))
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))

@router.put("/{project_id}", response_model=ProjectResponse)
def edit_project(project_id: int, payload: ProjectEditRequest, svc: ProjectService = Depends(get_project_service)):
    """
    Edit an existing project.

    - **project_id**: Project ID (path parameter)
    - **name**: Updated project name (required, max 30 characters)
    - **description**: Updated project description (max 150 characters)

    Returns the updated project.
    """
    try:
        p = svc.edit_project(project_id, payload.name, payload.description or "")
        return ProjectResponse(id=p.id, name=p.name, description=p.description, tasks_count=len(p.tasks))
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))

@router.delete("/{project_id}")
def delete_project(project_id: int, svc: ProjectService = Depends(get_project_service)):
    """
    Delete a project by ID.

    - **project_id**: Project ID to delete (path parameter)

    When a project is deleted, all associated tasks are automatically deleted (cascade delete).
    Returns a success status.
    """
    ok = svc.delete_project(project_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Project not found")
    return {"status": "deleted"}
    

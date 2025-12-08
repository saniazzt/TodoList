from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from todolist.api.controller_schemas.requests.task_request_schema import TaskCreateRequest, TaskEditRequest, TaskStatusRequest
from todolist.api.controller_schemas.responses.task_response_schema import TaskResponse
from todolist.db.session import SessionLocal
from todolist.repositories.sqlalchemy_task_repository import SqlAlchemyTaskRepository
from todolist.services.task_service import TaskService
from todolist.repositories.sqlalchemy_project_repository import SqlAlchemyProjectRepository

router = APIRouter(prefix="/api/tasks", tags=["tasks"])

def get_task_service():
    db = SessionLocal()
    try:
        repo = SqlAlchemyTaskRepository(db)
        p_repo = SqlAlchemyProjectRepository(db)
        svc = TaskService(repo)
        yield svc, p_repo
    finally:
        db.close()

@router.get("/project/{project_id}", response_model=List[TaskResponse])
def list_tasks(project_id: int, deps = Depends(get_task_service)):
    """
    Retrieve all tasks for a specific project.

    - **project_id**: Project ID (path parameter)

    Returns a list of all tasks in the project, including their status, deadline, and closed timestamp.
    """
    svc, p_repo = deps
    project = p_repo.get(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    tasks = svc.list_tasks(project)
    return [
        TaskResponse(
            id=t.id,
            project_id=t.project_id,
            title=t.title,
            description=t.description,
            status=t.status.value if hasattr(t.status, "value") else str(t.status),
            deadline=t.deadline,
            closed_at=t.closed_at,
        )
        for t in tasks
    ]

@router.post("/project/{project_id}", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def add_task(project_id: int, payload: TaskCreateRequest, deps = Depends(get_task_service)):
    """
    Create a new task within a project.

    - **project_id**: Project ID (path parameter)
    - **title**: Task title (required, max 30 characters)
    - **description**: Optional task description (max 150 characters)
    - **deadline**: Optional deadline in YYYY-MM-DD format

    Returns the created task with initial status 'todo'.
    """
    svc, p_repo = deps
    project = p_repo.get(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    try:
        t = svc.add_task(project, payload.title, payload.description or "", payload.deadline)
        return TaskResponse(
            id=t.id,
            project_id=t.project_id,
            title=t.title,
            description=t.description,
            status=t.status.value if hasattr(t.status, "value") else str(t.status),
            deadline=t.deadline,
            closed_at=t.closed_at,
        )
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))

@router.patch("/{task_id}", response_model=TaskResponse)
def edit_task(task_id: int, payload: TaskEditRequest, deps = Depends(get_task_service)):
    """
    Edit an existing task.

    - **task_id**: Task ID (path parameter)
    - **title**: Updated task title (optional, max 30 characters)
    - **description**: Updated task description (optional, max 150 characters)
    - **status**: Updated status - 'todo', 'doing', or 'done' (optional)
    - **deadline**: Updated deadline in YYYY-MM-DD format (optional)

    When status is changed to 'done', the closed_at timestamp is automatically set.
    All fields are optional - only provide fields you want to update.
    """
    svc, p_repo = deps
    # load task first
    t = svc.repo.get(task_id)
    if not t:
        raise HTTPException(status_code=404, detail="Task not found")
    project = p_repo.get(t.project_id)
    try:
        updated = svc.edit_task(project, task_id, payload.title, payload.description, payload.status, payload.deadline)
        return TaskResponse(
            id=updated.id,
            project_id=updated.project_id,
            title=updated.title,
            description=updated.description,
            status=updated.status.value if hasattr(updated.status, "value") else str(updated.status),
            deadline=updated.deadline,
            closed_at=updated.closed_at,
        )
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))

@router.delete("/{task_id}")
def delete_task(task_id: int, deps = Depends(get_task_service)):
    """
    Delete a task by ID.

    - **task_id**: Task ID to delete (path parameter)

    Returns a success status when the task is deleted.
    """
    svc, p_repo = deps
    t = svc.repo.get(task_id)
    if not t:
        raise HTTPException(status_code=404, detail="Task not found")
    ok = svc.delete_task(p_repo.get(t.project_id), task_id)
    if not ok:
        raise HTTPException(status_code=400, detail="Could not delete")
    return {"status": "deleted"}

@router.patch("/{tid}/status")
def change_task_status(tid: int, payload: TaskStatusRequest, deps=Depends(get_task_service)):
    """
    Change the status of a task.

    - **tid**: Task ID (path parameter)
    - **status**: New status - 'todo', 'doing', or 'done' (required)

    When status is changed to 'done', the closed_at timestamp is automatically set to the current time.
    """
    svc, p_repo = deps
    t = svc.repo.get(tid)
    if not t:
        raise HTTPException(status_code=404, detail="Task not found.")
    p = p_repo.get(t.project_id)
    try:
        updated = svc.change_status(p, tid, payload.status)
        return TaskResponse(
            id=updated.id,
            project_id=updated.project_id,
            title=updated.title,
            description=updated.description,
            status=updated.status.value if hasattr(updated.status, "value") else str(updated.status),
            deadline=updated.deadline,
            closed_at=updated.closed_at,
        )
    except ValueError as err:
        raise HTTPException(status_code=400, detail=str(err))
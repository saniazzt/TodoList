from fastapi import APIRouter
from todolist.api.controllers import projects_controller, tasks_controller

router = APIRouter()
router.include_router(projects_controller.router)
router.include_router(tasks_controller.router)

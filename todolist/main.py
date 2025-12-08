import argparse
import sys
import threading
from contextlib import contextmanager

from fastapi import FastAPI

from todolist.api.routers import router as api_router
from todolist.cli.menu import CLI
from todolist.commands.scheduler import start_scheduler
from todolist.db.session import SessionLocal
from todolist.repositories.sqlalchemy_project_repository import SqlAlchemyProjectRepository
from todolist.repositories.sqlalchemy_task_repository import SqlAlchemyTaskRepository
from todolist.services.project_service import ProjectService
from todolist.services.task_service import TaskService


def create_api_app() -> FastAPI:
    """Factory function for FastAPI app."""
    app = FastAPI(title="ToDoList API", version="1.0.0")
    app.include_router(api_router)
    return app


@contextmanager
def get_cli_context():
    """Context manager for CLI resources."""
    db = SessionLocal()
    try:
        project_repo = SqlAlchemyProjectRepository(db)
        task_repo = SqlAlchemyTaskRepository(db)
        project_service = ProjectService(project_repo)
        task_service = TaskService(task_repo)
        yield CLI(project_service, task_service), db
    finally:
        db.close()


def parse_args():
    parser = argparse.ArgumentParser(description="ToDoList Application")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--menu", action="store_true", help="Run CLI menu")
    group.add_argument("--schedule", action="store_true", help="Run scheduler only")
    group.add_argument("--both", action="store_true", help="Run CLI with background scheduler")
    group.add_argument("--api", action="store_true", help="Create API app")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    return parser.parse_args()


def main():
    args = parse_args()
    
    if args.api:
        if __name__ == "__main__":
            import uvicorn
            uvicorn.run(create_api_app(), host=args.host, port=args.port)
        return create_api_app()
    
    with get_cli_context() as (cli, db):
        if args.schedule:
            print("Starting scheduler...")
            start_scheduler()
        elif args.both:
            # Check for projects before starting scheduler
            if not cli.project_service.list_projects():
                print("Warning: No projects found. Scheduler disabled.")
            else:
                threading.Thread(target=start_scheduler, daemon=True).start()
                print("Scheduler running in background")
            cli.run()
        else:
            cli.run()


if __name__ == "__main__":
    main()
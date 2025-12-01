from todolist.db.session import SessionLocal
from todolist.repositories.sqlalchemy_project_repository import SqlAlchemyProjectRepository
from todolist.repositories.sqlalchemy_task_repository import SqlAlchemyTaskRepository
from todolist.services.project_service import ProjectService
from todolist.services.task_service import TaskService
from todolist.cli.menu import CLI
from todolist.commands.autoclose import autoclose
from todolist.commands.scheduler import start_scheduler

import threading
import sys

def create_app_cli():
    db = SessionLocal()
    project_repo = SqlAlchemyProjectRepository(db)
    task_repo = SqlAlchemyTaskRepository(db)
    project_service = ProjectService(project_repo)
    task_service = TaskService(task_repo)
    return CLI(project_service, task_service), db

def main():
    # Check for optional CLI argument to start scheduler
    run_sched = "--scheduler" in sys.argv

    cli, db = create_app_cli()

    try:
        if run_sched:
            # Run scheduler in a separate thread so CLI is not blocked
            scheduler_thread = threading.Thread(target=start_scheduler, daemon=True)
            scheduler_thread.start()
            print("Scheduler is running in the background...")
        
        cli.run()
    finally:
        db.close()

if __name__ == "__main__":
    main()

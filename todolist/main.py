from todolist.db.session import SessionLocal
from todolist.repositories.sqlalchemy_project_repository import SqlAlchemyProjectRepository
from todolist.repositories.sqlalchemy_task_repository import SqlAlchemyTaskRepository
from todolist.services.project_service import ProjectService
from todolist.services.task_service import TaskService
from todolist.cli.menu import CLI

def create_app_cli():
    db = SessionLocal()
    project_repo = SqlAlchemyProjectRepository(db)
    task_repo = SqlAlchemyTaskRepository(db)
    project_service = ProjectService(project_repo)
    task_service = TaskService(task_repo)
    return CLI(project_service, task_service), db

def main():
    cli, db = create_app_cli()
    try:
        cli.run()
    finally:
        db.close()

if __name__ == "__main__":
    main()
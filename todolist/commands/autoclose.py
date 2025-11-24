from todolist.db.session import SessionLocal
from todolist.repositories.sqlalchemy_task_repository import SqlAlchemyTaskRepository
from todolist.services.task_service import TaskService

def autoclose() -> int:
    db = SessionLocal()
    try:
        repo = SqlAlchemyTaskRepository(db)
        service = TaskService(repo)
        n = service.autoclose_overdue()
        print(f"Autoclosed {n} overdue tasks.")
        return n
    finally:
        db.close()

if __name__ == "__main__":
    autoclose()
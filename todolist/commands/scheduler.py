import time
import schedule
from todolist.db.session import SessionLocal
from todolist.commands.autoclose import autoclose
from todolist.repositories.sqlalchemy_task_repository import SqlAlchemyTaskRepository
from todolist.services.task_service import TaskService

def run_autoclose():
    autoclose()

def start_scheduler():
    schedule.every(5).minutes.do(run_autoclose)
    print("Scheduler started (Runs autoclose every 5 minutes)")

    while True:
        schedule.run_pending()
        time.sleep(2)

if __name__ == "__main__":
    start_scheduler()

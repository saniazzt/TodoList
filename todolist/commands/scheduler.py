import time
import schedule
from todolist.db.session import SessionLocal
from todolist.commands.autoclose import autoclose
from todolist.repositories.sqlalchemy_task_repository import SqlAlchemyTaskRepository
from todolist.services.task_service import TaskService

def run_autoclose():
    autoclose()

def start_scheduler():
    schedule.every().day.at("00:00").do(run_autoclose)
    print("Scheduler started (Runs autoclose daily at 00:00)")

    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    start_scheduler()

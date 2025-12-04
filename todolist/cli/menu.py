from __future__ import annotations
from typing import Optional
from datetime import datetime
from todolist.services.project_service import ProjectService
from todolist.services.task_service import TaskService
from todolist.utils.env_loader import get_env_int

def parse_date(s: str) -> Optional[datetime.date]:
    if not s:
        return None
    try:
        return datetime.strptime(s, "%Y-%m-%d").date()
    except ValueError:
        raise ValueError("Date must be in YYYY-MM-DD format.")

class CLI:
    def __init__(self, project_service: ProjectService, task_service: TaskService) -> None:
        self.project_service = project_service
        self.task_service = task_service

    def pause(self) -> None:
        input("\nPress Enter to continue...")

    def show_projects(self, pause: bool = True) -> bool:
        projects = self.project_service.list_projects()
        if not projects:
            print("[INFO] No projects found.")
            if pause: self.pause()
            return False
        print("\nProjects:")
        print("-" * 100)
        print(f"{'ID':<6} | {'Name':<20} | {'Tasks':<6} | Description")
        print("-" * 100)
        for p in projects:
            desc = p.description or ""
            desc = desc if len(desc) <= 50 else desc[:47] + "..."
            print(f"{p.id:<6} | {p.name:<20} | {len(p.tasks):<6} | {desc}")
        print("-" * 100)
        if pause: self.pause()
        return True

    def show_tasks(self, project_id: int, pause: bool = True) -> bool:
        project = self.project_service.get_project(project_id)
        if not project:
            print("[ERROR] Project not found.")
            if pause: self.pause()
            return False
        tasks = self.task_service.list_tasks(project)
        if not tasks:
            print("[INFO] No tasks for this project.")
            if pause: self.pause()
            return False
        print("\nTasks:")
        print("-" * 80)
        print(f"{'ID':<6} | {'Title':<25} | {'Status':<6} | Deadline")
        print("-" * 80)
        for t in tasks:
            dl = t.deadline.isoformat() if t.deadline else "—"
            print(f"{t.id:<6} | {t.title:<25} | {t.status.value:<6} | {dl}")
        print("-" * 80)
        if pause: self.pause()
        return True

    def create_project(self) -> None:
        name = input("Project name: ").strip()
        desc = input("Project description: ").strip()
        try:
            p = self.project_service.create_project(name, desc)
            print(f"[OK] Created project {p.id} | {p.name}")
        except Exception as e:
            print(f"[ERROR] {e}")
        self.pause()

    def edit_project(self) -> None:
        if not self.show_projects(pause=False): return
        pid_raw = input("Project id: ").strip()
        try:
            pid = int(pid_raw)
        except ValueError:
            print("[ERROR] Invalid project id.")
            self.pause(); return
        new_name = input("New name: ").strip()
        new_desc = input("New description: ").strip()
        try:
            p = self.project_service.edit_project(pid, new_name, new_desc)
            print(f"[OK] Updated project {p.id} | {p.name}")
        except Exception as e:
            print(f"[ERROR] {e}")
        self.pause()

    def delete_project(self) -> None:
        if not self.show_projects(pause=False): return
        pid_raw = input("Project id to delete: ").strip()
        try:
            pid = int(pid_raw)
        except ValueError:
            print("[ERROR] Invalid project id.")
            self.pause(); return
        ok = self.project_service.delete_project(pid)
        print("[OK] Project deleted." if ok else "[ERROR] Project not found.")
        self.pause()

    def add_task(self) -> None:
        if not self.show_projects(pause=False): return
        pid_raw = input("Project id to add task: ").strip()
        try:
            pid = int(pid_raw)
        except ValueError:
            print("[ERROR] Invalid project id."); self.pause(); return
        project = self.project_service.get_project(pid)
        if not project:
            print("[ERROR] Project not found."); self.pause(); return
        title = input("Task title: ").strip()
        desc = input("Task description: ").strip()
        dl_raw = input("Deadline (YYYY-MM-DD) or blank: ").strip()
        try:
            dl = parse_date(dl_raw) if dl_raw else None
            t = self.task_service.add_task(project, title, desc, dl)
            print(f"[OK] Task added {t.id} | {t.title}")
        except Exception as e:
            print(f"[ERROR] {e}")
        self.pause()

    def list_tasks(self) -> None:
        if not self.show_projects(pause=False): return
        pid_raw = input("Project id to view tasks: ").strip()
        try:
            pid = int(pid_raw)
        except ValueError:
            print("[ERROR] Invalid project id."); self.pause(); return
        self.show_tasks(pid, pause=True)

    def edit_task(self) -> None:
        if not self.show_projects(pause=False): return
        pid_raw = input("Project id: ").strip()
        try:
            pid = int(pid_raw)
        except ValueError:
            print("[ERROR] Invalid project id."); self.pause(); return
        project = self.project_service.get_project(pid)
        if not project:
            print("[ERROR] Project not found."); self.pause(); return
        if not self.show_tasks(pid, pause=False): return
        tid_raw = input("Task id: ").strip()
        try:
            tid = int(tid_raw)
        except ValueError:
            print("[ERROR] Invalid task id."); self.pause(); return
        print("Leave blank to keep current value.")
        title = input("New title: ").strip() or None
        desc = input("New description: ").strip() or None
        status = input("New status (todo/doing/done): ").strip() or None
        dl_raw = input("New deadline (YYYY-MM-DD) or blank: ").strip() or None
        try:
            dl = parse_date(dl_raw) if dl_raw else None
            t = self.task_service.edit_task(project, tid, title, desc, status, dl)
            print(f"[OK] Task updated {t.id} | {t.title} | {t.status.value}")
        except Exception as e:
            print(f"[ERROR] {e}")
        self.pause()

    def delete_task(self) -> None:
        if not self.show_projects(pause=False): return
        pid_raw = input("Project id: ").strip()
        try:
            pid = int(pid_raw)
        except ValueError:
            print("[ERROR] Invalid project id."); self.pause(); return
        project = self.project_service.get_project(pid)
        if not project:
            print("[ERROR] Project not found."); self.pause(); return
        if not self.show_tasks(pid, pause=False): return
        tid_raw = input("Task id to delete: ").strip()
        try:
            tid = int(tid_raw)
        except ValueError:
            print("[ERROR] Invalid task id."); self.pause(); return
        ok = self.task_service.delete_task(project, tid)
        print("[OK] Task deleted." if ok else "[ERROR] Task not found.")
        self.pause()

    def change_task_status(self) -> None:
        if not self.show_projects(pause=False): return
        pid_raw = input("Project id: ").strip()
        try:
            pid = int(pid_raw)
        except ValueError:
            print("[ERROR] Invalid project id."); self.pause(); return
        project = self.project_service.get_project(pid)
        if not project:
            print("[ERROR] Project not found."); self.pause(); return
        if not self.show_tasks(pid, pause=False): return
        tid_raw = input("Task id: ").strip()
        try:
            tid = int(tid_raw)
        except ValueError:
            print("[ERROR] Invalid task id."); self.pause(); return
        status = input("New status (todo/doing/done): ").strip()
        try:
            t = self.task_service.change_status(project, tid, status)
            print(f"[OK] Status updated: {t.id} -> {t.status.value}")
        except Exception as e:
            print(f"[ERROR] {e}")
        self.pause()

    def run(self) -> None:
        actions = {
            "1": ("List projects", self.show_projects),
            "2": ("Create project", self.create_project),
            "3": ("Edit project", self.edit_project),
            "4": ("Delete project", self.delete_project),
            "5": ("List tasks by project", self.list_tasks),
            "6": ("Add task", self.add_task),
            "7": ("Edit task", self.edit_task),
            "8": ("Delete task", self.delete_task),
            "9": ("Change task status", self.change_task_status),
            "q": ("Quit", None),
        }
        while True:
            print("\n=== ToDoList Menu ===\n")
            for k, v in actions.items():
                print(f"{k}) {v[0]}")
            choice = input("Choose: ").strip().lower()
            if choice == "q":
                print("Goodbye")
                break
            action = actions.get(choice)
            if not action:
                print("[ERROR] Invalid choice.")
                continue
            _, func = action
            if func:
                func()
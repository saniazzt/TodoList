from __future__ import annotations

from datetime import datetime
from typing import Optional

from todolist.core.services.project_service import ProjectService
from todolist.utils.formatter import success, error, info, format_entity


def parse_date(s: str) -> Optional[datetime.date]:
    if not s:
        return None
    try:
        return datetime.strptime(s, "%Y-%m-%d").date()
    except ValueError:
        raise ValueError("Date must be in YYYY-MM-DD format.")


class CLI:
    def __init__(self) -> None:
        self.project_service = ProjectService()

    # ---------- Utility ----------
    def pause_for_user(self) -> None:
        """Wait for user input before returning to the main menu."""
        input(info("\nPress Enter to return to the menu..."))

    # ---------- Helper displays ----------
    def show_projects(self, pause: bool = True) -> None:
        """Show all projects. Pause only if explicitly requested."""
        projects = self.project_service.list_projects()
        if not projects:
            print(info("No projects found."))
            if pause:
                self.pause_for_user()
            return

        print("\nAvailable Projects:")
        print("-" * 100)
        print(f"{'ID':<6} | {'Name':<20} | {'Tasks':<6} | {'Description'}")
        print("-" * 100)
        for p in projects:
            desc = p.description if len(p.description) <= 50 else p.description[:47] + "..."
            print(f"{p.id:<6} | {p.name:<20} | {len(p.tasks):<6} | {desc}")
        print("-" * 100)

        if pause:
            self.pause_for_user()

    def show_tasks(self, project_id: str, pause: bool = True) -> bool:
        """Show all tasks for a project. Returns False if no tasks exist."""
        try:
            tasks = self.task_service.list_tasks(project_id)
        except Exception as exc:
            print(error(str(exc)))
            if pause:
                self.pause_for_user()
            return False

        if not tasks:
            print(info("No tasks found for this project."))
            if pause:
                self.pause_for_user()
            return False

        print("\nTasks in Project:")
        print("-" * 70)
        print(f"{'ID':<5} | {'Title':<25} | {'Status':<6} | Deadline")
        print("-" * 70)
        for t in tasks:
            dl = t.deadline.isoformat() if t.deadline else "—"
            print(f"{t.id:<5} | {t.title:<25} | {t.status:<6} | {dl}")
        print("-" * 70)

        if pause:
            self.pause_for_user()

        return True
    # ---------- Project operations ----------
    def create_project(self) -> None:
        name = input("Project name: ").strip()
        desc = input("Project description: ").strip()
        try:
            proj = self.project_service.create_project(name, desc)
            print(success(f"Project created: {format_entity(proj)}"))
        except Exception as exc:
            print(error(str(exc)))
        self.pause_for_user()

    def edit_project(self) -> None:
        self.show_projects(pause=False)
        pid = input("Enter project id to edit: ").strip()
        new_name = input("New project name: ").strip()
        new_desc = input("New project description: ").strip()
        try:
            proj = self.project_service.edit_project(pid, new_name, new_desc)
            print(success(f"Project updated: {proj.id} | {proj.name}"))
        except Exception as exc:
            print(error(str(exc)))
        self.pause_for_user()

    def delete_project(self) -> None:
        if not self.show_projects(pause=False):
            return  # Stop if no projects
        pid = input("Enter project id to delete: ").strip()
        try:
            ok = self.project_service.delete_project(pid)
            print(success("Project deleted") if ok else error("Project not found"))
        except Exception as exc:
            print(error(str(exc)))
        self.pause_for_user()

    # ---------- Task operations ----------
    def add_task(self) -> None:
        if not self.show_projects(pause=False):
            return  # Stop if no projects

        pid = input("Enter project id to add task: ").strip()
        project = self.project_service.get_project(pid)
        if not project:
            print(error("Project not found."))
            self.pause_for_user()
            return

        title = input("Task title: ").strip()
        desc = input("Task description: ").strip()
        dl = input("Deadline (YYYY-MM-DD) or blank: ").strip()

        try:
            deadline = parse_date(dl) if dl else None
            task = self.task_service.add_task(pid, title, desc, deadline)
            print(success(f"Task added: {task.id} | {task.title}"))
        except Exception as exc:
            print(error(str(exc)))
        self.pause_for_user()

    def edit_task(self) -> None:
        if not self.show_projects(pause=False):
            return  # Stop if no projects

        pid = input("Enter project id: ").strip()
        project = self.project_service.get_project(pid)
        if not project:
            print(error("Project not found."))
            self.pause_for_user()
            return

        if not self.show_tasks(pid, pause=False):
            return  # Stop if no tasks

        tid = input("Enter task id to edit: ").strip()

        print("\nLeave any field blank to keep current value.")
        title = input("New title: ").strip() or None
        desc = input("New description: ").strip() or None
        status = input("New status (todo/doing/done): ").strip() or None
        dl = input("New deadline (YYYY-MM-DD) or blank: ").strip() or None

        try:
            deadline = parse_date(dl) if dl else None
            task = self.task_service.edit_task(pid, tid, title, desc, status, deadline)
            print(success(f"Task updated: {task.id} | {task.title} | {task.status}"))
        except Exception as exc:
            print(error(str(exc)))
        self.pause_for_user()

    def delete_task(self) -> None:
        if not self.show_projects(pause=False):
            return  # Stop if no projects

        pid = input("Enter project id: ").strip()
        project = self.project_service.get_project(pid)
        if not project:
            print(error("Project not found."))
            self.pause_for_user()
            return

        if not self.show_tasks(pid, pause=False):
            return  # Stop if no tasks

        tid = input("Enter task id to delete: ").strip()
        try:
            ok = self.task_service.delete_task(pid, tid)
            print(success("Task deleted") if ok else error("Task not found"))
        except Exception as exc:
            print(error(str(exc)))
        self.pause_for_user()

    def change_task_status(self) -> None:
        if not self.show_projects(pause=False):
            return  # Stop if no projects

        pid = input("Enter project id: ").strip()
        project = self.project_service.get_project(pid)
        if not project:
            print(error("Project not found."))
            self.pause_for_user()
            return

        if not self.show_tasks(pid, pause=False):
            return  # Stop if no tasks

        tid = input("Enter task id to change status: ").strip()
        status = input("New status (todo/doing/done): ").strip()
        try:
            t = self.task_service.change_status(pid, tid, status)
            print(success(f"Status updated: {t.id} is now {t.status}"))
        except Exception as exc:
            print(error(str(exc)))
        self.pause_for_user()

    # ---------- Menu ----------
    def run(self) -> None:
        actions = {
            "1": ("Create project", self.create_project),
            "2": ("Edit project", self.edit_project),
            "3": ("Delete project", self.delete_project),
            "4": ("Add task", self.add_task),
            "5": ("Edit task", self.edit_task),
            "6": ("Change task status", self.change_task_status),
            "7": ("Delete task", self.delete_task),
            "q": ("Quit", None),
        }

        while True:
            print("\n=== ToDoList Menu ===")
            for k, (label, _) in actions.items():
                print(f"{k}) {label}")
            choice = input("Choose: ").strip().lower()
            if choice == "q":
                print(info("Goodbye"))
                break
            action = actions.get(choice)
            if not action:
                print(error("Invalid choice"))
                continue
            _, func = action
            if func:
                try:
                    func()
                except Exception as exc:
                    print(error(f"Unhandled error: {exc}"))

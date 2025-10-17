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

    # ---------- Menu ----------
    def run(self) -> None:
        actions = {
            "1": ("Create project", self.create_project),
            "2": ("Edit project", self.edit_project),
            "3": ("Delete project", self.delete_project),
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

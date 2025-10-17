from __future__ import annotations

from typing import Dict, Optional, List
from todolist.core.entities.project import Project
from todolist.core.entities.task import Task


class MemoryStorage:

    def __init__(self) -> None:
        self.projects: Dict[str, Project] = {}

    def add_project(self, project: Project) -> None:
        self.projects[project.id] = project

    def get_project(self, project_id: str) -> Optional[Project]:
        return self.projects.get(project_id)

    def remove_project(self, project_id: str) -> bool:
        if project_id in self.projects:
            del self.projects[project_id]
            return True
        return False
    
    def find_project_by_name(self, name: str) -> Optional[Project]:
        for p in self.projects.values():
            if p.name == name:
                return p
        return None
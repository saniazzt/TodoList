from __future__ import annotations

from typing import Dict, Optional, List
from todolist.core.entities.project import Project
from todolist.core.entities.task import Task


class MemoryStorage:

    def __init__(self) -> None:
        self.projects: Dict[str, Project] = {}

    def add_project(self, project: Project) -> None:
        self.projects[project.id] = project

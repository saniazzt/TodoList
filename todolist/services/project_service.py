from __future__ import annotations
from typing import List, Optional
from todolist.repositories.abstract import ProjectRepositoryInterface
from todolist.models.project import Project
from todolist.validators.project_validator import (
    validate_project_name,
    validate_project_uniqueness,
    validate_project_limit,
)
from todolist.exceptions.not_found import NotFoundError


class ProjectService:
    def __init__(self, repo: ProjectRepositoryInterface):
        self.repo = repo

    def create_project(self, name: str, description: str) -> Project:
        validate_project_name(name)
        validate_project_limit(self.repo)
        validate_project_uniqueness(self.repo, name)

        proj = Project(name=name, description=description)
        return self.repo.add(proj)

    def list_projects(self) -> List[Project]:
        return self.repo.list()

    def get_project(self, project_id: int) -> Optional[Project]:
        return self.repo.get(project_id)

    def edit_project(self, project_id: int, name: str, description: str) -> Project:
        proj = self.repo.get(project_id)
        if not proj:
            raise NotFoundError("Project not found.")

        validate_project_name(name)
        validate_project_uniqueness(self.repo, name, exclude_project_id=proj.id)

        proj.name = name
        proj.description = description
        return self.repo.add(proj)

    def delete_project(self, project_id: int) -> bool:
        return self.repo.delete(project_id)
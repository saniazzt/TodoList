from __future__ import annotations
from typing import List, Optional
from sqlalchemy.orm import Session
from todolist.models.project import Project

class SqlAlchemyProjectRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def add(self, project: Project) -> Project:
        self.db.add(project)
        self.db.commit()
        self.db.refresh(project)
        return project

    def get(self, project_id: int) -> Optional[Project]:
        return self.db.get(Project, project_id)

    def list(self) -> List[Project]:
        return self.db.query(Project).order_by(Project.id).all()

    def delete(self, project_id: int) -> bool:
        obj = self.get(project_id)
        if not obj:
            return False
        self.db.delete(obj)
        self.db.commit()
        return True

    def find_by_name(self, name: str) -> Optional[Project]:
        return self.db.query(Project).filter(Project.name == name).one_or_none()
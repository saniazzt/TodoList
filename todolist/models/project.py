from __future__ import annotations
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from todolist.db.base import Base

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(30), nullable=False, unique=True, index=True)
    description = Column(String(150), nullable=True)

    tasks = relationship("Task", back_populates="project", cascade="all, delete-orphan")

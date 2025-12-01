from __future__ import annotations
from datetime import datetime, date
import enum
from sqlalchemy import Column, Integer, String, ForeignKey, Date, DateTime, Enum, Index
from sqlalchemy.orm import relationship
from todolist.db.base import Base

class TaskStatus(enum.Enum):
    todo = "todo"
    doing = "doing"
    done = "done"

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(30), nullable=False)
    description = Column(String(150), nullable=True)
    status = Column(Enum(TaskStatus), nullable=False, default=TaskStatus.todo)
    deadline = Column(Date, nullable=True)
    closed_at = Column(DateTime, nullable=True)

    project = relationship("Project", back_populates="tasks")

Index("ix_tasks_deadline_status", Task.deadline, Task.status)

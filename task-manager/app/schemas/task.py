from pydantic import BaseModel
from typing import Optional
from app.models.enums import TaskPriority

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    priority: Optional[TaskPriority] = TaskPriority.LOW

class TaskCreate(TaskBase):
    user_id: int

class TaskUpdateStatus(BaseModel):
    status: str

class Task(TaskBase):
    id: int
    status: str
    user_id: int

    class Config:
        from_attributes = True
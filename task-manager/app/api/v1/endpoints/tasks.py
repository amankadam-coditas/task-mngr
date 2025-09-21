from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas import task as task_schema
from app.services import task_service
from app.api import deps

router = APIRouter()                                                                                                                                                                                                                                                               

@router.post("/", response_model=task_schema.Task)
def create_task(task: task_schema.TaskCreate, db: Session = Depends(deps.get_db)):
    return task_service.create_task(db=db, task=task)

@router.get("/", response_model=List[task_schema.Task])
def read_tasks(db: Session = Depends(deps.get_db)):
    return task_service.get_tasks(db=db)

@router.get("/user/{user_id}", response_model=List[task_schema.Task])
def read_tasks_by_user(user_id: int, db: Session = Depends(deps.get_db)):
    return task_service.get_tasks_by_user(db=db, user_id=user_id)

@router.patch("/{task_id}/status", response_model=task_schema.Task)
def update_task_status(task_id: int, update: task_schema.TaskUpdateStatus, db: Session = Depends(deps.get_db)):
    task = task_service.update_task_status(db=db, task_id=task_id, status=update.status)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.delete("/{task_id}", response_model=task_schema.Task)
def delete_task(task_id: int, db: Session = Depends(deps.get_db)):
    deleted_task = task_service.delete_task(db=db, task_id=task_id)
    if not deleted_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return deleted_task
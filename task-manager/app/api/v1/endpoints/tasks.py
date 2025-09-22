from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas import task as task_schema
from app.services import task_service
from app.api import deps
from app.models.user import User

router = APIRouter()                                                                                                                                                                                                                                                               

@router.post("/", response_model=task_schema.Task)
@deps.requires_auth
async def create_task(
    task: task_schema.TaskCreate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    # Ensure the task is created for the authenticated user
    task.user_id = current_user.id
    return task_service.create_task(db=db, task=task)

@router.get("/", response_model=List[task_schema.Task])
@deps.requires_auth
async def read_tasks(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    # Only return tasks for the authenticated user
    return task_service.get_tasks_by_user(db=db, user_id=current_user.id)

@router.get("/user/{user_id}", response_model=List[task_schema.Task])
@deps.requires_auth
async def read_tasks_by_user(
    user_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    # Only allow users to see their own tasks
    if user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not authorized to view other users' tasks"
        )
    return task_service.get_tasks_by_user(db=db, user_id=user_id)

@router.patch("/{task_id}/status", response_model=task_schema.Task)
@deps.requires_auth
async def update_task_status(
    task_id: int,
    update: task_schema.TaskUpdateStatus,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    # Get the task first to check ownership
    task = task_service.get_task(db=db, task_id=task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not authorized to modify this task"
        )
    
    updated_task = task_service.update_task_status(db=db, task_id=task_id, status=update.status)
    return updated_task

@router.delete("/{task_id}", response_model=task_schema.Task)
@deps.requires_auth
async def delete_task(
    task_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    # Get the task first to check ownership
    task = task_service.get_task(db=db, task_id=task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not authorized to delete this task"
        )
    
    deleted_task = task_service.delete_task(db=db, task_id=task_id)
    return deleted_task
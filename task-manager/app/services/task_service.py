from sqlalchemy.orm import Session
from app.models import task as task_model
from app.schemas import task as task_schema

def create_task(db: Session, task: task_schema.TaskCreate):
    db_task = task_model.Task(
        title=task.title,
        description=task.description,
        priority=task.priority,
        user_id=task.user_id,
        status="pending",
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def get_tasks(db: Session):
    return db.query(task_model.Task).all()

def get_tasks_by_user(db: Session, user_id: int):
    return db.query(task_model.Task).filter(task_model.Task.user_id == user_id).all()

def update_task_status(db: Session, task_id: int, status: str):
    task = db.query(task_model.Task).filter(task_model.Task.id == task_id).first()
    if task:
        task.status = status
        db.commit()
        db.refresh(task)
    return task

def delete_task(db: Session, task_id: int):
    task = db.query(task_model.Task).filter(task_model.Task.id == task_id).first()
    if task:
        db.delete(task)
        db.commit()
    return task
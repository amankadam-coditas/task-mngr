from sqlalchemy.orm import Session
from app.models import user as user_model
from app.schemas import user as user_schema

def create_user(db: Session, user: user_schema.UserCreate):
    db_user = user_model.User(name=user.name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_users(db: Session):
    return db.query(user_model.User).all()

def get_user(db: Session, user_id: int):
    return db.query(user_model.User).filter(user_model.User.id == user_id).first()

def delete_user(db: Session, user_id: int):
    user = db.query(user_model.User).filter(user_model.User.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
    return user
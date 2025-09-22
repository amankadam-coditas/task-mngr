from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas import user as user_schema
from app.services import user_service
from app.api import deps
from app.models.user import User

router = APIRouter()

@router.post("/", response_model=user_schema.User)
def create_user(user: user_schema.UserCreate, db: Session = Depends(deps.get_db)):
    """
    Create new user (signup) - unprotected endpoint
    """
    return user_service.create_user(db=db, user=user)

@router.get("/profile", response_model=user_schema.User)
@deps.requires_auth
async def read_user_profile(current_user: User = Depends(deps.get_current_user)):
    """
    Get current user's profile (protected endpoint)
    """
    return current_user

@router.get("/", response_model=List[user_schema.User])
@deps.requires_auth
async def read_users(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """
    Get all users (protected endpoint)
    """
    users = user_service.get_users(db)
    return users

@router.get("/{user_id}", response_model=user_schema.User)
@deps.requires_auth
async def read_user(
    user_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """
    Get user by ID (protected endpoint)
    Can only view own profile unless admin
    """
    if user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not authorized to view other users' profiles"
        )
    
    db_user = user_service.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.delete("/{user_id}", response_model=user_schema.User)
@deps.requires_auth
async def delete_user(
    user_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """
    Delete user (protected endpoint)
    Can only delete own account unless admin
    """
    if user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not authorized to delete other users"
        )
    
    deleted_user = user_service.delete_user(db=db, user_id=user_id)
    if not deleted_user:
        raise HTTPException(status_code=404, detail="User not found")
    return deleted_user
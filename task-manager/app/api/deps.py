from typing import Generator, Optional
from functools import wraps
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.database.session import SessionLocal
from app.core.auth import verify_token
from app.models.user import User
from sqlalchemy.orm import Session

# Create a bearer token instance
bearer_scheme = HTTPBearer()

def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)
) -> User:
    """
    Dependency to get current authenticated user from JWT token
    """
    # Verify the token
    token_data = verify_token(credentials.credentials)
    
    # Get user from database
    user = db.query(User).filter(User.id == token_data["sub"]).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    return user

def requires_auth(func):
    """
    Decorator for routes that require authentication
    """
    @wraps(func)
    async def wrapper(*args, current_user: User = Depends(get_current_user), **kwargs):
        return await func(*args, current_user=current_user, **kwargs)
    return wrapper
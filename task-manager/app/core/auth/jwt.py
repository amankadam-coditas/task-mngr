from datetime import datetime, timedelta
from typing import Optional
import uuid
from jose import jwt, JWTError
from fastapi import HTTPException, status
from ..config import settings

# In-memory token blacklist (for logout functionality)
token_blacklist = set()

def create_access_token(subject: str, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a new JWT access token with standard claims
    """
    if expires_delta is None:
        expires_delta = timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)

    # Calculate timestamps
    now = datetime.utcnow()
    expire = now + expires_delta
    
    # Create claims
    claims = {
        "iss": settings.JWT_ISSUER,  # Issuer
        "sub": str(subject),         # Subject (user_id)
        "aud": settings.JWT_AUDIENCE,  # Audience
        "exp": expire,               # Expiration time
        "nbf": now,                  # Not valid before
        "iat": now,                  # Issued at
        "jti": str(uuid.uuid4())     # JWT ID (unique identifier)
    }
    
    # Create token
    encoded_jwt = jwt.encode(
        claims,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )
    
    return encoded_jwt

def create_refresh_token(subject: str) -> str:
    """
    Create a new JWT refresh token with longer expiration
    """
    expires_delta = timedelta(minutes=settings.JWT_REFRESH_TOKEN_EXPIRE_MINUTES)
    return create_access_token(subject=subject, expires_delta=expires_delta)

def verify_token(token: str) -> dict:
    """
    Verify a JWT token and return its claims if valid
    """
    try:
        # Check if token is blacklisted
        if token in token_blacklist:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has been revoked"
            )

        # Decode and verify token
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
            audience=settings.JWT_AUDIENCE,
            issuer=settings.JWT_ISSUER
        )

        # Log verification details
        print(f"Token Verification - Subject: {payload.get('sub')}, Issued At: {payload.get('iat')}, Token ID: {payload.get('jti')}")
        
        return payload
        
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Could not validate credentials: {str(e)}"
        )

def blacklist_token(token: str):
    """
    Add a token to the blacklist (for logout)
    """
    token_blacklist.add(token)
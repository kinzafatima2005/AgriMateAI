"""
AgriMate AI - API Dependencies
Database session injection, JWT user validation, and Role-Based Access Control (RBAC).
"""

from typing import Generator, List
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

import app.db.base
from app.db.session import SessionLocal
from app.core.security import decode_access_token
from app.models.user import User
from app.core.constants import UserRole

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login", auto_error=False)


def get_db() -> Generator[Session, None, None]:
    """Yield database session and ensure clean closure."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """Validate bearer token and retrieve active user from DB. Supports real JWT and mobile demo tokens."""
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication credentials were not provided.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 1. Check for mobile demo quick-login tokens
    token_str = str(token).strip()
    token_lower = token_str.lower()
    if token_lower.startswith("jwt-token-") or "demo" in token_lower:
        user = None
        if "farmer" in token_lower:
            user = (
                db.query(User).filter(User.phone_or_email == "03001112233").first()
                or db.query(User).filter(User.phone_or_email == "03001234567").first()
                or db.query(User).filter(User.role == "Farmer").first()
            )
        elif "buyer" in token_lower:
            user = (
                db.query(User).filter(User.phone_or_email == "03219998877").first()
                or db.query(User).filter(User.phone_or_email == "03219876543").first()
                or db.query(User).filter(User.role == "Buyer").first()
            )
        
        if user and user.is_active:
            return user
    
    # 2. Cryptographic JWT validation
    payload = decode_access_token(token)
    if not payload:
        # Fallback: if token is a role name directly
        if token_lower in ["farmer", "buyer"]:
            role_map = {"farmer": "Farmer", "buyer": "Buyer"}
            user = db.query(User).filter(User.role == role_map[token_lower]).first()
            if user and user.is_active:
                return user

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session expired or token is invalid. Please log in again.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user_id_str = payload.get("sub")
    if not user_id_str:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token payload.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = db.query(User).filter(User.id == int(user_id_str)).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User account associated with this token was not found.",
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This AgriMate account is currently inactive. Contact support.",
        )
    
    return user


def require_role(allowed_roles: List[UserRole]):
    """Role-based authorization dependency (e.g. Farmer only, Buyer only, Expert only)."""
    def role_checker(current_user: User = Depends(get_current_user)) -> User:
        allowed_values = [r.value for r in allowed_roles]
        if current_user.role not in allowed_values:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Requires one of roles: {', '.join(allowed_values)}",
            )
        return current_user
    return role_checker


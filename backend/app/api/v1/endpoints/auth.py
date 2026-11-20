"""
AgriMate AI - Authentication Endpoints
Minimal registration: name, phone/email, password, role, location only.
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.core.security import get_password_hash, verify_password, create_access_token
from app.core.constants import UserRole, DECISION_SUPPORT_DISCLAIMER_EN
from app.models.user import User
from app.schemas.user import UserRegister, UserLogin, UserResponse, Token
from app.schemas.common import APIResponse

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.get("/roles", response_model=List[str], summary="List supported AgriMate user roles")
def get_roles():
    """Returns valid roles for minimal registration: Farmer, Buyer."""
    return [UserRole.FARMER.value, UserRole.BUYER.value]


@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED, summary="Minimal user registration")
def register_user(
    payload: UserRegister,
    db: Session = Depends(get_db)
):
    """
    Register with minimal fields ONLY:
    - name: Full Name
    - phone_or_email: Pakistani phone number (e.g. 03001234567) or email
    - password: Password (min 6 chars)
    - role: Farmer or Buyer
    - location: District and province (e.g. Multan, Punjab)
    """
    normalized_identifier = payload.phone_or_email.strip().lower()
    
    # Check if user already exists
    existing_user = db.query(User).filter(User.phone_or_email == normalized_identifier).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An account with this phone number or email is already registered in AgriMate."
        )
    
    # Hash password with PBKDF2-HMAC-SHA256
    hashed_pwd = get_password_hash(payload.password)
    
    new_user = User(
        name=payload.name.strip(),
        phone_or_email=normalized_identifier,
        hashed_password=hashed_pwd,
        role=payload.role.value,
        location=payload.location.strip(),
        is_active=True
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Generate JWT token
    access_token = create_access_token(subject=str(new_user.id), role=new_user.role)
    
    return Token(
        access_token=access_token,
        token_type="bearer",
        user=UserResponse.model_validate(new_user),
        disclaimer=DECISION_SUPPORT_DISCLAIMER_EN
    )


@router.post("/login", response_model=Token, summary="User login")
def login_user(
    payload: UserLogin,
    db: Session = Depends(get_db)
):
    """Login with registered phone/email and password."""
    user = db.query(User).filter(User.phone_or_email == payload.phone_or_email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect phone/email or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not verify_password(payload.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect phone/email or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is inactive. Please contact your local agricultural extension coordinator.",
        )
    
    # If a specific login role was selected, verify role alignment
    if payload.role:
        norm_expected = payload.role.strip().lower()
        norm_actual = user.role.strip().lower()
        if norm_expected != norm_actual and not (norm_expected in norm_actual or norm_actual in norm_expected):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"This account is registered as a {user.role}, not as a {payload.role}.",
                headers={"WWW-Authenticate": "Bearer"},
            )
    
    access_token = create_access_token(subject=str(user.id), role=user.role)
    
    return Token(
        access_token=access_token,
        token_type="bearer",
        user=UserResponse.model_validate(user),
        disclaimer=DECISION_SUPPORT_DISCLAIMER_EN
    )


@router.post("/demo-login/{role_name}", response_model=Token, summary="Instant demo sign-in for mobile prototype testing")
def demo_login_by_role(
    role_name: str,
    db: Session = Depends(get_db)
):
    """Generates an instant genuine JWT for the requested role (Farmer, Buyer)."""
    norm = role_name.strip().lower()
    target_role = "Farmer"
    phone_filter = "03001112233"
    if "buyer" in norm:
        target_role = "Buyer"
        phone_filter = "03219998877"

    user = db.query(User).filter(User.phone_or_email == phone_filter).first() or \
           db.query(User).filter(User.role == target_role).first()
    
    if not user:
        raise HTTPException(status_code=404, detail=f"No active user found for role {target_role}")

    access_token = create_access_token(subject=str(user.id), role=user.role)
    return Token(
        access_token=access_token,
        token_type="bearer",
        user=UserResponse.model_validate(user),
        disclaimer=DECISION_SUPPORT_DISCLAIMER_EN
    )


@router.get("/me", response_model=UserResponse, summary="Get current logged-in user profile")
def get_current_user_profile(
    current_user: User = Depends(get_current_user)
):
    """Retrieve verified profile of authenticated farmer, buyer, or expert."""
    return UserResponse.model_validate(current_user)


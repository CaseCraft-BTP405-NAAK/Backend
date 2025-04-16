from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.user import User
from app.schemas.user import User as UserSchema, UserCreate, Token
from app.auth.jwt import (
    verify_password,
    get_password_hash,
    create_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    get_current_active_user
)

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserSchema, status_code=status.HTTP_201_CREATED)
def register_user(user_in: UserCreate, db: Session = Depends(get_db)) -> Any:
    """
    Register a new user.
    
    Args:
        user_in: User registration data including email, username, and password
        db: Database session dependency
        
    Returns:
        The newly created user object
        
    Raises:
        HTTPException: If email or username already exists
    """
    # Check if user with this email already exists
    user = db.query(User).filter(User.email == user_in.email).first()
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )
    
    # Check if user with this username already exists
    user = db.query(User).filter(User.username == user_in.username).first()
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this username already exists"
        )
    
    # Create new user
    db_user = User(
        email=user_in.email,
        username=user_in.username,
        full_name=user_in.full_name,
        hashed_password=get_password_hash(user_in.password)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post("/token", response_model=Token, status_code=status.HTTP_200_OK)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests.
    
    Args:
        form_data: OAuth2 password request form containing username and password
        db: Database session dependency
        
    Returns:
        Token object with access token and token type
        
    Raises:
        HTTPException: If authentication fails
    """
    # Try to find user by username
    user = db.query(User).filter(User.username == form_data.username).first()
    
    # If not found, try by email
    if not user:
        user = db.query(User).filter(User.email == form_data.username).first()
    
    # Verify user and password
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserSchema, status_code=status.HTTP_200_OK)
def read_users_me(current_user: User = Depends(get_current_active_user)) -> Any:
    """
    Get current user information based on the JWT token.
    
    Args:
        current_user: Current authenticated user from JWT token
        
    Returns:
        Current user information
    """
    return current_user
"""
Authentication router for user login, signup and profile access.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from typing import Any

from app.core.config import settings, oauth2_scheme
from app.core.security import create_access_token, verify_password
from app.database.session import get_db
from app import crud, schemas

router = APIRouter()


@router.post("/signup", response_model=schemas.UserRead)
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)) -> Any:
    """
    Register a new user.
    
    Args:
        user: User data
        db: Database session
        
    Returns:
        Created user data
        
    Raises:
        HTTPException: If email already exists
    """
    db_user = crud.get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db, user)


@router.post("/token")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
) -> Any:
    """
    Authenticate user and return JWT token.
    
    Args:
        form_data: Login credentials
        db: Database session
        
    Returns:
        JWT token
        
    Raises:
        HTTPException: If authentication fails
    """
    user = crud.get_user_by_email(db, email=form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    access_token = create_access_token(subject=user.email)
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/login", response_model=schemas.Token)
def login_json(
    login_data: schemas.UserLogin,
    db: Session = Depends(get_db)
) -> Any:
    """
    Login endpoint that accepts JSON payload directly.
    
    Args:
        login_data: Login credentials as JSON
        db: Database session
        
    Returns:
        JWT token
        
    Raises:
        HTTPException: If authentication fails
    """
    user = crud.get_user_by_email(db, email=login_data.email)
    if not user or not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    access_token = create_access_token(subject=user.email)
    return {"access_token": access_token, "token_type": "bearer"}


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> Any:
    """
    Get current user from JWT token.
    
    Args:
        token: JWT token
        db: Database session
        
    Returns:
        User object
        
    Raises:
        HTTPException: If token is invalid
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = crud.get_user_by_email(db, email=username)
    if user is None:
        raise credentials_exception
    return user


@router.get("/me", response_model=schemas.UserRead)
def read_users_me(current_user = Depends(get_current_user)) -> Any:
    """
    Get current user info.
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        User data
    """
    return current_user

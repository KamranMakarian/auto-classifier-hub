from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.user import UserCreate
from services.auth import register_user, register_admin_user
from config.db import get_db
from dependencies.auth_dependencies import get_current_user, admin_only
from fastapi.security import OAuth2PasswordRequestForm
from passlib.hash import bcrypt
from fastapi import status
from jose import jwt
from datetime import timedelta, datetime
from schemas.token import Token
from utils.jwt import SECRET_KEY, ALGORITHM
from models.user import User

router = APIRouter()

@router.post("/register", status_code=201, summary="Register a regular user (admin role blocked)")
def register(user: UserCreate, db: Session = Depends(get_db)):
    try:
        new_user = register_user(db, user.dict())
        return {"message": f"User '{new_user.username}' registered successfully"}
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))

@router.post("/admin/register", status_code=201, summary="Admin-only: Create a new admin user")
def register_admin(
    user: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_only)
):
    try:
        new_user = register_admin_user(db=db, user_data=user.dict(), current_user=current_user)
        return {"message": f"Admin user '{new_user.username}' created successfully"}
    except PermissionError as pe:
        raise HTTPException(status_code=403, detail=str(pe))
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))

ACCESS_TOKEN_EXPIRE_MINUTES = 60

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()

    if not user or not bcrypt.verify(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )

    to_encode = {
        "sub": str(user.id),
        "role": user.role,
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return {"access_token": token, "token_type": "bearer"}
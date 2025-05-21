from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from config.db import get_db
from dependencies.auth_dependencies import admin_only
from models.user import User
from models.trained_model import TrainedModel

router = APIRouter()

@router.get("/admin/users", tags=["Admin"])
def list_all_users(db: Session = Depends(get_db), current_user: User = Depends(admin_only)):
    return db.query(User).all()


@router.delete("/admin/user/{user_id}", tags=["Admin"])
def delete_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(admin_only)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Prevent deleting self
    if user.id == current_user.id:
        raise HTTPException(status_code=400, detail="You cannot delete yourself.")

    db.delete(user)
    db.commit()
    return {"message": f"User '{user.username}' deleted successfully"}

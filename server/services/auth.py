from models.user import User
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from passlib.hash import bcrypt
from models.user import User


def register_user(db: Session, user_data: dict):
    """Register a regular user (public-facing endpoint)."""
    hashed_password = bcrypt.hash(user_data["password"])

    user = User(
        username=user_data["username"],
        email=user_data["email"],
        name=user_data["name"],
        password=hashed_password,
        role="user"  # Enforce role safety
    )

    db.add(user)
    try:
        db.commit()
        db.refresh(user)
        return user
    except IntegrityError:
        db.rollback()
        raise ValueError("Username or email already exists.")


def register_admin_user(db: Session, user_data: dict, current_user: User):
    """Admin-only: create a new user with custom role (e.g., admin or user)."""
    if current_user.role != "admin":
        raise PermissionError("Only admins can create users with elevated roles.")

    valid_roles = ["admin", "user"]
    role = user_data.get("role", "user")
    if role not in valid_roles:
        raise ValueError("Invalid role.")

    hashed_password = bcrypt.hash(user_data["password"])

    user = User(
        username=user_data["username"],
        email=user_data["email"],
        name=user_data["name"],
        password=hashed_password,
        role=role
    )

    db.add(user)
    try:
        db.commit()
        db.refresh(user)
        return user
    except IntegrityError:
        db.rollback()
        raise ValueError("Username or email already exists.")

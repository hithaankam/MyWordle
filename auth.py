from sqlalchemy import func

from database import SessionLocal
from models import Result, User
from validators import (
    validate_username,
    validate_password,
    validate_confirm_password,
)


def register_user(username, password, confirm_password):
    session = SessionLocal()

    try:
        errors = []

        username = username.strip()
        username_key = username.lower()

        errors.extend(validate_username(username))
        errors.extend(validate_password(password))
        errors.extend(
            validate_confirm_password(password, confirm_password)
        )

        existing_user = (
            session.query(User)
            .filter(func.lower(User.username) == username_key)
            .first()
        )

        if existing_user:
            errors.append("Username already exists.")

        if errors:
            return Result(
                success=False,
                errors=errors
            )

        new_user = User(
            username=username,
            password=password,
            role="PLAYER"
        )

        session.add(new_user)
        session.commit()

        return Result(
            success=True,
            errors=[]
        )

    finally:
        session.close()


def create_admin(username, password):
    session = SessionLocal()

    try:
        admin = User(
            username=username.strip(),
            password=password,
            role="ADMIN"
        )

        session.add(admin)
        session.commit()

    finally:
        session.close()


def login_user(username, password, is_admin=False):
    session = SessionLocal()

    try:
        username_key = username.strip().lower()

        user = (
            session.query(User)
            .filter(func.lower(User.username) == username_key)
            .first()
        )

        if user is None:
            return Result(
                success=False,
                errors=["Invalid username or password."]
            )

        if user.password != password:
            return Result(
                success=False,
                errors=["Invalid username or password."]
            )

        if is_admin and user.role != "ADMIN":
            return Result(
                success=False,
                errors=["Invalid username or password."]
            )

        if not is_admin and user.role != "PLAYER":
            return Result(
                success=False,
                errors=["Invalid username or password."]
            )

        return Result(
            success=True,
            errors=[]
        )

    finally:
        session.close()
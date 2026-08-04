from models import Result
from storage import users, PLAYER, ADMIN
from validators import (
    validate_username,
    validate_password,
    validate_confirm_password
)



def register_user(username, password, confirm_password):

    errors = []

    username = username.strip()
    username_key = username.lower()

    errors.extend(validate_username(username))
    errors.extend(validate_password(password))
    errors.extend(
        validate_confirm_password(password, confirm_password)
    )

    if username_key in users:
        errors.append("Username already exists.")

    if errors:
        return Result(
            success=False,
            errors=errors
        )

    users[username_key] = {
        "username": username,
        "password": password,
        "role": PLAYER
    }

    return Result(
        success=True,
        errors=[]
    )


def create_admin(username, password):

    username = username.strip()

    users[username.lower()] = {
        "username": username,
        "password": password,
        "role": ADMIN
    }


def login_user(username, password, is_admin=False):

    username_key = username.strip().lower()

    if username_key not in users:
        return Result(
            success=False,
            errors=["Invalid username or password."]
        )

    user = users[username_key]

    if user["password"] != password:
        return Result(
            success=False,
            errors=["Invalid username or password."]
        )

    if is_admin and user["role"] != ADMIN:
        return Result(
            success=False,
            errors=["Invalid username or password."]
        )

    if not is_admin and user["role"] != PLAYER:
        return Result(
            success=False,
            errors=["Invalid username or password."]
        )

    return Result(
        success=True,
        errors=[]
    )
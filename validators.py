import re


def validate_username(username):
    errors = []

    if username == "":
        errors.append("Username cannot be empty.")

    elif len(username) < 5:
        errors.append("Username must be at least 5 characters long.")

    return errors


def validate_password(password):
    errors = []

    if password == "":
        errors.append("Password cannot be empty.")
        return errors

    if len(password) < 5:
        errors.append("Password must be at least 5 characters long.")

    if not re.search(r"[A-Za-z]", password):
        errors.append(
            "Password must contain at least one alphabet character."
        )

    if not re.search(r"\d", password):
        errors.append(
            "Password must contain at least one number."
        )

    allowed = "$%*&"

    specials = re.findall(r"[^A-Za-z0-9]", password)

    if len(specials) == 0:
        errors.append(
            "Password must contain at least one special character ($, %, *, &)."
        )

    elif any(ch not in allowed for ch in specials):
        errors.append(
            "Password contains invalid special characters. Allowed characters are $, %, *, &."
        )

    return errors


def validate_confirm_password(password, confirm_password):

    if password != confirm_password:
        return ["Password and confirmation do not match."]

    return []
from auth import register_user, login_user, create_admin

def test_player_can_register_with_valid_credentials():
    result = register_user(
        username="AliceA",
        password="Pass1$",
        confirm_password="Pass1$"
    )

    assert result.success is True
    assert result.errors == []


def test_register_duplicate_username():
    register_user(
        username="BobBB",
        password="Pass2$",
        confirm_password="Pass2$"
    )

    result = register_user(
        username="BobBB",
        password="Pass3$",
        confirm_password="Pass3$"
    )

    assert result.success is False
    assert "Username already exists." in result.errors


def test_register_duplicate_username_different_case():
    register_user(
        username="AliceA",
        password="Pass1$",
        confirm_password="Pass1$"
    )

    result = register_user(
        username="alicea",
        password="Pass2$",
        confirm_password="Pass2$"
    )

    assert result.success is False
    assert "Username already exists." in result.errors


def test_register_username_too_short():
    result = register_user(
        username="Abc",
        password="Pass1$",
        confirm_password="Pass1$"
    )

    assert result.success is False
    assert "Username must be at least 5 characters long." in result.errors


def test_register_empty_username():
    result = register_user(
        username="",
        password="Pass1$",
        confirm_password="Pass1$"
    )

    assert result.success is False
    assert "Username cannot be empty." in result.errors


def test_register_password_too_short():
    result = register_user(
        username="CharlieC",
        password="P1$",
        confirm_password="P1$"
    )

    assert result.success is False
    assert "Password must be at least 5 characters long." in result.errors


def test_register_empty_password():
    result = register_user(
        username="EmptyPass",
        password="",
        confirm_password=""
    )

    assert result.success is False
    assert "Password cannot be empty." in result.errors


def test_register_password_missing_alphabet():
    result = register_user(
        username="DavidD",
        password="12345$",
        confirm_password="12345$"
    )

    assert result.success is False
    assert "Password must contain at least one alphabet character." in result.errors


def test_register_password_missing_number():
    result = register_user(
        username="EveEE",
        password="Alpha$",
        confirm_password="Alpha$"
    )

    assert result.success is False
    assert "Password must contain at least one number." in result.errors


def test_register_password_missing_special_character():
    result = register_user(
        username="FrankF",
        password="Alpha1",
        confirm_password="Alpha1"
    )

    assert result.success is False
    assert (
        "Password must contain at least one special character ($, %, *, &)."
        in result.errors
    )


def test_register_password_invalid_special_character():
    result = register_user(
        username="GraceG",
        password="Alpha1@",
        confirm_password="Alpha1@"
    )

    assert result.success is False
    assert (
        "Password contains invalid special characters. Allowed characters are $, %, *, &."
        in result.errors
    )


def test_register_password_confirmation_mismatch():
    result = register_user(
        username="HankHH",
        password="Alpha1$",
        confirm_password="Alpha2$"
    )

    assert result.success is False
    assert "Password and confirmation do not match." in result.errors


def test_register_password_multiple_errors():
    result = register_user(
        username="MultiError",
        password="abc",
        confirm_password="abc"
    )

    assert result.success is False
    assert "Password must be at least 5 characters long." in result.errors
    assert "Password must contain at least one number." in result.errors
    assert (
        "Password must contain at least one special character ($, %, *, &)."
        in result.errors
    )



def test_player_can_login_with_valid_credentials():
    register_user(
        username="PlayerOne",
        password="Pass1$",
        confirm_password="Pass1$"
    )

    result = login_user(
        username="PlayerOne",
        password="Pass1$"
    )

    assert result.success is True
    assert result.errors == []


def test_admin_can_login_with_valid_credentials():
    create_admin(
        username="admin",
        password="Admin1$"
    )

    result = login_user(
        username="admin",
        password="Admin1$",
        is_admin=True
    )

    assert result.success is True
    assert result.errors == []


def test_player_cannot_login_as_admin():
    register_user(
        username="PlayerRole",
        password="Pass1$",
        confirm_password="Pass1$"
    )

    result = login_user(
        username="PlayerRole",
        password="Pass1$",
        is_admin=True
    )

    assert result.success is False
    assert "Invalid username or password." in result.errors


def test_admin_cannot_login_as_player():
    create_admin(
        username="admin2",
        password="Admin2$"
    )

    result = login_user(
        username="admin2",
        password="Admin2$",
        is_admin=False
    )

    assert result.success is False
    assert "Invalid username or password." in result.errors


def test_login_wrong_password():
    register_user(
        username="PlayerTwo",
        password="Pass1$",
        confirm_password="Pass1$"
    )

    result = login_user(
        username="PlayerTwo",
        password="Wrong1$"
    )

    assert result.success is False
    assert "Invalid username or password." in result.errors


def test_login_unknown_user():
    result = login_user(
        username="UnknownUser",
        password="Pass1$"
    )

    assert result.success is False
    assert "Invalid username or password." in result.errors


def test_login_username_case_insensitive():
    register_user(
        username="AliceA",
        password="Pass1$",
        confirm_password="Pass1$"
    )

    result = login_user(
        username="alicea",
        password="Pass1$"
    )

    assert result.success is True
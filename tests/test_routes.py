from app import create_app
from auth import register_user
from game_service import start_game


def test_login_page_renders():
    app = create_app()
    client = app.test_client()

    response = client.get("/login")

    assert response.status_code == 200
    assert b"Sign in" in response.data


def test_dashboard_requires_login():
    app = create_app()
    client = app.test_client()

    response = client.get("/dashboard", follow_redirects=False)

    assert response.status_code == 302
    assert response.headers["Location"].endswith("/login")


def test_guess_colors_persist_after_logout_and_login():
    app = create_app()
    client = app.test_client()

    register_user("ColorUser", "Pass1$", "Pass1$")
    game = start_game("ColorUser", word="APPLE")

    client.post(
        "/login",
        data={"username": "ColorUser", "password": "Pass1$"},
        follow_redirects=False,
    )

    client.post(
        "/game",
        data={"game_id": game.game_id, "guess": "APPLE"},
        follow_redirects=False,
    )

    client.get("/logout", follow_redirects=False)

    client.post(
        "/login",
        data={"username": "ColorUser", "password": "Pass1$"},
        follow_redirects=False,
    )

    response = client.get(f"/game?game_id={game.game_id}", follow_redirects=False)

    assert response.status_code == 200
    assert b"tile-GREEN" in response.data

from auth import register_user
from game_service import start_game, get_game
from guess_service import submit_guess, get_guesses


def test_player_can_submit_guess():
    register_user(
        username="GuessPlayer01",
        password="Pass1$",
        confirm_password="Pass1$"
    )

    game = start_game("GuessPlayer01")

    result = submit_guess(
        game.game_id,
        "APPLE"
    )

    assert result.success is True
    assert result.errors == []
    assert result.colors is not None


def test_guess_is_saved():
    register_user(
        username="GuessPlayer02",
        password="Pass1$",
        confirm_password="Pass1$"
    )

    game = start_game("GuessPlayer02")

    submit_guess(
        game.game_id,
        "APPLE"
    )

    guesses = get_guesses(game.game_id)

    assert len(guesses) == 1
    assert guesses[0].guessed_word == "APPLE"
    assert guesses[0].guess_number == 1


def test_multiple_guesses_are_saved_in_order():
    register_user(
        username="GuessPlayer03",
        password="Pass1$",
        confirm_password="Pass1$"
    )

    game = start_game("GuessPlayer03")

    submit_guess(game.game_id, "APPLE")
    submit_guess(game.game_id, "HOUSE")

    guesses = get_guesses(game.game_id)

    assert len(guesses) == 2
    assert guesses[0].guess_number == 1
    assert guesses[1].guess_number == 2


def test_guess_updates_guess_count():
    register_user(
        username="GuessPlayer04",
        password="Pass1$",
        confirm_password="Pass1$"
    )

    game = start_game("GuessPlayer04")

    submit_guess(game.game_id, "APPLE")

    game = get_game(game.game_id)

    assert game.guesses_used == 1


def test_invalid_guess_is_rejected():
    register_user(
        username="GuessPlayer05",
        password="Pass1$",
        confirm_password="Pass1$"
    )

    game = start_game("GuessPlayer05")

    result = submit_guess(
        game.game_id,
        "abc"
    )

    assert result.success is False
    assert len(result.errors) == 1


def test_cannot_submit_guess_after_game_is_over():
    register_user(
        username="GuessPlayer06",
        password="Pass1$",
        confirm_password="Pass1$"
    )

    game = start_game("GuessPlayer06")

    # Lose the game
    for _ in range(5):
        submit_guess(game.game_id, "ZZZZZ")

    result = submit_guess(
        game.game_id,
        "APPLE"
    )

    assert result.success is False
    assert "Game has already ended." in result.errors


def test_game_status_changes_to_won():
    register_user(
        username="GuessPlayer07",
        password="Pass1$",
        confirm_password="Pass1$"
    )

    game = start_game("GuessPlayer07")

    # We don't know the secret word, so skip if not guessed.
    # This test will be updated once deterministic word selection is added.
    pass


def test_game_status_changes_to_lost():
    register_user(
        username="GuessPlayer08",
        password="Pass1$",
        confirm_password="Pass1$"
    )

    game = start_game("GuessPlayer08")

    for _ in range(5):
        submit_guess(game.game_id, "ZZZZZ")

    game = get_game(game.game_id)

    assert game.status == "LOST"

def test_game_returns_active_status_after_wrong_guess():
    register_user(
        username="GuessPlayer09",
        password="Pass1$",
        confirm_password="Pass1$"
    )

    game = start_game("GuessPlayer09")

    result = submit_guess(
        game.game_id,
        "ZZZZZ"
    )

    assert result.success
    assert result.game_status == "ACTIVE"
    assert result.message is None

def test_game_returns_win_status():
    register_user(
        username="GuessPlayer10",
        password="Pass1$",
        confirm_password="Pass1$"
    )

    game = start_game(
        "GuessPlayer10",
        word="APPLE"
    )

    result = submit_guess(
        game.game_id,
        "APPLE"
    )

    assert result.success
    assert result.game_status == "WON"
    assert result.message == "Congratulations! You guessed the word."

def test_game_returns_loss_status():
    register_user(
        username="GuessPlayer11",
        password="Pass1$",
        confirm_password="Pass1$"
    )

    game = start_game(
        "GuessPlayer11",
        word="APPLE"
    )

    for _ in range(4):
        submit_guess(game.game_id, "ZZZZZ")

    result = submit_guess(
        game.game_id,
        "ZZZZZ"
    )

    assert result.success
    assert result.game_status == "LOST"
    assert result.message == "Better luck next time."
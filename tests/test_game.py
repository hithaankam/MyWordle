from auth import register_user
from game_service import (
    start_game,
    get_game,
)


def test_player_can_start_game():
    register_user(
        username="GamePlayer1",
        password="Pass1$",
        confirm_password="Pass1$"
    )

    result = start_game("GamePlayer1")

    assert result.success is True


def test_new_game_has_zero_guesses():
    register_user(
        username="GamePlayer2",
        password="Pass1$",
        confirm_password="Pass1$"
    )

    result = start_game("GamePlayer2")

    game = get_game(result.game_id)

    assert game.guesses_used == 0


def test_new_game_is_active():
    register_user(
        username="GamePlayer3",
        password="Pass1$",
        confirm_password="Pass1$"
    )

    result = start_game("GamePlayer3")

    game = get_game(result.game_id)

    assert game.status == "ACTIVE"


def test_player_cannot_start_fourth_game_in_same_day():
    register_user(
        username="LimitPlayer",
        password="Pass1$",
        confirm_password="Pass1$"
    )

    start_game("LimitPlayer")
    start_game("LimitPlayer")
    start_game("LimitPlayer")

    result = start_game("LimitPlayer")

    assert result.success is False
    assert "Daily game limit reached." in result.errors


def test_player_does_not_receive_same_word_twice():
    register_user(
        username="HistoryPlayer",
        password="Pass1$",
        confirm_password="Pass1$"
    )

    first = start_game("HistoryPlayer")
    second = start_game("HistoryPlayer")

    first_game = get_game(first.game_id)
    second_game = get_game(second.game_id)

    assert first_game.word_id != second_game.word_id
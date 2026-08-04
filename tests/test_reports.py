from auth import register_user
from game_service import start_game
from guess_service import submit_guess
from report_service import (
    get_daily_report,
    get_user_report
)


def test_daily_report_counts_users():
    register_user(
        "ReportPlayer01",
        "Pass1$",
        "Pass1$"
    )

    register_user(
        "ReportPlayer02",
        "Pass1$",
        "Pass1$"
    )

    start_game(
        "ReportPlayer01",
        word="APPLE"
    )

    start_game(
        "ReportPlayer02",
        word="HOUSE"
    )

    report = get_daily_report()

    assert report.success
    assert report.users == 2


def test_daily_report_counts_correct_guesses():
    register_user(
        "ReportPlayer03",
        "Pass1$",
        "Pass1$"
    )

    game = start_game(
        "ReportPlayer03",
        word="APPLE"
    )

    submit_guess(
        game.game_id,
        "APPLE"
    )

    report = get_daily_report()

    assert report.success
    assert report.correct_guesses == 1


def test_user_report_words_tried():
    register_user(
        "ReportPlayer04",
        "Pass1$",
        "Pass1$"
    )

    start_game(
        "ReportPlayer04",
        word="APPLE"
    )

    start_game(
        "ReportPlayer04",
        word="HOUSE"
    )

    report = get_user_report(
        "ReportPlayer04"
    )

    assert report.success
    assert len(report.history) == 1
    assert report.history[0]["words_tried"] == 2


def test_user_report_correct_guesses():
    register_user(
        "ReportPlayer05",
        "Pass1$",
        "Pass1$"
    )

    game = start_game(
        "ReportPlayer05",
        word="APPLE"
    )

    submit_guess(
        game.game_id,
        "APPLE"
    )

    report = get_user_report(
        "ReportPlayer05"
    )

    assert report.success
    assert len(report.history) == 1
    assert report.history[0]["correct_guesses"] == 1


def test_user_report_contains_date():
    register_user(
        "ReportPlayer06",
        "Pass1$",
        "Pass1$"
    )

    start_game(
        "ReportPlayer06",
        word="APPLE"
    )

    report = get_user_report(
        "ReportPlayer06"
    )

    assert report.success
    assert len(report.history) == 1
    assert "date" in report.history[0]


def test_unknown_user_report():
    report = get_user_report(
        "UnknownUser"
    )

    assert not report.success
    assert "User not found." in report.errors
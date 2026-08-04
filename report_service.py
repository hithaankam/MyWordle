from collections import defaultdict
from datetime import date

from sqlalchemy import func

from database import SessionLocal
from models import DailyReport, UserReport, User, Game


def get_daily_report(report_date=None):
    session = SessionLocal()

    try:
        if report_date is None:
            report_date = date.today()

        games = (
            session.query(Game)
            .filter(
                func.date(Game.started_at) == report_date
            )
            .all()
        )

        users = len(
            {
                game.user_id
                for game in games
            }
        )

        correct_guesses = sum(
            1
            for game in games
            if game.status == "WON"
        )

        return DailyReport(
            success=True,
            users=users,
            correct_guesses=correct_guesses
        )

    finally:
        session.close()


def get_user_report(username):
    session = SessionLocal()

    try:
        user = (
            session.query(User)
            .filter(
                User.username.ilike(username)
            )
            .first()
        )

        if user is None:
            return UserReport(
                success=False,
                errors=["User not found."]
            )

        games = (
            session.query(Game)
            .filter(
                Game.user_id == user.id
            )
            .order_by(Game.started_at)
            .all()
        )

        grouped = defaultdict(
            lambda: {
                "words_tried": 0,
                "correct_guesses": 0
            }
        )

        for game in games:
            played_date = game.started_at.date()

            grouped[played_date]["words_tried"] += 1

            if game.status == "WON":
                grouped[played_date]["correct_guesses"] += 1

        history = []

        for played_date in sorted(grouped):
            history.append(
                {
                    "date": played_date,
                    "words_tried": grouped[played_date]["words_tried"],
                    "correct_guesses": grouped[played_date]["correct_guesses"]
                }
            )

        return UserReport(
            success=True,
            history=history
        )

    finally:
        session.close()
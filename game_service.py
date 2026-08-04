from datetime import date

from sqlalchemy import func

from database import SessionLocal
from models import Result, User, Word, Game

from random import choice


DAILY_GAME_LIMIT = 3


def start_game(username, word = None):
    session = SessionLocal()

    try:

        user = (
            session.query(User)
            .filter(
                func.lower(User.username) == username.lower()
            )
            .first()
        )

        if user is None:
            return Result(
                success=False,
                errors=["User not found."]
            )

        today_games = (
            session.query(Game)
            .filter(
                Game.user_id == user.id,
                func.date(Game.started_at) == date.today()
            )
            .count()
        )

        if today_games >= DAILY_GAME_LIMIT:
            return Result(
                success=False,
                errors=["Daily game limit reached."]
            )

        played_word_ids = (
            session.query(Game.word_id)
            .filter(
                Game.user_id == user.id
            )
            .all()
        )

        played_word_ids = {
            row[0]
            for row in played_word_ids
        }
        print("Total words:", session.query(Word).count())

        played = session.query(Game.word_id).filter(
            Game.user_id == user.id
        ).all()
        print("Played word ids:", played)

        available_words = (
            session.query(Word)
            .filter(~Word.id.in_({row[0] for row in played}))
            .all()
        )

        print("Available words:", [w.word for w in available_words])

        if not available_words:
            available_words = session.query(Word).all()

        selected_word = choice(available_words)

        game = Game(
            user_id=user.id,
            word_id=selected_word.id
        )

        session.add(game)

        session.commit()

        return Result(
            success=True,
            game_id=game.id
        )

    finally:
        session.close()


def get_game(game_id):
    session = SessionLocal()

    try:
        return (
            session.query(Game)
            .filter(
                Game.id == game_id
            )
            .first()
        )

    finally:
        session.close()
from datetime import date

from sqlalchemy import func

from database import SessionLocal
from models import Result, User, Word, Game

from random import choice


DAILY_GAME_LIMIT = 3


def start_game(username, word=None):
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
        played = session.query(Game.word_id).filter(
            Game.user_id == user.id
        ).all()

        if word is not None:
            selected_word = (
                session.query(Word)
                .filter(func.upper(Word.word) == word.upper())
                .first()
            )
            if selected_word is None:
                return Result(
                    success=False,
                    errors=["Word not found."]
                )
        else:
            available_words = (
                session.query(Word)
                .filter(~Word.id.in_({row[0] for row in played}))
                .all()
            )

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
from database import SessionLocal
from models import Result, Game, Guess, Word
from game_engine import WordleEngine
from word_service import get_all_words


def get_guesses(game_id):
    session = SessionLocal()

    try:
        return (
            session.query(Guess)
            .filter(Guess.game_id == game_id)
            .order_by(Guess.guess_number)
            .all()
        )

    finally:
        session.close()


def submit_guess(game_id, guess):
    session = SessionLocal()

    try:

        game = (
            session.query(Game)
            .filter(Game.id == game_id)
            .first()
        )

        if game is None:
            return Result(
                success=False,
                errors=["Game not found."]
            )

        if game.status != "ACTIVE":
            return Result(
                success=False,
                errors=["Game has already ended."]
            )

        allowed_words = {word.upper() for word in get_all_words()}
        normalized_guess = guess.upper().strip()
        if normalized_guess not in allowed_words:
            return Result(
                success=False,
                errors=["Guess must be a valid word from the game dictionary."]
            )

        secret_word = (
            session.query(Word)
            .filter(Word.id == game.word_id)
            .first()
        ).word

        engine = WordleEngine(secret_word)

        previous_guesses = (
            session.query(Guess)
            .filter(Guess.game_id == game.id)
            .order_by(Guess.guess_number)
            .all()
        )

        try:
            # Replay previous guesses to restore engine state
            for previous_guess in previous_guesses:
                engine.submit_guess(previous_guess.guessed_word)

            # Submit current guess
            colors = engine.submit_guess(normalized_guess)

        except ValueError as e:
            return Result(
                success=False,
                errors=[str(e)]
            )

        session.add(
            Guess(
                game_id=game.id,
                guess_number=len(previous_guesses) + 1,
                guessed_word=normalized_guess
            )
        )

        game.guesses_used = len(previous_guesses) + 1

        message = None

        if engine.is_won():
            game.status = "WON"
            message = f"Congratulations! You guessed the word: {secret_word}."

        elif engine.is_lost():
            game.status = "LOST"
            message = f"Better luck next time. The word was {secret_word}."

        session.commit()

        return Result(
            success=True,
            colors=colors,
            game_status=game.status,
            message=message
        )
    finally:
        session.close()
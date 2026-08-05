from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from database import SessionLocal
from game_service import start_game
from guess_service import submit_guess
from models import Game, Guess, User, Word
from game_engine import WordleEngine


game_bp = Blueprint("game", __name__)


@game_bp.route("/game", methods=["GET", "POST"])
def play_game():
    if "user_id" not in session:
        flash("Please log in to continue.", "warning")
        return redirect(url_for("auth.login"))

    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == session["user_id"]).first()
        game_id = request.args.get("game_id")
        game = None

        if request.method == "POST":
            game_id = request.form.get("game_id")
            if not game_id:
                result = start_game(user.username)
                if not result.success:
                    flash(result.errors[0], "danger")
                    return redirect(url_for("dashboard.player_dashboard"))
                game_id = result.game_id
            else:
                game_id = int(game_id)

            if request.form.get("guess"):
                result = submit_guess(game_id, request.form["guess"].upper())
                if not result.success:
                    flash(result.errors[0], "danger")
                else:
                    if result.message:
                        flash(result.message, "success" if result.game_status == "WON" else "info")

            return redirect(url_for("game.play_game", game_id=game_id))

        if game_id:
            game = db.query(Game).filter(Game.id == int(game_id)).first()
        else:
            active_games = (
                db.query(Game)
                .filter(Game.user_id == user.id, Game.status == "ACTIVE")
                .order_by(Game.started_at.desc())
                .all()
            )
            if active_games:
                game = active_games[0]
            else:
                result = start_game(user.username)
                if not result.success:
                    flash(result.errors[0], "danger")
                    return redirect(url_for("dashboard.player_dashboard"))
                game = db.query(Game).filter(Game.id == result.game_id).first()

        if game is None:
            flash("Game not found.", "danger")
            return redirect(url_for("dashboard.player_dashboard"))

        guesses = (
            db.query(Guess)
            .filter(Guess.game_id == game.id)
            .order_by(Guess.guess_number)
            .all()
        )
        word = db.query(Word).filter(Word.id == game.word_id).first()

        guess_colors_by_number = {}
        if guesses:
            secret_word = word.word
            engine = WordleEngine(secret_word)
            for guess in guesses:
                colors = engine.submit_guess(guess.guessed_word)
                guess_colors_by_number[str(guess.guess_number)] = [
                    state.value if hasattr(state, "value") else str(state)
                    for state in colors
                ]

        return render_template(
            "game.html",
            game=game,
            guesses=guesses,
            word=word,
            user=user,
            guess_colors_by_number=guess_colors_by_number,
        )
    finally:
        db.close()


@game_bp.route("/new-game")
def new_game():
    if "user_id" not in session:
        flash("Please log in to continue.", "warning")
        return redirect(url_for("auth.login"))

    result = start_game(session.get("username"))
    if not result.success:
        flash(result.errors[0], "danger")
    else:
        flash("New game started.", "success")
    return redirect(url_for("dashboard.player_dashboard"))
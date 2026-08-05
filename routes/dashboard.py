from flask import Blueprint, redirect, render_template, session, url_for, flash

from database import SessionLocal
from models import Game, User
from report_service import get_daily_report


dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/dashboard")
def player_dashboard():
    if "user_id" not in session:
        flash("Please log in to continue.", "warning")
        return redirect(url_for("auth.login"))

    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == session["user_id"]).first()
        games = (
            db.query(Game)
            .filter(Game.user_id == user.id)
            .order_by(Game.started_at.desc())
            .all()
        )
        active_games = [game for game in games if game.status == "ACTIVE"]
        finished_games = [game for game in games if game.status != "ACTIVE"]
        return render_template(
            "dashboard.html",
            user=user,
            games=games,
            active_games=active_games,
            finished_games=finished_games,
        )
    finally:
        db.close()


@dashboard_bp.route("/admin-dashboard")
def admin_dashboard():
    if "user_id" not in session or session.get("role") != "ADMIN":
        flash("Please log in as an admin.", "warning")
        return redirect(url_for("auth.login"))

    report = get_daily_report()
    db = SessionLocal()
    try:
        user_count = db.query(User).count()
        game_count = db.query(Game).count()
        win_count = db.query(Game).filter(Game.status == "WON").count()
        return render_template(
            "admin_dashboard.html",
            report=report,
            user_count=user_count,
            game_count=game_count,
            win_count=win_count,
        )
    finally:
        db.close()
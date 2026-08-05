from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session,
)

from sqlalchemy import func

from auth import (
    register_user,
    login_user,
)

from database import SessionLocal
from models import User

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "GET":
        return render_template("login.html")

    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")
    is_admin = request.form.get("admin") == "on"

    result = login_user(
        username=username,
        password=password,
        is_admin=is_admin,
    )

    if not result.success:
        for error in result.errors:
            flash(error, "danger")
        return render_template("login.html")

    db = SessionLocal()

    try:

        user = (
            db.query(User)
            .filter(func.lower(User.username) == username.lower())
            .first()
        )

        session["user_id"] = user.id
        session["username"] = user.username
        session["role"] = user.role

    finally:
        db.close()

    if session["role"] == "ADMIN":
        return redirect(url_for("dashboard.admin_dashboard"))

    return redirect(url_for("dashboard.player_dashboard"))


@auth_bp.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "GET":
        return render_template("register.html")

    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")
    confirm_password = request.form.get("confirm_password", "")

    result = register_user(
        username=username,
        password=password,
        confirm_password=confirm_password,
    )

    if not result.success:

        for error in result.errors:
            flash(error, "danger")

        return render_template("register.html")

    login = login_user(
        username=username,
        password=password,
        is_admin=False,
    )

    if not login.success:
        flash("Registration successful. Please login.", "success")
        return redirect(url_for("auth.login"))

    db = SessionLocal()

    try:

        user = (
            db.query(User)
            .filter(func.lower(User.username) == username.lower())
            .first()
        )

        session["user_id"] = user.id
        session["username"] = user.username
        session["role"] = user.role

    finally:
        db.close()

    return redirect(url_for("dashboard.player_dashboard"))


@auth_bp.route("/logout")
def logout():

    session.clear()

    flash("Logged out successfully.", "success")

    return redirect(url_for("auth.login"))
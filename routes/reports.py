from flask import Blueprint, flash, redirect, render_template, session, url_for

from report_service import get_daily_report, get_user_report

reports_bp = Blueprint("reports", __name__)


@reports_bp.route("/reports/daily")
def daily_report():
    if "user_id" not in session or session.get("role") != "ADMIN":
        flash("Please log in as an admin.", "warning")
        return redirect(url_for("auth.login"))

    report = get_daily_report()
    return render_template("daily_report.html", report=report)


@reports_bp.route("/reports/user/<username>")
def user_report(username):
    if "user_id" not in session or session.get("role") != "ADMIN":
        flash("Please log in as an admin.", "warning")
        return redirect(url_for("auth.login"))

    report = get_user_report(username)
    return render_template("user_report.html", report=report, username=username)
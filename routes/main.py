from flask import Blueprint, render_template

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def home():
    return render_template("login.html")


@main_bp.route("/survey")
def survey():
    return render_template("survey.html")


@main_bp.route("/appointments")
def appointments():
    return render_template("appointments.html")


@main_bp.route("/reports")
def reports():
    return render_template("reports.html")

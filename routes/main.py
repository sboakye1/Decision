from flask import Blueprint, render_template
from utils.auth import login_required, require_role
from utils.survey import check_monthly_survey

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def home():
    return render_template("login.html")


@main_bp.route("/student_dashboard")
@login_required
@require_role("student")
@check_monthly_survey
def student_dashboard():
    return render_template("student_dashboard.html")


@main_bp.route("/counselor_dashboard")
@login_required
@require_role("counselor")
def counselor_dashboard():
    return render_template("counselor_dashboard.html")


@main_bp.route("/admin_dashboard")
@login_required
@require_role("admin")
def admin_dashboard():
    return render_template("admin_dashboard.html")


@main_bp.route("/appointments")
@login_required
def appointments():
    return render_template("appointments.html")


@main_bp.route("/reports")
@login_required
def reports():
    return render_template("reports.html")

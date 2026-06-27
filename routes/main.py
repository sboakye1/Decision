from flask import Blueprint, render_template, redirect, url_for, session, flash, request
from utils.auth import login_required, require_role
from utils.survey import check_monthly_survey
from services.student_service import StudentService
from services.admin_service import AdminService

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def home():
    return render_template("login.html")


@main_bp.route("/student_dashboard")
@login_required
@require_role("student")
@check_monthly_survey
def student_dashboard():
    user_id = session.get("user_id")
    if not user_id:
        flash("Please log in to continue.", "warning")
        return redirect(url_for("auth.login"))

    profile = StudentService.get_profile(user_id)
    if not profile:
        flash("Student profile not found.", "danger")
        return redirect(url_for("auth.login"))

    survey = StudentService.get_latest_survey(profile["student_id"])
    if not survey:
        flash("No survey data available. Please complete the monthly survey.", "warning")
        return redirect(url_for("survey.survey"))

    return render_template(
        "student_dashboard.html",
        profile=profile,
        survey=survey,
    )


@main_bp.route("/counselor_dashboard")
@login_required
@require_role("counselor")
def counselor_dashboard():
    return render_template("counselor_dashboard.html")


@main_bp.route("/admin_dashboard")
@login_required
@require_role("admin")
def admin_dashboard():
    risk_filter = request.args.get("filter", "All")
    if risk_filter not in ["All", "Low", "Medium", "High"]:
        risk_filter = "All"

    surveys = AdminService.get_latest_student_surveys(
        None if risk_filter == "All" else risk_filter
    )

    return render_template(
        "admin_dashboard.html",
        surveys=surveys,
        selected_filter=risk_filter,
    )


@main_bp.route("/appointments")
@login_required
def appointments():
    return render_template("appointments.html")


@main_bp.route("/reports")
@login_required
def reports():
    return render_template("reports.html")

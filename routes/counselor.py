from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from utils.auth import login_required, require_role
from services.counselor_service import CounselorService

counselor_bp = Blueprint("counselor", __name__, template_folder="../templates")


@counselor_bp.route("/counselor_dashboard")
@login_required
@require_role("counselor")
def counselor_dashboard():
    user_id = session.get("user_id")
    counselor_id = CounselorService.get_counselor_id(user_id)
    if not counselor_id:
        flash("Counselor profile not found.", "danger")
        return redirect(url_for("auth.login"))

    students = CounselorService.get_assigned_students(counselor_id)
    appointments = CounselorService.get_upcoming_appointments(counselor_id)

    return render_template(
        "counselor_dashboard.html",
        students=students,
        appointments=appointments,
    )


@counselor_bp.route("/student_case/<int:student_id>")
@login_required
@require_role("counselor")
def student_case(student_id):
    user_id = session.get("user_id")
    counselor_id = CounselorService.get_counselor_id(user_id)
    if not counselor_id:
        flash("Counselor profile not found.", "danger")
        return redirect(url_for("auth.login"))

    case = CounselorService.get_student_case_history(student_id, counselor_id)
    if not case:
        flash("You do not have access to that student case.", "danger")
        return redirect(url_for("counselor.counselor_dashboard"))

    return render_template("student_case.html", case=case)


@counselor_bp.route("/student_note/<int:student_id>", methods=["POST"])
@login_required
@require_role("counselor")
def student_note(student_id):
    user_id = session.get("user_id")
    counselor_id = CounselorService.get_counselor_id(user_id)
    if not counselor_id:
        flash("Counselor profile not found.", "danger")
        return redirect(url_for("auth.login"))

    note_text = request.form.get("note_text", "").strip()
    if not note_text:
        flash("Note text cannot be empty.", "danger")
        return redirect(url_for("counselor.student_case", student_id=student_id))

    if CounselorService.add_note(student_id, counselor_id, note_text):
        flash("Note saved successfully.", "success")
    else:
        flash("Unable to save note.", "danger")

    return redirect(url_for("counselor.student_case", student_id=student_id))


@counselor_bp.route("/schedule_appointment/<int:student_id>", methods=["POST"])
@login_required
@require_role("counselor")
def schedule_appointment(student_id):
    user_id = session.get("user_id")
    counselor_id = CounselorService.get_counselor_id(user_id)
    if not counselor_id:
        flash("Counselor profile not found.", "danger")
        return redirect(url_for("auth.login"))

    appointment_datetime = request.form.get("appointment_datetime")
    notes = request.form.get("notes", "").strip()

    if not appointment_datetime:
        flash("Appointment date and time are required.", "danger")
        return redirect(url_for("counselor.counselor_dashboard"))

    if CounselorService.schedule_appointment(student_id, counselor_id, appointment_datetime, notes):
        flash("Appointment scheduled successfully.", "success")
    else:
        flash("Unable to schedule appointment.", "danger")

    return redirect(url_for("counselor.counselor_dashboard"))

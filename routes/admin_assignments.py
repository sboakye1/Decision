from flask import Blueprint, render_template, request, redirect, url_for, flash
from utils.auth import login_required, require_role
from services.admin_service import AdminService

admin_assignments_bp = Blueprint("admin_assignments", __name__, template_folder="../templates")


@admin_assignments_bp.route("/admin_assignments")
@login_required
@require_role("admin")
def admin_assignments():
    students = AdminService.get_assignable_students()
    counselors = AdminService.get_counselor_workload()
    return render_template(
        "admin_assignments.html",
        students=students,
        counselors=counselors,
    )


@admin_assignments_bp.route("/admin_assignments/assign", methods=["POST"])
@login_required
@require_role("admin")
def assign_student():
    student_id = request.form.get("student_id")
    counselor_id = request.form.get("counselor_id")

    if not student_id or not counselor_id:
        flash("Please select a counselor before assigning.", "danger")
        return redirect(url_for("admin_assignments.admin_assignments"))

    if AdminService.assign_student(student_id, counselor_id):
        flash("Student assigned successfully.", "success")
    else:
        flash("Unable to assign student. Try again.", "danger")

    return redirect(url_for("admin_assignments.admin_assignments"))


@admin_assignments_bp.route("/admin_assignments/close", methods=["POST"])
@login_required
@require_role("admin")
def close_assignment():
    student_id = request.form.get("student_id")
    if not student_id:
        flash("Unable to close assignment without a student.", "danger")
        return redirect(url_for("admin_assignments.admin_assignments"))

    if AdminService.close_assignment(student_id):
        flash("Assignment closed successfully.", "success")
    else:
        flash("No active assignment found for this student.", "warning")

    return redirect(url_for("admin_assignments.admin_assignments"))


@admin_assignments_bp.route("/admin_analytics")
@login_required
@require_role("admin")
def admin_analytics():
    data = AdminService.get_analytics_data()
    return render_template("admin_analytics.html", data=data)

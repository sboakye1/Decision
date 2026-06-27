from flask import session, redirect, url_for, flash
from services.survey_service import SurveyService


def check_monthly_survey(f):
    def wrapper(*args, **kwargs):
        user_id = session.get("user_id")
        if not user_id:
            flash("Please log in to continue.", "warning")
            return redirect(url_for("auth.login"))

        student_id = SurveyService.get_student_id_for_user(user_id)
        if not student_id:
            flash("Student profile not found.", "danger")
            return redirect(url_for("auth.login"))

        if not SurveyService.has_submitted_current_month(student_id):
            flash("You must complete the monthly survey before accessing the dashboard.", "warning")
            return redirect(url_for("survey.survey"))

        return f(*args, **kwargs)

    wrapper.__name__ = f.__name__
    return wrapper

from flask import render_template, request, redirect, url_for, flash, session
from services.survey_service import SurveyService


class SurveyController:
    @staticmethod
    def handle_survey():
        user_id = session.get("user_id")
        if not user_id:
            flash("Please log in to continue.", "warning")
            return redirect(url_for("auth.login"))

        student_id = SurveyService.get_student_id_for_user(user_id)
        if not student_id:
            flash("Student profile not found.", "danger")
            return redirect(url_for("auth.login"))

        if request.method == "POST":
            answers = {key: request.form.get(key) for key in SurveyService.question_keys()}

            if SurveyService.has_submitted_current_month(student_id):
                flash("You already completed this month's survey.", "info")
                return redirect(url_for("main.student_dashboard"))

            if not SurveyService.validate_answers(answers):
                flash("Please answer all survey questions before submitting.", "danger")
                return render_template("survey.html", questions=SurveyService.get_questions())

            summary = SurveyService.process_submission(student_id, answers)
            flash(f"Survey submitted successfully. Risk level: {summary['risk_level']}", "success")
            return redirect(url_for("main.student_dashboard"))

        return render_template("survey.html", questions=SurveyService.get_questions())

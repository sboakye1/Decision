from flask import Blueprint
from controllers.survey_controller import SurveyController
from utils.auth import login_required, require_role

survey_bp = Blueprint("survey", __name__, template_folder="../templates")


@survey_bp.route("/survey", methods=["GET", "POST"])
@login_required
@require_role("student")
def survey():
    return SurveyController.handle_survey()

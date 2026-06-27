from flask import Blueprint
from controllers.auth_controller import AuthController

auth_bp = Blueprint("auth", __name__, template_folder="../templates")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    return AuthController.login()


@auth_bp.route("/logout")
def logout():
    return AuthController.logout()

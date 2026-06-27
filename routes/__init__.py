from flask import Blueprint


def register_routes(app):
    from .main import main_bp
    from .auth import auth_bp
    from .survey import survey_bp
    from .counselor import counselor_bp
    from .admin_assignments import admin_assignments_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(survey_bp)
    app.register_blueprint(counselor_bp)
    app.register_blueprint(admin_assignments_bp)
    app.register_blueprint(main_bp)

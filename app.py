from datetime import timedelta
from flask import Flask
from config.config import Config
from routes import register_routes


def create_app():
    app = Flask(__name__, static_folder="static", template_folder="templates")
    app.config.from_object(Config)
    app.secret_key = app.config["SECRET_KEY"]
    app.permanent_session_lifetime = timedelta(minutes=app.config.get("SESSION_TIMEOUT_MINUTES", 30))

    register_routes(app)

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=app.config["DEBUG"])

from functools import wraps
from datetime import datetime
from flask import session, redirect, url_for, flash, current_app


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = session.get("user_id")
        last_active = session.get("last_active")

        if not user_id:
            flash("Please log in to continue.", "warning")
            return redirect(url_for("auth.login"))

        if last_active:
            try:
                last_active_dt = datetime.fromisoformat(last_active)
                if datetime.utcnow() - last_active_dt > current_app.permanent_session_lifetime:
                    session.clear()
                    flash("Your session has expired. Please log in again.", "warning")
                    return redirect(url_for("auth.login"))
            except ValueError:
                session.clear()
                return redirect(url_for("auth.login"))

        session["last_active"] = datetime.utcnow().isoformat()
        return f(*args, **kwargs)

    return decorated_function


def require_role(*allowed_roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if session.get("user_role") not in allowed_roles:
                flash("Unauthorized access.", "danger")
                return redirect(url_for("auth.login"))
            return f(*args, **kwargs)

        return decorated_function

    return decorator

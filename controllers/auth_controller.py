from flask import render_template, request, redirect, url_for, flash, session
from services.auth_service import AuthService


class AuthController:
    @staticmethod
    def login():
        if request.method == "POST":
            email = request.form.get("email", "").strip().lower()
            password = request.form.get("password", "")

            if not email or not password:
                flash("Please enter both email and password.", "danger")
                return render_template("login.html")

            user = AuthService.authenticate_user(email, password)
            if not user:
                flash("Invalid email or password.", "danger")
                return render_template("login.html")

            session.permanent = True
            session["user_id"] = user["user_id"]
            session["user_name"] = user["name"]
            session["user_role"] = user["role"]
            session["last_active"] = AuthService.current_timestamp()

            if user["role"] == "student":
                return redirect(url_for("main.student_dashboard"))
            if user["role"] == "counselor":
                return redirect(url_for("main.counselor_dashboard"))
            if user["role"] == "admin":
                return redirect(url_for("main.admin_dashboard"))

            return redirect(url_for("main.home"))

        return render_template("login.html")

    @staticmethod
    def logout():
        session.clear()
        flash("You have been logged out successfully.", "success")
        return redirect(url_for("auth.login"))

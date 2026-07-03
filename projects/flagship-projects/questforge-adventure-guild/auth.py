import re
import sqlite3
from functools import wraps

from flask import flash, redirect, render_template, request, url_for
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from werkzeug.security import check_password_hash, generate_password_hash

from database import get_db_connection, get_user_by_email, get_user_by_id
from models import User


login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.login_message = "Please log in to access this page."
login_manager.login_message_category = "warning"


@login_manager.user_loader
def load_user(user_id):
    user_row = get_user_by_id(user_id)

    if user_row is None:
        return None

    return User(user_row)


def redirect_for_role(user):
    """Send a logged-in user to the page for their account role."""
    if user.role == "GuildMaster":
        return redirect(url_for("guild_master_dashboard"))

    if user.role == "Admin":
        return redirect(url_for("admin_dashboard"))

    return redirect(url_for("adventurer_profile"))


def require_role(role):
    """Protect a view so only a logged-in user with the given role can use it."""
    def decorator(view_function):
        @wraps(view_function)
        @login_required
        def wrapped_view(*args, **kwargs):
            if current_user.role != role:
                flash("You do not have permission to access that page.", "danger")
                return redirect(url_for("home"))

            return view_function(*args, **kwargs)

        return wrapped_view

    return decorator


def login():
    if current_user.is_authenticated:
        return redirect_for_role(current_user)

    email = ""

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        if email == "" or password == "":
            flash("Please enter your email and password.", "danger")
            return render_template("login.html", email=email)

        user_row = get_user_by_email(email)

        if user_row is None or not check_password_hash(
            user_row["password_hash"],
            password,
        ):
            flash("Invalid email or password.", "danger")
            return render_template("login.html", email=email)

        user = User(user_row)
        login_user(user)
        flash(f"Welcome back, {user.first_name}.", "success")
        return redirect_for_role(user)

    return render_template("login.html", email=email)


def register():
    if current_user.is_authenticated:
        return redirect_for_role(current_user)

    form_values = {
        "first_name": "",
        "last_name": "",
        "email": "",
        "role": "Adventurer",
    }

    if request.method == "POST":
        form_values = {
            "first_name": request.form.get("first_name", "").strip(),
            "last_name": request.form.get("last_name", "").strip(),
            "email": request.form.get("email", "").strip().lower(),
            "role": request.form.get("role", "").strip(),
        }
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        if (
            form_values["first_name"] == ""
            or form_values["last_name"] == ""
            or form_values["email"] == ""
            or password == ""
            or confirm_password == ""
            or form_values["role"] == ""
        ):
            flash("Please fill in all required fields.", "danger")
            return render_template("register.html", form_values=form_values)

        if re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", form_values["email"]) is None:
            flash("Please enter a valid email address.", "danger")
            return render_template("register.html", form_values=form_values)

        if password != confirm_password:
            flash("Password and confirmation password must match.", "danger")
            return render_template("register.html", form_values=form_values)

        if form_values["role"] not in ("Adventurer", "GuildMaster"):
            flash("Please choose Adventurer or Guild Master.", "danger")
            return render_template("register.html", form_values=form_values)

        if get_user_by_email(form_values["email"]) is not None:
            flash("An account with that email already exists.", "danger")
            return render_template("register.html", form_values=form_values)

        connection = get_db_connection()

        try:
            connection.execute(
                """
                INSERT INTO users (
                    first_name, last_name, email, password_hash, role
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    form_values["first_name"],
                    form_values["last_name"],
                    form_values["email"],
                    generate_password_hash(password),
                    form_values["role"],
                ),
            )
            connection.commit()
        except sqlite3.IntegrityError:
            connection.close()
            flash("An account with that email already exists.", "danger")
            return render_template("register.html", form_values=form_values)

        connection.close()
        flash("Your account was created. You can now log in.", "success")
        return redirect(url_for("login"))

    return render_template("register.html", form_values=form_values)


def logout():
    logout_user()
    flash("You have been logged out.", "success")
    return redirect(url_for("home"))

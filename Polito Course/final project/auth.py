import sqlite3

from flask import flash, redirect, render_template, request, session, url_for
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from database import get_db_connection
from models import User


login_manager = LoginManager()
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    connection = get_db_connection()
    user = connection.execute(
        "SELECT * FROM users WHERE id = ?",
        (user_id,)
    ).fetchone()
    connection.close()

    if user is None:
        return None

    return User(user)


def save_profile_picture(uploaded_file, user_id):
    if not uploaded_file:
        return ""

    if not uploaded_file.filename:
        return ""

    filename_parts = uploaded_file.filename.rsplit(".", 1)
    if len(filename_parts) != 2:
        return ""

    extension = filename_parts[-1].lower()
    if extension not in ["jpg", "jpeg", "png", "webp"]:
        return ""

    filename = f"user_{user_id}.{extension}"
    save_path = f"static/uploads/{filename}"
    uploaded_file.save(save_path)

    return f"uploads/{filename}"


def is_safe_next_url(next_url):
    # We accept only local links such as /tour/1/reserve.
    if not next_url:
        return False

    if not next_url.startswith("/"):
        return False

    if next_url.startswith("//"):
        return False

    return True


def complete_login(user, next_url=None):
    user_object = User(user)
    login_user(user_object)

    session["user_id"] = user["id"]
    session["role"] = user["role"]
    session["full_name"] = user["full_name"]

    if "pending_login_user_ids" in session:
        session.pop("pending_login_user_ids")

    if "pending_login_next" in session:
        session.pop("pending_login_next")

    flash(f"Welcome back, {user['full_name']}.")

    if is_safe_next_url(next_url):
        if user["role"] == "Participant":
            return redirect(next_url)

    if user["role"] == "Guide":
        return redirect(url_for("guide_dashboard"))

    return redirect(url_for("participant_dashboard"))


def require_role(role):
    if not current_user.is_authenticated:
        flash("Please log in first.")
        return redirect(url_for("login"))

    if current_user.role != role:
        flash(f"This page is only available for {role.lower()} accounts.")
        return redirect(url_for("home"))

    return None


def login():
    next_url = request.args.get("next", "").strip()

    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()
        next_url = request.form.get("next", "").strip()

        if not email or not password:
            flash("Please enter both email and password.")
            return render_template("login.html", next_url=next_url)

        connection = get_db_connection()
        users = connection.execute(
            "SELECT * FROM users WHERE email = ? ORDER BY role",
            (email,)
        ).fetchall()
        connection.close()

        matching_users = []
        for user in users:
            stored_hash = None
            if "password_hash" in user.keys():
                stored_hash = user["password_hash"]

            if stored_hash:
                password_is_correct = check_password_hash(stored_hash, password)
                if password_is_correct:
                    matching_users.append(user)

        if not matching_users:
            flash("Invalid email or password.")
            return render_template("login.html", next_url=next_url)

        if len(matching_users) == 1:
            return complete_login(matching_users[0], next_url=next_url)

        pending_user_ids = []
        role_choices = []
        for user in matching_users:
            pending_user_ids.append(user["id"])
            role_choices.append(dict(user))

        session["pending_login_user_ids"] = pending_user_ids

        if is_safe_next_url(next_url):
            session["pending_login_next"] = next_url
        else:
            session["pending_login_next"] = ""

        return render_template(
            "login.html",
            role_choices=role_choices,
            next_url=next_url
        )

    return render_template("login.html", next_url=next_url)


def select_login_role():
    selected_user_id = request.form.get("user_id", "").strip()
    pending_user_ids = session.get("pending_login_user_ids", [])
    next_url = session.get("pending_login_next", "")

    try:
        selected_user_id_int = int(selected_user_id)
    except ValueError:
        flash("Please choose a valid account role.")
        return redirect(url_for("login"))

    if selected_user_id_int not in pending_user_ids:
        flash("Please log in again before choosing the account role.")
        return redirect(url_for("login"))

    connection = get_db_connection()
    user = connection.execute(
        "SELECT * FROM users WHERE id = ?",
        (selected_user_id_int,)
    ).fetchone()
    connection.close()

    if user is None:
        flash("Please log in again before choosing the account role.")
        return redirect(url_for("login"))

    return complete_login(user, next_url=next_url)


@login_required
def logout():
    logout_user()
    session.clear()
    flash("You have been logged out.")
    return redirect(url_for("home"))


def register():
    selected_role = request.args.get("role", "").strip()
    next_url = request.args.get("next", "").strip()

    if selected_role not in ["Participant", "Guide"]:
        selected_role = ""

    if not is_safe_next_url(next_url):
        next_url = ""

    if request.method == "POST":
        first_name = request.form.get("first_name", "").strip()
        last_name = request.form.get("last_name", "").strip()
        full_name = request.form.get("full_name", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()
        confirm_password = request.form.get("confirm_password", "").strip()
        role = request.form.get("role", "").strip()
        next_url = request.form.get("next", "").strip()
        profile_picture_file = request.files.get("profile_picture")

        language_list = request.form.getlist("spoken_languages")
        spoken_languages = ", ".join(language_list)

        if role not in ["Participant", "Guide"]:
            role = selected_role

        if not is_safe_next_url(next_url):
            next_url = ""

        if full_name:
            if not first_name or not last_name:
                name_parts = full_name.split(" ", 1)
                if not first_name:
                    first_name = name_parts[0]
                if not last_name:
                    if len(name_parts) > 1:
                        last_name = name_parts[1]
                    else:
                        last_name = ""

        full_name = f"{first_name} {last_name}".strip()

        if not first_name or not last_name or not email or not password or not confirm_password or not role:
            flash("Please fill in all required fields.")
            return render_template("register.html", selected_role=role, next_url=next_url)

        if password != confirm_password:
            flash("Password and confirm password do not match.")
            return render_template("register.html", selected_role=role, next_url=next_url)

        if role not in ["Participant", "Guide"]:
            flash("Please choose Participant or Guide.")
            return render_template("register.html", selected_role=role, next_url=next_url)

        if role == "Guide" and not spoken_languages:
            flash("Guides must choose at least one spoken language.")
            return render_template("register.html", selected_role=role, next_url=next_url)

        connection = get_db_connection()
        existing_same_role = connection.execute(
            "SELECT id FROM users WHERE email = ? AND role = ?",
            (email, role)
        ).fetchone()

        if existing_same_role is not None:
            connection.close()
            flash(f"This email is already registered as a {role.lower()} account.")
            return render_template("register.html", selected_role=role, next_url=next_url)

        if role == "Guide":
            saved_languages = spoken_languages
        else:
            saved_languages = ""

        try:
            cursor = connection.execute(
                """
                INSERT INTO users (
                    full_name, first_name, last_name, email, password,
                    password_hash, role, spoken_languages, profile_picture
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    full_name,
                    first_name,
                    last_name,
                    email,
                    password,
                    generate_password_hash(password),
                    role,
                    saved_languages,
                    ""
                )
            )

            new_user_id = cursor.lastrowid
            profile_picture_path = save_profile_picture(profile_picture_file, new_user_id)

            if profile_picture_path:
                connection.execute(
                    "UPDATE users SET profile_picture = ? WHERE id = ?",
                    (profile_picture_path, new_user_id)
                )

            connection.commit()
            connection.close()
        except sqlite3.IntegrityError:
            connection.close()
            flash("This email and role combination is already registered.")
            return render_template("register.html", selected_role=role, next_url=next_url)

        flash("Account created. You can now log in.")
        if next_url:
            return redirect(url_for("login", next=next_url))
        return redirect(url_for("login"))

    return render_template("register.html", selected_role=selected_role, next_url=next_url)

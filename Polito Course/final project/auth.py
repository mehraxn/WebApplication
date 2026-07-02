import re

from flask import flash, redirect, render_template, request, session, url_for
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from database import get_db_connection
from models import User



login_manager = LoginManager()

# Simple email check: some text, an @, some text, a dot, some text (no spaces).
EMAIL_PATTERN = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"

# Redirect unauthenticated users to the login page when they open a protected page.
login_manager.login_view = "login"


# Flask-Login calls this to rebuild the logged-in user from the user_id stored in the session.
@login_manager.user_loader
def load_user(user_id):
    connection = get_db_connection()
    user = connection.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    connection.close()

    if user is None:
        return None

    return User(user)


# Check that a "next" redirect URL is a safe local path before redirecting.
def is_safe_next_url(next_url):

    if next_url is None or next_url == "":
        return False

    if next_url[0] != "/":
        return False

    if next_url.startswith("//"):
        return False

    return True



def login():

    # Keep the "next" target so the user returns to the page they came from after login.
    if "next" in request.args:
        next_url = request.args["next"].strip()
    else:
        next_url = ""

    if request.method != "POST":
        return render_template("login.html", next_url=next_url)

    if "email" in request.form:
        email = request.form["email"].strip()
    else:
        email = ""

    # Passwords are kept exactly as typed; only the email is trimmed.
    if "password" in request.form:
        password = request.form["password"]
    else:
        password = ""

    if "next" in request.form:
        next_url = request.form["next"].strip()
    else:
        next_url = ""



    if email == "" and password == "":
        flash("Please enter your email and password.")
        return render_template("login.html", next_url=next_url)

    if email == "":
        flash("Please enter your email.")
        return render_template("login.html", next_url=next_url)

    if password == "":
        flash("Please enter your password.")
        return render_template("login.html", next_url=next_url)
    

    connection = get_db_connection()
    # The same email can exist under different roles (e.g. Guide and Participant).
    users_with_submitted_email = connection.execute("SELECT * FROM users WHERE email = ? ORDER BY role",(email,)).fetchall()
    connection.close()

    matching_users = []

    for x in users_with_submitted_email:
        stored_password_hash = x["password_hash"]

        password_is_correct = check_password_hash(stored_password_hash, password)

        if password_is_correct is True:
            matching_users.append(x)

    if len(matching_users) == 0:
        flash("Invalid email or password.")
        return render_template("login.html", next_url=next_url)

    if len(matching_users) == 1:
        return complete_login(matching_users[0], next_url=next_url)

    # Multiple matches mean the same email and password belong to more than one role,
    # so let the user choose which account to log in as.
    pending_user_ids = []
    role_choices = []

    for x in matching_users:
        pending_user_ids.append(x["id"])
        role_choices.append(dict(x))

    # Stored for use in select_login_role().
    session["pending_login_user_ids"] = pending_user_ids

    if not is_safe_next_url(next_url):
        next_url = ""

    session["pending_login_next"] = next_url

    # Re-render login with the role choices so the template can show the selection modal.
    return render_template("login.html",role_choices=role_choices, next_url=next_url)


# Called when a user picks a role in the modal shown for accounts that share an email and password.
def select_login_role():

    if "user_id" in request.form:
        selected_user_id = request.form["user_id"].strip()
    else:
        selected_user_id = ""

    if "pending_login_user_ids" in session:
        pending_user_ids = session["pending_login_user_ids"]
    else:
        pending_user_ids = []

    if "pending_login_next" in session:
        next_url = session["pending_login_next"]
    else:
        next_url = ""

    if not selected_user_id.isdigit():
        flash("Please choose a valid account role.")
        return redirect(url_for("login"))

    selected_user_id_int = int(selected_user_id)

    if selected_user_id_int not in pending_user_ids:
        flash("Please log in again before choosing the account role.")
        return redirect(url_for("login"))

    connection = get_db_connection()
    user = connection.execute("SELECT * FROM users WHERE id = ?", (selected_user_id_int,)).fetchone()
    connection.close()

    if user is None:
        flash("Please log in again before choosing the account role.")
        return redirect(url_for("login"))

    return complete_login(user, next_url=next_url)



def complete_login(attempting_user, next_url):
    
    if next_url is None or next_url == "":
        next_url = None

    
    user_object = User(attempting_user)

    # Register the successful login with Flask-Login.
    login_user(user_object)

    # Also store identity in the session for the parts of the app that read it directly.
    session["user_id"] = attempting_user["id"]
    
    session["role"] = attempting_user["role"]
    
    session["full_name"] = attempting_user["full_name"]

    if "pending_login_user_ids" in session:
        session.pop("pending_login_user_ids")


    if "pending_login_next" in session:
        session.pop("pending_login_next")

    flash("Welcome back, " + str(attempting_user["full_name"]) + ".")

    role = attempting_user["role"]


    if role == "Participant" and is_safe_next_url(next_url):
        return redirect(next_url)

    if role == "Guide":
        return redirect(url_for("guide_dashboard"))

    if role == "Admin":
        return redirect(url_for("admin_dashboard"))

    return redirect(url_for("participant_dashboard"))


@login_required
def logout():
    logout_user()
    session.clear()
    flash("You have been logged out.")
    return redirect(url_for("home"))


def register():

    # A pre-selected role may arrive in the URL (e.g. "Register as participant" from the reservation page).
    if "role" in request.args:
        selected_role = request.args["role"].strip()
    else:
        selected_role = ""

    # Keep the "next" target so the user can return to it after registering.
    if "next" in request.args:
        next_url = request.args["next"].strip()
    else:
        next_url = ""

    if selected_role not in ["Participant", "Guide"]:
        selected_role = ""

    if not is_safe_next_url(next_url):
        next_url = ""

    if request.method != "POST":
        return render_template(
            "register.html",
            selected_role=selected_role,
            next_url=next_url
        )

    if "first_name" in request.form:
        first_name = request.form["first_name"].strip()
    else:
        first_name = ""

    if "last_name" in request.form:
        last_name = request.form["last_name"].strip()
    else:
        last_name = ""

    if "email" in request.form:
        email = request.form["email"].strip()
    else:
        email = ""

    # Passwords are kept exactly as typed; only the email is trimmed.
    if "password" in request.form:
        password = request.form["password"]
    else:
        password = ""

    if "confirm_password" in request.form:
        confirm_password = request.form["confirm_password"]
    else:
        confirm_password = ""

    if "role" in request.form:
        role = request.form["role"].strip()
    else:
        role = ""

    if "next" in request.form:
        next_url = request.form["next"].strip()
    else:
        next_url = ""

    if "spoken_languages" in request.form:
        language_list = request.form.getlist("spoken_languages")
    else:
        language_list = []

    spoken_languages = ", ".join(language_list)

    if role not in ["Participant", "Guide"]:
        role = selected_role

    if not is_safe_next_url(next_url):
        next_url = ""

    # The register form has separate first name and last name fields,
    # so we simply build full_name from them for display (dashboards, etc.).
    full_name = first_name + " " + last_name
    full_name = full_name.strip()

    if first_name == "":
        flash("Please fill in all required fields.")
        return render_template("register.html", selected_role=role, next_url=next_url)

    if last_name == "":
        flash("Please fill in all required fields.")
        return render_template("register.html", selected_role=role, next_url=next_url)

    if email == "":
        flash("Please fill in all required fields.")
        return render_template("register.html", selected_role=role, next_url=next_url)

    if re.match(EMAIL_PATTERN, email) is None:
        flash("Please enter a valid email address.")
        return render_template("register.html", selected_role=role, next_url=next_url)

    if password == "":
        flash("Please fill in all required fields.")
        return render_template("register.html", selected_role=role, next_url=next_url)

    if confirm_password == "":
        flash("Please fill in all required fields.")
        return render_template("register.html", selected_role=role, next_url=next_url)

    if role == "":
        flash("Please fill in all required fields.")
        return render_template("register.html", selected_role=role, next_url=next_url)

    if password != confirm_password:
        flash("Password and confirm password do not match.")
        return render_template("register.html", selected_role=role, next_url=next_url)

    if role not in ["Participant", "Guide"]:
        flash("Please choose Participant or Guide.")
        return render_template("register.html", selected_role=role, next_url=next_url)

    if role == "Guide":
        allowed_languages = ["Italian", "English", "Spanish", "Portuguese", "German"]

        if len(language_list) == 0:
            flash("Guides must choose at least one spoken language.")
            return render_template("register.html", selected_role=role, next_url=next_url)

        for x in language_list:
            if x not in allowed_languages:
                flash("Please choose valid spoken languages.")
                return render_template("register.html", selected_role=role, next_url=next_url)

    connection = get_db_connection()

    # The same email may register once per role, so block only duplicates of the same role.
    existing_same_role = connection.execute(
        "SELECT id FROM users WHERE email = ? AND role = ?",
        (email, role)
    ).fetchone()

    if existing_same_role is not None:
        connection.close()
        flash("This email is already registered as a " + role.lower() + " account.")
        return render_template("register.html", selected_role=role, next_url=next_url)

    if role == "Guide":
        saved_languages = spoken_languages
    else:
        saved_languages = ""

    connection.execute(
        """
        INSERT INTO users (
            full_name, first_name, last_name, email,
            password_hash, role, spoken_languages
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            full_name,
            first_name,
            last_name,
            email,
            generate_password_hash(password),
            role,
            saved_languages
        )
    )

    connection.commit()
    connection.close()

    flash("Account created. You can now log in.")

    if next_url is not None and next_url != "":
        return redirect(url_for("login", next=next_url))

    return redirect(url_for("login"))

# Guard a page so only logged-in users with the given role can access it.
# Returns None when access is allowed, or a redirect response otherwise.
def require_role(role):

    if not current_user.is_authenticated:
        flash("Please log in first.")
        return redirect(url_for("login"))

    if current_user.role == role:
        return None

    flash("This page is only available for " + role.lower() + " accounts.")
    return redirect(url_for("home"))

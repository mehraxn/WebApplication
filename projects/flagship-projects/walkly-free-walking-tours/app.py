import os

from flask import Flask, render_template

from admin import admin_dashboard as admin_dashboard_page
from auth import login_manager
from auth import login as login_page
from auth import logout as logout_page
from auth import register as register_page
from auth import select_login_role as select_login_role_page
from database import initialize_database
from guide import completed_tours as completed_tours_page
from guide import create_tour as create_tour_page
from guide import edit_tour as edit_tour_page
from guide import guide_dashboard as guide_dashboard_page
from reservations import cancel_reservation as cancel_reservation_page
from reservations import my_reservations as my_reservations_page
from reservations import participant_dashboard as participant_dashboard_page
from reservations import reserve_tour as reserve_tour_page
from tours import guide_profile as guide_profile_page
from tours import home as home_page
from tours import tour_detail as tour_detail_page


app = Flask(__name__)

# Read the secret key from the environment in production; the fallback keeps local testing simple.
app.config["SECRET_KEY"] = os.environ.get(
    "SECRET_KEY",
    "replace-this-dev-key-with-a-random-production-secret"
)

# Limit uploaded files to 8 MB.
app.config["MAX_CONTENT_LENGTH"] = 8 * 1024 * 1024

login_manager.init_app(app)
initialize_database()


@app.route("/")
def home():
    return home_page()


@app.route("/tour/<int:tour_id>")
def tour_detail(tour_id):
    return tour_detail_page(tour_id)


@app.route("/guide/<int:guide_id>")
def guide_profile(guide_id):
    return guide_profile_page(guide_id)


@app.route("/login", methods=["GET", "POST"])
def login():
    return login_page()


@app.route("/login/select-role", methods=["POST"])
def select_login_role():
    return select_login_role_page()


@app.route("/logout")
def logout():
    return logout_page()


@app.route("/register", methods=["GET", "POST"])
def register():
    return register_page()


@app.route("/tour/<int:tour_id>/reserve", methods=["GET", "POST"])
def reserve_tour(tour_id):
    return reserve_tour_page(tour_id)


@app.route("/participant-dashboard")
def participant_dashboard():
    return participant_dashboard_page()


@app.route("/my-reservations")
def my_reservations():
    return my_reservations_page()


@app.route("/reservation/<int:reservation_id>/cancel", methods=["POST"])
def cancel_reservation(reservation_id):
    return cancel_reservation_page(reservation_id)


@app.route("/guide-dashboard")
def guide_dashboard():
    return guide_dashboard_page()


@app.route("/guide/create-tour", methods=["GET", "POST"])
def create_tour():
    return create_tour_page()


@app.route("/guide/edit-tour/<int:tour_id>", methods=["GET", "POST"])
def edit_tour(tour_id):
    return edit_tour_page(tour_id)


@app.route("/guide/completed-tours", methods=["GET", "POST"])
def completed_tours():
    return completed_tours_page()


@app.route("/admin-dashboard")
def admin_dashboard():
    return admin_dashboard_page()


@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404


@app.errorhandler(500)
def server_error(error):
    return render_template("500.html"), 500


if __name__ == "__main__":
    # Debug mode is enabled only when FLASK_DEBUG=1 is set in the environment.
    app.run(debug=os.environ.get("FLASK_DEBUG") == "1")

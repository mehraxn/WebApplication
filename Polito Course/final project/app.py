from pathlib import Path

from flask import Flask

from auth import login, login_manager, logout, register, select_login_role
from database import initialize_database
from guide import completed_tours, create_tour, edit_tour, guide_dashboard
from reservations import cancel_reservation, my_reservations, participant_dashboard, reserve_tour
from tours import home, tour_detail

app = Flask(__name__)
app.config["SECRET_KEY"] = "temporary-secret-key"
app.config["UPLOAD_FOLDER"] = "static/uploads"
Path(app.root_path, app.config["UPLOAD_FOLDER"]).mkdir(parents=True, exist_ok=True)

login_manager.init_app(app)
initialize_database()

app.add_url_rule("/", "home", home)
app.add_url_rule("/tour/<int:tour_id>", "tour_detail", tour_detail)
app.add_url_rule("/tour/<int:tour_id>/reserve", "reserve_tour", reserve_tour, methods=["GET", "POST"])

app.add_url_rule("/login", "login", login, methods=["GET", "POST"])
app.add_url_rule("/logout", "logout", logout)
app.add_url_rule("/login/select-role", "select_login_role", select_login_role, methods=["POST"])
app.add_url_rule("/register", "register", register, methods=["GET", "POST"])

app.add_url_rule("/participant-dashboard", "participant_dashboard", participant_dashboard)
app.add_url_rule("/my-reservations", "my_reservations", my_reservations)
app.add_url_rule("/reservation/<int:reservation_id>/cancel", "cancel_reservation", cancel_reservation, methods=["POST"])

app.add_url_rule("/guide-dashboard", "guide_dashboard", guide_dashboard)
app.add_url_rule("/guide/create-tour", "create_tour", create_tour, methods=["GET", "POST"])
app.add_url_rule("/guide/edit-tour/<int:tour_id>", "edit_tour", edit_tour, methods=["GET", "POST"])
app.add_url_rule("/guide/completed-tours", "completed_tours", completed_tours, methods=["GET", "POST"])


if __name__ == "__main__":
    app.run(debug=True)

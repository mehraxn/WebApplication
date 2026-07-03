import os

from flask import Flask
from flask_login import login_required

from admin import admin_dashboard as admin_dashboard_page
from auth import login as login_page
from auth import login_manager
from auth import logout as logout_page
from auth import register as register_page
from auth import require_role
from database import initialize_database
from guild_master import cancel_session as cancel_session_page
from guild_master import create_quest as create_quest_page
from guild_master import edit_session as edit_session_page
from guild_master import guild_master_dashboard as guild_master_dashboard_page
from guild_master import schedule_session as schedule_session_page
from participations import adventurer_profile as adventurer_profile_page
from participations import cancel_participation as cancel_participation_page
from participations import edit_participation as edit_participation_page
from participations import join_session as join_session_page
from quests import home as home_page
from quests import quest_detail as quest_detail_page


app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get(
    "SECRET_KEY",
    "replace-this-development-key-before-deployment",
)

login_manager.init_app(app)
initialize_database()


@app.route("/")
def home():
    return home_page()


@app.route("/login", methods=["GET", "POST"])
def login():
    return login_page()


@app.route("/register", methods=["GET", "POST"])
def register():
    return register_page()


@app.route("/logout")
@login_required
def logout():
    return logout_page()


@app.route("/session/<int:session_id>")
def quest_detail(session_id):
    return quest_detail_page(session_id)


@app.route("/session/<int:session_id>/join", methods=["GET", "POST"])
@require_role("Adventurer")
def join_session(session_id):
    return join_session_page(session_id)


@app.route("/my-participations")
@require_role("Adventurer")
def adventurer_profile():
    return adventurer_profile_page()


@app.route(
    "/participation/<int:participation_id>/edit",
    methods=["GET", "POST"],
)
@require_role("Adventurer")
def edit_participation(participation_id):
    return edit_participation_page(participation_id)


@app.route(
    "/participation/<int:participation_id>/cancel",
    methods=["POST"],
)
@require_role("Adventurer")
def cancel_participation(participation_id):
    return cancel_participation_page(participation_id)


@app.route("/guild-master")
@require_role("GuildMaster")
def guild_master_dashboard():
    return guild_master_dashboard_page()


@app.route("/guild-master/quests/create", methods=["GET", "POST"])
@require_role("GuildMaster")
def create_quest():
    return create_quest_page()


@app.route("/guild-master/sessions/create", methods=["GET", "POST"])
@require_role("GuildMaster")
def schedule_session():
    return schedule_session_page()


@app.route(
    "/guild-master/sessions/<int:session_id>/edit",
    methods=["GET", "POST"],
)
@require_role("GuildMaster")
def edit_session(session_id):
    return edit_session_page(session_id)


@app.route(
    "/guild-master/sessions/<int:session_id>/cancel",
    methods=["POST"],
)
@require_role("GuildMaster")
def cancel_session(session_id):
    return cancel_session_page(session_id)


@app.route("/admin")
@require_role("Admin")
def admin_dashboard():
    return admin_dashboard_page()


if __name__ == "__main__":
    app.run(debug=os.environ.get("FLASK_DEBUG") == "1")

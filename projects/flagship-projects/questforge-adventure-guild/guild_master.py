import sqlite3

from flask import flash, redirect, render_template, request, url_for

from database import get_db_connection
from helpers import (
    DAY_ORDER,
    DIFFICULTIES,
    LOCATIONS,
    QUEST_TYPES,
    get_day_order,
    get_remaining_places_for_role,
    get_role_capacity,
    get_total_reserved_places,
    is_valid_time,
    location_has_session_overlap,
)


PARTY_ROLES = ["Warrior", "Mage", "Healer"]


def get_all_quests():
    connection = get_db_connection()
    quests = connection.execute(
        "SELECT * FROM quests ORDER BY title"
    ).fetchall()
    connection.close()
    return quests


def get_session(session_id):
    connection = get_db_connection()
    session = connection.execute(
        """
        SELECT quest_sessions.*,
               quests.title,
               quests.duration_minutes,
               COUNT(participations.id) AS participation_count
        FROM quest_sessions
        JOIN quests ON quests.id = quest_sessions.quest_id
        LEFT JOIN participations
               ON participations.session_id = quest_sessions.id
        WHERE quest_sessions.id = ?
        GROUP BY quest_sessions.id, quests.id
        """,
        (session_id,),
    ).fetchone()
    connection.close()
    return session


def validate_session_form(form_values, quest_id, ignored_session_id=None):
    """Validate scheduling fields and return the selected quest when valid."""
    connection = get_db_connection()
    quest = connection.execute(
        "SELECT * FROM quests WHERE id = ?",
        (quest_id,),
    ).fetchone()
    connection.close()

    if quest is None:
        return None, "Please select a valid quest."

    if form_values["day_of_week"] not in DAY_ORDER:
        return None, "Please select a valid day of the week."

    if not is_valid_time(form_values["start_time"]):
        return None, "Please enter a valid time in HH:MM format."

    if form_values["location"] not in LOCATIONS:
        return None, "Please select a valid guild location."

    if location_has_session_overlap(
        form_values["day_of_week"],
        form_values["start_time"],
        int(quest["duration_minutes"]),
        form_values["location"],
        ignored_session_id,
    ):
        return None, "That location already has an overlapping quest session."

    return quest, None


def guild_master_dashboard():
    quests = get_all_quests()
    connection = get_db_connection()
    session_rows = connection.execute(
        """
        SELECT quest_sessions.*,
               quests.title,
               quests.quest_type,
               quests.difficulty,
               quests.duration_minutes,
               COUNT(participations.id) AS participation_count
        FROM quest_sessions
        JOIN quests ON quests.id = quest_sessions.quest_id
        LEFT JOIN participations
               ON participations.session_id = quest_sessions.id
        GROUP BY quest_sessions.id, quests.id
        """
    ).fetchall()
    connection.close()

    sessions = []

    for row in session_rows:
        session = dict(row)
        session["total_reserved_places"] = get_total_reserved_places(row["id"])
        session["role_availability"] = []

        for role in PARTY_ROLES:
            session["role_availability"].append(
                {
                    "name": role,
                    "capacity": get_role_capacity(role),
                    "remaining": get_remaining_places_for_role(row["id"], role),
                }
            )

        session["can_manage"] = int(row["participation_count"]) == 0
        sessions.append(session)

    sessions.sort(
        key=lambda session: (
            get_day_order(session["day_of_week"]),
            session["start_time"],
        )
    )

    return render_template(
        "guild_master_dashboard.html",
        quests=quests,
        sessions=sessions,
    )


def create_quest():
    form_values = {
        "title": "",
        "quest_type": "Combat",
        "difficulty": "Easy",
        "duration_minutes": "",
        "description": "",
        "image_filename": "",
    }

    if request.method == "POST":
        form_values = {
            "title": request.form.get("title", "").strip(),
            "quest_type": request.form.get("quest_type", "").strip(),
            "difficulty": request.form.get("difficulty", "").strip(),
            "duration_minutes": request.form.get("duration_minutes", "").strip(),
            "description": request.form.get("description", "").strip(),
            "image_filename": request.form.get("image_filename", "").strip(),
        }

        if form_values["title"] == "":
            flash("Quest title is required.", "danger")
            return redirect(url_for("create_quest"))

        if form_values["quest_type"] not in QUEST_TYPES:
            flash("Please select a valid quest type.", "danger")
            return redirect(url_for("create_quest"))

        if form_values["difficulty"] not in DIFFICULTIES:
            flash("Please select a valid difficulty.", "danger")
            return redirect(url_for("create_quest"))

        try:
            duration_minutes = int(form_values["duration_minutes"])
        except ValueError:
            duration_minutes = 0

        if duration_minutes <= 0:
            flash("Duration must be a positive number of minutes.", "danger")
            return redirect(url_for("create_quest"))

        if form_values["description"] == "":
            flash("Quest description is required.", "danger")
            return redirect(url_for("create_quest"))

        connection = get_db_connection()
        connection.execute(
            """
            INSERT INTO quests (
                title, quest_type, difficulty, duration_minutes,
                description, image_filename
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                form_values["title"],
                form_values["quest_type"],
                form_values["difficulty"],
                duration_minutes,
                form_values["description"],
                form_values["image_filename"] or None,
            ),
        )
        connection.commit()
        connection.close()

        flash("The quest was created.", "success")
        return redirect(url_for("guild_master_dashboard"))

    return render_template(
        "create_quest.html",
        form_values=form_values,
        quest_types=QUEST_TYPES,
        difficulties=DIFFICULTIES,
    )


def schedule_session():
    quests = get_all_quests()
    form_values = {
        "quest_id": "",
        "day_of_week": "Monday",
        "start_time": "09:00",
        "location": LOCATIONS[0],
    }

    if request.method == "POST":
        form_values = {
            "quest_id": request.form.get("quest_id", "").strip(),
            "day_of_week": request.form.get("day_of_week", "").strip(),
            "start_time": request.form.get("start_time", "").strip(),
            "location": request.form.get("location", "").strip(),
        }

        try:
            quest_id = int(form_values["quest_id"])
        except ValueError:
            quest_id = 0

        quest, validation_error = validate_session_form(form_values, quest_id)

        if validation_error is not None:
            flash(validation_error, "danger")
            return redirect(url_for("schedule_session"))

        connection = get_db_connection()
        connection.execute(
            """
            INSERT INTO quest_sessions (
                quest_id, day_of_week, start_time, location
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                quest["id"],
                form_values["day_of_week"],
                form_values["start_time"],
                form_values["location"],
            ),
        )
        connection.commit()
        connection.close()

        flash("The quest session was scheduled.", "success")
        return redirect(url_for("guild_master_dashboard"))

    return render_template(
        "schedule_session.html",
        form_values=form_values,
        quests=quests,
        days=list(DAY_ORDER.keys()),
        locations=LOCATIONS,
    )


def edit_session(session_id):
    session = get_session(session_id)

    if session is None:
        flash("Quest session not found.", "danger")
        return redirect(url_for("guild_master_dashboard"))

    if int(session["participation_count"]) > 0:
        flash("Sessions with participations cannot be edited.", "danger")
        return redirect(url_for("guild_master_dashboard"))

    form_values = {
        "day_of_week": session["day_of_week"],
        "start_time": session["start_time"],
        "location": session["location"],
    }

    if request.method == "POST":
        form_values = {
            "day_of_week": request.form.get("day_of_week", "").strip(),
            "start_time": request.form.get("start_time", "").strip(),
            "location": request.form.get("location", "").strip(),
        }
        quest, validation_error = validate_session_form(
            form_values,
            session["quest_id"],
            session_id,
        )

        if validation_error is not None:
            flash(validation_error, "danger")
            return redirect(
                url_for("edit_session", session_id=session_id)
            )

        connection = get_db_connection()
        connection.execute(
            """
            UPDATE quest_sessions
            SET day_of_week = ?, start_time = ?, location = ?
            WHERE id = ?
            """,
            (
                form_values["day_of_week"],
                form_values["start_time"],
                form_values["location"],
                session_id,
            ),
        )
        connection.commit()
        connection.close()

        flash("The quest session was updated.", "success")
        return redirect(url_for("guild_master_dashboard"))

    return render_template(
        "edit_session.html",
        session=session,
        form_values=form_values,
        days=list(DAY_ORDER.keys()),
        locations=LOCATIONS,
    )


def cancel_session(session_id):
    session = get_session(session_id)

    if session is None:
        flash("Quest session not found.", "danger")
        return redirect(url_for("guild_master_dashboard"))

    if int(session["participation_count"]) > 0:
        flash("Sessions with participations cannot be cancelled.", "danger")
        return redirect(url_for("guild_master_dashboard"))

    connection = get_db_connection()

    try:
        connection.execute("DELETE FROM quest_sessions WHERE id = ?", (session_id,))
        connection.commit()
    except sqlite3.IntegrityError:
        connection.rollback()
        connection.close()
        flash("Sessions with participations cannot be cancelled.", "danger")
        return redirect(url_for("guild_master_dashboard"))

    connection.close()

    flash("The quest session was cancelled.", "success")
    return redirect(url_for("guild_master_dashboard"))

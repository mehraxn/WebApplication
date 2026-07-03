import sqlite3

from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user

from database import get_db_connection
from helpers import (
    SIMULATED_CURRENT_DAY,
    SIMULATED_CURRENT_TIME,
    can_modify_participation,
    get_day_order,
    get_remaining_places_for_role,
    get_role_capacity,
    hours_until_session,
    time_to_minutes,
)


PARTY_ROLES = ["Warrior", "Mage", "Healer"]


def get_session(session_id):
    """Return a session together with its quest information."""
    connection = get_db_connection()
    session = connection.execute(
        """
        SELECT quest_sessions.id AS session_id,
               quest_sessions.day_of_week,
               quest_sessions.start_time,
               quest_sessions.location,
               quests.id AS quest_id,
               quests.title,
               quests.quest_type,
               quests.difficulty,
               quests.duration_minutes,
               quests.description
        FROM quest_sessions
        JOIN quests ON quests.id = quest_sessions.quest_id
        WHERE quest_sessions.id = ?
        """,
        (session_id,),
    ).fetchone()
    connection.close()
    return session


def get_owned_participation(participation_id, user_id):
    """Return a participation only when it belongs to the given Adventurer."""
    connection = get_db_connection()
    participation = connection.execute(
        """
        SELECT participations.*,
               quest_sessions.day_of_week,
               quest_sessions.start_time,
               quest_sessions.location,
               quests.title,
               quests.duration_minutes
        FROM participations
        JOIN quest_sessions ON quest_sessions.id = participations.session_id
        JOIN quests ON quests.id = quest_sessions.quest_id
        WHERE participations.id = ? AND participations.user_id = ?
        """,
        (participation_id, user_id),
    ).fetchone()
    connection.close()
    return participation


def build_role_availability(session_id, exclude_participation_id=None):
    """Build role-capacity data for the join and edit forms."""
    role_availability = []

    for role in PARTY_ROLES:
        role_availability.append(
            {
                "name": role,
                "capacity": get_role_capacity(role),
                "remaining": get_remaining_places_for_role(
                    session_id,
                    role,
                    exclude_participation_id,
                ),
            }
        )

    return role_availability


def render_participation_form(
    session,
    form_values,
    participation=None,
):
    excluded_id = participation["id"] if participation is not None else None

    return render_template(
        "join_session.html",
        session=dict(session),
        role_availability=build_role_availability(
            session["session_id"],
            excluded_id,
        ),
        form_values=form_values,
        participation=participation,
        is_editing=participation is not None,
    )


def parse_participation_form():
    """Read and validate the role and number of requested places."""
    role_category = request.form.get("role_category", "").strip()
    places_text = request.form.get("places_reserved", "").strip()

    try:
        places_reserved = int(places_text)
    except ValueError:
        places_reserved = 0

    form_values = {
        "role_category": role_category,
        "places_reserved": places_text,
    }

    if role_category not in PARTY_ROLES:
        return form_values, None, "Please choose Warrior, Mage, or Healer."

    if places_reserved not in (1, 2):
        return form_values, None, "You can reserve only one or two places."

    return form_values, places_reserved, None


def adventurer_has_overlapping_session(
    user_id,
    selected_session,
    ignored_participation_id=None,
):
    """Return True when an existing participation overlaps the selected session."""
    query = """
        SELECT participations.id,
               quest_sessions.day_of_week,
               quest_sessions.start_time,
               quests.duration_minutes
        FROM participations
        JOIN quest_sessions ON quest_sessions.id = participations.session_id
        JOIN quests ON quests.id = quest_sessions.quest_id
        WHERE participations.user_id = ?
    """
    parameters = [user_id]

    if ignored_participation_id is not None:
        query += " AND participations.id != ?"
        parameters.append(ignored_participation_id)

    connection = get_db_connection()
    existing_sessions = connection.execute(query, parameters).fetchall()
    connection.close()

    selected_start = time_to_minutes(selected_session["start_time"])

    if selected_start is None:
        return True

    selected_end = selected_start + int(selected_session["duration_minutes"])

    for existing in existing_sessions:
        if existing["day_of_week"] != selected_session["day_of_week"]:
            continue

        existing_start = time_to_minutes(existing["start_time"])

        if existing_start is None:
            continue

        existing_end = existing_start + int(existing["duration_minutes"])

        if selected_start < existing_end and existing_start < selected_end:
            return True

    return False


def join_session(session_id):
    session = get_session(session_id)

    if session is None:
        flash("Quest session not found.", "danger")
        return redirect(url_for("home"))

    form_values = {
        "role_category": "Warrior",
        "places_reserved": "1",
    }

    if request.method == "POST":
        form_values, places_reserved, validation_error = parse_participation_form()

        if validation_error is not None:
            flash(validation_error, "danger")
            return redirect(url_for("join_session", session_id=session_id))

        hours = hours_until_session(session["day_of_week"], session["start_time"])

        if hours is None or hours <= 0:
            flash("This quest session has already started.", "danger")
            return redirect(url_for("quest_detail", session_id=session_id))

        connection = get_db_connection()
        duplicate = connection.execute(
            """
            SELECT id
            FROM participations
            WHERE user_id = ? AND session_id = ?
            """,
            (current_user.id, session_id),
        ).fetchone()
        participation_count = connection.execute(
            "SELECT COUNT(*) AS count FROM participations WHERE user_id = ?",
            (current_user.id,),
        ).fetchone()["count"]
        connection.close()

        if duplicate is not None:
            flash("You have already joined this quest session.", "danger")
            return redirect(url_for("join_session", session_id=session_id))

        if participation_count >= 3:
            flash("You can join at most three quest sessions per week.", "danger")
            return redirect(url_for("join_session", session_id=session_id))

        if adventurer_has_overlapping_session(current_user.id, session):
            flash("This quest session overlaps one of your existing sessions.", "danger")
            return redirect(url_for("join_session", session_id=session_id))

        remaining_places = get_remaining_places_for_role(
            session_id,
            form_values["role_category"],
        )

        if places_reserved > remaining_places:
            flash("That role does not have enough remaining places.", "danger")
            return redirect(url_for("join_session", session_id=session_id))

        connection = get_db_connection()

        try:
            connection.execute(
                """
                INSERT INTO participations (
                    user_id, session_id, role_category,
                    places_reserved, created_at
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    current_user.id,
                    session_id,
                    form_values["role_category"],
                    places_reserved,
                    f"{SIMULATED_CURRENT_DAY} {SIMULATED_CURRENT_TIME}",
                ),
            )
            connection.commit()
        except sqlite3.IntegrityError:
            connection.rollback()
            connection.close()
            flash("The participation could not be saved. Please check availability.", "danger")
            return redirect(url_for("join_session", session_id=session_id))

        connection.close()
        flash("You joined the quest session.", "success")
        return redirect(url_for("adventurer_profile"))

    return render_participation_form(session, form_values)


def adventurer_profile():
    connection = get_db_connection()
    rows = connection.execute(
        """
        SELECT participations.*,
               quest_sessions.day_of_week,
               quest_sessions.start_time,
               quest_sessions.location,
               quests.title,
               quests.quest_type,
               quests.difficulty,
               quests.duration_minutes
        FROM participations
        JOIN quest_sessions ON quest_sessions.id = participations.session_id
        JOIN quests ON quests.id = quest_sessions.quest_id
        WHERE participations.user_id = ?
        """,
        (current_user.id,),
    ).fetchall()
    connection.close()

    participations = []

    for row in rows:
        participation = dict(row)
        participation["can_modify"] = can_modify_participation(
            row["day_of_week"],
            row["start_time"],
        )
        participation["hours_until"] = hours_until_session(
            row["day_of_week"],
            row["start_time"],
        )
        participations.append(participation)

    participations.sort(
        key=lambda participation: (
            get_day_order(participation["day_of_week"]),
            participation["start_time"],
        )
    )

    return render_template(
        "adventurer_profile.html",
        participations=participations,
    )


def cancel_participation(participation_id):
    participation = get_owned_participation(participation_id, current_user.id)

    if participation is None:
        flash("Participation not found or it does not belong to you.", "danger")
        return redirect(url_for("adventurer_profile"))

    if not can_modify_participation(
        participation["day_of_week"],
        participation["start_time"],
    ):
        flash(
            "This participation cannot be cancelled within eight hours of the session.",
            "danger",
        )
        return redirect(url_for("adventurer_profile"))

    connection = get_db_connection()
    connection.execute(
        "DELETE FROM participations WHERE id = ? AND user_id = ?",
        (participation_id, current_user.id),
    )
    connection.commit()
    connection.close()

    flash("Your participation was cancelled.", "success")
    return redirect(url_for("adventurer_profile"))


def edit_participation(participation_id):
    participation = get_owned_participation(participation_id, current_user.id)

    if participation is None:
        flash("Participation not found or it does not belong to you.", "danger")
        return redirect(url_for("adventurer_profile"))

    if not can_modify_participation(
        participation["day_of_week"],
        participation["start_time"],
    ):
        flash(
            "This participation cannot be modified within eight hours of the session.",
            "danger",
        )
        return redirect(url_for("adventurer_profile"))

    session = get_session(participation["session_id"])
    form_values = {
        "role_category": participation["role_category"],
        "places_reserved": str(participation["places_reserved"]),
    }

    if request.method == "POST":
        form_values, places_reserved, validation_error = parse_participation_form()

        if validation_error is not None:
            flash(validation_error, "danger")
            return redirect(
                url_for("edit_participation", participation_id=participation_id)
            )

        remaining_places = get_remaining_places_for_role(
            participation["session_id"],
            form_values["role_category"],
            participation_id,
        )

        if places_reserved > remaining_places:
            flash("That role does not have enough remaining places.", "danger")
            return redirect(
                url_for("edit_participation", participation_id=participation_id)
            )

        connection = get_db_connection()

        try:
            connection.execute(
                """
                UPDATE participations
                SET role_category = ?, places_reserved = ?
                WHERE id = ? AND user_id = ?
                """,
                (
                    form_values["role_category"],
                    places_reserved,
                    participation_id,
                    current_user.id,
                ),
            )
            connection.commit()
        except sqlite3.IntegrityError:
            connection.rollback()
            connection.close()
            flash("The participation could not be updated. Please check availability.", "danger")
            return redirect(
                url_for("edit_participation", participation_id=participation_id)
            )

        connection.close()
        flash("Your participation was updated.", "success")
        return redirect(url_for("adventurer_profile"))

    return render_participation_form(session, form_values, participation)

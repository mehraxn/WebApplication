from flask import flash, redirect, render_template, request, url_for

from database import get_db_connection
from helpers import (
    DAY_ORDER,
    DIFFICULTIES,
    QUEST_TYPES,
    get_day_order,
    get_remaining_places_for_role,
    get_reserved_places_for_role,
    get_role_capacity,
    get_simulated_time,
    get_total_reserved_places,
)


PARTY_ROLES = ["Warrior", "Mage", "Healer"]


def read_filters():
    """Read valid quest-board filters from the query string."""
    selected_filters = {
        "day": request.args.get("day", "").strip(),
        "quest_type": request.args.get("quest_type", "").strip(),
        "difficulty": request.args.get("difficulty", "").strip(),
        "available_role": request.args.get("available_role", "").strip(),
    }

    if selected_filters["day"] not in DAY_ORDER:
        selected_filters["day"] = ""

    if selected_filters["quest_type"] not in QUEST_TYPES:
        selected_filters["quest_type"] = ""

    if selected_filters["difficulty"] not in DIFFICULTIES:
        selected_filters["difficulty"] = ""

    if selected_filters["available_role"] not in PARTY_ROLES:
        selected_filters["available_role"] = ""

    return selected_filters


def get_quest_sessions(selected_filters):
    """Load quest sessions and apply the selected public filters."""
    query = """
        SELECT quest_sessions.id AS session_id,
               quest_sessions.day_of_week,
               quest_sessions.start_time,
               quest_sessions.location,
               quests.id AS quest_id,
               quests.title,
               quests.quest_type,
               quests.difficulty,
               quests.duration_minutes,
               quests.description,
               quests.image_filename,
               COALESCE(SUM(
                   CASE WHEN participations.role_category = 'Warrior'
                        THEN participations.places_reserved ELSE 0 END
               ), 0) AS warrior_reserved,
               COALESCE(SUM(
                   CASE WHEN participations.role_category = 'Mage'
                        THEN participations.places_reserved ELSE 0 END
               ), 0) AS mage_reserved,
               COALESCE(SUM(
                   CASE WHEN participations.role_category = 'Healer'
                        THEN participations.places_reserved ELSE 0 END
               ), 0) AS healer_reserved
        FROM quest_sessions
        JOIN quests ON quests.id = quest_sessions.quest_id
        LEFT JOIN participations
               ON participations.session_id = quest_sessions.id
        WHERE 1 = 1
    """
    parameters = []

    if selected_filters["day"]:
        query += " AND quest_sessions.day_of_week = ?"
        parameters.append(selected_filters["day"])

    if selected_filters["quest_type"]:
        query += " AND quests.quest_type = ?"
        parameters.append(selected_filters["quest_type"])

    if selected_filters["difficulty"]:
        query += " AND quests.difficulty = ?"
        parameters.append(selected_filters["difficulty"])

    query += " GROUP BY quest_sessions.id, quests.id"

    connection = get_db_connection()
    rows = connection.execute(query, parameters).fetchall()
    connection.close()

    sessions = []

    for row in rows:
        session = dict(row)
        reserved_by_role = {
            "Warrior": int(row["warrior_reserved"]),
            "Mage": int(row["mage_reserved"]),
            "Healer": int(row["healer_reserved"]),
        }
        session["role_availability"] = []

        for role in PARTY_ROLES:
            capacity = get_role_capacity(role)
            reserved = reserved_by_role[role]
            session["role_availability"].append(
                {
                    "name": role,
                    "capacity": capacity,
                    "reserved": reserved,
                    "remaining": max(capacity - reserved, 0),
                }
            )

        available_role = selected_filters["available_role"]

        if available_role:
            selected_role = next(
                role
                for role in session["role_availability"]
                if role["name"] == available_role
            )

            if selected_role["remaining"] == 0:
                continue

        sessions.append(session)

    sessions.sort(
        key=lambda session: (
            get_day_order(session["day_of_week"]),
            session["start_time"],
        )
    )
    return sessions


def home():
    selected_filters = read_filters()
    sessions = get_quest_sessions(selected_filters)

    return render_template(
        "home.html",
        sessions=sessions,
        selected_filters=selected_filters,
        days=list(DAY_ORDER.keys()),
        quest_types=QUEST_TYPES,
        difficulties=DIFFICULTIES,
        party_roles=PARTY_ROLES,
        simulated_time=get_simulated_time(),
    )


def quest_detail(session_id):
    connection = get_db_connection()
    session_row = connection.execute(
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
               quests.description,
               quests.image_filename
        FROM quest_sessions
        JOIN quests ON quests.id = quest_sessions.quest_id
        WHERE quest_sessions.id = ?
        """,
        (session_id,),
    ).fetchone()
    connection.close()

    if session_row is None:
        flash("Quest session not found.", "danger")
        return redirect(url_for("home"))

    session = dict(session_row)
    session["role_availability"] = []

    for role in PARTY_ROLES:
        session["role_availability"].append(
            {
                "name": role,
                "capacity": get_role_capacity(role),
                "reserved": get_reserved_places_for_role(session_id, role),
                "remaining": get_remaining_places_for_role(session_id, role),
            }
        )

    session["has_available_role"] = any(
        role["remaining"] > 0 for role in session["role_availability"]
    )
    session["total_reserved_places"] = get_total_reserved_places(session_id)

    return render_template("quest_detail.html", session=session)

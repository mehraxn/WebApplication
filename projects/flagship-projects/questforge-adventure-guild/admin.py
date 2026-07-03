from flask import render_template

from database import get_db_connection
from helpers import get_day_order


PARTY_ROLES = ["Warrior", "Mage", "Healer"]


def get_summary_statistics(connection):
    """Return the headline totals displayed by the Admin dashboard."""
    return {
        "adventurers": connection.execute(
            "SELECT COUNT(*) FROM users WHERE role = 'Adventurer'"
        ).fetchone()[0],
        "guild_masters": connection.execute(
            "SELECT COUNT(*) FROM users WHERE role = 'GuildMaster'"
        ).fetchone()[0],
        "quests": connection.execute(
            "SELECT COUNT(*) FROM quests"
        ).fetchone()[0],
        "sessions": connection.execute(
            "SELECT COUNT(*) FROM quest_sessions"
        ).fetchone()[0],
        "participations": connection.execute(
            "SELECT COUNT(*) FROM participations"
        ).fetchone()[0],
        "reserved_places": connection.execute(
            "SELECT COALESCE(SUM(places_reserved), 0) FROM participations"
        ).fetchone()[0],
    }


def get_users(connection):
    return connection.execute(
        """
        SELECT first_name, last_name, email, role
        FROM users
        ORDER BY role, last_name, first_name
        """
    ).fetchall()


def get_sessions(connection):
    rows = connection.execute(
        """
        SELECT quest_sessions.id,
               quest_sessions.day_of_week,
               quest_sessions.start_time,
               quest_sessions.location,
               quests.title,
               quests.quest_type,
               quests.difficulty,
               COALESCE(SUM(participations.places_reserved), 0)
                   AS total_reserved_places
        FROM quest_sessions
        JOIN quests ON quests.id = quest_sessions.quest_id
        LEFT JOIN participations
               ON participations.session_id = quest_sessions.id
        GROUP BY quest_sessions.id, quests.id
        """
    ).fetchall()

    sessions = [dict(row) for row in rows]
    sessions.sort(
        key=lambda session: (
            get_day_order(session["day_of_week"]),
            session["start_time"],
        )
    )
    return sessions


def get_role_statistics(connection):
    rows = connection.execute(
        """
        SELECT role_category,
               COALESCE(SUM(places_reserved), 0) AS reserved_places
        FROM participations
        GROUP BY role_category
        """
    ).fetchall()
    totals = {role: 0 for role in PARTY_ROLES}

    for row in rows:
        totals[row["role_category"]] = int(row["reserved_places"])

    return totals


def get_popularity_statistics(connection):
    popular_type = connection.execute(
        """
        SELECT quests.quest_type,
               SUM(participations.places_reserved) AS reserved_places
        FROM quests
        JOIN quest_sessions ON quest_sessions.quest_id = quests.id
        JOIN participations
             ON participations.session_id = quest_sessions.id
        GROUP BY quests.quest_type
        ORDER BY reserved_places DESC, quests.quest_type
        LIMIT 1
        """
    ).fetchone()

    popular_session = connection.execute(
        """
        SELECT quest_sessions.id,
               quests.title,
               quest_sessions.day_of_week,
               quest_sessions.start_time,
               SUM(participations.places_reserved) AS reserved_places
        FROM quest_sessions
        JOIN quests ON quests.id = quest_sessions.quest_id
        JOIN participations
             ON participations.session_id = quest_sessions.id
        GROUP BY quest_sessions.id, quests.id
        ORDER BY reserved_places DESC, quest_sessions.id
        LIMIT 1
        """
    ).fetchone()

    return {
        "quest_type": dict(popular_type) if popular_type is not None else None,
        "session": dict(popular_session) if popular_session is not None else None,
    }


def admin_dashboard():
    connection = get_db_connection()
    summary = get_summary_statistics(connection)
    users = get_users(connection)
    sessions = get_sessions(connection)
    role_statistics = get_role_statistics(connection)
    popularity = get_popularity_statistics(connection)
    connection.close()

    return render_template(
        "admin_dashboard.html",
        summary=summary,
        users=users,
        sessions=sessions,
        role_statistics=role_statistics,
        popularity=popularity,
    )

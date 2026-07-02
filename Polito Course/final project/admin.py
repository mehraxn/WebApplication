from flask import render_template
from flask_login import login_required

from auth import require_role
from database import get_db_connection




def get_basic_statistics(connection):
    guide_count = connection.execute(
        "SELECT COUNT(*) AS count FROM users WHERE role = 'Guide'").fetchone()["count"]

    participant_count = connection.execute(
        "SELECT COUNT(*) AS count FROM users WHERE role = 'Participant'"
    ).fetchone()["count"]

    tour_count = connection.execute(
        "SELECT COUNT(*) AS count FROM tours"
    ).fetchone()["count"]

    reservation_count = connection.execute(
        "SELECT COUNT(*) AS count FROM reservations"
    ).fetchone()["count"]

    return {
        "guide_count": guide_count,
        "participant_count": participant_count,
        "tour_count": tour_count,
        "reservation_count": reservation_count
    }


def get_reservations_by_language(connection):
    tours = connection.execute(
        "SELECT id, language FROM tours ORDER BY language"
    ).fetchall()

    reservations = connection.execute(
        "SELECT tour_id FROM reservations"
    ).fetchall()

    reservation_counts = {}
    for x in reservations:
        tour_id = x["tour_id"]

        if tour_id not in reservation_counts:
            reservation_counts[tour_id] = 0

        reservation_counts[tour_id] = reservation_counts[tour_id] + 1

    language_counts = {}
    for x in tours:
        language = x["language"]

        if language not in language_counts:
            language_counts[language] = 0

        tour_reservation_count = reservation_counts.get(x["id"], 0)
        language_counts[language] = (
            language_counts[language] + tour_reservation_count
        )

    result = []
    for language, count in language_counts.items():
        display_language = language
        if display_language is None or display_language == "":
            display_language = "Not specified"

        result.append({
            "language": display_language,
            "count": count
        })

    return result


def get_all_guides(connection):
    guides = connection.execute(
        """
        SELECT id, first_name, last_name, full_name, email, spoken_languages
        FROM users
        WHERE role = 'Guide'
        ORDER BY last_name, first_name
        """
    ).fetchall()

    guide_list = []

    for x in guides:
        tours = connection.execute(
            """
            SELECT id, title, language, duration_minutes, meeting_point
            FROM tours
            WHERE guide_id = ?
            ORDER BY title
            """,
            (x["id"],)
        ).fetchall()

        tour_list = []
        for y in tours:
            tour_list.append({
                "id": y["id"],
                "title": y["title"],
                "language": y["language"],
                "duration_minutes": y["duration_minutes"],
                "meeting_point": y["meeting_point"]
            })

        guide_list.append({
            "id": x["id"],
            "first_name": x["first_name"],
            "last_name": x["last_name"],
            "full_name": x["full_name"],
            "email": x["email"],
            "spoken_languages": x["spoken_languages"],
            "tours": tour_list
        })

    return guide_list


@login_required
def admin_dashboard():
    role_redirect = require_role("Admin")
    
    if role_redirect is not None:
        return role_redirect

    connection = get_db_connection()
    statistics = get_basic_statistics(connection)
    reservations_by_language = get_reservations_by_language(connection)
    guides = get_all_guides(connection)
    connection.close()

    return render_template(
        "admin_dashboard.html",
        statistics=statistics,
        reservations_by_language=reservations_by_language,guides=guides)

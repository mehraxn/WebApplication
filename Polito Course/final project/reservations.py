from datetime import datetime, timedelta

from flask import abort, flash, redirect, render_template, request, session, url_for
from flask_login import current_user, login_required

from auth import require_role
from database import get_db_connection
from models import get_current_user
from tours import build_reservation_calendar_options, get_available_slots_for_tour, get_tour_by_id


def reserve_tour(tour_id):
    tour = get_tour_by_id(tour_id)

    if tour is None:
        abort(404)

    available_slots = get_available_slots_for_tour(tour_id)
    reservation_calendars, reservation_month_options = build_reservation_calendar_options(tour_id)
    is_logged_in = session.get("user_id") is not None
    current_role = session.get("role")
    reservation_template_context = {
        "tour": tour,
        "available_slots": available_slots,
        "reservation_calendars": reservation_calendars,
        "reservation_month_options": reservation_month_options,
        "is_logged_in": is_logged_in,
        "current_role": current_role
    }

    if request.method == "POST":
        if not is_logged_in:
            flash("Please log in as a participant before reserving a tour.")
            return redirect(url_for("login"))

        if current_role == "Guide":
            flash("Guides cannot reserve tours as participants.")
            return redirect(url_for("tour_detail", tour_id=tour_id))

        if current_role != "Participant":
            flash("Please log in as a participant before reserving a tour.")
            return redirect(url_for("login"))

        participant_name = request.form.get("participant_name", "").strip()
        participant_email = request.form.get("participant_email", "").strip()
        selected_date = request.form.get("selected_date", "").strip()
        selected_time = request.form.get("selected_time", "").strip()
        extra_people = request.form.get("extra_people", "0").strip()
        phone_number = request.form.get("phone_number", "").strip()
        message_to_guide = request.form.get("message_to_guide", "").strip()
        extra_people_count = int(extra_people or 0)
        extra_people_names = [
            request.form.get(f"extra_person_{index}", "").strip()
            for index in range(1, extra_people_count + 1)
        ]

        if not participant_name or not participant_email or not selected_date or not selected_time:
            flash("Please fill in your name, email, date, and time before confirming the reservation.")
            return render_template("reservation.html", **reservation_template_context)

        if extra_people_count < 0 or extra_people_count > 3:
            flash("You can reserve for yourself and up to 3 extra people.")
            return render_template("reservation.html", **reservation_template_context)

        if extra_people_count and any(not name for name in extra_people_names):
            flash("Please enter the full name of each extra participant.")
            return render_template("reservation.html", **reservation_template_context)

        participant_id = session.get("user_id")

        connection = get_db_connection()

        available_slot = connection.execute(
            """
            SELECT id
            FROM tour_dates
            WHERE tour_id = ?
              AND tour_date = ?
              AND tour_time = ?
              AND date(tour_date) >= date('now')
            """,
            (tour_id, selected_date, selected_time)
        ).fetchone()

        if available_slot is None:
            connection.close()
            flash("This date and time are not available for this tour.")
            return render_template("reservation.html", **reservation_template_context)

        reserved_people = connection.execute(
            """
            SELECT COALESCE(SUM(1 + COALESCE(extra_people_count, extra_people, 0)), 0) AS total
            FROM reservations
            WHERE tour_id = ?
              AND selected_date = ?
              AND selected_time = ?
              AND status != 'Cancelled'
            """,
            (tour_id, selected_date, selected_time)
        ).fetchone()["total"]

        requested_people = 1 + extra_people_count
        if reserved_people + requested_people > int(tour["max_participants"]):
            connection.close()
            flash("This tour date does not have enough remaining places for your group.")
            return render_template("reservation.html", **reservation_template_context)

        cursor = connection.execute(
            """
            INSERT INTO reservations (
                tour_id, participant_id, selected_date, selected_time,
                main_participant_name, extra_people, extra_people_count,
                phone_number, message_to_guide, status
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                tour_id,
                participant_id,
                selected_date,
                selected_time,
                participant_name,
                extra_people_count,
                extra_people_count,
                phone_number,
                message_to_guide,
                "Pending"
            )
        )
        reservation_id = cursor.lastrowid

        for name in extra_people_names:
            connection.execute(
                """
                INSERT INTO reservation_extra_people (reservation_id, full_name)
                VALUES (?, ?)
                """,
                (reservation_id, name)
            )
        connection.commit()
        connection.close()

        flash("Your reservation was saved in the database.")
        return redirect(url_for("my_reservations"))

    return render_template("reservation.html", **reservation_template_context)


def get_reservations_for_participant(participant_id):
    connection = get_db_connection()
    reservations = connection.execute(
        """
        SELECT reservations.*, tours.title, tours.image, tours.meeting_point
        FROM reservations
        JOIN tours ON tours.id = reservations.tour_id
        WHERE reservations.participant_id = ?
        ORDER BY reservations.selected_date
        """,
        (participant_id,)
    ).fetchall()

    result = []

    for reservation in reservations:
        reservation_dict = dict(reservation)
        extra_people_count = reservation_dict.get("extra_people_count")
        if extra_people_count is None:
            extra_people_count = reservation_dict["extra_people"] or 0

        extra_names = connection.execute(
            """
            SELECT full_name
            FROM reservation_extra_people
            WHERE reservation_id = ?
            ORDER BY id
            """,
            (reservation_dict["id"],)
        ).fetchall()

        try:
            tour_start = datetime.strptime(
                f"{reservation_dict['selected_date']} {reservation_dict['selected_time']}",
                "%Y-%m-%d %H:%M"
            )
            can_cancel = reservation_dict["status"] != "Cancelled" and tour_start - datetime.now() >= timedelta(hours=24)
        except ValueError:
            can_cancel = False

        result.append({
            "id": reservation_dict["id"],
            "date": reservation_dict["selected_date"],
            "time": reservation_dict["selected_time"],
            "extra_people": extra_people_count,
            "extra_names": [item["full_name"] for item in extra_names],
            "can_cancel": can_cancel,
            "status": reservation_dict["status"],
            "tour": {
                "id": reservation_dict["tour_id"],
                "title": reservation_dict["title"],
                "image": reservation_dict["image"],
                "meeting_point": reservation_dict["meeting_point"]
            }
        })

    connection.close()
    return result


@login_required
def participant_dashboard():
    role_redirect = require_role("Participant")
    if role_redirect:
        return role_redirect

    logged_user = get_current_user()
    participant_id = int(current_user.id)

    reservations = get_reservations_for_participant(participant_id)
    upcoming_count = len(reservations)
    confirmed_count = sum(1 for reservation in reservations if reservation["status"] == "Confirmed")

    return render_template(
        "participant_dashboard.html",
        current_user=logged_user,
        reservations=reservations,
        upcoming_count=upcoming_count,
        confirmed_count=confirmed_count
    )


@login_required
def my_reservations():
    role_redirect = require_role("Participant")
    if role_redirect:
        return role_redirect

    logged_user = get_current_user()
    participant_id = int(current_user.id)

    reservations = get_reservations_for_participant(participant_id)

    return render_template(
        "my_reservations.html",
        current_user=logged_user,
        reservations=reservations
    )


@login_required
def cancel_reservation(reservation_id):
    role_redirect = require_role("Participant")
    if role_redirect:
        return role_redirect

    connection = get_db_connection()
    reservation = connection.execute(
        """
        SELECT *
        FROM reservations
        WHERE id = ? AND participant_id = ?
        """,
        (reservation_id, int(current_user.id))
    ).fetchone()

    if reservation is None:
        connection.close()
        abort(404)

    try:
        tour_start = datetime.strptime(
            f"{reservation['selected_date']} {reservation['selected_time']}",
            "%Y-%m-%d %H:%M"
        )
    except ValueError:
        connection.close()
        flash("This reservation has an invalid date and cannot be cancelled online.")
        return redirect(url_for("my_reservations"))

    if tour_start - datetime.now() < timedelta(hours=24):
        connection.close()
        flash("Reservations can only be cancelled at least 24 hours before the tour starts.")
        return redirect(url_for("my_reservations"))

    connection.execute(
        "UPDATE reservations SET status = 'Cancelled' WHERE id = ?",
        (reservation_id,)
    )
    connection.commit()
    connection.close()

    flash("Reservation cancelled.")
    return redirect(url_for("my_reservations"))

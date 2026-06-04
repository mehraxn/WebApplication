from datetime import datetime

from flask import flash, redirect, render_template, request, session, url_for
from flask_login import current_user, login_required

from auth import require_role
from database import get_db_connection
from models import get_current_user
from tours import build_reservation_calendar_options, get_available_slots_for_tour, get_tour_by_id


def get_time_minutes(time_text):
    try:
        time_object = datetime.strptime(time_text, "%H:%M")
    except ValueError:
        return None

    return time_object.hour * 60 + time_object.minute


def get_start_minute_number(date_text, time_text):
    try:
        date_object = datetime.strptime(date_text, "%Y-%m-%d").date()
    except ValueError:
        return None

    time_minutes = get_time_minutes(time_text)
    if time_minutes is None:
        return None

    return date_object.toordinal() * 24 * 60 + time_minutes


def read_duration_minutes(duration_text, saved_duration_minutes):
    if saved_duration_minutes:
        return int(saved_duration_minutes)

    digits = ""
    for character in duration_text:
        if character.isdigit():
            digits = digits + character

    if digits:
        return int(digits)

    return 90


def intervals_overlap(first_start, first_end, second_start, second_end):
    if first_start < second_end and second_start < first_end:
        return True

    return False


def participant_has_overlapping_reservation(connection, participant_id, selected_date, selected_time, duration_minutes):
    new_start = get_start_minute_number(selected_date, selected_time)

    if new_start is None:
        return True

    new_end = new_start + duration_minutes

    existing_reservations = connection.execute(
        """
        SELECT reservations.selected_date, reservations.selected_time,
               tours.duration, tours.duration_minutes, tours.title
        FROM reservations
        JOIN tours ON tours.id = reservations.tour_id
        WHERE reservations.participant_id = ?
          AND reservations.status != 'Cancelled'
        """,
        (participant_id,)
    ).fetchall()

    for reservation in existing_reservations:
        existing_start = get_start_minute_number(
            reservation["selected_date"],
            reservation["selected_time"]
        )

        if existing_start is None:
            continue

        existing_duration = read_duration_minutes(
            reservation["duration"],
            reservation["duration_minutes"]
        )
        existing_end = existing_start + existing_duration

        if intervals_overlap(new_start, new_end, existing_start, existing_end):
            return True

    return False


def reserve_tour(tour_id):
    tour = get_tour_by_id(tour_id)

    if tour is None:
        flash("Tour not found.")
        return redirect(url_for("home"))

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

        try:
            extra_people_count = int(extra_people or 0)
        except ValueError:
            extra_people_count = 0

        extra_people_names = []
        for index in range(1, extra_people_count + 1):
            field_name = f"extra_person_{index}"
            extra_person_name = request.form.get(field_name, "").strip()
            extra_people_names.append(extra_person_name)

        if not participant_name or not participant_email or not selected_date or not selected_time:
            flash("Please fill in your name, email, date, and time before confirming the reservation.")
            return render_template("reservation.html", **reservation_template_context)

        if extra_people_count < 0 or extra_people_count > 3:
            flash("You can reserve for yourself and up to 3 extra people.")
            return render_template("reservation.html", **reservation_template_context)

        missing_extra_person = False
        for name in extra_people_names:
            if not name:
                missing_extra_person = True

        if extra_people_count and missing_extra_person:
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

        tour_duration_minutes = read_duration_minutes(
            tour["duration"],
            tour.get("duration_minutes")
        )

        has_overlap = participant_has_overlapping_reservation(
            connection,
            participant_id,
            selected_date,
            selected_time,
            tour_duration_minutes
        )

        if has_overlap:
            connection.close()
            flash("You already have another reservation that overlaps with this tour time.")
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
        ORDER BY reservations.selected_date, reservations.selected_time
        """,
        (participant_id,)
    ).fetchall()

    result = []

    for reservation in reservations:
        reservation_dict = dict(reservation)

        extra_people_count = reservation_dict.get("extra_people_count")
        if extra_people_count is None:
            extra_people_count = reservation_dict["extra_people"] or 0

        extra_names_rows = connection.execute(
            """
            SELECT full_name
            FROM reservation_extra_people
            WHERE reservation_id = ?
            ORDER BY id
            """,
            (reservation_dict["id"],)
        ).fetchall()

        extra_names = []
        for item in extra_names_rows:
            extra_names.append(item["full_name"])

        is_past = False
        try:
            tour_start_text = f"{reservation_dict['selected_date']} {reservation_dict['selected_time']}"
            tour_start = datetime.strptime(tour_start_text, "%Y-%m-%d %H:%M")
            time_difference = tour_start - datetime.now()
            seconds_left = time_difference.total_seconds()

            if seconds_left < 0:
                is_past = True

            if reservation_dict["status"] != "Cancelled" and seconds_left >= 24 * 60 * 60:
                can_cancel = True
            else:
                can_cancel = False
        except ValueError:
            can_cancel = False

        result.append({
            "id": reservation_dict["id"],
            "date": reservation_dict["selected_date"],
            "time": reservation_dict["selected_time"],
            "extra_people": extra_people_count,
            "extra_names": extra_names,
            "can_cancel": can_cancel,
            "is_past": is_past,
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

    upcoming_count = 0
    past_count = 0
    confirmed_count = 0

    for reservation in reservations:
        if reservation["is_past"]:
            past_count = past_count + 1
        else:
            upcoming_count = upcoming_count + 1

        if reservation["status"] == "Confirmed":
            confirmed_count = confirmed_count + 1

    return render_template(
        "participant_dashboard.html",
        current_user=logged_user,
        reservations=reservations,
        upcoming_count=upcoming_count,
        past_count=past_count,
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
        flash("Reservation not found.")
        return redirect(url_for("my_reservations"))

    try:
        tour_start_text = f"{reservation['selected_date']} {reservation['selected_time']}"
        tour_start = datetime.strptime(tour_start_text, "%Y-%m-%d %H:%M")
    except ValueError:
        connection.close()
        flash("This reservation has an invalid date and cannot be cancelled online.")
        return redirect(url_for("my_reservations"))

    time_difference = tour_start - datetime.now()
    seconds_left = time_difference.total_seconds()

    if seconds_left < 24 * 60 * 60:
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

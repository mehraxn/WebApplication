from datetime import date, datetime

from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from auth import require_role
from database import get_db_connection
from models import get_current_user
from tours import build_reservation_calendar_options, get_available_slots_for_tour, get_tour_by_id, read_duration_minutes
from reservation_overlapping_helpers import (
    get_start_minute_number,
    participant_has_overlapping_reservation,
    participant_has_overlapping_guided_tour
)


def reserve_tour(tour_id):
    # Load the selected tour with all data needed by the reservation page.
    tour = get_tour_by_id(tour_id)

    if tour is None:
        flash("Tour not found.")
        return redirect(url_for("home"))

    # Load future available slots for this tour.
    available_slots = get_available_slots_for_tour(tour_id)

    # Build the calendar data and month options used by the reservation page.
    reservation_calendars, reservation_month_options = build_reservation_calendar_options(tour_id)

    is_logged_in = current_user.is_authenticated

    if is_logged_in:
        current_role = current_user.role
    else:
        current_role = None

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

        selected_slot = request.form.get("selected_slot", "").strip()

        phone_number = request.form.get("phone_number", "").strip()

        message_to_guide = request.form.get("message_to_guide", "").strip()

        parts = selected_slot.split("|")

        selected_date = ""
        selected_time = ""

        if len(parts) == 2:
            selected_date = parts[0].strip()
            selected_time = parts[1].strip()

        extra_people_names = []
        for x in range(1, 4):
            name = request.form.get("extra_person_" + str(x), "").strip()
            if name:
                extra_people_names.append(name)

        extra_people_count = len(extra_people_names)

        if not participant_name or not participant_email or not selected_date or not selected_time:
            flash("Please fill in your name, email, date, and time before confirming the reservation.")
            return render_template(
                "reservation.html",
                tour=tour,
                available_slots=available_slots,
                reservation_calendars=reservation_calendars,
                reservation_month_options=reservation_month_options,
                is_logged_in=is_logged_in,
                current_role=current_role
            )

        participant_id = int(current_user.id)

        connection = get_db_connection()

        # Check that the selected date and time exist for this tour.
        available_slot = connection.execute(
            """
            SELECT id, tour_date
            FROM tour_dates
            WHERE tour_id = ?
              AND tour_date = ?
              AND tour_time = ?
            """,
            (tour_id, selected_date, selected_time)
        ).fetchone()

        slot_is_in_future = False

        if available_slot is not None:
            slot_date_text = available_slot["tour_date"]

            try:
                date.fromisoformat(slot_date_text)
            except ValueError:
                slot_is_in_future = False
            else:
                today_string = date.today().strftime("%Y-%m-%d")
                slot_is_in_future = slot_date_text > today_string

        if not slot_is_in_future:
            connection.close()
            flash("This date and time are not available for this tour.")
            return render_template(
                "reservation.html",
                tour=tour,
                available_slots=available_slots,
                reservation_calendars=reservation_calendars,
                reservation_month_options=reservation_month_options,
                is_logged_in=is_logged_in,
                current_role=current_role
            )

        tour_duration_minutes = read_duration_minutes(tour.get("duration_minutes"))

        has_overlap = participant_has_overlapping_reservation( connection, participant_id, selected_date, selected_time,tour_duration_minutes)

        if has_overlap:
            connection.close()
            flash("You already have another reservation that overlaps with this tour time.")
            return render_template(
                "reservation.html",
                tour=tour,
                available_slots=available_slots,
                reservation_calendars=reservation_calendars,
                reservation_month_options=reservation_month_options,
                is_logged_in=is_logged_in,
                current_role=current_role
            )

        # If this participant also has a Guide account with the same email,
        # they cannot reserve their own tour or another tour that overlaps
        # with a tour they guide.
        guide_blocked, guide_message = participant_has_overlapping_guided_tour(
            connection,
            current_user.email,
            tour_id,
            selected_date,
            selected_time,
            tour_duration_minutes
        )

        if guide_blocked:
            connection.close()
            flash(guide_message)
            return render_template(
                "reservation.html",
                tour=tour,
                available_slots=available_slots,
                reservation_calendars=reservation_calendars,
                reservation_month_options=reservation_month_options,
                is_logged_in=is_logged_in,
                current_role=current_role
            )

        # Count confirmed participants already reserved for this tour slot.
        reservation_rows = connection.execute(
            """
            SELECT extra_people_count
            FROM reservations
            WHERE tour_id = ?
              AND selected_date = ?
              AND selected_time = ?
              AND status != 'Cancelled'
            """,(tour_id, selected_date, selected_time)).fetchall()

        reserved_people = 0

        for x in reservation_rows:
            reservation_extra_people_count = x["extra_people_count"]

            if reservation_extra_people_count is None:
                reservation_extra_people_count = 0

            reserved_people = reserved_people + 1 + int(reservation_extra_people_count)

        requested_people = 1 + extra_people_count
        if reserved_people + requested_people > int(tour["max_participants"]):
            connection.close()
            flash("This tour date does not have enough remaining places for your group.")
            return render_template(
                "reservation.html",
                tour=tour,
                available_slots=available_slots,
                reservation_calendars=reservation_calendars,
                reservation_month_options=reservation_month_options,
                is_logged_in=is_logged_in,
                current_role=current_role)

        cursor = connection.execute("""
            INSERT INTO reservations (
                tour_id, participant_id, selected_date, selected_time,
                main_participant_name, extra_people_count,
                phone_number, message_to_guide, status
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                tour_id,
                participant_id,
                selected_date,
                selected_time,
                participant_name,
                extra_people_count,
                phone_number,
                message_to_guide,
                "Confirmed"
            )
        )
        reservation_id = cursor.lastrowid

        for x in extra_people_names:
            connection.execute(
                """
                INSERT INTO reservation_extra_people (reservation_id, full_name)
                VALUES (?, ?)
                """,
                (reservation_id, x)
            )

        connection.commit()
        connection.close()

        flash("Your reservation was saved in the database.")
        return redirect(url_for("my_reservations"))

    return render_template(
        "reservation.html",
        tour=tour,
        available_slots=available_slots,
        reservation_calendars=reservation_calendars,
        reservation_month_options=reservation_month_options,
        is_logged_in=is_logged_in,
        current_role=current_role
    )


def get_reservations_for_participant(participant_id):
    connection = get_db_connection()

    reservations = connection.execute(
        """
        SELECT *
        FROM reservations
        WHERE participant_id = ?
        ORDER BY selected_date, selected_time
        """,
        (participant_id,)).fetchall()

    result = []

    for x in reservations:
        reservation_dict = dict(x)

        # Load the related tour separately instead of using a JOIN.
        tour = connection.execute(
            """
            SELECT title, image, meeting_point
            FROM tours
            WHERE id = ?
            """,
            (reservation_dict["tour_id"],)
        ).fetchone()

        if tour is not None:
            reservation_dict["title"] = tour["title"]
            reservation_dict["image"] = tour["image"]
            reservation_dict["meeting_point"] = tour["meeting_point"]
        else:
            reservation_dict["title"] = "Unknown tour"
            reservation_dict["image"] = ""
            reservation_dict["meeting_point"] = ""

        extra_people_count = reservation_dict.get("extra_people_count")

        if extra_people_count is None:
            extra_people_count = 0

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

        for y in extra_names_rows:
            extra_names.append(y["full_name"])

        is_past = False
        can_cancel = False

        date_text = reservation_dict["selected_date"]
        time_text = reservation_dict["selected_time"]

        tour_start_minutes = get_start_minute_number(date_text, time_text)

        if tour_start_minutes is not None:
            now = datetime.now()
            current_time_minutes = now.hour * 60 + now.minute
            current_start_minutes = date.today().toordinal() * 24 * 60 + current_time_minutes
            minutes_left = tour_start_minutes - current_start_minutes

            if minutes_left < 0:
                is_past = True

            if reservation_dict["status"] != "Cancelled":
                if minutes_left >= 24 * 60:
                    can_cancel = True

        reservation_data = {
            "id": reservation_dict["id"],
            "date": reservation_dict["selected_date"],
            "time": reservation_dict["selected_time"],
            "extra_people_count": extra_people_count,
            "extra_names": extra_names,
            "can_cancel": can_cancel,
            "is_past": is_past,
            "status": reservation_dict["status"],
            "tour": {
                "id": reservation_dict["tour_id"],
                "title": reservation_dict["title"],
                "image": reservation_dict["image"],
                "meeting_point": reservation_dict["meeting_point"]  }
        }

        result.append(reservation_data)

    connection.close()

    return result



@login_required
def participant_dashboard():
    role_redirect = require_role("Participant")
    if role_redirect:
        return role_redirect

    logged_user = get_current_user()
    participant_id = int(logged_user["id"])

    reservations = get_reservations_for_participant(participant_id)

    upcoming_count = 0
    past_count = 0
    confirmed_count = 0


    for x in reservations:
        if x["is_past"]:
            past_count = past_count + 1
        else:
            upcoming_count = upcoming_count + 1

        if x["status"] == "Confirmed":
            confirmed_count = confirmed_count + 1

    return render_template(
        "participant_dashboard.html",
        current_user=logged_user,
        reservations=reservations,
        upcoming_count=upcoming_count,
        past_count=past_count,
        confirmed_count=confirmed_count)


@login_required
def my_reservations():
    role_redirect = require_role("Participant")
    if role_redirect:
        return role_redirect

    logged_user = get_current_user()
    participant_id = int(current_user.id)
    reservations = get_reservations_for_participant(participant_id)

    return render_template(
        "my_reservations.html",current_user=logged_user,reservations=reservations)


@login_required
def cancel_reservation(reservation_id):
    role_redirect = require_role("Participant")
    if role_redirect:
        return role_redirect

    connection = get_db_connection()
    reservation = connection.execute(
        """
        SELECT *FROM reservations WHERE id = ? AND participant_id = ?
        """,(reservation_id, int(current_user.id))).fetchone()

    if reservation is None:
        connection.close()
        flash("Reservation not found.")
        return redirect(url_for("my_reservations"))

    if reservation["status"] == "Cancelled":
        connection.close()
        flash("This reservation is already cancelled.")
        return redirect(url_for("my_reservations"))

    tour_start_minutes = get_start_minute_number(reservation["selected_date"],reservation["selected_time"])

    if tour_start_minutes is None:
        connection.close()
        flash("This reservation has an invalid date and cannot be cancelled online.")
        return redirect(url_for("my_reservations"))

    now = datetime.now()
    current_time_minutes = now.hour * 60 + now.minute
    current_start_minutes = date.today().toordinal() * 24 * 60 + current_time_minutes
    minutes_left = tour_start_minutes - current_start_minutes

    if minutes_left < 24 * 60:
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

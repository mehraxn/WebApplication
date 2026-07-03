from datetime import date

from tours import get_time_minutes, read_duration_minutes


# Convert a date and time into a single comparable minute number.
def get_start_minute_number(date_text, time_text):
    try:
        date_object = date.fromisoformat(date_text)
    except ValueError:
        return None

    time_minutes = get_time_minutes(time_text)
    if time_minutes is None:
        return None

    # toordinal() maps the date to a fixed day number, giving an absolute minute value.
    return date_object.toordinal() * 24 * 60 + time_minutes


# Shared half-open interval overlap check.
def intervals_overlap(first_start, first_end, second_start, second_end):
    return first_start < second_end and second_start < first_end


# Block reservations that overlap in time with another reservation by the same participant.
def participant_has_overlapping_reservation(connection, participant_id, selected_date, selected_time, duration_minutes):

    tour_start = get_start_minute_number(selected_date, selected_time)

    if tour_start is None:
        return True

    tour_end = tour_start + duration_minutes

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

    for x in existing_reservations:
        find_tour_start = get_start_minute_number(x["selected_date"],x["selected_time"])

        if find_tour_start is None:
            continue

        find_tour_duration = read_duration_minutes(x["duration_minutes"])

        find_tour_End = find_tour_start + find_tour_duration

        if intervals_overlap(tour_start, tour_end, find_tour_start, find_tour_End):
            return True

    return False


# If this participant also has a Guide account with the same email, block reserving a tour
# that overlaps with one they guide (including their own tours).
def participant_has_overlapping_guided_tour(connection, participant_email, selected_tour_id, selected_date, selected_time, selected_duration_minutes):

    # Look for a Guide account that uses the same email.
    guide = connection.execute(
        """
        SELECT id
        FROM users
        WHERE email = ?
          AND role = 'Guide'
        """,
        (participant_email,)
    ).fetchone()

    # No guide account with this email, so there is nothing to block.
    if guide is None:
        return False, ""

    guide_id = guide["id"]

    # Block reserving a tour the participant guides themselves.
    selected_tour = connection.execute(
        """
        SELECT guide_id
        FROM tours
        WHERE id = ?
        """,
        (selected_tour_id,)
    ).fetchone()

    if selected_tour is not None and selected_tour["guide_id"] == guide_id:
        return True, "You cannot reserve a tour that you guide."

    selected_start = get_time_minutes(selected_time)

    if selected_start is None:
        return False, ""

    selected_end = selected_start + selected_duration_minutes

    # Check every tour this person guides for a time clash on the selected date.
    guided_tours = connection.execute(
        """
        SELECT id, duration_minutes
        FROM tours
        WHERE guide_id = ?
        """,
        (guide_id,)
    ).fetchall()

    for guided_tour in guided_tours:
        guided_duration = read_duration_minutes(guided_tour["duration_minutes"])

        # Find the times this guided tour runs on the selected date.
        guided_dates = connection.execute(
            """
            SELECT tour_time
            FROM tour_dates
            WHERE tour_id = ?
              AND tour_date = ?
            """,
            (guided_tour["id"], selected_date)
        ).fetchall()

        for guided_date in guided_dates:
            guided_start = get_time_minutes(guided_date["tour_time"])

            if guided_start is None:
                continue

            guided_end = guided_start + guided_duration

            if intervals_overlap(selected_start, selected_end, guided_start, guided_end):
                return True, "You already guide another tour at this time."

    return False, ""

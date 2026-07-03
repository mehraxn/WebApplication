from datetime import date

from flask import request

from tours import get_time_minutes


WEEKDAYS = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday"
]


def get_weekly_start_minute(weekday, start_time):
    if weekday not in WEEKDAYS:
        return None

    time_minutes = get_time_minutes(start_time)

    if time_minutes is None:
        return None

    weekday_index = WEEKDAYS.index(weekday)

    return weekday_index * 24 * 60 + time_minutes


def weekly_intervals_overlap(first_start, first_end, second_start, second_end):
    week_minutes = 7 * 24 * 60

    for x in [-week_minutes, 0, week_minutes]:
        shifted_start = second_start + x
        shifted_end = second_end + x

        if first_start < shifted_end and shifted_start < first_end:
            return True

    return False


def schedules_overlap_with_each_other(schedules, duration_minutes):
    for i in range(len(schedules)):
        first = schedules[i]

        first_start = get_weekly_start_minute(
            first["weekday"],
            first["start_time"]
        )

        if first_start is None:
            return True

        first_end = first_start + duration_minutes

        for j in range(len(schedules)):
            if i == j:
                continue

            second = schedules[j]

            second_start = get_weekly_start_minute(
                second["weekday"],
                second["start_time"]
            )

            if second_start is None:
                return True

            second_end = second_start + duration_minutes

            if weekly_intervals_overlap(
                first_start,
                first_end,
                second_start,
                second_end
            ):
                return True

    return False


def guide_has_schedule_overlap(
    connection,
    guide_id,
    schedules,
    duration_minutes,
    tour_id_to_ignore=None
):
    if tour_id_to_ignore is None:
        other_tours_schedules = connection.execute(
            """
            SELECT tours.id, tours.title, tours.duration, tours.duration_minutes,
                   tour_schedules.weekday, tour_schedules.start_time
            FROM tours
            JOIN tour_schedules ON tour_schedules.tour_id = tours.id
            WHERE tours.guide_id = ?
            """,
            (guide_id,)
        ).fetchall()
    else:
        other_tours_schedules = connection.execute(
            """
            SELECT tours.id, tours.title, tours.duration, tours.duration_minutes,
                   tour_schedules.weekday, tour_schedules.start_time
            FROM tours
            JOIN tour_schedules ON tour_schedules.tour_id = tours.id
            WHERE tours.guide_id = ?
              AND tours.id != ?
            """,
            (guide_id, tour_id_to_ignore)
        ).fetchall()

    for x in schedules:
        new_start = get_weekly_start_minute(x["weekday"], x["start_time"])

        if new_start is None:
            return True

        new_end = new_start + duration_minutes

        for y in other_tours_schedules:
            old_start = get_weekly_start_minute(
                y["weekday"],
                y["start_time"]
            )

            if old_start is None:
                continue

            if y["duration_minutes"]:
                old_duration = int(y["duration_minutes"])
            else:
                old_duration = 90

            old_end = old_start + old_duration

            if weekly_intervals_overlap(
                new_start,
                new_end,
                old_start,
                old_end
            ):
                return True

    return False


def read_schedule_rows_from_form():
    weekday_list = request.form.getlist("schedule_weekday")
    time_list = request.form.getlist("schedule_start_time")

    schedules = []
    used_weekdays = []

    for index in range(len(weekday_list)):
        weekday = weekday_list[index].strip()

        start_time = ""

        if index < len(time_list):
            start_time = time_list[index].strip()

        if weekday == "" and start_time == "":
            continue

        if weekday not in WEEKDAYS:
            return [], "Please choose valid weekly schedule days."

        if get_time_minutes(start_time) is None:
            return [], "Please enter all start times in HH:MM format."

        weekday_was_already_used = weekday in used_weekdays

        if weekday_was_already_used:
            return (
                [],
                "The same tour can have only one start time per weekday."
            )

        used_weekdays.append(weekday)

        schedules.append({
            "weekday": weekday,
            "start_time": start_time
        })

    if len(schedules) == 0:
        return [], "Please add at least one weekly schedule day."

    return schedules, ""


def create_dates_for_schedule(connection, tour_id, weekday, start_time):
    today = date.today()

    weekday_number = None

    if weekday in WEEKDAYS:
        weekday_number = WEEKDAYS.index(weekday)

    tour = connection.execute(
        """
        SELECT guide_id, duration_minutes
        FROM tours
        WHERE id = ?
        """,
        (tour_id,)
    ).fetchone()

    participant_user = None
    new_duration = 90

    if tour is not None:
        if tour["duration_minutes"]:
            new_duration = int(tour["duration_minutes"])

        guide = connection.execute(
            """
            SELECT email
            FROM users
            WHERE id = ?
            """,
            (tour["guide_id"],)
        ).fetchone()

        if guide is not None:
            participant_user = connection.execute(
                """
                SELECT id
                FROM users
                WHERE email = ? AND role = 'Participant'
                """,
                (guide["email"],)
            ).fetchone()

    for i in range(0, 366):
        year = today.year
        month = today.month
        day = today.day + i

        while True:
            if month in [1, 3, 5, 7, 8, 10, 12]:
                days_in_month = 31
            elif month in [4, 6, 9, 11]:
                days_in_month = 30
            else:
                leap_year = False

                if year % 4 == 0:
                    if year % 100 != 0 or year % 400 == 0:
                        leap_year = True

                if leap_year:
                    days_in_month = 29
                else:
                    days_in_month = 28

            if day <= days_in_month:
                break

            day = day - days_in_month
            month = month + 1

            if month > 12:
                month = 1
                year = year + 1

        future_date = date(year, month, day)

        if weekday_number is not None and future_date.weekday() == weekday_number:
            existing = connection.execute(
                """
                SELECT id
                FROM tour_dates
                WHERE tour_id = ? AND tour_date = ?
                """,
                (tour_id, future_date.isoformat())
            ).fetchone()

            if existing is None:
                guide_busy_as_participant = False

                if participant_user is not None:
                    new_start = get_time_minutes(start_time)

                    if new_start is not None:
                        new_end = new_start + new_duration

                        participant_reservations = connection.execute(
                            """
                            SELECT reservations.selected_time,
                                   tours.duration_minutes
                            FROM reservations
                            JOIN tours ON tours.id = reservations.tour_id
                            WHERE reservations.participant_id = ?
                              AND reservations.selected_date = ?
                              AND reservations.status != 'Cancelled'
                            """,
                            (participant_user["id"], future_date.isoformat())
                        ).fetchall()

                        for reservation in participant_reservations:
                            old_start = get_time_minutes(
                                reservation["selected_time"]
                            )

                            if old_start is None:
                                continue

                            if reservation["duration_minutes"]:
                                old_duration = int(
                                    reservation["duration_minutes"]
                                )
                            else:
                                old_duration = 90

                            old_end = old_start + old_duration

                            if new_start < old_end and old_start < new_end:
                                guide_busy_as_participant = True
                                break

                if not guide_busy_as_participant:
                    connection.execute(
                        """
                        INSERT INTO tour_dates (tour_id, tour_date, tour_time)
                        VALUES (?, ?, ?)
                        """,
                        (tour_id, future_date.isoformat(), start_time)
                    )


def create_dates_for_schedules(connection, tour_id, schedules):
    for x in schedules:
        create_dates_for_schedule(
            connection,
            tour_id,
            x["weekday"],
            x["start_time"]
        )

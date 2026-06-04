from datetime import date, datetime

from flask import flash, redirect, render_template, request, session, url_for

from database import get_db_connection


MONTH_NAMES = [
    "",
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December"
]

WEEKDAYS = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday"
]


def is_leap_year(year):
    if year % 4 != 0:
        return False

    if year % 100 != 0:
        return True

    if year % 400 == 0:
        return True

    return False


def get_days_in_month(year, month):
    if month in [1, 3, 5, 7, 8, 10, 12]:
        return 31

    if month in [4, 6, 9, 11]:
        return 30

    if is_leap_year(year):
        return 29

    return 28


def add_days_to_date(start_date, days_to_add):
    year = start_date.year
    month = start_date.month
    day = start_date.day + days_to_add

    while True:
        days_in_month = get_days_in_month(year, month)

        if day <= days_in_month:
            break

        day = day - days_in_month
        month = month + 1

        if month > 12:
            month = 1
            year = year + 1

    return date(year, month, day)


def is_valid_time(time_text):
    try:
        datetime.strptime(time_text, "%H:%M")
        return True
    except ValueError:
        return False


def read_duration_minutes(duration_text, fallback_value=None):
    if fallback_value:
        return int(fallback_value)

    digits = ""
    for character in duration_text:
        if character.isdigit():
            digits = digits + character

    if digits:
        return int(digits)

    return 90


def calculate_rating(tour_id):
    connection = get_db_connection()
    result = connection.execute(
        "SELECT AVG(rating) AS average_rating FROM reviews WHERE tour_id = ?",
        (tour_id,)
    ).fetchone()
    connection.close()

    if result is not None:
        if result["average_rating"] is not None:
            average = float(result["average_rating"])
            return round(average, 1)

    return 4.8


def full_star_count(rating):
    stars = int(round(float(rating)))

    if stars < 0:
        return 0

    if stars > 5:
        return 5

    return stars


def get_all_tours(language=None, duration=None, selected_date=None):
    connection = get_db_connection()

    query = "SELECT DISTINCT tours.* FROM tours"
    parameters = []
    conditions = []

    if selected_date:
        query = query + " JOIN tour_dates ON tour_dates.tour_id = tours.id"
        conditions.append("tour_dates.tour_date = ?")
        parameters.append(selected_date)

    if language:
        conditions.append("(tours.language = ? OR tours.languages LIKE ?)")
        parameters.append(language)
        parameters.append(f"%{language}%")

    if duration:
        conditions.append("(tours.duration_minutes = ? OR tours.duration LIKE ?)")
        parameters.append(duration)
        parameters.append(f"%{duration}%")

    if conditions:
        query = query + " WHERE " + " AND ".join(conditions)

    query = query + " ORDER BY tours.id"

    tours = connection.execute(query, parameters).fetchall()
    connection.close()

    result = []
    for tour in tours:
        tour_dict = dict(tour)
        rating = calculate_rating(tour_dict["id"])
        tour_dict["rating"] = f"{rating:.1f}"
        tour_dict["full_stars"] = full_star_count(rating)
        result.append(tour_dict)

    return result


def get_existing_reservations_for_participant(tour_id):
    participant_id = session.get("user_id")
    role = session.get("role")

    if not participant_id or role != "Participant":
        return []

    connection = get_db_connection()
    reservations = connection.execute(
        """
        SELECT selected_date, selected_time, status
        FROM reservations
        WHERE tour_id = ?
          AND participant_id = ?
          AND status != 'Cancelled'
        ORDER BY selected_date, selected_time
        """,
        (tour_id, participant_id)
    ).fetchall()
    connection.close()

    result = []
    for reservation in reservations:
        result.append(dict(reservation))

    return result


def get_tour_by_id(tour_id):
    connection = get_db_connection()

    tour = connection.execute(
        """
        SELECT tours.*, users.full_name AS guide,
               users.id AS guide_user_id,
               users.profile_picture AS guide_profile_picture,
               users.spoken_languages AS guide_spoken_languages
        FROM tours
        JOIN users ON users.id = tours.guide_id
        WHERE tours.id = ?
        """,
        (tour_id,)
    ).fetchone()

    if tour is None:
        connection.close()
        return None

    tour_dict = dict(tour)

    stops = connection.execute(
        """
        SELECT *
        FROM tour_stops
        WHERE tour_id = ?
        ORDER BY stop_order
        """,
        (tour_id,)
    ).fetchall()

    dates = connection.execute(
        """
        SELECT *
        FROM tour_dates
        WHERE tour_id = ?
        ORDER BY tour_date, tour_time
        """,
        (tour_id,)
    ).fetchall()

    schedules = connection.execute(
        """
        SELECT *
        FROM tour_schedules
        WHERE tour_id = ?
        ORDER BY id
        """,
        (tour_id,)
    ).fetchall()

    reviews = connection.execute(
        """
        SELECT reviews.*, users.full_name
        FROM reviews
        JOIN users ON users.id = reviews.participant_id
        WHERE reviews.tour_id = ?
        ORDER BY reviews.id DESC
        """,
        (tour_id,)
    ).fetchall()

    photos = connection.execute(
        """
        SELECT photo_path
        FROM tour_photos
        WHERE tour_id = ?
        ORDER BY photo_order
        """,
        (tour_id,)
    ).fetchall()

    connection.close()

    rating = calculate_rating(tour_id)
    tour_dict["rating"] = f"{rating:.1f}"
    tour_dict["full_stars"] = full_star_count(rating)

    stop_names = []
    normal_stops = []
    finish_stops = []

    for stop in stops:
        stop_names.append(stop["stop_name"])

        if stop["stop_type"] == "Stop":
            normal_stops.append(stop["stop_name"])

        if stop["stop_type"] == "Finish":
            finish_stops.append(stop["stop_name"])

    tour_dict["stops"] = stop_names

    if tour_dict.get("path_type"):
        tour_dict["terrain"] = tour_dict.get("path_type")
    else:
        tour_dict["terrain"] = "Urban walking path"

    if normal_stops:
        tour_dict["rest_stops"] = normal_stops
    else:
        tour_dict["rest_stops"] = ["Short rest during the route"]

    if normal_stops or finish_stops:
        photo_stops = []
        for stop_name in normal_stops:
            photo_stops.append(stop_name)
        for stop_name in finish_stops:
            photo_stops.append(stop_name)
        tour_dict["photo_stops"] = photo_stops
    else:
        tour_dict["photo_stops"] = ["Main route viewpoint"]

    tour_dict["what_to_bring"] = ["Comfortable shoes", "Water", "Camera or phone", "Sun protection"]
    tour_dict["audience"] = "All people can participate. Check the fitness level before reserving."

    schedule = []
    available_dates = []
    used_schedule_labels = []
    today = date.today()

    if schedules:
        first_schedule = schedules[0]
        tour_dict["schedule_weekday"] = first_schedule["weekday"]
        tour_dict["schedule_start_time"] = first_schedule["start_time"]
    else:
        tour_dict["schedule_weekday"] = "Monday"
        tour_dict["schedule_start_time"] = "10:00"

    for schedule_row in schedules:
        schedule_label = f"Every {schedule_row['weekday']} at {schedule_row['start_time']}"
        if schedule_label not in used_schedule_labels:
            schedule.append(schedule_label)
            used_schedule_labels.append(schedule_label)

    for item in dates:
        date_text = item["tour_date"]
        time_text = item["tour_time"]

        try:
            slot_date = datetime.strptime(date_text, "%Y-%m-%d").date()
            weekday_name = WEEKDAYS[slot_date.weekday()]
        except ValueError:
            continue

        if slot_date >= today:
            available_dates.append({
                "date": date_text,
                "time": time_text,
                "label": f"{date_text} - {weekday_name} at {time_text}"
            })

    review_list = []
    for review in reviews:
        review_list.append(dict(review))

    photo_list = []
    for photo in photos:
        photo_list.append(photo["photo_path"])

    tour_dict["schedule"] = schedule
    tour_dict["available_dates"] = available_dates
    tour_dict["reviews"] = review_list
    tour_dict["photos"] = photo_list
    tour_dict["existing_reservations"] = get_existing_reservations_for_participant(tour_id)

    return tour_dict


def month_offset(base_date, offset):
    month = base_date.month + offset
    year = base_date.year + (month - 1) // 12
    month = (month - 1) % 12 + 1
    return year, month


def build_month_calendar(year, month, available_slots):
    first_day = date(year, month, 1)
    first_weekday = first_day.weekday()
    days_in_month = get_days_in_month(year, month)
    today = date.today()

    weeks = []
    week = []

    for number in range(first_weekday):
        week.append(None)

    for day_number in range(1, days_in_month + 1):
        current_date = date(year, month, day_number)
        current_date_text = current_date.isoformat()
        available_time = available_slots.get(current_date_text)

        is_available = False
        if available_time is not None:
            if current_date >= today:
                is_available = True

        day_data = {
            "day": day_number,
            "iso": current_date_text,
            "time": available_time,
            "available": is_available,
            "past": current_date < today,
            "today": current_date == today
        }
        week.append(day_data)

        if len(week) == 7:
            weeks.append(week)
            week = []

    if week:
        while len(week) < 7:
            week.append(None)
        weeks.append(week)

    calendar = {
        "month_name": MONTH_NAMES[month],
        "year": year,
        "weeks": weeks
    }
    return calendar


def get_available_slot_dictionary(tour_id):
    connection = get_db_connection()
    dates = connection.execute(
        """
        SELECT tour_date, tour_time
        FROM tour_dates
        WHERE tour_id = ?
        ORDER BY tour_date, tour_time
        """,
        (tour_id,)
    ).fetchall()
    connection.close()

    available_slots = {}
    for item in dates:
        available_slots[item["tour_date"]] = item["tour_time"]

    return available_slots, dates


def build_calendars(tour_id):
    available_slots, dates = get_available_slot_dictionary(tour_id)

    today = date.today()
    first_year, first_month = month_offset(today, 0)
    second_year, second_month = month_offset(today, 1)

    calendars = []
    calendars.append(build_month_calendar(first_year, first_month, available_slots))
    calendars.append(build_month_calendar(second_year, second_month, available_slots))

    return calendars


def build_reservation_calendar_options(tour_id):
    available_slots, dates = get_available_slot_dictionary(tour_id)

    today = date.today()
    last_allowed_year = today.year + 1
    last_allowed_month = 12
    last_allowed_key = f"{last_allowed_year}-{last_allowed_month:02d}"

    available_month_keys = []
    used_month_keys = []

    for item in dates:
        date_text = item["tour_date"]

        try:
            slot_date = datetime.strptime(date_text, "%Y-%m-%d").date()
        except ValueError:
            continue

        month_key = f"{slot_date.year}-{slot_date.month:02d}"

        if slot_date < today:
            continue

        if month_key > last_allowed_key:
            continue

        if month_key in used_month_keys:
            continue

        available_month_keys.append(month_key)
        used_month_keys.append(month_key)

    if not available_month_keys:
        current_year, current_month = month_offset(today, 0)
        available_month_keys.append(f"{current_year}-{current_month:02d}")

    calendar_keys = []
    month_options = []

    for index, month_key in enumerate(available_month_keys):
        year_text, month_text = month_key.split("-")
        year = int(year_text)
        month = int(month_text)

        if year == today.year and month == today.month:
            next_year, next_month = month_offset(today, 1)
            start_year = year
            start_month = month
            end_year = next_year
            end_month = next_month
        else:
            month_date = date(year, month, 1)
            previous_year, previous_month = month_offset(month_date, -1)
            start_year = previous_year
            start_month = previous_month
            end_year = year
            end_month = month

        start_key = f"{start_year}-{start_month:02d}"
        end_key = f"{end_year}-{end_month:02d}"

        if start_key not in calendar_keys:
            calendar_keys.append(start_key)

        if end_key not in calendar_keys:
            calendar_keys.append(end_key)

        month_options.append({
            "key": month_key,
            "label": f"{MONTH_NAMES[month]} {year}",
            "start_key": start_key,
            "end_key": end_key,
            "selected": index == 0
        })

    calendars = []
    calendar_keys.sort()

    for month_key in calendar_keys:
        year_text, month_text = month_key.split("-")
        year = int(year_text)
        month = int(month_text)
        calendar = build_month_calendar(year, month, available_slots)
        calendar["key"] = month_key
        calendars.append(calendar)

    return calendars, month_options


def get_available_slots_for_tour(tour_id):
    connection = get_db_connection()
    dates = connection.execute(
        """
        SELECT tour_date, tour_time
        FROM tour_dates
        WHERE tour_id = ?
        ORDER BY tour_date, tour_time
        """,
        (tour_id,)
    ).fetchall()
    connection.close()

    today = date.today()
    available_slots = []

    for item in dates:
        date_text = item["tour_date"]
        time_text = item["tour_time"]

        try:
            slot_date = datetime.strptime(date_text, "%Y-%m-%d").date()
        except ValueError:
            continue

        if slot_date < today:
            continue

        available_slots.append({
            "date": date_text,
            "time": time_text,
            "label": f"{WEEKDAYS[slot_date.weekday()]}, {MONTH_NAMES[slot_date.month]} {slot_date.day}, {slot_date.year} at {time_text}"
        })

    return available_slots


def home():
    language = request.args.get("language", "").strip()
    duration = request.args.get("duration", "").strip()
    selected_date = request.args.get("date", "").strip()

    tours = get_all_tours(
        language=language,
        duration=duration,
        selected_date=selected_date
    )

    return render_template(
        "home.html",
        tours=tours,
        selected_language=language,
        selected_duration=duration,
        selected_date=selected_date
    )


def tour_detail(tour_id):
    tour = get_tour_by_id(tour_id)

    if tour is None:
        flash("Tour not found.")
        return redirect(url_for("home"))

    calendars = build_calendars(tour_id)

    return render_template("tour_detail.html", tour=tour, calendars=calendars)


def guide_profile(guide_id):
    connection = get_db_connection()

    guide = connection.execute(
        "SELECT * FROM users WHERE id = ? AND role = 'Guide'",
        (guide_id,)
    ).fetchone()

    if guide is None:
        connection.close()
        flash("Guide profile not found.")
        return redirect(url_for("home"))

    tours = connection.execute(
        "SELECT * FROM tours WHERE guide_id = ? ORDER BY title",
        (guide_id,)
    ).fetchall()

    connection.close()

    guide_tours = []
    for tour in tours:
        tour_dict = dict(tour)
        rating = calculate_rating(tour_dict["id"])
        tour_dict["rating"] = f"{rating:.1f}"
        tour_dict["full_stars"] = full_star_count(rating)
        guide_tours.append(tour_dict)

    return render_template(
        "guide_profile.html",
        guide=dict(guide),
        guide_tours=guide_tours
    )

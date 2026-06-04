from calendar import month_name, monthrange
from datetime import date, datetime

from flask import abort, render_template, request

from database import get_db_connection


def calculate_rating(tour_id):
    """Calculate average rating from reviews. If no review exists, use a default value."""
    connection = get_db_connection()
    result = connection.execute(
        "SELECT AVG(rating) AS average_rating FROM reviews WHERE tour_id = ?",
        (tour_id,)
    ).fetchone()
    connection.close()

    if result and result["average_rating"] is not None:
        average = round(float(result["average_rating"]), 1)
    else:
        average = 4.8

    return average


def full_star_count(rating):
    """Return a safe number of filled stars for the template."""
    stars = int(round(float(rating)))

    if stars < 0:
        return 0
    if stars > 5:
        return 5

    return stars


def get_all_tours(language=None, duration=None, selected_date=None):
    """Read all tours from the tours table."""
    connection = get_db_connection()
    query = "SELECT DISTINCT tours.* FROM tours"
    parameters = []
    conditions = []

    if selected_date:
        query += " JOIN tour_dates ON tour_dates.tour_id = tours.id"
        conditions.append("tour_dates.tour_date = ?")
        parameters.append(selected_date)

    if language:
        conditions.append("(tours.language = ? OR tours.languages LIKE ?)")
        parameters.extend([language, f"%{language}%"])

    if duration:
        conditions.append("(tours.duration_minutes = ? OR tours.duration LIKE ?)")
        parameters.extend([duration, f"%{duration}%"])

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    query += " ORDER BY tours.id"

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


def get_tour_by_id(tour_id):
    """Read one complete tour with stops, dates, reviews, and guide name."""
    connection = get_db_connection()

    tour = connection.execute(
        """
        SELECT tours.*, users.full_name AS guide
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

    tour_dict["stops"] = [stop["stop_name"] for stop in stops]
    tour_dict["terrain"] = tour_dict.get("path_type") or "Urban walking path"

    normal_stops = [stop["stop_name"] for stop in stops if stop["stop_type"] == "Stop"]
    finish_stops = [stop["stop_name"] for stop in stops if stop["stop_type"] == "Finish"]

    tour_dict["rest_stops"] = normal_stops if normal_stops else ["Short rest during the route"]
    tour_dict["photo_stops"] = normal_stops + finish_stops if normal_stops or finish_stops else ["Main route viewpoint"]
    tour_dict["what_to_bring"] = ["Comfortable shoes", "Water", "Camera or phone", "Sun protection"]
    tour_dict["audience"] = "All people can participate. Check the fitness level before reserving."

    schedule = []
    available_dates = []
    used_schedule_labels = set()

    for item in dates:
        date_text = item["tour_date"]
        time_text = item["tour_time"]

        try:
            weekday_name = datetime.strptime(date_text, "%Y-%m-%d").strftime("%A")
        except ValueError:
            weekday_name = "Date"

        schedule_label = f"{weekday_name} {time_text}"

        if schedule_label not in used_schedule_labels:
            schedule.append(schedule_label)
            used_schedule_labels.add(schedule_label)

        available_dates.append({
            "date": date_text,
            "time": time_text,
            "label": f"{date_text} - {weekday_name} at {time_text}"
        })

    tour_dict["schedule"] = schedule
    tour_dict["available_dates"] = available_dates
    tour_dict["reviews"] = [dict(review) for review in reviews]
    tour_dict["photos"] = [photo["photo_path"] for photo in photos]

    return tour_dict


def month_offset(base_date, offset):
    month = base_date.month + offset
    year = base_date.year + (month - 1) // 12
    month = (month - 1) % 12 + 1
    return year, month


def build_month_calendar(year, month, available_slots):
    """
    Build a month grid for the tour calendar.

    available_slots is a dictionary:
        {"2026-06-05": "18:00"}

    Only future/today dates that exist in available_slots are clickable.
    Empty cells are blank, so previous/next month dates do not appear.
    """
    first_weekday, days_in_month = monthrange(year, month)
    today = date.today()

    weeks = []
    week = []

    for _ in range(first_weekday):
        week.append(None)

    for day_number in range(1, days_in_month + 1):
        current_date = date(year, month, day_number)
        current_date_text = current_date.isoformat()
        available_time = available_slots.get(current_date_text)

        is_available = available_time is not None and current_date >= today

        week.append({
            "day": day_number,
            "iso": current_date_text,
            "time": available_time,
            "available": is_available,
            "past": current_date < today,
            "today": current_date == today
        })

        if len(week) == 7:
            weeks.append(week)
            week = []

    if week:
        while len(week) < 7:
            week.append(None)
        weeks.append(week)

    return {
        "month_name": month_name[month],
        "year": year,
        "weeks": weeks
    }


def build_calendars(tour_id):
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

    available_slots = {
        item["tour_date"]: item["tour_time"]
        for item in dates
    }

    today = date.today()

    first_year, first_month = month_offset(today, 0)
    second_year, second_month = month_offset(today, 1)

    return [
        build_month_calendar(first_year, first_month, available_slots),
        build_month_calendar(second_year, second_month, available_slots)
    ]


def build_reservation_calendar_options(tour_id):
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

    available_slots = {
        item["tour_date"]: item["tour_time"]
        for item in dates
    }

    today = date.today()
    last_allowed_year = today.year + 1
    last_allowed_month = 12
    last_allowed_key = f"{last_allowed_year}-{last_allowed_month:02d}"

    available_month_keys = []
    used_month_keys = set()

    for item in dates:
        date_text = item["tour_date"]

        try:
            slot_date = datetime.strptime(date_text, "%Y-%m-%d").date()
        except ValueError:
            continue

        month_key = f"{slot_date.year}-{slot_date.month:02d}"

        if slot_date < today or month_key > last_allowed_key or month_key in used_month_keys:
            continue

        available_month_keys.append(month_key)
        used_month_keys.add(month_key)

    if not available_month_keys:
        current_year, current_month = month_offset(today, 0)
        available_month_keys.append(f"{current_year}-{current_month:02d}")

    calendar_keys = set()
    month_options = []

    for index, month_key in enumerate(available_month_keys):
        year_text, month_text = month_key.split("-")
        year = int(year_text)
        month = int(month_text)

        if year == today.year and month == today.month:
            next_year, next_month = month_offset(today, 1)
            start_year, start_month = year, month
            end_year, end_month = next_year, next_month
        else:
            previous_date = date(year, month, 1)
            previous_year, previous_month = month_offset(previous_date, -1)
            start_year, start_month = previous_year, previous_month
            end_year, end_month = year, month

        start_key = f"{start_year}-{start_month:02d}"
        end_key = f"{end_year}-{end_month:02d}"
        calendar_keys.add(start_key)
        calendar_keys.add(end_key)

        month_options.append({
            "key": month_key,
            "label": f"{month_name[month]} {year}",
            "start_key": start_key,
            "end_key": end_key,
            "selected": index == 0
        })

    calendars = []

    for month_key in sorted(calendar_keys):
        year_text, month_text = month_key.split("-")
        year = int(year_text)
        month = int(month_text)
        calendar = build_month_calendar(year, month, available_slots)
        calendar["key"] = month_key
        calendars.append(calendar)

    return calendars, month_options


def get_available_slots_for_tour(tour_id):
    """Return future/today date and time slots that can be reserved for one tour."""
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
            "label": f"{slot_date.strftime('%A, %B %d, %Y')} at {time_text}"
        })

    return available_slots


def home():
    language = request.args.get("language", "").strip()
    duration = request.args.get("duration", "").strip()
    selected_date = request.args.get("date", "").strip()
    tours = get_all_tours(language=language, duration=duration, selected_date=selected_date)
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
        abort(404)

    calendars = build_calendars(tour_id)

    return render_template("tour_detail.html", tour=tour, calendars=calendars)

from datetime import date

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


def get_time_minutes(time_text):
    parts = time_text.split(":")

    if len(parts) != 2:
        return None

    try:
        hour = int(parts[0])
        minute = int(parts[1])
    except ValueError:
        return None

    if hour < 0 or hour > 23:
        return None

    if minute < 0 or minute > 59:
        return None

    return hour * 60 + minute


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


def read_duration_minutes(duration_minutes):
    if duration_minutes:
        return int(duration_minutes)

    return 90


def get_duration_options():
    connection = get_db_connection()
    rows = connection.execute(
        """
        SELECT DISTINCT duration_minutes
        FROM tours
        WHERE duration_minutes IS NOT NULL
        ORDER BY duration_minutes
        """
    ).fetchall()
    connection.close()

    duration_options = []
    for x in rows:
        duration_options.append(x["duration_minutes"])

    return duration_options


def get_all_tours(language, duration, selected_date):
    connection = get_db_connection()

    if language is None:
        language = ""

    if duration is None:
        duration = ""

    if selected_date is None:
        selected_date = ""

    tours = connection.execute(
        "SELECT * FROM tours ORDER BY id"
    ).fetchall()

    tour_ids_for_selected_date = []
    if selected_date != "":
        date_rows = connection.execute(
            "SELECT tour_id FROM tour_dates WHERE tour_date = ?",
            (selected_date,)
        ).fetchall()

        for x in date_rows:
            if x["tour_id"] not in tour_ids_for_selected_date:
                tour_ids_for_selected_date.append(x["tour_id"])

    tour_ids_for_language = []
    if language != "":
        language_rows = connection.execute(
            """
            SELECT id
            FROM tours
            WHERE language = ? OR languages LIKE ?
            """,
            (language, "%" + language + "%")).fetchall()

        for x in language_rows:
            tour_ids_for_language.append(x["id"])

    tour_ids_for_duration = []
    if duration != "":
        duration_rows = connection.execute(
            "SELECT id FROM tours WHERE duration_minutes = ?",
            (duration,)
        ).fetchall()

        for x in duration_rows:
            tour_ids_for_duration.append(x["id"])

    connection.close()

    result = []

    for x in tours:
        tour_dict = dict(x)

        if selected_date != "":
            if tour_dict["id"] not in tour_ids_for_selected_date:
                continue

        if language != "":
            if tour_dict["id"] not in tour_ids_for_language:
                continue

        if duration != "":
            if tour_dict["id"] not in tour_ids_for_duration:
                continue

        result.append(tour_dict)

    return result

def get_existing_reservations_for_participant(tour_id):
    participant_id = session.get("user_id")
    role = session.get("role")

    if (
        participant_id is None
        or participant_id == ""
        or participant_id == 0
        or role != "Participant"
    ):
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
    for x in reservations:
        result.append(dict(x))

    return result


def get_tour_by_id(tour_id):
    connection = get_db_connection()

    tour = connection.execute(
        "SELECT * FROM tours WHERE id = ?",
        (tour_id,)
    ).fetchone()

    if tour is None:
        connection.close()
        return None

    tour_dict = dict(tour)

    guide = connection.execute(
        "SELECT * FROM users WHERE id = ?",
        (tour_dict["guide_id"],)
    ).fetchone()

    if guide is not None:
        tour_dict["guide"] = guide["full_name"]
        tour_dict["guide_user_id"] = guide["id"]
    else:
        tour_dict["guide"] = "Unknown guide"
        tour_dict["guide_user_id"] = tour_dict["guide_id"]

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

    stop_names = []
    normal_stops = []
    finish_stops = []

    for x in stops:
        stop_names.append(x["stop_name"])

        if x["stop_type"] == "Stop":
            normal_stops.append(x["stop_name"])

        if x["stop_type"] == "Finish":
            finish_stops.append(x["stop_name"])

    tour_dict["stops"] = stop_names

    route_stops = []

    for x in stop_names:
        if x != tour_dict["meeting_point"]:
            route_stops.append(x)

    tour_dict["route_stops"] = route_stops

    if tour_dict.get("path_type") is not None and tour_dict.get("path_type") != "":
        tour_dict["terrain"] = tour_dict.get("path_type")
    else:
        tour_dict["terrain"] = "Urban walking path"

    if len(normal_stops) > 0:
        tour_dict["rest_stops"] = normal_stops
    else:
        tour_dict["rest_stops"] = ["Short rest during the route"]

    tour_dict["what_to_bring"] = ["Comfortable shoes", "Water", "Camera or phone", "Sun protection"]
    tour_dict["audience"] = "All people can participate. Check the fitness level before reserving."

    schedule = []
    available_dates = []
    used_schedule_labels = []
    today = date.today()

    tour_schedule_rows = []
    for x in schedules:
        tour_schedule_rows.append({
            "weekday": x["weekday"],
            "start_time": x["start_time"]
        })

    tour_dict["schedules"] = tour_schedule_rows
    today_string = today.strftime("%Y-%m-%d")

    for x in schedules:
        schedule_label = "Every " + str(x["weekday"]) + " at " + str(x["start_time"])
        if schedule_label not in used_schedule_labels:
            schedule.append(schedule_label)
            used_schedule_labels.append(schedule_label)

    for x in dates:
        date_text = x["tour_date"]
        time_text = x["tour_time"]

        try:
            slot_date = date.fromisoformat(date_text)
            weekday_name = WEEKDAYS[slot_date.weekday()]
        except ValueError:
            continue

        if date_text > today_string:
            available_dates.append({
                "date": date_text,
                "time": time_text,
                "label": date_text + " - " + weekday_name + " at " + time_text
            })

    photo_list = []
    for x in photos:
        photo_list.append(x["photo_path"])

    tour_dict["schedule"] = schedule
    tour_dict["available_dates"] = available_dates
    tour_dict["photos"] = photo_list
    tour_dict["existing_reservations"] = get_existing_reservations_for_participant(tour_id)

    return tour_dict

# Return the (year, month) reached by adding a month offset to a base date.
def month_offset(base_date, offset):
    month = base_date.month + offset
    year = base_date.year + (month - 1) // 12
    month = (month - 1) % 12 + 1
    return year, month

# Build the calendar grid for a single month, marking available days.
def build_month_calendar(year, month, available_slots):
    first_day = date(year, month, 1)
    first_weekday = first_day.weekday()
    days_in_month = get_days_in_month(year, month)
    today = date.today()

    weeks = []
    week = []

    for i in range(first_weekday):
        week.append(None)

    for day_number in range(1, days_in_month + 1):
        current_date = date(year, month, day_number)
        current_date_text = current_date.isoformat()
        available_time = available_slots.get(current_date_text)

        is_available = False
        if available_time is not None:
            if current_date > today:
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

    if len(week) > 0:
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
    date_rows = connection.execute(
        """
        SELECT tour_date, tour_time
        FROM tour_dates
        WHERE tour_id = ?
        ORDER BY tour_date, tour_time
        """,
        (tour_id,)
    ).fetchall()
    connection.close()

    today_string = str(date.today())

    dates = []

    for x in date_rows:
        date_text = x["tour_date"]

        try:
            date.fromisoformat(date_text)
        except ValueError:
            continue

        if date_text > today_string:
            dates.append(x)

    available_slots = {}
    for x in dates:
        available_slots[x["tour_date"]] = x["tour_time"]

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

# Build the calendar data and month options used by the reservation page.
def build_reservation_calendar_options(tour_id):
    available_slots, dates = get_available_slot_dictionary(tour_id)

    today = date.today()
    today_string = str(today)

    last_allowed_year = today.year + 1
    last_allowed_month = 12
    
    month_string = str(last_allowed_month)

    if last_allowed_month < 10:
        month_string = "0" + month_string

    last_allowed_key = str(last_allowed_year) + "-" + month_string

    available_month_keys = []
    used_month_keys = []

    for x in dates:
        date_text = x["tour_date"]

        try:
            slot_date = date.fromisoformat(date_text)
        except ValueError:
            continue

        month_key = str(slot_date)[:7]

        if date_text <= today_string:
            continue

        if month_key > last_allowed_key:
            continue

        if month_key in used_month_keys:
            continue

        available_month_keys.append(month_key)
        used_month_keys.append(month_key)

    
    if len(available_month_keys) == 0:
        current_year, current_month = month_offset(today, 0)

        month_string = str(current_month)

        if current_month < 10:
            month_string = "0" + month_string

        available_month_keys.append(str(current_year) + "-" + month_string)

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

        

        start_month_string = str(start_month)

        if start_month < 10:
            start_month_string = "0" + start_month_string

        start_key = str(start_year) + "-" + start_month_string


        end_month_string = str(end_month)

        if end_month < 10:
            end_month_string = "0" + end_month_string

        end_key = str(end_year) + "-" + end_month_string

        if start_key not in calendar_keys:
            calendar_keys.append(start_key)

        if end_key not in calendar_keys:
            calendar_keys.append(end_key)

        month_options.append({
            "key": month_key,
            "label": str(MONTH_NAMES[month]) + " " + str(year),
            "start_key": start_key,
            "end_key": end_key,
            "selected": index == 0
        })

    calendars = []
    calendar_keys.sort()

    for x in calendar_keys:
        year_text, month_text = x.split("-")
        year = int(year_text)
        month = int(month_text)
        calendar = build_month_calendar(year, month, available_slots)
        calendar["key"] = x
        calendars.append(calendar)

    return calendars, month_options


# Load future available slots for this tour.
def get_available_slots_for_tour(tour_id):
    
    today_string = str(date.today())

    connection = get_db_connection()
    dates = connection.execute("""
        SELECT tour_date, tour_time
        FROM tour_dates
        WHERE tour_id = ?
          AND tour_date > ?
        ORDER BY tour_date, tour_time
        """, (tour_id, today_string)).fetchall() 
    
    connection.close()

    available_slots = []

    for x in dates:
        available_slots.append({
            "date": x["tour_date"],
            "time": x["tour_time"],
            "label": x["tour_date"] + " at " + x["tour_time"]
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
    duration_options = get_duration_options()

    return render_template(
        "home.html",
        tours=tours,
        duration_options=duration_options,
        selected_language=language,
        selected_duration=duration,selected_date=selected_date)


def tour_detail(tour_id):
    tour = get_tour_by_id(tour_id)

    if tour is None:
        flash("Tour not found.")
        return redirect(url_for("home"))

    calendars = build_calendars(tour_id)

    return render_template("tour_detail.html", tour=tour, calendars=calendars)


def guide_profile(guide_id):
    connection = get_db_connection()

    guide = connection.execute("SELECT * FROM users WHERE id = ? AND role = 'Guide'",(guide_id,)).fetchone()

    if guide is None:
        connection.close()
        flash("Guide profile not found.")
        return redirect(url_for("home"))

    tours = connection.execute("SELECT * FROM tours WHERE guide_id = ? ORDER BY title",
        (guide_id,)
).fetchall()

    connection.close()

    guide_tours = []
    for x in tours:
        guide_tours.append(dict(x))

    return render_template(
        "guide_profile.html",
        guide=dict(guide),
        guide_tours=guide_tours
    )

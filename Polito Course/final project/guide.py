from datetime import date

from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from auth import require_role
from database import get_db_connection
from models import get_current_user
from tours import calculate_rating, full_star_count, get_tour_by_id


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


def read_duration_minutes(duration_text):
    digits = ""
    for character in duration_text:
        if character.isdigit():
            digits = digits + character

    if digits:
        return int(digits)

    return 90


def get_weekly_start_minute(weekday, start_time):
    if weekday not in WEEKDAYS:
        return None

    time_minutes = get_time_minutes(start_time)
    if time_minutes is None:
        return None

    weekday_index = WEEKDAYS.index(weekday)
    return weekday_index * 24 * 60 + time_minutes


def intervals_overlap(first_start, first_end, second_start, second_end):
    if first_start < second_end and second_start < first_end:
        return True

    return False


def weekly_intervals_overlap(first_start, first_end, second_start, second_end):
    week_minutes = 7 * 24 * 60

    for shift in [-week_minutes, 0, week_minutes]:
        shifted_start = second_start + shift
        shifted_end = second_end + shift

        if intervals_overlap(first_start, first_end, shifted_start, shifted_end):
            return True

    return False


def guide_has_schedule_overlap(connection, guide_id, weekday, start_time, duration_minutes, ignored_tour_id=None):
    new_start = get_weekly_start_minute(weekday, start_time)
    if new_start is None:
        return True

    new_end = new_start + duration_minutes

    rows = connection.execute(
        """
        SELECT tours.id, tours.title, tours.duration, tours.duration_minutes,
               tour_schedules.weekday, tour_schedules.start_time
        FROM tours
        JOIN tour_schedules ON tour_schedules.tour_id = tours.id
        WHERE tours.guide_id = ?
        """,
        (guide_id,)
    ).fetchall()

    for row in rows:
        if ignored_tour_id is not None:
            if int(row["id"]) == int(ignored_tour_id):
                continue

        old_start = get_weekly_start_minute(row["weekday"], row["start_time"])
        if old_start is None:
            continue

        if row["duration_minutes"]:
            old_duration = int(row["duration_minutes"])
        else:
            old_duration = read_duration_minutes(row["duration"])

        old_end = old_start + old_duration

        if weekly_intervals_overlap(new_start, new_end, old_start, old_end):
            return True

    return False


def split_languages(language_text):
    cleaned_text = language_text.replace("/", ",")
    raw_items = cleaned_text.split(",")

    languages = []
    for item in raw_items:
        language = item.strip()
        if language:
            languages.append(language)

    return languages


def tour_languages_allowed_for_guide(connection, guide_id, tour_languages):
    guide = connection.execute(
        "SELECT spoken_languages FROM users WHERE id = ?",
        (guide_id,)
    ).fetchone()

    if guide is None:
        return False

    guide_languages = split_languages(guide["spoken_languages"] or "")
    guide_languages_lower = []
    for language in guide_languages:
        guide_languages_lower.append(language.lower())

    requested_languages = split_languages(tour_languages)

    for language in requested_languages:
        if language.lower() not in guide_languages_lower:
            return False

    return True


def date_matches_weekday(date_object, weekday_name):
    if weekday_name not in WEEKDAYS:
        return False

    weekday_number = WEEKDAYS.index(weekday_name)
    return date_object.weekday() == weekday_number


def create_dates_for_schedule(connection, tour_id, weekday, start_time):
    today = date.today()

    for day_offset in range(0, 366):
        future_date = add_days_to_date(today, day_offset)

        if date_matches_weekday(future_date, weekday):
            existing = connection.execute(
                """
                SELECT id
                FROM tour_dates
                WHERE tour_id = ? AND tour_date = ?
                """,
                (tour_id, future_date.isoformat())
            ).fetchone()

            if existing is None:
                connection.execute(
                    """
                    INSERT INTO tour_dates (tour_id, tour_date, tour_time)
                    VALUES (?, ?, ?)
                    """,
                    (tour_id, future_date.isoformat(), start_time)
                )


def save_uploaded_file(uploaded_file, prefix, item_id):
    if not uploaded_file:
        return ""

    if not uploaded_file.filename:
        return ""

    filename_parts = uploaded_file.filename.rsplit(".", 1)
    if len(filename_parts) != 2:
        return ""

    extension = filename_parts[-1].lower()
    if extension not in ["jpg", "jpeg", "png", "webp"]:
        return ""

    filename = f"{prefix}_{item_id}.{extension}"
    save_path = f"static/uploads/{filename}"
    uploaded_file.save(save_path)

    return f"uploads/{filename}"


def get_completed_tours_for_guide(guide_id):
    connection = get_db_connection()
    completed_tours = connection.execute(
        """
        SELECT completed_tours.*, tours.title, tours.image, tours.meeting_point
        FROM completed_tours
        JOIN tours ON tours.id = completed_tours.tour_id
        WHERE completed_tours.guide_id = ?
        ORDER BY completed_tours.completed_date DESC
        """,
        (guide_id,)
    ).fetchall()
    connection.close()

    result = []

    for item in completed_tours:
        item_dict = dict(item)
        completed_item = {
            "id": item_dict["id"],
            "date": item_dict["completed_date"],
            "participants": item_dict["participants_count"],
            "status": "Reported",
            "tour": {
                "id": item_dict["tour_id"],
                "title": item_dict["title"],
                "image": item_dict["image"],
                "meeting_point": item_dict["meeting_point"]
            }
        }
        result.append(completed_item)

    return result


@login_required
def guide_dashboard():
    role_redirect = require_role("Guide")
    if role_redirect:
        return role_redirect

    logged_user = get_current_user()
    guide_id = int(current_user.id)

    connection = get_db_connection()
    guide_tours = connection.execute(
        "SELECT * FROM tours WHERE guide_id = ? ORDER BY id",
        (guide_id,)
    ).fetchall()

    guide_tour_list = []
    upcoming_participants = 0

    for tour in guide_tours:
        tour_dict = dict(tour)
        rating = calculate_rating(tour_dict["id"])
        tour_dict["rating"] = f"{rating:.1f}"
        tour_dict["full_stars"] = full_star_count(rating)

        scheduled_dates = connection.execute(
            """
            SELECT tour_dates.tour_date AS selected_date,
                   tour_dates.tour_time AS selected_time,
                   COUNT(reservations.id) AS reservations_count,
                   COALESCE(SUM(1 + COALESCE(reservations.extra_people_count, reservations.extra_people, 0)), 0) AS expected_participants
            FROM tour_dates
            LEFT JOIN reservations
              ON reservations.tour_id = tour_dates.tour_id
             AND reservations.selected_date = tour_dates.tour_date
             AND reservations.selected_time = tour_dates.tour_time
             AND reservations.status != 'Cancelled'
            WHERE tour_dates.tour_id = ?
            GROUP BY tour_dates.tour_date, tour_dates.tour_time
            ORDER BY tour_dates.tour_date, tour_dates.tour_time
            """,
            (tour_dict["id"],)
        ).fetchall()

        reservation_summaries = []
        for item in scheduled_dates:
            item_dict = dict(item)
            reservation_summaries.append(item_dict)
            upcoming_participants = upcoming_participants + item_dict["expected_participants"]

        tour_dict["reservation_summaries"] = reservation_summaries
        guide_tour_list.append(tour_dict)

    connection.close()

    completed = get_completed_tours_for_guide(guide_id)

    return render_template(
        "guide_dashboard.html",
        current_user=logged_user,
        guide_tours=guide_tour_list,
        completed_tours=completed,
        upcoming_participants=upcoming_participants
    )


@login_required
def create_tour():
    role_redirect = require_role("Guide")
    if role_redirect:
        return role_redirect

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        main_language = request.form.get("main_language", "English").strip()
        languages = request.form.get("languages", "").strip()
        duration = request.form.get("duration", "").strip()
        distance = request.form.get("distance", "").strip()
        max_participants = request.form.get("max_participants", "15").strip()
        meeting_point = request.form.get("meeting_point", "").strip()
        description = request.form.get("description", "").strip()
        start_point = request.form.get("start_point", "").strip()
        stop_one = request.form.get("stop_one", "").strip()
        stop_two = request.form.get("stop_two", "").strip()
        finish_point = request.form.get("finish_point", "").strip()
        rest_stops = request.form.get("rest_stops", "").strip()
        fitness_level = request.form.get("fitness_level", "Easy").strip()
        path_type = request.form.get("path_type", "Urban walking path").strip()
        mountain_path = request.form.get("mountain_path", "No").strip()
        children_allowed = request.form.get("children_allowed", "Yes").strip()
        pets_allowed = request.form.get("pets_allowed", "Yes, on leash").strip()
        what_to_bring = request.form.get("what_to_bring", "").strip()
        schedule_weekday = request.form.get("schedule_weekday", "Monday").strip()
        schedule_start_time = request.form.get("schedule_start_time", "10:00").strip()
        tour_image = request.files.get("tour_image")

        if not title:
            flash("Please enter a tour title.")
            return render_template("create_tour.html")

        if not languages:
            languages = f"English / {main_language} / Spanish"

        if not duration:
            duration = "90 min"

        if not distance:
            distance = "2.0 km"

        if not meeting_point:
            meeting_point = "Meeting point not specified"

        if not description:
            description = "New walking tour description."

        if schedule_weekday not in WEEKDAYS:
            flash("Please choose a valid weekly schedule day.")
            return render_template("create_tour.html")

        if get_time_minutes(schedule_start_time) is None:
            flash("Please enter the start time in HH:MM format.")
            return render_template("create_tour.html")

        stops = [start_point, stop_one, stop_two, finish_point]
        valid_stop_count = 0
        for stop in stops:
            if stop:
                valid_stop_count = valid_stop_count + 1

        if valid_stop_count < 4:
            flash("Please enter at least four route points: start, two stops, and finish.")
            return render_template("create_tour.html")

        guide_id = int(current_user.id)
        duration_minutes = read_duration_minutes(duration)

        try:
            max_participants_number = int(max_participants or 15)
        except ValueError:
            max_participants_number = 15

        if what_to_bring:
            notes = what_to_bring
        elif rest_stops:
            notes = rest_stops
        else:
            notes = "Created by guide."

        connection = get_db_connection()

        if not tour_languages_allowed_for_guide(connection, guide_id, languages):
            connection.close()
            flash("Tour languages must be among the languages selected during guide registration.")
            return render_template("create_tour.html")

        schedule_overlap = guide_has_schedule_overlap(
            connection,
            guide_id,
            schedule_weekday,
            schedule_start_time,
            duration_minutes
        )

        if schedule_overlap:
            connection.close()
            flash("This weekly schedule overlaps with another tour created by this guide.")
            return render_template("create_tour.html")

        cursor = connection.execute(
            """
            INSERT INTO tours (
                guide_id, title, description, image, languages, language,
                duration, duration_minutes, distance, price, meeting_point,
                max_participants, fitness_level, path_type, mountain_path,
                pets_allowed, children_allowed, accessibility, notes
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                guide_id,
                title,
                description,
                "images/places/griffith-observatory.jpg",
                languages,
                languages.split("/")[0].strip(),
                duration,
                duration_minutes,
                distance,
                "Walking tour",
                meeting_point,
                max_participants_number,
                fitness_level,
                path_type,
                mountain_path,
                pets_allowed,
                children_allowed,
                "Accessibility information not added yet.",
                notes
            )
        )

        tour_id = cursor.lastrowid

        saved_image_path = save_uploaded_file(tour_image, "tour", tour_id)
        if saved_image_path:
            connection.execute(
                "UPDATE tours SET image = ? WHERE id = ?",
                (saved_image_path, tour_id)
            )

        for index, stop_name in enumerate(stops, start=1):
            if index == 1:
                stop_type = "Start"
            elif index == len(stops):
                stop_type = "Finish"
            else:
                stop_type = "Stop"

            connection.execute(
                """
                INSERT INTO tour_stops (tour_id, stop_order, stop_name, stop_type)
                VALUES (?, ?, ?, ?)
                """,
                (tour_id, index, stop_name, stop_type)
            )

        connection.execute(
            """
            INSERT INTO tour_schedules (tour_id, weekday, start_time)
            VALUES (?, ?, ?)
            """,
            (tour_id, schedule_weekday, schedule_start_time)
        )

        create_dates_for_schedule(connection, tour_id, schedule_weekday, schedule_start_time)

        connection.commit()
        connection.close()

        flash("New tour saved in the database.")
        return redirect(url_for("guide_dashboard"))

    return render_template("create_tour.html")


@login_required
def edit_tour(tour_id):
    role_redirect = require_role("Guide")
    if role_redirect:
        return role_redirect

    tour = get_tour_by_id(tour_id)

    if tour is None:
        flash("Tour not found.")
        return redirect(url_for("guide_dashboard"))

    if tour["guide_id"] != int(current_user.id):
        flash("You can edit only your own tours.")
        return redirect(url_for("guide_dashboard"))

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        languages = request.form.get("languages", "").strip()
        duration = request.form.get("duration", "").strip()
        distance = request.form.get("distance", "").strip()
        meeting_point = request.form.get("meeting_point", "").strip()
        description = request.form.get("description", "").strip()
        schedule_weekday = request.form.get("schedule_weekday", tour["schedule_weekday"]).strip()
        schedule_start_time = request.form.get("schedule_start_time", tour["schedule_start_time"]).strip()
        tour_image = request.files.get("tour_image")

        connection = get_db_connection()
        reservation_count = connection.execute(
            "SELECT COUNT(*) AS count FROM reservations WHERE tour_id = ? AND status != 'Cancelled'",
            (tour_id,)
        ).fetchone()["count"]

        if reservation_count:
            connection.execute(
                "UPDATE tours SET description = ? WHERE id = ?",
                (description, tour_id)
            )
            flash("This tour already has reservations, so only the description was updated.")
        else:
            if not title or not languages or not duration or not distance or not meeting_point or not description:
                connection.close()
                flash("Please fill in all basic tour fields.")
                return render_template("edit_tour.html", tour=tour)

            if schedule_weekday not in WEEKDAYS:
                connection.close()
                flash("Please choose a valid weekly schedule day.")
                return render_template("edit_tour.html", tour=tour)

            if get_time_minutes(schedule_start_time) is None:
                connection.close()
                flash("Please enter the start time in HH:MM format.")
                return render_template("edit_tour.html", tour=tour)

            stops = []
            for index in range(1, 5):
                stop_name = request.form.get(f"stop_{index}", "").strip()
                stops.append(stop_name)

            valid_stop_count = 0
            for stop in stops:
                if stop:
                    valid_stop_count = valid_stop_count + 1

            if valid_stop_count < 4:
                connection.close()
                flash("Please keep at least four route points for the tour.")
                return render_template("edit_tour.html", tour=tour)

            if not tour_languages_allowed_for_guide(connection, int(current_user.id), languages):
                connection.close()
                flash("Tour languages must be among the languages selected during guide registration.")
                return render_template("edit_tour.html", tour=tour)

            duration_minutes = read_duration_minutes(duration)
            schedule_overlap = guide_has_schedule_overlap(
                connection,
                int(current_user.id),
                schedule_weekday,
                schedule_start_time,
                duration_minutes,
                ignored_tour_id=tour_id
            )

            if schedule_overlap:
                connection.close()
                flash("This weekly schedule overlaps with another tour created by this guide.")
                return render_template("edit_tour.html", tour=tour)

            if languages:
                main_language = languages.split("/")[0].strip()
            else:
                main_language = ""

            connection.execute(
                """
                UPDATE tours
                SET title = ?, languages = ?, language = ?, duration = ?,
                    duration_minutes = ?, distance = ?, meeting_point = ?,
                    description = ?, price = ?
                WHERE id = ?
                """,
                (
                    title,
                    languages,
                    main_language,
                    duration,
                    duration_minutes,
                    distance,
                    meeting_point,
                    description,
                    "Walking tour",
                    tour_id
                )
            )

            saved_image_path = save_uploaded_file(tour_image, "tour", tour_id)
            if saved_image_path:
                connection.execute(
                    "UPDATE tours SET image = ? WHERE id = ?",
                    (saved_image_path, tour_id)
                )

            connection.execute("DELETE FROM tour_stops WHERE tour_id = ?", (tour_id,))
            connection.execute("DELETE FROM tour_schedules WHERE tour_id = ?", (tour_id,))
            connection.execute("DELETE FROM tour_dates WHERE tour_id = ?", (tour_id,))

            for index, stop_name in enumerate(stops, start=1):
                if index == 1:
                    stop_type = "Start"
                elif index == 4:
                    stop_type = "Finish"
                else:
                    stop_type = "Stop"

                connection.execute(
                    """
                    INSERT INTO tour_stops (tour_id, stop_order, stop_name, stop_type)
                    VALUES (?, ?, ?, ?)
                    """,
                    (tour_id, index, stop_name, stop_type)
                )

            connection.execute(
                """
                INSERT INTO tour_schedules (tour_id, weekday, start_time)
                VALUES (?, ?, ?)
                """,
                (tour_id, schedule_weekday, schedule_start_time)
            )
            create_dates_for_schedule(connection, tour_id, schedule_weekday, schedule_start_time)

        connection.commit()
        connection.close()

        if not reservation_count:
            flash("Tour updated in the database.")

        return redirect(url_for("guide_dashboard"))

    return render_template("edit_tour.html", tour=tour)


@login_required
def completed_tours():
    role_redirect = require_role("Guide")
    if role_redirect:
        return role_redirect

    guide_id = int(current_user.id)

    if request.method == "POST":
        tour_id = request.form.get("tour_id", "").strip()
        tour_date = request.form.get("tour_date", "").strip()
        actual_participants_count = request.form.get("actual_participants_count", "").strip()
        notes = request.form.get("notes", "").strip()
        evidence_photo = request.files.get("evidence_photo")

        if not tour_id or not tour_date or not actual_participants_count:
            flash("Please select a tour date and enter actual participants.")
            return redirect(url_for("completed_tours"))

        try:
            participant_number = int(actual_participants_count or 0)
        except ValueError:
            participant_number = 0

        connection = get_db_connection()
        owns_date = connection.execute(
            """
            SELECT tour_dates.id
            FROM tour_dates
            JOIN tours ON tours.id = tour_dates.tour_id
            WHERE tour_dates.tour_id = ?
              AND tour_dates.tour_date = ?
              AND tours.guide_id = ?
            """,
            (tour_id, tour_date, guide_id)
        ).fetchone()

        if owns_date is None:
            connection.close()
            flash("You can report only scheduled dates from your own tours.")
            return redirect(url_for("completed_tours"))

        evidence_path = save_uploaded_file(evidence_photo, f"completed_{tour_id}_{tour_date.replace('-', '')}", guide_id)

        connection.execute(
            """
            INSERT INTO completed_tours (
                tour_id, guide_id, completed_date, tour_date, participants_count,
                actual_participants_count, evidence_photo_path, notes
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                tour_id,
                guide_id,
                tour_date,
                tour_date,
                participant_number,
                participant_number,
                evidence_path,
                notes
            )
        )
        connection.commit()
        connection.close()

        flash("Completed tour report saved.")
        return redirect(url_for("completed_tours"))

    completed = get_completed_tours_for_guide(guide_id)

    connection = get_db_connection()
    reportable_dates_rows = connection.execute(
        """
        SELECT tours.id AS tour_id, tours.title,
               tour_dates.tour_date AS tour_date,
               tour_dates.tour_time AS tour_time,
               COALESCE(SUM(1 + COALESCE(reservations.extra_people_count, reservations.extra_people, 0)), 0) AS expected_participants
        FROM tour_dates
        JOIN tours ON tours.id = tour_dates.tour_id
        LEFT JOIN reservations
          ON reservations.tour_id = tour_dates.tour_id
         AND reservations.selected_date = tour_dates.tour_date
         AND reservations.selected_time = tour_dates.tour_time
         AND reservations.status != 'Cancelled'
        WHERE tours.guide_id = ?
          AND datetime(tour_dates.tour_date || ' ' || tour_dates.tour_time) < datetime('now')
          AND NOT EXISTS (
              SELECT 1
              FROM completed_tours
              WHERE completed_tours.tour_id = tour_dates.tour_id
                AND completed_tours.tour_date = tour_dates.tour_date
          )
        GROUP BY tours.id, tour_dates.tour_date, tour_dates.tour_time
        ORDER BY tour_dates.tour_date DESC, tour_dates.tour_time DESC
        """,
        (guide_id,)
    ).fetchall()
    connection.close()

    reportable_dates = []
    for item in reportable_dates_rows:
        reportable_dates.append(dict(item))

    return render_template(
        "completed_tours.html",
        completed_tours=completed,
        reportable_dates=reportable_dates
    )

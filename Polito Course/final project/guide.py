from datetime import date , datetime

from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from auth import require_role
from database import get_db_connection
from models import get_current_user
from tours import get_time_minutes, get_tour_by_id
from image_helpers import (
    DEFAULT_TOUR_IMAGE,
    count_uploaded_photo_files,
    uploaded_photo_extensions_are_valid,
    read_tour_photo_files,
    save_tour_photos,
    get_current_tour_photos,
    save_uploaded_file
)

from guide_overlapping_helpers import (
    read_schedule_rows_from_form,
    schedules_overlap_with_each_other,
    guide_has_schedule_overlap,
    create_dates_for_schedules
)




def split_languages(language_text):
    cleaned_text = language_text.replace("/", ",")
    raw_items = cleaned_text.split(",")

    languages = []
    for x in raw_items:
        y = x.strip()
        if y != "":
            languages.append(y)

    return languages


# A tour may only use languages the guide selected during registration.
def tour_languages_allowed_for_guide(connection, guide_id, tour_languages):

    guide = connection.execute("SELECT spoken_languages FROM users WHERE id = ?",(guide_id,)).fetchone()

    if guide is None:
        return False

    guide_languages = split_languages(guide["spoken_languages"] or "")
    
    guide_languages_lower = []
    
    for x in guide_languages:
        guide_languages_lower.append(x.lower())

    requested_languages = split_languages(tour_languages)

    for x in requested_languages:
        if x.lower() not in guide_languages_lower:
            return False

    return True

def get_completed_tours_for_guide(guide_id):
    connection = get_db_connection()
    completed_tours = connection.execute(
        """
        SELECT completed_tours.*, tours.title, tours.image, tours.meeting_point
        FROM completed_tours
        JOIN tours ON tours.id = completed_tours.tour_id
        WHERE completed_tours.guide_id = ?
        ORDER BY completed_tours.tour_date DESC
        """,
        (guide_id,)
    ).fetchall()
    connection.close()

    result = []

    for x in completed_tours:
        item_dict = dict(x)
        completed_item = {
            "id": item_dict["id"],
            "date": item_dict["tour_date"],
            "participants": item_dict["actual_participants_count"],
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


def get_reservation_details_for_date(connection, tour_id, selected_date, selected_time):
    rows = connection.execute(
        """
        SELECT reservations.id, reservations.main_participant_name,
               users.full_name,
               1 + COALESCE(reservations.extra_people_count, 0) AS group_size,
               reservations.phone_number, reservations.message_to_guide,
               reservations.status
        FROM reservations
        JOIN users ON users.id = reservations.participant_id
        WHERE reservations.tour_id = ?
          AND reservations.selected_date = ?
          AND reservations.selected_time = ?
          AND reservations.status != 'Cancelled'
        ORDER BY users.full_name
        """,
        (tour_id, selected_date, selected_time)
    ).fetchall()

    reservation_list = []
    for x in rows:
        reservation = dict(x)

        extra_people_rows = connection.execute(
            """
            SELECT full_name
            FROM reservation_extra_people
            WHERE reservation_id = ?
            ORDER BY id
            """,
            (reservation["id"],)
        ).fetchall()

        extra_names = []
        for y in extra_people_rows:
            extra_names.append(y["full_name"])

        reservation["extra_names"] = extra_names
        reservation_list.append(reservation)

    return reservation_list


def tour_has_reservations(tour_id):
    connection = get_db_connection()
    reservation = connection.execute(
        """
        SELECT id
        FROM reservations
        WHERE tour_id = ?
          AND status != 'Cancelled'
        LIMIT 1
        """,
        (tour_id,)
    ).fetchone()
    connection.close()

    if reservation is not None:
        return True
    return False


@login_required
def guide_dashboard():
    role_redirect = require_role("Guide")
    if role_redirect is not None:
        return role_redirect

    logged_user = get_current_user()

    guide_id = int(current_user.id)

    connection = get_db_connection()

    # Load all tours created by this guide.
    guide_tours = connection.execute("SELECT * FROM tours WHERE guide_id = ? ORDER BY id",(guide_id,)).fetchall()

    guide_tour_list = []

    upcoming_participants = 0

    for x in guide_tours:
        tour_dict = dict(x)
        tour_dict["has_reservations"] = tour_has_reservations(tour_dict["id"])

        # Load up to the next 12 upcoming dates for this tour.
        scheduled_dates = connection.execute(
            """
            SELECT tour_date AS selected_date,
                tour_time AS selected_time
            FROM tour_dates
            WHERE tour_id = ?
            AND tour_date >= date('now')
            ORDER BY tour_date, tour_time
            LIMIT 12
            """, (tour_dict["id"],)).fetchall()

        reservation_summaries = []

        # Count expected participants for each upcoming date.
        for y in scheduled_dates:
            item_dict = dict(y)

            reservations = connection.execute(
                """
                SELECT *
                FROM reservations
                WHERE tour_id = ?
                  AND selected_date = ?
                  AND selected_time = ?
                  AND status != 'Cancelled'
                """,
                (
                    tour_dict["id"],
                    item_dict["selected_date"],
                    item_dict["selected_time"]
                )
            ).fetchall()

            expected_participants = 0

            for z in reservations:
                extra = z["extra_people_count"]
                if extra is None:
                    extra = 0

                expected_participants = expected_participants + 1 + extra

            item_dict["reservations_count"] = len(reservations)
            item_dict["expected_participants"] = expected_participants
            item_dict["reservations"] = get_reservation_details_for_date(
                connection,
                tour_dict["id"],
                item_dict["selected_date"],
                item_dict["selected_time"]
            )

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
    # Only guides may create tours.
    flag = require_role("Guide")

    if flag is not None:
        return flag

    if request.method != "POST":
        return render_template("create_tour.html")

    title = request.form.get("title", "").strip()
    main_language = request.form.get("main_language", "").strip()
    selected_languages = request.form.getlist("languages")
    languages = " / ".join(selected_languages)

    duration_input = request.form.get("duration", "").strip()
    distance_input = request.form.get("distance", "").strip()
    max_participants = request.form.get("max_participants", "").strip()

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

    photo_files = read_tour_photo_files()

    if count_uploaded_photo_files(photo_files) != 5:
        flash("Please upload exactly 5 promotional photos for the tour.")
        return render_template("create_tour.html")

    if not uploaded_photo_extensions_are_valid(photo_files):
        flash("Tour photos must be jpg, jpeg, png, or webp files.")
        return render_template("create_tour.html")

    if title == "":
        flash("Please fill in the tour title.")
        return render_template("create_tour.html")

    if main_language == "":
        flash("Please choose the main language.")
        return render_template("create_tour.html")

    if duration_input == "":
        flash("Please fill in the duration.")
        return render_template("create_tour.html")

    if max_participants == "":
        flash("Please fill in the maximum participants.")
        return render_template("create_tour.html")

    if meeting_point == "":
        flash("Please fill in the meeting point.")
        return render_template("create_tour.html")

    if description == "":
        flash("Please fill in the description.")
        return render_template("create_tour.html")

    if languages == "":
        languages = main_language
    else:
        language_list = split_languages(languages)

        if main_language not in language_list:
            languages = main_language + " / " + languages

    try:
        duration_minutes = int(duration_input)
    except ValueError:
        flash("Duration must be a whole number of minutes.")
        return render_template("create_tour.html")

    if duration_minutes <= 0:
        flash("Duration must be at least 1 minute.")
        return render_template("create_tour.html")

    duration = str(duration_minutes) + " min"

    distance = ""

    if distance_input != "":
        try:
            distance_number = float(distance_input)
        except ValueError:
            flash("Distance must be a number.")
            return render_template("create_tour.html")

        if distance_number < 0:
            flash("Distance cannot be negative.")
            return render_template("create_tour.html")

        distance = str(distance_number) + " km"

    try:
        max_participants_number = int(max_participants)
    except ValueError:
        flash("Maximum participants must be a number.")
        return render_template("create_tour.html")

    if max_participants_number < 1:
        flash("Maximum participants must be between 1 and 30.")
        return render_template("create_tour.html")

    if max_participants_number > 30:
        flash("Maximum participants must be between 1 and 30.")
        return render_template("create_tour.html")

    # Read the weekly schedule rows from the form; schedule_error holds any validation message.
    schedules, schedule_error = read_schedule_rows_from_form()

    if schedule_error != "":
        flash(schedule_error)
        return render_template("create_tour.html")

    if schedules_overlap_with_each_other(schedules, duration_minutes):
        flash("The weekly schedule rows overlap with each other.")
        return render_template("create_tour.html")

    valid_stop_count = 0

    if start_point != "":
        valid_stop_count = valid_stop_count + 1

    if stop_one != "":
        valid_stop_count = valid_stop_count + 1

    if stop_two != "":
        valid_stop_count = valid_stop_count + 1

    if finish_point != "":
        valid_stop_count = valid_stop_count + 1

    if valid_stop_count < 4:
        flash("Please enter at least four route points: start, two stops, and finish.")
        return render_template("create_tour.html")

    guide_id = int(current_user.id)

    # Combine rest stops and what to bring into the notes field, keeping both when both are filled.
    notes_parts = []

    if rest_stops != "":
        notes_parts.append("Rest stops: " + rest_stops)

    if what_to_bring != "":
        notes_parts.append("What to bring: " + what_to_bring)

    if len(notes_parts) > 0:
        notes = " | ".join(notes_parts)
    else:
        notes = "Created by guide."

    connection = get_db_connection()

    if not tour_languages_allowed_for_guide(connection, guide_id, languages):
        connection.close()
        flash("Tour languages must be among the languages selected during guide registration.")
        return render_template("create_tour.html")

    if guide_has_schedule_overlap(connection, guide_id, schedules, duration_minutes):
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
            DEFAULT_TOUR_IMAGE,
            languages,
            main_language,
            duration,
            duration_minutes,
            distance,
            "Free / Tip-based",
            meeting_point,
            max_participants_number,
            fitness_level,
            path_type,
            mountain_path,
            pets_allowed,
            children_allowed,
            "Accessibility information not added yet.",
            notes))

    tour_id = cursor.lastrowid

    photos_saved = save_tour_photos(connection, tour_id, photo_files, old_main_image=DEFAULT_TOUR_IMAGE)

    if not photos_saved:
        connection.rollback()
        connection.close()
        flash("Please upload 5 valid promotional photos for the tour.")
        return render_template("create_tour.html")

    stops = [
        start_point,
        stop_one,
        stop_two,
        finish_point
    ]

    stop_number = 1

    for x in stops:
        stop_type = "Stop"

        if stop_number == 1:
            stop_type = "Start"

        if stop_number == len(stops):
            stop_type = "Finish"

        connection.execute(
            """
            INSERT INTO tour_stops (tour_id, stop_order, stop_name, stop_type)
            VALUES (?, ?, ?, ?)
            """,
            (tour_id, stop_number, x, stop_type)
        )

        stop_number = stop_number + 1

    for x in schedules:
        connection.execute(
            """
            INSERT INTO tour_schedules (tour_id, weekday, start_time)
            VALUES (?, ?, ?)
            """,
            (tour_id, x["weekday"], x["start_time"])
        )

    create_dates_for_schedules(connection, tour_id, schedules)

    connection.commit()
    connection.close()

    flash("New tour saved in the database.")
    return redirect(url_for("guide_dashboard"))

@login_required
def edit_tour(tour_id):
    role_redirect = require_role("Guide")
    if role_redirect is not None:
        return role_redirect

    tour = get_tour_by_id(tour_id)

    if tour is None:
        flash("Tour not found.")
        return redirect(url_for("guide_dashboard"))

    if tour["guide_id"] != int(current_user.id):
        flash("You can edit only your own tours.")
        return redirect(url_for("guide_dashboard"))

    if tour_has_reservations(tour_id):
        flash("This tour cannot be edited because it already has reservations.")
        return redirect(url_for("guide_dashboard"))

    current_photos = get_current_tour_photos(tour_id)

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        selected_languages = request.form.getlist("languages")
        languages = " / ".join(selected_languages)
        main_language = request.form.get("main_language", "").strip()
        duration_input = request.form.get("duration", "").strip()
        distance_input = request.form.get("distance", "").strip()
        meeting_point = request.form.get("meeting_point", "").strip()
        description = request.form.get("description", "").strip()
        children_allowed = request.form.get("children_allowed", "Yes").strip()
        pets_allowed = request.form.get("pets_allowed", "Yes, on leash").strip()
        what_to_bring = request.form.get("what_to_bring", "").strip()
        photo_files = read_tour_photo_files()

        # The database connection is not open yet at this point, so these
        # early validation returns do not need to close any connection.
        new_photo_count = count_uploaded_photo_files(photo_files)

        if new_photo_count == 0 and len(current_photos) < 5:
            flash("This tour must have 5 promotional photos. Please upload 5 photos.")
            return render_template("edit_tour.html", tour=tour, current_photos=current_photos)

        if new_photo_count > 0 and new_photo_count != 5:
            flash("To replace tour photos, please upload exactly 5 new promotional photos.")
            return render_template("edit_tour.html", tour=tour, current_photos=current_photos)

        if new_photo_count > 0 and not uploaded_photo_extensions_are_valid(photo_files):
            flash("Tour photos must be jpg, jpeg, png, or webp files.")
            return render_template("edit_tour.html", tour=tour, current_photos=current_photos)

        connection = get_db_connection()
        reservation = connection.execute(
            """
            SELECT id
            FROM reservations
            WHERE tour_id = ? AND status != 'Cancelled'
            LIMIT 1
            """,
            (tour_id,)
        ).fetchone()

        if reservation is not None:
            connection.close()
            flash("This tour cannot be edited because it already has reservations.")
            return redirect(url_for("guide_dashboard"))
        else:
            if (
                title == ""
                or main_language == ""
                or duration_input == ""
                or meeting_point == ""
                or description == ""):
                
                connection.close()
                flash("Please fill in all required tour fields.")
                return render_template("edit_tour.html", tour=tour, current_photos=current_photos)

            try:
                duration_minutes = int(duration_input)
            except ValueError:
                connection.close()
                flash("Duration must be a whole number of minutes.")
                return render_template("edit_tour.html", tour=tour, current_photos=current_photos)

            if duration_minutes <= 0:
                connection.close()
                flash("Duration must be at least 1 minute.")
                return render_template("edit_tour.html", tour=tour, current_photos=current_photos)

            duration = str(duration_minutes) + " min"

            distance = ""
            if distance_input != "":
                try:
                    distance_number = float(distance_input)
                except ValueError:
                    connection.close()
                    flash("Distance must be a number.")
                    return render_template("edit_tour.html", tour=tour, current_photos=current_photos)

                if distance_number < 0:
                    connection.close()
                    flash("Distance cannot be negative.")
                    return render_template("edit_tour.html", tour=tour, current_photos=current_photos)


                if distance_number == int(distance_number):
                    distance = str(int(distance_number)) + " km"
                else:
                    distance = str(distance_number) + " km"

            if what_to_bring != "":
                notes = what_to_bring
            else:
                notes = tour["notes"] or "Created by guide."

            if languages == "":
                languages = main_language

            if main_language not in split_languages(languages):
                languages = main_language + " / " + languages

            # schedule_error only reports invalid input; overlap is checked separately below.
            schedules, schedule_error = read_schedule_rows_from_form()

            if schedule_error != "":
                connection.close()
                flash(schedule_error)
                return render_template("edit_tour.html", tour=tour, current_photos=current_photos)

            if schedules_overlap_with_each_other(schedules, duration_minutes):
                connection.close()
                flash("The weekly schedule rows overlap with each other.")
                return render_template("edit_tour.html", tour=tour, current_photos=current_photos)

            stops = []
            for index in range(1, 5):
                stop_name = request.form.get("stop_" + str(index), "").strip()
                stops.append(stop_name)

            valid_stop_count = 0
            for x in stops:
                if x != "":
                    valid_stop_count = valid_stop_count + 1

            if valid_stop_count < 4:
                connection.close()
                flash("Please keep at least four route points for the tour.")
                return render_template("edit_tour.html", tour=tour, current_photos=current_photos)

            if not tour_languages_allowed_for_guide(connection, int(current_user.id), languages):
                connection.close()
                flash("Tour languages must be among the languages selected during guide registration.")
                return render_template("edit_tour.html", tour=tour, current_photos=current_photos)

            if guide_has_schedule_overlap(connection, int(current_user.id), schedules, duration_minutes, tour_id_to_ignore=tour_id):
                connection.close()
                flash("This weekly schedule overlaps with another tour created by this guide.")
                return render_template("edit_tour.html", tour=tour, current_photos=current_photos)

            connection.execute(
                """
                UPDATE tours
                SET title = ?, languages = ?, language = ?, duration = ?,
                    duration_minutes = ?, distance = ?, meeting_point = ?,
                    description = ?, price = ?, children_allowed = ?,
                    pets_allowed = ?, notes = ?
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
                    "Free / Tip-based",
                    children_allowed,
                    pets_allowed,
                    notes,
                    tour_id
                )
            )

            photos_saved = save_tour_photos(connection, tour_id, photo_files, old_main_image=tour["image"])

            if not photos_saved:
                connection.rollback()
                connection.close()
                flash("Please upload 5 valid promotional photos for the tour.")
                return render_template("edit_tour.html", tour=tour, current_photos=current_photos)

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

            for x in schedules:
                connection.execute(
                    """
                    INSERT INTO tour_schedules (tour_id, weekday, start_time)
                    VALUES (?, ?, ?)
                    """,
                    (tour_id, x["weekday"], x["start_time"])
                )

            create_dates_for_schedules(connection, tour_id, schedules)

        connection.commit()
        connection.close()

        flash("Tour updated in the database.")

        return redirect(url_for("guide_dashboard"))

    return render_template("edit_tour.html", tour=tour, current_photos=current_photos)


@login_required
def completed_tours():
    role_redirect = require_role("Guide")

    if role_redirect is not None:
        return role_redirect

    guide_id = int(current_user.id)

    if request.method == "POST":
        # The guide selects a tour date from a dropdown rather than typing a tour id.
        tour_date_id = request.form.get("tour_date_id", "").strip()
        actual_participants_count = request.form.get("actual_participants_count", "").strip()
        notes = request.form.get("notes", "").strip()
        evidence_photo = request.files.get("evidence_photo")

        if tour_date_id == "" or actual_participants_count == "":
            flash("Please select a tour date and enter actual participants.")
            return redirect(url_for("completed_tours"))

        if evidence_photo is None or evidence_photo.filename == "":
            flash("Please upload one evidence photo for the completed tour.")
            return redirect(url_for("completed_tours"))

        try:
            participant_number = int(actual_participants_count)
        except ValueError:
            flash("Actual participants must be a valid number.")
            return redirect(url_for("completed_tours"))

        if participant_number < 0:
            flash("Actual participants cannot be negative.")
            return redirect(url_for("completed_tours"))

        connection = get_db_connection()

        error_message = "You can report only past tour dates from your own tours that had reservations and were not already reported."

        # Each tour date has a unique id; a tour cannot have two start times on the same day.
        tour_date_row = connection.execute("SELECT * FROM tour_dates WHERE id = ?", (tour_date_id,)).fetchone()

        if tour_date_row is None:
            connection.close()
            flash(error_message)
            return redirect(url_for("completed_tours"))

        tour_id = tour_date_row["tour_id"]
        tour_date = tour_date_row["tour_date"]
        tour_time = tour_date_row["tour_time"]

        tour_row = connection.execute("SELECT * FROM tours WHERE id = ?",(tour_id,)).fetchone()

        # A guide can report only their own tours.
        if tour_row is None or tour_row["guide_id"] != guide_id:
            connection.close()
            flash(error_message)
            return redirect(url_for("completed_tours"))

        # Only past tour dates can be reported.
        today_string = date.today().strftime("%Y-%m-%d")
        now = datetime.now()
        current_time_minutes = now.hour * 60 + now.minute
        tour_time_minutes = get_time_minutes(tour_time)

        is_past_tour = False
        if tour_time_minutes is not None:
            if tour_date < today_string:
                is_past_tour = True
            elif tour_date == today_string and tour_time_minutes < current_time_minutes:
                is_past_tour = True

        if not is_past_tour:
            connection.close()
            flash(error_message)
            return redirect(url_for("completed_tours"))

        # A tour date can be reported only once.
        already_reported = connection.execute(
            "SELECT * FROM completed_tours WHERE tour_id = ? AND tour_date = ?",(tour_id, tour_date)).fetchone()

        if already_reported is not None:
            connection.close()
            flash(error_message)
            return redirect(url_for("completed_tours"))

        # A tour date can be reported only if it had at least one active reservation.
        reservations = connection.execute(
            """
            SELECT * FROM reservations
            WHERE tour_id = ?
              AND selected_date = ?
              AND selected_time = ?
              AND status != 'Cancelled'
            """,
            (tour_id, tour_date, tour_time)
        ).fetchall()

        if len(reservations) == 0:
            connection.close()
            flash(error_message)
            return redirect(url_for("completed_tours"))

        # Actual participants cannot exceed the number expected from reservations.
        expected_participants = 0
        for x in reservations:
            extra = x["extra_people_count"]
            if extra is None:
                extra = 0
            expected_participants = expected_participants + 1 + extra

        if participant_number > expected_participants:
            connection.close()
            flash("Actual participants cannot be greater than expected participants.")
            return redirect(url_for("completed_tours"))

        tour_date_compact = tour_date.replace("-", "")
        evidence_path = save_uploaded_file(evidence_photo, "completed_" + str(tour_id) + "_" + tour_date_compact, guide_id)

        if evidence_path == "":
            connection.close()
            flash("Please upload a valid evidence photo.")
            return redirect(url_for("completed_tours"))

        report_date = date.today().isoformat()

        connection.execute(
            """
            INSERT INTO completed_tours (
                tour_id, guide_id, completed_date, tour_date,
                actual_participants_count, evidence_photo_path, notes
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                tour_id,
                guide_id,
                report_date,
                tour_date,
                participant_number,
                evidence_path,
                notes
            )
        )
        connection.commit()
        connection.close()

        flash("Completed tour report saved.")
        return redirect(url_for("completed_tours"))


    # GET request: show reported tours and the dates still available to report.
    completed = get_completed_tours_for_guide(guide_id)

    connection = get_db_connection()

    # Load all tour dates that belong to this guide.
    all_tour_dates = connection.execute(
        """
        SELECT tour_dates.id AS tour_date_id,
               tours.id AS tour_id,
               tours.title AS title,
               tour_dates.tour_date AS tour_date,
               tour_dates.tour_time AS tour_time
        FROM tour_dates
        JOIN tours ON tours.id = tour_dates.tour_id
        WHERE tours.guide_id = ?
        ORDER BY tour_dates.tour_date DESC, tour_dates.tour_time DESC
        """,
        (guide_id,)).fetchall()

    today = date.today()
    today_string = today.strftime("%Y-%m-%d")
    now = datetime.now()
    current_time_minutes = now.hour * 60 + now.minute

    reportable_dates = []

    for x in all_tour_dates:
        tour_id = x["tour_id"]
        tour_date = x["tour_date"]
        tour_time = x["tour_time"]

        # Only past tour dates can be reported.
        tour_time_minutes = get_time_minutes(tour_time)
        if tour_time_minutes is None:
            continue

        is_past_tour = False
        if tour_date < today_string:
            is_past_tour = True
        elif tour_date == today_string and tour_time_minutes < current_time_minutes:
            is_past_tour = True

        if not is_past_tour:
            continue

        # Skip dates that were already reported.
        already_reported = connection.execute(
            "SELECT * FROM completed_tours WHERE tour_id = ? AND tour_date = ?",
            (tour_id, tour_date)
        ).fetchone()
        if already_reported is not None:
            continue

        # Skip dates that had no active reservations.
        reservations = connection.execute(
            """
            SELECT * FROM reservations
            WHERE tour_id = ?
              AND selected_date = ?
              AND selected_time = ?
              AND status != 'Cancelled'
            """,
            (tour_id, tour_date, tour_time)
        ).fetchall()

        if len(reservations) == 0:
            continue

        # Count expected participants from the active reservations.
        expected_participants = 0
        for y in reservations:
            extra = y["extra_people_count"]
            if extra is None:
                extra = 0
            expected_participants = expected_participants + 1 + extra

        reportable_dates.append({
            "tour_date_id": x["tour_date_id"],
            "tour_id": tour_id,
            "title": x["title"],
            "tour_date": tour_date,
            "tour_time": tour_time,
            "expected_participants": expected_participants,
        })

    connection.close()

    return render_template("completed_tours.html",completed_tours=completed,reportable_dates=reportable_dates)

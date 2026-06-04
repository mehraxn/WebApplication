from datetime import date, timedelta
from pathlib import Path

from flask import abort, current_app, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from auth import require_role
from database import get_db_connection
from models import get_current_user
from tours import calculate_rating, full_star_count, get_tour_by_id


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
        result.append({
            "id": item_dict["id"],
            "date": item_dict["completed_date"],
            "participants": item_dict["participants_count"],
            "tips": "Tip-based",
            "status": "Reported",
            "tour": {
                "id": item_dict["tour_id"],
                "title": item_dict["title"],
                "image": item_dict["image"],
                "meeting_point": item_dict["meeting_point"]
            }
        })

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
        tour_reservations = connection.execute(
            """
            SELECT selected_date, selected_time,
                   COUNT(*) AS reservations_count,
                   COALESCE(SUM(1 + COALESCE(extra_people_count, extra_people, 0)), 0) AS expected_participants
            FROM reservations
            WHERE tour_id = ? AND status != 'Cancelled'
            GROUP BY selected_date, selected_time
            ORDER BY selected_date, selected_time
            """,
            (tour_dict["id"],)
        ).fetchall()
        tour_dict["reservation_summaries"] = [dict(item) for item in tour_reservations]
        upcoming_participants += sum(item["expected_participants"] for item in tour_reservations)
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
        start_point = request.form.get("start_point", "Start: Meeting point").strip()
        stop_one = request.form.get("stop_one", "Stop 1").strip()
        stop_two = request.form.get("stop_two", "Stop 2").strip()
        finish_point = request.form.get("finish_point", "Finish: Final point").strip()
        rest_stops = request.form.get("rest_stops", "").strip()
        fitness_level = request.form.get("fitness_level", "Easy").strip()
        path_type = request.form.get("path_type", "Urban walking path").strip()
        mountain_path = request.form.get("mountain_path", "No").strip()
        children_allowed = request.form.get("children_allowed", "Yes").strip()
        pets_allowed = request.form.get("pets_allowed", "Yes, on leash").strip()
        what_to_bring = request.form.get("what_to_bring", "").strip()

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

        guide_id = int(current_user.id)

        connection = get_db_connection()
        cursor = connection.execute(
            """
            INSERT INTO tours (
                guide_id, title, description, image, languages, duration, distance,
                price, meeting_point, max_participants, fitness_level, path_type,
                mountain_path, pets_allowed, children_allowed, accessibility, notes
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                guide_id,
                title,
                description,
                "images/places/griffith-observatory.jpg",
                languages,
                duration,
                distance,
                "Free / Tip-based",
                meeting_point,
                int(max_participants or 15),
                fitness_level,
                path_type,
                mountain_path,
                pets_allowed,
                children_allowed,
                "Accessibility information not added yet.",
                what_to_bring or rest_stops or "Created by guide."
            )
        )

        tour_id = cursor.lastrowid

        stops = [start_point, stop_one, stop_two, finish_point]

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

        today = date.today()
        for days_ahead in [7, 14, 21]:
            future_date = today + timedelta(days=days_ahead)
            connection.execute(
                """
                INSERT INTO tour_dates (tour_id, tour_date, tour_time)
                VALUES (?, ?, ?)
                """,
                (tour_id, future_date.isoformat(), "10:00")
            )

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
        abort(404)

    if tour["guide_id"] != int(current_user.id):
        abort(403)

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        languages = request.form.get("languages", "").strip()
        duration = request.form.get("duration", "").strip()
        distance = request.form.get("distance", "").strip()
        meeting_point = request.form.get("meeting_point", "").strip()
        description = request.form.get("description", "").strip()

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
            connection.execute(
                """
                UPDATE tours
                SET title = ?, languages = ?, language = ?, duration = ?, distance = ?,
                    meeting_point = ?, description = ?
                WHERE id = ?
                """,
                (title, languages, languages.split("/")[0].strip() if languages else "", duration, distance, meeting_point, description, tour_id)
            )

            connection.execute(
                "DELETE FROM tour_stops WHERE tour_id = ?",
                (tour_id,)
            )

            for index in range(1, 5):
                stop_name = request.form.get(f"stop_{index}", "").strip()

                if stop_name:
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

        evidence_path = ""
        if evidence_photo and evidence_photo.filename:
            extension = evidence_photo.filename.rsplit(".", 1)[-1].lower()
            if extension not in ["jpg", "jpeg", "png", "webp"]:
                flash("Evidence photo must be JPG, PNG, or WEBP.")
                return redirect(url_for("completed_tours"))
            filename = f"completed_{tour_id}_{tour_date.replace('-', '')}.{extension}"
            save_path = Path(current_app.root_path) / current_app.config["UPLOAD_FOLDER"] / filename
            evidence_photo.save(save_path)
            evidence_path = f"uploads/{filename}"

        connection = get_db_connection()
        owns_tour = connection.execute(
            "SELECT id FROM tours WHERE id = ? AND guide_id = ?",
            (tour_id, guide_id)
        ).fetchone()
        if owns_tour is None:
            connection.close()
            abort(403)

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
                int(actual_participants_count or 0),
                int(actual_participants_count or 0),
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
    reportable_dates = connection.execute(
        """
        SELECT tours.id AS tour_id, tours.title, reservations.selected_date AS tour_date,
               reservations.selected_time AS tour_time,
               COALESCE(SUM(1 + COALESCE(reservations.extra_people_count, reservations.extra_people, 0)), 0) AS expected_participants
        FROM reservations
        JOIN tours ON tours.id = reservations.tour_id
        WHERE tours.guide_id = ?
          AND reservations.status != 'Cancelled'
          AND datetime(reservations.selected_date || ' ' || reservations.selected_time) < datetime('now')
        GROUP BY tours.id, reservations.selected_date, reservations.selected_time
        ORDER BY reservations.selected_date DESC
        """,
        (guide_id,)
    ).fetchall()
    connection.close()

    return render_template(
        "completed_tours.html",
        completed_tours=completed,
        reportable_dates=[dict(item) for item in reportable_dates]
    )

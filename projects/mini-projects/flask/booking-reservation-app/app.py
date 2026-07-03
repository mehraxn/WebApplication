"""Booking Reservation App — a small Flask application for reserving seats at
events/services, with capacity checks, date validation, and SQLite storage.

Uses Flask + sqlite3 only (no SQLAlchemy, no Flask-WTF).
"""
import re
from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for, flash, abort

import database

app = Flask(__name__)
app.secret_key = "dev-secret-key"  # required for flash messages

database.init_db()

# A simple email pattern — good enough for basic validation
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def is_past(date_str):
    """True if the given YYYY-MM-DD date is before today."""
    try:
        service_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return False
    return service_date < datetime.now().date()


@app.route("/")
def index():
    services = database.get_services()
    # Build a small list with availability info for each service
    items = []
    for s in services:
        items.append(
            {
                "service": s,
                "available": database.seats_available(s["id"]),
                "past": is_past(s["date"]),
            }
        )
    return render_template("index.html", items=items)


@app.route("/service/<int:service_id>")
def service_detail(service_id):
    service = database.get_service(service_id)
    if service is None:
        abort(404)
    available = database.seats_available(service_id)
    return render_template(
        "service_detail.html",
        service=service,
        available=available,
        past=is_past(service["date"]),
    )


@app.route("/reserve/<int:service_id>", methods=["GET", "POST"])
def reserve(service_id):
    service = database.get_service(service_id)
    if service is None:
        abort(404)

    available = database.seats_available(service_id)

    # Can't reserve for a past event
    if is_past(service["date"]):
        flash("This event has already passed and can no longer be booked.", "danger")
        return redirect(url_for("service_detail", service_id=service_id))

    if request.method == "POST":
        name = request.form.get("customer_name", "").strip()
        email = request.form.get("customer_email", "").strip()
        seats_raw = request.form.get("seats", "").strip()

        # ---- Back-end validation ----
        if not name:
            flash("Name is required.", "danger")
        elif not EMAIL_RE.match(email):
            flash("Please enter a valid email address.", "danger")
        elif not seats_raw.isdigit() or int(seats_raw) < 1:
            flash("Seats must be a positive whole number.", "danger")
        elif int(seats_raw) > available:
            flash(f"Only {available} seat(s) left for this event.", "danger")
        else:
            database.add_reservation(service_id, name, email, int(seats_raw))
            flash("Reservation confirmed!", "success")
            return redirect(url_for("reservations"))

        # On any validation error, re-show the form keeping the input
        return render_template(
            "reserve.html",
            service=service,
            available=available,
            name=name,
            email=email,
            seats=seats_raw,
        )

    # GET: show the empty reservation form
    return render_template("reserve.html", service=service, available=available)


@app.route("/reservations")
def reservations():
    all_reservations = database.get_reservations()
    return render_template("reservations.html", reservations=all_reservations)


@app.route("/reservations/cancel/<int:reservation_id>", methods=["POST"])
def cancel_reservation(reservation_id):
    reservation = database.get_reservation(reservation_id)
    if reservation is None:
        abort(404)
    database.delete_reservation(reservation_id)
    flash("Reservation cancelled.", "success")
    return redirect(url_for("reservations"))


@app.errorhandler(404)
def not_found(error):
    return render_template("error.html", message="Page or item not found."), 404


if __name__ == "__main__":
    app.run(debug=True)

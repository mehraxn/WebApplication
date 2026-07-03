"""All SQLite database functions for the Booking Reservation App.

Kept separate from app.py so routes stay clean. Uses only the standard-library
sqlite3 module.
"""
import sqlite3
from datetime import datetime

DB_NAME = "booking.db"


def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row  # access columns by name
    return conn


def init_db():
    """Create the tables and seed a few sample services on first run."""
    conn = get_connection()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS services (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            date TEXT NOT NULL,
            time TEXT NOT NULL,
            capacity INTEGER NOT NULL
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS reservations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            service_id INTEGER NOT NULL,
            customer_name TEXT NOT NULL,
            customer_email TEXT NOT NULL,
            seats INTEGER NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY (service_id) REFERENCES services (id)
        )
        """
    )

    # Seed sample services only if the table is empty
    count = conn.execute("SELECT COUNT(*) FROM services").fetchone()[0]
    if count == 0:
        conn.executemany(
            "INSERT INTO services (name, description, date, time, capacity) "
            "VALUES (?, ?, ?, ?, ?)",
            [
                ("Yoga Class", "A relaxing beginner-friendly yoga session.", "2026-12-01", "09:00", 15),
                ("Cooking Workshop", "Learn to cook a three-course Italian meal.", "2026-12-05", "18:30", 10),
                ("Guided City Tour", "A two-hour walking tour of the old town.", "2026-12-10", "14:00", 20),
                ("Live Jazz Night", "An evening of live jazz with local musicians.", "2026-12-15", "20:00", 40),
            ],
        )
    conn.commit()
    conn.close()


# ---- SERVICES ----
def get_services():
    conn = get_connection()
    services = conn.execute("SELECT * FROM services ORDER BY date, time").fetchall()
    conn.close()
    return services


def get_service(service_id):
    conn = get_connection()
    service = conn.execute(
        "SELECT * FROM services WHERE id = ?", (service_id,)
    ).fetchone()
    conn.close()
    return service


def seats_reserved(service_id):
    """Total seats already reserved for a service."""
    conn = get_connection()
    row = conn.execute(
        "SELECT COALESCE(SUM(seats), 0) AS total FROM reservations WHERE service_id = ?",
        (service_id,),
    ).fetchone()
    conn.close()
    return row["total"]


def seats_available(service_id):
    """Capacity minus seats already reserved."""
    service = get_service(service_id)
    if service is None:
        return 0
    return service["capacity"] - seats_reserved(service_id)


# ---- RESERVATIONS ----
def add_reservation(service_id, customer_name, customer_email, seats):
    conn = get_connection()
    conn.execute(
        "INSERT INTO reservations (service_id, customer_name, customer_email, seats, created_at) "
        "VALUES (?, ?, ?, ?, ?)",
        (service_id, customer_name, customer_email, seats, datetime.now().strftime("%Y-%m-%d %H:%M")),
    )
    conn.commit()
    conn.close()


def get_reservations():
    """All reservations, joined with their service name/date for display."""
    conn = get_connection()
    reservations = conn.execute(
        """
        SELECT r.*, s.name AS service_name, s.date AS service_date, s.time AS service_time
        FROM reservations r
        JOIN services s ON r.service_id = s.id
        ORDER BY r.id DESC
        """
    ).fetchall()
    conn.close()
    return reservations


def get_reservation(reservation_id):
    conn = get_connection()
    reservation = conn.execute(
        "SELECT * FROM reservations WHERE id = ?", (reservation_id,)
    ).fetchone()
    conn.close()
    return reservation


def delete_reservation(reservation_id):
    conn = get_connection()
    conn.execute("DELETE FROM reservations WHERE id = ?", (reservation_id,))
    conn.commit()
    conn.close()

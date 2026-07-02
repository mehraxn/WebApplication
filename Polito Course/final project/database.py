import os
import sqlite3

from werkzeug.security import generate_password_hash


# Build an absolute path so the database is found no matter where the app is started from.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, "database.db")


def get_db_connection():
    """Open the database connection and enable foreign keys."""
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def create_base_tables(connection):
    
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            email TEXT NOT NULL,
            role TEXT NOT NULL CHECK(role IN ('Participant', 'Guide', 'Admin')),
            first_name TEXT,
            last_name TEXT,
            password_hash TEXT NOT NULL,
            spoken_languages TEXT,
            created_at TEXT,
            UNIQUE(email, role)
        )
        """
    )

    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS tours (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            guide_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            image TEXT,
            languages TEXT NOT NULL,
            duration TEXT NOT NULL,
            distance TEXT NOT NULL,
            price TEXT DEFAULT 'Free / Tip-based',
            meeting_point TEXT NOT NULL,
            max_participants INTEGER NOT NULL,
            fitness_level TEXT,
            path_type TEXT,
            mountain_path TEXT,
            pets_allowed TEXT,
            children_allowed TEXT,
            accessibility TEXT,
            notes TEXT,
            duration_minutes INTEGER,
            language TEXT,
            created_at TEXT,
            FOREIGN KEY (guide_id) REFERENCES users(id)
        )
        """
    )

    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS tour_stops (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tour_id INTEGER NOT NULL,
            stop_order INTEGER NOT NULL,
            stop_name TEXT NOT NULL,
            stop_type TEXT,
            FOREIGN KEY (tour_id) REFERENCES tours(id)
        )
        """
    )

    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS tour_dates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tour_id INTEGER NOT NULL,
            tour_date TEXT NOT NULL,
            tour_time TEXT NOT NULL,
            FOREIGN KEY (tour_id) REFERENCES tours(id)
        )
        """
    )

    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS tour_schedules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tour_id INTEGER NOT NULL,
            weekday TEXT NOT NULL,
            start_time TEXT NOT NULL,
            UNIQUE(tour_id, weekday),
            FOREIGN KEY (tour_id) REFERENCES tours(id)
        )
        """
    )

    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS tour_photos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tour_id INTEGER NOT NULL,
            photo_path TEXT NOT NULL,
            photo_order INTEGER NOT NULL,
            FOREIGN KEY (tour_id) REFERENCES tours(id)
        )
        """
    )

    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS reservations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tour_id INTEGER NOT NULL,
            participant_id INTEGER NOT NULL,
            selected_date TEXT NOT NULL,
            selected_time TEXT NOT NULL,
            phone_number TEXT,
            message_to_guide TEXT,
            status TEXT DEFAULT 'Pending',
            main_participant_name TEXT,
            extra_people_count INTEGER DEFAULT 0,
            created_at TEXT,
            FOREIGN KEY (tour_id) REFERENCES tours(id),
            FOREIGN KEY (participant_id) REFERENCES users(id)
        )
        """
    )

    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS reservation_extra_people (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            reservation_id INTEGER NOT NULL,
            full_name TEXT NOT NULL,
            FOREIGN KEY (reservation_id) REFERENCES reservations(id)
        )
        """
    )

    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS completed_tours (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tour_id INTEGER NOT NULL,
            guide_id INTEGER NOT NULL,
            completed_date TEXT NOT NULL,
            notes TEXT,
            tour_date TEXT,
            actual_participants_count INTEGER,
            evidence_photo_path TEXT,
            created_at TEXT,
            FOREIGN KEY (tour_id) REFERENCES tours(id),
            FOREIGN KEY (guide_id) REFERENCES users(id)
        )
        """
    )


def insert_sample_users(connection):
    sample_users = [
        ("Maria", "Rossi", "guide1@example.com", "guide123", "Guide", "English, Italian, Spanish"),
        ("Daniel", "Miller", "guide2@example.com", "guide123", "Guide", "English, German, Portuguese"),
        ("Alex", "Johnson", "participant1@example.com", "participant123", "Participant", ""),
        ("Sofia", "Garcia", "participant2@example.com", "participant123", "Participant", ""),
        ("Luca", "Bianchi", "participant3@example.com", "participant123", "Participant", ""),
        ("Nora", "Admin", "admin@example.com", "admin123", "Admin", ""),
    ]

    for first_name, last_name, email, password, role, spoken_languages in sample_users:
        existing = connection.execute(
            "SELECT id FROM users WHERE email = ? AND role = ?",
            (email, role),
        ).fetchone()

        if existing is None:
            connection.execute(
                """
                INSERT INTO users (
                    full_name, first_name, last_name, email,
                    password_hash, role, spoken_languages
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    first_name + " " + last_name,
                    first_name,
                    last_name,
                    email,
                    generate_password_hash(password),
                    role,
                    spoken_languages,
                ),
            )


def initialize_database():
    """Set up the database when the app starts."""
    connection = get_db_connection()

    create_base_tables(connection)
    insert_sample_users(connection)

    connection.commit()
    connection.close()

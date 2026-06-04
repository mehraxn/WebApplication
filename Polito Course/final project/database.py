from pathlib import Path
import sqlite3

from werkzeug.security import generate_password_hash

BASE_DIR = Path(__file__).resolve().parent
DATABASE = BASE_DIR / "database.db"


def get_db_connection():
    """Open a connection to database.db and return rows like dictionaries."""
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def table_columns(connection, table_name):
    return [row["name"] for row in connection.execute(f"PRAGMA table_info({table_name})").fetchall()]


def add_column_if_missing(connection, table_name, column_name, column_sql):
    if column_name not in table_columns(connection, table_name):
        connection.execute(f"ALTER TABLE {table_name} ADD COLUMN {column_sql}")

def migrate_users_unique_email_role(connection):
    """Allow the same email once as Participant and once as Guide.

    The first version of the project had users.email as UNIQUE, which meant
    one email could only have one account.  The professor's requirement allows
    the same email to be registered with different roles, so the uniqueness rule
    must be changed to the pair (email, role).
    """
    table_info = connection.execute(
        "SELECT sql FROM sqlite_master WHERE type = 'table' AND name = 'users'"
    ).fetchone()

    if table_info is None:
        return

    table_sql = table_info["sql"] or ""

    compact_table_sql = table_sql.replace(" ", "")

    if "UNIQUE(email,role)" in compact_table_sql:
        return

    connection.execute("PRAGMA foreign_keys = OFF")

    connection.execute(
        """
        CREATE TABLE users_new (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            email TEXT NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL CHECK(role IN ('Participant', 'Guide')),
            first_name TEXT,
            last_name TEXT,
            password_hash TEXT,
            spoken_languages TEXT,
            created_at TEXT,
            UNIQUE(email, role)
        )
        """
    )

    existing_columns = table_columns(connection, "users")
    desired_columns = [
        "id", "full_name", "email", "password", "role", "first_name",
        "last_name", "password_hash", "spoken_languages", "created_at"
    ]
    copied_columns = [column for column in desired_columns if column in existing_columns]
    column_list = ", ".join(copied_columns)

    connection.execute(
        f"INSERT INTO users_new ({column_list}) SELECT {column_list} FROM users"
    )
    connection.execute("DROP TABLE users")
    connection.execute("ALTER TABLE users_new RENAME TO users")
    connection.execute("PRAGMA foreign_keys = ON")


def initialize_database():
    connection = get_db_connection()

    migrate_users_unique_email_role(connection)

    add_column_if_missing(connection, "users", "first_name", "first_name TEXT")
    add_column_if_missing(connection, "users", "last_name", "last_name TEXT")
    add_column_if_missing(connection, "users", "password_hash", "password_hash TEXT")
    add_column_if_missing(connection, "users", "spoken_languages", "spoken_languages TEXT")
    add_column_if_missing(connection, "users", "created_at", "created_at TEXT")

    add_column_if_missing(connection, "tours", "duration_minutes", "duration_minutes INTEGER")
    add_column_if_missing(connection, "tours", "language", "language TEXT")
    add_column_if_missing(connection, "tours", "created_at", "created_at TEXT")

    add_column_if_missing(connection, "reservations", "main_participant_name", "main_participant_name TEXT")
    add_column_if_missing(connection, "reservations", "extra_people_count", "extra_people_count INTEGER DEFAULT 0")
    add_column_if_missing(connection, "reservations", "created_at", "created_at TEXT")

    add_column_if_missing(connection, "reviews", "created_at", "created_at TEXT")

    add_column_if_missing(connection, "completed_tours", "tour_date", "tour_date TEXT")
    add_column_if_missing(connection, "completed_tours", "actual_participants_count", "actual_participants_count INTEGER")
    add_column_if_missing(connection, "completed_tours", "evidence_photo_path", "evidence_photo_path TEXT")
    add_column_if_missing(connection, "completed_tours", "created_at", "created_at TEXT")

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
        CREATE TABLE IF NOT EXISTS reservation_extra_people (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            reservation_id INTEGER NOT NULL,
            full_name TEXT NOT NULL,
            FOREIGN KEY (reservation_id) REFERENCES reservations(id)
        )
        """
    )

    users = connection.execute("SELECT * FROM users").fetchall()
    for user in users:
        full_name = user["full_name"]
        name_parts = full_name.split(" ", 1)
        first_name = user["first_name"] or name_parts[0]
        last_name = user["last_name"] or (name_parts[1] if len(name_parts) > 1 else "")
        password_hash = user["password_hash"]
        if not password_hash:
            password_hash = generate_password_hash(user["password"])
        spoken_languages = user["spoken_languages"] or ("English, Italian, Spanish" if user["role"] == "Guide" else "")
        connection.execute(
            """
            UPDATE users
            SET first_name = ?, last_name = ?, password_hash = ?, spoken_languages = ?
            WHERE id = ?
            """,
            (first_name, last_name, password_hash, spoken_languages, user["id"])
        )

    sample_users = [
        ("Maria", "Rossi", "guide1@example.com", "guide123", "Guide", "English, Italian, Spanish"),
        ("Daniel", "Miller", "guide2@example.com", "guide123", "Guide", "English, German, Portuguese"),
        ("Alex", "Johnson", "participant1@example.com", "participant123", "Participant", ""),
        ("Sofia", "Garcia", "participant2@example.com", "participant123", "Participant", ""),
        ("Luca", "Bianchi", "participant3@example.com", "participant123", "Participant", "")
    ]
    for first_name, last_name, email, password, role, spoken_languages in sample_users:
        existing = connection.execute("SELECT id FROM users WHERE email = ? AND role = ?", (email, role)).fetchone()
        if existing is None:
            connection.execute(
                """
                INSERT INTO users (
                    full_name, first_name, last_name, email, password, password_hash, role, spoken_languages
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    f"{first_name} {last_name}",
                    first_name,
                    last_name,
                    email,
                    password,
                    generate_password_hash(password),
                    role,
                    spoken_languages
                )
            )

    tours = connection.execute("SELECT * FROM tours ORDER BY id").fetchall()
    fallback_photos = [
        "images/places/griffith-observatory.jpg",
        "images/places/hollywood-walk-of-fame.jpg",
        "images/places/grand-central-market.jpg",
        "images/places/santa-monica-pier.jpg",
        "images/places/venice-boardwalk.jpg"
    ]

    for tour in tours:
        language = tour["language"] or (tour["languages"].split("/")[0].strip() if tour["languages"] else "English")
        duration_digits = "".join(ch for ch in tour["duration"] if ch.isdigit())
        duration_minutes = tour["duration_minutes"] or int(duration_digits or 90)
        connection.execute(
            "UPDATE tours SET language = ?, duration_minutes = ? WHERE id = ?",
            (language, duration_minutes, tour["id"])
        )

        dates = connection.execute(
            "SELECT tour_date, tour_time FROM tour_dates WHERE tour_id = ? ORDER BY tour_date, tour_time",
            (tour["id"],)
        ).fetchall()
        for item in dates:
            try:
                from datetime import datetime
                weekday = datetime.strptime(item["tour_date"], "%Y-%m-%d").strftime("%A")
            except ValueError:
                continue
            connection.execute(
                """
                INSERT OR IGNORE INTO tour_schedules (tour_id, weekday, start_time)
                VALUES (?, ?, ?)
                """,
                (tour["id"], weekday, item["tour_time"])
            )

        photo_count = connection.execute(
            "SELECT COUNT(*) AS count FROM tour_photos WHERE tour_id = ?",
            (tour["id"],)
        ).fetchone()["count"]
        if photo_count < 5:
            connection.execute("DELETE FROM tour_photos WHERE tour_id = ?", (tour["id"],))
            tour_main_image = tour["image"] or fallback_photos[0]
            photos = [tour_main_image] + [photo for photo in fallback_photos if photo != tour_main_image]
            while len(photos) < 5:
                photos.append(fallback_photos[len(photos) % len(fallback_photos)])
            for index, photo_path in enumerate(photos[:5], start=1):
                connection.execute(
                    """
                    INSERT INTO tour_photos (tour_id, photo_path, photo_order)
                    VALUES (?, ?, ?)
                    """,
                    (tour["id"], photo_path, index)
                )

    connection.commit()
    connection.close()

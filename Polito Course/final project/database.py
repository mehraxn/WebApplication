import sqlite3

from datetime import date, datetime
from werkzeug.security import generate_password_hash


DATABASE = "database.db"


WEEKDAYS = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday"
]


def get_db_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def table_columns(connection, table_name):
    rows = connection.execute(f"PRAGMA table_info({table_name})").fetchall()
    column_names = []

    for row in rows:
        column_names.append(row["name"])

    return column_names


def add_column_if_missing(connection, table_name, column_name, column_sql):
    columns = table_columns(connection, table_name)

    if column_name not in columns:
        connection.execute(f"ALTER TABLE {table_name} ADD COLUMN {column_sql}")


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


def migrate_users_unique_email_role(connection):
    table_info = connection.execute(
        "SELECT sql FROM sqlite_master WHERE type = 'table' AND name = 'users'"
    ).fetchone()

    if table_info is None:
        return

    table_sql = table_info["sql"]
    if table_sql is None:
        table_sql = ""

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
            profile_picture TEXT,
            created_at TEXT,
            UNIQUE(email, role)
        )
        """
    )

    existing_columns = table_columns(connection, "users")
    desired_columns = [
        "id",
        "full_name",
        "email",
        "password",
        "role",
        "first_name",
        "last_name",
        "password_hash",
        "spoken_languages",
        "profile_picture",
        "created_at"
    ]

    copied_columns = []
    for column in desired_columns:
        if column in existing_columns:
            copied_columns.append(column)

    column_list = ", ".join(copied_columns)

    connection.execute(
        f"INSERT INTO users_new ({column_list}) SELECT {column_list} FROM users"
    )
    connection.execute("DROP TABLE users")
    connection.execute("ALTER TABLE users_new RENAME TO users")
    connection.execute("PRAGMA foreign_keys = ON")


def update_existing_users(connection):
    users = connection.execute("SELECT * FROM users").fetchall()

    for user in users:
        full_name = user["full_name"]
        name_parts = full_name.split(" ", 1)

        first_name = user["first_name"]
        if not first_name:
            first_name = name_parts[0]

        last_name = user["last_name"]
        if not last_name:
            if len(name_parts) > 1:
                last_name = name_parts[1]
            else:
                last_name = ""

        password_hash = user["password_hash"]
        if not password_hash:
            password_hash = generate_password_hash(user["password"])

        spoken_languages = user["spoken_languages"]
        if not spoken_languages:
            if user["role"] == "Guide":
                spoken_languages = "English, Italian, Spanish"
            else:
                spoken_languages = ""

        profile_picture = ""
        if "profile_picture" in user.keys():
            profile_picture = user["profile_picture"] or ""

        connection.execute(
            """
            UPDATE users
            SET first_name = ?, last_name = ?, password_hash = ?,
                spoken_languages = ?, profile_picture = ?
            WHERE id = ?
            """,
            (
                first_name,
                last_name,
                password_hash,
                spoken_languages,
                profile_picture,
                user["id"]
            )
        )


def insert_sample_users(connection):
    sample_users = [
        ("Maria", "Rossi", "guide1@example.com", "guide123", "Guide", "English, Italian, Spanish"),
        ("Daniel", "Miller", "guide2@example.com", "guide123", "Guide", "English, German, Portuguese"),
        ("Alex", "Johnson", "participant1@example.com", "participant123", "Participant", ""),
        ("Sofia", "Garcia", "participant2@example.com", "participant123", "Participant", ""),
        ("Luca", "Bianchi", "participant3@example.com", "participant123", "Participant", "")
    ]

    for item in sample_users:
        first_name = item[0]
        last_name = item[1]
        email = item[2]
        password = item[3]
        role = item[4]
        spoken_languages = item[5]

        existing = connection.execute(
            "SELECT id FROM users WHERE email = ? AND role = ?",
            (email, role)
        ).fetchone()

        if existing is None:
            full_name = f"{first_name} {last_name}"
            password_hash = generate_password_hash(password)
            connection.execute(
                """
                INSERT INTO users (
                    full_name, first_name, last_name, email, password,
                    password_hash, role, spoken_languages, profile_picture
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    full_name,
                    first_name,
                    last_name,
                    email,
                    password,
                    password_hash,
                    role,
                    spoken_languages,
                    ""
                )
            )


def read_duration_minutes(duration_text, saved_duration_minutes):
    if saved_duration_minutes:
        return int(saved_duration_minutes)

    duration_digits = ""
    for character in duration_text:
        if character.isdigit():
            duration_digits = duration_digits + character

    if duration_digits:
        return int(duration_digits)

    return 90


def update_tour_basic_fields(connection, tour):
    language = tour["language"]
    if not language:
        if tour["languages"]:
            language = tour["languages"].split("/")[0].strip()
        else:
            language = "English"

    duration_minutes = read_duration_minutes(tour["duration"], tour["duration_minutes"])

    connection.execute(
        """
        UPDATE tours
        SET language = ?, duration_minutes = ?, price = ?
        WHERE id = ?
        """,
        (language, duration_minutes, "Walking tour", tour["id"])
    )


def update_tour_schedules(connection, tour):
    schedule_count = connection.execute(
        "SELECT COUNT(*) AS count FROM tour_schedules WHERE tour_id = ?",
        (tour["id"],)
    ).fetchone()["count"]

    if schedule_count > 0:
        return

    dates = connection.execute(
        "SELECT tour_date, tour_time FROM tour_dates WHERE tour_id = ? ORDER BY tour_date, tour_time",
        (tour["id"],)
    ).fetchall()

    for item in dates:
        try:
            date_object = datetime.strptime(item["tour_date"], "%Y-%m-%d").date()
            weekday = WEEKDAYS[date_object.weekday()]
        except ValueError:
            continue

        connection.execute(
            """
            INSERT OR IGNORE INTO tour_schedules (tour_id, weekday, start_time)
            VALUES (?, ?, ?)
            """,
            (tour["id"], weekday, item["tour_time"])
        )


def update_tour_photos(connection, tour):
    fallback_photos = [
        "images/places/griffith-observatory.jpg",
        "images/places/hollywood-walk-of-fame.jpg",
        "images/places/grand-central-market.jpg",
        "images/places/santa-monica-pier.jpg",
        "images/places/venice-boardwalk.jpg"
    ]

    photo_count = connection.execute(
        "SELECT COUNT(*) AS count FROM tour_photos WHERE tour_id = ?",
        (tour["id"],)
    ).fetchone()["count"]

    if photo_count >= 5:
        return

    connection.execute("DELETE FROM tour_photos WHERE tour_id = ?", (tour["id"],))

    tour_main_image = tour["image"]
    if not tour_main_image:
        tour_main_image = fallback_photos[0]

    photos = []
    photos.append(tour_main_image)

    for photo_path in fallback_photos:
        if photo_path != tour_main_image:
            photos.append(photo_path)

    while len(photos) < 5:
        next_photo_index = len(photos) % len(fallback_photos)
        photos.append(fallback_photos[next_photo_index])

    for index, photo_path in enumerate(photos[:5], start=1):
        connection.execute(
            """
            INSERT INTO tour_photos (tour_id, photo_path, photo_order)
            VALUES (?, ?, ?)
            """,
            (tour["id"], photo_path, index)
        )


def date_matches_weekday(date_object, weekday_name):
    if weekday_name not in WEEKDAYS:
        return False

    weekday_number = WEEKDAYS.index(weekday_name)
    return date_object.weekday() == weekday_number


def extend_tour_dates_from_weekly_schedule(connection, tour_id):
    schedules = connection.execute(
        "SELECT weekday, start_time FROM tour_schedules WHERE tour_id = ?",
        (tour_id,)
    ).fetchall()

    if not schedules:
        return

    today = date.today()

    for day_offset in range(0, 366):
        future_date = add_days_to_date(today, day_offset)

        for schedule in schedules:
            if date_matches_weekday(future_date, schedule["weekday"]):
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
                        (tour_id, future_date.isoformat(), schedule["start_time"])
                    )


def initialize_database():
    connection = get_db_connection()

    migrate_users_unique_email_role(connection)

    add_column_if_missing(connection, "users", "first_name", "first_name TEXT")
    add_column_if_missing(connection, "users", "last_name", "last_name TEXT")
    add_column_if_missing(connection, "users", "password_hash", "password_hash TEXT")
    add_column_if_missing(connection, "users", "spoken_languages", "spoken_languages TEXT")
    add_column_if_missing(connection, "users", "profile_picture", "profile_picture TEXT")
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

    update_existing_users(connection)
    insert_sample_users(connection)

    tours = connection.execute("SELECT * FROM tours ORDER BY id").fetchall()
    for tour in tours:
        update_tour_basic_fields(connection, tour)
        update_tour_schedules(connection, tour)
        update_tour_photos(connection, tour)
        extend_tour_dates_from_weekly_schedule(connection, tour["id"])

    connection.commit()
    connection.close()

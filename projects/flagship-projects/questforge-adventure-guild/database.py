import os
import sqlite3

from werkzeug.security import generate_password_hash


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, "database.db")

ROLE_CAPACITIES = {
    "Warrior": 4,
    "Mage": 3,
    "Healer": 2,
}

# Maps sample quest titles to their local SVG artwork in static/images/.
# Used both when seeding fresh data and when correcting an existing database
# that still holds outdated image_filename values.
SAMPLE_QUEST_IMAGE_FILENAMES = {
    "Crypt of the Silver Flame": "quest-combat.svg",
    "Whispers of the Emerald Path": "quest-exploration.svg",
    "Runes of the Forgotten Gate": "quest-puzzle.svg",
    "Shadow over Raven Keep": "quest-stealth.svg",
    "Trial of the Arcane Star": "quest-magic.svg",
    "Frozen Peak Expedition": "quest-survival.svg",
}


def get_db_connection():
    """Open a SQLite connection and return rows that support name access."""
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def initialize_database():
    """Create the database tables and add the sample records."""
    connection = get_db_connection()

    connection.executescript(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE COLLATE NOCASE,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL
                CHECK (role IN ('Adventurer', 'GuildMaster', 'Admin'))
        );

        CREATE TABLE IF NOT EXISTS quests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            quest_type TEXT NOT NULL
                CHECK (quest_type IN (
                    'Combat', 'Exploration', 'Puzzle',
                    'Stealth', 'Magic', 'Survival'
                )),
            difficulty TEXT NOT NULL
                CHECK (difficulty IN ('Easy', 'Medium', 'Hard', 'Legendary')),
            duration_minutes INTEGER NOT NULL CHECK (duration_minutes > 0),
            description TEXT NOT NULL,
            image_filename TEXT
        );

        CREATE TABLE IF NOT EXISTS quest_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            quest_id INTEGER NOT NULL,
            day_of_week TEXT NOT NULL
                CHECK (day_of_week IN (
                    'Monday', 'Tuesday', 'Wednesday', 'Thursday',
                    'Friday', 'Saturday', 'Sunday'
                )),
            start_time TEXT NOT NULL CHECK (length(start_time) = 5),
            location TEXT NOT NULL
                CHECK (location IN (
                    'Dungeon Hall', 'Enchanted Forest', 'Wizard Tower',
                    'Dragon Cave', 'Mystic Library'
                )),
            FOREIGN KEY (quest_id) REFERENCES quests(id)
        );

        CREATE TABLE IF NOT EXISTS participations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            session_id INTEGER NOT NULL,
            role_category TEXT NOT NULL
                CHECK (role_category IN ('Warrior', 'Mage', 'Healer')),
            places_reserved INTEGER NOT NULL
                CHECK (places_reserved IN (1, 2)),
            created_at TEXT NOT NULL,
            UNIQUE (user_id, session_id),
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (session_id) REFERENCES quest_sessions(id)
        );

        CREATE INDEX IF NOT EXISTS idx_sessions_day_time
            ON quest_sessions(day_of_week, start_time);

        CREATE INDEX IF NOT EXISTS idx_participations_session_role
            ON participations(session_id, role_category);

        CREATE INDEX IF NOT EXISTS idx_participations_user
            ON participations(user_id);

        CREATE TRIGGER IF NOT EXISTS check_capacity_before_insert
        BEFORE INSERT ON participations
        WHEN (
            SELECT COALESCE(SUM(places_reserved), 0)
            FROM participations
            WHERE session_id = NEW.session_id
              AND role_category = NEW.role_category
        ) + NEW.places_reserved >
            CASE NEW.role_category
                WHEN 'Warrior' THEN 4
                WHEN 'Mage' THEN 3
                WHEN 'Healer' THEN 2
            END
        BEGIN
            SELECT RAISE(ABORT, 'Role capacity exceeded for this session');
        END;

        CREATE TRIGGER IF NOT EXISTS check_capacity_before_update
        BEFORE UPDATE OF session_id, role_category, places_reserved ON participations
        WHEN (
            SELECT COALESCE(SUM(places_reserved), 0)
            FROM participations
            WHERE session_id = NEW.session_id
              AND role_category = NEW.role_category
              AND id != OLD.id
        ) + NEW.places_reserved >
            CASE NEW.role_category
                WHEN 'Warrior' THEN 4
                WHEN 'Mage' THEN 3
                WHEN 'Healer' THEN 2
            END
        BEGIN
            SELECT RAISE(ABORT, 'Role capacity exceeded for this session');
        END;
        """
    )

    has_existing_users = connection.execute(
        "SELECT EXISTS(SELECT 1 FROM users) AS has_users"
    ).fetchone()["has_users"]
    connection.commit()
    connection.close()

    update_existing_quest_image_filenames()

    if not has_existing_users:
        seed_sample_data()


def update_existing_quest_image_filenames():
    """Correct outdated image_filename values on already-seeded quest rows.

    When database.db already exists, seed_sample_data() does not run again, so
    sample quests can keep stale filenames (for example the original .jpg names).
    This aligns existing rows with the local SVG artwork by matching quest title.
    """
    connection = get_db_connection()
    for title, image_filename in SAMPLE_QUEST_IMAGE_FILENAMES.items():
        connection.execute(
            """
            UPDATE quests
            SET image_filename = ?
            WHERE title = ? AND image_filename IS NOT ?
            """,
            (image_filename, title, image_filename),
        )
    connection.commit()
    connection.close()


def seed_sample_data():
    """Insert a reusable set of demo users, quests, sessions, and participations."""
    connection = get_db_connection()

    sample_users = [
        ("Aria", "Stormwind", "aria@questforge.example", "Adventurer"),
        ("Borin", "Ironshield", "borin@questforge.example", "Adventurer"),
        ("Lyra", "Moonspell", "lyra@questforge.example", "Adventurer"),
        ("Eldrin", "Oakwarden", "guildmaster@questforge.example", "GuildMaster"),
        ("Celeste", "Starseer", "admin@questforge.example", "Admin"),
    ]

    for first_name, last_name, email, role in sample_users:
        existing_user = connection.execute(
            "SELECT id FROM users WHERE email = ?",
            (email,),
        ).fetchone()

        if existing_user is None:
            connection.execute(
                """
                INSERT INTO users (
                    first_name, last_name, email, password_hash, role
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    first_name,
                    last_name,
                    email,
                    generate_password_hash("password123"),
                    role,
                ),
            )

    sample_quests = [
        (
            "Crypt of the Silver Flame",
            "Combat",
            "Hard",
            120,
            "Defend the ancient crypt and recover the silver flame.",
            "quest-combat.svg",
        ),
        (
            "Whispers of the Emerald Path",
            "Exploration",
            "Easy",
            90,
            "Map a forgotten path through the enchanted woodland.",
            "quest-exploration.svg",
        ),
        (
            "Runes of the Forgotten Gate",
            "Puzzle",
            "Medium",
            75,
            "Decode the runes that seal an abandoned gateway.",
            "quest-puzzle.svg",
        ),
        (
            "Shadow over Raven Keep",
            "Stealth",
            "Hard",
            105,
            "Enter Raven Keep unseen and recover the stolen guild ledger.",
            "quest-stealth.svg",
        ),
        (
            "Trial of the Arcane Star",
            "Magic",
            "Legendary",
            150,
            "Survive a sequence of magical trials beneath the Wizard Tower.",
            "quest-magic.svg",
        ),
        (
            "Frozen Peak Expedition",
            "Survival",
            "Medium",
            180,
            "Cross the frozen ridge and establish a safe mountain camp.",
            "quest-survival.svg",
        ),
    ]

    for quest in sample_quests:
        existing_quest = connection.execute(
            "SELECT id FROM quests WHERE title = ?",
            (quest[0],),
        ).fetchone()

        if existing_quest is None:
            connection.execute(
                """
                INSERT INTO quests (
                    title, quest_type, difficulty, duration_minutes,
                    description, image_filename
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                quest,
            )

    sample_sessions = [
        ("Crypt of the Silver Flame", "Monday", "09:00", "Dungeon Hall"),
        ("Runes of the Forgotten Gate", "Monday", "14:00", "Mystic Library"),
        ("Whispers of the Emerald Path", "Tuesday", "10:00", "Enchanted Forest"),
        ("Trial of the Arcane Star", "Tuesday", "18:00", "Wizard Tower"),
        ("Crypt of the Silver Flame", "Wednesday", "09:00", "Dragon Cave"),
        ("Runes of the Forgotten Gate", "Wednesday", "13:00", "Mystic Library"),
        ("Frozen Peak Expedition", "Thursday", "11:00", "Enchanted Forest"),
        ("Shadow over Raven Keep", "Friday", "16:00", "Dungeon Hall"),
        ("Frozen Peak Expedition", "Saturday", "10:00", "Dragon Cave"),
        ("Trial of the Arcane Star", "Saturday", "15:00", "Wizard Tower"),
        ("Whispers of the Emerald Path", "Sunday", "12:00", "Enchanted Forest"),
    ]

    for quest_title, day, start_time, location in sample_sessions:
        quest_row = connection.execute(
            "SELECT id FROM quests WHERE title = ?",
            (quest_title,),
        ).fetchone()

        existing_session = connection.execute(
            """
            SELECT id
            FROM quest_sessions
            WHERE quest_id = ?
              AND day_of_week = ?
              AND start_time = ?
              AND location = ?
            """,
            (quest_row["id"], day, start_time, location),
        ).fetchone()

        if existing_session is None:
            connection.execute(
                """
                INSERT INTO quest_sessions (
                    quest_id, day_of_week, start_time, location
                )
                VALUES (?, ?, ?, ?)
                """,
                (quest_row["id"], day, start_time, location),
            )

    sample_participations = [
        ("aria@questforge.example", "Monday", "09:00", "Warrior", 1),
        ("borin@questforge.example", "Monday", "09:00", "Warrior", 2),
        ("lyra@questforge.example", "Monday", "09:00", "Healer", 1),
        ("aria@questforge.example", "Monday", "14:00", "Mage", 2),
        ("borin@questforge.example", "Tuesday", "10:00", "Warrior", 1),
        ("lyra@questforge.example", "Tuesday", "18:00", "Mage", 1),
        ("aria@questforge.example", "Wednesday", "09:00", "Healer", 2),
        ("borin@questforge.example", "Friday", "16:00", "Warrior", 1),
    ]

    for email, day, start_time, role_category, places_reserved in sample_participations:
        user_row = connection.execute(
            "SELECT id FROM users WHERE email = ?",
            (email,),
        ).fetchone()
        session_row = connection.execute(
            """
            SELECT id
            FROM quest_sessions
            WHERE day_of_week = ? AND start_time = ?
            ORDER BY id
            LIMIT 1
            """,
            (day, start_time),
        ).fetchone()

        existing_participation = connection.execute(
            """
            SELECT id
            FROM participations
            WHERE user_id = ? AND session_id = ?
            """,
            (user_row["id"], session_row["id"]),
        ).fetchone()

        if existing_participation is None:
            connection.execute(
                """
                INSERT INTO participations (
                    user_id, session_id, role_category,
                    places_reserved, created_at
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    user_row["id"],
                    session_row["id"],
                    role_category,
                    places_reserved,
                    "2026-01-07 10:00:00",
                ),
            )

    connection.commit()
    connection.close()


def get_user_by_id(user_id):
    """Return one user row by ID, or None when the user does not exist."""
    connection = get_db_connection()
    user = connection.execute(
        "SELECT * FROM users WHERE id = ?",
        (user_id,),
    ).fetchone()
    connection.close()
    return user


def get_user_by_email(email):
    """Return one user row by email, or None when the user does not exist."""
    connection = get_db_connection()
    user = connection.execute(
        "SELECT * FROM users WHERE email = ?",
        (email.strip(),),
    ).fetchone()
    connection.close()
    return user

from flask_login import UserMixin

from database import get_db_connection


class User(UserMixin):
    def __init__(self, row):
        self.id = str(row["id"])
        self.first_name = row["first_name"] if "first_name" in row.keys() else ""
        self.last_name = row["last_name"] if "last_name" in row.keys() else ""
        self.full_name = row["full_name"] if "full_name" in row.keys() else f"{self.first_name} {self.last_name}".strip()
        self.email = row["email"]
        self.role = row["role"]
        self.spoken_languages = row["spoken_languages"] if "spoken_languages" in row.keys() else ""


def get_current_user():
    """Return the logged-in user from the session, or None."""
    from flask import session

    user_id = session.get("user_id")

    if not user_id:
        return None

    connection = get_db_connection()
    user = connection.execute(
        "SELECT * FROM users WHERE id = ?",
        (user_id,)
    ).fetchone()
    connection.close()

    return user


def get_first_participant_id():
    """Temporary helper: use the first participant if the user is not logged in yet."""
    connection = get_db_connection()
    user = connection.execute(
        "SELECT id FROM users WHERE role = 'Participant' ORDER BY id LIMIT 1"
    ).fetchone()
    connection.close()

    return user["id"] if user else None


def get_first_guide_id():
    """Temporary helper: use the first guide for guide pages."""
    connection = get_db_connection()
    user = connection.execute(
        "SELECT id FROM users WHERE role = 'Guide' ORDER BY id LIMIT 1"
    ).fetchone()
    connection.close()

    return user["id"] if user else None

from flask import session
from flask_login import UserMixin

from database import get_db_connection


class User(UserMixin):
    def __init__(self, row):
        self.id = str(row["id"])

        if "first_name" in row.keys():
            self.first_name = row["first_name"]
        else:
            self.first_name = ""

        if "last_name" in row.keys():
            self.last_name = row["last_name"]
        else:
            self.last_name = ""

        if "full_name" in row.keys():
            self.full_name = row["full_name"]
        else:
            self.full_name = f"{self.first_name} {self.last_name}".strip()

        self.email = row["email"]
        self.role = row["role"]

        if "spoken_languages" in row.keys():
            self.spoken_languages = row["spoken_languages"]
        else:
            self.spoken_languages = ""

        if "profile_picture" in row.keys():
            self.profile_picture = row["profile_picture"]
        else:
            self.profile_picture = ""


def get_current_user():
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
    connection = get_db_connection()
    user = connection.execute(
        "SELECT id FROM users WHERE role = 'Participant' ORDER BY id LIMIT 1"
    ).fetchone()
    connection.close()

    if user is None:
        return None

    return user["id"]


def get_first_guide_id():
    connection = get_db_connection()
    user = connection.execute(
        "SELECT id FROM users WHERE role = 'Guide' ORDER BY id LIMIT 1"
    ).fetchone()
    connection.close()

    if user is None:
        return None

    return user["id"]

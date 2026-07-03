from flask_login import UserMixin


class User(UserMixin):
    """Small Flask-Login user wrapper around a SQLite row."""

    def __init__(self, row):
        self.id = str(row["id"])
        self.first_name = row["first_name"]
        self.last_name = row["last_name"]
        self.full_name = f"{self.first_name} {self.last_name}"
        self.email = row["email"]
        self.role = row["role"]

"""All SQLite database functions for the Blog CRUD App.

Kept separate from app.py so routes stay clean. Uses only the standard-library
sqlite3 module.
"""
import sqlite3
from datetime import datetime

DB_NAME = "blog.db"


def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row  # access columns by name
    return conn


def init_db():
    """Create the posts table if it doesn't exist."""
    conn = get_connection()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            author TEXT NOT NULL,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()


def _now():
    return datetime.now().strftime("%Y-%m-%d %H:%M")


# ---- CREATE ----
def add_post(title, content, author):
    now = _now()
    conn = get_connection()
    conn.execute(
        "INSERT INTO posts (title, content, author, created_at, updated_at) "
        "VALUES (?, ?, ?, ?, ?)",
        (title, content, author, now, now),
    )
    conn.commit()
    conn.close()


# ---- READ (all, with optional title search) ----
def get_posts(search=""):
    conn = get_connection()
    if search:
        # LIKE with wildcards for a simple title search (? placeholder keeps it safe)
        rows = conn.execute(
            "SELECT * FROM posts WHERE title LIKE ? ORDER BY id DESC",
            (f"%{search}%",),
        ).fetchall()
    else:
        rows = conn.execute("SELECT * FROM posts ORDER BY id DESC").fetchall()
    conn.close()
    return rows


# ---- READ (one) ----
def get_post(post_id):
    conn = get_connection()
    row = conn.execute("SELECT * FROM posts WHERE id = ?", (post_id,)).fetchone()
    conn.close()
    return row


# ---- UPDATE ----
def update_post(post_id, title, content, author):
    conn = get_connection()
    conn.execute(
        "UPDATE posts SET title = ?, content = ?, author = ?, updated_at = ? "
        "WHERE id = ?",
        (title, content, author, _now(), post_id),
    )
    conn.commit()
    conn.close()


# ---- DELETE ----
def delete_post(post_id):
    conn = get_connection()
    conn.execute("DELETE FROM posts WHERE id = ?", (post_id,))
    conn.commit()
    conn.close()

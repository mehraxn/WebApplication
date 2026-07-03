"""All SQLite database functions for the Task Manager.

Kept separate from app.py so the routes stay clean and the data layer is easy to find.
Uses only the sqlite3 module from the Python standard library.
"""
import sqlite3
from datetime import datetime

DB_NAME = "tasks.db"

# Allowed values (also used for validation in app.py)
VALID_PRIORITIES = ("Low", "Medium", "High")
VALID_STATUSES = ("pending", "completed")


def get_connection():
    """Open a connection with rows accessible by column name."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Create the tasks table if it doesn't already exist."""
    conn = get_connection()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            priority TEXT NOT NULL DEFAULT 'Medium',
            status TEXT NOT NULL DEFAULT 'pending',
            created_at TEXT NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()


# ---- CREATE ----
def add_task(title, description, priority):
    conn = get_connection()
    conn.execute(
        "INSERT INTO tasks (title, description, priority, status, created_at) "
        "VALUES (?, ?, ?, ?, ?)",
        (title, description, priority, "pending", datetime.now().strftime("%Y-%m-%d %H:%M")),
    )
    conn.commit()
    conn.close()


# ---- READ (all, with optional filter) ----
def get_tasks(status_filter="all"):
    """Return tasks. status_filter can be 'all', 'pending', or 'completed'."""
    conn = get_connection()
    if status_filter in VALID_STATUSES:
        tasks = conn.execute(
            "SELECT * FROM tasks WHERE status = ? ORDER BY id DESC", (status_filter,)
        ).fetchall()
    else:
        tasks = conn.execute("SELECT * FROM tasks ORDER BY id DESC").fetchall()
    conn.close()
    return tasks


# ---- READ (one) ----
def get_task(task_id):
    conn = get_connection()
    task = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    conn.close()
    return task


# ---- UPDATE ----
def update_task(task_id, title, description, priority, status):
    conn = get_connection()
    conn.execute(
        "UPDATE tasks SET title = ?, description = ?, priority = ?, status = ? "
        "WHERE id = ?",
        (title, description, priority, status, task_id),
    )
    conn.commit()
    conn.close()


def set_status(task_id, status):
    """Update only the status (used by 'mark as completed')."""
    conn = get_connection()
    conn.execute("UPDATE tasks SET status = ? WHERE id = ?", (status, task_id))
    conn.commit()
    conn.close()


# ---- DELETE ----
def delete_task(task_id):
    conn = get_connection()
    conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()

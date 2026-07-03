# Database helpers for the create demo.
import sqlite3

DB_NAME = "database.db"


def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Create the messages table if it doesn't exist."""
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def add_message(text):
    """Insert a new message (uses a ? placeholder for safety)."""
    conn = get_connection()
    conn.execute("INSERT INTO messages (text) VALUES (?)", (text,))
    conn.commit()
    conn.close()


def get_messages():
    """Return all messages, newest first."""
    conn = get_connection()
    messages = conn.execute("SELECT * FROM messages ORDER BY id DESC").fetchall()
    conn.close()
    return messages

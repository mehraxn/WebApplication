# Database helpers for the read demo.
import sqlite3

DB_NAME = "database.db"


def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row  # access columns by name
    return conn


def init_db():
    """Create the table and add sample rows the first time."""
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    """)
    # Only seed sample data if the table is empty
    count = conn.execute("SELECT COUNT(*) FROM items").fetchone()[0]
    if count == 0:
        conn.executemany(
            "INSERT INTO items (name) VALUES (?)",
            [("Notebook",), ("Pen",), ("Backpack",)],
        )
    conn.commit()
    conn.close()


def get_items():
    """Return all items."""
    conn = get_connection()
    items = conn.execute("SELECT * FROM items").fetchall()
    conn.close()
    return items

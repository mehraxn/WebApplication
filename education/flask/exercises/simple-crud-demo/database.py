# Database helpers for the CRUD demo.
import sqlite3

DB_NAME = "database.db"


def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


# CREATE
def add_note(content):
    conn = get_connection()
    conn.execute("INSERT INTO notes (content) VALUES (?)", (content,))
    conn.commit()
    conn.close()


# READ (all)
def get_notes():
    conn = get_connection()
    notes = conn.execute("SELECT * FROM notes ORDER BY id DESC").fetchall()
    conn.close()
    return notes


# READ (one)
def get_note(note_id):
    conn = get_connection()
    note = conn.execute("SELECT * FROM notes WHERE id = ?", (note_id,)).fetchone()
    conn.close()
    return note


# UPDATE
def update_note(note_id, content):
    conn = get_connection()
    conn.execute("UPDATE notes SET content = ? WHERE id = ?", (content, note_id))
    conn.commit()
    conn.close()


# DELETE
def delete_note(note_id):
    conn = get_connection()
    conn.execute("DELETE FROM notes WHERE id = ?", (note_id,))
    conn.commit()
    conn.close()

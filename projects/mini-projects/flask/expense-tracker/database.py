"""All SQLite database functions for the Expense Tracker.

Kept separate from app.py so the routes stay clean. Uses only the standard-library
sqlite3 module.
"""
import sqlite3

DB_NAME = "expenses.db"

# Categories offered in the app (also used for validation)
CATEGORIES = ("Food", "Transport", "Housing", "Entertainment", "Health", "Other")


def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row  # access columns by name
    return conn


def init_db():
    """Create the expenses table if it doesn't exist."""
    conn = get_connection()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL,
            note TEXT
        )
        """
    )
    conn.commit()
    conn.close()


# ---- CREATE ----
def add_expense(title, amount, category, date, note):
    conn = get_connection()
    conn.execute(
        "INSERT INTO expenses (title, amount, category, date, note) VALUES (?, ?, ?, ?, ?)",
        (title, amount, category, date, note),
    )
    conn.commit()
    conn.close()


# ---- READ (all, with optional category filter) ----
def get_expenses(category_filter="all"):
    conn = get_connection()
    if category_filter and category_filter != "all":
        rows = conn.execute(
            "SELECT * FROM expenses WHERE category = ? ORDER BY date DESC, id DESC",
            (category_filter,),
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT * FROM expenses ORDER BY date DESC, id DESC"
        ).fetchall()
    conn.close()
    return rows


# ---- READ (one) ----
def get_expense(expense_id):
    conn = get_connection()
    row = conn.execute(
        "SELECT * FROM expenses WHERE id = ?", (expense_id,)
    ).fetchone()
    conn.close()
    return row


# ---- UPDATE ----
def update_expense(expense_id, title, amount, category, date, note):
    conn = get_connection()
    conn.execute(
        "UPDATE expenses SET title = ?, amount = ?, category = ?, date = ?, note = ? "
        "WHERE id = ?",
        (title, amount, category, date, note, expense_id),
    )
    conn.commit()
    conn.close()


# ---- DELETE ----
def delete_expense(expense_id):
    conn = get_connection()
    conn.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
    conn.commit()
    conn.close()


# ---- TOTALS ----
def get_total(category_filter="all"):
    """Total spending, optionally limited to one category."""
    conn = get_connection()
    if category_filter and category_filter != "all":
        row = conn.execute(
            "SELECT COALESCE(SUM(amount), 0) AS total FROM expenses WHERE category = ?",
            (category_filter,),
        ).fetchone()
    else:
        row = conn.execute(
            "SELECT COALESCE(SUM(amount), 0) AS total FROM expenses"
        ).fetchone()
    conn.close()
    return row["total"]


def get_totals_by_category():
    """Return a list of (category, total) rows, highest first."""
    conn = get_connection()
    rows = conn.execute(
        "SELECT category, SUM(amount) AS total FROM expenses "
        "GROUP BY category ORDER BY total DESC"
    ).fetchall()
    conn.close()
    return rows

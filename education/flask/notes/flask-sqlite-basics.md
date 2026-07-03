# Flask SQLite Basics

To store data that survives restarts (users, tasks, posts), you need a **database**.
SQLite is perfect for learning: it's built into Python, needs no separate server, and
stores everything in a single file.

## What is SQLite?
A lightweight database saved as one file (e.g. `database.db`). Python's built-in
`sqlite3` module talks to it — no installation required.

## Connecting to the database
Open a connection to the file (it's created if it doesn't exist), then make a
**cursor** to run commands.
```python
import sqlite3

conn = sqlite3.connect("database.db")   # open (or create) the db file
cursor = conn.cursor()                  # run SQL through the cursor
```

## Creating tables
Define your table once. `IF NOT EXISTS` avoids an error if it's already there.
```python
cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        done INTEGER DEFAULT 0
    )
""")
conn.commit()   # save the change
```
`id` auto-increments; `title` is required text; `done` defaults to 0 (false).

## Inserting records
Use **placeholders (`?`)** for values — never build SQL with f-strings (that risks SQL
injection). Pass the values as a tuple.
```python
cursor.execute(
    "INSERT INTO tasks (title, done) VALUES (?, ?)",
    ("Learn Flask", 0)
)
conn.commit()   # inserts/updates/deletes must be committed to save
```

## Selecting records
Run a `SELECT`, then fetch the rows.
```python
cursor.execute("SELECT * FROM tasks")
rows = cursor.fetchall()   # list of all rows
for row in rows:
    print(row)             # e.g. (1, 'Learn Flask', 0)

# one row only:
cursor.execute("SELECT * FROM tasks WHERE id = ?", (1,))
task = cursor.fetchone()
```
Tip: set `conn.row_factory = sqlite3.Row` right after connecting to access columns by
name (`row["title"]`) instead of by index.

## Closing connections
Always close the connection when done to free resources.
```python
conn.close()
```

## Putting it together in Flask
A common pattern is a small helper that opens a fresh connection per request.
```python
import sqlite3
from flask import g

def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row   # rows behave like dicts
    return conn

@app.route("/tasks")
def tasks():
    conn = get_db()
    rows = conn.execute("SELECT * FROM tasks").fetchall()
    conn.close()
    return render_template("tasks.html", tasks=rows)
```

### Common mistakes
- **Forgetting `conn.commit()`** after INSERT/UPDATE/DELETE — the change isn't saved.
- **Building SQL with f-strings/`+`** — always use `?` placeholders to prevent SQL
  injection.
- Not closing the connection.
- Passing a single value without a tuple — it must be `(value,)` (note the comma).

---

### Quick review
- `sqlite3.connect("file.db")` → `conn.cursor()` to run SQL.
- `CREATE TABLE IF NOT EXISTS ...`, then `commit()`.
- Insert/select with `?` placeholders and a values tuple; `commit()` after writes.
- `fetchall()` / `fetchone()` to read; `conn.close()` when done.

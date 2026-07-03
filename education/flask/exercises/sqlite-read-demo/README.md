# Exercise: SQLite Read Demo

## Goal
Read items from a SQLite database and display them on a page.

## Concepts practiced
- Keeping database code in a separate `database.py`
- Connecting to SQLite with `sqlite3`
- Creating a table with `CREATE TABLE IF NOT EXISTS`
- Seeding sample data once
- Selecting rows and displaying them with a Jinja loop
- Using `sqlite3.Row` to access columns by name

## How to run
```bash
pip install flask
python app.py
```
Open http://127.0.0.1:5000. A `database.db` file is created automatically with sample
items.

## Files included
- `app.py` — reads and displays items
- `database.py` — connection, table creation, and read helper
- `templates/index.html` — lists the items
- `README.md` — this file

## What I learned
- Separating database logic into `database.py` keeps `app.py` clean.
- `CREATE TABLE IF NOT EXISTS` is safe to run every start.
- `sqlite3.Row` lets me use `item["name"]` instead of numeric indexes.

## Difficulty
Intermediate

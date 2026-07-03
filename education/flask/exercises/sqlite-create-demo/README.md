# Exercise: SQLite Create Demo

## Goal
Create records through a form and save them to a SQLite database, then display them.

## Concepts practiced
- Inserting rows with `INSERT INTO ... VALUES (?)`
- Reading POST data with `request.form.get()`
- Basic validation (skip empty input)
- Redirect-after-POST
- Keeping database logic in `database.py`

## How to run
```bash
pip install flask
python app.py
```
Open http://127.0.0.1:5000, add a few messages, and watch them appear. Data persists in
`database.db` across restarts.

## Files included
- `app.py` — form handling and routes
- `database.py` — table creation, insert, and read helpers
- `templates/index.html` — form + message list
- `README.md` — this file

## What I learned
- `?` placeholders keep inserts safe from SQL injection.
- `conn.commit()` is required to actually save an insert.
- The Post/Redirect/Get pattern avoids duplicate submissions on refresh.
- Data stored in SQLite survives server restarts.

## Difficulty
Intermediate

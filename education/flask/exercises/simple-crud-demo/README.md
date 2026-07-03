# Exercise: Simple CRUD Demo

## Goal
Build a small CRUD app for notes: add, list, edit, and delete records stored in SQLite.

## Concepts practiced
- Full CRUD: Create, Read, Update, Delete
- Route patterns: `/add`, `/edit/<int:id>`, `/delete/<int:id>`
- Reading and validating form input
- Flash messages for feedback
- Template inheritance with `base.html`
- Redirect-after-POST and `url_for`
- Deletes via a POST form (not a link)

## How to run
```bash
pip install flask
python app.py
```
Open http://127.0.0.1:5000. Add notes, edit them, and delete them. Data persists in
`database.db`.

## Files included
- `app.py` — CRUD routes
- `database.py` — all SQLite helpers (create/read/update/delete)
- `templates/base.html` — shared layout + flash messages
- `templates/index.html` — list + add form
- `templates/edit.html` — edit form
- `static/style.css` — styling
- `README.md` — this file

## What I learned
- The four CRUD operations map to INSERT, SELECT, UPDATE, and DELETE.
- Editing uses the same route for GET (show form) and POST (save).
- Deletes should use a POST form so they aren't triggered accidentally.
- Separating `database.py` from `app.py` keeps the code organized — the same structure
  used in the real portfolio project.

## Difficulty
Intermediate

# Task Manager with SQLite

## Project Overview
A small but complete **Flask CRUD application** for managing tasks. You can create, view,
edit, delete, and complete tasks, filter them by status, and everything is stored in a
SQLite database. Built with plain Flask and the standard-library `sqlite3` module — no
SQLAlchemy, no Flask-WTF.

## Features
1. View all tasks
2. Create a new task
3. Edit a task
4. Delete a task
5. Mark a task as completed
6. Filter tasks by **all / pending / completed**
7. Tasks stored in SQLite (`tasks.db`)
8. Flash messages for feedback
9. Back-end validation
10. Clean Jinja templates with inheritance (`base.html`)
11. Simple, responsive CSS

## Technologies Used
- Python 3
- Flask (routing, templates, flash messages)
- sqlite3 (Python standard library)
- Jinja2 templates
- Plain, responsive CSS

## Folder Structure
```
task-manager-sqlite/
├── app.py                 # routes and request handling
├── database.py            # all SQLite functions (CRUD)
├── requirements.txt       # dependencies (Flask)
├── README.md              # this file
├── static/
│   └── style.css          # responsive styling
├── templates/
│   ├── base.html          # shared layout + flash messages
│   ├── index.html         # task list + filters
│   ├── create_task.html   # new task form
│   ├── edit_task.html     # edit task form
│   ├── task_detail.html   # single task view
│   └── 404.html           # friendly not-found page
└── screenshots/           # add screenshots here
```
> `tasks.db` is created automatically the first time you run the app.

## How to Run or Open
```bash
pip install -r requirements.txt
python app.py
```
Then open **http://127.0.0.1:5000** in your browser.

## Database Schema
Table **`tasks`**: `id` (PK), `title` (required), `description` (optional), `priority`
(`Low`/`Medium`/`High`, default `Medium`), `status` (`pending`/`completed`, default
`pending`), `created_at` (timestamp).

**Validation:** title is required; priority must be Low, Medium, or High; description is
optional. On failure the app flashes an error and re-renders the form; on success it
redirects (Post/Redirect/Get).

## What I Learned
- The full request cycle: routing, Jinja inheritance, forms, validation, flash, and PRG.
- Complete CRUD against SQLite with a clean split between `app.py` and `database.py`.
- Filtering records by a query-string parameter.

## Resume Value
The flagship "I can build a real back-end" project. It demonstrates routing, templates with
inheritance, GET/POST form handling, server-side validation, flash feedback, and full CRUD
against a real SQLite database.

## Future Improvements
- Add user accounts and login (with password hashing)
- Add due dates, sorting, and search
- Move the secret key to an environment variable
- Add automated tests and deploy with `debug=False`

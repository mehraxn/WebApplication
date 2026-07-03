# Flask Projects

Flask applications built with Python. The **portfolio project** is a complete, polished
CRUD app; the **practice projects** are smaller demos exploring individual Flask features.
All use Flask (and, where needed, the standard-library `sqlite3`) — no heavy extra
dependencies.

## Portfolio projects

| Project | Description | Key concepts |
|---------|-------------|--------------|
| [task-manager-sqlite/](task-manager-sqlite/) | Complete task manager with full CRUD, filtering, flash messages, and SQLite storage | Routing, Jinja inheritance, forms + validation, flash, SQLite CRUD, PRG |
| [booking-reservation-app/](booking-reservation-app/) | Event booking app with reservations, capacity checks, and date validation | Two related tables + JOIN, capacity logic, date/email validation, flash, PRG |
| [expense-tracker/](expense-tracker/) | Track expenses by category with totals and a per-category summary | CRUD, filtering, SQL aggregation (`SUM`/`GROUP BY`), validation, flash, PRG |
| [blog-crud-app/](blog-crud-app/) | Blog with full post CRUD and title search | CRUD, `LIKE` search, timestamps, validation, Jinja inheritance, flash, PRG |

## Practice / demo projects

Smaller Flask demos already in this folder:

| Project | Description |
|---------|-------------|
| [routing-demo/](routing-demo/) | Basic routing and view functions |
| [jinja-fruit-list/](jinja-fruit-list/) | Rendering a list with Jinja loops |
| [url-for-static-demo/](url-for-static-demo/) | Serving static files with `url_for` |
| [form-handling-demo/](form-handling-demo/) | Handling GET/POST form submissions |

## How to run any project
```bash
pip install flask
cd <project-folder>
python app.py
```
Then open http://127.0.0.1:5000 in your browser. Projects that use a database create the
`.db` file automatically on first run.

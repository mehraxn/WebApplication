# Expense Tracker

## Project Overview
A small but complete **Flask application** for tracking personal expenses by category. You
can add, edit, and delete expenses, filter them by category, see your total spending, and
view a per-category summary with percentage bars. Everything is stored in SQLite. Built with
plain Flask and `sqlite3` (no SQLAlchemy, no Flask-WTF).

## Features
1. View all expenses
2. Add an expense
3. Edit an expense
4. Delete an expense
5. Categorize expenses (Food, Transport, Housing, Entertainment, Health, Other)
6. Show total spending
7. Show spending by category (with percentage bars)
8. Filter expenses by category
9. SQLite storage
10. Flash messages for feedback
11. Back-end validation

## Technologies Used
- Python 3
- Flask (routing, templates, flash messages)
- sqlite3 (Python standard library)
- Jinja2 templates with inheritance
- Plain, responsive CSS

## Folder Structure
```
expense-tracker/
├── app.py                 # routes, validation, request handling
├── database.py            # SQLite functions (CRUD + totals)
├── requirements.txt       # dependencies (Flask)
├── README.md              # this file
├── static/
│   └── style.css          # responsive styling
├── templates/
│   ├── base.html          # shared layout + flash messages
│   ├── index.html         # expense list + filter + total
│   ├── add_expense.html   # add form
│   ├── edit_expense.html  # edit form
│   └── summary.html       # totals by category
└── screenshots/           # add screenshots here
```
> `expenses.db` is created automatically the first time you run the app.

## How to Run or Open
```bash
pip install -r requirements.txt
python app.py
```
Then open **http://127.0.0.1:5000** in your browser.

## Database Schema
Table **`expenses`**: `id` (PK), `title` (required), `amount` (REAL, positive), `category`
(required), `date` (`YYYY-MM-DD`, required), `note` (optional).

**Validation:** title required; amount must be a positive number; category required and
valid; date required and a valid `YYYY-MM-DD`; note optional.

## What I Learned
- SQL aggregation with `SUM` and `GROUP BY` to compute totals per category.
- Filtering records by a query-string parameter.
- Full CRUD + validation with a clean split between `app.py` and `database.py`.

## Resume Value
A classic full-stack exercise showing real data handling: CRUD, filtering, and aggregation.
Demonstrates the complete Flask workflow — routing, Jinja inheritance, forms with validation,
flash messages, and SQLite.

## Future Improvements
- Add month/date-range filtering
- Add a real chart (e.g. a pie chart) on the summary page
- Export expenses to CSV
- Move the secret key to an environment variable and deploy with `debug=False`

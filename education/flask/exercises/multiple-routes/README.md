# Exercise: Multiple Routes

## Goal
Build a Flask app with three pages — home, about, and contact — each with its own route
and template.

## Concepts practiced
- Defining multiple routes
- `render_template` for each page
- A shared navigation using `url_for`
- Organizing HTML in the `templates/` folder

## How to run
```bash
pip install flask
python app.py
```
Open http://127.0.0.1:5000 and use the nav links to move between pages.

## Files included
- `app.py` — three routes
- `templates/home.html`, `templates/about.html`, `templates/contact.html`
- `README.md` — this file

## What I learned
- Each page gets its own route and template.
- `url_for('about')` links by the view function name, so links don't break if the URL
  changes.
- Templates live in the `templates/` folder that Flask looks in automatically.

## Difficulty
Beginner

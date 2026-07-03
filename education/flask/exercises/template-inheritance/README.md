# Exercise: Template Inheritance

## Goal
Use a `base.html` layout and have child pages (`home`, `about`) inherit from it, plus a
shared stylesheet from `static/`.

## Concepts practiced
- Template inheritance (`{% extends %}` and `{% block %}`)
- A shared base layout (navbar + footer)
- Linking a static CSS file with `url_for('static', ...)`
- `url_for` navigation links

## How to run
```bash
pip install flask
python app.py
```
Open http://127.0.0.1:5000 and switch between Home and About.

## Files included
- `app.py` — two routes
- `templates/base.html` — the shared layout
- `templates/home.html`, `templates/about.html` — child pages
- `static/style.css` — shared styles
- `README.md` — this file

## What I learned
- `{% extends "base.html" %}` lets a page reuse a common layout.
- Child pages only fill in `{% block %}` sections, so the navbar/footer aren't repeated.
- One CSS file in `static/` styles every page via the base template.

## Difficulty
Beginner+

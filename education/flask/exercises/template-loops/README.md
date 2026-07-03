# Exercise: Template Loops

## Goal
Render a list of items from Python using a Jinja `for` loop in the template.

## Concepts practiced
- Passing a list to a template with `render_template`
- Jinja `for` loops (`{% for %}` / `{% endfor %}`)
- A Jinja `if`/`else` to handle an empty list
- The `length` filter

## How to run
```bash
pip install flask
python app.py
```
Open http://127.0.0.1:5000 to see the list.

## Files included
- `app.py` — passes a list to the template
- `templates/index.html` — loops over the list
- `README.md` — this file

## What I learned
- `{% for item in list %}` repeats HTML for each item.
- `{% if %}` lets me show a fallback message when the list is empty.
- Filters like `{{ fruits|length }}` transform values right in the template.

## Difficulty
Beginner

# Exercise: Form GET/POST

## Goal
Create a form and handle both the GET request (show the form) and the POST request
(process the submitted data).

## Concepts practiced
- A route that accepts `methods=["GET", "POST"]`
- Branching on `request.method`
- Reading input with `request.form.get()`
- Basic server-side validation
- Rendering a different template for the result

## How to run
```bash
pip install flask
python app.py
```
Open http://127.0.0.1:5000, submit the form, and try submitting it empty to see the
validation message.

## Files included
- `app.py` — GET/POST handling
- `templates/form.html`, `templates/result.html`
- `README.md` — this file

## What I learned
- The same route can show a form (GET) and process it (POST) by checking
  `request.method`.
- `request.form.get("name")` safely reads a field even if it's missing.
- Always validate on the server, then show either an error or a result page.

## Difficulty
Beginner+

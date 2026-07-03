# Exercise: Flash Message Demo

## Goal
Show one-time flash messages after a form submission — a success message on valid input
and an error message on empty input.

## Concepts practiced
- Setting `app.secret_key` (required for flashing)
- `flash("message", "category")`
- Displaying messages with `get_flashed_messages(with_categories=True)`
- Styling success vs error messages
- Redirect-after-POST so messages appear once

## How to run
```bash
pip install flask
python app.py
```
Open http://127.0.0.1:5000, then submit with and without a name.

## Files included
- `app.py` — flashing logic
- `templates/base.html` — renders flashed messages
- `templates/index.html` — the form
- `README.md` — this file

## What I learned
- Flash messages need a secret key because they use the session.
- Categories (`success`, `error`) let me style messages differently.
- After flashing I redirect, and the message shows once then disappears.

## Difficulty
Beginner+

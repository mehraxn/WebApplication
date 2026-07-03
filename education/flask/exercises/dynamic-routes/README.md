# Exercise: Dynamic Routes

## Goal
Use dynamic route parameters so the same route works for many different values.

## Concepts practiced
- Dynamic routes with `<username>`
- Passing the captured value into a template
- Type converters (`<int:number>`)
- Building responses from URL data

## How to run
```bash
pip install flask
python app.py
```
Then try these URLs:
- http://127.0.0.1:5000/user/alex
- http://127.0.0.1:5000/square/5

## Files included
- `app.py` — dynamic routes
- `templates/profile.html`
- `README.md` — this file

## What I learned
- `<name>` in a route becomes an argument to the view function.
- The `int:` converter makes a route accept only whole numbers (others give a 404).
- Dynamic routes let one function serve many pages (one per user, per id, etc.).

## Difficulty
Beginner

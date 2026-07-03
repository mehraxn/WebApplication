# Flask Education

This section covers **Flask**, a lightweight Python web framework for building real,
data-driven web applications. It's where the front-end skills (HTML, CSS, Bootstrap)
meet the back-end: routing, templates, forms, databases, and CRUD. This is the core of a
junior **Flask developer** skill set.

## Overview

- **`notes/`** — clear, beginner-friendly notes on each core Flask topic, written for
  quick exam and interview review. Every note explains the idea in plain English, shows
  practical Python/HTML code, and lists common mistakes.
- **`exercises/`** — small, focused practice apps that apply the ideas from the notes.

> To run any Flask example: install Flask (`pip install flask`), save the code as
> `app.py`, run `python app.py`, and open `http://127.0.0.1:5000` in your browser.

## Notes table

| File | What it covers |
|------|----------------|
| `notes/flask-project-structure.md` | `app.py`, `templates/`, `static/`, `requirements.txt`, `README.md`, and why structure matters. |
| `notes/flask-routing.md` | `@app.route`, view functions, dynamic routes, parameters, returning HTML/templates. |
| `notes/flask-templates-jinja.md` | `render_template`, variables, `if`/`for`, template inheritance, `url_for`. |
| `notes/flask-static-files.md` | The `static/` folder and linking CSS, JS, and images with `url_for`. |
| `notes/flask-forms.md` | GET vs POST forms, `request.form`, validation, redirect-after-POST. |
| `notes/flask-flash-messages.md` | `flash()`, `get_flashed_messages()`, the secret key, success/error categories. |
| `notes/flask-sqlite-basics.md` | Connecting to SQLite, creating tables, inserting, selecting, closing. |
| `notes/flask-crud.md` | Create, Read, Update, Delete and the common route patterns. |
| `notes/flask-error-handling.md` | Custom 404 pages, validation errors, defensive back-end checks. |
| `notes/flask-security-basics.md` | Trusting no input, password hashing, environment variables, secret key, debug mode. |

## Exercises table

Each exercise is a small, focused Flask app. Run any of them with `python app.py` (after
`pip install flask`) and open http://127.0.0.1:5000.

| Exercise | Concepts | Difficulty |
|----------|----------|------------|
| `exercises/hello-flask/` | One route, returning a response | Beginner |
| `exercises/multiple-routes/` | Several routes + templates, `url_for` nav | Beginner |
| `exercises/dynamic-routes/` | Dynamic URL parameters, `int` converter | Beginner |
| `exercises/template-loops/` | Passing a list, Jinja `for`/`if`, filters | Beginner |
| `exercises/template-inheritance/` | `base.html`, blocks, static CSS | Beginner+ |
| `exercises/form-get-post/` | GET vs POST, `request.form`, validation | Beginner+ |
| `exercises/flash-message-demo/` | `flash()`, categories, secret key, PRG | Beginner+ |
| `exercises/sqlite-read-demo/` | Read from SQLite, separate `database.py` | Intermediate |
| `exercises/sqlite-create-demo/` | Insert via form, `?` placeholders, PRG | Intermediate |
| `exercises/simple-crud-demo/` | Full CRUD: add, edit, delete + flash | Intermediate |

## Recommended study order

Work through the notes in this order — each builds on the previous:

1. **`flask-project-structure.md`** — understand the layout first.
2. **`flask-routing.md`** — connect URLs to Python functions.
3. **`flask-templates-jinja.md`** — render dynamic HTML pages.
4. **`flask-static-files.md`** — add CSS, JS, and images.
5. **`flask-forms.md`** — take input from users.
6. **`flask-flash-messages.md`** — give users feedback.
7. **`flask-sqlite-basics.md`** — store data in a database.
8. **`flask-crud.md`** — build full create/read/update/delete features.
9. **`flask-error-handling.md`** — handle mistakes gracefully.
10. **`flask-security-basics.md`** — avoid the most common security pitfalls.

## Skills learned

After this section you'll be able to:

- Structure and run a Flask project.
- Define routes, including dynamic ones with parameters.
- Render dynamic pages with Jinja templates and template inheritance.
- Serve CSS, JS, and images from `static/`.
- Handle GET and POST forms with server-side validation.
- Show one-time feedback with flash messages.
- Store and query data in an SQLite database.
- Build complete CRUD features.
- Handle errors and write defensive back-end code.
- Apply beginner-level security best practices.

These are exactly the Flask skills expected of a junior back-end / full-stack developer.

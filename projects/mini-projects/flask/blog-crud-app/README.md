# Flask Blog CRUD App

## Project Overview
A small but complete **Flask blog application** with full CRUD for posts. You can view all
posts, read a single post, create, edit, and delete posts, and search posts by title. Posts
are stored in SQLite, timestamps are tracked automatically, and all input is validated on
the server. Built with plain Flask and `sqlite3` (no SQLAlchemy, no Flask-WTF).

## Features
1. View all blog posts (with excerpts)
2. View a single post
3. Create a post
4. Edit a post
5. Delete a post
6. Search posts by title
7. SQLite storage
8. Flash messages for feedback
9. Back-end validation
10. Responsive layout

## Technologies Used
- Python 3
- Flask (routing, templates, flash messages)
- sqlite3 (Python standard library)
- Jinja2 templates with inheritance
- Plain, responsive CSS

## Folder Structure
```
blog-crud-app/
├── app.py                 # routes, validation, request handling
├── database.py            # SQLite functions (CRUD + search)
├── requirements.txt       # dependencies (Flask)
├── README.md              # this file
├── static/
│   └── style.css          # responsive styling
├── templates/
│   ├── base.html          # shared layout + flash messages
│   ├── index.html         # post list + title search
│   ├── post_detail.html   # single post view
│   ├── create_post.html   # new post form
│   └── edit_post.html     # edit post form
└── screenshots/           # add screenshots here
```
> `blog.db` is created automatically the first time you run the app.

## How to Run or Open
```bash
pip install -r requirements.txt
python app.py
```
Then open **http://127.0.0.1:5000** in your browser.

## Database Schema
Table **`posts`**: `id` (PK), `title` (required, max 100 chars), `content` (required),
`author` (required), `created_at` (set on creation), `updated_at` (updated on each edit).

**Validation:** title required and ≤ 100 characters; content required; author required. The
title search uses a safe SQL `LIKE` query with a `?` placeholder.

## What I Learned
- Full CRUD plus search via a parameterized `LIKE` query.
- Tracking `created_at` / `updated_at` timestamps automatically.
- Jinja inheritance, server-side validation, flash messages, and PRG.

## Resume Value
The textbook CRUD project done end to end: listing with previews, a detail view,
create/edit/delete, and search. Demonstrates routing, template inheritance, validation,
flash messages, timestamps, and SQLite.

## Future Improvements
- Add user accounts and authentication (only authors can edit their posts)
- Add pagination for long post lists
- Support Markdown in post content
- Add categories/tags and comments

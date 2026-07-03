# Flask CRUD

**CRUD** stands for the four things almost every app does with data:
**C**reate, **R**ead, **U**pdate, **D**elete. Once you can do CRUD, you can build task
managers, blogs, to-do lists, and more. This note shows the standard Flask + SQLite
route patterns.

Assume a `tasks` table with columns `id`, `title`, `done` (see the SQLite note).

## A small DB helper
```python
import sqlite3

def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row   # access columns by name
    return conn
```

## Create
Show a form (GET) and insert the new record (POST), then redirect.
```python
from flask import request, redirect, url_for, render_template

@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("title", "").strip()
    if title:                                  # basic validation
        conn = get_db()
        conn.execute("INSERT INTO tasks (title) VALUES (?)", (title,))
        conn.commit()
        conn.close()
    return redirect(url_for("index"))          # Post/Redirect/Get
```

## Read
Fetch records and pass them to a template.
```python
@app.route("/")
def index():
    conn = get_db()
    tasks = conn.execute("SELECT * FROM tasks").fetchall()
    conn.close()
    return render_template("index.html", tasks=tasks)
```
```html
<ul>
  {% for task in tasks %}
    <li>{{ task["title"] }}</li>
  {% endfor %}
</ul>
```

## Update
Load one record into an edit form (GET), then save the changes (POST). The record id is
usually part of the URL.
```python
@app.route("/edit/<int:task_id>", methods=["GET", "POST"])
def edit(task_id):
    conn = get_db()
    if request.method == "POST":
        new_title = request.form.get("title", "").strip()
        conn.execute("UPDATE tasks SET title = ? WHERE id = ?", (new_title, task_id))
        conn.commit()
        conn.close()
        return redirect(url_for("index"))
    # GET: fetch the current record to fill the form
    task = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    conn.close()
    return render_template("edit.html", task=task)
```

## Delete
Remove a record by id, then redirect. Use POST for deletes (not a plain link) so they
aren't triggered accidentally by crawlers or prefetching.
```python
@app.route("/delete/<int:task_id>", methods=["POST"])
def delete(task_id):
    conn = get_db()
    conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))
```
```html
<form action="{{ url_for('delete', task_id=task['id']) }}" method="POST">
  <button type="submit">Delete</button>
</form>
```

## Common route patterns
| Action | Route | Method |
|--------|-------|--------|
| List all | `/` | GET |
| Show add form / create | `/add` | GET / POST |
| Edit form / update | `/edit/<int:id>` | GET / POST |
| Delete | `/delete/<int:id>` | POST |

### Common mistakes
- Forgetting `conn.commit()` after create/update/delete.
- Using GET (a link) for delete — use a POST form.
- Not validating input before inserting.
- Forgetting `?` placeholders (SQL injection risk).

---

### Quick review
- CRUD = Create, Read, Update, Delete.
- Create → INSERT; Read → SELECT; Update → UPDATE `WHERE id`; Delete → DELETE `WHERE id`.
- Put the record id in the URL (`/edit/<int:id>`), commit writes, and redirect after.
- Deletes should use a POST form.

# Flask Error Handling

Things go wrong: a user visits a page that doesn't exist, submits an empty form, or asks
for a record that was deleted. Good apps handle these gracefully instead of crashing or
showing an ugly error. This note covers the basics.

## Custom 404 page
A 404 means "page not found." By default Flask shows a plain message; you can show your
own friendly page with an error handler.
```python
from flask import render_template

@app.errorhandler(404)
def not_found(error):
    # return your template AND the 404 status code
    return render_template("404.html", ), 404
```
`templates/404.html`:
```html
{% extends "base.html" %}
{% block content %}
  <h1>404 — Page not found</h1>
  <p>Sorry, that page doesn't exist. <a href="{{ url_for('index') }}">Go home</a>.</p>
{% endblock %}
```
Returning the status code (`, 404`) matters — it tells the browser and search engines the
page really is missing.

## Validation errors
When form input is bad, don't save it — send the user back with a helpful message.
```python
@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("title", "").strip()

    if not title:
        flash("Title cannot be empty.", "danger")
        return redirect(url_for("index"))

    # input is valid — continue
    ...
```
Return a clear message so the user knows what to fix, not a stack trace.

## Defensive back-end checks
Never assume the data or the request is valid. Check before you act.

**Does the record exist?**
```python
@app.route("/task/<int:task_id>")
def show_task(task_id):
    conn = get_db()
    task = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    conn.close()

    if task is None:
        abort(404)          # trigger the 404 handler instead of crashing
    return render_template("task.html", task=task)
```
`abort(404)` (from `flask import abort`) cleanly stops and shows the 404 page.

**Guard against bad values:**
```python
quantity = request.form.get("quantity", "")
if not quantity.isdigit():
    flash("Quantity must be a number.", "danger")
    return redirect(url_for("index"))
quantity = int(quantity)
```

**General principles:**
- Check that required fields are present and non-empty.
- Check that a record exists before editing/deleting it.
- Convert and validate types (don't `int()` something that might not be a number).
- Fail with a friendly message + correct status code, not a crash.

### Common mistakes
- Returning a 404 template **without** the `, 404` status code.
- Assuming `fetchone()` returns a row — it can be `None`; check it.
- Trusting form input types (calling `int()` on user text without checking).
- Showing raw Python errors to users (especially with debug mode on — see the security
  note).

---

### Quick review
- Handle missing pages with `@app.errorhandler(404)` returning `..., 404`.
- Validate form input; on failure, flash a message and redirect.
- Use `abort(404)` when a requested record doesn't exist.
- Be defensive: check presence, existence, and types before acting on data.

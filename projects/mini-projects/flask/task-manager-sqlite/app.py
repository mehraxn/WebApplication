"""Task Manager with SQLite — a small but complete Flask CRUD application.

Features: view, create, edit, delete, mark-complete, and filter tasks.
Uses Flask + sqlite3 only (no SQLAlchemy, no Flask-WTF).
"""
from flask import Flask, render_template, request, redirect, url_for, flash, abort

import database

app = Flask(__name__)
app.secret_key = "dev-secret-key"  # required for flash messages

# Make sure the database and table exist before the first request
database.init_db()


def validate_task(title, priority):
    """Return an error message string if invalid, otherwise None."""
    if not title:
        return "Title is required."
    if priority not in database.VALID_PRIORITIES:
        return "Priority must be Low, Medium, or High."
    return None


@app.route("/")
def index():
    # Read the ?filter= value; default to showing all tasks
    status_filter = request.args.get("filter", "all")
    if status_filter not in ("all", "pending", "completed"):
        status_filter = "all"
    tasks = database.get_tasks(status_filter)
    return render_template("index.html", tasks=tasks, current_filter=status_filter)


@app.route("/task/<int:task_id>")
def task_detail(task_id):
    task = database.get_task(task_id)
    if task is None:
        abort(404)
    return render_template("task_detail.html", task=task)


@app.route("/create", methods=["GET", "POST"])
def create_task():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        priority = request.form.get("priority", "Medium")

        error = validate_task(title, priority)
        if error:
            flash(error, "danger")
            # Re-render the form so the user doesn't lose their input
            return render_template(
                "create_task.html",
                title=title,
                description=description,
                priority=priority,
            )

        database.add_task(title, description, priority)
        flash("Task created successfully.", "success")
        return redirect(url_for("index"))

    # GET: show the empty form
    return render_template("create_task.html")


@app.route("/edit/<int:task_id>", methods=["GET", "POST"])
def edit_task(task_id):
    task = database.get_task(task_id)
    if task is None:
        abort(404)

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        priority = request.form.get("priority", "Medium")
        status = request.form.get("status", "pending")
        if status not in database.VALID_STATUSES:
            status = "pending"

        error = validate_task(title, priority)
        if error:
            flash(error, "danger")
            return redirect(url_for("edit_task", task_id=task_id))

        database.update_task(task_id, title, description, priority, status)
        flash("Task updated successfully.", "success")
        return redirect(url_for("index"))

    # GET: show the form pre-filled with the current values
    return render_template("edit_task.html", task=task)


@app.route("/complete/<int:task_id>", methods=["POST"])
def complete_task(task_id):
    task = database.get_task(task_id)
    if task is None:
        abort(404)
    database.set_status(task_id, "completed")
    flash("Task marked as completed.", "success")
    return redirect(url_for("index"))


@app.route("/delete/<int:task_id>", methods=["POST"])
def delete_task(task_id):
    task = database.get_task(task_id)
    if task is None:
        abort(404)
    database.delete_task(task_id)
    flash("Task deleted.", "success")
    return redirect(url_for("index"))


@app.errorhandler(404)
def not_found(error):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(debug=True)

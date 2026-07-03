# A small CRUD demo: add, edit, and delete notes stored in SQLite.
from flask import Flask, render_template, request, redirect, url_for, flash
import database

app = Flask(__name__)
app.secret_key = "dev-secret-key"  # needed for flash messages

database.init_db()


@app.route("/")
def index():
    notes = database.get_notes()
    return render_template("index.html", notes=notes)


# CREATE
@app.route("/add", methods=["POST"])
def add():
    content = request.form.get("content", "").strip()
    if not content:
        flash("Note cannot be empty.", "error")
    else:
        database.add_note(content)
        flash("Note added.", "success")
    return redirect(url_for("index"))


# UPDATE (show edit form on GET, save on POST)
@app.route("/edit/<int:note_id>", methods=["GET", "POST"])
def edit(note_id):
    note = database.get_note(note_id)
    if note is None:
        flash("Note not found.", "error")
        return redirect(url_for("index"))

    if request.method == "POST":
        content = request.form.get("content", "").strip()
        if not content:
            flash("Note cannot be empty.", "error")
            return redirect(url_for("edit", note_id=note_id))
        database.update_note(note_id, content)
        flash("Note updated.", "success")
        return redirect(url_for("index"))

    return render_template("edit.html", note=note)


# DELETE
@app.route("/delete/<int:note_id>", methods=["POST"])
def delete(note_id):
    database.delete_note(note_id)
    flash("Note deleted.", "success")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)

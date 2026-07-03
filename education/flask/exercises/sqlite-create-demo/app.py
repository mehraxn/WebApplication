# Create records through a form and save them to SQLite.
from flask import Flask, render_template, request, redirect, url_for
import database

app = Flask(__name__)

database.init_db()


@app.route("/")
def index():
    messages = database.get_messages()
    return render_template("index.html", messages=messages)


@app.route("/add", methods=["POST"])
def add():
    text = request.form.get("text", "").strip()
    # Basic validation: only save non-empty messages
    if text:
        database.add_message(text)
    # Redirect back after saving (Post/Redirect/Get)
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)

# Demonstrates flash messages shown after a form submission.
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
# A secret key is required for flash messages (they use the session)
app.secret_key = "dev-secret-key"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/submit", methods=["POST"])
def submit():
    name = request.form.get("name", "").strip()
    if not name:
        flash("Name cannot be empty.", "error")
    else:
        flash(f"Thanks, {name}! Your form was submitted.", "success")
    # Redirect back so the message shows once (Post/Redirect/Get)
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)

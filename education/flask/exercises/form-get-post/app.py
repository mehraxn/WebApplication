# Handling a form with both GET (show form) and POST (process it).
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def form():
    if request.method == "POST":
        # Read submitted data from request.form
        name = request.form.get("name", "").strip()
        # Simple validation
        if not name:
            return render_template("form.html", error="Please enter your name.")
        return render_template("result.html", name=name)

    # GET: just show the empty form
    return render_template("form.html")


if __name__ == "__main__":
    app.run(debug=True)

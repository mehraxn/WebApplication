# Passing a list to a template and rendering it with a Jinja loop.
from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index():
    # A simple list of items to display
    fruits = ["Apple", "Banana", "Cherry", "Orange", "Mango"]
    return render_template("index.html", fruits=fruits)


if __name__ == "__main__":
    app.run(debug=True)

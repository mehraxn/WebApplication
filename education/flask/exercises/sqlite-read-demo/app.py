# Reads items from SQLite and displays them.
from flask import Flask, render_template
import database

app = Flask(__name__)

# Make sure the table exists (and seed sample data) at startup
database.init_db()


@app.route("/")
def index():
    items = database.get_items()
    return render_template("index.html", items=items)


if __name__ == "__main__":
    app.run(debug=True)

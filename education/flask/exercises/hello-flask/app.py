# The smallest possible Flask app: one route that returns text.
from flask import Flask

app = Flask(__name__)


@app.route("/")
def home():
    # Whatever we return is sent to the browser
    return "<h1>Hello, Flask!</h1><p>My first Flask app is running.</p>"


if __name__ == "__main__":
    # debug=True auto-reloads on changes (development only)
    app.run(debug=True)

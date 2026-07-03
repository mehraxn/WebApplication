# Demonstrates dynamic route parameters in the URL.
from flask import Flask, render_template

app = Flask(__name__)


# <username> is captured from the URL and passed to the function
@app.route("/user/<username>")
def profile(username):
    return render_template("profile.html", username=username)


# <int:number> only matches whole numbers thanks to the int converter
@app.route("/square/<int:number>")
def square(number):
    return f"{number} squared is {number * number}"


@app.route("/")
def home():
    # Try visiting /user/alex or /square/5
    return "Try /user/alex or /square/5 in the URL."


if __name__ == "__main__":
    app.run(debug=True)

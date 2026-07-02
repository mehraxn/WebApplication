from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    user_name = "Mera"
    logged_in = True

    fruits = [
        {"name": "Apple", "color": "Red", "available": True},
        {"name": "Banana", "color": "Yellow", "available": True},
        {"name": "Cherry", "color": "Dark Red", "available": False},
        {"name": "Orange", "color": "Orange", "available": True}
    ]

    return render_template(
        "index.html",
        user_name=user_name,
        logged_in=logged_in,
        fruits=fruits
    )

if __name__ == "__main__":
    app.run(debug=True)
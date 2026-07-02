from flask import Flask, render_template, request

app = Flask(__name__)

# This list stores submitted form data while the app is running.
# If you stop/restart Flask, the list becomes empty again.
submissions = []


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        # The keys here must match the name="" attributes in the HTML inputs.
        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")

        submissions.append({
            "name": name,
            "email": email,
            "message": message
        })

    return render_template("index.html", submissions=submissions)


if __name__ == "__main__":
    app.run(debug=True)

# Flask Forms

Forms are how users send data to your app. In Flask you handle both **GET** (reading /
searching) and **POST** (sending / saving) requests, then read the submitted values from
the `request` object.

## GET forms
A GET form puts the data in the URL (`/search?q=cats`). Good for searches.
```html
<form action="/search" method="GET">
  <input type="text" name="q" />
  <button type="submit">Search</button>
</form>
```
```python
from flask import request

@app.route("/search")
def search():
    query = request.args.get("q")   # read GET data from the URL
    return f"You searched for: {query}"
```
Note: GET data is read from **`request.args`**.

## POST forms
A POST form sends data hidden in the request body. Use it for logins, sign-ups, and
anything that creates or changes data. The route must allow POST.
```html
<form action="/register" method="POST">
  <input type="text" name="username" />
  <input type="email" name="email" />
  <button type="submit">Register</button>
</form>
```
```python
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        return f"Registered {username} ({email})"
    # if it's a GET, just show the form page
    return render_template("register.html")
```

## `request.form`
For POST data, read values from **`request.form`**. The key is the field's `name`
attribute.
```python
username = request.form["username"]        # errors if missing
email = request.form.get("email")          # returns None if missing (safer)
```
Use `.get()` when a field might be absent so you don't crash.

## Validation basics
Never assume the data is good. Check it on the server before using it.
```python
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()

        if not username or not email:
            return "Please fill in all fields", 400
        if "@" not in email:
            return "Invalid email", 400

        # data looks OK — save it here
        return redirect(url_for("home"))
    return render_template("register.html")
```
HTML `required` helps, but users can bypass it — always validate on the server too.

## Redirect after POST
After a successful POST, **redirect** to another page instead of returning HTML directly.
This is the "Post/Redirect/Get" pattern — it stops the form from being re-submitted if
the user refreshes.
```python
from flask import redirect, url_for

@app.route("/add", methods=["POST"])
def add():
    # ... save the data ...
    return redirect(url_for("home"))   # send the user to the home route
```

### Common mistakes
- **405 Method Not Allowed** — the route is missing `methods=["POST"]`.
- Reading POST data from `request.args` (that's for GET) or GET data from
  `request.form`.
- Using `request.form["x"]` when the field might be missing — use `.get()`.
- Returning HTML after a POST instead of redirecting (causes duplicate submissions on
  refresh).

---

### Quick review
- GET data → `request.args`; POST data → `request.form`.
- Allow POST with `methods=["GET", "POST"]` and branch on `request.method`.
- Always validate on the server, even with HTML `required`.
- After a successful POST, `redirect(url_for(...))` (Post/Redirect/Get).

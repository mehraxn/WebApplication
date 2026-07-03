# Flask Routing

A **route** connects a URL to a Python function. When someone visits that URL, Flask
runs the function and sends back whatever it returns. This is the core of every Flask
app.

## `@app.route`
The decorator that maps a URL path to a function.
```python
from flask import Flask
app = Flask(__name__)

@app.route("/")
def home():
    return "This is the home page"

@app.route("/about")
def about():
    return "About us"
```
Visiting `/` runs `home()`; visiting `/about` runs `about()`.

## View functions
The function under a `@app.route` is called a **view function**. It handles the request
and returns a response (text, HTML, or a template). The function name is also used by
`url_for()` (see the templates note), so give it a clear name.

## Dynamic routes
Sometimes part of the URL changes — like a user id or a product name. Put it in angle
brackets and it becomes a function argument.
```python
@app.route("/user/<username>")
def profile(username):
    return f"Hello, {username}!"
```
- `/user/alex` → "Hello, alex!"
- `/user/sara` → "Hello, sara!"

## Route parameters (with types)
You can tell Flask what type the parameter should be using a **converter**.
```python
@app.route("/post/<int:post_id>")
def show_post(post_id):
    # post_id is an integer here
    return f"Showing post number {post_id}"
```
Common converters:
- `<string:name>` — text (the default)
- `<int:id>` — whole number
- `<float:price>` — decimal
- `<path:subpath>` — text that can include slashes

`/post/42` works; `/post/hello` gives a 404 because `hello` isn't an `int`.

## Returning HTML / templates
A view can return a plain string, some inline HTML, or (best) a rendered template file.
```python
from flask import render_template

@app.route("/")
def home():
    # returns simple HTML
    return "<h1>Welcome</h1>"

@app.route("/dashboard")
def dashboard():
    # renders templates/dashboard.html
    return render_template("dashboard.html")
```
For real pages, use `render_template` with an HTML file in `templates/` rather than
writing HTML inside Python.

## Choosing the HTTP method
By default a route only accepts **GET**. To also accept form submissions (POST), list
the methods:
```python
@app.route("/submit", methods=["GET", "POST"])
def submit():
    return "Handled GET or POST"
```
(More on this in the forms note.)

### Common mistakes
- **Two functions with the same name** — Flask uses function names internally; keep them
  unique.
- **Forgetting to add the parameter to the function** — `@app.route("/user/<name>")`
  requires `def profile(name):`.
- **Expecting POST to work by default** — you must add `methods=["POST"]`.

---

### Quick review
- `@app.route("/path")` maps a URL to a view function.
- `<var>` in the path becomes a function argument (add a converter like `<int:id>`).
- Return a string/HTML, or better, `render_template("file.html")`.
- Routes are GET-only unless you add `methods=["GET", "POST"]`.

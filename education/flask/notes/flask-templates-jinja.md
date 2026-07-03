# Flask Templates & Jinja

Instead of writing HTML inside Python, Flask uses **templates** — HTML files with special
placeholders. The templating engine is called **Jinja**. It lets you insert data, use
conditions and loops, and share layout between pages.

Templates live in the `templates/` folder.

## `render_template`
This function renders an HTML file and can pass data to it as keyword arguments.
```python
from flask import render_template

@app.route("/")
def home():
    return render_template("index.html", name="Alex", tasks=["Study", "Code"])
```
Here `name` and `tasks` become available inside `index.html`.

## Variables
Insert a value with double curly braces `{{ }}`.
```html
<h1>Hello, {{ name }}!</h1>
```
If `name = "Alex"`, this renders `Hello, Alex!`.

## If statements
Logic uses `{% %}` tags. Use `if` to show content conditionally.
```html
{% if tasks %}
  <p>You have tasks to do.</p>
{% else %}
  <p>All done! 🎉</p>
{% endif %}
```
Every `{% if %}` needs a matching `{% endif %}`.

## Loops
Repeat HTML for each item in a list with `for`.
```html
<ul>
  {% for task in tasks %}
    <li>{{ task }}</li>
  {% endfor %}
</ul>
```
This prints one `<li>` per task. Loops need `{% endfor %}`.

## Template inheritance
Avoid repeating the same header/footer on every page. Create a **base template** with
"blocks" that child pages fill in.

`templates/base.html`:
```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <title>{% block title %}My Site{% endblock %}</title>
  </head>
  <body>
    <nav>My Navbar</nav>

    {% block content %}{% endblock %}

    <footer>© 2026</footer>
  </body>
</html>
```

`templates/index.html`:
```html
{% extends "base.html" %}

{% block title %}Home{% endblock %}

{% block content %}
  <h1>Welcome home</h1>
{% endblock %}
```
The child page reuses the base layout and only fills in the blocks. This keeps every
page consistent.

## `url_for`
Never hard-code URLs or file paths — build them with `url_for()`. It takes the **function
name** of a route (or `'static'` for files).
```html
<!-- link to the route whose view function is named about -->
<a href="{{ url_for('about') }}">About</a>

<!-- link to a static CSS file -->
<link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}" />
```
Why use it? If you change a URL later, `url_for` updates automatically — hard-coded links
would break.

### Common mistakes
- Missing `{% endif %}` / `{% endfor %}` — Jinja will raise an error.
- Using `{{ }}` for logic — use `{% %}` for `if`/`for`, `{{ }}` only for output.
- Passing data to `render_template` but referencing a different variable name in the
  template.
- Hard-coding `/about` instead of `url_for('about')`.

---

### Quick review
- `render_template("file.html", key=value)` renders a template with data.
- `{{ value }}` outputs data; `{% if %}` / `{% for %}` do logic (with `endif`/`endfor`).
- `{% extends "base.html" %}` + `{% block %}` share a layout across pages.
- Use `url_for('view_name')` and `url_for('static', filename='...')` instead of
  hard-coded paths.

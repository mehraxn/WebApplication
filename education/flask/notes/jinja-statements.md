# README: Jinja `{% statement %}` in Flask

This guide explains **Jinja statements** in Flask templates in a clear and practical way.

---

## 1. What is `{% statement %}`?

In Flask, when you return an HTML file with `render_template()`, Flask uses **Jinja** to process that HTML file before sending it to the browser.

Jinja has special syntax:

* `{{ ... }}` → print a value
* `{% ... %}` → run a statement or instruction
* `{# ... #}` → comment inside the template

So `{% statement %}` is used for **template logic**.

It tells Jinja to do things like:

* loop over data
* check conditions
* define blocks
* include another file
* extend a base template
* set a variable

It is not mainly used to display text directly. It is used to **control what gets built in the final HTML**.

---

## 2. Where is `{% statement %}` used?

It is used in the **HTML template file**, not in the Flask Python file.

### Flask file

In `app.py`, you prepare data and send it to the template:

```python
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    user = "Mera"
    return render_template("index.html", user=user)
```

### HTML template file

In `templates/index.html`, you use Jinja syntax:

```html
<h1>Home Page</h1>
{% if user %}
    <p>Hello {{ user }}</p>
{% endif %}
```

### Simple idea

* **Flask file** = prepares the data
* **HTML template** = uses Jinja to display and control the page

---

## 3. Why do we need `{% statement %}`?

Without Jinja statements, your HTML would be static.

That means you would have to manually write everything.

For example, if you had 100 products, you would have to type 100 `<li>` lines by hand.

With Jinja statements, you can:

* loop through products
* show or hide sections
* reuse layouts
* keep HTML cleaner and smarter

---

## 4. Difference between `{{ ... }}` and `{% ... %}`

This is the most important distinction.

### `{{ ... }}`

Used to **print** a value.

```html
<p>{{ username }}</p>
```

If `username = "Mera"`, the browser receives:

```html
<p>Mera</p>
```

### `{% ... %}`

Used to **control logic**.

```html
{% if username %}
    <p>{{ username }}</p>
{% endif %}
```

This checks whether `username` exists, and only then prints it.

### Easy rule

* `{{ ... }}` = show data
* `{% ... %}` = do something

---

## 5. The most common Jinja statements

These are the statement tags you will use most often:

```jinja
{% if ... %}
{% elif ... %}
{% else %}
{% endif %}

{% for ... in ... %}
{% endfor %}

{% set ... = ... %}

{% include "file.html" %}
{% extends "base.html" %}

{% block content %}
{% endblock %}
```

---

## 6. Example: `if` statement

### Template

```html
{% if logged_in %}
    <p>Welcome back!</p>
{% endif %}
```

### Meaning

This means:

> Only show this paragraph if `logged_in` is true.

### Flask

```python
@app.route("/")
def home():
    return render_template("index.html", logged_in=True)
```

### Output

```html
<p>Welcome back!</p>
```

If `logged_in=False`, nothing inside the `if` block appears.

---

## 7. Example: `if / else`

### Template

```html
{% if age >= 18 %}
    <p>Adult</p>
{% else %}
    <p>Minor</p>
{% endif %}
```

### Meaning

This means:

* if age is 18 or more, show `Adult`
* otherwise, show `Minor`

---

## 8. Example: `if / elif / else`

### Template

```html
{% if score >= 90 %}
    <p>Grade A</p>
{% elif score >= 80 %}
    <p>Grade B</p>
{% elif score >= 70 %}
    <p>Grade C</p>
{% else %}
    <p>Grade D</p>
{% endif %}
```

This is useful when you have multiple possible conditions.

---

## 9. Example: `for` loop

### Template

```html
<ul>
{% for fruit in fruits %}
    <li>{{ fruit }}</li>
{% endfor %}
</ul>
```

### Flask

```python
@app.route("/")
def home():
    fruits = ["Apple", "Banana", "Cherry"]
    return render_template("index.html", fruits=fruits)
```

### Output

```html
<ul>
    <li>Apple</li>
    <li>Banana</li>
    <li>Cherry</li>
</ul>
```

### Meaning

This means:

> Take each item from `fruits` and repeat the `<li>` line.

---

## 10. Example: `for` loop with dictionaries

### Flask

```python
@app.route("/")
def home():
    students = [
        {"name": "Ali", "passed": True},
        {"name": "Sara", "passed": False}
    ]
    return render_template("index.html", students=students)
```

### Template

```html
<ul>
{% for student in students %}
    <li>
        {{ student.name }}
        {% if student.passed %}
            - Passed
        {% else %}
            - Failed
        {% endif %}
    </li>
{% endfor %}
</ul>
```

### Output

```html
<ul>
    <li>Ali - Passed</li>
    <li>Sara - Failed</li>
</ul>
```

This shows that statements can be nested inside other statements.

---

## 11. Nested statements

Jinja statements can be placed inside each other.

Example:

```html
{% for product in products %}
    <div>
        <h3>{{ product.name }}</h3>

        {% if product.available %}
            <p>Available</p>
        {% else %}
            <p>Out of stock</p>
        {% endif %}
    </div>
{% endfor %}
```

This means:

* loop through all products
* for each product, check if it is available
* then show the correct message

---

## 12. Example: `set`

You can create a variable inside the template.

```html
{% set city = "Rome" %}
<p>{{ city }}</p>
```

Output:

```html
<p>Rome</p>
```

Another example:

```html
{% set full_name = first_name + " " + last_name %}
<p>{{ full_name }}</p>
```

This is less common than `if` and `for`, but still useful.

---

## 13. Example: `include`

`include` inserts another template file.

### main template

```html
<h1>My Website</h1>
{% include "menu.html" %}
<p>Welcome to the page.</p>
```

### `menu.html`

```html
<ul>
    <li>Home</li>
    <li>About</li>
    <li>Contact</li>
</ul>
```

This helps you reuse small pieces of HTML.

Common uses:

* navbar
* footer
* sidebar
* reusable form parts

---

## 14. Example: `extends` and `block`

These are used for template inheritance.

### `base.html`

```html
<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}My Site{% endblock %}</title>
</head>
<body>
    <header>Header</header>

    {% block content %}{% endblock %}

    <footer>Footer</footer>
</body>
</html>
```

### `home.html`

```html
{% extends "base.html" %}

{% block title %}Home{% endblock %}

{% block content %}
    <h1>Welcome</h1>
    <p>This is the homepage.</p>
{% endblock %}
```

### Meaning

* `extends` says: use the base layout
* `block` says: replace this section with new content

This is very common in real Flask projects.

---

## 15. Example using `loop` inside `for`

Inside a `for` loop, Jinja gives you a special variable called `loop`.

### Show item number

```html
{% for fruit in fruits %}
    <p>{{ loop.index }} - {{ fruit }}</p>
{% endfor %}
```

Output:

```html
<p>1 - Apple</p>
<p>2 - Banana</p>
<p>3 - Cherry</p>
```

### Check the first item

```html
{% for fruit in fruits %}
    {% if loop.first %}
        <p>This is the first fruit:</p>
    {% endif %}
    <p>{{ fruit }}</p>
{% endfor %}
```

Useful loop values include:

* `loop.index` → starts at 1
* `loop.index0` → starts at 0
* `loop.first` → true for first item
* `loop.last` → true for last item

---

## 16. Full Flask example

### `app.py`

```python
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    user_name = "Mera"
    logged_in = True
    fruits = [
        {"name": "Apple", "color": "Red", "available": True},
        {"name": "Banana", "color": "Yellow", "available": True},
        {"name": "Cherry", "color": "Dark Red", "available": False}
    ]

    return render_template(
        "index.html",
        user_name=user_name,
        logged_in=logged_in,
        fruits=fruits
    )
```

### `templates/index.html`

```html
<!DOCTYPE html>
<html>
<head>
    <title>Jinja Demo</title>
</head>
<body>
    <h1>Fruit Page</h1>

    {% if logged_in %}
        <p>Hello, {{ user_name }}</p>
    {% else %}
        <p>Please log in.</p>
    {% endif %}

    {% if fruits %}
        <ul>
        {% for fruit in fruits %}
            <li>
                {{ loop.index }}. {{ fruit.name }} - {{ fruit.color }}
                {% if fruit.available %}
                    (Available)
                {% else %}
                    (Out of stock)
                {% endif %}
            </li>
        {% endfor %}
        </ul>
    {% else %}
        <p>No fruits found.</p>
    {% endif %}
</body>
</html>
```

### What this example teaches

It shows all of these concepts together:

* `{{ user_name }}` prints a variable
* `{% if logged_in %}` checks a condition
* `{% if fruits %}` checks whether the list is empty
* `{% for fruit in fruits %}` loops through items
* nested `{% if fruit.available %}` checks each fruit
* `{{ loop.index }}` gives the item number

---

## 17. How Jinja rendering works

When a user opens a page:

1. The browser sends a request to Flask.
2. Flask runs the matching route function.
3. Flask prepares data in Python.
4. Flask calls `render_template()`.
5. Jinja reads the HTML template.
6. Jinja processes all `{{ ... }}` and `{% ... %}` parts.
7. Jinja creates the final plain HTML.
8. Flask sends that final HTML to the browser.

So the browser does **not** see raw Jinja code. The browser receives the finished HTML after Jinja has processed it.

---

## 18. Common beginner mistakes

### Mistake 1: Using `{% ... %}` in Python file

Wrong:

```python
{% if user %}
```

This is invalid in Python.

Jinja syntax belongs in HTML template files.

---

### Mistake 2: Forgetting to close statements

Wrong:

```html
{% if user %}
    <p>Hello {{ user }}</p>
```

Correct:

```html
{% if user %}
    <p>Hello {{ user }}</p>
{% endif %}
```

---

### Mistake 3: Confusing `{{ ... }}` with `{% ... %}`

Wrong:

```html
{{ if user }}
```

Correct:

```html
{% if user %}
```

Use `{{ ... }}` only for values you want to print.

---

### Mistake 4: Placing template files outside `templates/`

Flask expects HTML templates inside a folder named `templates`.

Correct structure:

```text
project/
│ app.py
└── templates/
    └── index.html
```

---

### Mistake 5: Forgetting to send variables from Flask

If your template uses:

```html
{{ user_name }}
```

then Flask must send that variable:

```python
return render_template("index.html", user_name="Mera")
```

---

## 19. Quick cheat sheet

### Print a variable

```html
{{ name }}
```

### If statement

```html
{% if condition %}
    ...
{% endif %}
```

### If / else

```html
{% if condition %}
    ...
{% else %}
    ...
{% endif %}
```

### For loop

```html
{% for item in items %}
    {{ item }}
{% endfor %}
```

### Set a variable

```html
{% set x = 10 %}
```

### Include another file

```html
{% include "menu.html" %}
```

### Extend a base template

```html
{% extends "base.html" %}
```

### Define a block

```html
{% block content %}{% endblock %}
```

---

## 20. Best way to understand it

A useful way to think about Jinja is this:

* Flask gives the template **data**
* Jinja uses statements to decide **how to build the page**
* The browser receives the **final HTML only**

Another simple memory trick:

* `%` = logic
* `{{ }}` = output

So when you see this:

```html
{% for fruit in fruits %}
    <li>{{ fruit }}</li>
{% endfor %}
```

Read it like this:

* instruction: loop through fruits
* output: print each fruit

---

## 21. Practice examples

### Practice 1: Show a login message

```html
{% if logged_in %}
    <p>Welcome!</p>
{% else %}
    <p>Please log in.</p>
{% endif %}
```

### Practice 2: Show products

```html
<ul>
{% for product in products %}
    <li>{{ product }}</li>
{% endfor %}
</ul>
```

### Practice 3: Show pass/fail

```html
{% if mark >= 50 %}
    <p>Passed</p>
{% else %}
    <p>Failed</p>
{% endif %}
```

### Practice 4: Number the items

```html
{% for name in names %}
    <p>{{ loop.index }}. {{ name }}</p>
{% endfor %}
```

---

## 22. Final summary

`{% statement %}` in Jinja means:

> a control instruction written inside an HTML template that tells Jinja what to do before the page is sent to the browser.

It is used for things like:

* conditions
* loops
* variables
* blocks
* including files
* template inheritance

### In one sentence

* **Flask file** prepares data
* **HTML template** uses `{% ... %}` and `{{ ... }}`
* **Jinja** turns the template into final HTML

---

## 23. Mini glossary

### Flask

A Python web framework used to build web applications.

### Template

An HTML file that can contain Jinja syntax.

### Jinja

The template engine Flask uses.

### Statement

An instruction inside `{% ... %}`.

### Expression

A value inside `{{ ... }}` that gets printed.

### Render

The process of turning a template plus data into final HTML.

---

## 24. One final example to remember forever

### Flask

```python
@app.route("/")
def home():
    names = ["Ali", "Sara", "John"]
    show_title = True
    return render_template("index.html", names=names, show_title=show_title)
```

### HTML

```html
{% if show_title %}
    <h1>Student Names</h1>
{% endif %}

<ul>
{% for name in names %}
    <li>{{ name }}</li>
{% endfor %}
</ul>
```

### Meaning

* `if` decides whether the title appears
* `for` repeats the list item
* `{{ name }}` prints each name

That is the core idea of Jinja statements.

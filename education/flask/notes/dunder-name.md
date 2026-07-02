# Understanding `__name__` in Python and Flask

## 1. What does “dunder name” mean

In Python, you often see this special variable

```python
__name__
```

This is usually called dunder name.

The word dunder means

```text
double underscore
```

So when we say dunder name, we mean

```python
__name__
```

It has two underscores before `name` and two underscores after `name`.

---

## 2. `__name__` is a special Python variable

`__name__` is not created by us.

Python creates it automatically for every Python file.

For example, suppose we have this file

```text
app.py
```

Inside `app.py`, we can write

```python
print(__name__)
```

The value of `__name__` depends on how the file is used.

There are two main situations

1. The file is run directly.
2. The file is imported into another file.

---

# Part 1 `__name__` outside Flask

Before understanding Flask, we need to understand `__name__` in normal Python.

---

## 3. When a Python file is run directly

Imagine we have a file called `main.py`

```python
print(__name__)
```

Now we run it directly in the terminal

```bash
python main.py
```

The output will be

```text
__main__
```

Why

Because when Python runs a file directly, it gives that file this special name

```python
__main__
```

So in this case

```python
__name__ == __main__
```

This means

```text
This file is the main file currently being executed.
```

---

## 4. When a Python file is imported

Now imagine we have two files

```text
main.py
helper.py
```

Inside `helper.py`, we write

```python
print(__name__)
```

Inside `main.py`, we write

```python
import helper
```

Now we run `main.py`

```bash
python main.py
```

The output will be

```text
helper
```

Why

Because `helper.py` was not run directly.

It was imported.

So Python gives it the name of the module

```python
__name__ == helper
```

The important rule is

```text
If a file is run directly, __name__ becomes __main__.
If a file is imported, __name__ becomes the filemodule name.
```

---

## 5. Why do we use this condition

You will often see this code

```python
if __name__ == __main__
    print(This file is running directly)
```

This means

```text
Only run this code if this file is the main file.
```

So if the file is run directly, the code inside the `if` block runs.

But if the file is imported, the code inside the `if` block does not run.

---

## 6. Simple example

Create a file called `helper.py`

```python
print(This line always runs)

if __name__ == __main__
    print(helper.py is running directly)
else
    print(helper.py was imported)
```

If we run it directly

```bash
python helper.py
```

Output

```text
This line always runs
helper.py is running directly
```

But if another file imports it

```python
import helper
```

Output

```text
This line always runs
helper.py was imported
```

So the condition helps Python know whether the file is the main program or just an imported helper file.

---

## 7. Why is this useful

This is useful because sometimes we want some code to run only when the file is started directly.

For example

```python
def say_hello()
    print(Hello)

if __name__ == __main__
    say_hello()
```

Here, the function `say_hello()` only runs if this file is run directly.

But if another file imports this file, the function does not automatically run.

This is useful because importing a file should not always start the whole program.

---

# Part 2 `__name__` in Flask

Now that we understand `__name__` in normal Python, we can understand why Flask uses it.

A simple Flask app usually looks like this

```python
from flask import Flask

app = Flask(__name__)

@app.route()
def home()
    return Hello Flask

if __name__ == __main__
    app.run(debug=True)
```

There are two important places where `__name__` appears

```python
app = Flask(__name__)
```

and

```python
if __name__ == __main__
    app.run(debug=True)
```

They are related, but they do different jobs.

---

## 8. First use `app = Flask(__name__)`

This line creates the Flask application

```python
app = Flask(__name__)
```

Let us break it down.

### `Flask`

`Flask` is the class that creates a Flask web application.

We imported it here

```python
from flask import Flask
```

### `app`

`app` is the variable that stores our Flask application object.

The name `app` is common, but we could technically use another name.

For example

```python
my_website = Flask(__name__)
```

But most Flask developers use

```python
app = Flask(__name__)
```

### `__name__`

Here, `__name__` tells Flask where the application is located.

Flask uses this information to find important project folders, such as

```text
templates
static
```

The `templates` folder usually contains HTML files.

The `static` folder usually contains CSS files, JavaScript files, images, and other static files.

So this line

```python
app = Flask(__name__)
```

means

```text
Create a Flask app and use this Python file as the starting point to locate project files.
```

---

## 9. Why does Flask need `__name__`

Flask needs to know the location of your app so it can find files like

```text
templatesindex.html
staticstyle.css
staticimageslogo.png
```

For example, this Flask route may render an HTML file

```python
@app.route()
def home()
    return render_template(index.html)
```

When Flask sees

```python
render_template(index.html)
```

it looks inside the `templates` folder.

But to find the `templates` folder correctly, Flask needs to know where the app is located.

That is why we give Flask

```python
__name__
```

---

## 10. Example project structure

Imagine your project looks like this

```text
my_project
│
├── app.py
│
├── templates
│   └── index.html
│
└── static
    └── style.css
```

In `app.py`, we write

```python
from flask import Flask, render_template

app = Flask(__name__)

@app.route()
def home()
    return render_template(index.html)
```

Because we used

```python
app = Flask(__name__)
```

Flask understands that it should look near `app.py` for these folders

```text
templates
static
```

---

## 11. Second use `if __name__ == __main__`

At the bottom of many Flask apps, you see this

```python
if __name__ == __main__
    app.run(debug=True)
```

This is normal Python, not only Flask.

It means

```text
Only start the Flask development server if this file is run directly.
```

So if we run

```bash
python app.py
```

then

```python
__name__ == __main__
```

So this line runs

```python
app.run(debug=True)
```

That starts the Flask development server.

---

## 12. What does `app.run(debug=True)` do

This line starts the Flask development server

```python
app.run(debug=True)
```

It allows us to open our web app in the browser.

For example, Flask may show something like

```text
Running on http127.0.0.15000
```

Then we can visit that address in the browser.

### `debug=True`

The option

```python
debug=True
```

is useful while developing because it can

1. Show helpful error messages.
2. Restart the server when we change the code.

But it should not be used in a real production website.

It is mainly for development and learning.

---

## 13. Why not just write `app.run(debug=True)` without the `if`

We could write

```python
app.run(debug=True)
```

without

```python
if __name__ == __main__
```

But that is usually not a good habit.

Why

Because if another Python file imports this Flask app, the server may start automatically.

That can cause problems.

Example

```python
import app
```

If `app.py` has this directly

```python
app.run(debug=True)
```

then importing `app.py` could start the server immediately.

That is not always what we want.

So we protect it like this

```python
if __name__ == __main__
    app.run(debug=True)
```

This means

```text
Do not start the server when this file is imported.
Only start it when this file is run directly.
```

---

## 14. Full Flask example with explanation

Here is a simple Flask app

```python
from flask import Flask

app = Flask(__name__)

@app.route()
def home()
    return Hello Flask

if __name__ == __main__
    app.run(debug=True)
```

Now let us explain each important line.

---

### Line 1

```python
from flask import Flask
```

This imports the `Flask` class from the Flask library.

We need this class to create a Flask web application.

---

### Line 3

```python
app = Flask(__name__)
```

This creates the Flask application.

`__name__` tells Flask where this app is located.

Flask uses it to find folders like

```text
templates
static
```

---

### Line 5

```python
@app.route()
```

This is a route decorator.

It tells Flask

```text
When the user visits the homepage URL ``, run the function below.
```

The `` route means the homepage.

---

### Line 6

```python
def home()
```

This defines a Python function called `home`.

Flask will run this function when the user visits ``.

---

### Line 7

```python
return Hello Flask
```

This sends a response back to the browser.

The browser will show

```text
Hello Flask
```

---

### Line 9

```python
if __name__ == __main__
```

This checks whether this file is being run directly.

If the file is run directly, the condition is true.

If the file is imported, the condition is false.

---

### Line 10

```python
app.run(debug=True)
```

This starts the Flask development server.

Because it is inside the `if` block, it only runs when this file is run directly.

---

## 15. Important difference between the two uses of `__name__`

In Flask, these two uses of `__name__` are different

```python
app = Flask(__name__)
```

and

```python
if __name__ == __main__
    app.run(debug=True)
```

### `Flask(__name__)`

This gives Flask information about the app location.

It helps Flask find project files.

### `if __name__ == __main__`

This checks whether the file is being run directly.

It controls whether the server should start.

So remember

```text
Flask(__name__) helps Flask locate the app.
if __name__ == __main__ controls when the server starts.
```

---

## 16. Is `__name__` a Flask feature

No.

`__name__` is not originally from Flask.

It is a Python feature.

Flask uses it because it is useful.

So the correct idea is

```text
__name__ belongs to Python.
Flask uses __name__ to understand the app location.
```

---

## 17. Very simple final summary

`__name__` is a special Python variable.

When a file is run directly

```python
__name__ == __main__
```

When a file is imported

```python
__name__ == file_name
```

In Flask

```python
app = Flask(__name__)
```

means

```text
Create a Flask app and tell Flask where this app is located.
```

And

```python
if __name__ == __main__
    app.run(debug=True)
```

means

```text
Start the Flask server only when this file is run directly.
```

---

## 18. The most important thing to remember

Do not think `__name__` is only for Flask.

It is a Python special variable.

Flask just uses it in two common places

```python
app = Flask(__name__)
```

and

```python
if __name__ == __main__
    app.run(debug=True)
```

The first one helps Flask find your project.

The second one decides whether to start the server.

# Flask Project Structure

Flask is a small Python web framework. It doesn't force a folder layout on you, but
there's a **standard structure** that almost every Flask project uses. Learning it early
means your projects stay organized and understandable.

## A typical small Flask project
```
myapp/
├── app.py             # the main application file
├── requirements.txt   # list of Python packages the project needs
├── README.md          # what the project is and how to run it
├── templates/         # HTML files (Jinja templates)
│   ├── base.html
│   └── index.html
└── static/            # CSS, JavaScript, images
    ├── style.css
    └── logo.png
```

## `app.py`
The heart of the app. It creates the Flask application and defines the routes (URLs).
```python
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, Flask!"

if __name__ == "__main__":
    app.run(debug=True)
```
Bigger projects split this into multiple files, but for learning, one `app.py` is fine.

## `templates/`
Holds your **HTML files**. Flask looks in this exact folder name when you call
`render_template("index.html")`. Templates can contain Jinja placeholders like
`{{ name }}` that Flask fills in with real data.

## `static/`
Holds files that don't change on the server: **CSS, JavaScript, and images**. You link
to them with `url_for('static', filename='style.css')`. Flask serves this folder
automatically at the `/static/` URL.

## `requirements.txt`
A plain text list of the packages your project needs, so anyone can install them in one
command.
```
Flask==3.0.0
```
Install everything with:
```bash
pip install -r requirements.txt
```
Create it from your current environment with `pip freeze > requirements.txt`.

## `README.md`
Explains what the project does and how to run it — the first thing a recruiter or
teammate reads. Include the purpose, setup steps, and how to start the app.

## Why structure matters
- **Flask expects it** — `templates/` and `static/` must be named exactly that, or
  `render_template` and `url_for('static', ...)` won't find your files.
- **Readability** — anyone (including future you) can find things fast.
- **Scalability** — a tidy structure makes it easy to grow the app later.
- **Professionalism** — a clean layout with a `requirements.txt` and `README.md` is what
  employers expect to see.

---

### Quick review
- `app.py` = app + routes; run with `app.run(debug=True)`.
- `templates/` = HTML (used by `render_template`); `static/` = CSS/JS/images.
- `requirements.txt` lists packages; install with `pip install -r requirements.txt`.
- The `templates/` and `static/` folder names are required by Flask.

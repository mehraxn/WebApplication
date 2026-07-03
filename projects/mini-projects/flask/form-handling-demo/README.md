# Flask Form Handling Demo

## Project Overview
A simple Flask app demonstrating how HTML forms send data to Flask, with separate files for
the Python app, the HTML template, and the CSS. A practice project focused on the connection
between a form's `name` attributes and `request.form`.

## Features
- A form that submits data to Flask
- Reads submitted values with `request.form`
- Separate `app.py`, template, and stylesheet

## Technologies Used
- Python 3
- Flask
- Jinja2 templates
- CSS

## Folder Structure
```
form-handling-demo/
├── app.py            # handles the form (GET/POST)
├── templates/
│   └── index.html    # the form
├── static/
│   └── style.css     # styling
├── README.md         # this file
└── screenshots/      # add screenshots here
```

## How to Run or Open
```bash
pip install flask
python app.py
```
Then open **http://127.0.0.1:5000** in your browser.

## What I Learned
- The HTML input `name` attributes are the keys Flask uses in `request.form`.
  ```html
  <input type="text" name="name">
  ```
  ```python
  name = request.form.get("name")
  ```
- How to keep Flask, HTML, and CSS in separate files.
- The basic flow of submitting a form and reading it on the server.

## Resume Value
Form handling is the foundation of every interactive web app. This shows I understand
exactly how HTML forms connect to Flask's `request.form`.

## Future Improvements
- Add server-side validation and flash messages
- Add a redirect-after-POST result page
- Expand into a full CRUD example

# Jinja Fruit List

## Project Overview
A small Flask app that passes a list of items from Python to a template and renders it
with a Jinja loop. A practice project focused on the basics of dynamic templates.

## Features
- Passes a Python list to a template
- Renders the list with a Jinja `for` loop
- Minimal, single-route app

## Technologies Used
- Python 3
- Flask
- Jinja2 templates

## Folder Structure
```
jinja-fruit-list/
├── app.py           # single route passing a list
├── templates/
│   └── index.html   # loops over the list
├── static/          # (assets, if any)
├── README.md        # this file
└── screenshots/     # add screenshots here
```

## How to Run or Open
```bash
pip install flask
python app.py
```
Then open http://127.0.0.1:5000 in your browser.

## What I Learned
- How to pass data from a view function to a template.
- Using a Jinja `{% for %}` loop to render a list.
- The basic Flask request → template flow.

## Resume Value
Rendering dynamic data is the heart of any web app. This shows I understand how Flask and
Jinja work together to produce dynamic pages.

## Future Improvements
- Load the list from a database instead of hard-coding it
- Add an `{% if %}` fallback for an empty list
- Style the page with CSS

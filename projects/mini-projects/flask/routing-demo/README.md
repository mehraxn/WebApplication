# Routing Demo

## Project Overview
A small Flask app demonstrating basic routing — mapping different URLs to different view
functions and templates. A practice project focused on Flask's routing fundamentals.

## Features
- Multiple routes (home and about)
- Each route renders its own template
- Minimal, easy-to-follow structure

## Technologies Used
- Python 3
- Flask
- Jinja2 templates

## Folder Structure
```
routing-demo/
├── app.py            # defines the routes
├── templates/
│   ├── index.html    # home page
│   └── about.html    # about page
├── statics/          # (assets, if any)
├── README.md         # this file
└── screenshots/      # add screenshots here
```

## How to Run or Open
```bash
pip install flask
python app.py
```
Then open http://127.0.0.1:5000 in your browser.

## What I Learned
- How `@app.route` maps a URL to a view function.
- Rendering a different template per route.
- The basics of navigating between pages in Flask.

## Resume Value
Routing is the backbone of every Flask app. This shows I understand how URLs connect to
Python code and templates.

## Future Improvements
- Add a shared base template with navigation
- Add a dynamic route with a URL parameter
- Style the pages with CSS

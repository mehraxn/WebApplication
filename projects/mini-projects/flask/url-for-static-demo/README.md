# url_for & Static Files Demo

## Project Overview
A small Flask app demonstrating how to serve static files (CSS, images) and build links
with `url_for`. A practice project focused on connecting a Flask app to its static assets.

## Features
- Serves static files from the `static/` folder
- Uses `url_for('static', filename=...)` to link assets
- Home and about routes

## Technologies Used
- Python 3
- Flask
- Jinja2 templates

## Folder Structure
```
url-for-static-demo/
├── app.py           # routes
├── templates/
│   └── home.html    # home page linking static files
├── static/          # CSS / images
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
- How Flask serves files from the `static/` folder.
- Building safe, portable links with `url_for('static', filename=...)`.
- Why hard-coded `/static/` paths should be avoided.

## Resume Value
Every real Flask app needs CSS and images. This shows I know the correct, portable way to
link static assets in Flask.

## Future Improvements
- Add a JavaScript file and link it with `url_for`
- Add a shared base template
- Organize static files into `css/`, `js/`, and `images/` subfolders

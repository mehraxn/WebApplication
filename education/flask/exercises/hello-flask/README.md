# Exercise: Hello Flask

## Goal
Create the simplest possible Flask app: a single route that returns some text.

## Concepts practiced
- Creating a Flask app (`Flask(__name__)`)
- Defining a route with `@app.route`
- Returning a response from a view function
- Running the app with `app.run(debug=True)`

## How to run
```bash
pip install flask
python app.py
```
Then open http://127.0.0.1:5000 in your browser.

## Files included
- `app.py` — the Flask app
- `README.md` — this file

## What I learned
- A Flask app maps URLs to Python functions with `@app.route`.
- Whatever a view function returns is sent to the browser.
- `debug=True` reloads the server automatically while developing.

## Difficulty
Beginner

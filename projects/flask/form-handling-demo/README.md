# Flask Form Example

This is a simple Flask app with separate files for Flask, HTML, and CSS.

## Project Structure

```text
flask_form_app/
├── app.py
├── templates/
│   └── index.html
└── static/
    └── style.css
```

## How to Run

Install Flask:

```bash
pip install flask
```

Run the app:

```bash
python app.py
```

Then open this address in your browser:

```text
http://127.0.0.1:5000
```

## Important Idea

The HTML input `name` attributes are the keys Flask uses in `request.form`.

Example:

```html
<input type="text" name="name">
```

In Flask:

```python
name = request.form.get("name")
```

So the `name=""` attribute in HTML connects the form field to Flask.

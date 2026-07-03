# Flask Flash Messages

Flash messages are short, one-time notifications — "Saved successfully!", "Invalid
password" — shown to the user after an action, then gone. Flask has this built in with
`flash()` and `get_flashed_messages()`.

## The secret key (required first)
Flash messages are stored in the user's **session**, which Flask signs with a secret
key. Without one, flashing raises an error. Set it once when creating the app.
```python
from flask import Flask
app = Flask(__name__)
app.secret_key = "change-this-to-a-random-secret"
```
In real projects the key should be random and kept out of the code (see the security
note about environment variables).

## `flash()`
Call `flash("message")` in a view to queue a message for the next page the user sees.
```python
from flask import flash, redirect, url_for

@app.route("/save", methods=["POST"])
def save():
    # ... save something ...
    flash("Your changes were saved!")
    return redirect(url_for("home"))
```

## `get_flashed_messages()`
In your template, loop over the queued messages and display them. They appear once, then
clear automatically.
```html
{% for message in get_flashed_messages() %}
  <div class="alert">{{ message }}</div>
{% endfor %}
```
Put this near the top of your base template so messages show on every page.

## Success / error messages (categories)
You can tag a message with a **category** (like "success" or "error") to style it
differently.
```python
flash("Account created!", "success")
flash("Wrong password.", "error")
```
Then read the category too, using `with_categories=True`:
```html
{% for category, message in get_flashed_messages(with_categories=True) %}
  <div class="alert alert-{{ category }}">{{ message }}</div>
{% endfor %}
```
If the category matches a Bootstrap class (e.g. `success`, `danger`), `alert-{{ category }}`
gives you colored alerts for free. (Note: Bootstrap uses `danger`, not `error`, so you
may flash with `"danger"` to match.)

## Full mini example
```python
@app.route("/login", methods=["POST"])
def login():
    password = request.form.get("password", "")
    if password == "secret":
        flash("Welcome back!", "success")
        return redirect(url_for("home"))
    flash("Incorrect password.", "danger")
    return redirect(url_for("login_page"))
```

### Common mistakes
- **Runtime error when flashing** — you forgot to set `app.secret_key`.
- Flashing but never rendering `get_flashed_messages()` in a template, so nothing shows.
- Flashing then returning a template instead of **redirecting** — flash is designed to
  survive a redirect (the PRG pattern).
- Category `"error"` not matching Bootstrap's `alert-danger` — use `"danger"`.

---

### Quick review
- Set `app.secret_key` or flashing won't work.
- `flash("msg", "category")` queues a one-time message.
- Loop `get_flashed_messages(with_categories=True)` in the template to show them.
- Flash then `redirect(...)` — messages persist across the redirect and clear after
  showing once.

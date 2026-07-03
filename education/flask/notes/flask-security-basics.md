# Flask Security Basics

You don't need to be a security expert to avoid the most common, dangerous mistakes.
These beginner-level habits will keep your Flask apps reasonably safe.

## 1. Never trust user input
Anything that comes from the user — form fields, URL parameters, query strings — could be
wrong, empty, or malicious. Always validate and use safe techniques.

**Use `?` placeholders for SQL (prevents SQL injection):**
```python
# BAD — an attacker could inject SQL through `name`
conn.execute(f"SELECT * FROM users WHERE name = '{name}'")

# GOOD — the value is safely escaped
conn.execute("SELECT * FROM users WHERE name = ?", (name,))
```

**Jinja auto-escapes output (prevents most XSS):**
```html
<!-- Safe: Jinja escapes HTML in `comment` automatically -->
<p>{{ comment }}</p>
```
Avoid the `| safe` filter on user-provided content — it turns escaping off.

Also validate presence and types (see the error-handling note) before acting on input.

## 2. Password hashing (concept)
**Never store passwords as plain text.** If your database leaks, every password is
exposed. Instead store a **hash** — a scrambled, one-way version. At login you hash the
entered password and compare hashes.

Werkzeug (installed with Flask) provides helpers:
```python
from werkzeug.security import generate_password_hash, check_password_hash

# when a user registers:
hashed = generate_password_hash("user_password")   # store this, not the raw password

# when they log in:
check_password_hash(hashed, "entered_password")     # True if it matches
```
Key idea: you can go password → hash, but not hash → password. You never "unhash."

## 3. Environment variables (keep secrets out of code)
Don't hard-code secrets (API keys, the secret key, DB passwords) in your source — they'd
end up on GitHub. Read them from the **environment** instead.
```python
import os
app.secret_key = os.environ.get("SECRET_KEY")
```
Set the variable outside the code (in your shell, a `.env` file that's git-ignored, or the
hosting platform's settings). This keeps secrets private and lets each environment use
different values.

## 4. The secret key
Flask uses `app.secret_key` to sign sessions and flash messages. It should be:
- **Random and long** (not `"secret"` or `"123"`).
- **Kept out of the code** (load it from an environment variable).
- **Different in production** than in development.
```python
app.secret_key = os.environ.get("SECRET_KEY", "dev-only-fallback")
```
If the key leaks, attackers could tamper with sessions.

## 5. Don't run debug mode in production
`debug=True` is great while developing (auto-reload, error pages), but **dangerous
live**: its error pages can expose your code and even allow running code on the server.
```python
# fine for local development
app.run(debug=True)

# in production: debug OFF (and use a real server like gunicorn)
app.run(debug=False)
```
Rule: debug on for learning on your machine, debug off for anything public.

### Common mistakes
- Building SQL with f-strings instead of `?` placeholders.
- Storing plain-text passwords.
- Hard-coding secret keys/API keys in the code and pushing them to GitHub.
- Leaving `debug=True` on a live site.
- Using `| safe` on user content, disabling Jinja's XSS protection.

---

### Quick review
- Never trust user input: `?` placeholders for SQL, let Jinja escape output.
- Store password **hashes** (`generate_password_hash` / `check_password_hash`), never
  plain text.
- Keep the secret key and other secrets in **environment variables**, not in code.
- Use a strong, random `secret_key`.
- Turn **off** `debug` in production.

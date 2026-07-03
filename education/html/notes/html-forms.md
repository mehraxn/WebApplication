# HTML Forms

Forms are how users send data to a website — logging in, signing up, searching, contacting. As a Flask developer you'll build forms constantly, so learn this well.

## The `<form>` tag
Wraps all the fields. Two important attributes: `action` (where the data goes) and `method` (how it's sent).

```html
<form action="/submit" method="POST">
  <!-- fields go here -->
</form>
```

## `<input>` and input types
`<input>` is the most common field. The `type` attribute changes what it does.

```html
<input type="text" name="username" />
<input type="email" name="email" />
<input type="password" name="password" />
<input type="number" name="age" />
<input type="date" name="birthday" />
<input type="tel" name="phone" />
<input type="url" name="website" />
```
The browser gives helpful behavior automatically — e.g. `type="email"` checks for an `@`, `type="password"` hides the text.

## `<label>`
A label describes a field. Connect it to an input with `for` matching the input's `id`. Clicking the label then focuses the input — great for usability and accessibility.

```html
<label for="username">Username</label>
<input type="text" id="username" name="username" />
```

## `<textarea>`
A multi-line text box (messages, comments).
```html
<label for="message">Message</label>
<textarea id="message" name="message" rows="4"></textarea>
```

## `<select>` (dropdown)
A dropdown menu of choices.
```html
<label for="country">Country</label>
<select id="country" name="country">
  <option value="it">Italy</option>
  <option value="us">United States</option>
</select>
```
The `value` is what gets sent; the text is what the user sees.

## Checkbox
For "choose any / none / all." Each can be checked independently.
```html
<label>
  <input type="checkbox" name="terms" /> I agree to the terms
</label>
```

## Radio button
For "choose exactly one." Give them the **same `name`** so only one can be selected at a time.
```html
<label><input type="radio" name="plan" value="free" /> Free</label>
<label><input type="radio" name="plan" value="pro" /> Pro</label>
```

## Submit button
Sends the form.
```html
<button type="submit">Send</button>
<!-- or -->
<input type="submit" value="Send" />
```

## `required` attribute
Stops the form from submitting if the field is empty. A quick, built-in validation.
```html
<input type="email" name="email" required />
```

## `name` attribute (very important)
The `name` is the **key** used when the data is sent to the server. Without a `name`, the field's value is not sent at all.

If you submit `<input name="email" value="a@b.com">`, the server receives `email = a@b.com`.
In Flask you'd read it with `request.form["email"]`.

## `method`: GET vs POST (beginner level)
- **GET** — data is added to the URL (`/search?q=cats`). Use it for searches and things that are safe to bookmark or repeat. Not for passwords (the data shows in the URL).
- **POST** — data is sent in the request body, hidden from the URL. Use it for logins, sign-ups, and anything that creates or changes data.

```html
<form action="/login" method="POST">
  ...
</form>
```

Rule of thumb: **GET = reading/searching, POST = sending/saving.**

---

### Quick review
- Every field needs a `name` or its value won't be sent.
- Match `<label for>` to the input's `id`.
- Same `name` groups radio buttons together.
- `required` = simple built-in check.
- GET puts data in the URL; POST hides it in the body.

# Exercise: Accessible Contact Form

## Goal
Build a contact form that includes labels, several input fields, a textarea, a
select dropdown, a checkbox, and a submit button — all connected accessibly.

## Concepts practiced
- The `<form>` tag with `action` and `method="POST"`
- Different input types: `text`, `email`, `tel`
- Connecting `<label>` to inputs with `for` and `id`
- `<textarea>` for multi-line input
- `<select>` with `<option>` values
- Checkbox with a wrapping label
- `<button type="submit">`
- The `required` attribute for basic validation
- The `name` attribute (the key sent to the server)

## Files included
- `index.html` — the contact form
- `README.md` — this file

## What I learned
- Every field needs a `name` or its value won't be sent to the server.
- Labels connected with `for`/`id` make the form usable for screen readers and
  let users click the label to focus the field.
- `required` stops the form submitting when key fields are empty.
- `POST` is the right method for sending/saving data (vs `GET` for reading).
- These are the exact fields I'll later read in Flask with `request.form`.

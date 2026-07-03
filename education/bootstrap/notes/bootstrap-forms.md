# Bootstrap Forms

Bootstrap makes forms look clean and consistent with a few classes. Since you'll build
lots of forms as a Flask developer, this is worth knowing well.

## `form-control` (text inputs & textareas)
Add `form-control` to inputs and textareas for the standard styled look (full width,
padding, border, focus ring).
```html
<input type="text" class="form-control" />
<input type="email" class="form-control" placeholder="you@example.com" />
<textarea class="form-control" rows="3"></textarea>
```

## `form-label` (labels)
Add `form-label` to `<label>` for correct spacing. Keep the label connected to its
input with `for` + `id`.
```html
<label for="name" class="form-label">Full name</label>
<input type="text" id="name" class="form-control" />
```

A field is usually wrapped in a spacing div:
```html
<div class="mb-3">
  <label for="email" class="form-label">Email</label>
  <input type="email" id="email" class="form-control" />
</div>
```
The `mb-3` adds space below each field so they don't touch.

## `form-select` (dropdowns)
Use `form-select` (not `form-control`) on `<select>` elements.
```html
<label for="country" class="form-label">Country</label>
<select id="country" class="form-select">
  <option value="it">Italy</option>
  <option value="us">United States</option>
</select>
```

## Checks (checkboxes & radios)
Wrap each in a `form-check`; the input gets `form-check-input` and the label
`form-check-label`.
```html
<!-- Checkbox -->
<div class="form-check">
  <input type="checkbox" id="agree" class="form-check-input" />
  <label for="agree" class="form-check-label">I agree to the terms</label>
</div>

<!-- Radio group (same name = pick one) -->
<div class="form-check">
  <input type="radio" name="plan" id="free" class="form-check-input" />
  <label for="free" class="form-check-label">Free</label>
</div>
<div class="form-check">
  <input type="radio" name="plan" id="pro" class="form-check-input" />
  <label for="pro" class="form-check-label">Pro</label>
</div>
```
For a toggle switch look, add `form-switch` to the wrapper.

## Validation styling basics
Bootstrap gives colored feedback classes you can apply to show valid/invalid fields.

Manual styling with `is-valid` / `is-invalid`:
```html
<input type="email" class="form-control is-invalid" />
<div class="invalid-feedback">Please enter a valid email.</div>

<input type="text" class="form-control is-valid" />
<div class="valid-feedback">Looks good!</div>
```
- `is-invalid` turns the field red and shows the `invalid-feedback` text.
- `is-valid` turns it green and shows the `valid-feedback` text.

This pairs perfectly with server-side validation in Flask: if the server finds an
error, render the field with `is-invalid` and show the message.

A complete small form:
```html
<form>
  <div class="mb-3">
    <label for="user" class="form-label">Username</label>
    <input type="text" id="user" class="form-control" required />
  </div>
  <div class="mb-3">
    <label for="pass" class="form-label">Password</label>
    <input type="password" id="pass" class="form-control" required />
  </div>
  <div class="form-check mb-3">
    <input type="checkbox" id="remember" class="form-check-input" />
    <label for="remember" class="form-check-label">Remember me</label>
  </div>
  <button type="submit" class="btn btn-primary">Log in</button>
</form>
```

### Common mistakes
- Using `form-control` on a `<select>` — use **`form-select`** instead.
- Forgetting the `form-check` wrapper, so checkboxes/radios look misaligned.
- Leaving off `for`/`id` on labels — bad for accessibility even with Bootstrap.
- Expecting `is-invalid` to appear automatically — you (or JS/Flask) apply it.

---

### Quick review
- Inputs/textareas → `form-control`; selects → `form-select`; labels → `form-label`.
- Checkboxes/radios → `form-check` + `form-check-input` + `form-check-label`.
- Wrap fields in `mb-3` for spacing.
- Show errors with `is-invalid` + `invalid-feedback` (great with Flask validation).

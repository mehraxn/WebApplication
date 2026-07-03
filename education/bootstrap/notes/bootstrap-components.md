# Bootstrap Components

Components are **ready-made UI pieces** you drop into your HTML with the right classes.
Here are the ones you'll use in almost every project.

## Buttons
Use `btn` plus a color class.
```html
<button class="btn btn-primary">Primary</button>
<button class="btn btn-secondary">Secondary</button>
<button class="btn btn-success">Success</button>
<button class="btn btn-danger">Danger</button>
<button class="btn btn-outline-primary">Outline</button>
```
Sizes: `btn-lg`, `btn-sm`. Full width: `w-100`.
```html
<button class="btn btn-primary btn-lg w-100">Big full-width button</button>
```

## Cards
A flexible content box with an optional image, title, text, and buttons.
```html
<div class="card" style="width: 18rem;">
  <div class="card-body">
    <h5 class="card-title">Card title</h5>
    <p class="card-text">Some quick example text.</p>
    <a href="#" class="btn btn-primary">Go somewhere</a>
  </div>
</div>
```
Key classes: `card`, `card-body`, `card-title`, `card-text`, `card-img-top`.

## Navbar
A responsive navigation bar that collapses into a "hamburger" menu on small screens.
(Needs the Bootstrap JS bundle for the toggle to work.)
```html
<nav class="navbar navbar-expand-md navbar-dark bg-dark">
  <div class="container-fluid">
    <a class="navbar-brand" href="#">MySite</a>
    <button class="navbar-toggler" data-bs-toggle="collapse" data-bs-target="#menu">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="menu">
      <ul class="navbar-nav">
        <li class="nav-item"><a class="nav-link" href="#">Home</a></li>
        <li class="nav-item"><a class="nav-link" href="#">About</a></li>
      </ul>
    </div>
  </div>
</nav>
```
- `navbar-expand-md` → full menu from medium screens up, collapsed below.
- `navbar-dark bg-dark` → dark theme.

## Alerts
Colored message boxes for feedback.
```html
<div class="alert alert-success">Saved successfully!</div>
<div class="alert alert-danger">Something went wrong.</div>
<div class="alert alert-warning">Please double-check this.</div>
<div class="alert alert-info">Just so you know…</div>
```
Great for showing Flask flash messages later.

## Badges
Small labels for counts or statuses.
```html
<span class="badge bg-primary">New</span>
<span class="badge bg-danger">3</span>
<button class="btn btn-primary">
  Inbox <span class="badge bg-light text-dark">5</span>
</button>
```

## Forms
Styled form controls (covered in depth in `bootstrap-forms.md`).
```html
<form>
  <label for="email" class="form-label">Email</label>
  <input type="email" id="email" class="form-control" />
  <button type="submit" class="btn btn-primary mt-2">Send</button>
</form>
```

## Modal
A pop-up dialog on top of the page. (Needs the JS bundle.)
```html
<!-- Button that opens the modal -->
<button class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#myModal">
  Open modal
</button>

<!-- The modal itself -->
<div class="modal" id="myModal" tabindex="-1">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title">Title</h5>
        <button class="btn-close" data-bs-dismiss="modal"></button>
      </div>
      <div class="modal-body">Modal content goes here.</div>
      <div class="modal-footer">
        <button class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
      </div>
    </div>
  </div>
</div>
```
The `data-bs-toggle` / `data-bs-target` attributes wire the button to the modal.

### Common mistakes
- **Interactive components not working** (navbar toggle, modal) — you forgot the
  Bootstrap **JS bundle** before `</body>`.
- Wrong `data-bs-target` id — it must match the modal's `id` with a leading `#`.
- Missing structural classes (e.g. `card-body` inside `card`) so styling looks off.

---

### Quick review
- `btn btn-*` for buttons, `card` + `card-body` for cards, `alert alert-*` for messages.
- Navbar and modal need the **JS bundle** and matching `data-bs-target` ids.
- `badge bg-*` for small labels.
- Components = whole widgets; combine with utilities to adjust spacing/alignment.

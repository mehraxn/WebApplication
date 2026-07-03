# Bootstrap Overview

## What is Bootstrap?
Bootstrap is the most popular **CSS framework**. It's a big, ready-made stylesheet
(plus some JavaScript) full of pre-built classes and components — buttons, cards,
navbars, grids, forms — so you can build good-looking, responsive pages fast without
writing all the CSS yourself.

You style elements by adding **class names** to your HTML:
```html
<button class="btn btn-primary">Save</button>
```
That one class gives you a styled, colored, padded button instantly.

## Why developers use it
- **Speed** — build a professional layout in minutes, not hours.
- **Responsive by default** — its grid and utilities adapt to phones, tablets, and
  desktops automatically.
- **Consistency** — everything follows one design system, so a site looks uniform.
- **Cross-browser** — it handles browser quirks for you.
- **Huge community** — tons of examples, themes, and answers online.

## CDN usage (the fastest way to start)
The easiest way to add Bootstrap is via a **CDN** (a link to files hosted online) — no
downloads, no build step. Put the CSS in `<head>` and the JS bundle before `</body>`:

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <!-- Bootstrap CSS -->
    <link
      href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css"
      rel="stylesheet"
    />
    <title>My Page</title>
  </head>
  <body>
    <button class="btn btn-primary">Hello Bootstrap</button>

    <!-- Bootstrap JS bundle (needed for navbar toggle, modals, etc.) -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
  </body>
</html>
```
The **CSS link** is required for styling. The **JS bundle** is only needed for
interactive components (modals, dropdowns, the mobile navbar toggle).

## Components vs utilities
Bootstrap gives you two kinds of classes — knowing the difference clears up a lot of
confusion:

- **Components** = complete, pre-built UI pieces. One "thing" made of several classes.
  Examples: `card`, `navbar`, `modal`, `alert`, `btn`.
  ```html
  <div class="alert alert-warning">Careful!</div>
  ```
- **Utilities** = tiny, single-purpose helper classes that change one property. You mix
  and match them.
  Examples: `m-3` (margin), `text-center`, `d-flex`, `bg-light`, `p-2` (padding).
  ```html
  <div class="d-flex justify-content-center p-3">...</div>
  ```

Rule of thumb: **components** give you a whole widget; **utilities** fine-tune spacing,
alignment, colors, and layout.

## When NOT to use Bootstrap
Bootstrap is great, but it's not always the right choice:
- **You need a very custom, unique design** — fighting Bootstrap's defaults can be more
  work than writing your own CSS.
- **You want a tiny page** — loading the whole framework for one button is overkill.
- **You're learning CSS fundamentals** — lean on plain CSS first so you actually
  understand the box model, Flexbox, and Grid (Bootstrap is built on those).
- **Every site looks "Bootstrappy"** — without customization, sites can look generic.

A good path: learn plain CSS first, then use Bootstrap to move faster on real projects.

---

### Quick review
- Bootstrap = a CSS framework of ready-made classes and components.
- Add it fast via the CDN: CSS in `<head>`, JS bundle before `</body>`.
- **Components** = full widgets (card, navbar); **utilities** = one-property helpers (`m-3`, `text-center`).
- Skip it for highly custom designs or when learning core CSS.

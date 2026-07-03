# Bootstrap Education

This section covers **Bootstrap**, the most popular CSS framework. It lets you build
responsive, professional-looking pages quickly using ready-made classes and components.
Because it's built on top of CSS (Flexbox, the box model, media queries), it's the
natural next step after the CSS section.

## Overview

- **`notes/`** — clear, beginner-friendly notes on each core Bootstrap topic, written
  for quick project and interview review. Every note explains the class names in plain
  English with practical code examples.
- **`exercises/`** — hands-on practice files that apply the ideas from the notes *(to be
  added)*.

> Tip: to try any example, add the Bootstrap CDN to your HTML — CSS link in `<head>`,
> and the JS bundle before `</body>` for interactive components (navbar toggle, modals).

## Notes table

| File | What it covers |
|------|----------------|
| `notes/bootstrap-overview.md` | What Bootstrap is, why it's used, CDN setup, components vs utilities, when not to use it. |
| `notes/bootstrap-grid.md` | `container`, `row`, `col`, `col-md-*`, breakpoints, and the 12-column system. |
| `notes/bootstrap-utilities.md` | Margin, padding, text, display, flex, and background utility classes. |
| `notes/bootstrap-components.md` | Buttons, cards, navbar, alerts, badges, forms, and modals. |
| `notes/bootstrap-forms.md` | `form-control`, `form-label`, `form-select`, checks, and validation styling. |
| `notes/bootstrap-responsive-layout.md` | Mobile-first design, responsive columns, hiding/showing elements, spacing by breakpoint. |

## Exercises table

Each exercise is a self-contained folder with an `index.html` (loaded via the Bootstrap
CDN) and a `README.md` (goal, concepts, important classes, difficulty).

| Exercise | Bootstrap concepts | Difficulty |
|----------|--------------------|------------|
| `exercises/bootstrap-navbar/` | Responsive navbar with collapse toggler | Beginner |
| `exercises/bootstrap-alerts-badges/` | Alerts (incl. dismissible) and badges | Beginner |
| `exercises/bootstrap-card-grid/` | Grid + cards, responsive columns, `h-100` | Beginner+ |
| `exercises/bootstrap-form-layout/` | Styled form controls centered with the grid | Beginner+ |
| `exercises/bootstrap-responsive-columns/` | 1→2→3 columns across breakpoints | Beginner+ |
| `exercises/bootstrap-modal-practice/` | Modal triggered with data attributes | Intermediate |
| `exercises/bootstrap-pricing-section/` | Pricing cards with grid, highlight, flex utils | Intermediate |

## Recommended study order

Work through the notes in this order — each builds on the previous:

1. **`bootstrap-overview.md`** — start here to understand what Bootstrap is and how to
   add it.
2. **`bootstrap-grid.md`** — the grid is the foundation of every Bootstrap layout.
3. **`bootstrap-utilities.md`** — spacing, text, flex, and color helpers you'll use
   everywhere.
4. **`bootstrap-components.md`** — the ready-made UI pieces (buttons, cards, navbar…).
5. **`bootstrap-forms.md`** — styled forms, key for a Flask developer.
6. **`bootstrap-responsive-layout.md`** — ties it together with responsive, mobile-first
   design.

## Skills learned

After this section you'll be able to:

- Add Bootstrap to any page via the CDN.
- Build responsive layouts with the 12-column grid.
- Style spacing, text, colors, and alignment with utility classes.
- Use pre-built components (buttons, cards, navbar, alerts, badges, modals).
- Create clean, styled forms with validation feedback.
- Make pages adapt across phones, tablets, and desktops using breakpoints.

These are the Bootstrap skills expected of a junior web / Flask developer building real,
responsive interfaces quickly.

# Exercise: CSS Variables Theme

## Goal
Build a small page that uses CSS variables for colors, spacing, and font sizes, so
the whole theme can be changed from one place.

## CSS concepts practiced
- Defining global variables in `:root`
- Custom properties (`--primary`, `--space-md`, `--font-lg`, etc.)
- Using variables with `var()`
- A reusable color palette and spacing scale
- Applying the same variables across multiple components

## Files included
- `index.html` — themed cards and buttons
- `style.css` — variables defined in `:root` and used throughout
- `README.md` — this file

## What I learned
- Defining values once in `:root` and reading them with `var()` keeps a design
  consistent and makes global changes a one-line edit.
- A spacing scale (`--space-sm/md/lg`) keeps padding and gaps consistent across the
  page.
- Variables cascade, so they could be overridden for a dark theme or a section.

## Difficulty
Beginner+

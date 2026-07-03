# Exercise: Grid Photo Gallery

## Goal
Build a responsive image/gallery grid using CSS Grid that adjusts the number of
columns automatically as the screen size changes.

## CSS concepts practiced
- `display: grid`
- `grid-template-columns` with `repeat()`
- `auto-fit` to create as many columns as fit
- `minmax(180px, 1fr)` for flexible column sizing
- `gap` between grid items
- Centering content inside tiles with Flexbox

## Files included
- `index.html` — gallery markup (colored tiles as image placeholders)
- `style.css` — CSS Grid layout
- `README.md` — this file

## What I learned
- `repeat(auto-fit, minmax(180px, 1fr))` is a one-line responsive grid — it fits as
  many columns as possible and wraps the rest, with no media queries.
- Grid handles two dimensions (rows *and* columns) at once, unlike Flexbox.
- `1fr` makes columns share the remaining space evenly.

## Difficulty
Beginner+

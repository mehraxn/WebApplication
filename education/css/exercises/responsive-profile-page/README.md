# Exercise: Responsive Profile Page

## Goal
Build a simple profile layout that stacks vertically on mobile and switches to a
side-by-side layout on desktop using a media query.

## CSS concepts practiced
- Mobile-first design (base styles for small screens)
- `@media (min-width: 700px)` to enhance for larger screens
- Switching `flex-direction` from `column` to `row`
- The `flex` shorthand for a fixed sidebar (`flex: 0 0 250px`) and flexible content
  (`flex: 1`)
- `max-width` + `margin: 0 auto` to center the layout

## Files included
- `index.html` — sidebar + content layout
- `style.css` — responsive styles with a media query
- `README.md` — this file

## What I learned
- Writing the mobile layout first and then adding a `min-width` media query is the
  clean, modern approach.
- A single media query can completely change a layout by flipping `flex-direction`.
- `flex: 0 0 250px` fixes the sidebar width while `flex: 1` lets the content take the
  remaining space.

## Difficulty
Intermediate

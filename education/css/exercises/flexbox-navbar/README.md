# Exercise: Flexbox Navbar

## Goal
Build a responsive navigation bar using Flexbox, with a brand on the left and links
on the right that wrap on small screens.

## CSS concepts practiced
- `display: flex` on the container
- `justify-content: space-between` to push brand and links apart
- `align-items: center` for vertical alignment
- `flex-wrap: wrap` so links drop below on narrow screens
- `gap` for spacing between links
- Nested flex (the links group is its own flex row)
- `:hover` on links

## Files included
- `index.html` — navbar markup
- `style.css` — flexbox styles
- `README.md` — this file

## What I learned
- `justify-content` controls spacing along the main (horizontal) axis, while
  `align-items` handles the cross (vertical) axis.
- `space-between` is the classic "logo left, menu right" pattern.
- `flex-wrap: wrap` makes the navbar adapt to small screens without media queries.
- `gap` is cleaner than adding margins to each link.

## Difficulty
Beginner

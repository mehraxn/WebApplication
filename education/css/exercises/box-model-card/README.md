# Exercise: Box Model Card

## Goal
Build a simple card that demonstrates how `margin`, `padding`, `border`, `width`,
and `box-sizing` work together.

## CSS concepts practiced
- `width` on a block element
- `padding` (space inside the box)
- `border` (line around the padding)
- `margin` (space outside the box, `auto` to center)
- `box-sizing: border-box` so width includes padding + border
- `border-radius` for rounded corners

## Files included
- `index.html` — the card markup
- `style.css` — box model styles
- `README.md` — this file

## What I learned
- Padding is *inside* the box and takes the background; margin is *outside* and is
  transparent.
- With `box-sizing: border-box`, a `width: 320px` card stays 320px wide even with
  padding and a border — without it, the box would be wider than expected.
- `margin: 24px auto` centers a fixed-width block horizontally.

## Difficulty
Beginner

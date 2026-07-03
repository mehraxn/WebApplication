# Exercise: Positioning Badge Card

## Goal
Build a product card with a discount badge placed in the corner using absolute
positioning.

## CSS concepts practiced
- `position: relative` on the parent as a positioning anchor
- `position: absolute` on the badge to place it precisely
- `top` / `right` offsets
- `z-index` to stack the badge above the image
- `overflow: hidden` with `border-radius` for clean rounded corners
- `box-shadow` for depth

## Files included
- `index.html` — product card with a badge
- `style.css` — positioning styles
- `README.md` — this file

## What I learned
- An `absolute` element positions itself relative to its nearest **positioned**
  ancestor — so the parent card needs `position: relative`, or the badge would jump
  to the page corner.
- `top` and `right` place the badge exactly in the card's corner.
- `z-index` decides what sits on top when elements overlap (badge over image).

## Difficulty
Intermediate

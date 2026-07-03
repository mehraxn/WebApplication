# Exercise: Flexbox Pricing Row

## Goal
Build three pricing cards in a row using Flexbox that wrap onto multiple lines on
small screens.

## CSS concepts practiced
- `display: flex` with `flex-wrap: wrap`
- `gap` between cards
- `justify-content: center` to center the row
- The `flex` shorthand (`flex: 1 1 240px` — grow, shrink, ideal width)
- `list-style: none` to clean up the feature lists
- Highlighting one card with a border and `transform: scale()`

## Files included
- `index.html` — three pricing cards
- `style.css` — flexbox layout
- `README.md` — this file

## What I learned
- `flex: 1 1 240px` lets each card grow to fill space but wrap when there isn't
  enough room for its ideal width.
- `flex-wrap: wrap` is what turns a fixed row into a responsive layout — the cards
  stack on narrow screens automatically.
- `gap` spaces the cards evenly without margins.

## Difficulty
Beginner+

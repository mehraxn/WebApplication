# Exercise: Hover Transition Buttons

## Goal
Build several buttons that each demonstrate a different smooth hover transition.

## CSS concepts practiced
- `transition` on the base element (so it animates both in and out)
- `transform: scale()` for growing
- `transform: translateY()` for a "lift" effect
- `box-shadow` on hover for depth
- Animating `background` and `color` for a color/fill change
- `:hover` pseudo-class

## Files included
- `index.html` — four buttons
- `style.css` — hover transition styles
- `README.md` — this file

## What I learned
- The `transition` belongs on the **base** button rule, not the `:hover` rule, so the
  effect is smooth both when entering and leaving hover.
- `transform` (scale/translate) is smoother than animating layout properties and
  doesn't push other elements around.
- Combining `translateY` with `box-shadow` creates the popular "lift" effect.

## Difficulty
Beginner+

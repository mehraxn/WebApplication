# Responsive Pricing Cards

## Project Overview
A clean, responsive pricing page with three plans. The middle "Pro" plan is highlighted as
the most popular, and each card lifts on hover. Built with plain HTML and CSS — no
frameworks.

## Features
- Three pricing plans (Starter, Pro, Business)
- Featured plan highlight with a "Most popular" tag
- Responsive layout that wraps and stacks on small screens
- Hover lift effect on each card
- Call-to-action buttons with hover transitions

## Technologies Used
- HTML5
- CSS3 (Flexbox, CSS variables, transitions — no Bootstrap)

## Folder Structure
```
responsive-pricing-cards/
├── index.html    # the pricing page
├── style.css     # styling
├── README.md     # this file
└── screenshots/  # add screenshots here
```

## How to Run or Open
Open `index.html` directly in any web browser. Resize the window to see the responsive
behavior.

## What I Learned
- CSS variables (`:root`) for a reusable color and spacing palette.
- Flexbox with `flex-wrap` for a responsive card row.
- `transition` + `transform` for hover lift effects and `position: absolute` for the tag.

## Resume Value
A common real-world marketing component that is responsive, polished, and uses design
tokens (CSS variables) — a very frequent front-end task.

## Future Improvements
- Add a monthly/yearly billing toggle (needs JavaScript)
- Add icons to feature lists
- Add a dark theme by overriding the CSS variables

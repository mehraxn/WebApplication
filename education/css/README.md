# CSS Education

This section covers **CSS** — the language that styles and lays out web pages. After
HTML gives a page its structure, CSS controls how it *looks*: colors, spacing, layout,
responsiveness, and motion. These are core skills for any front-end or Flask developer.

## Section overview

- **`notes/`** — clear, beginner-friendly notes on each core CSS topic, written for quick
  exam and interview review. Every note explains the concept in plain English, shows
  practical code, and calls out common mistakes.
- **`exercises/`** — hands-on practice files that apply the ideas from the notes *(to be
  added)*.

## Recommended study order

Work through the notes in this order — each builds on the previous:

1. **`css-selectors.md`** — how to target elements; you need this before anything else.
2. **`css-box-model.md`** — how size, padding, border, and margin work.
3. **`css-positioning.md`** — static, relative, absolute, fixed, sticky, z-index.
4. **`css-flexbox.md`** — one-dimensional layout (rows/columns).
5. **`css-grid.md`** — two-dimensional layout (grids and galleries).
6. **`responsive-design.md`** — make it work on every screen size.
7. **`css-transitions-animations.md`** — add smooth motion and hover effects.
8. **`css-variables.md`** — reusable colors and spacing; ties everything together.

## Notes table

| File | What it covers |
|------|----------------|
| `notes/css-selectors.md` | Element, class, id, descendant, grouping selectors; `:hover` and specificity basics. |
| `notes/css-box-model.md` | Content, padding, border, margin, width/height, and `box-sizing: border-box`. |
| `notes/css-positioning.md` | `static`, `relative`, `absolute`, `fixed`, `sticky`, `z-index`, and common mistakes. |
| `notes/css-flexbox.md` | `display: flex`, `flex-direction`, `justify-content`, `align-items`, `gap`, `flex-wrap`, layouts. |
| `notes/css-grid.md` | `display: grid`, `grid-template-columns`, `gap`, `repeat()`, `minmax()`, responsive grids. |
| `notes/responsive-design.md` | Viewport, relative units, `max-width`, media queries, mobile-first design. |
| `notes/css-transitions-animations.md` | `transition`, `transform`, hover effects, and `@keyframes` animations. |
| `notes/css-variables.md` | `:root`, custom properties, and reusable colors/spacing. |

## Exercises table

Each exercise is a self-contained folder with `index.html`, `style.css`, and a
`README.md` (goal, concepts, files, what I learned, difficulty). No Bootstrap — plain
HTML and CSS only.

| Exercise | Main concept | Difficulty |
|----------|--------------|------------|
| `exercises/box-model-card/` | Box model: padding, border, margin, `box-sizing` | Beginner |
| `exercises/flexbox-navbar/` | Flexbox navbar (`space-between`, `align-items`, wrap) | Beginner |
| `exercises/flexbox-pricing-row/` | Flexbox row of cards that wraps (`flex`, `flex-wrap`) | Beginner+ |
| `exercises/grid-photo-gallery/` | CSS Grid responsive gallery (`auto-fit`, `minmax`) | Beginner+ |
| `exercises/positioning-badge-card/` | `position: absolute` badge on a `relative` card, `z-index` | Intermediate |
| `exercises/responsive-profile-page/` | Media queries + mobile-first layout switch | Intermediate |
| `exercises/hover-transition-buttons/` | `transition` + `transform` hover effects | Beginner+ |
| `exercises/css-variables-theme/` | CSS variables in `:root` for colors, spacing, fonts | Beginner+ |

## Skills learned

After completing this section you'll be able to:

- Target exactly the elements you want with the right selectors.
- Control spacing and sizing confidently using the box model.
- Position elements and build overlays, sticky headers, and floating buttons.
- Build modern layouts with **Flexbox** and **Grid**.
- Make pages **responsive** across phones, tablets, and desktops.
- Add smooth **transitions and animations** for a polished feel.
- Keep styles clean and consistent using **CSS variables**.

These are exactly the CSS fundamentals expected of a junior web / Flask developer.

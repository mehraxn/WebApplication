# CSS Grid

Grid is a layout tool for **two dimensions** — rows *and* columns at the same time. Where Flexbox handles a single line, Grid handles full page layouts and image/card grids.

```css
.container {
  display: grid;
}
```

## `display: grid`
Makes the element a grid container. Its children become grid items placed into cells.

## `grid-template-columns`
Defines how many columns there are and how wide each is. Each value is one column.
```css
.container {
  display: grid;
  grid-template-columns: 200px 200px 200px;  /* 3 columns, 200px each */
}
```
Use the `fr` unit ("fraction") to share available space:
```css
.container {
  grid-template-columns: 1fr 1fr 1fr;  /* 3 equal flexible columns */
  grid-template-columns: 2fr 1fr;      /* first column twice as wide */
}
```

## `gap`
Space between rows and columns.
```css
.container {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}
```

## `repeat()`
A shortcut so you don't type the same value many times.
```css
/* these two lines are identical */
grid-template-columns: 1fr 1fr 1fr 1fr;
grid-template-columns: repeat(4, 1fr);
```

## `minmax()`
Sets a **minimum and maximum** size for a column: "at least X, at most Y."
```css
grid-template-columns: repeat(3, minmax(150px, 1fr));
/* each column is at least 150px, but grows to share space */
```

## Simple responsive grid (the famous one-liner)
This creates a grid that automatically fits as many columns as will comfortably fit, wrapping to new rows on smaller screens — **no media queries needed**.
```css
.gallery {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
}
```
- `auto-fit` → create as many columns as fit.
- `minmax(200px, 1fr)` → each is at least 200px, then grows evenly.

On a wide screen you might get 5 columns; on a phone, 1 — automatically.

### Common mistakes
- Putting grid properties on the **items** instead of the **container**.
- Forgetting the container needs `display: grid` before any `grid-template-*` works.
- Using fixed `px` columns everywhere, which breaks on small screens — prefer `fr` and `minmax()`.
- Mixing up `auto-fit` and `auto-fill` (start with `auto-fit`; it collapses empty tracks).

## Grid vs Flexbox — which one?
- **Flexbox** → one direction (a row *or* a column). Navbars, button groups.
- **Grid** → two directions (rows *and* columns). Page layouts, galleries, card grids.

---

### Quick review
- `display: grid` + `grid-template-columns` defines the columns.
- `fr` shares space; `repeat(n, ...)` avoids repetition; `minmax()` sets limits.
- `repeat(auto-fit, minmax(200px, 1fr))` = instant responsive grid.
- Grid = 2D, Flexbox = 1D.

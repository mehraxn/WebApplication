# CSS Flexbox

Flexbox is a layout tool for arranging items in **one direction** — a row or a column. It's perfect for navbars, button groups, centering things, and card rows.

Turn any element into a flex **container** and its direct children become flex **items**.

```css
.container {
  display: flex;
}
```

## `display: flex`
Makes the element a flex container. Its children now line up in a row by default.
```html
<div class="container">
  <div>A</div>
  <div>B</div>
  <div>C</div>
</div>
```
```css
.container { display: flex; }   /* A B C sit side by side */
```

## `flex-direction`
Sets the main axis — the direction items flow.
```css
.container {
  flex-direction: row;     /* default: left to right */
  flex-direction: column;  /* top to bottom */
}
```

## `justify-content`
Aligns items **along the main axis** (horizontal in a row).
```css
.container {
  justify-content: flex-start;    /* default: packed at start */
  justify-content: center;        /* centered */
  justify-content: space-between; /* first & last at edges, gaps between */
  justify-content: space-around;  /* equal space around each item */
}
```

## `align-items`
Aligns items **across the cross axis** (vertical in a row).
```css
.container {
  align-items: stretch;     /* default: fill the height */
  align-items: center;      /* vertically centered */
  align-items: flex-start;  /* top */
}
```

**Centering trick** — center anything both ways:
```css
.container {
  display: flex;
  justify-content: center;  /* horizontal */
  align-items: center;      /* vertical */
}
```

## `gap`
Adds space **between** items — cleaner than adding margins to each one.
```css
.container {
  display: flex;
  gap: 16px;
}
```

## `flex-wrap`
By default items squeeze onto one line. `wrap` lets them drop to the next line when there's no room — key for responsive card grids.
```css
.container {
  display: flex;
  flex-wrap: wrap;
}
```

## Common layout examples

**Navbar with logo left, links right:**
```css
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
```

**Responsive card row:**
```css
.cards {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
}
.cards > * {
  flex: 1 1 200px;   /* grow, shrink, ideal width 200px */
}
```

### Common mistakes
- Applying flex properties (`justify-content`, etc.) to the **items** instead of the **container** — they go on the container.
- Confusing `justify-content` (main axis) with `align-items` (cross axis). In a *column*, these swap directions!
- Forgetting `flex-wrap: wrap`, so items overflow instead of wrapping on small screens.
- Using margins for spacing when `gap` is simpler and cleaner.

---

### Quick review
- `display: flex` on the container; children become flex items.
- `justify-content` = main axis, `align-items` = cross axis.
- `center` + `center` = perfect centering.
- `gap` for spacing, `flex-wrap: wrap` for responsiveness.

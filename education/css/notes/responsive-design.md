# Responsive Design

Responsive design means a page **looks good on every screen size** — phones, tablets, and desktops — using one codebase that adapts.

## The viewport meta tag (required first step)
Without this tag in your HTML `<head>`, phones pretend to be a wide desktop and shrink your page. Always include it:
```html
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
```
- `width=device-width` → use the real device width.
- `initial-scale=1.0` → don't zoom by default.

No CSS responsiveness works properly without this.

## Relative units (instead of fixed pixels)
Fixed `px` sizes don't adapt. Relative units scale with the screen or font size.

| Unit | Relative to | Good for |
|------|-------------|----------|
| `%`  | the parent element | widths |
| `rem`| the root font size | font sizes, spacing (consistent) |
| `em` | the element's own font size | spacing tied to text |
| `vw` / `vh` | 1% of viewport width / height | full-screen sections |

```css
.container {
  width: 90%;        /* scales with the screen */
  font-size: 1rem;   /* respects user settings */
  padding: 2rem;
}
```

## `max-width`
A very common pattern: let a box grow but **cap** it so lines don't get too wide on big screens, while still shrinking on small ones.
```css
.container {
  width: 90%;
  max-width: 1100px;   /* never wider than 1100px */
  margin: 0 auto;      /* center it */
}
```
This one rule handles a huge range of screen sizes.

## Media queries
Apply different CSS at different screen widths. A media query is an `if` for the screen.
```css
/* base styles apply to all sizes */
.card { width: 100%; }

/* when the screen is at least 600px wide */
@media (min-width: 600px) {
  .card { width: 50%; }
}

/* at least 900px wide */
@media (min-width: 900px) {
  .card { width: 33%; }
}
```
Common breakpoints (rough): ~600px (phone→tablet), ~900px (tablet→desktop).

## Mobile-first design
Write the styles for **small screens first**, then add `min-width` media queries to enhance for bigger screens. This keeps CSS simpler and matches how most people browse (mobile).

```css
/* mobile: default, single column */
.menu { display: block; }

/* tablet and up: horizontal */
@media (min-width: 700px) {
  .menu { display: flex; gap: 20px; }
}
```
The opposite approach (desktop-first with `max-width` queries) works too, but mobile-first is the modern default.

### Common mistakes
- **Forgetting the viewport meta tag** — the page won't be responsive at all, no matter your CSS.
- **Using fixed `px` widths** everywhere so nothing adapts. Prefer `%`, `rem`, and `max-width`.
- **Too many breakpoints** — let the content decide; don't target specific phone models.
- **Testing only on desktop** — resize the browser or use the device toolbar in DevTools.
- **Fixed heights** that cut off content on small screens.

---

### Quick review
- Always add the viewport meta tag first.
- Use relative units (`%`, `rem`, `vw`) instead of fixed `px`.
- `width: 90%; max-width: …; margin: 0 auto;` is a workhorse pattern.
- Media queries apply CSS at set widths; go **mobile-first** with `min-width`.

# Bootstrap Grid

Bootstrap's grid is how you build **responsive layouts** — arranging content into rows
and columns that adapt to screen size. It's the most important Bootstrap topic.

The grid has three pieces: **container → row → col**.

```html
<div class="container">
  <div class="row">
    <div class="col">Column A</div>
    <div class="col">Column B</div>
  </div>
</div>
```

## `container`
The outer wrapper. It centers your content and adds side padding.
- `container` → a fixed max-width that changes at each breakpoint.
- `container-fluid` → full width, edge to edge.
```html
<div class="container">...</div>
<div class="container-fluid">...</div>
```

## `row`
Goes inside a container and holds columns. Rows use Flexbox under the hood and handle
the spacing (gutters) between columns.
```html
<div class="row">...columns...</div>
```
Always put columns inside a `row`, and rows inside a `container`.

## `col`
Goes inside a row. Plain `col` means "share the space equally."
```html
<div class="row">
  <div class="col">1/3</div>
  <div class="col">1/3</div>
  <div class="col">1/3</div>
</div>
```
Three `col`s automatically each take one third.

## The 12-column system
Every row is divided into **12 invisible columns**. You choose how many each element
spans, and the numbers should add up to 12.
```html
<div class="row">
  <div class="col-4">4 of 12 (one third)</div>
  <div class="col-8">8 of 12 (two thirds)</div>
</div>
```
```html
<div class="row">
  <div class="col-6">Half</div>
  <div class="col-6">Half</div>
</div>
```
If they add up to more than 12, the extra columns wrap to a new line.

## `col-md-*` and responsive breakpoints
This is where the grid becomes **responsive**. The letters (`sm`, `md`, `lg`…) set the
screen size at which the rule kicks in. Bootstrap is **mobile-first**, so a class
applies at that size **and up**.

| Class prefix | Applies from width |
|--------------|--------------------|
| `col-` | all sizes (extra small +) |
| `col-sm-` | ≥ 576px |
| `col-md-` | ≥ 768px |
| `col-lg-` | ≥ 992px |
| `col-xl-` | ≥ 1200px |
| `col-xxl-` | ≥ 1400px |

Common pattern — full width on phones, side by side on desktops:
```html
<div class="row">
  <div class="col-12 col-md-6">Left</div>
  <div class="col-12 col-md-6">Right</div>
</div>
```
- `col-12` → each takes the full row on small screens (stacked).
- `col-md-6` → from medium screens up, each takes half (side by side).

A three-card layout that adapts:
```html
<div class="row">
  <div class="col-12 col-sm-6 col-lg-4">Card</div>
  <div class="col-12 col-sm-6 col-lg-4">Card</div>
  <div class="col-12 col-sm-6 col-lg-4">Card</div>
</div>
```
1 column on phones → 2 on tablets → 3 on large screens.

### Common mistakes
- **Columns not inside a `row`**, or rows not inside a container — spacing breaks.
- **Numbers adding up to more than 12** (unless you *want* wrapping).
- Forgetting the **viewport meta tag** in `<head>` — the responsive breakpoints won't
  work on phones without it.

---

### Quick review
- Structure: `container` → `row` → `col`.
- Rows are 12 columns wide; span numbers should total 12.
- `col-md-6` = half width **from medium screens up** (mobile-first).
- Combine `col-12 col-md-6` to stack on phones and split on desktops.

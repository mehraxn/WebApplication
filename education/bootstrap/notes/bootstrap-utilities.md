# Bootstrap Utilities

Utilities are tiny **single-purpose helper classes** that change one CSS property. You
combine them right in your HTML to fine-tune spacing, text, colors, and layout — no
custom CSS needed. This note covers the ones you'll use constantly.

## Margin utilities (spacing outside)
Pattern: `m` + side + `-` + size.
- Property: `m` = margin.
- Side: `t` top, `b` bottom, `s` start/left, `e` end/right, `x` left+right, `y` top+bottom, or nothing for all sides.
- Size: `0` to `5` (0 = none, 5 = largest), or `auto`.

```html
<div class="m-3">margin on all sides</div>
<div class="mt-2">margin-top small</div>
<div class="mb-4">margin-bottom large</div>
<div class="mx-auto">horizontal auto (centers a fixed-width block)</div>
<div class="my-5">big margin top and bottom</div>
```

## Padding utilities (spacing inside)
Exactly like margins, but `p` for padding. Same sides and sizes.
```html
<div class="p-3">padding all sides</div>
<div class="px-4">padding left and right</div>
<div class="py-2">padding top and bottom</div>
<div class="pt-0">no padding on top</div>
```
Tip: remember `m` = outside, `p` = inside (same as the box model).

## Text utilities
Control alignment, color, weight, and more.
```html
<p class="text-center">Centered text</p>
<p class="text-end">Right-aligned</p>
<p class="text-muted">Gray, secondary text</p>
<p class="fw-bold">Bold text</p>
<p class="fst-italic">Italic text</p>
<p class="text-uppercase">ALL CAPS</p>
<p class="text-primary">Blue (theme) text</p>
```

## Display utilities
Set the CSS `display` value, often per breakpoint.
```html
<span class="d-none">hidden</span>
<div class="d-block">block</div>
<div class="d-inline-block">inline-block</div>
<div class="d-flex">flex container</div>

<!-- responsive: hidden on phones, shown from md up -->
<div class="d-none d-md-block">Visible on tablets and larger</div>
```

## Flex utilities
Turn on Flexbox and control alignment without writing CSS. Use with `d-flex`.
```html
<div class="d-flex justify-content-between align-items-center">
  <span>Left</span>
  <span>Right</span>
</div>
```
Handy ones:
- `justify-content-start | center | end | between | around` (main axis)
- `align-items-start | center | end | stretch` (cross axis)
- `flex-row | flex-column` (direction)
- `flex-wrap` (allow wrapping)
- `gap-2`, `gap-3` (space between items)

```html
<div class="d-flex flex-column gap-2">
  <div>Item 1</div>
  <div>Item 2</div>
</div>
```

## Background utilities
Set background (and often paired text) colors from the theme.
```html
<div class="bg-primary text-white p-3">Primary background</div>
<div class="bg-light p-3">Light gray background</div>
<div class="bg-success text-white p-3">Success green</div>
<div class="bg-danger text-white p-3">Danger red</div>
<div class="bg-warning p-3">Warning yellow</div>
```
Common theme colors: `primary`, `secondary`, `success`, `danger`, `warning`, `info`,
`light`, `dark`.

### Common mistakes
- Forgetting flex utilities need **`d-flex`** first (`justify-content-*` does nothing
  without it).
- Mixing up `m` (margin/outside) and `p` (padding/inside).
- Overusing utilities to the point the HTML is a wall of classes — for repeated
  patterns, a small custom class can be cleaner.

---

### Quick review
- Spacing: `m` = margin, `p` = padding; add side (`t/b/s/e/x/y`) and size (`0–5`).
- `text-center`, `fw-bold`, `text-muted` for text; `bg-*` for backgrounds.
- `d-flex` + `justify-content-*` / `align-items-*` for quick Flexbox layouts.
- Add breakpoints like `d-md-block` to make utilities responsive.

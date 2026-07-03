# Bootstrap Responsive Layout

Responsive layout means your page **adapts to every screen size**. Bootstrap is built
for this — once you understand its breakpoint system, you can control how things look
on phones, tablets, and desktops with just class names.

## Mobile-first design
Bootstrap is **mobile-first**: plain classes (with no breakpoint letter) apply to the
smallest screens **and up**, and you add breakpoint classes to change things on larger
screens. So you design for phones first, then enhance.

The breakpoints:
| Prefix | Kicks in at |
|--------|-------------|
| *(none)* | all sizes (phones +) |
| `sm` | ≥ 576px |
| `md` | ≥ 768px |
| `lg` | ≥ 992px |
| `xl` | ≥ 1200px |
| `xxl` | ≥ 1400px |

A class like `col-md-6` means "half width **from medium up**" — below that it falls
back to the smaller rule (or full width).

## Responsive columns
Stack columns on phones, place them side by side on larger screens by giving each
element two column classes:
```html
<div class="row">
  <div class="col-12 col-md-6 col-lg-4">Item</div>
  <div class="col-12 col-md-6 col-lg-4">Item</div>
  <div class="col-12 col-md-6 col-lg-4">Item</div>
</div>
```
- `col-12` → full width on phones (stacked).
- `col-md-6` → 2 per row on tablets.
- `col-lg-4` → 3 per row on large screens.

## Hiding / showing elements by screen size
Use the display utilities with breakpoints to show or hide content.
```html
<!-- Hidden on phones, visible from md up -->
<div class="d-none d-md-block">Desktop-only content</div>

<!-- Visible on phones, hidden from md up -->
<div class="d-block d-md-none">Mobile-only content</div>
```
This is handy for showing a full menu on desktop but a compact version on mobile.

## Spacing changes by breakpoint
Spacing utilities also accept breakpoints: `p{side}-{breakpoint}-{size}`.
```html
<!-- small padding on phones, larger padding from md up -->
<div class="p-2 p-md-5">...</div>

<!-- no top margin on phones, big top margin on large screens -->
<div class="mt-0 mt-lg-5">...</div>
```
The pattern is: property + side + breakpoint + size, e.g. `px-md-4` = horizontal
padding size 4 from medium screens up.

## A responsive layout example
```html
<div class="container">
  <div class="row">
    <!-- Sidebar: hidden on phones, 1/4 width on desktop -->
    <aside class="col-lg-3 d-none d-lg-block bg-light p-3">Sidebar</aside>
    <!-- Content: full width on phones, 3/4 on desktop -->
    <main class="col-12 col-lg-9 p-3">Main content</main>
  </div>
</div>
```

### Common mistakes
- **Forgetting the viewport meta tag** in `<head>` — none of the responsive behavior
  works on real phones without it:
  ```html
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  ```
- Thinking `col-md-6` means "only medium" — it actually means "medium **and up**."
- Setting only large-screen classes and forgetting how it looks on mobile (test small
  first — mobile-first!).

---

### Quick review
- Bootstrap is mobile-first: no-prefix classes = smallest screens and up.
- Breakpoints: `sm 576`, `md 768`, `lg 992`, `xl 1200`, `xxl 1400`.
- `col-12 col-md-6` stacks on phones, splits on tablets+.
- `d-none d-md-block` hides on phones, shows on desktop; spacing takes breakpoints too (`p-md-5`).
- Always include the viewport meta tag.

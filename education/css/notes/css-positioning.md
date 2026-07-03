# CSS Positioning

The `position` property controls how an element is placed and whether it can be moved with `top`, `right`, `bottom`, and `left`. There are five values to know.

## `static` (the default)
Every element is `static` unless you change it. It sits in the normal document flow, and `top`/`left` etc. have **no effect**.
```css
.box {
  position: static;  /* default — you rarely write this */
}
```

## `relative`
Positioned relative to **where it would normally be**. You can nudge it with `top`/`left`, but the space it originally took is kept.
```css
.box {
  position: relative;
  top: 10px;    /* moves 10px down from its normal spot */
  left: 20px;   /* moves 20px right */
}
```
Its most common use: as an **anchor** for an `absolute` child (see below).

## `absolute`
Removed from the normal flow and positioned relative to its **nearest positioned ancestor** (an ancestor with `position: relative/absolute/fixed`). If there's none, it uses the page.
```css
.parent { position: relative; }   /* the anchor */
.badge {
  position: absolute;
  top: 0;
  right: 0;                        /* sits in the parent's top-right corner */
}
```
Use it for badges, tooltips, dropdowns, "X" close buttons.

## `fixed`
Positioned relative to the **browser window**, and it stays put when you scroll.
```css
.back-to-top {
  position: fixed;
  bottom: 20px;
  right: 20px;   /* always visible in the corner */
}
```
Great for sticky headers, floating buttons, and modals.

## `sticky`
A hybrid: acts `relative` until you scroll to a threshold, then "sticks" like `fixed`.
```css
.nav {
  position: sticky;
  top: 0;   /* sticks to the top once it reaches it while scrolling */
}
```
Perfect for headers that stay visible as you scroll.

## `z-index`
Controls **stacking order** — which element sits on top when they overlap. Higher number = closer to the front. Only works on **positioned** elements (not `static`).
```css
.modal   { position: fixed; z-index: 100; }
.overlay { position: fixed; z-index: 99; }
```

### Common mistakes
- **`top`/`left` doing nothing** — the element is still `static`. Set a `position` first.
- **`absolute` jumping to the page corner** — the parent isn't positioned. Add `position: relative` to the intended anchor.
- **`z-index` not working** — the element has no `position` set, or a parent creates a new stacking context. Give it a position.
- **Overusing `absolute`/`fixed`** for layout — prefer Flexbox/Grid for normal layout and reserve positioning for overlays.
- **`sticky` not sticking** — you forgot to give it a threshold like `top: 0`, or a parent has `overflow: hidden`.

---

### Quick review
- `static` = default (no moving). `relative` = nudge from normal spot + anchor for children.
- `absolute` = positioned inside nearest positioned ancestor. `fixed` = pinned to the window.
- `sticky` = relative until scrolled, then sticks.
- `z-index` needs a positioned element; higher = on top.

# CSS `display` Property — Complete Reference Guide

 Version 1.0  Level Beginner → Advanced  Topic CSS Layout

---

## Table of Contents

1. [What is the `display` Property](#1-what-is-the-display-property)
2. [How Browsers Use It](#2-how-browsers-use-it)
3. [The Box Model Connection](#3-the-box-model-connection)
4. [All Display Values Overview](#4-all-display-values-overview)
5. [`display block`](#5-display-block)
6. [`display inline`](#6-display-inline)
7. [`display inline-block`](#7-display-inline-block)
8. [`display none`](#8-display-none)
9. [`display flex`](#9-display-flex)
10. [`display inline-flex`](#10-display-inline-flex)
11. [`display grid`](#11-display-grid)
12. [`display inline-grid`](#12-display-inline-grid)
13. [`display list-item`](#13-display-list-item)
14. [Table Display Values](#14-table-display-values)
15. [`display contents`](#15-display-contents)
16. [`display flow-root`](#16-display-flow-root)
17. [Global  Keyword Values](#17-global--keyword-values)
18. [Default Display Values for HTML Elements](#18-default-display-values-for-html-elements)
19. [Flex vs Grid — When to Use Which](#19-flex-vs-grid--when-to-use-which)
20. [Accessibility Considerations](#20-accessibility-considerations)
21. [Browser Compatibility](#21-browser-compatibility)
22. [Common Mistakes and How to Fix Them](#22-common-mistakes-and-how-to-fix-them)
23. [Real-World Layout Patterns](#23-real-world-layout-patterns)
24. [Quick Reference Cheatsheet](#24-quick-reference-cheatsheet)

---

## 1. What is the `display` Property

The CSS `display` property is the single most important layout property in CSS. It controls two things simultaneously

1. Outer display type — how the element participates in its parent's layout (does it sit on its own line, or flow inline with text)
2. Inner display type — how the element's own children are arranged inside it (normal flow, flexbox, grid, etc.)

### Syntax

```css
element {
  display value;
}
```

### Why it matters

Without understanding `display`, you cannot
- Center things reliably
- Build navigation bars
- Create card grids
- Control spacing between elements
- Hide and show UI elements

Every HTML element on a page has some display value — either inherited by the browser's default stylesheet (called the user-agent stylesheet) or set explicitly by you in your CSS.

---

## 2. How Browsers Use It

When a browser renders an HTML page, it builds something called the formatting context for each element. The `display` property tells the browser which formatting context to use.

There are several formatting contexts
- Block Formatting Context (BFC) — used by `block`, `flow-root`, `flex`, `grid`
- Inline Formatting Context (IFC) — used by `inline`, `inline-block`
- Flex Formatting Context — used by `flex`, `inline-flex`
- Grid Formatting Context — used by `grid`, `inline-grid`
- Table Formatting Context — used by `table` and related values

Understanding which context an element creates helps predict how it and its children will behave.

---

## 3. The Box Model Connection

Every element with a `display` value other than `none` creates a box. This box has

```
+--------------------------------------------+
                  MARGIN                    
  +--------------------------------------+  
                BORDER                    
    +--------------------------------+    
                PADDING                 
      +--------------------------+      
              CONTENT                 
      +--------------------------+      
    +--------------------------------+    
  +--------------------------------------+  
+--------------------------------------------+
```

The `display` value determines
- Whether the box starts on a new line (`block`) or sits inline (`inline`)
- Whether `width` and `height` apply
- How margin and padding behave
- What layout system is used for the children inside

---

## 4. All Display Values Overview

 Category  Values 
------
 Basic  `block`, `inline`, `inline-block`, `none` 
 Flexible Box  `flex`, `inline-flex` 
 Grid  `grid`, `inline-grid` 
 Table  `table`, `inline-table`, `table-row`, `table-cell`, `table-caption`, `table-row-group`, `table-header-group`, `table-footer-group`, `table-column`, `table-column-group` 
 List  `list-item` 
 Special  `contents`, `flow-root` 
 Global  `inherit`, `initial`, `unset`, `revert`, `revert-layer` 

---

## 5. `display block`

### What it does

A block-level element creates a rectangular box that
- Starts on a new line, pushing everything before it and after it above and below
- Stretches to fill the full available width of its parent by default
- Respects `width`, `height`, `margin`, and `padding` on all four sides
- Stacks vertically with other block elements

### Example

```html
div class=box-aBox Adiv
div class=box-bBox Bdiv
div class=box-cBox Cdiv
```

```css
.box-a, .box-b, .box-c {
  display block;
  width 200px;
  height 50px;
  margin 10px;
  background steelblue;
}
```

Result All three boxes appear one below the other, even though their width is only 200px — not the full page width.

### Margin Collapsing (important!)

A subtle but critical behavior of block elements vertical margins collapse. If two block elements are stacked and the top one has `margin-bottom 20px` while the bottom one has `margin-top 30px`, the space between them is 30px (the larger one), not 50px.

```css
.first  { margin-bottom 20px; }
.second { margin-top 30px; }
 Gap between them = 30px, not 50px 
```

This only happens vertically between block elements and does not happen with flex or grid children.

### Common block elements

`div`, `p`, `h1`–`h6`, `section`, `article`, `header`, `footer`, `main`, `nav`, `aside`, `ul`, `ol`, `form`, `figure`, `blockquote`, `pre`, `hr`

---

## 6. `display inline`

### What it does

An inline element
- Stays in the same line as surrounding content (like words in a sentence)
- Only takes up as much width as its content requires
- Does not start a new line
- Does not respond to `width` or `height` declarations
- Top and bottom margins have no effect; left and right margins work normally
- Top and bottom padding is applied visually but does not push other elements away

### Example

```html
p
  This is a span class=highlighthighlighted wordspan inside a sentence.
p
```

```css
.highlight {
  display inline;
  background yellow;
  padding 2px 5px;
}
```

Result The highlighted word sits naturally within the text without breaking the line.

### What does NOT work on inline elements

```css
span {
  display inline;
  width 200px;     ❌ Has no effect 
  height 50px;     ❌ Has no effect 
  margin-top 20px;     ❌ No effect on layout 
  margin-bottom 20px;  ❌ No effect on layout 
}
```

### Common inline elements

`span`, `a`, `strong`, `em`, `code`, `label`, `abbr`, `cite`, `time`, `small`, `sup`, `sub`, `b`, `i`, `u`

---

## 7. `display inline-block`

### What it does

`inline-block` is a hybrid — it combines the best of both worlds

 Feature  `inline`  `block`  `inline-block` 
------------
 Stays in same line  ✅  ❌  ✅ 
 Accepts `width` & `height`  ❌  ✅  ✅ 
 Full-width by default  ❌  ✅  ❌ 
 Starts on new line  ❌  ✅  ❌ 
 Topbottom margin works  ❌  ✅  ✅ 

### Example

```html
a class=btnHomea
a class=btnAbouta
a class=btnContacta
```

```css
.btn {
  display inline-block;
  width 100px;
  height 40px;
  line-height 40px;
  text-align center;
  background navy;
  color white;
  border-radius 5px;
  margin 5px;
}
```

Result Three buttons sit side by side, each with exact sizing.

### The whitespace gap issue

When you write inline-block elements on separate HTML lines, a small whitespace gap appears between them. This is because the browser renders the newline character as a space.

Fix options

```css
 Option 1 Set font-size to 0 on the parent 
.parent { font-size 0; }
.child  { font-size 16px; }

 Option 2 Use negative margin 
.child { margin-right -4px; }

 Option 3 Use flex instead (recommended modern solution) 
.parent { display flex; gap 5px; }
```

### Common use cases

- Buttons and pill tags
- Navigation links in older codebases
- Badges and labels
- Small image + text combos
- Anywhere you need elements side-by-side with box sizing (before flex became universal)

---

## 8. `display none`

### What it does

The element and all its children are completely removed from the layout
- Not visible
- Takes no space — other elements close the gap
- Not accessible by screen readers (in most implementations)
- Still exists in the DOM and can be re-shown with JavaScript

### Example

```css
.modal {
  display none;  Hidden by default 
}

.modal.is-open {
  display block;  Shown when JS adds the class 
}
```

### The critical difference `display none` vs `visibility hidden` vs `opacity 0`

 Property  Visible  Takes space  Accessible to screen readers  Events fire 
---------------
 `display none`  ❌  ❌  ❌ (usually)  ❌ 
 `visibility hidden`  ❌  ✅  ❌ (usually)  ❌ 
 `opacity 0`  ❌  ✅  ✅  ✅ 

### Transition limitation

You cannot transition `display none` to `display block` directly — transitions do not work on `display`. For smooth showhide animations, a common pattern is

```css
 Use opacity + pointer-events instead 
.element {
  opacity 0;
  pointer-events none;
  transition opacity 0.3s ease;
}

.element.is-visible {
  opacity 1;
  pointer-events auto;
}
```

Or use the newer `@starting-style` rule (Chrome 117+, Firefox 129+) which finally allows transitions from `display none`.

---

## 9. `display flex`

### What it does

`display flex` creates a Flex Container. Its direct children automatically become Flex Items and are arranged along a single axis (row or column) using the Flexbox layout model.

Flexbox solves problems that were extremely painful in older CSS
- Vertically centering an element
- Making equal-height columns
- Distributing space evenly between elements
- Reordering elements visually without changing HTML

### Visual model

```
Flex Container
┌──────────────────────────────────────────────────┐
│  Main Axis (→ row direction by default)          │
│                                                  │
│  ┌────────┐  ┌────────┐  ┌────────┐             │
│  │ Item 1 │  │ Item 2 │  │ Item 3 │  ↕ Cross    │
│  └────────┘  └────────┘  └────────┘    Axis     │
│                                                  │
└──────────────────────────────────────────────────┘
```

### Basic example

```html
div class=container
  div class=item1div
  div class=item2div
  div class=item3div
div
```

```css
.container {
  display flex;
  flex-direction row;        default horizontal layout 
  justify-content center;   align along main axis 
  align-items center;       align along cross axis 
  gap 16px;                 space between items 
}
```

### Essential Flex Container properties

 Property  Values  What it does 
---------
 `flex-direction`  `row`, `row-reverse`, `column`, `column-reverse`  Sets the main axis direction 
 `justify-content`  `flex-start`, `flex-end`, `center`, `space-between`, `space-around`, `space-evenly`  Aligns items along the main axis 
 `align-items`  `stretch`, `flex-start`, `flex-end`, `center`, `baseline`  Aligns items along the cross axis 
 `flex-wrap`  `nowrap`, `wrap`, `wrap-reverse`  Whether items can wrap to next line 
 `gap`  `length`  Space between items (row-gap and column-gap) 
 `align-content`  same as `justify-content`  Aligns rows of wrapped items 

### Essential Flex Item properties

 Property  What it does 
------
 `flex-grow`  How much the item grows relative to others when there's extra space 
 `flex-shrink`  How much the item shrinks relative to others when there's less space 
 `flex-basis`  The initial size of the item before growingshrinking 
 `flex`  Shorthand for `flex-grow flex-shrink flex-basis` 
 `align-self`  Overrides `align-items` for a single item 
 `order`  Visually reorders items without changing HTML 

### The `flex` shorthand

```css
 flex grow shrink basis 
.item { flex 1 1 auto; }    grows, shrinks, auto size 
.item { flex 1; }           shorthand for 1 1 0 
.item { flex none; }        shorthand for 0 0 auto — rigid size 
```

### Centering with flex (the most common use case)

```css
 Perfect center — both horizontally and vertically 
.container {
  display flex;
  justify-content center;
  align-items center;
  height 100vh;
}
```

### Building a navbar with flex

```css
.navbar {
  display flex;
  justify-content space-between;  logo left, links right 
  align-items center;
  padding 0 24px;
}
```

---

## 10. `display inline-flex`

### What it does

`inline-flex` works exactly like `flex` for the element's children, but the container itself behaves inline in relation to its surroundings — it does not take the full width.

### When to use it

```css
 A flex layout that sits inside a sentence or next to other inline content 
.tag-list {
  display inline-flex;
  gap 6px;
}
```

### Comparison

```css
.flex-box        { display flex; }          container = block-level 
.inline-flex-box { display inline-flex; }   container = inline-level 
 Both children use flexbox layout 
```

---

## 11. `display grid`

### What it does

`display grid` creates a Grid Container. It enables a two-dimensional layout system where you can control both rows and columns simultaneously.

CSS Grid is the most powerful layout system available in CSS. It was specifically designed for page-level layout where you need both horizontal and vertical control.

### Visual model

```
Grid Container
┌──────────────────────────────────────┐
│  col 1    │  col 2    │  col 3      │
├───────────┼───────────┼─────────────┤
│  row 1    │  row 1    │  row 1      │
├───────────┼───────────┼─────────────┤
│  row 2    │  row 2    │  row 2      │
└──────────────────────────────────────┘
```

### Basic example

```html
div class=grid
  divAdiv
  divBdiv
  divCdiv
  divDdiv
  divEdiv
  divFdiv
div
```

```css
.grid {
  display grid;
  grid-template-columns repeat(3, 1fr);  3 equal columns 
  grid-template-rows auto auto;          2 auto-height rows 
  gap 20px;
}
```

### Essential Grid Container properties

 Property  Example  What it does 
---------
 `grid-template-columns`  `repeat(3, 1fr)`  Defines column sizes 
 `grid-template-rows`  `100px auto`  Defines row sizes 
 `gap` (or `row-gap`, `column-gap`)  `20px`  Space between tracks 
 `grid-template-areas`  `header header main aside`  Name areas for placement 
 `justify-items`  `center`  Aligns items horizontally within their cell 
 `align-items`  `center`  Aligns items vertically within their cell 
 `place-items`  `center`  Shorthand for both 
 `justify-content`  `space-between`  Aligns entire grid horizontally 
 `align-content`  `center`  Aligns entire grid vertically 

### Essential Grid Item properties

 Property  Example  What it does 
---------
 `grid-column`  `1  3`  Spans item from column line 1 to 3 
 `grid-row`  `1  2`  Spans item from row line 1 to 2 
 `grid-column` with `span`  `span 2`  Spans item across 2 columns 
 `grid-area`  `header`  Places item in a named area 
 `justify-self`  `end`  Overrides horizontal alignment 
 `align-self`  `start`  Overrides vertical alignment 

### The `fr` unit (Fractional Unit)

The `fr` unit is exclusive to CSS Grid. It represents a fraction of the available space.

```css
grid-template-columns 1fr 2fr 1fr;
 Column 2 gets twice as much space as columns 1 and 3 
 If container = 400px, columns = 100px, 200px, 100px 
```

### Named template areas

One of Grid's most readable features

```css
.page {
  display grid;
  grid-template-areas
    header  header  header
    sidebar main    main  
    footer  footer  footer;
  grid-template-columns 200px 1fr 1fr;
  grid-template-rows 60px 1fr 40px;
  height 100vh;
}

.page-header  { grid-area header; }
.page-sidebar { grid-area sidebar; }
.page-main    { grid-area main; }
.page-footer  { grid-area footer; }
```

### `auto-fill` vs `auto-fit` (responsive grids without media queries)

```css
 auto-fill creates as many columns as will fit, even if empty 
.grid {
  grid-template-columns repeat(auto-fill, minmax(200px, 1fr));
}

 auto-fit collapses empty columns, stretching items to fill 
.grid {
  grid-template-columns repeat(auto-fit, minmax(200px, 1fr));
}
```

This creates a fully responsive card grid without a single media query!

---

## 12. `display inline-grid`

### What it does

Like `inline-flex`, `inline-grid` creates a grid container that behaves inline with surrounding content — it shrinks to fit its content rather than spanning full width.

```css
.mini-grid {
  display inline-grid;
  grid-template-columns repeat(3, 30px);
  gap 4px;
}
```

---

## 13. `display list-item`

### What it does

Makes an element generate a principal block box and an additional marker box (the bullet point or number). This is the default display of `li` elements.

```css
.custom-list-item {
  display list-item;
  list-style-type disc;
  list-style-position inside;
  margin-left 20px;
}
```

### When to use it

Useful when you want non-`li` elements to render like list items, for example inside a `div` styled list

```html
div class=items
  div class=itemFirstdiv
  div class=itemSeconddiv
div
```

```css
.item {
  display list-item;
  list-style-type → ;
  margin-left 1.5em;
}
```

---

## 14. Table Display Values

These values make non-table HTML elements mimic the behavior of HTML table elements. They are mostly used for legacy compatibility or niche layout situations today.

 CSS Value  Equivalent HTML element 
------
 `table`  `table` 
 `table-row`  `tr` 
 `table-cell`  `td` or `th` 
 `table-row-group`  `tbody` 
 `table-header-group`  `thead` 
 `table-footer-group`  `tfoot` 
 `table-column`  `col` 
 `table-column-group`  `colgroup` 
 `table-caption`  `caption` 
 `inline-table`  inline `table` 

### Example old vertical centering trick (now replaced by flexgrid)

```css
.parent {
  display table;
  width 100%;
  height 300px;
}
.child {
  display table-cell;
  vertical-align middle;
  text-align center;
}
```

 ⚠️ Modern advice Prefer `flexbox` or `grid` for vertical centering. Table display values create implicit anonymous table boxes which can cause unpredictable layout behavior.

---

## 15. `display contents`

### What it does

When you set `display contents` on an element, the element's box itself disappears from the rendering tree, but its children remain and participate in the parent's layout as if the element was never there.

Think of it as unwrapping an element.

### When it is useful

Problem scenario
```html
div class=flex-parent
  div class=wrapper    !-- This extra div breaks the flex layout --
    div class=itemAdiv
    div class=itemBdiv
  div
  div class=itemCdiv
div
```

Without `display contents` `.wrapper` is a single flex item — `A` and `B` are not direct flex children.

With `display contents`
```css
.wrapper {
  display contents;  .wrapper's box vanishes — A and B are now direct flex children 
}
```

Now A, B, and C all participate equally in the flex layout.

### Accessibility warning

`display contents` currently has accessibility bugs in some browsers — it can remove elements from the accessibility tree (making them invisible to screen readers) even though they appear visually. Use it carefully and test with screen readers.

---

## 16. `display flow-root`

### What it does

`display flow-root` creates a new Block Formatting Context (BFC) without changing the outer display type. This is its primary use to contain floats and prevent margin collapse, without any of the visual side effects of other BFC-creating hacks.

### Why it matters

Before `flow-root`, developers had to use hacks to create a BFC
- `overflow hidden` — but this clips content
- `float left` — changes layout behavior
- `display inline-block` — changes how the element participates in flow

`flow-root` is the clean, semantic solution

```css
 The .parent now fully contains its floated children 
.parent {
  display flow-root;
}

.child {
  float left;
  width 100px;
}
```

### Preventing margin collapse

```css
.container {
  display flow-root;  Margins of children no longer collapse with parent 
}
```

 Browser support All modern browsers. If you need to support very old browsers, use `overflow auto` as a fallback.

---

## 17. Global  Keyword Values

These values apply to `display` (and any CSS property) and control inheritance

### `inherit`

Forces the element to take the exact `display` value of its parent element.

```css
.child {
  display inherit;  Same display as parent 
}
```

### `initial`

Resets the property to its CSS specification default (which is `inline` for most elements, since that's the spec default — not the browser stylesheet default).

```css
.element {
  display initial;  Resets to 'inline' per CSS spec 
}
```

 ⚠️ Note `initial` resets to the CSS spec default, which may differ from what the browser stylesheet applies by default (e.g., `div` defaults to `block` in browsers, but the CSS spec initial value is `inline`).

### `unset`

- If the property is inherited (i.e., it normally passes from parent to child) acts like `inherit`
- If the property is not inherited (like `display`) acts like `initial`

Since `display` is not inherited, `unset` behaves like `initial` for `display`.

```css
.element {
  display unset;  For display, acts like 'initial' → becomes 'inline' 
}
```

### `revert`

Rolls back the value to the browser's default stylesheet (the user-agent stylesheet), rather than the CSS spec default. This is usually what you actually want when you want to undo your CSS.

```css
h1 {
  display revert;  Restores h1 to browser default (block) 
}
```

### `revert-layer`

Similar to `revert`, but only reverts to the previous cascade layer. Used in advanced cascade layer scenarios (`@layer`).

```css
@layer base {
  .element { display flex; }
}

@layer override {
  .element { display revert-layer; }  Goes back to 'flex' from the base layer 
}
```

---

## 18. Default Display Values for HTML Elements

The browser applies these defaults via its built-in stylesheet before your CSS runs

### Block-level by default

 Element  Default Display 
------
 `div`  `block` 
 `p`  `block` 
 `h1`–`h6`  `block` 
 `section`  `block` 
 `article`  `block` 
 `header`  `block` 
 `footer`  `block` 
 `main`  `block` 
 `nav`  `block` 
 `aside`  `block` 
 `ul`, `ol`  `block` 
 `form`  `block` 
 `blockquote`  `block` 
 `figure`  `block` 
 `pre`  `block` 
 `hr`  `block` 
 `details`  `block` 

### Inline-level by default

 Element  Default Display 
------
 `span`  `inline` 
 `a`  `inline` 
 `strong`, `b`  `inline` 
 `em`, `i`  `inline` 
 `code`  `inline` 
 `small`  `inline` 
 `label`  `inline` 
 `abbr`  `inline` 
 `time`  `inline` 
 `sup`, `sub`  `inline` 

### Special defaults

 Element  Default Display  Notes 
---------
 `img`  `inline`  But behaves like a replaced element — widthheight work 
 `input`  `inline-block`  (varies by browser) 
 `button`  `inline-block`  (varies by browser) 
 `select`  `inline-block`  (varies by browser) 
 `li`  `list-item`  Creates a bulletmarker box 
 `table`  `table`  
 `tr`  `table-row`  
 `td`, `th`  `table-cell`  
 `thead`  `table-header-group`  
 `tbody`  `table-row-group`  
 `tfoot`  `table-footer-group`  

---

## 19. Flex vs Grid — When to Use Which

A common question Should I use Flexbox or Grid

The short answer Flex for one dimension, Grid for two dimensions.

The longer answer

### Use Flexbox (`display flex`) when

- You're laying out items in a single row or column (navigation bars, button groups, form inputs)
- The content drives the size of your layout
- You need dynamic wrapping based on content
- You want easy alignment (centering, spacing) along one axis

```css
 Perfect for navbars, button groups, form rows, icon + text combos 
.navbar { display flex; justify-content space-between; }
.button-group { display flex; gap 8px; }
.input-with-icon { display flex; align-items center; }
```

### Use Grid (`display grid`) when

- You're laying out in rows AND columns simultaneously
- The layout drives the content placement (page skeletons, dashboards, card grids)
- You want precise control over both dimensions at once
- You need elements to span across multiple rows or columns

```css
 Perfect for page layouts, dashboards, card grids, image galleries 
.page-layout { display grid; grid-template-areas header main footer; }
.card-grid   { display grid; grid-template-columns repeat(auto-fit, minmax(250px, 1fr)); }
```

### They can be combined

There's no rule against using both. A typical page uses Grid for the overall structure and Flex for individual components inside

```css
 Overall page Grid 
.page {
  display grid;
  grid-template-columns 260px 1fr;
}

 Inside each card Flex 
.card {
  display flex;
  flex-direction column;
  gap 12px;
}

 Inside the navbar Flex 
.navbar {
  display flex;
  justify-content space-between;
  align-items center;
}
```

---

## 20. Accessibility Considerations

The `display` property can affect how screen readers and assistive technologies interpret your content.

### `display none` hides from screen readers

Elements with `display none` are typically not announced by screen readers and are excluded from the accessibility tree. Use this intentionally.

If you want to hide something visually but keep it accessible (e.g., a skip-to-content link, or labels for icon buttons), use the visually-hidden pattern instead

```css
.sr-only {
  position absolute;
  width 1px;
  height 1px;
  padding 0;
  margin -1px;
  overflow hidden;
  clip rect(0, 0, 0, 0);
  white-space nowrap;
  border 0;
}
```

### `display contents` — proceed with caution

As noted earlier, `display contents` can unexpectedly remove elements from the accessibility tree. If the element has a semantic role (e.g., it's a `button` or `nav`), removing its box can also strip its ARIA role.

### `order` in FlexboxGrid — visual vs DOM order

CSS Grid and Flexbox allow you to visually reorder elements with the `order` property or `grid-template-areas`. However, the DOM order (which screen readers and keyboard tab order follow) remains unchanged.

```css
 ⚠️ Visually reordered, but tab order is wrong 
.item-a { order 2; }
.item-b { order 1; }  appears first visually, but keyboard focus hits .item-a first 
```

Only use visual reordering for truly visual-only differences that don't affect navigation logic.

---

## 21. Browser Compatibility

 Display Value  Chrome  Firefox  Safari  Edge 
---------------
 `block`, `inline`, `inline-block`, `none`  All versions  All versions  All versions  All versions 
 `flex`  21+ (prefixed), 29+  20+ (prefixed), 28+  6.1+ (prefixed), 9+  12+ 
 `grid`  57+  52+  10.1+  16+ 
 `contents`  65+  37+  11.1+ (buggy)  79+ 
 `flow-root`  58+  53+  13+  79+ 
 `inline-flex`  21+, 29+  20+, 28+  6.1+, 9+  12+ 
 `inline-grid`  57+  52+  10.1+  16+ 
 `list-item`  All  All  All  All 
 `table-` values  All  All  All  All 
 `revert`  84+  67+  9.1+  84+ 
 `revert-layer`  99+  97+  15.4+  99+ 

 ✅ For all modern web projects in 2024+, you can safely use `flex`, `grid`, `flow-root`, and `contents` without prefixes or significant compatibility concerns. Only if you need to support Internet Explorer 11 would you need significant workarounds.

---

## 22. Common Mistakes and How to Fix Them

### Mistake 1 Trying to set widthheight on inline elements

```css
 ❌ Wrong — width has no effect on inline 
span {
  display inline;
  width 200px;
}

 ✅ Fix — use inline-block or block 
span {
  display inline-block;
  width 200px;
}
```

### Mistake 2 Forgetting flexgrid only affect direct children

```css
.container { display flex; }

 ❌ .grandchild is NOT a flex item 
div class=container
  div class=child
    div class=grandchildNOT a flex item!div
  div
div

 ✅ .child IS a flex item — add flex to .child for grandchildren 
.child { display flex; }
```

### Mistake 3 Using `display none` when you want an animation

```css
 ❌ This does not animate 
.box { display none; transition display 0.3s; }
.box.show { display block; }

 ✅ Use opacity + pointer-events for animatable hiding 
.box { opacity 0; pointer-events none; transition opacity 0.3s; }
.box.show { opacity 1; pointer-events auto; }
```

### Mistake 4 Not knowing `display flex` changes the children's margin behavior

Flexbox disables margin collapsing between flex children. This is usually what you want, but can surprise you if you're used to block margin collapsing.

```css
 In a flex container, margins don't collapse — they add up 
.flex-container { display flex; flex-direction column; }
.item { margin-bottom 20px; }
.next-item { margin-top 20px; }
 Gap between items = 40px, not 20px 
 Use 'gap' on the container instead for consistent spacing 
```

### Mistake 5 Setting `display block` on `td` or `tr`

Table elements have strict relationship requirements. Changing their display type breaks the table layout algorithm.

```css
 ❌ Breaks the table 
td { display block; }

 ✅ Use a different layout approach if you need this behavior 
```

### Mistake 6 Confusing `align-items` and `justify-content` direction

In `flex-direction row` (default)
- `justify-content` = horizontal (main axis)
- `align-items` = vertical (cross axis)

In `flex-direction column`
- `justify-content` = vertical (main axis)
- `align-items` = horizontal (cross axis)

They swap meaning when you change `flex-direction`.

```css
 Centering in column direction 
.container {
  display flex;
  flex-direction column;
  justify-content center;  NOW this is vertical 
  align-items center;      NOW this is horizontal 
}
```

---

## 23. Real-World Layout Patterns

### Pattern 1 Holy Grail Layout

The classic sidebar + main content + footer layout

```css
body {
  display grid;
  grid-template
    header 60px
    sidebar main 1fr
    footer 40px
     220px 1fr;
  min-height 100vh;
}

header { grid-area header; }
aside  { grid-area sidebar; }
main   { grid-area main; }
footer { grid-area footer; }
```

### Pattern 2 Responsive Card Grid

```css
.card-grid {
  display grid;
  grid-template-columns repeat(auto-fit, minmax(280px, 1fr));
  gap 24px;
  padding 24px;
}
```

No media queries needed — automatically adjusts columns based on screen width.

### Pattern 3 Centering Anything

```css
 Center a single element in the viewport 
body {
  display flex;             or grid 
  place-items center;       shorthand for justify + align 
  min-height 100vh;
}
```

### Pattern 4 Sticky Footer

```css
body {
  display flex;
  flex-direction column;
  min-height 100vh;
}
main {
  flex 1;  Takes all available space, pushes footer down 
}
footer {
   Stays at the bottom 
}
```

### Pattern 5 Sidebar that doesn't wrap

```css
.layout {
  display flex;
  gap 24px;
}
.sidebar {
  flex 0 0 240px;  Don't grow, don't shrink, fixed 240px 
}
.main-content {
  flex 1;  Take remaining space 
  min-width 0;  Prevents overflow in some cases 
}
```

### Pattern 6 Equal-height columns

```css
.columns {
  display flex;        or grid 
  align-items stretch;  default — all children match the tallest 
}

.column {
  flex 1;
}
```

---

## 24. Quick Reference Cheatsheet

```css
 ─── Basic ─────────────────────────────────────────── 
display block;          Full-width, new line, box sizing works 
display inline;         Stays in text flow, no widthheight 
display inline-block;   In text flow + full box sizing 
display none;           Completely removed from layout + hidden 

 ─── Flexbox ────────────────────────────────────────── 
display flex;           Block-level flex container 
display inline-flex;    Inline-level flex container 

 Common flex properties 
 flex-direction row  column 
 justify-content flex-start  center  flex-end  space-between  space-around  space-evenly 
 align-items stretch  center  flex-start  flex-end  baseline 
 flex-wrap nowrap  wrap 
 gap length 

 ─── Grid ───────────────────────────────────────────── 
display grid;           Block-level grid container 
display inline-grid;    Inline-level grid container 

 Common grid properties 
 grid-template-columns repeat(3, 1fr)  200px 1fr  etc. 
 grid-template-rows auto  100px 1fr  etc. 
 grid-template-areas a b c d 
 gap length 
 place-items center (shorthand for align + justify) 

 ─── Special ────────────────────────────────────────── 
display list-item;      Renders a markerbullet like li 
display flow-root;      Creates BFC — contains floats cleanly 
display contents;       Element's own box disappears; children remain 

 ─── Table ──────────────────────────────────────────── 
display table;
display table-row;
display table-cell;
display inline-table;

 ─── Global ─────────────────────────────────────────── 
display inherit;        Copy parent's display value 
display initial;        Reset to CSS spec default (usually inline) 
display unset;          inherit if inheritable, else initial 
display revert;         Roll back to browser stylesheet default 
display revert-layer;   Roll back to previous cascade layer 
```

---

## Summary

The `display` property is foundational to everything in CSS layout. Here's what to remember

 Value  One-liner 
------
 `block`  Own line, full width, full box model 
 `inline`  Flows with text, no widthheight 
 `inline-block`  Text flow + full box sizing 
 `none`  Gone from layout and visibility 
 `flex`  1D layout — row or column 
 `inline-flex`  Same as flex, but container is inline 
 `grid`  2D layout — rows and columns 
 `inline-grid`  Same as grid, but container is inline 
 `list-item`  Adds a bulletcounter marker 
 `flow-root`  Creates a BFC to contain floats 
 `contents`  Removes element box, keeps children 
 `table-`  Emulate HTML table behavior 

Priority for beginners Master `block`, `inline`, `inline-block`, `none`, `flex`, and `grid`. These six values cover 95% of real-world web development needs.

---

This guide covers CSS Display behavior as of 2024, reflecting the CSS Display Module Level 3 specification.
# CSS Selectors

A selector tells the browser **which elements to style**. Everything in CSS starts here.

```css
selector {
  property: value;
}
```

## Element selectors
Target every element of a given type by its tag name.
```css
p {
  color: gray;
}
h1 {
  font-size: 32px;
}
```
This styles **all** `<p>` and **all** `<h1>` on the page.

## Class selectors
Target elements that have a specific `class`. Start with a dot `.`. Classes are reusable — many elements can share one.
```css
.button {
  background: blue;
  color: white;
}
```
```html
<button class="button">Save</button>
<a class="button">Learn more</a>
```
Classes are the most common selector you'll use.

## ID selectors
Target one unique element by its `id`. Start with a hash `#`. An id should appear **only once** per page.
```css
#main-header {
  background: black;
}
```
```html
<header id="main-header">...</header>
```
Prefer classes for styling; keep ids for unique hooks (like scroll anchors).

## Descendant selectors
Target elements **inside** another element. Separate with a space.
```css
nav a {
  text-decoration: none;
}
```
This styles every `<a>` that is inside a `<nav>` — but not links elsewhere.

## Grouping selectors
Apply the same styles to several selectors at once. Separate with commas.
```css
h1, h2, h3 {
  font-family: Arial, sans-serif;
}
```
This avoids repeating the same rules three times.

## Pseudo-classes (like `:hover`)
Style an element in a certain **state**. They start with a colon `:`.
```css
a:hover {
  color: red;         /* when the mouse is over the link */
}
input:focus {
  border-color: blue; /* when the field is selected */
}
li:first-child {
  font-weight: bold;  /* the first item in a list */
}
```
`:hover` and `:focus` are the ones you'll use most.

## Specificity basics
When two rules target the same element, the **more specific** one wins. Rough order (weakest → strongest):

1. Element selectors (`p`) — weakest
2. Class selectors (`.button`) — stronger
3. ID selectors (`#main`) — strongest
4. Inline styles (`style="..."`) — beats them all

```css
p { color: gray; }        /* weak */
.note { color: green; }   /* beats the above */
#alert { color: red; }    /* beats both */
```
If specificity is equal, the rule that comes **last** in the file wins.

### Common mistakes
- **Overusing IDs** for styling — they're hard to override later. Use classes.
- **Forgetting the `.` or `#`** — `button` (all buttons) is very different from `.button` (elements with `class="button"`).
- **Fighting specificity with `!important`** — this is a red flag. Restructure your selectors instead.
- **Descendant selector spacing** — `.card.title` (one element with both classes) vs `.card .title` (a `.title` inside a `.card`) mean different things.

---

### Quick review
- `p` = element, `.x` = class, `#x` = id.
- Space = "inside" (descendant); comma = "also apply to."
- `:hover` / `:focus` style states.
- Specificity: inline > id > class > element; ties go to the last rule.

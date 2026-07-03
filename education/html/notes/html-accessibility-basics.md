# HTML Accessibility Basics

Accessibility (often shortened to **a11y**) means building pages that *everyone* can use — including people who use screen readers, keyboards instead of a mouse, or have low vision. Good news: most of it is just writing clean, correct HTML.

## 1. Alt text on images
Every meaningful image needs an `alt` describing it. Screen readers read it aloud; it also shows if the image fails to load.
```html
<img src="team.jpg" alt="Our team standing outside the office" />
```
Decorative image? Use an empty alt so it's skipped:
```html
<img src="line.png" alt="" />
```

## 2. Labels on form fields
Every input needs a label so users know what to type. Connect them with `for` and `id`.
```html
<label for="email">Email address</label>
<input type="email" id="email" name="email" />
```
Without a label, screen reader users hear "edit text" with no idea what it's for. Placeholders are **not** a replacement for labels.

## 3. Heading hierarchy
Use headings in order to create an outline of the page. Don't skip levels or pick a heading just because of its size (use CSS for size).
```html
<h1>Main page title</h1>     <!-- one per page -->
  <h2>Section title</h2>
    <h3>Sub-point</h3>
  <h2>Another section</h2>
```
Screen reader users navigate by jumping between headings, so a clean structure is like a table of contents for them.

## 4. Button vs link
This trips up beginners. Choose based on **what it does**, not how it looks.
- **`<a>` (link)** → goes somewhere (a new page or URL).
  ```html
  <a href="/about">About us</a>
  ```
- **`<button>`** → does an action (submit a form, open a menu, toggle something).
  ```html
  <button type="button">Open menu</button>
  ```
Don't fake a button with a `<div>` and JavaScript — a real `<button>` is keyboard-focusable and announced correctly for free.

## 5. Meaningful text
Link and button text should make sense on its own.
```html
<!-- Bad: meaningless out of context -->
<a href="/report">Click here</a>

<!-- Good: describes the destination -->
<a href="/report">Download the 2026 report</a>
```
Screen reader users often list all links at once — "click here" ten times is useless.

## 6. Keyboard-friendly structure
Many people navigate with the **Tab** key instead of a mouse. If you use the right elements, this works automatically:
- Use real `<a>`, `<button>`, `<input>`, `<select>` — they're focusable and operable by keyboard out of the box.
- Keep a logical source order (the order elements appear in the HTML is the tab order).
- Use semantic landmarks (`<nav>`, `<main>`, `<footer>`) so users can jump around.

Quick test: try using your page with **only the keyboard**. If you can reach and activate everything with Tab and Enter, you're in good shape.

---

### Quick review
- Images → `alt`. Decorative → `alt=""`.
- Every input → a real `<label>`.
- Headings in order, one `<h1>` per page.
- Link = go somewhere; button = do something.
- Write link text that makes sense alone.
- Use real interactive elements so keyboard users can reach everything.

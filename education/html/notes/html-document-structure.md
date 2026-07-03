# HTML Document Structure

Every HTML page follows the same basic skeleton. Learn this once and you can start any page from memory.

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>My Page</title>
    <link rel="stylesheet" href="styles.css" />
  </head>
  <body>
    <h1>Hello</h1>
    <script src="app.js"></script>
  </body>
</html>
```

## `<!DOCTYPE html>`
The very first line. It tells the browser: "use modern HTML (HTML5) rules."
Without it, browsers can switch to an old, buggy "quirks mode." It is not a tag — just a declaration.

## `<html>` tag
The root element. Everything on the page lives inside it.
Add `lang="en"` so browsers and screen readers know the language.

```html
<html lang="en">
```

## `<head>` tag
Holds information *about* the page, not the visible content. Things like the title, character set, and links to CSS go here. Nothing in `<head>` shows up on the page itself (except the title, which shows in the browser tab).

## `<body>` tag
Holds everything the user actually **sees**: text, images, buttons, forms, etc.

## `<title>`
Sets the text shown in the browser tab and in search results. Keep it short and descriptive.

```html
<title>Contact Us - My Shop</title>
```

## `<meta charset="UTF-8">`
Sets the character encoding. UTF-8 supports almost every character and emoji, so text like `é`, `ü`, or `€` displays correctly. Put it near the top of `<head>`.

## Viewport meta tag
Makes your page responsive on phones. Without it, mobile browsers zoom out and everything looks tiny.

```html
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
```
- `width=device-width` → match the screen width.
- `initial-scale=1.0` → no zoom by default.

## Linking CSS
Connect an external stylesheet in the `<head>`:

```html
<link rel="stylesheet" href="styles.css" />
```
`rel="stylesheet"` says what kind of file it is; `href` is the path to it.

## `<script>` tag basics
Adds JavaScript. Put it just before the closing `</body>` tag so the HTML loads first (the script can then find the elements it needs).

```html
<script src="app.js"></script>
```
You can also write JS directly inside the tags:
```html
<script>
  console.log("Page loaded");
</script>
```

---

### Quick review
- `<!DOCTYPE html>` = use modern HTML.
- `<head>` = info about the page. `<body>` = what the user sees.
- Always include `charset` and the `viewport` meta tag.
- CSS links go in `<head>`; scripts go at the end of `<body>`.

# CSS Variables (Custom Properties)

CSS variables let you store a value once and reuse it everywhere. Change it in one place and it updates across the whole site — perfect for colors, spacing, and theming.

## Declaring variables in `:root`
`:root` targets the top of the document, so variables defined there are **global** — usable anywhere. Custom property names always start with two dashes `--`.
```css
:root {
  --primary-color: #2563eb;
  --text-color: #333333;
  --spacing: 16px;
  --radius: 8px;
}
```

## Custom properties and `var()`
Use a variable with the `var()` function.
```css
.button {
  background: var(--primary-color);
  color: white;
  padding: var(--spacing);
  border-radius: var(--radius);
}
.card {
  padding: var(--spacing);
  color: var(--text-color);
}
```

`var()` can take a **fallback** value in case the variable isn't defined:
```css
color: var(--text-color, black);   /* uses black if --text-color is missing */
```

## Reusable colors and spacing
This is the main win. Define your palette and spacing scale once:
```css
:root {
  /* colors */
  --primary: #2563eb;
  --danger: #dc2626;
  --bg: #f9fafb;

  /* spacing scale */
  --space-sm: 8px;
  --space-md: 16px;
  --space-lg: 32px;
}
```
Now every component pulls from the same source of truth:
```css
.alert { background: var(--danger); padding: var(--space-md); }
.section { background: var(--bg); margin-bottom: var(--space-lg); }
```
If the brand color changes, you edit **one line** instead of hunting through the whole file.

## Bonus: easy theming
Because variables cascade, you can override them for a section or a dark theme:
```css
.dark-theme {
  --bg: #111827;
  --text-color: #f9fafb;
}
```
Everything inside `.dark-theme` using those variables updates automatically.

### Common mistakes
- **Forgetting the `--` prefix** — it's `--primary`, and you read it with `var(--primary)`.
- **Missing `var()`** — `color: --primary;` doesn't work; it must be `color: var(--primary);`.
- **Confusing with Sass variables** (`$color`) — CSS variables are native, live in the browser, and can change at runtime; Sass variables are compiled away.
- **Defining everything locally** instead of in `:root`, losing the reuse benefit.

---

### Quick review
- Define globals in `:root` with a `--name`.
- Use them with `var(--name)`, optional fallback `var(--name, default)`.
- One source of truth for colors and spacing = easy, consistent updates and theming.

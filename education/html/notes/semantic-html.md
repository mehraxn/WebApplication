# Semantic HTML

"Semantic" means the tag *describes what the content is*, not just how it looks.
A `<div>` says nothing. A `<nav>` says "this is navigation." Browsers, screen readers, and search engines all understand semantic tags — so use them.

## The main layout tags

```html
<body>
  <header>...</header>
  <nav>...</nav>
  <main>
    <section>
      <article>...</article>
      <article>...</article>
    </section>
    <aside>...</aside>
  </main>
  <footer>...</footer>
</body>
```

### `<header>`
The top of a page or a section. Usually holds the logo, site title, and sometimes the navigation.
```html
<header>
  <h1>My Blog</h1>
</header>
```

### `<nav>`
A block of navigation links (a menu). You can have more than one (e.g. main menu + footer menu).
```html
<nav>
  <a href="/">Home</a>
  <a href="/about">About</a>
</nav>
```

### `<main>`
The main, unique content of the page. There should be **only one** `<main>` per page, and it should not include repeated things like the header, nav, or footer.

### `<section>`
A grouped chunk of related content, usually with its own heading. Think "chapter."
```html
<section>
  <h2>Our Services</h2>
  <p>...</p>
</section>
```

### `<article>`
A self-contained piece that would make sense on its own — a blog post, a news item, a product card, a comment.
```html
<article>
  <h2>How to Learn HTML</h2>
  <p>Start with structure...</p>
</article>
```

### `<aside>`
Content related to, but separate from, the main content — a sidebar, related links, or an ad.
```html
<aside>
  <h3>Related posts</h3>
  <ul>...</ul>
</aside>
```

### `<footer>`
The bottom of a page or section. Usually holds copyright, contact info, and secondary links.
```html
<footer>
  <p>&copy; 2026 My Blog</p>
</footer>
```

## Why semantic HTML matters
- **Readable code** — you and other developers instantly see the page structure.
- **Accessibility** — screen readers let users jump straight to the `<nav>`, `<main>`, etc. A page of only `<div>`s gives them nothing to navigate by.
- **SEO** — search engines understand your structure better and can rank/present content more accurately.
- **Less confusion** — clear structure means fewer bugs and easier styling.

## Accessibility and SEO benefits (in plain terms)
- Screen reader users can skip repeated content and go straight to `<main>`.
- Headings + landmarks (`<nav>`, `<main>`, `<footer>`) create a map of the page.
- Google reads `<article>` and `<section>` to understand what your content *is*, not just what it looks like.

---

### Quick review
- Use the tag that *describes the content*, not just `<div>` everywhere.
- One `<main>` per page.
- `<article>` = stands alone; `<section>` = grouped content with a heading.
- Semantic tags help accessibility **and** SEO for free.

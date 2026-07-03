# HTML Education

This section covers the fundamentals of **HTML** — the language that gives every web page its structure and content. It's the first building block of the front-end stack, and the foundation everything else (CSS, Bootstrap, Flask templates) sits on top of.

## What this section contains

- **`notes/`** — clear, beginner-friendly notes on each core HTML topic, written for quick exam and interview review. Each note explains the concept in plain English and shows practical code examples.
- **`exercises/`** — hands-on practice files that apply the ideas from the notes (small pages and snippets you write yourself).

## How the notes are organized

Each note is a single focused topic. Together they cover writing a complete, correct, accessible HTML page:

| File | What it covers |
|------|----------------|
| `notes/html-document-structure.md` | The page skeleton: `<!DOCTYPE>`, `<html>`, `<head>`, `<body>`, title, meta tags, linking CSS, and scripts. |
| `notes/semantic-html.md` | Meaningful layout tags (`header`, `nav`, `main`, `section`, `article`, `aside`, `footer`) and why they help accessibility and SEO. |
| `notes/html-forms.md` | Building forms: inputs, labels, textarea, select, checkboxes, radios, submit buttons, `required`, `name`, and GET vs POST. |
| `notes/html-tables.md` | Displaying data: `table`, `thead`, `tbody`, `tr`, `th`, `td`, `caption`, and when tables should/shouldn't be used. |
| `notes/html-media.md` | Adding media: images and alt text, audio, video, iframes, and `figure`/`figcaption`. |
| `notes/html-accessibility-basics.md` | Making pages usable by everyone: alt text, labels, heading order, button vs link, meaningful text, keyboard-friendly structure. |

## HTML exercises

Each exercise is a small, self-contained folder with an `index.html` and its own
`README.md` (goal, concepts practiced, files, and what I learned).

| Exercise | Concepts | Difficulty |
|----------|----------|------------|
| `exercises/semantic-page-layout/` | Semantic tags: `header`, `nav`, `main`, `section`, `article`, `aside`, `footer`; heading hierarchy | Beginner |
| `exercises/product-comparison-table/` | Tables: `table`, `caption`, `thead`, `tbody`, `tr`, `th`, `td`, `scope` | Beginner |
| `exercises/media-gallery-page/` | Media: `img` + `alt`, `figure`/`figcaption`, `audio`, `video`, `source` | Beginner+ |
| `exercises/multi-section-article/` | Article structure: nested sections, headings, `ul`/`ol`, `blockquote`, links, images | Beginner+ |
| `exercises/accessible-contact-form/` | Forms: labels, input types, `textarea`, `select`, checkbox, submit, `required`, `name`, POST | Intermediate |

## What the exercises prove

Completing the exercises in this section shows that you can:

- Build a valid HTML5 page from scratch, structured correctly.
- Use **semantic tags** to organize content the way real websites do.
- Create **working forms** — the core skill for any Flask developer handling user input.
- Present **tabular data** properly with accessible tables.
- Embed **images and media** with correct, accessible markup.
- Write **accessible, SEO-friendly HTML** by default, not as an afterthought.

These are exactly the fundamentals a junior web / Flask developer is expected to know.

## Recommended study order

Work through the notes in this order — each one builds on the previous:

1. **`html-document-structure.md`** — start here; you need the page skeleton before anything else.
2. **`semantic-html.md`** — learn how to organize the content inside `<body>`.
3. **`html-forms.md`** — the most important topic for a future Flask developer.
4. **`html-tables.md`** — displaying structured data correctly.
5. **`html-media.md`** — adding images and media.
6. **`html-accessibility-basics.md`** — ties everything together with best practices you should apply to all the topics above.

After reading each note, do the matching exercise before moving on.

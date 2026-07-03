# Blog Article Layout

## Project Overview
A clean, semantic HTML layout for a single blog article. It models how a real blog post is
structured: a title with author/date metadata, a table of contents, several content
sections with headings, a pull quote, and a related-articles sidebar.

## Features
- Article title
- Author and date metadata (using `<time>`)
- Table of contents linking to each section
- Section headings and paragraphs
- Quote section (`<blockquote>`)
- Related articles sidebar (`<aside>`)
- Site header with navigation and a page footer

## Technologies Used
- HTML5
- Semantic markup (`article`, `section`, `nav`, `aside`, `time`, `blockquote`) — no CSS yet

## Folder Structure
```
blog-article-layout/
├── index.html    # the blog article page
├── README.md     # this file
└── screenshots/  # add screenshots here
```

## How to Run or Open
Open `index.html` directly in any web browser — no server or build step needed.

## What I Learned
- Structuring a content-heavy page: one `<article>` broken into linked `<section>`s.
- Marking up metadata with `<time>` and building an in-page table of contents.
- Placing related content correctly in an `<aside>`.

## Resume Value
Shows I understand how content-heavy pages (news sites, blogs) are structured
semantically, with metadata and a working table of contents.

## Future Improvements
- Add CSS for readable typography and a comfortable reading width
- Add a sticky table of contents
- Convert it into a reusable Flask/Jinja template for a blog CRUD app

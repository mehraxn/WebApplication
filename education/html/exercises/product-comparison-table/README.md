# Exercise: Product Comparison Table

## Goal
Build a clean, accessible HTML table that compares three products (subscription
plans) across several features.

## Concepts practiced
- `<table>` structure with `<thead>` and `<tbody>`
- `<caption>` to title the table
- `<tr>` rows, `<th>` header cells, `<td>` data cells
- Using `<th scope="col">` for column headers and `<th scope="row">` for row headers
- Presenting real tabular data (not using tables for layout)

## Files included
- `index.html` — the comparison table
- `README.md` — this file

## What I learned
- Separating `<thead>` from `<tbody>` makes the structure clear and helps browsers
  and screen readers.
- `scope` on `<th>` tells assistive tech whether a header labels a column or a row.
- The first cell of each row can itself be a `<th scope="row">` to label that row.
- Tables are the right tool for data like this — but never for page layout (use CSS
  for that).

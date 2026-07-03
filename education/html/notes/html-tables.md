# HTML Tables

Tables display **data in rows and columns** — like a spreadsheet. Use them for real tabular data (prices, schedules, stats), *not* for page layout.

## A full example

```html
<table>
  <caption>Weekly Schedule</caption>
  <thead>
    <tr>
      <th>Day</th>
      <th>Subject</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Monday</td>
      <td>HTML</td>
    </tr>
    <tr>
      <td>Tuesday</td>
      <td>CSS</td>
    </tr>
  </tbody>
</table>
```

## The tags explained

### `<table>`
The container that wraps the whole table.

### `<thead>`
The header section — the top row(s) that label the columns. Keeping headers here helps accessibility and lets browsers repeat them when printing long tables.

### `<tbody>`
The body — the actual data rows. Separating `<thead>` from `<tbody>` makes the structure clear.

### `<tr>` (table row)
One horizontal row. Everything in a single row goes inside one `<tr>`.

### `<th>` (table header cell)
A heading cell. Browsers make it **bold and centered** by default, and screen readers announce it as a header for its column or row.
```html
<th>Price</th>
```
Tip: add `scope="col"` or `scope="row"` to tell assistive tech which direction the header applies to.
```html
<th scope="col">Price</th>
```

### `<td>` (table data cell)
A normal data cell — the individual pieces of data inside a row.
```html
<td>€19.99</td>
```

### `<caption>`
A title for the whole table. Place it right after `<table>`. It helps everyone (especially screen reader users) know what the table is about.
```html
<caption>Menu Prices</caption>
```

## When to use tables — and when NOT to
**Use a table when:**
- You have real tabular data: rows and columns that relate to each other.
- Examples: price lists, timetables, sports standings, financial reports, comparison charts.

**Do NOT use a table for:**
- **Page layout** (positioning your header, sidebar, content). This was common 20 years ago but is now wrong. Use **CSS Flexbox or Grid** instead.
- Making things line up visually when the data isn't actually a grid of related values.

Rule of thumb: if you'd naturally put it in Excel, a table is right. If you're just trying to arrange boxes on a page, use CSS.

---

### Quick review
- Structure: `<table>` → `<caption>` → `<thead>` (with `<th>`) → `<tbody>` (with `<td>`).
- `<tr>` = a row, `<th>` = header cell, `<td>` = data cell.
- Add `scope` to `<th>` for accessibility.
- Tables are for **data**, never for **layout**.

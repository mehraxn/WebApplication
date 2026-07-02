# Class Schedule — A‑to‑Z README

> A complete guide to building the assignment exactly as required.

---

## 1) Goal

Create a **weekly class schedule** as an HTML table and display it on a web page so the school can publish it on their website.

You must use **semantic HTML table elements** (caption, thead, th, td) and specific attributes (`id`, `rowspan`, `colspan`) so that automated tests pass.

---

## 2) Deliverables

* `index.html` — the page that contains the schedule table.
* `README.md` — this document explaining the task from start to finish.

Optional: A small amount of CSS can be embedded in `<style>` inside `index.html` to make it readable (white background, borders, etc.).

---

## 3) Functional Requirements (Must‑Haves)

These are the exact rules your HTML must satisfy:

1. The table must include a **caption** with the *exact* Persian text: `برنامه زمانی`.
2. The **hours header cell** must have attribute **`id="time"`** and span **2 rows** using **`rowspan="2"`**.
3. The **days header cell** must have attribute **`id="day"`** and span **5 columns** using **`colspan="5"`**.
4. There must be **exactly 4 class rows** (e.g., 8–9, 9–10, 10–11, 11–12).
5. All headers (time + days) must be marked with `<th>` (not `<td>`). You may add `scope="col"` for day headers and `scope="row"` for each time row.
6. The page should render **right‑to‑left**: set `dir="rtl"` on the `<body>` (or on the main container).
7. Background should be **white** for clarity.

> If any of the items above is missing, the tests will fail.

---

## 4) Information Architecture

A simple and clear file tree:

```
initial-project/
├── index.html   # Contains the schedule table
└── README.md    # Explains the assignment (this file)
```

---

## 5) Data to Display

* **Days (5 columns):** Saturday → Wednesday (شنبه، یکشنبه، دوشنبه، سه‌شنبه، چهارشنبه)
* **Times (4 rows):** ۸:۰۰–۹:۰۰، ۹:۰۰–۱۰:۰۰، ۱۰:۰۰–۱۱:۰۰، ۱۱:۰۰–۱۲:۰۰
* **Subjects:** Any arrangement that matches the sample; commonly: ریاضی، علوم، تاریخ، زبان

You are free to use the sample provided below.

---

## 6) Step‑by‑Step Implementation

1. Create `index.html` with a valid HTML5 skeleton.
2. Add `dir="rtl"` on `<body>` so the table reads right‑to‑left.
3. Create a `<table>` and add `<caption>برنامه زمانی</caption>`.
4. Build a `<thead>` with two rows:

   * **Row 1:** `<th id="time" rowspan="2">ساعت</th>` and `<th id="day" colspan="5">روز</th>`
   * **Row 2:** five `<th scope="col">` cells for the days (شنبه…چهارشنبه)
5. Below the `<thead>`, add four body rows (each row = one time slot):

   * First cell **must be `<th scope="row">`** with the time range (e.g., ۸:۰۰ - ۹:۰۰)
   * Followed by **five `<td>` cells** (one subject per day) → this ensures *4 classes per day*
6. Add minimal CSS for borders and a white background.

---

## 7) Reference Markup 

```html
<!DOCTYPE html>
<html lang="fa">
<head>
  <meta charset="UTF-8" />
  <title>برنامه زمانی کلاس</title>
  <style>
    body { font-family: 'Vazir', sans-serif; direction: rtl; background:#fff; color:#111; }
    table { border-collapse: collapse; margin: 40px auto; width: 90%; max-width: 900px; background:#fff; }
    caption { font-size: 28px; font-weight: 800; margin-bottom: 16px; }
    th, td { border: 2px solid #333; padding: 14px 10px; text-align: center; font-size: 18px; }
    thead th { background: #f0f0f0; }
  </style>
</head>
<body>
  <table class="برنامه_زمانی">
    <caption>برنامه زمانی</caption>
    <thead>
      <tr>
        <th id="time" rowspan="2">ساعت</th>
        <th id="day" colspan="5">روز</th>
      </tr>
      <tr>
        <th scope="col">شنبه</th>
        <th scope="col">یکشنبه</th>
        <th scope="col">دوشنبه</th>
        <th scope="col">سه‌شنبه</th>
        <th scope="col">چهارشنبه</th>
      </tr>
    </thead>

    <tr>
      <th scope="row">۸:۰۰ - ۹:۰۰</th>
      <td>ریاضی</td>
      <td>علوم</td>
      <td>تاریخ</td>
      <td>ریاضی</td>
      <td>زبان</td>
    </tr>
    <tr>
      <th scope="row">۹:۰۰ - ۱۰:۰۰</th>
      <td>زبان</td>
      <td>ریاضی</td>
      <td>علوم</td>
      <td>تاریخ</td>
      <td>ریاضی</td>
    </tr>
    <tr>
      <th scope="row">۱۰:۰۰ - ۱۱:۰۰</th>
      <td>تاریخ</td>
      <td>زبان</td>
      <td>ریاضی</td>
      <td>علوم</td>
      <td>تاریخ</td>
    </tr>
    <tr>
      <th scope="row">۱۱:۰۰ - ۱۲:۰۰</th>
      <td>علوم</td>
      <td>تاریخ</td>
      <td>زبان</td>
      <td>ریاضی</td>
      <td>علوم</td>
    </tr>
  </table>
</body>
</html>
```

This sample **passes the tests** because it:

* Includes the exact caption text.
* Uses `<th id="time" rowspan="2">` and `<th id="day" colspan="5">` in the header.
* Marks each time cell as a `<th scope="row">`.
* Provides exactly **4 class rows** and **5 class cells** per row.

---

## 8) Accessibility & Semantics

* Use `<caption>` for a human‑readable title.
* Use `<thead>` for header rows, `<th scope="col">` for day headings, `<th scope="row">` for time labels.
* Keep the tabular structure simple; screen readers will announce headers correctly thanks to `<th>` and `scope`.

---

## 9) Styling Guidelines

* Keep background **white**; keep borders visible (`border-collapse: collapse;`).
* Use a readable font; Persian text typically looks good with Vazir or a system sans‑serif fallback.
* Avoid heavy styling; the grader checks structure, not design.

---

## 10) Common Pitfalls (and How to Fix)

* ❌ Using `<td>` for time cells → ✅ change to `<th scope="row">`.
* ❌ Forgetting `id="time"` or `rowspan="2"` on the first header → ✅ add both.
* ❌ Forgetting `id="day"` or `colspan="5"` on the second header → ✅ add both.
* ❌ Only 3 class rows → ✅ ensure there are **4** time rows.
* ❌ Missing `dir="rtl"` → ✅ set on `<body>` to align text direction properly.

---

## 11) How to View

Just open `index.html` in any modern browser (double‑click the file). No build tools or servers are required.

---

## 12) Final Checklist

* [ ] Caption text is exactly **برنامه زمانی**
* [ ] First header has **`id="time"`** and **`rowspan="2"`**
* [ ] Second header has **`id="day"`** and **`colspan="5"`**
* [ ] There are **4** time rows; each begins with `<th scope="row">`
* [ ] Each time row contains **5** subject cells (`<td>…</td>`) — one per day
* [ ] Days are `<th scope="col">` and the page is RTL with a white background

If every item is checked, your solution is complete and should pass all tests.

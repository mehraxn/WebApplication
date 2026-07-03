# CSS Box Model

Every element on a page is a rectangular **box**. The box model describes the layers that make up that box: content, padding, border, and margin. Understanding it fixes most "why is there space there?" confusion.

```
+-----------------------------+
|          margin             |  (space outside the box)
|  +-----------------------+  |
|  |       border          |  |
|  |  +-----------------+  |  |
|  |  |    padding      |  |  |
|  |  |  +-----------+  |  |  |
|  |  |  | content   |  |  |  |
|  |  |  +-----------+  |  |  |
|  |  +-----------------+  |  |
|  +-----------------------+  |
+-----------------------------+
```

## Content
The actual text or image inside the box. Its size is controlled by `width` and `height`.

## Padding
Space **inside** the box, between the content and the border. Padding pushes the border away from the content and takes the background color.
```css
.card {
  padding: 20px;            /* all four sides */
  padding: 10px 20px;       /* top/bottom  left/right */
}
```

## Border
A line around the padding. You set its thickness, style, and color.
```css
.card {
  border: 2px solid black;
}
```

## Margin
Space **outside** the box, pushing other elements away. Margins are transparent (no background).
```css
.card {
  margin: 16px;             /* space around the whole box */
  margin: 0 auto;           /* 0 top/bottom, auto left/right = center horizontally */
}
```

## Width and height
Set the size of the content area.
```css
.box {
  width: 300px;
  height: 150px;
}
```

## `box-sizing: border-box` (very important)
By **default** (`content-box`), `width` sets only the *content* width — padding and border are added **on top**, making the box bigger than you expected.

```css
/* default: content-box */
.box {
  width: 200px;
  padding: 20px;
  border: 5px solid;
  /* actual visible width = 200 + 20 + 20 + 5 + 5 = 250px  😖 */
}
```

`box-sizing: border-box` makes `width` include the padding and border, so the box stays the size you set.
```css
.box {
  box-sizing: border-box;
  width: 200px;
  padding: 20px;
  border: 5px solid;
  /* actual visible width = 200px exactly  ✅ */
}
```

Most developers apply it to everything at the top of their CSS:
```css
* {
  box-sizing: border-box;
}
```

### Common mistakes
- **Forgetting `border-box`** and then wondering why layouts overflow — the #1 box model gotcha.
- **Confusing padding and margin** — padding = space *inside* (has background), margin = space *outside* (transparent).
- **Margin collapse** — vertical margins between two stacked elements can *merge* into one (the larger of the two), not add up. Surprising but normal.
- Setting a fixed `height` on text containers — content can overflow. Prefer letting height grow, or use `min-height`.

---

### Quick review
- Box = content → padding → border → margin (inside to outside).
- Padding is inside (colored), margin is outside (transparent).
- `box-sizing: border-box` makes `width` include padding + border — use it everywhere.

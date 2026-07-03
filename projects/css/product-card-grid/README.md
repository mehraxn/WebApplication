# Product Card Grid

## Project Overview
A responsive product grid, like an e-commerce listing page. Each card shows an image
placeholder, product name, star rating, price, and an "Add to cart" button. The grid adapts
the number of columns automatically to the screen width.

## Features
- Product cards
- Image placeholders (ready to swap for real `<img>`)
- Price for each product
- Star rating with review count
- "Add to cart" buttons
- Responsive CSS Grid layout with hover effects

## Technologies Used
- HTML5
- CSS3 (Grid, CSS variables, transitions — no Bootstrap)

## Folder Structure
```
product-card-grid/
├── index.html    # the product grid
├── style.css     # styling
├── README.md     # this file
└── screenshots/  # add screenshots here
```

## How to Run or Open
Open `index.html` directly in any web browser. Resize the window to see the grid reflow.

## What I Learned
- Building a responsive grid with `repeat(auto-fill, minmax(240px, 1fr))` (no media queries).
- Using `gap` for even spacing between cards.
- `transition` + `transform` for a hover lift, with `overflow: hidden` for clean corners.

## Resume Value
Product grids are the core of any online shop. This shows I can build a responsive,
data-style card layout with CSS Grid that looks clean at any screen size.

## Future Improvements
- Replace placeholders with real product images
- Add a "sale" badge using absolute positioning
- Render the cards dynamically from a Flask + database back-end

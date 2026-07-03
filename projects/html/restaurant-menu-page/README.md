# Restaurant Menu Page

## Project Overview
A semantic HTML menu page for a fictional Italian restaurant, "Bella Cucina." It presents
menu categories, dishes with prices and dietary labels, weekly opening hours, and contact
information — organized cleanly with semantic markup.

## Features
- Restaurant header with name and tagline
- Menu categories (Starters, Main Courses, Desserts)
- Menu items with descriptions and prices
- Dietary labels (vegetarian, vegan, gluten-free, allergens)
- Opening hours (accessible data table)
- Contact information using `<address>`
- In-page navigation between sections

## Technologies Used
- HTML5
- Semantic markup (`section`, `article`, `nav`, `address`, `table`) — no CSS yet

## Folder Structure
```
restaurant-menu-page/
├── index.html    # the menu page
├── README.md     # this file
└── screenshots/  # add screenshots here
```

## How to Run or Open
Open `index.html` directly in any web browser — no server or build step needed.

## What I Learned
- Modeling real-world content with the right semantic elements (`section` per category, `article` per dish).
- Building an accessible data table for opening hours.
- Using `<address>` for contact details.

## Resume Value
Demonstrates the ability to model real business content with semantic HTML and accessible
tables — clean, maintainable structure a business could actually use.

## Future Improvements
- Add CSS for an appealing, branded design
- Make it responsive for phones
- Add dish photos with `figure`/`figcaption`
- Add a reservation link or embedded map

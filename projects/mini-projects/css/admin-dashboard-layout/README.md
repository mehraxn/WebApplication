# Admin Dashboard Layout

## Project Overview
A static admin dashboard layout built with CSS Grid and Flexbox. It includes a sidebar, a
top navigation bar, statistic cards, a main overview panel, and a recent activity feed —
the classic "admin panel" structure — and collapses to a single column on smaller screens.

## Features
- Fixed sidebar with navigation
- Top navigation bar with search and user avatar
- Dashboard statistic cards
- Statistics section (revenue, orders, customers, refunds)
- Recent activity section
- Responsive behavior (sidebar collapses, panels stack)

## Technologies Used
- HTML5
- CSS3 (Grid + Flexbox, CSS variables — no Bootstrap)

## Folder Structure
```
admin-dashboard-layout/
├── index.html    # the dashboard layout
├── style.css     # styling
├── README.md     # this file
└── screenshots/  # add screenshots here
```

## How to Run or Open
Open `index.html` directly in any web browser. Resize the window to see the layout
collapse to a single column.

## What I Learned
- Using CSS Grid for the overall page shell (`grid-template-columns: 240px 1fr`).
- Combining Grid (structure) with Flexbox (component alignment).
- A media query to switch to a single-column mobile layout.

## Resume Value
Dashboards are one of the most common real-world UI patterns. This shows I can combine Grid
and Flexbox to build a professional, responsive layout from scratch.

## Future Improvements
- Add real charts (Chart.js) in the overview panel
- Make the sidebar collapsible with a toggle button (JavaScript)
- Add a dark mode via CSS variables

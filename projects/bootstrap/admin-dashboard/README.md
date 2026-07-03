# Admin Dashboard (Bootstrap)

## Project Overview
A static Bootstrap admin dashboard with a sidebar, summary cards, a recent-orders table,
status badges, and progress bars. It uses the Bootstrap grid to place a sidebar next to the
main content and collapses gracefully on smaller screens.

## Features
- Sidebar navigation (stacks above content on mobile)
- Top bar with search and an admin badge
- Summary cards (revenue, orders, customers, refunds)
- Recent orders table with status badges
- Monthly goals with progress bars
- Fully responsive grid

## Technologies Used
- HTML5
- Bootstrap 5 (via CDN)
- Minimal custom CSS (full-height sidebar on desktop only)

## Folder Structure
```
admin-dashboard/
├── index.html    # the dashboard
├── README.md     # this file
└── screenshots/  # add screenshots here
```

## How to Run or Open
Open `index.html` directly in any web browser. Bootstrap loads from its CDN, so an internet
connection is needed. Resize the window to see the responsive behavior.

## What I Learned
- Combining the Bootstrap grid with tables, cards, badges, and progress bars.
- Using colored `text-bg-*` cards and `progress` components.
- Making a sidebar + content layout responsive with the grid.

## Resume Value
Admin dashboards are one of the most requested UI types in real jobs. This shows I can build
a data-rich, responsive back-office interface with Bootstrap.

## Future Improvements
- Add real charts (e.g. Chart.js)
- Make the sidebar collapsible with a toggle button
- Add pagination and sorting to the table
- Connect it to a Flask back-end for live data

# Web Application Portfolio

## Overview

This repository contains my **web development learning path and portfolio projects**. It
brings together the notes, exercises, and practical applications I have built while learning
the core of modern web development:

- **HTML5** — semantic page structure
- **CSS3** — layout, responsive design, and styling
- **Bootstrap** — responsive components and grid system
- **Python / Flask** — lightweight back-end web applications
- **Jinja** — dynamic templates rendered by Flask
- **SQLite** — relational data storage

The goal is a single, organized place that shows both *how* I learned each technology
(structured notes and exercises) and *what* I can build with it (complete, documented
projects). It is aimed at demonstrating the skills of a junior web / Flask developer.

## Repository Structure

```
WebApplication/
├── education/        # notes and exercises for each technology
├── projects/         # portfolio projects (HTML, CSS, Bootstrap, Flask)
├── archive/          # original source files kept for reference
└── Polito Course/    # original university coursework (preserved, unchanged)
```

- **`education/`** — learning material organized by topic (`html/`, `css/`, `bootstrap/`,
  `flask/`), each with beginner-friendly `notes/` and hands-on `exercises/`.
- **`projects/`** — portfolio projects grouped by technology, each in its own folder with a
  README and a `screenshots/` placeholder.
- **`archive/`** — original archived files (e.g. zipped source) kept for reference.
- **`Polito Course/`** — original university coursework, **preserved exactly as submitted and
  intentionally left unchanged**.

## Technologies

- **HTML5**
- **CSS3**
- **Bootstrap** (v5)
- **Python** (3)
- **Flask**
- **Jinja** (templates)
- **SQLite** (via Python's standard-library `sqlite3`)
- **Git / GitHub**

## Education

The [`education/`](education/) folder contains notes and exercises that build up the
fundamentals step by step:

- **HTML** — [notes](education/html/) on document structure, semantic tags, forms, tables,
  media, and accessibility, plus exercises like a semantic layout, an accessible form, and a
  comparison table.
- **CSS** — [notes](education/css/) on selectors, the box model, Flexbox, Grid, positioning,
  responsive design, transitions/animations, and CSS variables, plus exercises such as a
  Flexbox navbar, a Grid gallery, and a responsive profile page.
- **Bootstrap** — [notes](education/bootstrap/) on the grid, utilities, components, forms, and
  responsive layout, plus exercises like a navbar, card grid, modal, and pricing section.
- **Flask** — [notes](education/flask/) on project structure, routing, Jinja templates, static
  files, forms, flash messages, SQLite, CRUD, error handling, and security basics, plus
  exercises building from a single route up to a full CRUD demo.

## Portfolio Projects

Each project is a self-contained folder with its own README (Project Overview, Features,
Technologies Used, Folder Structure, How to Run or Open, What I Learned, Resume Value, Future
Improvements) and a `screenshots/` folder. Category indexes:
[HTML](projects/html/README.md) · [CSS](projects/css/README.md) ·
[Bootstrap](projects/bootstrap/README.md) · [Flask](projects/flask/README.md).

### HTML Projects

| Project | Description | Technologies | Path |
|---------|-------------|--------------|------|
| Personal Resume Page | Semantic resume / CV page | HTML5 | [projects/html/personal-resume-page/](projects/html/personal-resume-page/) |
| Restaurant Menu Page | Menu with categories, prices, and opening hours | HTML5 | [projects/html/restaurant-menu-page/](projects/html/restaurant-menu-page/) |
| Blog Article Layout | Blog post with a table of contents and sidebar | HTML5 | [projects/html/blog-article-layout/](projects/html/blog-article-layout/) |
| Class Schedule Table | Weekly schedule presented as an HTML table | HTML5 | [projects/html/class-schedule-table/](projects/html/class-schedule-table/) |
| Contact Map | Contact page with an embedded map | HTML5 | [projects/html/contact-map/](projects/html/contact-map/) |
| Invitation Form | Invitation / RSVP form | HTML5 | [projects/html/invitation-form/](projects/html/invitation-form/) |
| Retro Pong | Retro-style Pong page | HTML5, JavaScript | [projects/html/retro-pong/](projects/html/retro-pong/) |
| Spanish Pronunciation Guide | Pronunciation guide with embedded audio | HTML5, audio | [projects/html/spanish-pronunciation-guide/](projects/html/spanish-pronunciation-guide/) |

### CSS Projects

| Project | Description | Technologies | Path |
|---------|-------------|--------------|------|
| Responsive Pricing Cards | Pricing cards with a highlighted plan | HTML5, CSS3 | [projects/css/responsive-pricing-cards/](projects/css/responsive-pricing-cards/) |
| Admin Dashboard Layout | Dashboard using CSS Grid + Flexbox | HTML5, CSS3 | [projects/css/admin-dashboard-layout/](projects/css/admin-dashboard-layout/) |
| Animated Login Page | Login page with transitions and animation | HTML5, CSS3 | [projects/css/animated-login-page/](projects/css/animated-login-page/) |
| Product Card Grid | Responsive e-commerce product grid | HTML5, CSS3 | [projects/css/product-card-grid/](projects/css/product-card-grid/) |
| Contact Form | Styled login/contact form | HTML5, CSS3 | [projects/css/contact-form/](projects/css/contact-form/) |
| Flight Booking UI | Travel/flight booking interface | HTML5, CSS3, JavaScript | [projects/css/flight-booking-ui/](projects/css/flight-booking-ui/) |
| Laptop Grid Layout | Product grid of laptops | HTML5, CSS3, JavaScript | [projects/css/laptop-grid-layout/](projects/css/laptop-grid-layout/) |
| Newsletter Signup | Newsletter sign-up section | HTML5, CSS3 | [projects/css/newsletter-signup/](projects/css/newsletter-signup/) |
| Profile Header | Profile header with social links | HTML5, CSS3 | [projects/css/profile-header/](projects/css/profile-header/) |
| Questionnaire | Questionnaire / survey form | HTML5, CSS3 | [projects/css/questionnaire/](projects/css/questionnaire/) |
| Restaurant Categories | Restaurant category tiles | HTML5, CSS3 | [projects/css/restaurant-categories/](projects/css/restaurant-categories/) |
| Restaurant Sidebar | Dashboard sidebar navigation | HTML5, CSS3 | [projects/css/restaurant-sidebar/](projects/css/restaurant-sidebar/) |

### Bootstrap Projects

| Project | Description | Technologies | Path |
|---------|-------------|--------------|------|
| Personal Portfolio | Responsive personal portfolio site | HTML5, Bootstrap 5 | [projects/bootstrap/personal-portfolio/](projects/bootstrap/personal-portfolio/) |
| Startup Landing Page | SaaS landing page with an FAQ accordion | HTML5, Bootstrap 5 | [projects/bootstrap/startup-landing-page/](projects/bootstrap/startup-landing-page/) |
| Admin Dashboard | Dashboard with cards, table, and progress bars | HTML5, Bootstrap 5 | [projects/bootstrap/admin-dashboard/](projects/bootstrap/admin-dashboard/) |
| Bootstrap Grid Demo | 12-column grid demonstration | HTML5, Bootstrap 5 | [projects/bootstrap/bootstrap-grid-demo/](projects/bootstrap/bootstrap-grid-demo/) |
| Bootstrap Modal Demo | Modal component demo | HTML5, Bootstrap 5 | [projects/bootstrap/bootstrap-modal-demo/](projects/bootstrap/bootstrap-modal-demo/) |
| Responsive Layout Demo | Responsive layout demonstration | HTML5, Bootstrap 5 | [projects/bootstrap/responsive-layout-demo/](projects/bootstrap/responsive-layout-demo/) |

### Flask Projects

| Project | Description | Technologies | Path |
|---------|-------------|--------------|------|
| Task Manager (SQLite) | Full CRUD task manager with status filtering | Flask, Jinja, SQLite | [projects/flask/task-manager-sqlite/](projects/flask/task-manager-sqlite/) |
| Booking Reservation App | Event booking with capacity and date checks | Flask, Jinja, SQLite | [projects/flask/booking-reservation-app/](projects/flask/booking-reservation-app/) |
| Expense Tracker | Track expenses by category with totals | Flask, Jinja, SQLite | [projects/flask/expense-tracker/](projects/flask/expense-tracker/) |
| Blog CRUD App | Blog with full post CRUD and title search | Flask, Jinja, SQLite | [projects/flask/blog-crud-app/](projects/flask/blog-crud-app/) |
| Routing Demo | Basic routing and view functions | Flask, Jinja | [projects/flask/routing-demo/](projects/flask/routing-demo/) |
| Jinja Fruit List | Rendering a list with a Jinja loop | Flask, Jinja | [projects/flask/jinja-fruit-list/](projects/flask/jinja-fruit-list/) |
| url_for & Static Demo | Serving static files with `url_for` | Flask, Jinja | [projects/flask/url-for-static-demo/](projects/flask/url-for-static-demo/) |
| Form Handling Demo | Handling form data with `request.form` | Flask, Jinja | [projects/flask/form-handling-demo/](projects/flask/form-handling-demo/) |

## Strongest Resume Projects

The projects that best demonstrate my current skills:

1. **Polito Course — final Flask project.** The [`Polito Course/`](Polito%20Course/) folder
   contains my original university coursework, including a Flask project. It has been
   **preserved unchanged** exactly as it was submitted.
2. **[Task Manager (SQLite)](projects/flask/task-manager-sqlite/)** — a complete Flask CRUD
   app: routing, Jinja templates, server-side validation, flash messages, and SQLite storage.
3. **[Booking Reservation App](projects/flask/booking-reservation-app/)** — two related tables
   with live capacity checks and date validation; shows real business logic.
4. **[Blog CRUD App](projects/flask/blog-crud-app/)** — full post CRUD plus title search and
   automatic timestamp tracking.
5. **[Personal Portfolio (Bootstrap)](projects/bootstrap/personal-portfolio/)** — a responsive
   multi-section portfolio site that ties the front-end skills together.

## How to Run Flask Projects

The Flask projects use only Flask and Python's standard library. From the repository root:

```bash
cd projects/flask/project-name
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

On **macOS / Linux**, activate the virtual environment with:

```bash
source .venv/bin/activate
```

Then open **http://127.0.0.1:5000** in your browser. Projects that use a database create
their `.db` file automatically on first run.

## Resume Value

This repository demonstrates the ability to:

- Write **semantic HTML**
- Build **responsive CSS** layouts (Flexbox, Grid, media queries)
- Develop **Bootstrap** UIs quickly
- Handle **Flask routing and templates** (Jinja)
- Build **CRUD applications**
- Use an **SQLite database** for persistent storage
- Apply **back-end validation** to user input
- Maintain clear, consistent **project organization** and documentation

## Future Improvements

- Add screenshots to each project's `screenshots/` folder
- Deploy the static projects (HTML/CSS/Bootstrap) with **GitHub Pages**
- Deploy the Flask projects to a hosting platform later
- Add **automated tests** for the Flask projects
- Add **Docker** to the strongest Flask projects for easy setup

## Repository Notes

Old GitHub Actions workflows were archived because they belonged to a previous CI/CD setup and were not needed for this web application portfolio.

---

> Note: No live demos are deployed yet. Screenshots and deployment links will be added as
> the projects go live.

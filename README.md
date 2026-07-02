# Web Application Portfolio

## 1. Overview

This repository documents my web development learning path and portfolio projects. It brings together the fundamentals and practical implementations I have built while learning:

- **HTML** — semantic page structure
- **CSS** — layouts, responsive design, and styling
- **Bootstrap** — responsive components and grid system
- **Flask** — lightweight Python web applications
- **Jinja templates** — dynamic rendering inside Flask
- **SQLite** — relational data storage

The repository is organized into two main parts:

- **`education/`** — notes, exercises, and learning material that show how I built up the fundamentals.
- **`projects/`** — portfolio-style mini projects and practical implementations.

The **`Polito Course/`** folder is preserved as original university coursework and was intentionally left unchanged.

## 2. Repository Structure

```
WebApplication/
├── education/
│   ├── html/
│   ├── css/
│   ├── bootstrap/
│   └── flask/
├── projects/
│   ├── html/
│   ├── css/
│   ├── bootstrap/
│   └── flask/
├── archive/
│   └── original-zips/
├── Polito Course/
├── README.md
└── .gitignore
```

## 3. Technologies Used

- **HTML5:** semantic page structure
- **CSS3:** layouts, responsive design, styling, forms, cards, grids
- **Bootstrap:** responsive components, grid system, modals, layout utilities
- **Flask:** routing, templates, forms, static files, small backend applications
- **Jinja:** dynamic rendering in Flask templates
- **SQLite:** database usage in the university course project
- **Git/GitHub:** version control and repository organization

## 4. Education Section

The **`education/`** directory contains the material behind the learning path:

- **Notes** — written explanations of core concepts (HTML, CSS, Bootstrap, Flask).
- **Basic exercises** — small, focused tasks practicing a single concept.
- **Small practice examples** — short demos exploring layout, styling, and templating.
- **Learning experiments** — exploratory pages used to test ideas.

These are **not** the main resume projects. They are included to show learning progress and a solid grasp of fundamentals.

## 5. Portfolio Projects

The **`projects/`** directory contains the portfolio-style work, grouped by technology.

| Project                    | Category  | Description                                                                     | Technologies              |
| -------------------------- | --------- | ------------------------------------------------------------------------------- | ------------------------- |
| Spanish Pronunciation Guide| HTML      | Interactive learning page with embedded audio for Spanish pronunciation.        | HTML                      |
| Class Schedule Table       | HTML      | Weekly class timetable built with semantic HTML tables.                         | HTML, CSS                 |
| Invitation Form            | HTML      | Event invitation page with a structured, styled form.                           | HTML, CSS                 |
| Contact Map                | HTML      | Contact page featuring an embedded location map.                                | HTML, CSS                 |
| Retro Pong                 | HTML      | Self-playing retro Pong animation rendered in the browser.                      | HTML, CSS, JavaScript     |
| Restaurant Categories      | CSS       | Restaurant category cards with custom icons and an RTL layout.                  | HTML, CSS                 |
| Newsletter Signup          | CSS       | Newsletter subscription interface with styled input and call-to-action.         | HTML, CSS                 |
| Contact Form               | CSS       | Responsive form interface with custom styling.                                  | HTML, CSS                 |
| Flight Booking UI          | CSS       | Travel booking interface layout with styled sections.                           | HTML, CSS                 |
| Profile Header             | CSS       | Social profile header with avatar and social links.                             | HTML, CSS                 |
| Questionnaire              | CSS       | Styled questionnaire / survey form layout.                                       | HTML, CSS                 |
| Restaurant Sidebar         | CSS       | Restaurant page with a fixed sidebar navigation.                                | HTML, CSS                 |
| Laptop Grid Layout         | CSS       | Product grid showcasing laptops using CSS grid.                                  | HTML, CSS, JavaScript     |
| Bootstrap Grid Demo        | Bootstrap | Demonstrates Bootstrap's 12-column responsive grid system.                      | HTML, CSS, Bootstrap      |
| Bootstrap Modal Demo       | Bootstrap | Demonstrates Bootstrap modal behavior and component structure.                  | HTML, CSS, Bootstrap      |
| Responsive Layout Demo     | Bootstrap | Responsive layout built with Bootstrap utilities and components.                | HTML, CSS, Bootstrap      |
| Jinja Fruit List           | Flask     | Flask app rendering a dynamic list with Jinja loops and conditionals.           | Python, Flask, Jinja      |
| Flask Form Handling Demo   | Flask     | Small Flask app demonstrating routes, templates, and form submission.           | Python, Flask, Jinja      |
| Routing Demo               | Flask     | Flask app illustrating multiple routes and view functions.                      | Python, Flask, Jinja      |
| URL For / Static Demo      | Flask     | Flask app demonstrating `url_for` and linking static files.                     | Python, Flask, Jinja      |

## 6. Polito Course

The **`Polito Course/`** folder contains original university coursework, labs, midterm work, and the final Flask project. It has been preserved in its original structure and was not modified during the repository reorganization.

## 7. How to Run Flask Projects

Each Flask project can be run locally:

```bash
cd projects/flask/project-folder-name
python -m venv .venv
source .venv/bin/activate   # macOS/Linux
.venv\Scripts\activate      # Windows
pip install flask
python app.py
```

Individual Flask projects may include their own `README.md` or `requirements.txt` with more specific instructions.

## 8. Resume Value

This repository demonstrates:

- Frontend fundamentals (HTML, CSS)
- Responsive layouts
- Bootstrap component usage
- Flask routing and templating
- Clear project organization
- A structured GitHub portfolio

## 9. Future Improvements

- Add screenshots for each project
- Add live demos using GitHub Pages for the static projects
- Build a polished personal portfolio website
- Add a Flask task manager app with SQLite
- Add a Flask booking app with input validation
- Add individual README files for the strongest projects

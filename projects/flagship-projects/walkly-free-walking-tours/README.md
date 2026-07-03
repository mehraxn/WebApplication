# Walkly — Free Walking Tours Platform

![Python](https://img.shields.io/badge/Python-3.x-blue)
![Flask](https://img.shields.io/badge/Flask-Web%20Application-black)
![SQLite](https://img.shields.io/badge/Database-SQLite-lightgrey)
![Bootstrap](https://img.shields.io/badge/UI-Bootstrap-purple)
![HTML5](https://img.shields.io/badge/HTML5-Semantic-orange)
![CSS3](https://img.shields.io/badge/CSS3-Responsive-blue)
![Status](https://img.shields.io/badge/Status-Completed-success)

**Walkly** is a full-stack web application for discovering, booking, and managing free walking tours.

The platform connects local guides with participants who want to explore a city through themed walking experiences. Guides can create tours, participants can reserve places for specific dates, and the system manages availability, user roles, reservations, cancellation rules, and completed-tour reports.

The project is built with **Flask**, **SQLite**, **Flask-Login**, **Jinja**, **HTML5**, **CSS3**, and **Bootstrap**.

---

## Table of Contents

- [Overview](#overview)
- [Main Features](#main-features)
- [User Roles](#user-roles)
- [Screenshots](#screenshots)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Core Modules](#core-modules)
- [Database Overview](#database-overview)
- [How to Run Locally](#how-to-run-locally)
- [Sample Accounts](#sample-accounts)
- [User Flows](#user-flows)
- [Validation and Business Rules](#validation-and-business-rules)
- [What I Learned](#what-i-learned)
- [Future Improvements](#future-improvements)
- [Author](#author)

---

## Overview

Walkly is designed as a realistic booking platform for free walking tours.

Visitors can explore tours without an account, while registered participants can reserve places for specific tour dates. Guides have their own dashboard to create and manage tours, view reservations, and report completed tours. An administrator dashboard provides a high-level overview of the platform.

The application focuses on:

- Clean role separation
- Tour discovery
- Reservation management
- Capacity control
- Authentication
- Guide dashboards
- Participant dashboards
- Admin statistics
- SQLite data persistence

---

## Main Features

### Public Tour Browsing

Visitors can browse all available walking tours without logging in.

They can view:

- Tour title
- Description
- Meeting point
- Duration
- Language
- Guide information
- Weekly schedule
- Tour stops
- Promotional photos

The homepage also supports filtering tours by:

- Date
- Duration
- Language

---

### Tour Detail Pages

Each tour has a dedicated detail page with full information about the experience.

A tour detail page includes:

- Full tour description
- List of places visited
- Meeting point
- Duration
- Language
- Maximum number of participants
- Available dates
- Promotional image gallery
- Reservation access for participants

---

### Authentication

The application uses **Flask-Login** for authentication and session management.

Users can:

- Register
- Log in
- Log out
- Access role-specific pages

The system supports different user types and protects pages based on role.

---

### Participant Reservations

Participants can reserve a place for a specific tour date.

A reservation can include:

- The participant
- Up to three additional people

So one reservation can include from **1 to 4 people**.

The system checks the remaining capacity before confirming the booking.

Example:

```text
Tour capacity: 10
Already reserved: 8
Available places: 2

A reservation for 3 people is rejected.
```

---

### Reservation Cancellation

Participants can cancel a reservation only if the cancellation is made at least **24 hours before the tour starts**.

This rule makes the reservation system more realistic and prevents last-minute cancellations after the allowed deadline.

---

### Participant Dashboard

Participants have a personal area where they can see their reservations.

The dashboard shows:

- Reserved tour
- Tour date
- Start time
- Meeting point
- Number of people included
- Additional participant names
- Cancellation availability

---

### Guide Dashboard

Guides have a dedicated dashboard to manage their tours.

Guides can:

- Create new tours
- Add weekly schedules
- Upload promotional photos
- View their own tours
- Check reservations for each tour
- See the expected number of participants for each tour date
- Submit reports for completed tours

Guides can only manage tours that they created.

---

### Tour Management

Each tour includes:

- Title
- Guide
- Weekly schedule
- Start time
- Meeting point
- Duration
- Language
- Maximum number of participants
- List of stops
- Description
- Promotional photos

The language of a tour must match one of the languages spoken by the guide.

Once a tour already has reservations, important information is protected from modification to avoid breaking existing bookings.

---

### Completed Tour Reporting

After a tour has taken place, the guide can submit a completed-tour report.

The report includes:

- Actual number of participants who attended
- Evidence photo showing that the tour took place

This simulates a real platform process where completed activities need to be reported and verified.

---

### Administrator Dashboard

The administrator has access to a platform overview page.

The admin can view:

- Registered guides
- Registered participants
- Tours created by guides
- Total number of tours
- Total number of reservations
- Reservation statistics by language

The administrator does not create tours or make reservations. The role is used only for monitoring platform activity.

---

## User Roles

| Role | Main Purpose |
|---|---|
| Visitor | Browse public tours and view tour details |
| Participant | Reserve tours and manage reservations |
| Guide | Create tours, view reservations, and submit completed-tour reports |
| Administrator | View platform statistics and user information |

---

## Screenshots

Add screenshots here after uploading them to the repository.

Recommended screenshots:

```text
screenshots/
├── homepage.png
├── tour-detail.png
├── reservation-page.png
├── participant-dashboard.png
├── guide-dashboard.png
├── completed-tour-report.png
└── admin-dashboard.png
```

Example section:

```markdown
### Homepage

![Homepage](screenshots/homepage.png)

### Tour Detail Page

![Tour Detail](screenshots/tour-detail.png)

### Guide Dashboard

![Guide Dashboard](screenshots/guide-dashboard.png)
```

---

## Technology Stack

| Area | Technology |
|---|---|
| Backend | Python, Flask |
| Authentication | Flask-Login |
| Database | SQLite |
| Templates | Jinja |
| Frontend | HTML5, CSS3 |
| UI Framework | Bootstrap |
| Styling | Custom CSS |
| File Handling | Image uploads |
| Data Storage | Relational database |

---

## Project Structure

```text
.
├── app.py
├── auth.py
├── database.py
├── guide.py
├── reservations.py
├── tours.py
├── admin.py
├── models.py
├── image_helpers.py
├── guide_overlapping_helpers.py
├── reservation_overlapping_helpers.py
├── requirements.txt
├── database.db
├── static/
│   ├── css/
│   ├── js/
│   └── uploads/
└── templates/
    ├── base.html
    ├── home.html
    ├── login.html
    ├── register.html
    ├── tour_detail.html
    ├── reservation.html
    ├── my_reservations.html
    ├── guide_dashboard.html
    ├── create_tour.html
    ├── edit_tour.html
    ├── completed_tours.html
    └── admin_dashboard.html
```

---

## Core Modules

### `app.py`

Main application entry point.

It initializes the Flask app, configures authentication, connects routes, and starts the application.

---

### `auth.py`

Handles authentication and account logic.

Main responsibilities:

- User registration
- Login
- Logout
- Role handling
- Flask-Login integration
- Safe redirects after login

---

### `database.py`

Handles SQLite database initialization.

It creates the required database tables and prepares sample data used by the application.

---

### `tours.py`

Handles public tour pages.

Main responsibilities:

- Homepage
- Tour filtering
- Tour listing
- Tour detail pages
- Public tour browsing

---

### `reservations.py`

Handles participant reservation logic.

Main responsibilities:

- Reservation creation
- Capacity validation
- Additional participant handling
- Reservation cancellation
- Participant dashboard

---

### `guide.py`

Handles guide-specific features.

Main responsibilities:

- Guide dashboard
- Tour creation
- Tour editing
- Reservation overview
- Completed-tour reporting

---

### `admin.py`

Handles administrator pages and platform statistics.

Main responsibilities:

- Guide overview
- Participant overview
- Tour overview
- Reservation statistics
- Language-based reservation counts

---

### `image_helpers.py`

Handles image upload logic.

It is used for:

- Promotional tour photos
- Completed-tour evidence photos

---

### `guide_overlapping_helpers.py`

Contains helper functions related to guide schedule validation and tour timing conflicts.

---

### `reservation_overlapping_helpers.py`

Contains helper functions related to participant reservation conflicts and timing checks.

---

## Database Overview

The application uses SQLite as its relational database.

Main tables:

| Table | Purpose |
|---|---|
| `users` | Stores participants, guides, and admin accounts |
| `tours` | Stores tour information |
| `tour_dates` | Stores generated tour dates based on weekly schedules |
| `reservations` | Stores participant reservations |
| `completed_tours` | Stores reports submitted by guides after completed tours |

---

## How to Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY_NAME.git
cd YOUR_REPOSITORY_NAME
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the virtual environment

Windows:

```bash
.venv\Scripts\activate
```

macOS/Linux:

```bash
source .venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the application

```bash
python app.py
```

### 6. Open the app in your browser

```text
http://127.0.0.1:5000
```

---

## Sample Accounts

Replace the placeholder credentials below with the real sample accounts from your database.

| Role | Email | Password |
|---|---|---|
| Participant | participant@example.com | password |
| Guide | guide@example.com | password |
| Admin | admin@example.com | password |

---

## User Flows

### Visitor Flow

```text
Open homepage
→ Browse tours
→ Apply filters
→ Open tour detail page
→ Register or log in to reserve
```

---

### Participant Flow

```text
Register or log in
→ Browse available tours
→ Open tour details
→ Select a date
→ Add extra participants if needed
→ Confirm reservation
→ View reservation in profile
→ Cancel reservation if allowed
```

---

### Guide Flow

```text
Register or log in as guide
→ Open guide dashboard
→ Create a new tour
→ Add schedule, stops, photos, and capacity
→ View reservations
→ Check expected participants
→ Submit completed-tour report after the tour
```

---

### Admin Flow

```text
Log in as admin
→ Open admin dashboard
→ View guides, participants, tours, reservations, and statistics
```

---

## Validation and Business Rules

The application includes backend validation and role-based business rules.

Examples:

- Required form fields are validated before saving data.
- Tour language must be one of the guide's spoken languages.
- Participants can reserve only available tour dates.
- A reservation cannot exceed the remaining capacity of a tour date.
- A reservation can include at most three additional people.
- Participants cannot cancel less than 24 hours before the tour starts.
- Guides can manage only their own tours.
- Participants cannot create tours.
- Guides cannot make participant reservations.
- Admin pages are protected from unauthorized access.

---

## Design Approach

Walkly is designed to feel like a small but realistic booking platform.

The design focuses on:

- Clear navigation
- Simple user flows
- Separate dashboards for different roles
- Semantic HTML structure
- Bootstrap-based responsive layout
- Custom CSS for visual identity
- Readable backend code
- Explicit business logic

The goal was to keep the app understandable while still implementing realistic full-stack behavior.

---

## What This Project Demonstrates

This project demonstrates practical experience with:

- Flask application development
- Multi-page web applications
- Authentication with Flask-Login
- Role-based access control
- SQLite database design
- Jinja template rendering
- Form handling
- Backend validation
- Reservation logic
- Capacity checking
- File upload handling
- Dashboard development
- HTML5 semantic structure
- CSS3 styling
- Bootstrap components
- Modular backend organization

---

## What I Learned

Through this project, I practiced:

- Structuring a Flask project into multiple modules
- Designing a relational database with SQLite
- Managing users with different roles
- Building secure route access based on user roles
- Creating dynamic pages with Jinja
- Handling GET and POST requests
- Validating form input on the backend
- Implementing realistic reservation rules
- Managing uploaded images
- Building dashboards for different users
- Keeping frontend and backend logic organized

---

## Future Improvements

Possible future improvements include:

- Add email confirmation during registration
- Add password reset functionality
- Add map integration for meeting points
- Add public guide profile pages
- Add participant reviews and ratings
- Add tour categories and themes
- Add search by neighborhood or stop name
- Add calendar export for reservations
- Add automated tests
- Add Docker support
- Add REST API endpoints
- Improve deployment configuration
- Improve image compression and validation
- Add pagination for large tour lists

---

## Project Status

The main functionality is complete.

Current status:

| Feature | Status |
|---|---|
| Public tour browsing | Complete |
| Tour filtering | Complete |
| User authentication | Complete |
| Participant reservations | Complete |
| Reservation cancellation rules | Complete |
| Guide dashboard | Complete |
| Tour creation | Complete |
| Completed-tour reporting | Complete |
| Admin dashboard | Complete |
| SQLite integration | Complete |
| Role-based access control | Complete |

---

## Author

Developed by **MEHRAN BAYAT**.

This project is part of my web application portfolio and demonstrates my ability to build a complete Flask-based web application with authentication, database logic, templates, validation, role-based access control, and reservation management.

---

## License

This project is intended for educational and portfolio purposes.

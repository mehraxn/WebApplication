# Booking Reservation App

## Project Overview
A small but complete **Flask application** for booking seats at events/services. Users can
browse available events, view details, make a reservation, see all reservations, and cancel
one. The app enforces capacity limits, date checks, and input validation, and stores
everything in SQLite. Built with plain Flask and `sqlite3` (no SQLAlchemy, no Flask-WTF).

## Features
1. View a list of available services/events
2. View service/event details
3. Make a reservation
4. See a list of reservations
5. Cancel a reservation
6. Capacity check before a reservation is accepted
7. Date validation (no booking past events)
8. Back-end validation for all form inputs
9. SQLite storage
10. Flash messages for feedback
11. Responsive layout

## Technologies Used
- Python 3
- Flask (routing, templates, flash messages)
- sqlite3 (Python standard library)
- Jinja2 templates with inheritance
- Plain, responsive CSS

## Folder Structure
```
booking-reservation-app/
├── app.py                    # routes, validation, request handling
├── database.py               # SQLite functions + capacity helpers
├── requirements.txt          # dependencies (Flask)
├── README.md                 # this file
├── static/
│   └── style.css             # responsive styling
├── templates/
│   ├── base.html             # shared layout + flash messages
│   ├── index.html            # list of events with availability
│   ├── service_detail.html   # single event details
│   ├── reserve.html          # reservation form
│   ├── reservations.html     # all reservations + cancel
│   └── error.html            # friendly error/404 page
└── screenshots/              # add screenshots here
```
> `booking.db` is created automatically on first run, seeded with sample events.

## How to Run or Open
```bash
pip install -r requirements.txt
python app.py
```
Then open **http://127.0.0.1:5000** in your browser.

## Database Schema
**`services`**: `id` (PK), `name`, `description`, `date`, `time`, `capacity`.
**`reservations`**: `id` (PK), `service_id` (FK), `customer_name`, `customer_email`,
`seats`, `created_at`.

**Validation:** name required; valid email format; seats positive; seats cannot exceed
available capacity (`capacity − seats already reserved`); cannot reserve for past events.

## What I Learned
- Modeling a domain across two related tables and joining them for display.
- Computing live capacity from existing reservations before accepting a new one.
- Combining date, email, and numeric validation with flash feedback and PRG.

## Resume Value
Shows I can model a real domain (events + reservations) and enforce genuine business rules:
capacity limits computed from live data, date validation, and thorough server-side input
validation — with a clean split between routes and the data layer.

## Future Improvements
- Add user accounts so people only see their own reservations
- Send confirmation emails
- Let an admin add/edit/remove events through the UI
- Move the secret key to an environment variable and deploy with `debug=False`

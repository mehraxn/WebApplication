# Walking Tours Web Application

**Student:** MEHRAN BAYAT
**Student number:** S320636
**PythonAnywhere URL:** https://mehraxn.pythonanywhere.com

This is my Flask project for a walking tours website.

## Platform and device support

This project is a browser-based web application.

The interface is desktop-first, but it is responsive and can also be used on:

* laptops
* tablets
* mobile phones

Responsiveness is mainly implemented with Bootstrap grid classes, responsive cards, responsive forms, responsive tables, and a collapsible Bootstrap navbar.

---

## User roles

The application has four main kinds of users:

* visitors
* participants
* guides
* one platform administrator

Visitors can browse tours, use filters, and read tour details.

Participants can register, log in, reserve tours, see their reservations, and cancel a reservation when cancellation is still allowed.

Guides can register, log in, create tours, edit their tours, see reservations for their tours, and report completed tours.

The administrator can log in and see the guide overview and Prova finale statistics.

The guide languages used in the project are the five languages from the assignment:

```text
Italian, English, Spanish, Portuguese, German
```

---

## Backend structure

The backend is split into several Python files:

```text
app.py
auth.py
database.py
models.py
tours.py
reservations.py
reservation_overlapping_helpers.py
guide.py
guide_overlapping_helpers.py
image_helpers.py
admin.py
```

### app.py

This is the main file of the project.

It creates the Flask app, configures Flask-Login, initializes the database, registers the routes, and defines the custom 404 and 500 error handlers.

The route URLs are registered in `app.py`, while the page logic is separated into files such as `auth.py`, `tours.py`, `reservations.py`, `guide.py`, and `admin.py`.

### auth.py

This file manages registration, login, role selection, logout, and role checking.

A user can register once as a participant and once as a guide with the same email. The database allows this by making the pair `email + role` unique.

```sql
UNIQUE(email, role)
```

Passwords are stored as hashes, not as plain text.

### database.py

This file opens the SQLite database and creates the required tables if they do not already exist.

Important tables include:

* users
* tours
* tour_stops
* tour_schedules
* tour_dates
* reservations
* reservation_extra_people
* completed_tours
* tour_photos

### models.py

This file contains the `User` class used by Flask-Login.

It stores the user id, name, email, role, and spoken languages.

### tours.py

This file manages public tour pages.

It reads tours from the database, applies the home page filters, builds calendar data, and shows tour details.

### reservations.py

This file manages participant reservation pages and reservation actions.

It checks that:

* the user is logged in
* the user is a participant
* the selected date and time are available
* the group size does not exceed the maximum capacity
* the participant does not already have another overlapping reservation
* the same real person is not guiding another tour at the selected time

Participants can cancel a reservation only if the tour is at least 24 hours away.

### reservation_overlapping_helpers.py

This file contains helper functions for reservation time conflicts.

It checks normal participant reservation overlaps.

It also checks the case where the logged-in participant also has a guide account with the same email. In that case, the user cannot reserve their own guided tour and cannot reserve another tour that overlaps with a tour they guide.

### guide.py

This file manages guide pages.

Guides can create tours, edit tours, view their dashboard, and report completed tours.

The guide dashboard shows upcoming scheduled dates and the reservation list for those dates.

### guide_overlapping_helpers.py

This file contains helper functions for guide schedule conflicts.

It checks that a guide does not create or edit tours with overlapping schedules.

### image_helpers.py

This file manages uploaded tour images.

It validates uploaded image files, checks their extensions, opens them with Pillow, converts them to RGB when needed, saves them, and stores the photo paths in the database.

### admin.py

This file manages the administrator dashboard.

The administrator can see:

* all registered guides
* tours created by each guide
* total number of guides
* total number of participants
* total number of tours
* total number of reservations
* reservations per language

---

## Database design

The project uses one `users` table for participants, guides, and the administrator.

The `role` column identifies whether the user is a participant, guide, or admin.

The same email can be used once as participant and once as guide, but not twice for the same role.

Stops are stored in a separate table because each tour has several stops.

Extra participants are stored in a separate table because one reservation can include additional people.

Tour photos are stored in a separate table because each tour has five promotional photos.

Weekly schedules are stored separately from concrete tour dates. The weekly schedule describes when a tour repeats, while `tour_dates` stores the actual future bookable dates.

---

## Main rules implemented

* Public users can browse tours without registration.
* Participants can reserve tours and manage their reservations.
* A participant cannot reserve overlapping tours.
* A participant can reserve more than one tour on the same day only if the times do not overlap.
* Maximum capacity is checked for each tour date and time.
* A logged-in guide profile cannot directly reserve tours.
* A person who also has a guide account can reserve another guide's tour as a participant only if the time does not overlap with a tour they guide.
* A person cannot reserve a tour that they guide.
* Guides can create and edit tours.
* Guides cannot create overlapping schedules.
* A tour can have more than one weekly day, but not two start times on the same weekday.
* Each tour has at least four stops.
* Each tour has five promotional photos.
* Tour languages must be among the guide's spoken languages.
* Guides can report completed tours with evidence.
* The admin dashboard shows the Prova finale statistics and guide overview.

---

## Responsiveness

The project is responsive and supports laptop, tablet, and mobile screen sizes.

This is mainly done with Bootstrap classes such as:

```text
container
row
col-12
col-md-*
col-lg-*
navbar-expand-lg
table-responsive
```

On small screens, form fields and cards stack vertically. On larger screens, they are arranged in columns.

The navbar collapses on smaller screens using Bootstrap JavaScript.

---

## External libraries or resources not covered in the course

Most libraries and tools used in the project are part of the course material, such as Flask, SQLite, Flask-Login, Werkzeug password hashing, Bootstrap, Bootstrap JavaScript, and Pillow.

The project also uses Python standard library date tools:

```text
date
datetime
```

These are not external libraries. They are used for date comparison, future tour dates, reservation cancellation rules, and completed-tour reporting windows.

The only additional frontend resource is:

```text
Bootstrap Icons
```

Bootstrap Icons is used only for small visual icons, such as the globe icon for languages and the clock icon for duration. It is a visual aid only and does not affect application logic.

---

## Credentials

The following accounts can be used to test the application.

```text
Administrator account:
email: admin@example.com
password: admin123

Participant account:
email: maryammirzakhani@gmail.com
password: 23579

Participant and Guide account:
email: meranbayat@gmail.com
password: 1234
note: this email has both a Participant profile and a Guide profile, so after login the user can choose the role.

Participant and Guide account:
email: sabersaberain@gmail.com
password: saber
note: this email has both a Participant profile and a Guide profile, so after login the user can choose the role.
```

Additional seeded accounts are also available:

```text
Guide account:
email: guide1@example.com
password: guide123

Guide account:
email: guide2@example.com
password: guide123

Participant account:
email: participant1@example.com
password: participant123

Participant account:
email: participant2@example.com
password: participant123

Participant account:
email: participant3@example.com
password: participant123
```

---

## Notes

The goal of the project was to keep the code clear, structured, and close to the course examples, while still implementing the required walking-tour functionality.

The backend is separated into files by responsibility, and the overlap checks are placed in helper files to keep the main route files easier to read and explain.

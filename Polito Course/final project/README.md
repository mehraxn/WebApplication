# Walking Tours Web Application - Backend README

This is my backend README for the Walking Tours web application project.
I wrote the backend as a Flask application with a simple structure. I tried to keep the code close to what we used in the course, so I avoided unnecessary external libraries. The backend is split into different Python files, because I wanted each file to have one clear job.

The project is a walking-tour reservation website. There are public users, participants, and guides. Public users can browse tours. Participants can register, log in, reserve tours, and cancel reservations. Guides can register, log in, create tours, edit tours, manage schedules, and report completed tours.

---

## 1. Main idea of the project

The application is for walking tours. A guide creates a tour and sets its weekly schedule. A participant can choose a future date and reserve that tour. The system checks the role of the user, the capacity of the tour, the selected date and time, and possible overlaps.

The backend tries to satisfy the project Q&A points as much as possible. I added the important checks that were risky, especially reservation overlap checking, guide schedule overlap checking, weekly repeated schedules, and completed-tour reports.

---

## 2. Backend file structure

The backend is divided like this:

```text
app.py              Main Flask app and all route connections
database.py         Database creation, schema updates, sample data, and schedule generation
models.py           User model and helper functions for logged-in user data
auth.py             Registration, login, logout, role selection, and profile image upload
tours.py            Homepage, tour details, filters, ratings, and public guide profile
reservations.py     Reservation creation, capacity check, overlap check, dashboard, and cancellation
guide.py            Guide dashboard, create/edit tour, weekly schedules, and completed tour reports
```

I kept this structure because it is easier to understand than putting everything inside one big `app.py` file.

---

## 3. Libraries used in the backend

I tried to use only libraries that are clearly connected to the course.

The backend uses:

```text
flask
flask_login
werkzeug.security
sqlite3
datetime
```

### Why I used them

- `flask` is used for the web application, routes, templates, form data, redirects, flash messages, sessions, and URLs.
- `flask_login` is used for login, logout, current user, and protected pages.
- `werkzeug.security` is used to hash passwords and check passwords.
- `sqlite3` is used for the SQLite database.
- `datetime` is used for dates, times, future dates, past dates, and overlap checking.

### Libraries I avoided

I avoided unnecessary libraries like:

```text
os
pathlib
calendar
uuid
random
PIL
```

For example, instead of using `os` or `pathlib` to create folders, I included the upload folder directly in the project:

```text
static/uploads/
```

So the backend does not need extra path libraries.

---

## 4. How to run the project

First install the requirements:

```bash
pip install -r requirements.txt
```

Then run the project:

```bash
python app.py
```

Then open the browser here:

```text
http://127.0.0.1:5000
```

---

## 5. What `app.py` does

`app.py` is the main starting file.

It does these things:

- creates the Flask app object;
- sets the secret key for sessions and login;
- sets the upload folder path;
- connects Flask-Login to the app;
- initializes the database;
- connects every URL to the correct function.

The routes are connected with `app.add_url_rule(...)`.

The main routes are:

```text
/                                  Homepage
/tour/<tour_id>                    Tour detail page
/guide/<guide_id>                  Public guide profile page
/tour/<tour_id>/reserve            Reservation page
/login                             Login page
/logout                            Logout route
/login/select-role                 Role selection after login
/register                          Register page
/participant-dashboard             Participant dashboard
/my-reservations                   Participant reservations page
/reservation/<reservation_id>/cancel Reservation cancellation
/guide-dashboard                   Guide dashboard
/guide/create-tour                 Guide create tour page
/guide/edit-tour/<tour_id>         Guide edit tour page
/guide/completed-tours             Guide completed tours page
```

---

## 6. Database features

The backend uses SQLite.

The database code is mainly in `database.py`.

The database part can:

- connect to the database;
- return rows by column name;
- create tables if they do not exist;
- add missing columns if the database is old;
- update old data when the schema changes;
- insert sample users and sample tours;
- create future tour dates from weekly schedules;
- keep data persistent after the app is restarted.

The main database tables are:

```text
users
teours/tours
tour_dates
tour_schedules
tour_stops
tour_photos
reservations
reservation_extra_people
reviews
completed_tours
```

The important tables are:

- `users`: stores participants and guides;
- `tours`: stores the main tour information;
- `tour_dates`: stores concrete generated tour dates;
- `tour_schedules`: stores the repeated weekly schedule;
- `tour_stops`: stores the stops of a tour;
- `reservations`: stores participant reservations;
- `reservation_extra_people`: stores extra people names for a reservation;
- `reviews`: stores tour reviews and ratings;
- `completed_tours`: stores reports submitted by guides after a tour is completed.

---

## 7. User and authentication features

The authentication code is in `auth.py`.

The backend supports:

- user registration;
- user login;
- user logout;
- password hashing;
- password checking;
- role-based login;
- role selection if the same email has more than one role;
- session storage;
- optional profile picture upload.

A user can register as:

```text
Participant
Guide
```

During registration, the backend can store:

- first name;
- last name;
- full name;
- email;
- password hash;
- role;
- spoken languages for guides;
- profile picture path.

The password is not checked as plain text directly. It is checked with the hashed password.

---

## 8. Login and role selection

The backend supports login with email and password.

If the email exists only once, the user logs in directly.

If the same email exists for more than one role, the backend sends the user to a role selection step. This is useful because one email can theoretically be used for both a participant and a guide account.

After login, the session stores useful information such as:

- user id;
- role;
- full name.

The backend also supports redirecting a user back to the page they wanted before login.

---

## 9. Role-based access control

The backend separates guide pages and participant pages.

Participant-only pages:

- participant dashboard;
- reservation page;
- my reservations page;
- reservation cancellation.

Guide-only pages:

- guide dashboard;
- create tour;
- edit tour;
- completed tours/report page.

The backend checks the role before allowing the user to access protected pages.

This means:

- a guide should not reserve tours as a participant;
- a participant should not create or edit guide tours;
- public users can browse tours but cannot reserve until login.

---

## 10. Public browsing features

A user who is not logged in can still use public pages.

Public users can:

- open the homepage;
- browse tours;
- filter tours;
- open a tour detail page;
- see the public guide profile;
- see tours created by a guide.

Public users cannot:

- reserve a tour;
- cancel reservations;
- create tours;
- edit tours;
- report completed tours.

---

## 11. Homepage features

The homepage shows the available tours.

The backend supports server-side filtering by:

- language;
- duration;
- selected date.

The filtering is done in the backend with SQL conditions.

The homepage can show useful tour information such as:

- title;
- image;
- description;
- guide name;
- language;
- duration;
- distance;
- meeting point;
- rating;
- future availability.

---

## 12. Tour detail page features

The tour detail page gives more complete information about one tour.

It can show:

- tour title;
- tour image;
- tour description;
- guide name;
- link to public guide profile;
- guide profile picture;
- guide spoken languages;
- tour language or languages;
- duration;
- distance;
- meeting point;
- maximum participants;
- fitness level;
- path type;
- mountain path information;
- children allowed rule;
- pets allowed rule;
- accessibility information;
- route stops;
- rest stops;
- photo stops;
- what to bring;
- audience information;
- tour photos;
- reviews;
- average rating;
- full star count;
- weekly schedule;
- future generated dates.

For logged-in participants, the backend can also show if the participant already has reservations for that tour.

---

## 13. Public guide profile feature

The project includes a public guide profile page.

This page can show:

- guide name;
- guide profile picture;
- guide spoken languages;
- all tours created by that guide;
- rating information for the guide's tours.

This was optional in the Q&A, but it is implemented because it improves the project.

---

## 14. Participant reservation features

The reservation code is in `reservations.py`.

A participant can reserve a tour by choosing:

- date;
- time;
- name;
- email;
- phone number;
- message to the guide;
- number of extra people;
- full name of each extra person.

The backend checks many things before saving the reservation.

It checks:

- the user is logged in;
- the user is a participant;
- the tour exists;
- the date and time exist for that tour;
- the selected date is not in the past;
- required fields are filled;
- extra people count is valid;
- extra participant names are filled;
- the tour has enough free capacity;
- the participant does not already have another overlapping reservation.

---

## 15. Extra people in reservation

The project allows the participant to reserve for themselves and for extra people.

The backend stores:

- the main participant in the reservation table;
- the extra people names in `reservation_extra_people`.

The capacity calculation includes:

```text
main participant + extra people
```

So if a participant reserves for themselves and two extra people, the system counts 3 people.

---

## 16. Capacity checking

Each tour has a maximum number of participants.

Before inserting a reservation, the backend calculates how many people are already reserved for that tour, date, and time.

It ignores cancelled reservations.

Then it checks:

```text
already reserved people + requested people <= maximum participants
```

If the capacity would be exceeded, the reservation is rejected.

---

## 17. Participant reservation overlap checking

This is one of the most important Q&A fixes.

The backend checks if the participant already has another active reservation that overlaps with the new one.

It compares:

- selected date;
- selected start time;
- duration of the new tour;
- existing reservation date;
- existing reservation start time;
- duration of the existing tour.

If the time intervals overlap, the new reservation is blocked.

Cancelled reservations are ignored.

This prevents a participant from booking two tours that happen at the same time.

---

## 18. Same tour on different dates

A participant can reserve the same tour on different dates.

This is allowed because the Q&A says it should be possible.

The backend does not block the same tour on another date, as long as the reservations do not overlap and capacity is available.

---

## 19. Reservation cancellation features

Participants can cancel their own reservations.

The backend checks:

- the reservation exists;
- the reservation belongs to the current participant;
- the tour date and time are valid;
- the tour starts at least 24 hours later.

If the tour starts in less than 24 hours, online cancellation is not allowed.

When a reservation is cancelled, it is not deleted from the database. Its status becomes:

```text
Cancelled
```

This keeps the reservation history.

---

## 20. Participant dashboard features

The participant dashboard can show:

- all reservations of the participant;
- upcoming reservations;
- past reservations;
- confirmed reservations;
- cancelled reservations;
- tour title;
- tour image;
- meeting point;
- reservation date;
- reservation time;
- extra people;
- reservation status;
- whether cancellation is still possible.

There is also a `my_reservations` page for a clearer list of reservations.

---

## 21. Guide registration features

When a guide registers, the backend stores the guide's spoken languages.

The project does not have a guide profile edit page for changing languages later.

This is good because the Q&A says guide languages should not change after registration.

The backend also checks tour languages against the guide's registered languages.

This means a guide should not create a tour in a language that was not selected during registration.

---

## 22. Guide dashboard features

The guide dashboard shows information about the current guide's tours.

It can show:

- tours created by the guide;
- tour ratings;
- full star count;
- scheduled dates;
- reservation summaries;
- expected participants;
- completed tour reports.

The guide dashboard also shows scheduled dates with zero reservations.

This is important because the Q&A says empty scheduled dates should also be visible to the guide.

---

## 23. Guide create tour features

The create-tour code is in `guide.py`.

A guide can create a tour with:

- title;
- main language;
- languages;
- duration;
- distance;
- maximum participants;
- meeting point;
- description;
- start point;
- stop 1;
- stop 2;
- finish point;
- rest stops;
- fitness level;
- path type;
- mountain path information;
- children allowed;
- pets allowed;
- what to bring;
- weekly schedule day;
- weekly start time;
- optional tour image.

The backend validates:

- title is not empty;
- schedule weekday is valid;
- schedule start time is valid;
- at least four stops are present;
- the tour language is allowed for that guide;
- the guide does not already have another overlapping tour;
- maximum participants is a valid number.

When the tour is saved, the backend inserts:

- the tour information;
- the tour stops;
- the weekly schedule;
- generated future dates.

---

## 24. At least four stops validation

The backend checks that the tour has at least four route points.

The four important points are:

```text
start point
stop one
stop two
finish point
```

This is stored in a separate table called `tour_stops`.

This follows the requirement that tours should have at least four stops and that it is better to store stops separately.

---

## 25. Guide edit tour features

A guide can edit only their own tours.

If a tour already has active reservations, the backend is stricter.

In that case, only the description can be updated. This protects participants from suddenly having their reserved tour changed.

If the tour has no active reservations, the guide can edit:

- title;
- languages;
- duration;
- distance;
- meeting point;
- description;
- stops;
- weekly schedule;
- tour image.

The backend checks the same important rules again during editing:

- at least four stops;
- valid weekday;
- valid start time;
- allowed language;
- no guide schedule overlap.

---

## 26. Guide schedule overlap checking

This is another important Q&A fix.

When a guide creates or edits a tour, the backend checks if the new weekly schedule overlaps with another tour from the same guide.

The overlap check uses:

- weekday;
- start time;
- duration;
- weekly minute position.

The backend also considers tours that can cross midnight or cross the end of the week.

If there is an overlap, the tour is not saved.

---

## 27. Weekly repeated schedule feature

The project supports repeated weekly schedules.

Each tour has a weekly schedule with:

```text
weekday
start time
```

The backend stores this in `tour_schedules`.

Then it generates future concrete dates in `tour_dates`.

These generated dates are used for:

- showing availability;
- making reservations;
- validating reservation date and time;
- guide dashboard;
- completed-tour reporting.

This was added because the Q&A says schedules should be weekly and not only manually fixed dates.

---

## 28. Tours crossing midnight

The backend treats the tour as belonging to the starting day.

For overlap checking, the backend calculates the start and end time using the duration.

So if a tour starts late and ends after midnight, the overlap logic can still consider the interval correctly.

---

## 29. Completed tour report features

The completed-tour code is in `guide.py`.

Guides can report tours that already happened.

The completed-tour page shows past scheduled tour dates, even when they had zero reservations.

For a completed tour report, the guide can submit:

- selected tour/date;
- actual participant count;
- notes;
- optional evidence photo.

The backend checks:

- the selected scheduled date belongs to one of the guide's tours;
- required fields are filled;
- actual participants count is a number;
- the optional evidence file has an allowed image extension.

After that, the report is inserted into `completed_tours`.

---

## 30. Empty scheduled dates for guides

The project shows scheduled dates even if nobody reserved them.

This is important because a guide should know that a tour date existed, even if there were zero participants.

The backend does not only depend on reservations for guide reporting. It also reads from `tour_dates`.

---

## 31. File upload features

The backend supports image uploads for:

- profile pictures;
- tour images;
- completed-tour evidence photos.

The accepted extensions are:

```text
jpg
jpeg
png
webp
```

The files are saved in:

```text
static/uploads/
```

I did not use extra libraries such as `PIL`, `uuid`, `os`, or `pathlib` for this.

The file names are simple and based on ids and prefixes.

---

## 32. Reviews and rating features

The backend can calculate tour ratings from the reviews table.

It can calculate:

- average rating;
- full star count.

The rating is used on tour cards, guide dashboard, guide profile, and tour detail page.

---

## 33. Payment and reward representation

The backend and interface should not support or represent cash reward or tips.

I removed tip/payment wording from the project because the Q&A says cash reward must not be represented by the application.

The project is only about tour reservation and tour management.

---

## 34. Server-side validation features

The backend does not trust only the HTML form.

It also validates data in Python.

Examples of backend validation:

- required fields;
- valid role;
- valid email/password login;
- password confirmation;
- allowed image extension;
- guide ownership of a tour;
- participant ownership of a reservation;
- reservation capacity;
- reservation overlap;
- guide schedule overlap;
- at least four stops;
- valid schedule weekday;
- valid time format;
- valid extra people names.

---

## 35. Security-related features

The backend includes these security-related points:

- passwords are hashed;
- login-required pages are protected;
- participant and guide roles are checked;
- users cannot cancel someone else's reservation;
- guides cannot edit another guide's tour;
- guides cannot report another guide's scheduled date;
- uploaded file extensions are checked;
- cancelled reservations are kept as history instead of being deleted.

---

## 36. Sample accounts

The database can create sample accounts for testing.

Example accounts:

```text
guide1@example.com / guide123
guide2@example.com / guide123
participant1@example.com / participant123
participant2@example.com / participant123
participant3@example.com / participant123
```

These are useful to test participant and guide behavior.

---

# Questions and doubts to ask the professor

These are the points that I am not 100% sure about. I should ask the professor to avoid misunderstanding the requirements.

---

## 1. One weekly schedule or multiple weekly schedules per tour?

Right now each tour has one weekly day and one start time.

Question:

> Should one tour be allowed to have multiple weekly days and times, or is one repeated weekly schedule enough?

---

## 2. Is generating future dates acceptable?

The backend stores the weekly schedule, but it also generates future concrete dates to make reservations easier.

Question:

> Is it acceptable to generate future dates from the weekly schedule, or should the dates be generated dynamically without storing them?

---

## 3. How long should future dates be generated?

The schedule is weekly, but practical reservation pages need a limited set of future dates.

Question:

> For an indefinite weekly schedule, how far into the future should the system show or generate reservable dates?

---

## 4. Should overlap checks be only for the same guide?

The backend blocks overlaps between tours of the same guide.

Question:

> Should overlap also be checked between different guides if the meeting point or route is the same, or only for the same guide?

---

## 5. Should cancelled reservations count in overlap checks?

The backend ignores cancelled reservations when checking participant overlap.

Question:

> Is it correct that cancelled reservations do not block future overlapping reservations?

---

## 6. Should same tour be allowed more than once per day?

The Q&A says the same tour should not happen more than once per day. My backend follows one weekly slot per tour.

Question:

> If a tour has multiple time slots in one day, should that be forbidden completely, or just controlled by overlap and capacity?

---

## 7. Can a guide edit schedule after reservations exist?

My backend allows only description edit after a tour has active reservations.

Question:

> Is it correct to block editing schedule, stops, language, meeting point, and capacity after reservations exist?

---

## 8. Should completed-tour reports be unique?

The completed-tour page tries to avoid showing already reported dates.

Question:

> Should the database also enforce that a guide can submit only one completed-tour report for the same tour date?

---

## 9. Is profile picture upload during registration enough?

The project supports optional profile picture upload during registration.

Question:

> Should users also have a profile edit page to change their profile picture later?

---

## 10. Is checking only file extension enough?

The backend checks file extensions like JPG, PNG, and WEBP. I avoided image-processing libraries because of the strict library rule.

Question:

> Is file extension validation enough for this project, or should the file content also be checked?

---

## 11. Should old password column be removed?

The backend uses password hashing, but the database may still keep an old password column for compatibility with old data.

Question:

> Is it acceptable to keep the old password column if login uses password hashes, or should the old column be removed completely?

---

## 12. Is admin needed?

The Q&A says admin can be implemented, but it does not seem mandatory.

Question:

> Is the participant/guide system enough, or is an admin role expected for full completion?

---

## 13. Should tour languages be a separate table?

The backend stores languages as text and validates them against the guide languages.

Question:

> Is storing languages as text acceptable, or should I create a separate table for tour languages?

---

## 14. Should extra participants be registered users?

The backend stores extra people as names in the reservation.

Question:

> Is it correct that extra participants are just names, or should every participant be registered?

---

## 15. Should empty scheduled dates be reportable with zero participants?

The backend shows empty past scheduled dates to the guide.

Question:

> If nobody reserved a scheduled tour date, should the guide still submit a completed-tour report with zero participants, or should it only be shown as information?

---

## 16. Should guide languages be editable in any way?

The backend stores guide languages during registration and does not provide a profile edit page.

Question:

> Are guide spoken languages completely fixed after registration, or can they be changed by an admin or special process?

---

## 17. Is a public guide profile required or just optional?

I implemented a public guide profile page because it was useful, but it was optional in the clarification.

Question:

> Is the public guide profile expected in the final project evaluation, or is it only a nice optional feature?

---

## 18. Should the project show both past and future scheduled meetings for every tour?

The backend has participant reservations, guide scheduled dates, and completed-tour reports.

Question:

> Do you expect a separate page that lists all past and future scheduled meetings for every tour, even when there are no reservations?

---

## 19. Should the participant see an already-reserved message on the tour page?

The backend can provide existing reservation information for the same tour.

Question:

> Is it enough to show this information on the reservation page/dashboard, or should it be clearly shown on the tour detail page too?

---

## 20. Should capacity count only registered participants or all people?

The backend counts the main participant and all extra people.

Question:

> For maximum participants, is it correct to count extra people in the same reservation as real participants for capacity?

---

# Final summary

My backend supports the main required application behavior: users can register and log in, participants can reserve tours, guides can create and edit tours, schedules repeat weekly, overlaps are checked, capacity is checked, completed tours can be reported, and the database keeps the application data.

I also tried to follow the strict library rule by using only course-related libraries and avoiding extra external libraries where possible.

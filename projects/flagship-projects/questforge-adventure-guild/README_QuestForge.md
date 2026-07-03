# QuestForge — Fantasy Adventure Guild Platform

![Python](https://img.shields.io/badge/Python-3.x-blue)
![Flask](https://img.shields.io/badge/Flask-Web%20Application-black)
![SQLite](https://img.shields.io/badge/Database-SQLite-lightgrey)
![Flask--Login](https://img.shields.io/badge/Auth-Flask--Login-green)
![Bootstrap](https://img.shields.io/badge/UI-Bootstrap-purple)
![Status](https://img.shields.io/badge/Status-Portfolio%20Project-success)

**QuestForge** is a full-stack Flask web application for managing a fantasy adventure guild.

The platform lets adventurers explore a weekly quest board, join quest sessions, reserve party roles, and manage their participations. The Guild Master can create quests, schedule sessions, monitor party composition, and keep the guild’s weekly program organized. A Guild Council administrator can review platform activity and statistics.

The project is built with **Flask**, **SQLite**, **Flask-Login**, **Jinja templates**, **HTML5**, **CSS3**, and **Bootstrap**.

---

## Table of Contents

- [Overview](#overview)
- [Concept](#concept)
- [Main Features](#main-features)
- [User Roles](#user-roles)
- [Quest Sessions](#quest-sessions)
- [Party Role System](#party-role-system)
- [Business Rules](#business-rules)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Core Modules](#core-modules)
- [Database Overview](#database-overview)
- [How to Run Locally](#how-to-run-locally)
- [Sample Accounts](#sample-accounts)
- [Screenshots](#screenshots)
- [User Flows](#user-flows)
- [What This Project Demonstrates](#what-this-project-demonstrates)
- [Future Improvements](#future-improvements)
- [Author](#author)

---

## Overview

QuestForge is a fantasy-themed web application centered around a fictional adventure guild.

The application manages a simulated week of quests, from **Monday to Sunday**. Instead of relying on real calendar dates, the app uses a **simulated current day and time** inside the fantasy week. This makes it possible to test scheduling, deadlines, availability, and modification rules in a controlled way.

The application supports:

- Public quest browsing
- Adventurer registration and login
- Quest participation reservations
- Role-based party capacity
- Overlap prevention
- Participation modification and cancellation rules
- Guild Master quest/session management
- Adventurer profile pages
- Guild Master dashboards
- Guild Council administrator statistics

---

## Concept

In QuestForge, the guild publishes a weekly board of adventure sessions. Adventurers can browse the program and join sessions based on their preferred role.

Each quest session has:

- A quest
- A day of the week
- A start time
- A location
- A difficulty level
- A quest type
- Available party roles

The application turns a fantasy guild into a realistic scheduling and booking system.

It is designed to feel like a playful fantasy product while still implementing serious web application logic: authentication, validation, relational data, permissions, scheduling rules, and dashboards.

---

## Main Features

### Public Quest Board

All users, including visitors who are not logged in, can explore the weekly quest program.

The quest board shows quest sessions ordered by:

1. Day of the week
2. Starting time

Users can filter quest sessions by:

- Day
- Quest type
- Difficulty level
- Available role

Each session can be opened to view full details.

---

### Quest Detail Pages

Each quest session has a detail page showing the information needed before joining.

A session detail page can include:

- Quest title
- Quest description
- Quest type
- Difficulty level
- Promotional image or illustration
- Day and start time
- Session location
- Duration
- Available party roles
- Remaining places per role
- Join button for authenticated adventurers

---

### Adventurer Accounts

Adventurers can register, log in, and join quest sessions.

Adventurers can:

- Browse all quest sessions
- Join a quest session
- Select a party role
- Reserve one or two places
- View their weekly participations
- Modify or cancel participations before the deadline

Each adventurer is identified by a unique login field, such as an email address or username.

---

### Guild Master Dashboard

The **Guild Master** manages the weekly quest program.

The Guild Master can:

- Create new quests
- Schedule quest sessions
- Assign sessions to locations
- Modify sessions before anyone joins
- Cancel sessions with no participants
- View participation statistics
- Check remaining capacity by role
- See the most requested roles for each session

The Guild Master can browse the website like an adventurer, but cannot join quest sessions.

---

### Guild Council Administration

The **Guild Council administrator** has a dedicated overview page for monitoring the guild.

The administrator can view:

- Registered adventurers
- Quest list
- Quest sessions
- Current participations
- Reserved places per role
- Most popular quest type
- Session with the highest number of reserved places

This role is read-only and focused on platform visibility, not direct quest management.

---

## User Roles

| Role | Description |
|---|---|
| Visitor | Can browse the weekly quest board and view session details |
| Adventurer | Can join quest sessions and manage personal participations |
| Guild Master | Can create quests, schedule sessions, and manage the weekly program |
| Guild Council Administrator | Can view users, quests, sessions, participations, and statistics |

---

## Quest Sessions

A **quest** represents the adventure itself.

Each quest includes:

- Title
- Duration in minutes
- Quest type
- Difficulty level
- Short description
- Promotional image or illustration
- Related quest sessions

A **quest session** represents a scheduled occurrence of a quest.

Each session includes:

- Day of the week
- Starting time
- Location
- Available party roles
- Current participations

Example locations:

- Dungeon Hall
- Enchanted Forest
- Wizard Tower

Example quest types:

- Combat
- Exploration
- Puzzle
- Stealth
- Magic
- Survival

Example difficulty levels:

- Easy
- Medium
- Hard
- Legendary

---

## Party Role System

Each quest session supports three role categories.

| Role | Places per Session |
|---|---:|
| Warrior | 4 places |
| Mage | 3 places |
| Healer | 2 places |

When an adventurer joins a session, they choose one role category.

A participation can reserve:

- 1 place
- 2 places

If 2 places are reserved, both places must use the same selected role.

Example:

```text
Quest Session: Crypt of the Silver Flame
Selected role: Mage
Reserved places: 2

Both places are counted as Mage places.
```

Once all places for a role are taken, adventurers can no longer join that session with that role.

---

## Business Rules

QuestForge includes several rules to keep the guild schedule realistic.

### Session Scheduling Rules

- A location can host only one quest session at the same day and time.
- The system prevents overlapping sessions in the same location.
- Quest sessions can be modified only if no adventurer has joined them.
- Quest sessions can be cancelled only if no adventurer has joined them.
- Once a quest is created, its main quest information is not modified.

---

### Participation Rules

- Adventurers must be logged in to join a session.
- An adventurer can join at most **3 quest sessions** during the week.
- An adventurer cannot join two overlapping quest sessions.
- An adventurer can reserve at most **2 places** for the same session.
- Both reserved places must use the same party role.
- A role cannot be selected if its capacity is full.

---

### Modification and Cancellation Deadline

Participations can be modified or cancelled only if the related quest session starts more than **8 hours** after the simulated current day and time.

After this deadline, the participation becomes locked.

This creates a realistic booking constraint while still allowing testing through a simulated time system.

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
| Data Storage | Relational SQLite database |
| Session Logic | Simulated weekly day/time system |

---

## Project Structure

```text
.
├── app.py
├── auth.py
├── database.py
├── quests.py
├── sessions.py
├── participations.py
├── guild_master.py
├── admin.py
├── models.py
├── helpers.py
├── requirements.txt
├── database.db
├── static/
│   ├── css/
│   ├── js/
│   └── images/
└── templates/
    ├── base.html
    ├── home.html
    ├── login.html
    ├── register.html
    ├── quest_detail.html
    ├── join_session.html
    ├── adventurer_profile.html
    ├── guild_master_dashboard.html
    ├── create_quest.html
    ├── schedule_session.html
    ├── edit_session.html
    └── admin_dashboard.html
```

> The exact file names may differ depending on the implementation, but the structure follows a modular Flask architecture.

---

## Core Modules

### `app.py`

Application entry point.

Responsible for:

- Creating the Flask app
- Configuring authentication
- Registering routes
- Starting the local development server

---

### `auth.py`

Handles authentication and account management.

Includes:

- Registration
- Login
- Logout
- Flask-Login integration
- Role-based redirects
- User session handling

---

### `database.py`

Handles SQLite database setup and initialization.

Includes:

- Database connection helpers
- Table creation
- Sample data initialization
- Database utility functions

---

### `quests.py`

Handles public quest browsing and quest detail pages.

Includes:

- Quest board
- Quest filters
- Quest detail view
- Session listing

---

### `sessions.py`

Handles quest session scheduling logic.

Includes:

- Session creation
- Location/time overlap validation
- Session modification rules
- Session cancellation rules

---

### `participations.py`

Handles adventurer participation logic.

Includes:

- Joining a quest session
- Role availability checks
- Capacity validation
- Participation modification
- Participation cancellation
- Adventurer profile data

---

### `guild_master.py`

Handles Guild Master functionality.

Includes:

- Guild Master dashboard
- Quest creation
- Session scheduling
- Session statistics
- Remaining capacity overview

---

### `admin.py`

Handles Guild Council administrator pages.

Includes:

- User overview
- Quest overview
- Session overview
- Platform statistics

---

## Database Overview

QuestForge uses SQLite as its relational database.

Possible main tables:

| Table | Purpose |
|---|---|
| `users` | Stores adventurers, Guild Master, and Guild Council admin accounts |
| `quests` | Stores quest information |
| `quest_sessions` | Stores scheduled sessions for each quest |
| `participations` | Stores adventurer reservations for quest sessions |
| `roles` | Stores role categories or role capacity logic, if implemented separately |

---

## Example Database Relationships

```text
users
  └── participations
        └── quest_sessions
              └── quests
```

A quest can have many sessions.  
A session can have many participations.  
An adventurer can have multiple participations, but only within the weekly limits.

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

Replace these placeholder credentials with the real accounts included in your database.

| Role | Username / Email | Password |
|---|---|---|
| Adventurer | adventurer@example.com | password |
| Adventurer | mage@example.com | password |
| Adventurer | warrior@example.com | password |
| Guild Master | guildmaster@example.com | password |
| Guild Council Admin | admin@example.com | password |

---

## Screenshots

Add screenshots after uploading them to the repository.

Recommended screenshots:

```text
screenshots/
├── homepage.png
├── quest-board.png
├── quest-detail.png
├── join-session.png
├── adventurer-profile.png
├── guild-master-dashboard.png
└── admin-dashboard.png
```

Example:

```markdown
### Quest Board

![Quest Board](screenshots/quest-board.png)

### Guild Master Dashboard

![Guild Master Dashboard](screenshots/guild-master-dashboard.png)
```

---

## User Flows

### Visitor Flow

```text
Open homepage
→ Browse weekly quest board
→ Filter by day, type, difficulty, or available role
→ Open quest session details
→ Register or log in to join
```

---

### Adventurer Flow

```text
Register or log in
→ Browse quest sessions
→ Open session details
→ Choose Warrior, Mage, or Healer
→ Reserve 1 or 2 places
→ View participation in profile
→ Modify or cancel before the 8-hour deadline
```

---

### Guild Master Flow

```text
Log in as Guild Master
→ Create a quest
→ Schedule quest sessions
→ Choose day, time, and location
→ Monitor participations
→ Check remaining role capacity
→ Modify or cancel empty sessions
```

---

### Guild Council Admin Flow

```text
Log in as Guild Council Admin
→ View adventurers
→ View quests and sessions
→ Review participation details
→ Check role statistics and popular quest types
```

---

## Validation and Security

The application includes validation and access-control logic.

Examples:

- Required fields are checked before saving.
- Login is required for joining quest sessions.
- Role-based pages are protected.
- Adventurers cannot access Guild Master management pages.
- Guild Master cannot join quest sessions.
- Session overlaps are prevented by day, time, and location.
- Adventurers cannot exceed the weekly participation limit.
- Role capacity is checked before confirming participation.
- Participation modification is blocked after the 8-hour deadline.
- SQLite queries should use parameterized statements to avoid SQL injection.

---

## Design Approach

QuestForge is designed as a playful fantasy application with real full-stack logic underneath.

The design goals are:

- Make the quest board easy to explore.
- Keep the fantasy theme visible but not confusing.
- Give adventurers a clear reservation flow.
- Give the Guild Master a practical management dashboard.
- Keep user roles separated.
- Use semantic HTML where possible.
- Keep CSS separate from HTML structure.
- Use Bootstrap for responsive layout and reusable components.
- Keep backend logic readable and modular.

---

## What This Project Demonstrates

This project demonstrates practical experience with:

- Flask application development
- SQLite database design
- Flask-Login authentication
- Role-based access control
- Jinja template rendering
- Form handling
- Backend validation
- Scheduling logic
- Capacity management
- Dashboard design
- Simulated time-based business rules
- Modular project organization
- Semantic HTML
- Responsive CSS and Bootstrap

---

## What I Learned

Through this project, I practiced:

- Building a multi-role Flask application
- Designing a fantasy-themed but realistic web platform
- Managing relational data with SQLite
- Creating user-specific dashboards
- Implementing reservation and capacity rules
- Preventing overlapping sessions
- Applying modification deadlines using simulated time
- Writing backend validation for business rules
- Organizing templates and static files
- Creating a complete project suitable for a portfolio

---

## Future Improvements

Possible future improvements include:

- Add character avatars for adventurers
- Add quest rewards and inventory items
- Add adventurer experience points
- Add guild ranking system
- Add quest reviews and ratings
- Add calendar-style weekly view
- Add map-style location overview
- Add email notifications
- Add automated tests
- Add Docker support
- Add REST API endpoints
- Improve admin analytics
- Add pagination for large quest boards
- Add better image upload validation

---

## Project Status

| Feature | Status |
|---|---|
| Public quest board | Complete |
| Quest filtering | Complete |
| Adventurer authentication | Complete |
| Guild Master dashboard | Complete |
| Quest creation | Complete |
| Session scheduling | Complete |
| Location/time overlap checks | Complete |
| Adventurer participation system | Complete |
| Role capacity checks | Complete |
| Participation modification deadline | Complete |
| Adventurer profile page | Complete |
| Guild Council admin dashboard | Complete |
| SQLite integration | Complete |

---

## Author

Developed by **MEHRAN BAYAT**.

This project is part of my web application portfolio and demonstrates my ability to build a complete Flask-based application with authentication, database logic, role-based access control, scheduling rules, dashboards, and a polished fantasy-themed user experience.

---

## License

This project is intended for educational and portfolio purposes.

# Backend changes for professor registration requirement

## 1. Same email can be both Guide and Participant

The `users` table was changed from this rule:

```sql
email TEXT NOT NULL UNIQUE
```

to this rule:

```sql
UNIQUE(email, role)
```

This means:

- the same email can be registered once as `Participant`;
- the same email can also be registered once as `Guide`;
- the same email cannot be registered twice with the same role.

## 2. Database migration

`database.py` now includes `migrate_users_unique_email_role()`.
When the app starts, `initialize_database()` calls this migration before the rest of the database initialization.

## 3. Registration flow

The registration page supports a preselected role using URLs such as:

- `/register?role=Participant`
- `/register?role=Guide`

When the role is selected from the reservation modal, the register page shows the selected role instead of asking again.

## 4. Reservation modal

On the reservation page, if the user is not logged in, clicking **Confirm reservation** opens a modal with choices:

- Login
- Register as Participant
- Register as Guide

If the logged-in user is a Guide, the modal explains that guide accounts cannot reserve tours and offers a participant registration/login path.

## 5. Login without checkbox

No login checkbox was added.
If the same email and password match more than one role, the backend shows a role-choice panel after the password is checked.
This allows the user to continue as Guide or Participant without using a checkbox in the login form.

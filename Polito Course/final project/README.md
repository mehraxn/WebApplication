# LA Walks

Flask final project for Introduction to Web Applications.

## Run Locally

```powershell
python -m pip install -r requirements.txt
python app.py
```

Open:

```text
http://127.0.0.1:5000/
```

The SQLite database file is `database.db`. The app runs a small startup migration to add missing exam tables and sample data without deleting existing data.

## Sample Accounts

Guide accounts:

```text
guide1@example.com / guide123
guide2@example.com / guide123
```

Participant accounts:

```text
participant1@example.com / participant123
participant2@example.com / participant123
participant3@example.com / participant123
```

## Main Routes To Test

```text
/                         Homepage and tour filters
/tour/1                   Tour details
/tour/1/reserve           Reservation page
/participant-dashboard    Participant dashboard
/my-reservations          Participant reservations and cancellation
/guide-dashboard          Guide dashboard
/guide/create-tour        Guide tour creation
/guide/completed-tours    Completed tour reports
```

## Deployment Note

PythonAnywhere deployment URL: add final URL here after deployment.

from database import ROLE_CAPACITIES, get_db_connection


SIMULATED_CURRENT_DAY = "Wednesday"
SIMULATED_CURRENT_TIME = "10:00"

DAY_ORDER = {
    "Monday": 0,
    "Tuesday": 1,
    "Wednesday": 2,
    "Thursday": 3,
    "Friday": 4,
    "Saturday": 5,
    "Sunday": 6,
}

QUEST_TYPES = [
    "Combat",
    "Exploration",
    "Puzzle",
    "Stealth",
    "Magic",
    "Survival",
]
DIFFICULTIES = ["Easy", "Medium", "Hard", "Legendary"]
LOCATIONS = [
    "Dungeon Hall",
    "Enchanted Forest",
    "Wizard Tower",
    "Dragon Cave",
    "Mystic Library",
]


def get_simulated_time():
    """Return the simulated guild day and time used by the application."""
    return {
        "day": SIMULATED_CURRENT_DAY,
        "time": SIMULATED_CURRENT_TIME,
    }


def get_day_order(day):
    """Return the Monday-to-Sunday position for a day name."""
    return DAY_ORDER.get(day, 7)


def get_role_capacity(role):
    """Return the maximum places available for a party role."""
    return ROLE_CAPACITIES.get(role, 0)


def get_reserved_places_for_role(session_id, role, exclude_participation_id=None):
    """Return how many places are reserved for one role in a session."""
    query = """
        SELECT COALESCE(SUM(places_reserved), 0) AS reserved_places
        FROM participations
        WHERE session_id = ? AND role_category = ?
    """
    parameters = [session_id, role]

    if exclude_participation_id is not None:
        query += " AND id != ?"
        parameters.append(exclude_participation_id)

    connection = get_db_connection()
    result = connection.execute(query, parameters).fetchone()
    connection.close()
    return int(result["reserved_places"])


def get_remaining_places_for_role(session_id, role, exclude_participation_id=None):
    """Return the places still available for one role in a session."""
    capacity = get_role_capacity(role)
    reserved = get_reserved_places_for_role(
        session_id,
        role,
        exclude_participation_id,
    )
    return max(capacity - reserved, 0)


def get_total_reserved_places(session_id):
    """Return the total number of reserved places in a session."""
    connection = get_db_connection()
    result = connection.execute(
        """
        SELECT COALESCE(SUM(places_reserved), 0) AS reserved_places
        FROM participations
        WHERE session_id = ?
        """,
        (session_id,),
    ).fetchone()
    connection.close()
    return int(result["reserved_places"])


def time_to_minutes(time_text):
    """Convert an HH:MM value to minutes after midnight."""
    try:
        hour_text, minute_text = time_text.split(":", 1)
        hour = int(hour_text)
        minute = int(minute_text)
    except (AttributeError, TypeError, ValueError):
        return None

    if hour < 0 or hour > 23 or minute < 0 or minute > 59:
        return None

    return hour * 60 + minute


def is_valid_time(time_text):
    """Return True only for a valid zero-padded HH:MM time."""
    return (
        isinstance(time_text, str)
        and len(time_text) == 5
        and time_text[2] == ":"
        and time_text[:2].isdigit()
        and time_text[3:].isdigit()
        and time_to_minutes(time_text) is not None
    )


def intervals_overlap(first_start, first_end, second_start, second_end):
    """Compare two half-open time intervals."""
    return first_start < second_end and second_start < first_end


def location_has_session_overlap(
    day_of_week,
    start_time,
    duration_minutes,
    location,
    ignored_session_id=None,
):
    """Check whether a location is already occupied by an overlapping session."""
    selected_start = time_to_minutes(start_time)

    if selected_start is None:
        return True

    selected_end = selected_start + duration_minutes
    query = """
        SELECT quest_sessions.id,
               quest_sessions.start_time,
               quests.duration_minutes
        FROM quest_sessions
        JOIN quests ON quests.id = quest_sessions.quest_id
        WHERE quest_sessions.day_of_week = ?
          AND quest_sessions.location = ?
    """
    parameters = [day_of_week, location]

    if ignored_session_id is not None:
        query += " AND quest_sessions.id != ?"
        parameters.append(ignored_session_id)

    connection = get_db_connection()
    existing_sessions = connection.execute(query, parameters).fetchall()
    connection.close()

    for session in existing_sessions:
        existing_start = time_to_minutes(session["start_time"])

        if existing_start is None:
            continue

        existing_end = existing_start + int(session["duration_minutes"])

        if intervals_overlap(
            selected_start,
            selected_end,
            existing_start,
            existing_end,
        ):
            return True

    return False


def hours_until_session(day, start_time):
    """Return hours from the simulated current time to a weekly session."""
    if day not in DAY_ORDER:
        return None

    current_time_minutes = time_to_minutes(SIMULATED_CURRENT_TIME)
    session_time_minutes = time_to_minutes(start_time)

    if current_time_minutes is None or session_time_minutes is None:
        return None

    current_week_minutes = (
        DAY_ORDER[SIMULATED_CURRENT_DAY] * 24 * 60 + current_time_minutes
    )
    session_week_minutes = DAY_ORDER[day] * 24 * 60 + session_time_minutes
    return (session_week_minutes - current_week_minutes) / 60


def can_modify_participation(day, start_time):
    """Return True only when a session begins strictly more than eight hours away."""
    hours_remaining = hours_until_session(day, start_time)
    return hours_remaining is not None and hours_remaining > 8

import csv
import os

class StudySession:
    """Represents a single study session with its details."""
    def __init__(self, subject, date, duration, notes):
        """
        Initializes a StudySession object.

        Args:
            subject (str): The subject of the study session.
            date (str): The date of the session in "YYYY-MM-DD" format.
            duration (int): The duration of the session in minutes.
            notes (str): Any additional notes for the session.
        """
        self.subject = subject
        self.date = date
        self.duration = duration
        self.notes = notes

session_list = []
CSV_FILE = "sessions.csv"

def save_session(session):
    """
    Adds a new study session to the in-memory list and appends it to the CSV file.

    Args:
        session (StudySession): The session object to save.
    """
    session_list.append(session)
    _append_to_csv(session)

def load_sessions():
    """
    Loads all study sessions from the CSV file into the in-memory list.

    Returns:
        list: A list of all loaded StudySession objects.
    """
    session_list.clear()
    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode="r", newline='', encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                session = StudySession(
                    row["Subject"],
                    row["Date"],
                    int(row["Duration"]),
                    row["Notes"]
                )
                session_list.append(session)
    return session_list

def update_session(index, updated_session):
    """
    Updates a study session at a specific index in the in-memory list and
    rewrites the entire CSV file to reflect the change.

    Args:
        index (int): The index of the session to update.
        updated_session (StudySession): The new session object to replace the old one.
    """
    if 0 <= index < len(session_list):
        session_list[index] = updated_session
        _write_all_to_csv()

def filter_sessions_by_date(date_str):
    """
    Filters the in-memory session list to find all sessions on a given date.

    Args:
        date_str (str): The date string in "YYYY-MM-DD" format to filter by.

    Returns:
        list: A list of StudySession objects that match the date.
    """
    return [s for s in session_list if s.date == date_str]

def _append_to_csv(session):
    """
    Appends a single study session to the CSV file.

    This is an internal function and handles creating the file and writing
    the header if it doesn't already exist.

    Args:
        session (StudySession): The session object to append.
    """
    file_exists = os.path.exists(CSV_FILE)
    with open(CSV_FILE, mode="a", newline='', encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["Subject", "Date", "Duration", "Notes"])
        if not file_exists:
            writer.writeheader()
        writer.writerow({
            "Subject": session.subject,
            "Date": session.date,
            "Duration": session.duration,
            "Notes": session.notes
        })

def _write_all_to_csv():
    """
    Overwrites the entire CSV file with all sessions currently in memory.

    This function is used for updates and deletions to ensure the file
    matches the in-memory state.
    """
    with open(CSV_FILE, mode="w", newline='', encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["Subject", "Date", "Duration", "Notes"])
        writer.writeheader()
        for session in session_list:
            writer.writerow({
                "Subject": session.subject,
                "Date": session.date,
                "Duration": session.duration,
                "Notes": session.notes
            })
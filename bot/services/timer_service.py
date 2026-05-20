from datetime import datetime
from database.db import get_connection

active_sessions = {}

def start_session(user_id, subject):
    active_sessions[user_id] = {
        "subject": subject,
        "start_time": datetime.now()
    }

def stop_session(user_id):
    if user_id not in active_sessions:
        return None

    session = active_sessions.pop(user_id)
    duration = datetime.now() - session["start_time"]
    total_seconds = int(duration.total_seconds())

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO study_sessions (user_id, subject, start_time, end_time, duration_seconds)
        VALUES (?, ?, ?, ?, ?)
    """, (
        user_id,
        session["subject"],
        session["start_time"].strftime("%Y-%m-%d %H:%M:%S"),
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        total_seconds
    ))

    conn.commit()
    conn.close()

    return session, total_seconds
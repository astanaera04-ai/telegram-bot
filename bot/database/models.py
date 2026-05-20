from .db import get_connection

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS study_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            subject TEXT,
            start_time TEXT,
            end_time TEXT,
            duration_seconds INTEGER
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_subjects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            subject_name TEXT,
            UNIQUE(user_id, subject_name)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_goals (
            user_id INTEGER PRIMARY KEY,
            daily_hours INTEGER
        )
    """)

    conn.commit()
    conn.close()
import os
import sqlite3
from datetime import datetime, timedelta

class StudyDatabase:
    def __init__(self, db_name="study_tracker.db"):
        # Дерекқор файлының нақты қай папкада тұрғанын анықтау (қате шықпас үшін)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.db_path = os.path.join(current_dir, "..", db_name)
        self.init_db() # Кестелерді құру функциясын шақыру

    def init_db(self):
        """Базадағы барлық кестелерді (Tables) құру функциясы"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # 1. Оқу сессияларын сақтайтын кесте (Кім, қанша уақыт, қай пәнді оқыды)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS study_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                user_name TEXT,
                subject TEXT,
                start_time TEXT,
                end_time TEXT,
                duration_seconds INTEGER
            )
        """)

        # Егер ескі кестеде user_name бағаны жоқ болса, қосады (Миграция)
        try:
            cursor.execute("ALTER TABLE study_sessions ADD COLUMN user_name TEXT")
        except sqlite3.OperationalError:
            pass

        # 2. Пайдаланушының жеке пәндері сақталатын кесте
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_subjects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                subject_name TEXT,
                UNIQUE(user_id, subject_name)
            )
        """)
        
        # 3. Күнделікті мақсаттары (сағатпен) сақталатын кесте
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_goals (
                user_id INTEGER PRIMARY KEY,
                daily_hours INTEGER
            )
        """)

        # 4. Бір күндік жоспарды (Schedule) сақтайтын кесте
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_schedules (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                time_slot TEXT,
                task_desc TEXT
            )
        """)

        conn.commit()
        conn.close()

    # --- Төмендегілер дерекқорға мәлімет жазатын және оқитын функциялар ---

    def add_custom_subject(self, user_id, subject_name):
        """Жаңа пән қосу. Егер ол пән бұрыннан бар болса, False қайтарады"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO user_subjects (user_id, subject_name) VALUES (?, ?)", (user_id, subject_name))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()

    def get_weekly_data(self, user_id):
        """Соңғы 7 күннің оқылған сағаттарын графикке беру үшін есептейді"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        weekly_data = {}
        now = datetime.now()
        
        # Алдымен соңғы 7 күнді бос (0 сағат) қылып дайындап аламыз
        for i in range(6, -1, -1):
            day = now - timedelta(days=i)
            day_str = day.strftime("%Y-%m-%d")
            weekly_data[day_str] = 0
            
        # SQL арқылы соңғы 7 күндегі уақыттарды күн бойынша қосып (SUM) аламыз
        cursor.execute("""
            SELECT date(start_time), SUM(duration_seconds) 
            FROM study_sessions 
            WHERE user_id = ? AND start_time >= date('now', '-7 days')
            GROUP BY date(start_time)
        """, (user_id,))
        
        # Табылған секундтарды сағатқа айналдырып, сөздікке (dictionary) жазамыз
        for row in cursor.fetchall():
            if row[0] in weekly_data:
                weekly_data[row[0]] = round(row[1] / 3600, 1)
        conn.close()
        return weekly_data

    # (Басқа get_stats_data, get_leaderboard, get_user_schedule функциялары да осылай жұмыс істейді: 
    # базаны ашады -> SQL бұйрық жібереді -> нәтижені қайтарады -> базаны жабады)
    
    # ... қалған кодтар сол күйінде ...

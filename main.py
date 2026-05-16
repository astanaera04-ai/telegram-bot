import asyncio
import logging
import sqlite3
from datetime import datetime
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import InlineKeyboardBuilder

TOKEN = "8863300742:AAH3Zg2IHP0uu_S5iN8DfmnHjd3kspEbQ5Y"

bot = Bot(token=TOKEN)
dp = Dispatcher()


# --- FSM STATES (Сұрақ-жауап күйлері) ---
class Form(StatesGroup):
    waiting_for_subject_name = State()
    waiting_for_daily_goal = State()


# --- DATABASE SETUP ---
def init_db():
    conn = sqlite3.connect("study_tracker.db")
    cursor = conn.cursor()

    # 1. Оқу сессиялары кестесі
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

    # 2. Пайдаланушының жеке пәндері
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_subjects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            subject_name TEXT,
            UNIQUE(user_id, subject_name)
        )
    """)

    # 3. Күнделікті мақсаттар (сағатпен)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_goals (
            user_id INTEGER PRIMARY KEY,
            daily_hours INTEGER
        )
    """)
    conn.commit()
    conn.close()


active_sessions = {}


# --- KEYBOARDS ---
def get_main_menu():
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="🚀 Start Studying", callback_data="menu_start"))
    builder.row(types.InlineKeyboardButton(text="📊 My Stats & Goal", callback_data="menu_stats"))
    builder.row(types.InlineKeyboardButton(text="🏆 Leaderboard", callback_data="menu_leaderboard"))
    builder.row(types.InlineKeyboardButton(text="⚙️ Settings (Subjects/Goal)", callback_data="menu_settings"))
    return builder.as_markup()


def get_settings_menu():
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="➕ Add Custom Subject", callback_data="set_add_subject"))
    builder.row(types.InlineKeyboardButton(text="🎯 Set Daily Goal", callback_data="set_daily_goal"))
    builder.row(types.InlineKeyboardButton(text="⬅️ Back to Menu", callback_data="back_to_menu"))
    return builder.as_markup()


def get_subjects_menu(user_id):
    builder = InlineKeyboardBuilder()

    # Дерекқордан пайдаланушының жеке пәндерін алу
    conn = sqlite3.connect("study_tracker.db")
    cursor = conn.cursor()
    cursor.execute("SELECT subject_name FROM user_subjects WHERE user_id = ?", (user_id,))
    rows = cursor.fetchall()
    conn.close()

    # Егер ештеңе қоспаған болса, базалық пәндер
    if not rows:
        subjects = ["English", "Coding", "Math"]
    else:
        subjects = [row[0] for row in rows]

    for sub in subjects:
        builder.row(types.InlineKeyboardButton(text=f"📚 {sub}", callback_data=f"subject_{sub}"))

    builder.row(types.InlineKeyboardButton(text="⬅️ Back", callback_data="back_to_menu"))
    return builder.as_markup()


def get_stop_menu():
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="🛑 Stop Session", callback_data="menu_stop"))
    return builder.as_markup()


# --- HANDLERS ---

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        f"Hi {message.from_user.first_name}! Welcome back to your Advanced YPT Bot 🔥\n"
        "Achieve your goals and climb the leaderboard!",
        reply_markup=get_main_menu()
    )


@dp.callback_query(F.data == "back_to_menu")
async def back_to_menu(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text("Main Menu:", reply_markup=get_main_menu())


# --- SETTINGS & CUSTOM SUBJECTS & GOALS ---
@dp.callback_query(F.data == "menu_settings")
async def settings_menu(callback: types.CallbackQuery):
    await callback.message.edit_text("⚙️ *Settings Panel*\n\nCustomize your subjects or change your daily target:",
                                     parse_mode="Markdown", reply_markup=get_settings_menu())


@dp.callback_query(F.data == "set_add_subject")
async def add_subject_start(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(Form.waiting_for_subject_name)
    await callback.message.edit_text(
        "📝 Please type the **name of the subject** you want to add (e.g., IELTS Writing, Physics):")


@dp.message(Form.waiting_for_subject_name)
async def add_subject_finish(message: types.Message, state: FSMContext):
    subject_name = message.text.strip()
    user_id = message.from_user.id

    conn = sqlite3.connect("study_tracker.db")
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO user_subjects (user_id, subject_name) VALUES (?, ?)", (user_id, subject_name))
        conn.commit()
        await message.answer(f"✅ Subject *'{subject_name}'* successfully added!", parse_mode="Markdown",
                             reply_markup=get_main_menu())
    except sqlite3.IntegrityError:
        await message.answer("❌ You already have this subject!", reply_markup=get_main_menu())
    finally:
        conn.close()
    await state.clear()


@dp.callback_query(F.data == "set_daily_goal")
async def set_goal_start(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(Form.waiting_for_daily_goal)
    await callback.message.edit_text("🎯 How many **hours** do you want to study daily? (Enter a number, e.g., 4):")


@dp.message(Form.waiting_for_daily_goal)
async def set_goal_finish(message: types.Message, state: FSMContext):
    try:
        hours = int(message.text.strip())
        user_id = message.from_user.id

        conn = sqlite3.connect("study_tracker.db")
        cursor = conn.cursor()
        cursor.execute("INSERT OR REPLACE INTO user_goals (user_id, daily_hours) VALUES (?, ?)", (user_id, hours))
        conn.commit()
        conn.close()

        await message.answer(f"🎯 Your daily target is set to *{hours} hours*! Keep it up!", parse_mode="Markdown",
                             reply_markup=get_main_menu())
    except ValueError:
        await message.answer("❌ Please enter a valid number (integer).")
    await state.clear()


# --- STUDY TIMER LOGIC ---
@dp.callback_query(F.data == "menu_start")
async def select_subject(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    if user_id in active_sessions:
        await callback.message.edit_text("You are already studying!", reply_markup=get_stop_menu())
        return
    await callback.message.edit_text("Select a subject to start:", reply_markup=get_subjects_menu(user_id))


@dp.callback_query(F.data.startswith("subject_"))
async def start_study(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    subject = callback.data.split("_")[1]

    active_sessions[user_id] = {"subject": subject, "start_time": datetime.now()}
    await callback.message.edit_text(f"⏱ Session started for *{subject}*.\nFocus and do your best! 💪",
                                     parse_mode="Markdown", reply_markup=get_stop_menu())


@dp.callback_query(F.data == "menu_stop")
async def stop_study(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    if user_id not in active_sessions:
        await callback.message.edit_text("No active session.", reply_markup=get_main_menu())
        return

    session = active_sessions.pop(user_id)
    duration = datetime.now() - session["start_time"]
    total_seconds = int(duration.total_seconds())

    # Базаға сақтау
    conn = sqlite3.connect("study_tracker.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO study_sessions (user_id, subject, start_time, end_time, duration_seconds)
        VALUES (?, ?, ?, ?, ?)
    """, (user_id, session["subject"], session["start_time"].strftime("%Y-%m-%d %H:%M:%S"),
          datetime.now().strftime("%Y-%m-%d %H:%M:%S"), total_seconds))
    conn.commit()
    conn.close()

    h, r = divmod(total_seconds, 3600)
    m, s = divmod(r, 60)
    await callback.message.edit_text(
        f"🛑 *Session finished!*\n📂 *Subject:* {session['subject']}\n⏱ *Time:* {h}h {m}m {s}s\n\nProgress saved! ☕️",
        parse_mode="Markdown", reply_markup=get_main_menu())


# --- STATISTICS & GOAL PROGRESS ---
@dp.callback_query(F.data == "menu_stats")
async def show_stats(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    today_str = datetime.now().strftime("%Y-%m-%d")

    conn = sqlite3.connect("study_tracker.db")
    cursor = conn.cursor()

    # 1. Пәндер бойынша жалпы уақыт
    cursor.execute("SELECT subject, SUM(duration_seconds) FROM study_sessions WHERE user_id = ? GROUP BY subject",
                   (user_id,))
    rows = cursor.fetchall()

    # 2. Күнделікті мақсат
    cursor.execute("SELECT daily_hours FROM user_goals WHERE user_id = ?", (user_id,))
    goal_row = cursor.fetchone()
    daily_goal_hours = goal_row[0] if goal_row else 0

    # 3. Бүгінгі оқыған уақыты (Мақсат пайызды есептеу үшін)
    cursor.execute("SELECT SUM(duration_seconds) FROM study_sessions WHERE user_id = ? AND start_time LIKE ?",
                   (user_id, f"{today_str}%"))
    today_row = cursor.fetchone()
    today_seconds = today_row[0] if today_row[0] else 0
    conn.close()

    stats_text = "📊 *Your Study Dashboard*\n\n"
    total_all = 0

    if not rows:
        stats_text += "No sessions recorded yet.\n"
    else:
        for row in rows:
            subject, total_seconds = row
            total_all += total_seconds
            h, r = divmod(total_seconds, 3600)
            m, _ = divmod(r, 60)
            stats_text += f"🔹 *{subject}:* {h}h {m}m\n"

    h_all, r_all = divmod(total_all, 3600)
    m_all, _ = divmod(r_all, 60)
    stats_text += f"\n🏆 *Total Time:* {h_all} hours, {m_all} minutes\n"
    stats_text += "-------------------------\n"

    # Күнделікті мақсат прогресін шығару
    today_h, today_r = divmod(today_seconds, 3600)
    today_m = today_r // 60
    stats_text += f"📅 *Today's Focus:* {today_h}h {today_m}m\n"

    if daily_goal_hours > 0:
        goal_seconds = daily_goal_hours * 3600
        percent = min(int((today_seconds / goal_seconds) * 100), 100)
        # Прогресс-бар сызу [████░░░░░░]
        filled_blocks = percent // 10
        bar = "█" * filled_blocks + "░" * (10 - filled_blocks)
        stats_text += f"🎯 *Daily Goal:* {daily_goal_hours}h\n📈 *Progress:* [{bar}] {percent}%\n"
    else:
        stats_text += "🎯 *Daily Goal:* Not set. Go to Settings to set one!\n"

    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="⬅️ Back", callback_data="back_to_menu"))
    await callback.message.edit_text(stats_text, parse_mode="Markdown", reply_markup=builder.as_markup())


# --- LEADERBOARD ---
@dp.callback_query(F.data == "menu_leaderboard")
async def show_leaderboard(callback: types.CallbackQuery):
    conn = sqlite3.connect("study_tracker.db")
    cursor = conn.cursor()
    # Ең көп оқыған топ-5 пайдаланушыны анықтау (бұл мысалда Telegram ID қолданылады, шынайы аттар үшін кейін профиль атын сақтаймыз)
    cursor.execute("""
        SELECT user_id, SUM(duration_seconds) 
        FROM study_sessions 
        GROUP BY user_id 
        ORDER BY SUM(duration_seconds) DESC 
        LIMIT 5
    """)
    rows = cursor.fetchall()
    conn.close()

    leader_text = "🏆 *Global Leaderboard (Top 5 Studious Users)*\n\n"
    medals = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣"]

    if not rows:
        leader_text += "The leaderboard is empty. Be the first one!"
    else:
        for i, row in enumerate(rows):
            user_id, total_seconds = row
            h = total_seconds // 3600
            m = (total_seconds % 3600) // 60
            # Өзіңіздің ID-іңізді белгілеп көрсету
            is_me = " (You)" if user_id == callback.from_user.id else ""
            leader_text += f"{medals[i]} *User ID: {user_id}*{is_me} — {h}h {m}m\n"

    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="⬅️ Back", callback_data="back_to_menu"))
    await callback.message.edit_text(leader_text, parse_mode="Markdown", reply_markup=builder.as_markup())


async def main():
    init_db()
    print("Super Bot is running...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types
from database.db import get_connection


def get_main_menu():
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="🚀 Start Studying", callback_data="menu_start"))
    builder.row(types.InlineKeyboardButton(text="📊 My Stats & Goal", callback_data="menu_stats"))
    builder.row(types.InlineKeyboardButton(text="🏆 Leaderboard", callback_data="menu_leaderboard"))
    builder.row(types.InlineKeyboardButton(text="⚙️ Settings", callback_data="menu_settings"))
    return builder.as_markup()


def get_subjects_menu(user_id):
    builder = InlineKeyboardBuilder()

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT subject_name FROM user_subjects WHERE user_id = ?", (user_id,))
    rows = cursor.fetchall()
    conn.close()

    subjects = [row[0] for row in rows] if rows else ["English", "Coding", "Math"]

    for sub in subjects:
        builder.row(types.InlineKeyboardButton(text=sub, callback_data=f"subject_{sub}"))

    return builder.as_markup()
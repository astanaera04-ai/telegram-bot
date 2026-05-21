from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder

class StudyKeyboards:
    @staticmethod
    def get_main_menu():
        """Негізгі мәзір батырмаларын Тор (Grid) түрінде қайтарады"""
        builder = InlineKeyboardBuilder()
        # builder.row арқылы батырмаларды бір қатарға екеуден қоямыз
        builder.row(
            types.InlineKeyboardButton(text="🚀 Start Study", callback_data="menu_start"),
            types.InlineKeyboardButton(text="👥 Online (⚡️)", callback_data="menu_online")
        )
        builder.row(
            types.InlineKeyboardButton(text="📊 Stats & Chart", callback_data="menu_stats"),
            types.InlineKeyboardButton(text="🏆 Leaderboard", callback_data="menu_leaderboard")
        )
        builder.row(
            types.InlineKeyboardButton(text="📅 My Daily Schedule", callback_data="menu_schedule")
        )
        builder.row(
            types.InlineKeyboardButton(text="⚙️ Settings Panel", callback_data="menu_settings")
        )
        # .as_markup() осы батырмаларды Телеграм түсінетін форматқа айналдырады
        return builder.as_markup()

    # ... қалған батырмалар да дәл осы логикамен жасалады. 
    # Батырма басылғанда ботқа callback_data ішіндегі сөз жіберіледі.

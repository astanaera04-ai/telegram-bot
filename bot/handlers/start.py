from aiogram import types, Router
from aiogram.filters import CommandStart
from bot.keyboards.inline import get_main_menu

router = Router()

def register(dp):
    dp.include_router(router)

@router.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer(
        f"👋 Hello, {message.from_user.first_name}! Welcome to your Study Tracker.\n"
        "Choose an option below to get started:",
        reply_markup=get_main_menu()
    )

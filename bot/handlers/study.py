from aiogram import types, F
from aiogram import Router
from keyboards.inline import get_subjects_menu, get_main_menu
from services.timer_service import start_session, stop_session

router = Router()

def register(dp):
    dp.include_router(router)


@router.callback_query(F.data == "menu_start")
async def select_subject(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "Select subject:",
        reply_markup=get_subjects_menu(callback.from_user.id)
    )


@router.callback_query(F.data.startswith("subject_"))
async def start_study(callback: types.CallbackQuery):
    subject = callback.data.split("_")[1]
    start_session(callback.from_user.id, subject)

    await callback.message.edit_text(f"Started {subject}")


@router.callback_query(F.data == "menu_stop")
async def stop_study(callback: types.CallbackQuery):
    result = stop_session(callback.from_user.id)

    if not result:
        await callback.message.edit_text("No session", reply_markup=get_main_menu())
        return

    session, seconds = result
    await callback.message.edit_text(f"Finished {session['subject']} ({seconds}s)")
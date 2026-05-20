from aiogram.fsm.state import State, StatesGroup

class Form(StatesGroup):
    waiting_for_subject_name = State()
    waiting_for_daily_goal = State()
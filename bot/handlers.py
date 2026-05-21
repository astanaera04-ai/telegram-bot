import asyncio
import os
from datetime import datetime
import matplotlib.pyplot as plt
from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.exceptions import TelegramBadRequest

from database import StudyDatabase
from keyboards import StudyKeyboards

# FSM (Finite State Machine) күйлері. 
# Бұл пайдаланушыдан кезекпен жауап (мәтін) күту үшін керек.
class Form(StatesGroup):
    waiting_for_subject_name = State() # Пән атын күту
    waiting_for_daily_goal = State()   # Мақсат сағатын күту
    waiting_for_time_slot = State()    # План уақытын күту
    waiting_for_task_desc = State()    # План тапсырмасын күту

class StudyHandlers:
    def __init__(self, db: StudyDatabase):
        self.db = db
        self.router = Router()
        # active_sessions — дәл қазір таймері қосылып тұрған адамдарды сақтайтын сөздік (dictionary)
        self.active_sessions = {}
        self.register_handlers()

    def register_handlers(self):
        """Телеграмнан келген сигналдарды (callback_data) тиісті функцияларға бағыттау"""
        self.router.message(Command("start"))(self.cmd_start)
        self.router.callback_query(F.data == "back_to_menu")(self.back_to_menu)
        # Мысалы: Егер пайдаланушы 'menu_schedule' батырмасын басса, show_schedule функциясы іске қосылады
        self.router.callback_query(F.data == "menu_schedule")(self.show_schedule)
        self.router.callback_query(F.data == "sched_add")(self.add_schedule_start)
        
        # FSM күйлері: Бұл жерде бот мәтін (message) күтеді
        self.router.message(Form.waiting_for_time_slot)(self.add_schedule_time)
        self.router.message(Form.waiting_for_task_desc)(self.add_schedule_finish)
        
        # ... басқа роутерлер ...

    async def start_study(self, callback: types.CallbackQuery):
        """Оқуды бастау. Пайдаланушыны active_sessions тізіміне қосу."""
        user_id = callback.from_user.id
        data_parts = callback.data.split("_")
        mode = data_parts[1] # normal немесе pomo режимі
        subject = data_parts[2]
        
        # Басталған уақытты жазып алып, сөздікке сақтаймыз
        self.active_sessions[user_id] = {
            "subject": subject,
            "start_time": datetime.now(),
            "user_name": callback.from_user.username or callback.from_user.first_name,
            "mode": mode
        }

        # Уақытты санайтын функцияны асинхронды (фондық) түрде іске қосамыз
        asyncio.create_task(self.update_live_timer(user_id, callback.message))

    async def update_live_timer(self, user_id: int, message: types.Message):
        """Фондық режимде жұмыс істеп, әр 10 секунд сайын хабарламадағы уақытты жаңартатын функция"""
        animation_frames = ["⏳", "⌛️", "🔆", "✨"]
        frame_index = 0

        # Пайдаланушы active_sessions ішінде тұрғанша цикл айнала береді
        while user_id in self.active_sessions:
            session = self.active_sessions.get(user_id)
            if not session: break

            # Өткен уақытты есептеу
            elapsed = datetime.now() - session["start_time"]
            total_seconds = int(elapsed.total_seconds())
            current_frame = animation_frames[frame_index % len(animation_frames)]
            frame_index += 1

            if session["mode"] == "pomo":
                # Помодоро логикасы (25 минуттан кері санау)
                remaining = 1500 - total_seconds
                if remaining <= 0:
                    # Уақыт бітсе, сессияны тоқтатып, базаға сақтап, ескерту жібереміз
                    self.active_sessions.pop(user_id, None)
                    self.db.save_session(...)
                    await message.answer("⏰ *Pomodoro finished!* Time for a break!")
                    break
                # ...
            
            # Хабарламаны жаңарту (edit_text)
            try:
                await message.edit_text(
                    f"{current_frame} *Subject:* {session['subject']}\n...",
                )
            except TelegramBadRequest:
                pass
            
            # 10 секунд күтеміз (жүйеге күш түспес үшін)
            await asyncio.sleep(10)

    async def show_stats(self, callback: types.CallbackQuery):
        """Статистиканы алып, Matplotlib арқылы график (сурет) сызып жіберу"""
        user_id = callback.from_user.id
        # ... базадан статистиканы алу кодтары ...

        # График жасау блогы
        weekly_data = self.db.get_weekly_data(user_id)
        days = [d[5:] for d in weekly_data.keys()]
        hours = list(weekly_data.values())

        # Графикті сызу (көк түсті бағандармен)
        plt.figure(figsize=(6, 3.5))
        plt.bar(days, hours, color='#3498db', edgecolor='#2980b9', width=0.5)
        plt.title('Weekly Study Progress (Hours)', fontsize=12, fontweight='bold')
        
        # Суретті уақытша файлға сақтау
        chart_path = f"chart_{user_id}.png"
        plt.savefig(chart_path, dpi=100)
        plt.close()

        # Суретті чатқа жіберу
        photo = types.FSInputFile(chart_path)
        await callback.message.answer_photo(photo=photo, caption="Статистика мәтіні...")
        
        # Жіберіп болған соң, компьютерде қоқыс жиналмас үшін суретті өшіріп тастау
        if os.path.exists(chart_path):
            os.remove(chart_path)

    # ... Schedule қосу (FSM) кодтары ...
    async def add_schedule_time(self, message: types.Message, state: FSMContext):
        """Скедуалдың 1-қадамы: Уақытты алып, оны уақытша жадқа (state.update_data) сақтау"""
        await state.update_data(time_slot=message.text.strip())
        # Келесі қадамға өту (тапсырма күту)
        await state.set_state(Form.waiting_for_task_desc)
        await message.answer("📝 Now type the task...")

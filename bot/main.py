import asyncio
import logging
from aiogram import Bot, Dispatcher
from database import StudyDatabase
from handlers import StudyHandlers

# Телеграмнан алған боттың жеке құпия кілті (Токен)
TOKEN = "8863300742:AAH3Zg2IHP0uu_S5iN8DfmnHjd3kspEbQ5Y"

async def main():
    # 1. Дерекқор класын іске қосамыз (Базаға қосылу осы кезде жүреді)
    db = StudyDatabase()
    
    # 2. Бот объектісін және Диспетчерді (хабарламаларды тарататын жүйе) құрамыз
    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    # 3. Хендлерлер (логика) класына дерекқорды беріп іске қосамыз
    study_handlers = StudyHandlers(db)
    # Хендлерлердің роутерін (маршрутизатор) диспетчерге тіркейміз
    dp.include_router(study_handlers.router)

    print("Super Bot Architecture is running smooth and bug-free...")
    
    # 4. Ботты тоқтаусыз жұмыс істеу режиміне (polling) қосамыз
    await dp.start_polling(bot)

if __name__ == "__main__":
    # Логтарды (терминалдағы ақпараттық хабарламаларды) қосу
    logging.basicConfig(level=logging.INFO)
    # Асинхронды main функциясын іске қосу
    asyncio.run(main())

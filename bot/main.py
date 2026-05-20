import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import TOKEN
from database.models import init_db

from handlers import start, study, stats, settings

bot = Bot(token=TOKEN)
dp = Dispatcher()

# подключаем хендлеры
start.register(dp)
study.register(dp)
stats.register(dp)
settings.register(dp)

async def main():
    await init_db()
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())

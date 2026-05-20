# Put this in both stats.py and settings.py if they are currently blank
from aiogram import Router

router = Router()

def register(dp):
    dp.include_router(router)

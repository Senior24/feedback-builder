from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from handlers.feedback import feedback_router

async def run_bot(token: str):
    default = DefaultBotProperties(parse_mode=ParseMode.HTML)
    bot = Bot(token, default=default)
    dp = Dispatcher()

    dp.include_router(feedback_router())

    await dp.start_polling(bot)

import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramConflictError, TelegramUnauthorizedError

from data.bots import running_dps
from database.sql import db
from handlers.feedback import feedback_router

async def run_bot(token: str):
    try:
        default = DefaultBotProperties(parse_mode=ParseMode.HTML)
        bot = Bot(token, default=default)
        dp = Dispatcher()

        dp.include_router(feedback_router())

        running_dps[token] = dp

        await dp.start_polling(bot)
    except TelegramConflictError:
        db.remove_bot(token)
    except TelegramUnauthorizedError:
        db.remove_bot(token)
    except asyncio.CancelledError:
        await bot.session.close()
        raise
    except Exception as error:
        ...
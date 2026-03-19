import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from data.config import BOT_TOKEN
from data.routers import routers_list
from database.sql import db
from utils.run_bot import run_bot

dp = Dispatcher()

async def main() -> None:
    default = DefaultBotProperties(parse_mode=ParseMode.HTML)
    bot = Bot(BOT_TOKEN, default=default)

    dp.include_routers(*routers_list)

    for token in db.tokens_list():
        asyncio.create_task(run_bot(token))

    print("Bot started")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

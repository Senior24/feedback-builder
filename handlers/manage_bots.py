import requests
from aiogram import Router, Bot, F
from aiogram.filters import CommandStart, CommandObject
from aiogram.types import Message
from aiogram.utils.deep_linking import create_start_link

from database.sql import db

router = Router()

@router.message(CommandStart(deep_link=True))
async def modify_bot(message: Message, command: CommandObject):
    arg = command.args

    await message.answer(f"Token: {arg.encode()}")

@router.message(F.text == "📋 Manage bots")
async def manage_bots(message: Message, bot: Bot):
    msg = ""
    for token in db.tokens_list():
        result = requests.get(f"https://api.telegram.org/bot{token}/getME")
        result = result.json()

        remove_link = await create_start_link(bot, token, encode=True)

        msg += f"{result['result']['first_name']} | <a href='{remove_link}'>Remove</a>\n"

    await message.answer(msg)

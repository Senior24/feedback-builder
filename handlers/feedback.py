from aiogram import Router, F, Bot
from aiogram.filters import CommandStart
from aiogram.types import Message

from database.sql import db

class SafeDict(dict):
    def __missing__(self, key):
        return f"{{{key}}}"

def format_message(text: str, message: Message):
    return text.format_map(SafeDict(
        name=message.from_user.full_name,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name,
    ))


def feedback_router():
    router = Router()

    @router.message(CommandStart())
    async def start(message: Message, bot: Bot):
        welcome_msg = db.get_welcome_message(bot.token)

        if welcome_msg:
            msg = format_message(welcome_msg, message)
        else:
            msg = f"Hello {message.from_user.first_name}!\n"
            msg += "Leave your question here and we will get back to you as soon as possible"

        await message.answer(msg)


    @router.message(F.text)
    async def question_submitted(message: Message, bot: Bot):
        for admin in db.admins_list(bot.token):
            await bot.forward_message(admin, message.from_user.id, message.message_id)
        await message.reply("Thank you")

    @router.message(~F.text)
    async def only_text(message: Message):
        await message.answer("Sorry, only text messages are accepted")

    return router

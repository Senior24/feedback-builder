from aiogram import Router, F, Bot
from aiogram.filters import BaseFilter, CommandStart
from aiogram.types import Message, ReactionTypeEmoji

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

class AdminFilter(BaseFilter):
    async def __call__(self, message: Message, bot: Bot):
        return message.from_user.id in db.admins_list(bot.token)


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

        if message.from_user.id in db.admins_list(bot.token):
            await message.answer("You can answer to questions by replying to messages <i>(This message won't be displayed to users)</i>")


    @router.message(AdminFilter())
    async def respond(message: Message, bot: Bot):
        try:
            await bot.copy_message(
                message.reply_to_message.forward_from.id,
                message.from_user.id,
                message.message_id
            )
            await message.react([ReactionTypeEmoji(emoji="👍")])
        except:
            await message.answer("You aren't replied to a message")


    @router.message(F.text)
    async def question_submitted(message: Message, bot: Bot):
        for admin in db.admins_list(bot.token):
            await bot.forward_message(admin, message.from_user.id, message.message_id)
        await message.reply("Thank you")


    @router.message(~F.text)
    async def only_text(message: Message):
        await message.answer("Sorry, only text messages are accepted")


    return router

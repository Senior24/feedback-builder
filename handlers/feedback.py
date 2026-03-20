from aiogram import Router, F, Bot
from aiogram.filters import CommandStart
from aiogram.types import Message

def feedback_router(owners_id: list[int] = None):
    router = Router()

    @router.message(CommandStart())
    async def start(message: Message):
        msg = f"Hello {message.from_user.first_name}!\n"
        msg += "Leave your question here and we will get back to you as soon as possible"

        await message.answer(msg)


    @router.message(F.text)
    async def question_submitted(message: Message, bot: Bot):
        await message.reply("Thank you")

    @router.message(~F.text)
    async def only_text(message: Message):
        await message.answer("Sorry, only text messages are accepted")

    return router

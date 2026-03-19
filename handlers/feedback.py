from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message

def feedback_router():
    router = Router()

    @router.message(CommandStart())
    async def start(message: Message):
        msg = f"Hello {message.from_user.first_name}!\n"
        msg += "Leave your question here and we will get back to you as soon as possible"

        await message.answer(msg)


    @router.message(F.text)
    async def question_submitted(message: Message):
        await message.reply("Thank you")

    return router

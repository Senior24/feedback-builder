from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from database.sql import db
from keyboards.reply import start_keyboard

router = Router()

@router.message(CommandStart())
async def start(message: Message):
    if not db.check_user(message.from_user.id):
        db.add_user(message.from_user.id)
        msg = f"Hello, {message.from_user.first_name}!\n"
        msg += "This bot helps you to create your own customer support bot without difficulty\n"
        msg += "Click one of the buttons below to get started"
        await message.answer(msg, reply_markup=start_keyboard(message.from_user.id))
    else:
        await message.answer("🔄️ Bot successfully updated", reply_markup=start_keyboard(message.from_user.id))


@router.message((F.text == "🚫 Cancel") | (F.text == "/cancel"))
async def cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Cancelled", reply_markup=start_keyboard(message.from_user.id))

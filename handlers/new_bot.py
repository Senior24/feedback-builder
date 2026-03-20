import asyncio
import requests

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

from database.sql import db
from keyboards.reply import cancel_button, start_keyboard
from utils.run_bot import run_bot

router = Router()

class GetToken(StatesGroup):
    token = State()

@router.message(F.text == "➕ New bot")
async def new_bot(message: Message, state: FSMContext):
    if db.check_pro(message.from_user.id) or db.bots_count(message.from_user.id) == 0:
        await state.set_state(GetToken.token)
        await message.answer("Enter your bot token", reply_markup=cancel_button)
    else:
        await message.answer("Sorry but you can add only one bot. Purchase Pro to add more bots")


@router.message(GetToken.token, F.text == "🚫 Cancel")
async def cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Cancelled", reply_markup=start_keyboard(message.from_user.id))


@router.message(GetToken.token, F.text)
async def check_token(message: Message, state: FSMContext):
    if db.check_bot(message.text):
        await message.answer("You already added this bot")
        return

    result = requests.get(f"https://api.telegram.org/bot{message.text}/getME")
    result = result.json()

    if result['ok']:
        db.add_bot(message.from_user.id, message.text)
        await state.clear()
        asyncio.create_task(run_bot(message.text))
        await message.answer(f"{result['result']['first_name']} bot added successfully",
                             reply_markup=start_keyboard(message.from_user.id))
    else:
        await message.answer("This token is invalid")

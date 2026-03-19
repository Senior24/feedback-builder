import requests

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

from database.sql import db

router = Router()

class GetToken(StatesGroup):
    token = State()

@router.message(F.text == "➕ New bot")
async def new_bot(message: Message, state: FSMContext):
    if db.bots_count(message.from_user.id) == 0:
        await state.set_state(GetToken.token)
        await message.answer("Enter your bot token")
    else:
        await message.answer("Sorry but you can add only one bot. Purchase premium to add more bots")


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
        await message.answer(f"Your bot {result['result']['first_name']} successfully added")
    else:
        await message.answer("This token is invalid")

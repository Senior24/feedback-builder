from aiogram import Router, Bot, F
from aiogram.filters import CommandStart, CommandObject
from aiogram.types import Message, CallbackQuery

from database.sql import db
from keyboards.inline import bots_list, bot_settings

router = Router()

@router.message(CommandStart(deep_link=True))
async def modify_bot(message: Message, command: CommandObject):
    arg = command.args

    await message.answer(f"Token: {arg.encode()}")


@router.message(F.text == "📋 Manage bots")
async def manage_bots(message: Message):
    if db.bots_count(message.from_user.id) > 0:
        await message.answer("Select one of the bots", reply_markup=bots_list(message.from_user.id))
    else:
        await message.answer("You haven't added any bots")


@router.callback_query(F.data.startswith("bot"))
async def bot_menu(callback: CallbackQuery):
    token = callback.data[3:]
    await callback.message.edit_text("Settings", reply_markup=bot_settings(token))


@router.callback_query(F.data.in_("@"))
async def manage(callback: CallbackQuery):
    data = callback.data.split("@")
    command = data[0]
    token = data[1]

    if command == "edit":
        ...
    if command == "ma":
        ...
    if command == "rm":
        ...


@router.callback_query(F.data.startswith("back"))
async def back(callback: CallbackQuery):
    page = callback.data.split("_")[1]

    if page == "bot":
        await callback.message.edit_text("Select one of the bots",
                                         reply_markup=bots_list(callback.from_user.id))

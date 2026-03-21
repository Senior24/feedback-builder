from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery

from database.sql import db
from keyboards.inline import bots_list, bot_settings
from keyboards.reply import cancel_button, start_keyboard

router = Router()

class WelcomeMessage(StatesGroup):
    message = State()

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


@router.callback_query(F.data.contains("@"))
async def manage(callback: CallbackQuery, state: FSMContext):
    data = callback.data.split("@")
    command = data[0]
    token = data[1]

    if command == "edit":
        if db.check_pro(callback.from_user.id):
            await callback.message.delete()
            await state.set_state(WelcomeMessage.message)
            await state.update_data(token=token)

            msg = "Send a custom welcome message (text-only)\n"
            msg += "The welcome message appears to users when they send the <code>/start</code> command\n"
            msg += "You can use format tags for personalisation:\n"
            msg += "<code>{name}</code> - displays the full name of the user\n"
            msg += "<code>{first_name}</code> - displays the first name of the user\n"
            msg += "<code>{last_name}</code> - displays the last name of the user\n"
            await callback.message.answer(msg, reply_markup=cancel_button)
        else:
            await callback.answer("This is a Pro feature")
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


@router.message(WelcomeMessage.message, F.text)
async def set_message(message: Message, state: FSMContext):
    data = await state.get_data()
    await state.clear()
    db.set_welcome_message(message.text, data['token'])
    await message.answer("Successfully set welcome message",
                         reply_markup=start_keyboard(message.from_user.id))


@router.message(WelcomeMessage.message, ~F.text)
async def text_only(message: Message):
    await message.answer("Only text messages are allowed")

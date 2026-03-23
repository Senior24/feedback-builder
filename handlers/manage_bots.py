from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery

from contextlib import suppress

from data.bots import running_bots, running_dps
from database.sql import db
from keyboards.inline import bots_list, bot_settings, manage_admins
from keyboards.reply import cancel_button, start_keyboard

router = Router()

class WelcomeMessage(StatesGroup):
    message = State()

class AddAdmin(StatesGroup):
    admin = State()

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

    if not db.check_bot(token):
        await callback.message.delete()
        return

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
            msg += "<code>{last_name}</code> - displays the last name of the user\n\n"

            current_message = db.get_welcome_message(token)

            if current_message:
                msg += "Current message:\n" + current_message

            await callback.message.answer(msg, reply_markup=cancel_button)
        else:
            await callback.answer("This is a Pro feature")
    if command == "ma":
        if db.check_pro(callback.from_user.id):
            await callback.message.edit_text("Add admin or remove by clicking on ID",
                                             reply_markup=manage_admins(token))
        else:
            await callback.answer("This is a Pro feature")
    if command == "rm":
        db.remove_bot(token)

        await running_dps[token].stop_polling()
        running_bots[token].cancel()

        del running_bots[token]
        del running_dps[token]

        await callback.answer("Deleted")
        await callback.message.delete()


@router.callback_query(F.data.startswith("back"))
async def back(callback: CallbackQuery):
    page = callback.data.split("%")[1]

    if page == "bot":
        await callback.message.edit_text("Select one of the bots",
                                         reply_markup=bots_list(callback.from_user.id))
    else:
        await callback.message.edit_text("Settings", reply_markup=bot_settings(page))


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


@router.callback_query(F.data.contains("$"))
async def admins_list(callback: CallbackQuery, state: FSMContext):
    data = callback.data.split("$")
    command = data[0]
    token = data[1]

    if command == "add":
        await state.set_state(AddAdmin.admin)
        await state.update_data(token=token)
        await callback.answer()
        await callback.message.answer("Forward a message from a user to add them as an administrator", reply_markup=cancel_button)
    else:
        admin = data[2]

        try:
            db.admin(int(admin), token, remove=True)
            await callback.answer("Successfully removed")
        except:
            await callback.answer("Already removed")

        with suppress(Exception):
            await callback.message.edit_reply_markup(reply_markup=manage_admins(token))


@router.message(AddAdmin.admin)
async def add_admin(message: Message, state: FSMContext):
    data = await state.get_data()
    try:
        if message.forward_from.id not in db.admins_list(data['token']):
            db.admin(message.forward_from.id, data['token'], add=True)
            await state.clear()
            await message.answer("New admin added successfully",
                                 reply_markup=start_keyboard(message.from_user.id))
        else:
            await message.answer("This admin already exists")
    except:
        await message.answer("This is not a forwarded message")

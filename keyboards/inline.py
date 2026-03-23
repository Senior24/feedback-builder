import requests

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.sql import db

def bots_list(user_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for token in db.tokens_list(user_id):
        result = requests.get(f"https://api.telegram.org/bot{token}/getME")
        result = result.json()

        builder.button(text=result['result']['first_name'], callback_data="bot"+token)

    builder.adjust(1)
    return builder.as_markup()

def bot_settings(token: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📝 Edit welcome message", callback_data="edit@"+token)],
        [InlineKeyboardButton(text="👤 Manage admins", callback_data="ma@"+token)],
        [InlineKeyboardButton(text="🗑️ Remove bot", callback_data="rm@"+token)],
        [InlineKeyboardButton(text="🔙 Back", callback_data="back_bot")]
    ])

def manage_admins(token: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    admins = db.admins_list(token, with_owner=False)

    builder.button(text="➕ Add admin", callback_data=f"add${token}")

    for admin in admins:
        builder.button(text=f"Remove: {admin}", callback_data=f"rm${token}${admin}")

    builder.button(text="🔙 Back", callback_data="back_bot")

    builder.adjust(1)
    return  builder.as_markup()

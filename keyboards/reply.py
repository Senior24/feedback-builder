from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from database.sql import db

def start_keyboard(user_id: int) -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    builder.button(text="➕ New bot")
    builder.button(text="📋 Manage bots")

    if not db.check_pro(user_id):
        builder.button(text="💎 Buy Pro")

    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)

cancel_button = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="🚫 Cancel")]
], resize_keyboard=True)

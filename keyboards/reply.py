from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

start_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="➕ New bot")],
    [KeyboardButton(text="📋 Manage bots")]
], resize_keyboard=True)

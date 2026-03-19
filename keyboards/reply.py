from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

start_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="➕ New bot")],
    [KeyboardButton(text="📋 Manage bots")],
    [KeyboardButton(text="💎 Buy Pro")]
], resize_keyboard=True)

cancel_button = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="🚫 Cancel")]
], resize_keyboard=True)

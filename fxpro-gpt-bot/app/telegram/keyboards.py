from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def start_keyboard():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton("🟢 Старт"))
    kb.add(KeyboardButton("🛑 Стоп"))
    return kb

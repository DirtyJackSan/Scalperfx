from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def settings_keyboard():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton("⚙️ Настройки"))
    kb.add(KeyboardButton("📊 Пары"))
    kb.add(KeyboardButton("📈 Плечо"))
    kb.add(KeyboardButton("💰 Риск"))
    kb.add(KeyboardButton("▶️ Запуск"))
    kb.add(KeyboardButton("⛔ Стоп"))
    return kb

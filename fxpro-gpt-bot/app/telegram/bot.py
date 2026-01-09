import os
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from dotenv import load_dotenv

from telegram.states import LoginState
from telegram.keyboards import start_keyboard
from users.user_manager import UserManager
from users.sessions import SessionStore
from mt5.connector import connect
from utils.crypto import encrypt

load_dotenv()

bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher(bot, storage=MemoryStorage())

users = UserManager()
sessions = SessionStore()

@dp.message_handler(commands=["start"])
async def start(msg: types.Message):
    users.create_user(msg.from_user.id)
    await msg.answer("Добро пожаловать. Нажмите 🟢 Старт", reply_markup=start_keyboard())

@dp.message_handler(lambda m: m.text == "🟢 Старт")
async def start_login(msg: types.Message):
    await msg.answer("Введите логин от FXPro MT5")
    await LoginState.waiting_login.set()

@dp.message_handler(state=LoginState.waiting_login)
async def get_login(msg: types.Message, state: FSMContext):
    await state.update_data(login=msg.text)
    await msg.answer("Введите пароль")
    await LoginState.waiting_password.set()

@dp.message_handler(state=LoginState.waiting_password)
async def get_password(msg: types.Message, state: FSMContext):
    data = await state.get_data()
    login = data["login"]
    password = msg.text

    encrypt(password)

    account = connect(login, password)

    if account:
        sessions.create(msg.from_user.id, login)
        await msg.answer(
            f"✅ Счёт подключён\nБаланс: {account['balance']} {account['currency']}"
        )
    else:
        await msg.answer("❌ Ошибка подключения")

    await state.finish()

def start_bot():
    executor.start_polling(dp)

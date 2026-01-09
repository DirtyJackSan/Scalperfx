import os
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from dotenv import load_dotenv

from app.telegram.states import LoginState
from app.telegram.trade_states import TradeSettingsState
from app.telegram.keyboards import start_keyboard
from app.telegram.trade_keyboards import settings_keyboard
from app.users.user_manager import UserManager
from app.users.sessions import SessionStore
from app.users.trade_settings import TradeSettings
from app.mt5.connector import connect
from app.utils.crypto import encrypt

load_dotenv()

bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher(bot, storage=MemoryStorage())

users = UserManager()
sessions = SessionStore()
trade_settings = TradeSettings()


@dp.message_handler(commands=["start"])
async def start(msg: types.Message):
    users.create_user(msg.from_user.id)
    trade_settings.init_user(msg.from_user.id)
    await msg.answer("Добро пожаловать", reply_markup=start_keyboard())


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
            f"✅ Счёт подключён\nБаланс: {account['balance']} {account['currency']}",
            reply_markup=settings_keyboard()
        )
    else:
        await msg.answer("❌ Ошибка подключения")

    await state.finish()


@dp.message_handler(lambda m: m.text == "📊 Пары")
async def set_pairs(msg: types.Message):
    await msg.answer("Введите пары через запятую (пример: EURUSD,XAUUSD)")
    await TradeSettingsState.waiting_pairs.set()


@dp.message_handler(state=TradeSettingsState.waiting_pairs)
async def save_pairs(msg: types.Message, state: FSMContext):
    pairs = [p.strip().upper() for p in msg.text.split(",")]
    trade_settings.set_pairs(msg.from_user.id, pairs)
    await msg.answer(f"✅ Пары сохранены: {pairs}")
    await state.finish()


@dp.message_handler(lambda m: m.text == "📈 Плечо")
async def set_leverage(msg: types.Message):
    await msg.answer("Введите плечо (100 / 200 / 500)")
    await TradeSettingsState.waiting_leverage.set()


@dp.message_handler(state=TradeSettingsState.waiting_leverage)
async def save_leverage(msg: types.Message, state: FSMContext):
    trade_settings.set_leverage(msg.from_user.id, int(msg.text))
    await msg.answer(f"✅ Плечо установлено: 1:{msg.text}")
    await state.finish()


@dp.message_handler(lambda m: m.text == "💰 Риск")
async def set_risk(msg: types.Message):
    await msg.answer("Введите риск на сделку (%)")
    await TradeSettingsState.waiting_risk.set()


@dp.message_handler(state=TradeSettingsState.waiting_risk)
async def save_risk(msg: types.Message, state: FSMContext):
    trade_settings.set_risk(msg.from_user.id, float(msg.text))
    await msg.answer(f"✅ Риск установлен: {msg.text}%")
    await state.finish()


def start_bot():
    executor.start_polling(dp)

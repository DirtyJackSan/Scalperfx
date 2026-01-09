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

from app.risk.risk_state import RiskState
from app.risk.risk_engine import RiskEngine

load_dotenv()

bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher(bot, storage=MemoryStorage())

users = UserManager()
sessions = SessionStore()
trade_settings = TradeSettings()

risk_state = RiskState()
risk_engine = RiskEngine(risk_state)


@dp.message_handler(commands=["start"])
async def start(msg: types.Message):
    users.create_user(msg.from_user.id)
    trade_settings.init_user(msg.from_user.id)
    risk_state.init_user(msg.from_user.id)
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


@dp.message_handler(lambda m: m.text == "▶️ Запуск")
async def try_start_trading(msg: types.Message):
    session = sessions.get(msg.from_user.id)
    settings = trade_settings.get(msg.from_user.id)

    if not session:
        await msg.answer("❌ Счёт не подключён")
        return

    balance = 5000  # временно mock

    allowed, reason = risk_engine.can_trade(msg.from_user.id, balance)
    if not allowed:
        await msg.answer(f"⛔ Торговля запрещена: {reason}")
        return

    lot = risk_engine.calculate_lot(
        balance=balance,
        risk_percent=settings["risk"]
    )

    await msg.answer(
        f"▶️ Торговля разрешена\n"
        f"Лот рассчитан: {lot}\n"
        f"Риск: {settings['risk']}%"
    )


def start_bot():
    executor.start_polling(dp)

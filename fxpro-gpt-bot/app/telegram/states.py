from aiogram.dispatcher.filters.state import State, StatesGroup

class LoginState(StatesGroup):
    waiting_login = State()
    waiting_password = State()

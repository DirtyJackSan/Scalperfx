from aiogram.dispatcher.filters.state import State, StatesGroup

class TradeSettingsState(StatesGroup):
    waiting_pairs = State()
    waiting_leverage = State()
    waiting_risk = State()

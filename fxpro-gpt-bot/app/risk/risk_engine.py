from app.risk.risk_config import (
    MAX_DAILY_DD_PERCENT,
    MAX_TRADES_PER_DAY,
    DEFAULT_STOP_LOSS_PIPS
)

class RiskEngine:
    def __init__(self, risk_state):
        self.risk_state = risk_state

    def can_trade(self, tg_id, balance):
        self.risk_state.reset_if_new_day(tg_id)
        state = self.risk_state.get(tg_id)

        max_daily_loss = balance * (MAX_DAILY_DD_PERCENT / 100)

        if state["daily_loss"] >= max_daily_loss:
            return False, "Дневной лимит убытка достигнут"

        if state["trades_today"] >= MAX_TRADES_PER_DAY:
            return False, "Лимит сделок на день достигнут"

        return True, "OK"

    def calculate_lot(
        self,
        balance: float,
        risk_percent: float,
        stop_loss_pips: int = DEFAULT_STOP_LOSS_PIPS,
        pip_value: float = 10.0
    ):
        risk_amount = balance * (risk_percent / 100)
        lot = risk_amount / (stop_loss_pips * pip_value)
        return round(max(lot, 0.01), 2)

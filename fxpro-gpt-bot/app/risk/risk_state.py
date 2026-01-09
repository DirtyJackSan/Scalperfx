from datetime import date

class RiskState:
    def __init__(self):
        self.state = {}

    def init_user(self, tg_id):
        if tg_id not in self.state:
            self.state[tg_id] = {
                "date": date.today(),
                "trades_today": 0,
                "daily_loss": 0.0
            }

    def reset_if_new_day(self, tg_id):
        from datetime import date
        if self.state[tg_id]["date"] != date.today():
            self.state[tg_id] = {
                "date": date.today(),
                "trades_today": 0,
                "daily_loss": 0.0
            }

    def register_trade(self, tg_id):
        self.state[tg_id]["trades_today"] += 1

    def register_loss(self, tg_id, loss):
        self.state[tg_id]["daily_loss"] += loss

    def get(self, tg_id):
        return self.state[tg_id]

class TradeSettings:
    def __init__(self):
        self.settings = {}

    def init_user(self, tg_id):
        if tg_id not in self.settings:
            self.settings[tg_id] = {
                "pairs": [],
                "leverage": 100,
                "risk": 0.3,
                "mode": "off"
            }

    def set_pairs(self, tg_id, pairs: list):
        self.settings[tg_id]["pairs"] = pairs

    def set_leverage(self, tg_id, leverage: int):
        self.settings[tg_id]["leverage"] = leverage

    def set_risk(self, tg_id, risk: float):
        self.settings[tg_id]["risk"] = risk

    def set_mode(self, tg_id, mode: str):
        self.settings[tg_id]["mode"] = mode

    def get(self, tg_id):
        return self.settings.get(tg_id)

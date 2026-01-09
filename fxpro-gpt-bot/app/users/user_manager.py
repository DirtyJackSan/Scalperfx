class UserManager:
    def __init__(self):
        self.users = {}

    def create_user(self, tg_id):
        if tg_id not in self.users:
            self.users[tg_id] = {
                "mt5_login": None,
                "session_active": False
            }

    def set_login(self, tg_id, login):
        self.users[tg_id]["mt5_login"] = login

    def activate_session(self, tg_id):
        self.users[tg_id]["session_active"] = True

class SessionStore:
    def __init__(self):
        self.sessions = {}

    def create(self, tg_id, login):
        self.sessions[tg_id] = {
            "login": login,
            "connected": True
        }

    def get(self, tg_id):
        return self.sessions.get(tg_id)

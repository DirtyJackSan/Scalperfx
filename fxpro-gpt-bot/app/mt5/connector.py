def connect(login: str, password: str):
    if login and password:
        return {
            "balance": 5000,
            "currency": "USD"
        }
    return None

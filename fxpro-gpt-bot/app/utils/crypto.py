from cryptography.fernet import Fernet

KEY = Fernet.generate_key()
fernet = Fernet(KEY)

def encrypt(text: str) -> bytes:
    return fernet.encrypt(text.encode())

def decrypt(token: bytes) -> str:
    return fernet.decrypt(token).decode()

from argon2 import PasswordHasher
from cryptography.fernet import Fernet
from src.settings import get_settings

def hash_password(password: str):
    ph = PasswordHasher()
    return ph.hash(password)

def check_password(password: str, hash: str):
    ph = PasswordHasher()
    return ph.verify(hash, password)

def fernet_crypt_info(info: str):
    key = get_settings().fernet_secret_key
    fernet = Fernet(key)
    return fernet.encrypt(info.encode()).decode()


def fernet_decrypt_info(info: str):
    key = get_settings().fernet_secret_key
    fernet = Fernet(key)
    return fernet.decrypt(info.encode()).decode()
import os

from argon2 import PasswordHasher
from cryptography.fernet import Fernet
from dotenv import load_dotenv
from fastapi import HTTPException


def error_message(e) -> HTTPException:
    if isinstance(e, HTTPException):
        return e
    else:
        return HTTPException(500, str(e))


def hash_password(password: str):
    ph = PasswordHasher()
    return ph.hash(password)


def check_password(password: str, hash: str):
    ph = PasswordHasher()
    return ph.verify(hash, password)


def fernet_crypt_info(info: str):
    load_dotenv()
    key = os.getenv('fernet_secret_key')
    fernet = Fernet(key)
    return fernet.encrypt(info.encode()).decode()


def fernet_decrypt_info(info: str):
    load_dotenv()
    key = os.getenv('fernet_secret_key')
    fernet = Fernet(key)
    return fernet.decrypt(info.encode()).decode()

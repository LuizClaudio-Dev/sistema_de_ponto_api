import datetime
import hashlib
import secrets

from argon2 import PasswordHasher
from cryptography.fernet import Fernet
from fastapi import HTTPException
import jwt
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


def create_access_token(sub, claims=None, expires_minutes=None):
    settings = get_settings()
    now = datetime.datetime.now(datetime.timezone.utc)
    minutes = expires_minutes or settings.jwt_access_token_expire_minutes

    payload = {
        "sub": str(sub),
        "iat": now,
        "exp": now + datetime.timedelta(minutes=minutes),
    }

    if claims:
        payload.update(claims)

    return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


def decode_token(token):
    settings = get_settings()
    try:
        return jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail={"error": "Token expirado"}, headers={
                            "WWW-Authenticate": "Bearer error='token expirado'"})
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail={"error": "Token invalido"}, headers={
                            "WWW-Authenticate": "Bearer error='token invalido'"})


def generate_session_token():
    return secrets.token_urlsafe(32)


def hash_session_token(token):
    return hashlib.sha256(token.encode()).hexdigest()

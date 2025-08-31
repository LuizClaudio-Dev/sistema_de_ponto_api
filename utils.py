import json
import os
from datetime import datetime

from argon2 import PasswordHasher
from cryptography.fernet import Fernet
from dotenv import load_dotenv
from fastapi import HTTPException


def error_message(e) -> HTTPException:
    if isinstance(e, HTTPException):
        raise e
    else:
        raise HTTPException(500, str(e))


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


def model_dict_json_serializer(model: list[dict[str, any]] | dict[str, any]) -> list[dict[str, any]] | dict[str, any]:
    if isinstance(model, list):
        result = json.loads(json.dumps(
            model, default=lambda o: o.isoformat() if isinstance(o, datetime) else o))
        return result
    else:
        result = model
        for key, value in result.items():
            if isinstance(value, datetime):
                model[key] = value.isoformat()
        return result


def resposta_get_com_paginacao(titulo: str, resposta: dict[str, any], total: int, pagina: int, limite: int):
    total_paginas = (total + limite - 1) // limite

    resposta = {
        "data": {titulo: resposta},
        "pagination": {
            "total": total,
            "pagina": pagina,
            "limite": limite,
            "total_paginas": total_paginas,
        },
    }

    return resposta

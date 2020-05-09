import base64
import hashlib
import hmac
import os
from typing import Tuple

from flask_login import current_user
from werkzeug.utils import redirect


def login_required(fun):
    # Функция-обертка для проверки, вошел ли пользователь

    def wrapper():
        if not current_user or not current_user.is_authenticated:
            return redirect('/login')
        return fun()

    return wrapper


def check_password(salt: str, hashed_password: str, password: str) -> bool:
    # Проверка хеша на соответсвие паролю
    return is_correct_password(
        salt=convert_string_to_bytes(salt),
        pw_hash=convert_string_to_bytes(hashed_password),
        password=password
    )


def prepare_password(password: str) -> Tuple[str, str]:
    salt, password = map(convert_bytes_to_string, hash_password(password))
    return salt, password


def convert_bytes_to_string(bytes: bytes) -> str:
    return base64.b64encode(bytes)


def convert_string_to_bytes(string: str) -> bytes:
    return base64.b64decode(string)


def hash_password(password: str) -> Tuple[bytes, bytes]:
    """
    Hash the provided password with a randomly-generated salt and return the
    salt and hash to store in the database.
    """
    salt = os.urandom(16)
    pw_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
    return salt, pw_hash


def is_correct_password(salt: bytes, pw_hash: bytes, password: str) -> bool:
    """
    Given a previously-stored salt and hash, and a password provided by a user
    trying to log in, check whether the password is correct.
    """
    return hmac.compare_digest(
        pw_hash,
        hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
    )

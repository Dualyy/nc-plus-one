from argon2 import PasswordHasher
from argon2.exceptions import InvalidHashError, VerifyMismatchError

hasher = PasswordHasher()


def hash_password(password: str):
    return hasher.hash(password)


def verify_password(hash: str, password: str):
    try:
        return hasher.verify(hash, password)
    except (InvalidHashError, VerifyMismatchError):
        return False

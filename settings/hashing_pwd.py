import bcrypt

# simple password auth


def password_hasher(password: str) -> bytes:
    pwd = password.encode()
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(pwd, salt)
    return hashed


def check_password(password: str, hashed_password: bytes) -> bool:
    pwd = password.encode()
    return bcrypt.checkpw(pwd, hashed_password)

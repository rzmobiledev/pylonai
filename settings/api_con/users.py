import bcrypt
from sqlalchemy import String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from .connection import db


class User(db.Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(150), nullable=False)

    def json(self):
        return {"id": self.id, "username": self.username, "email": self.email}


class TokenBlockList(db.Model):
    __tablename__ = "tokenblocklist"
    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    jti: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )


class UserQuery(object):
    @staticmethod
    def get_user_id_by_email_or_name(email=None, username=None):
        return User.query.filter(
            (User.email == email) | (User.username == username)
        ).first()

    @staticmethod
    def is_user_exists(email: str = None, username: str = None) -> bool:
        user = UserQuery.get_user_id_by_email_or_name(
            email=email, username=username
        )
        return hasattr(user, "id")

    @staticmethod
    def is_password_correct(username: str = None, passwd: str = None) -> bool:

        user = UserQuery.get_user_id_by_email_or_name(username=username)
        hashed_password = user.password if user else None
        if not hashed_password:
            return False
        db_passwd = bytes(hashed_password, "utf-8")
        return check_password(passwd, db_passwd)

    @staticmethod
    def format_user_with_hashed_password(**kwargs) -> User | str:
        if not kwargs.get("username") and not kwargs.get("email"):
            hashed_password = password_hasher(kwargs.get("password"))
            return hashed_password.decode("utf-8")

        hashed_password = password_hasher(kwargs.get("password"))
        hashed_pass_to_str = hashed_password.decode("utf-8")
        user = User(
            username=kwargs.get("username"),
            email=kwargs.get("email"),
            password=hashed_pass_to_str,
        )
        return user


def password_hasher(password: str) -> bytes:
    pwd = password.encode()
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(pwd, salt)
    return hashed


def check_password(password: str, hashed_password: bytes) -> bool:
    pwd = password.encode()
    return bcrypt.checkpw(pwd, hashed_password)

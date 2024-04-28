import bcrypt
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(150), nullable=False)

    def json(self):
        return {"id": self.id, "username": self.username, "email": self.email}


class UserQuery(object):
    @staticmethod
    def get_user_id_by_email_or_name(email=None, username=None):
        return User.query.filter((User.email == email) | (User.username == username)).first()

    @staticmethod
    def is_user_exists(email: str = None, username: str = None) -> bool:
        user = UserQuery.get_user_id_by_email_or_name(email=email, username=username)
        return hasattr(user, 'id')

    @staticmethod
    def is_password_correct(username: str = None, passwd: str = None) -> bool:

        user = UserQuery.get_user_id_by_email_or_name(username=username)
        db_passwd = user.password if user else None
        db_passwd = bytes(db_passwd, 'utf-8')
        return check_password(passwd, db_passwd)


def password_hasher(password: str) -> bytes:
    pwd = password.encode()
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(pwd, salt)
    return hashed


def check_password(password: str, hashed_password: bytes) -> bool:
    pwd = password.encode()
    return bcrypt.checkpw(pwd, hashed_password)

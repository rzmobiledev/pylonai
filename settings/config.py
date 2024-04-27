
from flask import Flask
import os
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from settings.hashing_pwd import check_password

load_dotenv()

DEBUG = os.environ.get('DEBUG')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('PGDATABASE_URL')
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(150), unique=True, nullable=False)

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
    def is_password_correct(username: str, passwd: str) -> bool:

        user = UserQuery.get_user_id_by_email_or_name(username=username)
        db_passwd = user.password if user else None
        return check_password(passwd, db_passwd)

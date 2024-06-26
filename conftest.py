import pytest
from faker import Faker
from flask import jsonify, make_response
from settings.api_con.connection import db
from settings.config import create_app
from settings.api_con.users import User, password_hasher
import os
from dotenv import load_dotenv
import jwt

load_dotenv()

fake = Faker()
secret_key = os.environ.get("JWT_SECRET_KEY")
password = "p1l0n41b4ck3nd"


@pytest.fixture
def app():
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("PGDATABASE_TEST")
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    yield app.test_client()


@pytest.fixture
def random_user():
    return {
        "username": fake.name(),
        "email": fake.email(),
        "password": hashing_password(),
    }


@pytest.fixture
def pylon_user():
    return {
        "username": "pylon",
        "email": "pylon@example.com",
        "password": "pyl0n123",
    }


def hashing_password():
    hashed_password = password_hasher(password)
    return hashed_password.decode("utf-8")


@pytest.fixture(scope="session")
def runner(app):
    return app.test_cli_runner()


@pytest.fixture(scope="session")
def user():
    users = User.query.all()
    return make_response(
        jsonify({"users": [user.json() for user in users]}), 200
    )


@pytest.fixture
def get_token():
    encoded_jwt = jwt.encode(
        {"username": "pylon"}, secret_key, algorithm="HS256"
    )
    return encoded_jwt


@pytest.fixture
def employee_payload():
    return {
        "designation": "VIP Workers",
        "project": "pylonAI",
        "team": "backend",
        "supervisor": "supervison12",
        "joinDate": "2024-04-09",
        "resignDate": "2025-04-09",
    }

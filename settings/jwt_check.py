from flask import jsonify, make_response, request
from datetime import datetime, timedelta

from functools import wraps
import jwt
import os
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
from .api_con.users import User, UserQuery

load_dotenv()

DEBUG = os.environ.get("JWT_SECRET_KEY")


def check_header_content(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            token = request.headers.get("Authorization")
            token = token.split("Bearer ")[1]
        if not token:
            return make_response(
                jsonify({"message": "Token is missing !!"}), 401
            )
        try:
            # decoding the payload to fetch the stored details
            data = jwt.decode(
                token, os.environ.get("JWT_SECRET_KEY"), algorithms="SH256"
            )
            # current_user = UserQuery.get_user_id_by_email_or_name(username=data['username'])
            from logger.logger import log

            log(data)
        except Exception:
            return make_response(
                jsonify({"message": "Token is invalid !!"}), 401
            )

    return wrapper


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        # jwt is passed in the request header
        if "Authorization" in request.headers:
            token = request.headers.get("Authorization")
            token = token.split("Bearer ")[1]

        # return 401 if token is not passed
        if not token:
            return make_response(
                jsonify({"message": "Token is missing !!"}), 401
            )

        try:

            # decoding the payload to fetch the stored details
            data = jwt.decode(token, DEBUG, algorithms="HS256")
            current_user = UserQuery.get_user_id_by_email_or_name(
                username=data["username"]
            )

        except Exception:

            return make_response(
                jsonify({"message": "Token is invalid !!"}), 401
            )
        # returns the current logged in users context to the routes
        return f(current_user, *args, **kwargs)

    return decorated


def get_jwt_token(username: str) -> jwt:
    return jwt.encode(
        {"username": username, "exp": datetime.now() + timedelta(minutes=30)},
        DEBUG,
        algorithm="HS256",
    )

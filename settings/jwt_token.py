from flask import jsonify, make_response, request
from datetime import datetime, timedelta, timezone

from functools import wraps
import jwt
import os
from dotenv import load_dotenv
from .api_con.users import UserQuery

load_dotenv()

DEBUG = os.environ.get("JWT_SECRET_KEY")


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # jwt is passed in the request header
        if "Authorization" in request.headers:
            token = request.headers.get("Authorization")
            if "Bearer" in token:
                token = token.split("Bearer ")[1]

        if not token:
            return make_response(
                jsonify({"message": "Token is missing !!"}), 401
            )
        try:
            # decoding the payload to fetch the stored details
            payload = jwt.decode(token, DEBUG, algorithms="HS256")
            current_user = UserQuery.get_user_id_by_email_or_name(
                username=payload["username"]
            )
        except jwt.ExpiredSignatureError:
            return make_response(jsonify({"message": "Token is expired."}), 401)
        except Exception:
            return make_response(
                jsonify({"message": "Token is invalid !!"}), 401
            )
        # returns the current logged in users context to the routes
        return f(current_user, *args, **kwargs)

    return decorated


def get_jwt_token(username: str) -> jwt:
    """
    get token valid for 30 mins.
    kindly change to suit your needs.
    """
    return jwt.encode(
        {
            "username": username,
            "exp": datetime.now(tz=timezone.utc) + timedelta(minutes=30),
        },
        DEBUG,
        algorithm="HS256",
    )

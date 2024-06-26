from flask_restx import fields, Resource, Namespace
from flask import request, Request, jsonify, make_response
from sqlalchemy.exc import IntegrityError

from .connection import db
from .users import User, UserQuery

from settings.jwt_token import token_required, get_jwt_token

api = Namespace("user", description="USERS ENDPOINT")
headers = {"Content-Type": "application/json"}

# user field type in swagger
user_field_model = api.model(
    "User Fields",
    {
        "username": fields.String(description="Username", required=True),
        "email": fields.String(description="Your email address", required=True),
        "password": fields.String(
            description="Password", format="password", required=True
        ),
    },
)

user_login_field = api.model(
    "User Login Fields",
    {
        "username": fields.String(description="Username", required=True),
        "password": fields.String(
            description="Password", format="password", required=True
        ),
    },
)


# hide password input in swagger
class password(object):
    def __call__(self, value):
        return value

    @property
    def __schema__(self):
        return {
            "type": "string",
            "format": "password",
        }


parser = api.parser()
parser.add_argument(
    "password",
    type=password(),
    location="args",
    help="Password cannot be empty",
)


@api.route("/users")
class UserRoute(Resource):

    @api.response(500, "Internal error")
    @api.response(200, "User created")
    @api.header("content-type", "application/json")
    @api.doc(
        model=user_field_model,
        params={
            "username": "Username",
            "email": "Email",
            "password": "Password",
        },
    )
    @api.expect(parser)
    def post(self, *args, **kwargs):
        try:
            data = get_request_user_dict(request)
            new_user = UserQuery.format_user_with_hashed_password(**data)
            db.session.add(new_user)
            db.session.commit()
            return make_response(jsonify({"message": "user created"}), 201)
        except IntegrityError:
            return make_response(
                jsonify({"message": "Username or email is already exists."}),
                404,
            )
        except Exception as e:
            return make_response(jsonify({"message": str(e)}), 500)

    @api.response(500, "Internal error")
    @api.response(200, "Success")
    @api.header("content-type", "application/json")
    @token_required
    def get(self, *args, **kwargs):
        try:
            users = User.query.all()
            return make_response(
                jsonify({"users": [user.json() for user in users]}), 200
            )
        except Exception:
            return make_response(
                jsonify({"message": "Cannot retrieve user data."}), 500
            )


@api.route("/login")
class LoginRoute(Resource):

    @api.response(500, "Internal error")
    @api.response(200, "Success")
    @api.header("content-type", "application/json")
    @api.doc(
        model=user_login_field,
        params={"username": "Username", "password": "Password"},
    )
    @api.expect(parser)
    def post(self):
        try:
            data = get_request_user_dict(request)
            is_user_exists = UserQuery.is_user_exists(
                username=data.get("username"), email=data.get("email")
            )
            is_password_correct = UserQuery.is_password_correct(
                data.get("username"), data.get("password")
            )
            if is_user_exists and is_password_correct:
                token = get_jwt_token(data.get("username"))
                return make_response(jsonify({"token": token}), 201)
            return make_response(
                jsonify({"message": "You are not authorized"}), 404
            )
        except Exception as e:
            return make_response(jsonify({"message": str(e)}), 500)


@api.route("/users/<int:id>")
@api.doc(params={"id": "id"})
class UserDetailRoute(Resource):

    @token_required
    def get(self, *args, **kwargs):
        try:
            user_id = kwargs.get("id")
            user = User.query.filter_by(id=user_id).first()
            if user:
                return make_response(jsonify({"user": user.json()}), 200)
            return make_response(jsonify({"message": "user not found"}), 404)
        except Exception:
            return make_response(
                jsonify({"message": "error getting user"}), 500
            )

    @api.response(500, "Internal error")
    @api.response(200, "Success")
    @api.header("content-type", "application/json")
    @api.doc(
        model=user_field_model,
        params={
            "password": "Password",
        },
    )
    @api.expect(parser)
    @token_required
    def patch(self, *args, **kwargs):
        try:
            id_in_params = kwargs.get("id")
            current_login_user_id = self.id

            if current_login_user_id != id_in_params:
                return make_response(
                    jsonify(
                        message="You are not authorized to perform the action."
                    ),
                    401,
                )

            password = get_request_user_dict(request)
            user = User.query.filter_by(id=id_in_params).first()
            if user:
                hashed_password = UserQuery.format_user_with_hashed_password(
                    **password
                )
                user.password = hashed_password
                db.session.commit()
                return make_response(jsonify(message="user updated"), 200)
            return make_response(jsonify({"message": "user not found"}), 404)

        except Exception:
            return make_response(
                jsonify({"message": "error updating user"}), 500
            )

    @token_required
    def delete(self, *args, **kwargs):
        try:
            id_in_params = kwargs.get("id")
            current_login_user_id = self.id

            if current_login_user_id != id_in_params:
                return make_response(
                    jsonify(
                        message="You are not authorized to perform the action."
                    ),
                    401,
                )

            user = User.query.filter_by(id=id_in_params).first()
            if user:
                db.session.delete(user)
                db.session.commit()
                return make_response(jsonify({"message": "user deleted"}), 200)
            return make_response(jsonify({"message": "user not found"}), 404)
        except Exception:
            return make_response(
                jsonify({"message": "error deleting user"}), 500
            )


def get_request_user_dict(request: Request) -> dict:
    username = request.args.get("username")
    email = request.args.get("email")
    password = request.args.get("password")

    if username or password:  # using swagger
        payload = dict(username=username, email=email, password=password)

    else:  # using postman
        payload = request.get_json()
    return payload

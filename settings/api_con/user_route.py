from flask_restx import fields, Resource, Namespace
from flask import request, jsonify, make_response
from sqlalchemy.exc import IntegrityError

from .connection import db
from .users import User, UserQuery, password_hasher

from settings.jwt_check import token_required, get_jwt_token

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


@api.route("/protected")
class ProtectedRoute(Resource):
    @token_required
    def get(self):
        return make_response(
            jsonify(message="You are authorized to see this page"), 200
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
    def post(self):
        try:

            username = request.args.get("username")
            email = request.args.get("email")
            password = request.args.get("password")

            if username:  # using swagger
                data = dict(username=username, email=email, password=password)

            else:  # using postman
                data = request.get_json()

            hashed_password = password_hasher(data.get("password"))
            hashed_pass_to_str = hashed_password.decode("utf-8")
            new_user = User(
                username=data.get("username"),
                email=data.get("email"),
                password=hashed_pass_to_str,
            )
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
    def get(self):
        try:
            users = User.query.all()
            return make_response(
                jsonify({"users": [user.json() for user in users]}), 200
            )
        except Exception as e:
            return make_response(jsonify({"message": str(e)}), 500)


@api.route("/login")
class LoginRoute(Resource):

    @api.response(500, "Internal error")
    @api.response(200, "Success")
    @api.doc(
        model=user_login_field,
        params={"username": "Username", "password": "Password"},
    )
    @api.expect(parser)
    def post(self):
        try:
            username = request.args.get("username")
            password = request.args.get("password")

            if username:  # using swagger
                data = dict(username=username, password=password)

            else:  # using postman
                data = request.get_json()

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
@api.doc(params={"id": "User ID"})
class UserDetailRoute(Resource):

    def get(self, id):
        try:
            user = User.query.filter(id=id).first()
            if user:
                return make_response(jsonify({"user": user.json()}), 200)
            return make_response(jsonify({"message": "user not found"}), 404)
        except Exception:
            return make_response(
                jsonify({"message": "error getting user"}), 500
            )

    # update user
    def put(self, id):
        try:
            data = request.get_json()
            user = User.query.filter_by(id=id).first()
            if user:
                user.username = data["username"]
                user.email = data["email"]
                db.session.commit()
                return make_response(jsonify({"message": "user updated"}), 200)
            return make_response(jsonify({"message": "user not found"}), 404)
        except Exception:
            return make_response(
                jsonify({"message": "error updating user"}), 500
            )

    def delete(self, id):
        try:
            user = User.query.filter_by(id=id).first()
            if user:
                db.session.delete()
                db.session.commit()
                return make_response(jsonify({"message": "user deleted"}), 200)
            return make_response(jsonify({"message": "user not found"}), 404)
        except Exception:
            return make_response(
                jsonify({"message": "error deleting user"}), 500
            )

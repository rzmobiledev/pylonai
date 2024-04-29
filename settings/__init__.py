from flask_restx import Api, Namespace
from flask import Blueprint
from dotenv import load_dotenv
from .api_con import api1
from .api_con import api2

load_dotenv()

index_url = Namespace("", description="Home")

blueprint_index = Blueprint("index", __name__, url_prefix="/")
blueprint_user = Blueprint("users", __name__, url_prefix="/api/v1/users")
blueprint_employee = Blueprint("employees", __name__, url_prefix="/api/v1")


authorizations = {
    "Bearer": {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization",
    },
}

api = Api(
    blueprint_employee,
    version="1.0",
    title="API Documentation",
    description="PylonAI Manpowerlist API Docs.",
    security="Bearer Auth",
    authorizations=authorizations,
)

api.add_namespace(index_url)
api.add_namespace(api1)
api.add_namespace(api2)

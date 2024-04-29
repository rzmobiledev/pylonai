from flask_restx import Api
from flask import Blueprint
from dotenv import load_dotenv
load_dotenv()

from .api_con import api as ns  # noqa


blueprint_url = Blueprint("api", __name__, url_prefix="/")

authorizations = {
    "Bearer": {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization",
    },
}


api = Api(
    blueprint_url,
    version="1.0",
    title="API Documentation",
    description="PylonAI Manpowerlist API Docs.",
    security="Bearer Auth",
    authorizations=authorizations,
)

api.add_namespace(ns)

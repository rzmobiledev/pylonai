
from flask_restx import Api
from flask import Blueprint
from dotenv import load_dotenv
from .api_con.route import api as ns  # noqa

load_dotenv()


blueprint_url = Blueprint("api", __name__, url_prefix="/api")

authorizations = {
    "Basic": {
        "type": "basic",
        "flow": "password",
    },
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
    authorizations=authorizations,
)

api.add_namespace(ns)
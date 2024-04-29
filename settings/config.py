import os
from flask import Flask
from dotenv import load_dotenv
from settings import blueprint_url
from .api_con.connection import db

load_dotenv()


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("PGDATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
    app.config["DEBUG"] = os.environ.get("DEBUG")
    app.config["TESTING"] = False
    db.init_app(app)
    app.register_blueprint(blueprint_url)
    return app

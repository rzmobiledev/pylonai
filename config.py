from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api
from flask import Flask, Blueprint
import os
from dotenv import load_dotenv

load_dotenv()

DEBUG = os.environ.get('DEBUG')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('PGDATABASE_URL')
db = SQLAlchemy(app)

blueprint = Blueprint('api', __name__, url_prefix='/api')

app.register_blueprint(blueprint)
api = Api(app, version='1.0', title='API Documentation',
          description='PylonAI Manpowerlist API Docs.',
          )


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

    def json(self):
        return {"id": self.id, "username": self.username, "email": self.email}



from flask import Flask
import os
from dotenv import load_dotenv


load_dotenv()

DEBUG = os.environ.get('DEBUG')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('PGDATABASE_URL')

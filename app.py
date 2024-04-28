
from settings.api_con.connection import db
import os
from flask_cors import CORS
from dotenv import load_dotenv
from settings.config import create_app

load_dotenv()


CORS(create_app(), resources={r'/*': {'origins': '*'}})

# Create user database
with create_app().app_context():
    db.create_all(bind_key=None)


if __name__ == "__main__":
    create_app().run(debug=os.environ.get('DEBUG'))

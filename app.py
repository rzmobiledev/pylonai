import os
from dotenv import load_dotenv
from settings.config import app
from settings import route

load_dotenv()

# Create user database
with app.app_context():
    route.db.create_all(bind_key=None)


# Register endpoint url as blueprint
app.register_blueprint(route.endpoint_url)


if __name__ == "__main__":
    app.run(debug=os.environ.get('DEBUG'))

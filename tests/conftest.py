import pytest
from settings.config import app


@pytest.fixture()
def app():
    app = app.create_app()

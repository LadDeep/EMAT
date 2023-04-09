from mongomock import MongoClient
import pytest
from app import create_app
from database.database import db

@pytest.fixture(scope="module")
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            yield client
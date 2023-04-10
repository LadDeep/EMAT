from flask_jwt_extended import create_access_token
from mongomock import MongoClient
import pytest
from app import create_app
from test_expensesCalculate import Calculator
from modules.models import Group
from modules.models.User import User

@pytest.fixture(scope="module")
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config["DEBUG"] = False
    # with app.test_client() as client:
    #     yield client
    yield app

@pytest.fixture(scope="module")
def test_client(app):
    with app.test_client() as client:
        yield client

@pytest.fixture
def calculator():
    return Calculator()

@pytest.fixture(scope="module")
def user():
    email = "test_user1@example.com"
    password = "TestPassword"
    first_name = "Test"
    last_name = "User"
    currency = "USD"
    monthly_budget_amount = 100
    warning_budget_amount = 90
    verificationToken = "123456"

    # Create a test user in the database
    user = User(
        email=email,
        first_name=first_name,
        last_name=last_name,
        currency=currency,
        monthly_budget_amount=monthly_budget_amount,
        warning_budget_amount=warning_budget_amount,
        verificationToken = verificationToken
    )
    user.hash_password(password)
    user.save()
    yield user
    user.delete()

@pytest.fixture(scope="module")
def group():
    id= 1,
    name = "XYZ",
    desciption = "desciption",
    baseCurrency = "CAD"
    participants = ["new_user2@example.com", "new_user@example.com", "test_user1@example.com"]

    group = Group()
    group.save()
    yield group
    group.delete()

@pytest.fixture(scope="module")
def token(app):
    with app.app_context():
        token = create_access_token("test")
        yield token
        
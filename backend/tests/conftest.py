from mongomock import MongoClient
import pytest
from app import create_app
from modules.models.User import User

@pytest.fixture(scope="module")
def test_client():
    app = create_app()
    app.config['TESTING'] = True
    app.config["DEBUG"] = False
    with app.test_client() as client:
        yield client

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
import pytest
from unittest import mock
from datetime import datetime
from main import get_user_data, requests
from unittest.mock import patch, Mock

@pytest.fixture(scope="module")
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture(scope="module")
def user():
    user = User(
        email="test@test.com",
        password="password",
        first_name="Eren",
        last_name="Yeager",
        currency="USD",
        monthly_budget_amount=1000,
        warning_budget_amount=800
    )
    user.save()
    return user

def test_register_endpoint(client, user):
    # Test with valid input
    response = client.post('/register', json={
        "email": "test2@test.com",
        "password": "password",
        "first_name": "Eren",
        "last_name": "Yeager",
        "currency": "USD",
        "monthly_budget_amount": 1000,
        "warning_budget_amount": 800
    })
    assert response.status_code == 200
    assert response.json == {
        "status": True,
        "message": "signup successfully"
    }

    # Test with an email that already exists
    response = client.post('/register', json={
        "email": "test@test.com",
        "password": "password",
        "first_name": "Eren",
        "last_name": "Yeager",
        "currency": "USD",
        "monthly_budget_amount": 1000,
        "warning_budget_amount": 800
    })
    assert response.status_code == 409
    assert response.json == {
        "status": False,
        "error": "User with the email has already existed"
    }

def test_login_endpoint(client, user):
    # Test with valid input and verified user
    user.isEmailVerified = True
    user.hash_password("password")
    user.save()
    return user
import pytest
from datetime import datetime
from mongomock import MongoClient
from main import app, User


@pytest.fixture(scope="module")
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture(scope="module")
def user():
    client = MongoClient()
    db = client['test_db']
    user_collection = db['users']
    user = User(
        email="test@test.com",
        password="password",
        first_name="Eren",
        last_name="Yeager",
        currency="USD",
        monthly_budget_amount=1000,
        warning_budget_amount=800
    )
    user_collection.insert_one(user.to_dict())
    return user


def test_register_endpoint(client, user):
    # Test with valid input
    response = client.post('/auth/register', json={
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
    response = client.post('/auth/register', json={
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
    client = MongoClient()
    db = client['test_db']
    user_collection = db['users']
    user_collection.update_one({"email": user.email}, {"$set": user.to_dict()})
    response = client.post('/auth/login', json={
        "email": "test@test.com",
        "password": "password"
    })
    assert response.status_code == 200
    assert response.json == {
        "status": True,
        "message": "login successfully"
    }

def test_register_endpoint_invalid_email(client):
    # Test with an invalid email format
    response = client.post('/auth/register', json={
        "email": "testtest.com",
        "password": "password",
        "first_name": "Eren",
        "last_name": "Yeager",
        "currency": "USD",
        "monthly_budget_amount": 1000,
        "warning_budget_amount": 800
    })
    assert response.status_code == 400
    assert response.json == {
        "status": False,
        "error": "Invalid email format"
    }

def test_register_endpoint_invalid_password(client):
    # Test with a password less than 8 characters
    response = client.post('/auth/register', json={
        "email": "test3@test.com",
        "password": "pass",
        "first_name": "Eren",
        "last_name": "Yeager",
        "currency": "USD",
        "monthly_budget_amount": 1000,
        "warning_budget_amount": 800
    })
    assert response.status_code == 400
    assert response.json == {
        "status": False,
        "error": "Password must be at least 8 characters long"
    }

def test_register_endpoint_invalid_currency(client):
    # Test with an invalid currency code
    response = client.post('/auth/register', json={
        "email": "test4@test.com",
        "password": "password",
        "first_name": "Eren",
        "last_name": "Yeager",
        "currency": "ABC",
        "monthly_budget_amount": 1000,
        "warning_budget_amount": 800
    })
    assert response.status_code == 400
    assert response.json == {
        "status": False,
        "error": "Invalid currency code"
    }

def test_login_endpoint_incorrect_password(client, user):
    # Test with incorrect password
    user.isEmailVerified = True
    user.hash_password("password")
    user.save()
    response = client.post('/auth/login', json={
        "email": "test@test.com",
        "password": "wrongpassword"
    })
    assert response.status_code == 401
    assert response.json == {
        "status": False,
        "error": "Invalid email or password"
    }

def test_login_endpoint_unverified_email(client, user):
    # Test with unverified email
    user.isEmailVerified = False
    user.hash_password("password")
    user.save()
    response = client.post('/auth/login', json={
        "email": "test@test.com",
        "password": "password"
    })
    assert response.status_code == 401
    assert response.json == {
        "status": False,
        "error": "Email not verified"
    }

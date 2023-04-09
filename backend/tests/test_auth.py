import json
from unittest import mock
import json
from unittest import mock
import pytest
from modules.models.User import User
from app import app


@pytest.fixture(scope="module")
def test_client():
    app.config["TESTING"] = True
    app.config["DEBUG"] = False
def test_client():
    app.config["TESTING"] = True
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

    # Create a test user in the database
    email = "test_user1@example.com"
    password = "TestPassword"
    first_name = "Test"
    last_name = "User"
    currency = "USD"
    monthly_budget_amount = 100
    warning_budget_amount = 90

    # Create a test user in the database
    user = User(
        email=email,
        first_name=first_name,
        last_name=last_name,
        currency=currency,
        monthly_budget_amount=monthly_budget_amount,
        warning_budget_amount=warning_budget_amount,
        email=email,
        first_name=first_name,
        last_name=last_name,
        currency=currency,
        monthly_budget_amount=monthly_budget_amount,
        warning_budget_amount=warning_budget_amount,
    )
    user.hash_password(password)
    user.save()
    yield user
    user.delete()


def test_register(test_client, user):
    # Test registration of a new user
    data = {
        "email": "new_user@example.com",
        "password": "TestPassword123",
        "first_name": "New",
        "last_name": "User",
        "currency": "USD",
        "monthly_budget_amount": 100,
        "warning_budget_amount": 90,
    }
    response = test_client.post("/auth/register", json=data)
    assert response.status_code == 200
    assert "user_id" in response.json

    # Test registration with an already registered email
    data = {
        "email": user.email,
        "password": "TestPassword123",
        "first_name": "Test",
        "last_name": "User",
        "currency": "USD",
        "monthly_budget_amount": 100,
        "warning_budget_amount": 90,
    }
    response = test_client.post("/auth/register", json=data)
    assert response.status_code == 409
    assert response.json["error"] == "User with the email has already existed"


def test_login(test_client, user):
    # Test successful login
    data = {"email": user.email, "password": "TestPassword"}
    response = test_client.post("/auth/login", json=data)
    assert response.status_code == 200
    assert "access_token" in response.json

    # Test login with incorrect password
    data = {"email": user.email, "password": "WrongPassword"}
    response = test_client.post("/login", json=data)
    assert response.status_code == 200
    assert response.json["status"] is False
    assert response.json["message"] == "wrong password"

    # Test login with non-existent email
    data = {"email": "nonexistent@example.com", "password": "TestPassword"}
    response = test_client.post("/login", json=data)
    assert response.status_code == 404
    assert response.json["error"] == "User with the email not found"


def test_logout(test_client, user):
    # Test logout with a logged-in user
    with test_client.session_transaction() as session:
        session["user_id"] = str(user.user_id)
    response = test_client.post("/logout")
    assert response.status_code == 200
    assert response.json["status"] is True

def test_register_user(client):
    user_data = {
        "email": "test@example.com",
        "password": "password123",
        "first_name": "Eren",
        "last_name": "Yeager",
        "currency": "USD",
        "monthly_budget_amount": 1000,
        "warning_budget_amount": 500
    }
    with mock.patch("modules.utils.utilFunctions.sendEmail") as send_email_mock:
        send_email_mock.return_value = None
        response = client.post("/auth/register", json=user_data)
        assert response.status_code == 200
        assert "user_id" in response.json


def test_register_existing_user(client):
    user_data = {
        "email": "test@example.com",
        "password": "password123",
        "first_name": "Eren",
        "last_name": "Yeager",
        "currency": "USD",
        "monthly_budget_amount": 1000,
        "warning_budget_amount": 500
    }
    user = User(email=user_data["email"])
    user.save()

    with mock.patch("modules.utils.utilFunctions.sendEmail") as send_email_mock:
        send_email_mock.return_value = None
        response = client.post("/auth/register", json=user_data)
        assert response.status_code == 409
        assert response.json["status"] is False


def test_register_invalid_data(client):
    user_data = {
        "email": "invalid_email",
        "password": "password123",
        "first_name": "Eren",
        "last_name": "Yeager",
        "currency": "USD",
        "monthly_budget_amount": 1000,
        "warning_budget_amount": 500
    }
    with mock.patch("modules.utils.utilFunctions.sendEmail") as send_email_mock:
        send_email_mock.return_value = None
        response = client.post("/auth/register", json=user_data)
        assert response.status_code == 400
        assert response.json["status"] is False


def test_login_valid_user(client):
    email = "test@example.com"
    password = "password123"
    user = User(email=email)
    user.hash_password(password)
    user.save()

    login_data = {
        "email": email,
        "password": password
    }

    with mock.patch("flask_jwt_extended.create_access_token") as create_token_mock:
        create_token_mock.return_value = "test_access_token"
        response = client.post("/auth/login", json=login_data)
        assert response.status_code == 200
        assert response.json["status"] is True
        assert "access_token" in response.json
        assert "user_id" in response.json


def test_login_invalid_user(client):
    email = "test@example.com"
    password = "password123"

    login_data = {
        "email": email,
        "password": password
    }

    with mock.patch("flask_jwt_extended.create_access_token") as create_token_mock:
        create_token_mock.return_value = "test_access_token"
        response = client.post("/auth/login", json=login_data)
        assert response.status_code == 404
        assert response.json["status"] is False
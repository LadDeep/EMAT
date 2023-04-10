import json
from unittest import mock
import pytest
from modules.models.User import User

# @pytest.fixture(scope="module")
# def test_client():
#     app.config["TESTING"] = True
#     app.config["DEBUG"] = False
#     with app.test_client() as client:
#         yield client


# @pytest.fixture(scope="module")
# def user():
#     email = "test_user1@example.com"
#     password = "TestPassword"
#     first_name = "Test"
#     last_name = "User"
#     currency = "USD"
#     monthly_budget_amount = 100
#     warning_budget_amount = 90

#     # Create a test user in the database
#     user = User(
#         email=email,
#         first_name=first_name,
#         last_name=last_name,
#         currency=currency,
#         monthly_budget_amount=monthly_budget_amount,
#         warning_budget_amount=warning_budget_amount,
#     )
#     user.hash_password(password)
#     user.save()
#     yield user
#     user.delete()


def test_register(test_client, user):
    # Test registration of a new user
    data = {
        "email": "new_user3@example.com",
        "password": "TestPassword123",
        "first_name": "New",
        "last_name": "User",
        "currency": "USD",
        "monthly_budget_amount": 100,
        "warning_budget_amount": 90,
        "verificationToken": "123456"
    }
    response = test_client.post("/auth/register", json=data)
    assert response.status_code == 200
    assert "user_id" in response.json
    print("user register : test successfully")

    # Test registration with an already registered email
    data = {
        "email": user.email,
        "password": "TestPassword123",
        "first_name": "Test",
        "last_name": "User",
        "currency": "USD",
        "monthly_budget_amount": 100,
        "warning_budget_amount": 90,
        "verificationToken": "123456"
    }
    response = test_client.post("/auth/register", json=data)
    assert response.status_code == 409
    assert response.json["error"] == "User with the email has already existed"
    print("user register fail with existing email: test successfully")


def test_login(test_client, user):
    # Test successful login
    data = {"email": user.email, "password": "TestPassword"}
    response = test_client.post("/auth/login", json=data)
    assert response.status_code == 200
    print("user register: test successfully")

    # Test login with incorrect password
    data = {"email": user.email, "password": "WrongPassword"}
    response = test_client.post("/auth/login", json=data)
    assert response.status_code == 200
    assert response.json["status"] is False
    assert response.json["message"] == "wrong password"
    print("user register fail wrong password: test successfully")

    # Test login with non-existent email
    data = {"email": "nonexistent@example.com", "password": "TestPassword"}
    response = test_client.post("/auth/login", json=data)
    assert response.status_code == 404
    assert response.json["error"] == "User with the email not found"
    print("user register fail with non email: test successfully")


def test_logout(test_client, user):
    # Test logout with a logged-in user
    with test_client.session_transaction() as session:
        session["user_id"] = str(user.user_id)
    response = test_client.post("/auth/logout")
    assert response.status_code == 200
    assert response.json["status"] is True
    print("user logout : test successfully")

def test_register_user(test_client):
    user_data = {
        "email": "test3@example.com",
        "password": "password123",
        "first_name": "Eren",
        "last_name": "Yeager",
        "currency": "USD",
        "monthly_budget_amount": 1000,
        "warning_budget_amount": 500,
        "verificationToken": "123456"
    }
    with mock.patch("modules.utils.utilFunctions.sendEmail") as send_email_mock:
        send_email_mock.return_value = None
        response = test_client.post("/auth/register", json=user_data)
        assert response.status_code == 200
        assert "user_id" in response.json
        print("user register with email: test successfully")

def test_register_existing_user(test_client):
    user_data = {
        "email": "test_user1@example.com",
        "password": "TestPassword",
        "first_name": "Test",
        "last_name": "User",
        "currency": "USD",
        "monthly_budget_amount": 100,
        "warning_budget_amount": 90,
        "verificationToken": "123456"
    }

    with mock.patch("modules.utils.utilFunctions.sendEmail") as send_email_mock:
        send_email_mock.return_value = None
        response = test_client.post("/auth/register", json=user_data)
        assert response.status_code == 409
        assert response.json["status"] is False
        print("user register fail with existing user: test successfully")


def test_register_missing_data(test_client):
    user_data = {
        "first_name": "Eren",
        "last_name": "Yeager",
        "currency": "USD",
        "monthly_budget_amount": 1000,
        "warning_budget_amount": 500,
        "verificationToken": "123456"
    }
    with mock.patch("modules.utils.utilFunctions.sendEmail") as send_email_mock:
        send_email_mock.return_value = None
        response = test_client.post("/auth/register", json=user_data)
        assert response.status_code == 500
        assert response.json["status"] is False
        print("user register fail with missing data: test successfully")

def test_register_invalid_data(test_client):
    user_data = {
        "email": 1500,
        "password": "password123",
        "first_name": "Eren",
        "last_name": "Yeager",
        "currency": "USD",
        "monthly_budget_amount": 1000,
        "warning_budget_amount": 500,
        "verificationToken": "123456"
    }
    with mock.patch("modules.utils.utilFunctions.sendEmail") as send_email_mock:
        send_email_mock.return_value = None
        response = test_client.post("/auth/register", json=user_data)
        assert response.status_code == 500
        assert response.json["status"] is False
        print("user register fail with invalid data: test successfully")


def test_login_valid_user(test_client):
    email = "test_user1@example.com"
    password = "TestPassword"
    # user = User(email=email)
    # user.save()

    login_data = {
        "email": email,
        "password": password
    }

    with mock.patch("flask_jwt_extended.create_access_token") as create_token_mock:
        create_token_mock.return_value = "test_access_token"
        response = test_client.post("/auth/login", json=login_data)
        assert response.status_code == 200
        assert response.json["status"] is True
        assert "user_id" in response.json
        print("user login with valid data: test successfully")

def test_login_invalid_user(test_client):
    email = 1000
    password = "password123"

    login_data = {
        "email": email,
        "password": password
    }

    with mock.patch("flask_jwt_extended.create_access_token") as create_token_mock:
        create_token_mock.return_value = "test_access_token"
        response = test_client.post("/auth/login", json=login_data)
        assert response.status_code == 404
        assert response.json["status"] is False
        print("user login with invalid data: test successfully")
import app
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


# Test the registration endpoint
@mock.patch("modules.utils.utilFunctions.sendEmail")
def test_register_endpoint(mock_sendEmail, client):
    # Test with valid input
    response = client.post('/register', json={
        "email": "test@test.com",
        "password": "password",
        "first_name": "John",
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
    mock_sendEmail.assert_called_once()

    # Test with an email that already exists
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


# Test the login endpoint
def test_login_endpoint(client):
    # Test with valid input and verified user
    user = User(
        email="test@test.com",
        password="password",
        first_name="Eren",
        last_name="Yeager",
        currency="USD",
        monthly_budget_amount=1000,
        warning_budget_amount=800,
        isEmailVerified=True
    )
    user.hash_password("password")
    user.save()
    response = client.post('/login', json={
        "email": "test@test.com",
        "password": "password"
    })
    assert response.status_code == 200
    assert response.json == {
        "status": True,
        "user_id": str(user.user_id),
        "message": "login successfully",
        "access_token": response.json['access_token']
    }

    # Test with valid input and unverified user
    user = User(
        email="test@test.com",
        password="password",
        first_name="Eren",
        last_name="Yeager",
        currency="USD",
        monthly_budget_amount=1000,
        warning_budget_amount=800,
        isEmailVerified=False
    )
    user.hash_password("password")
    user.save()
    response = client.post('/login', json={
        "email": "test@test.com",
        "password": "password"
    })
    assert response.status_code == 200
    assert response.json == {
        "status": True,
        "user_id": str(user.user_id),
        "message": "User is not Verified"
    }

@patch.object(requests, 'get')
def test_get_user_data(mock_get):
    # Mock response from the API
    mock_response = Mock()
    mock_response.json.return_value = {
        'name': 'Eren Smith',
        'age': 30,
        'email': 'Eren.smith@example.com'
    }
    mock_get.return_value = mock_response
    
    # Test case 1: Valid user ID
    result = get_user_data(123)
    assert result == {
        'name': 'Eren Smith',
        'age': 30,
        'email': 'Eren.smith@example.com'
    }
    
    # Test case 2: Invalid user ID
    mock_response.status_code = 404
    result = get_user_data(456)
    assert result == None
    
    # Test case 3: Network error
    mock_get.side_effect = Exception('Network error')
    result = get_user_data(789)
    assert result == None

   

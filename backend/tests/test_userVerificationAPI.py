import pytest
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_register_json_valid(client):
    data = {'email': 'test@example.com', 'first_name': 'Eren', 'last_name': 'Yeager'}
    headers = {'Content-Type': 'application/json'}
    response = client.post('/register', json=data, headers=headers)
    assert response.status_code == 200
    print("'email': 'test@example.com', 'first_name': 'Eren', 'last_name': 'Yeager': Registration failed")

def test_register_json_missing_fields(client):
    data = {'email': 'test@example.com', 'last_name': 'Yeager'}
    headers = {'Content-Type': 'application/json'}
    response = client.post('/register', json=data, headers=headers)
    assert response.status_code == 400
    print("'error': 'Missing required fields: first_name'")

def test_register_form_valid(client):
    data = {'email': 'test@example.com', 'first_name': 'Eren', 'last_name': 'Yeager'}
    response = client.post('/register', data=data)
    assert response.status_code == 200
    print("Form validated. User registered successfully.")

def test_register_form_missing_fields(client):
    data = {'email': 'test@example.com', 'last_name': 'Yeager'}
    response = client.post('/register', data=data)
    assert response.status_code == 400
    print("'error': 'Missing required fields: first_name'")

def test_register_content_type_not_supported(client):
    data = {'email': 'test@example.com', 'first_name': 'Eren', 'last_name': 'Yeager'}
    headers = {'Content-Type': 'application/xml'}
    response = client.post('/register', data=data, headers=headers)
    assert response.status_code == 400
    print("'error': 'Content-Type application/xml not supported'")

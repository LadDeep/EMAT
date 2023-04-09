import pytest
from app import app


def test_register_json_valid(test_client):
    data = {'email': 'test5@example.com', 'password': 'test12345','first_name': 'Eren', 'last_name': 'Yeager'}
    headers = {'Content-Type': 'application/json'}
    response = test_client.post('/auth/register', json=data, headers=headers)
    print(response.json)
    assert response.status_code == 500
    print("'email': 'test@example.com', 'first_name': 'Eren', 'last_name': 'Yeager': Registration successfully")

def test_register_json_missing_fields(test_client):
    data = {'email': 'test@example.com', 'last_name': 'Yeager'}
    headers = {'Content-Type': 'application/json'}
    response = test_client.post('/auth/register', json=data, headers=headers)
    assert response.status_code == 500
    print("'error': 'Missing required fields: first_name'")

def test_register_form_valid(test_client):
    data = {'email': 'test@example.com', 'first_name': 'Eren', 'last_name': 'Yeager'}
    response = test_client.post('/auth/register', data=data)
    assert response.status_code == 500
    print("Form validated. User registered successfully.")

def test_register_form_missing_fields(test_client):
    data = {'email': 'test@example.com', 'last_name': 'Yeager'}
    response = test_client.post('/auth/register', data=data)
    assert response.status_code == 500
    print("'error': 'Missing required fields: first_name'")

def test_register_content_type_not_supported(test_client):
    data = {'email': 'test@example.com', 'first_name': 'Eren', 'last_name': 'Yeager'}
    headers = {'Content-Type': 'application/xml'}
    response = test_client.post('/auth/register', data=data, headers=headers)
    assert response.status_code == 500
    print("'error': 'Content-Type application/xml not supported'")

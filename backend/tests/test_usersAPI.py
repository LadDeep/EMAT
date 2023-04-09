import pytest
import json
from modules.models.User import User

def test_register_with_json_data(client):
    headers = {'Content-Type': 'application/json'}
    data = {'email': 'test@example.com', 'first_name': 'John', 'last_name': 'Doe'}
    response = client.post('/register', headers=headers, json=data)
    assert response.status_code == 200
    assert response.content_type == 'application/json'
    assert response.json == {'status': True}

def test_register_with_form_data(client):
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    data = {'email': 'test@example.com', 'first_name': 'John', 'last_name': 'Doe'}
    response = client.post('/register', headers=headers, data=data)
    assert response.status_code == 200
    assert response.content_type == 'application/json'
    assert response.json == {'status': True}

def test_register_with_invalid_content_type(client):
    headers = {'Content-Type': 'text/plain'}
    response = client.post('/register', headers=headers)
    assert response.status_code == 400
    assert response.content_type == 'application/json'
    assert response.json == {'error': 'Content-Type text/plain not supported'}

def test_register_with_missing_fields(client):
    headers = {'Content-Type': 'application/json'}
    data = {'email': 'test@example.com'}
    response = client.post('/register', headers=headers, json=data)
    assert response.status_code == 400
    assert response.content_type == 'application/json'
    assert response.json == {'error': 'Missing required fields: first_name, last_name'}

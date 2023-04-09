import pytest
from app import app


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_register_json_valid(client):
    data = {'email': 'test@example.com',
            'first_name': 'Eren', 'last_name': 'Yeager'}
    headers = {'Content-Type': 'application/json'}
    response = client.post('/register', json=data, headers=headers)
    assert response.status_code == 200
    assert response.json == {'status': True, 'object': {
        'email': 'test@example.com', 'first_name': 'Eren', 'last_name': 'Yeager'}}


def test_register_json_missing_fields(client):
    data = {'email': 'test@example.com', 'last_name': 'Yeager'}
    headers = {'Content-Type': 'application/json'}
    response = client.post('/register', json=data, headers=headers)
    assert response.status_code == 400
    assert response.json == {'status': False,
                             'error': 'Missing required fields: first_name'}


def test_register_form_valid(client):
    data = {'email': 'test@example.com',
            'first_name': 'Eren', 'last_name': 'Yeager'}
    response = client.post('/register', data=data)
    assert response.status_code == 200
    assert response.json == {'status': True, 'object': {
        'email': 'test@example.com', 'first_name': 'Eren', 'last_name': 'Yeager'}}


def test_register_form_missing_fields(client):
    data = {'email': 'test@example.com', 'last_name': 'Yeager'}
    response = client.post('/register', data=data)
    assert response.status_code == 400
    assert response.json == {'status': False,
                             'error': 'Missing required fields: first_name'}


def test_register_content_type_not_supported(client):
    data = {'email': 'test@example.com',
            'first_name': 'Eren', 'last_name': 'Yeager'}
    headers = {'Content-Type': 'application/xml'}
    response = client.post('/register', data=data, headers=headers)
    assert response.status_code == 400
    assert response.json == {
        'status': False, 'error': 'Content-Type application/xml not supported'}


def test_register_json_missing_fields():
    with app.test_client() as client:
        headers = {"Content-Type": "application/json"}
        data = {"email": "test@example.com"}
        response = client.post("/register", headers=headers, json=data)
        assert response.status_code == 400
        assert "status" in response.json
        assert response.json["status"] == False
        assert "message" in response.json
        assert "first_name" in response.json["message"]
        assert "last_name" in response.json["message"]


def test_register_json_valid_data():
    with app.test_client() as client:
        headers = {"Content-Type": "application/json"}
        data = {"email": "test@example.com",
                "first_name": "John", "last_name": "Doe"}
        response = client.post("/register", headers=headers, json=data)
        assert response.status_code == 200
        assert "status" in response.json
        assert response.json["status"] == True


def test_register_form_missing_fields():
    with app.test_client() as client:
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = {"email": "test@example.com"}
        response = client.post("/register", headers=headers, data=data)
        assert response.status_code == 400
        assert "status" in response.json
        assert response.json["status"] == False
        assert "message" in response.json
        assert "first_name" in response.json["message"]
        assert "last_name" in response.json["message"]


def test_register_form_valid_data():
    with app.test_client() as client:
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = {"email": "test@example.com",
                "first_name": "John", "last_name": "Doe"}
        response = client.post("/register", headers=headers, data=data)
        assert response.status_code == 200
        assert "status" in response.json
        assert response.json["status"] == True


def test_register_invalid_content_type():
    with app.test_client() as client:
        headers = {"Content-Type": "text/plain"}
        response = client.post("/register", headers=headers)
        assert response.status_code == 400
        assert "status" in response.json
        assert response.json["status"] == False
        assert "error" in response.json

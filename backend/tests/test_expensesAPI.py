import pytest
import json
from app import app


# @pytest.fixture
# def client():
#     with app.test_client() as client:
#         yield client


def test_detail_expense(client):
    # Test valid request
    response = client.get('/expense/detail?expense_id=123&group_id=456',
                          headers={'Authorization': 'Bearer token'})
    assert response.status_code == 200
    assert response.content_type == 'application/json'
    print("Validating request.....")

    # Test missing expense_id
    response = client.get('/expense/detail?group_id=456',
                          headers={'Authorization': 'Bearer token'})
    assert response.status_code == 400
    assert response.content_type == 'application/json'
    print("Error:Expense ID cannot be null in the request params.")

    # Test missing group_id
    response = client.get('/expense/detail?expense_id=123',
                          headers={'Authorization': 'Bearer token'})
    assert response.status_code == 400
    assert response.content_type == 'application/json'
    print("Error:Group ID cannot be null in the request params")

    # Test invalid JWT token
    response = client.get('/expense/detail?expense_id=123&group_id=456',
                          headers={'Authorization': 'Bearer invalid'})
    assert response.status_code == 401
    assert response.content_type == 'application/json'
    print("Message:Invalid token")

    # Test server error
    with app.app_context():
        app.testing = False
        response = client.get('/expense/detail?expense_id=123&group_id=456',
                              headers={'Authorization': 'Bearer token'})
        assert response.status_code == 500
        assert response.content_type == 'application/json'
        print("Exception occurred")


def test_create_expense(client):
    # Test valid request
    data = {"group_id": 123, "amount": 100, "date": "2023-04-09T00:00:00.000Z"}
    response = client.post('/expense/create', headers={
                           'Authorization': 'Bearer token', 'Content-Type': 'application/json'}, json=data)
    assert response.status_code == 201
    assert response.content_type == 'application/json'
    print("Expense 12345 Created")

    # Test missing group_id
    data = {"amount": 100, "date": "2023-04-09T00:00:00.000Z"}
    response = client.post('/expense/create', headers={
                           'Authorization': 'Bearer token', 'Content-Type': 'application/json'}, json=data)
    assert response.status_code == 400
    assert response.content_type == 'application/json'
    print("Fields: group_id not in request")

    # Test missing amount
    data = {"group_id": 123, "date": "2023-04-09T00:00:00.000Z"}
    response = client.post('/expense/create', headers={
                           'Authorization': 'Bearer token', 'Content-Type': 'application/json'}, json=data)
    assert response.status_code == 400
    assert response.content_type == 'application/json'
    print("Expense missing amount.")


def test_edit_expense(client):
    # Test valid request
    data = {"expense_id": 12345, "group_id": 123,
            "amount": 100, "date": "2023-04-09T00:00:00.000Z"}
    response = client.put('/expense/edit', headers={
                          'Authorization': 'Bearer token', 'Content-Type': 'application/json'}, json=data)
    assert response.status_code == 200
    assert response.content_type == 'application/json'
    print("status: True, Expense 12345 Updated")

    # Test missing expense_id
    data = {"group_id": 123, "amount": 100, "date": "2023-04-09T00:00:00.000Z"}
    response = client.put('/expense/edit', headers={
                          'Authorization': 'Bearer token', 'Content-Type': 'application/json'}, json=data)
    assert response.status_code == 400
    assert response.content_type == 'application/json'
    print("Error - Fields: expense_id not in request")

    # Test missing group_id
    data = {"expense_id": 12345, "amount": 100,
            "date": "2023-04-09T00:00:00.000Z"}
    response = client.put('/expense/edit', headers={
                          'Authorization': 'Bearer token', 'Content-Type': 'application/json'}, json=data)
    assert response.status_code == 400
    assert response.content_type == 'application/json'
    print("Error - Fields: group_id not in request")

    # Test missing amount
    data = {"expense_id": 12345, "group_id": 123,
            "date": "2023-04-09T00:00:00.000Z"}
    response = client.put('/expense/edit', headers={
                          'Authorization': 'Bearer token', 'Content-Type': 'application/json'}, json=data)
    assert response.status_code == 400
    assert response.content_type == 'application/json'
    print("Error - Fields: amount not in request")

    # Test expense not found
    data = {"expense_id": 99999, "group_id": 123,
            "amount": 100, "date": "2023-04-09T00:00:00.000Z"}
    response = client.put('/expense/edit', headers={
                          'Authorization': 'Bearer token', 'Content-Type': 'application/json'}, json=data)
    assert response.status_code == 404
    assert response.content_type == 'application/json'
    print("Expense not found")

    # Test invalid JWT token
    data = {"expense_id": 12345, "group_id": 123,
            "amount": 100, "date": "2023-04-09T00:00:00.000Z"}
    response = client.put('/expense/edit', headers={
                          'Authorization': 'Bearer invalid', 'Content-Type': 'application/json'}, json=data)
    assert response.status_code == 401
<<<<<<< HEAD


def test_expense_list(client):
    response = client.get('/expense/list?group_id=1', headers={
        'Authorization': 'Bearer access_token'
    })
    assert response.status_code == 200
    assert response.json['status'] == True
    assert isinstance(response.json['response'], list)


def test_expense_list_with_missing_group_id(client):
    response = client.get('/expense/list', headers={
        'Authorization': 'Bearer access_token'
    })
    assert response.status_code == 400
    assert 'Incomplete Query Parameters' in response.json['response']

def test_expense_update(client):
    response = client.put('/expense/update?group_id=1&expense_id=1', headers={
        'Authorization': 'Bearer access_token'}, json={
        'description': 'update the expense',
        'amount': 150.0,
        'date': '2022-04-09T12:30:00.000Z'
    })
    assert response.status_code == 200
    assert response.json['status'] == True
    assert "Expense: 1 updated" in response.json['response']

def test_expense_update_with_invalid_content_type(client):
    response = client.put('/expense/update?group_id=1&expense_id=1', headers={
        'Authorization': 'Bearer access_token',
        'Content-Type': 'text/plain'
    }, json={
        'description': 'update the expense',
        'amount': 150.0,
        'date': '2022-04-09T12:30:00.000Z'
    })
    assert response.status_code == 415
    assert response.json['status'] == False
    assert 'Unsupported Header Content-Type' in response.json['error']

def test_expense_update_with_missing_group_id(client):
    response = client.put('/expense/update?expense_id=1', headers={
        'Authorization': 'Bearer access_token',
        'Content-Type': 'text/plain'
    }, json={
        'description': 'update the expense',
        'amount': 150.0,
        'date': '2022-04-09T12:30:00.000Z'
    })
    assert response.status_code == 400
    assert response.json['status'] == False
    assert 'Fields: group_id not in request' in response.json['error']
=======
    assert response.content_type == 'application/json'
    print("Invalid token")
>>>>>>> 45eca6effe16ce51c46eb613a23490bf5629b613

import uuid
from flask_jwt_extended import create_access_token
from mock import patch
import pytest
import json
from app import app

@patch('modules.api.expense.expenseAPI.get_jwt_identity')
@patch('flask_jwt_extended.view_decorators.verify_jwt_in_request')
def test_detail_expense(test_client, mock_jwt_required, mock_jwt_identity):
    mock_jwt_identity.return_value = "test_user1@example.com"
    # Test valid request
    with app.app_context():
        token = create_access_token(identity=uuid.uuid4())
        response = test_client.get('/expense/detail?expense_id=123&group_id=456',
                               headers={'Authorization': 'Bearer: Aceesss Token'})
    assert response.status_code == 200
    assert response.content_type == 'application/json'
    print("Validating request.....")

def test_detail_expense_missing_expense_id(test_client):
        # Test missing expense_id
    response = test_client.get('/expense/detail?group_id=456',
                        headers={'Authorization': 'Bearer token'})
    assert response.status_code == 400
    assert response.content_type == 'application/json'
    print("Error:Expense ID cannot be null in the request params.")

def test_detail_expense_missing_group_id(test_client):
    # Test missing group_id
    response = test_client.get('/expense/detail?expense_id=123',
                          headers={'Authorization': 'Bearer token'})
    assert response.status_code == 400
    assert response.content_type == 'application/json'
    print("Error:Group ID cannot be null in the request params")


def test_detail_expense_invalid_token(test_client):
    # Test invalid JWT token
    response = test_client.get('/expense/detail?expense_id=123&group_id=456',
                          headers={'Authorization': 'Bearer invalid'})
    assert response.status_code == 401
    assert response.content_type == 'application/json'
    print("Message:Invalid token")

    # Test server error
    with app.app_context():
        app.testing = False
        response = test_client.get('/expense/detail?expense_id=123&group_id=456',
                              headers={'Authorization': 'Bearer token'})
        assert response.status_code == 500
        assert response.content_type == 'application/json'
        print("Exception occurred")


def test_create_expense(test_client):
    # Test valid request
    data = {"group_id": 123, "amount": 100, "date": "2023-04-09T00:00:00.000Z"}
    response = test_client.post('/expense/create', headers={
                           'Authorization': 'Bearer token', 'Content-Type': 'application/json'}, json=data)
    assert response.status_code == 201
    assert response.content_type == 'application/json'
    print("Expense 12345 Created")

def test_create_expense_missing_group_id(test_client):
    # Test missing group_id
    data = {"amount": 100, "date": "2023-04-09T00:00:00.000Z"}
    response = test_client.post('/expense/create', headers={
                           'Authorization': 'Bearer token', 'Content-Type': 'application/json'}, json=data)
    assert response.status_code == 400
    assert response.content_type == 'application/json'
    print("Fields: group_id not in request")

def test_create_expense_missing_amount(test_client):
    # Test missing amount
    data = {"group_id": 123, "date": "2023-04-09T00:00:00.000Z"}
    response = test_client.post('/expense/create', headers={
                           'Authorization': 'Bearer token', 'Content-Type': 'application/json'}, json=data)
    assert response.status_code == 400
    assert response.content_type == 'application/json'
    print("Expense missing amount.")


def test_update_expense(test_client):
    # Test valid request
    data = {"expense_id": 12345, "group_id": 123, 'description': 'test for expense update',
            "amount": 100, "date": "2023-04-09T00:00:00.000Z"}
    response = test_client.put('/expense/update', headers={
                          'Authorization': 'Bearer token', 'Content-Type': 'application/json'}, json=data)
    assert response.status_code == 200
    assert response.content_type == 'application/json'
    print("status: True, Expense 12345 Updated")


def test_update_expense_missing_expense_id(test_client):
    # Test missing expense_id
    data = {"group_id": 123, "amount": 100, 'description': 'test for expense update', "date": "2023-04-09T00:00:00.000Z"}
    response = test_client.put('/expense/update', headers={
                          'Authorization': 'Bearer token', 'Content-Type': 'application/json'}, json=data)
    assert response.status_code == 400
    assert response.content_type == 'application/json'
    print("Error - Fields: expense_id not in request")

def test_update_expense_missing_group_id(test_client):
    # Test missing group_id
    data = {"expense_id": 12345, "amount": 100, 'description': 'test for expense update',
            "date": "2023-04-09T00:00:00.000Z"}
    response = test_client.put('/expense/update', headers={
                          'Authorization': 'Bearer token', 'Content-Type': 'application/json'}, json=data)
    assert response.status_code == 400
    assert response.content_type == 'application/json'
    print("Error - Fields: group_id not in request")

def test_update_expense_missing_amount(test_client):
    # Test missing amount
    data = {"expense_id": 12345, "group_id": 123, 'description': 'test for expense update',
            "date": "2023-04-09T00:00:00.000Z"}
    response = test_client.put('/expense/update', headers={
                          'Authorization': 'Bearer token', 'Content-Type': 'application/json'}, json=data)
    assert response.status_code == 400
    assert response.content_type == 'application/json'
    print("Error - Fields: amount not in request")

def test_edit_expense_not_found(test_client):
    # Test expense not found
    data = {"expense_id": 99999, "group_id": 123, 'description': 'test for expense update',
            "amount": 100, "date": "2023-04-09T00:00:00.000Z"}
    response = test_client.put('/expense/update', headers={
                          'Authorization': 'Bearer token', 'Content-Type': 'application/json'}, json=data)
    assert response.status_code == 404
    assert response.content_type == 'application/json'
    print("Expense not found")


def test_update_expense_invalid_token(test_client):
    # Test invalid JWT token
    data = {"expense_id": 12345, "group_id": 123, 'description': 'test for expense update',
            "amount": 100, "date": "2023-04-09T00:00:00.000Z"}
    response = test_client.put('/expense/update', headers={
                          'Authorization': 'Bearer invalid', 'Content-Type': 'application/json'}, json=data)
    assert response.status_code == 401
    assert response.content_type == 'application/json'
    print("Invalid token")

def test_get_expense_list(client):
    response = client.get("/expense/list?group_id=456", headers={
                          'Authorization': 'Bearer token', 'Content-Type': 'application/json'})
    assert response.status_code == 200
    assert response.content_type == 'application/json'
    print("Get expense list")

def test_get_expense_list_missing_groupid(client):
    response = client.get("/expense/list", headers={
                          'Authorization': 'Bearer token', 'Content-Type': 'application/json'})
    assert response.content_type == 'application/json'
    assert "response" in response.json and response.json["response"] == 'Incomplete Query Parameters: "group_id" cannot be empty'
    print("list expense missing group id")

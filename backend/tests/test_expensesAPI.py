import json
import pytest
from app import app

# Test cases for expenses API

# @pytest.fixture
# def client():
#     with app.test_client() as client:
#         yield client


def test_create_expense(client):
    response = client.post('/expense/create', headers={
        'Authorization': 'Bearer access_token',
        'Content-Type': 'application/json'
    }, json={
        'group_id': '1',
        'amount': 100.0,
        'date': '2022-04-09T12:00:00.000Z'
    })
    assert response.status_code == 201
    assert response.json['status'] == True
    assert 'Expense' in response.json['response']


def test_create_expense_without_authorization(client):
    response = client.post('/expense/create', headers={
        'Content-Type': 'application/json'
    }, json={
        'group_id': '1',
        'amount': 100.0,
        'date': '2022-04-09T12:00:00.000Z'
    })
    assert response.status_code == 401


def test_create_expense_with_invalid_content_type(client):
    response = client.post('/expense/create', headers={
        'Authorization': 'Bearer access_token',
        'Content-Type': 'text/plain'
    }, json={
        'group_id': '1',
        'amount': 100.0,
        'date': '2022-04-09T12:00:00.000Z'
    })
    assert response.status_code == 415
    assert 'Unsupported Header Content-Type' in response.json['error']


def test_create_expense_with_missing_fields(client):
    response = client.post('/expense/create', headers={
        'Authorization': 'Bearer access_token',
        'Content-Type': 'application/json'
    }, json={
        'group_id': '1'
    })
    assert response.status_code == 400
    assert 'Fields' in response.json['error']


def test_detail_expense(client):
    response = client.get('/expense/detail?group_id=1&expense_id=1', headers={
        'Authorization': 'Bearer access_token'
    })
    assert response.status_code == 200
    assert response.json['status'] == True
    assert 'amount' in response.json['response']


def test_detail_expense_with_invalid_group_id(client):
    response = client.get('/expense/detail?group_id=invalid&expense_id=1', headers={
        'Authorization': 'Bearer access_token'
    })
    assert response.status_code == 404


def test_detail_expense_with_invalid_expense_id(client):
    response = client.get('/expense/detail?group_id=1&expense_id=invalid', headers={
        'Authorization': 'Bearer access_token'
    })
    assert response.status_code == 404


def test_detail_expense_without_authorization(client):
    response = client.get('/expense/detail?group_id=1&expense_id=1')
    assert response.status_code == 401


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

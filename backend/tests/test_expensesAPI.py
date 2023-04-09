import pytest
import json
from app import app


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_detail_expense(client):
    # Test valid request
    response = client.get('/expense/detail?expense_id=123&group_id=456',
                          headers={'Authorization': 'Bearer token'})
    assert response.status_code == 200
    assert response.content_type == 'application/json'
    assert json.loads(response.data) == {"status": True, "response": {...}}

    # Test missing expense_id
    response = client.get('/expense/detail?group_id=456',
                          headers={'Authorization': 'Bearer token'})
    assert response.status_code == 400
    assert response.content_type == 'application/json'
    assert json.loads(response.data) == {
        "error": "Expense ID cannot be null in the request params"}

    # Test missing group_id
    response = client.get('/expense/detail?expense_id=123',
                          headers={'Authorization': 'Bearer token'})
    assert response.status_code == 400
    assert response.content_type == 'application/json'
    assert json.loads(response.data) == {
        "error": "Group ID cannot be null in the request params"}

    # Test invalid JWT token
    response = client.get('/expense/detail?expense_id=123&group_id=456',
                          headers={'Authorization': 'Bearer invalid'})
    assert response.status_code == 401
    assert response.content_type == 'application/json'
    assert json.loads(response.data) == {"msg": "Invalid token"}

    # Test server error
    with app.app_context():
        app.testing = False
        response = client.get('/expense/detail?expense_id=123&group_id=456',
                              headers={'Authorization': 'Bearer token'})
        assert response.status_code == 500
        assert response.content_type == 'application/json'
        assert json.loads(response.data) == {"error": "Exception occurred"}


def test_create_expense(client):
    # Test valid request
    data = {"group_id": 123, "amount": 100, "date": "2023-04-09T00:00:00.000Z"}
    response = client.post('/expense/create', headers={
                           'Authorization': 'Bearer token', 'Content-Type': 'application/json'}, json=data)
    assert response.status_code == 201
    assert response.content_type == 'application/json'
    assert json.loads(response.data) == {
        "status": True, "response": "Expense 12345 Created"}

    # Test missing group_id
    data = {"amount": 100, "date": "2023-04-09T00:00:00.000Z"}
    response = client.post('/expense/create', headers={
                           'Authorization': 'Bearer token', 'Content-Type': 'application/json'}, json=data)
    assert response.status_code == 400
    assert response.content_type == 'application/json'
    assert json.loads(response.data) == {
        "error": "Fields: group_id not in request"}

    # Test missing amount
    data = {"group_id": 123, "date": "2023-04-09T00:00:00.000Z"}
    response = client.post('/expense/create', headers={
                           'Authorization': 'Bearer token', 'Content-Type': 'application/json'}, json=data)
    assert response.status_code == 400
    assert response.content_type == 'application/json'
    assert json.loads


def test_edit_expense(client):
    # Test valid request
    data = {"expense_id": 12345, "group_id": 123,
            "amount": 100, "date": "2023-04-09T00:00:00.000Z"}
    response = client.put('/expense/edit', headers={
                          'Authorization': 'Bearer token', 'Content-Type': 'application/json'}, json=data)
    assert response.status_code == 200
    assert response.content_type == 'application/json'
    assert json.loads(response.data) == {
        "status": True, "response": "Expense 12345 Updated"}

    # Test missing expense_id
    data = {"group_id": 123, "amount": 100, "date": "2023-04-09T00:00:00.000Z"}
    response = client.put('/expense/edit', headers={
                          'Authorization': 'Bearer token', 'Content-Type': 'application/json'}, json=data)
    assert response.status_code == 400
    assert response.content_type == 'application/json'
    assert json.loads(response.data) == {
        "error": "Fields: expense_id not in request"}

    # Test missing group_id
    data = {"expense_id": 12345, "amount": 100,
            "date": "2023-04-09T00:00:00.000Z"}
    response = client.put('/expense/edit', headers={
                          'Authorization': 'Bearer token', 'Content-Type': 'application/json'}, json=data)
    assert response.status_code == 400
    assert response.content_type == 'application/json'
    assert json.loads(response.data) == {
        "error": "Fields: group_id not in request"}

    # Test missing amount
    data = {"expense_id": 12345, "group_id": 123,
            "date": "2023-04-09T00:00:00.000Z"}
    response = client.put('/expense/edit', headers={
                          'Authorization': 'Bearer token', 'Content-Type': 'application/json'}, json=data)
    assert response.status_code == 400
    assert response.content_type == 'application/json'
    assert json.loads(response.data) == {
        "error": "Fields: amount not in request"}

    # Test expense not found
    data = {"expense_id": 99999, "group_id": 123,
            "amount": 100, "date": "2023-04-09T00:00:00.000Z"}
    response = client.put('/expense/edit', headers={
                          'Authorization': 'Bearer token', 'Content-Type': 'application/json'}, json=data)
    assert response.status_code == 404
    assert response.content_type == 'application/json'
    assert json.loads(response.data) == {"error": "Expense not found"}

    # Test invalid JWT token
    data = {"expense_id": 12345, "group_id": 123,
            "amount": 100, "date": "2023-04-09T00:00:00.000Z"}
    response = client.put('/expense/edit', headers={
                          'Authorization': 'Bearer invalid', 'Content-Type': 'application/json'}, json=data)
    assert response.status_code == 401
    assert response.content_type == 'application/json'
    assert json.loads(response.data) == {"msg": "Invalid token"}

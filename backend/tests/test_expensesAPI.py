#not to be tested.

# from unittest import mock
# import uuid
# from flask_jwt_extended import create_access_token
# import pytest
# import json
# from app import app

# def test_detail_expense_valid_request(test_client):
#     # Test valid request
#     # with app.app_context():
#     #     # token = create_access_token(identity=uuid.uuid4())
#     #     token = "123444"
#     #     mock.patch('modules.api.expense.expenseAPI.get_jwt_identity', return_value="test_user1@example.com")
#     #     response = test_client.get('/expense/detail?expense_id=123&group_id=456',
#     #                            headers={'Authorization': f'Bearer {token}'})
#     # assert response.status_code == 200
#     # assert response.content_type == 'application/json'
#     # print("Validating request.....")
#     with app.test_request_context():
#         token = create_access_token(identity=uuid.uuid4())
#         mock.patch('modules.api.expense.expenseAPI.get_jwt_identity', return_value="test_user1@example.com")
#         response = test_client.get('/expense/detail?expense_id=123&group_id=456',
#                                headers={'Authorization': f'Bearer {token}'})
        
#     assert response.status_code == 200
#     assert response.content_type == 'application/json'
#     print("Validating request.....")

# def test_detail_expense_missing_expense_id(test_client):
#     # Test missing expense_id
#     response = test_client.get('/expense/detail?group_id=456',
#                         headers={'Authorization': 'Bearer token'})
#     assert response.status_code == 400
#     assert response.content_type == 'application/json'
#     print("Error:Expense ID cannot be null in the request params.")

# def test_detail_expense_missing_group_id(test_client):
#     # Test missing group_id
#     response = test_client.get('/expense/detail?expense_id=123',
#                           headers={'Authorization': 'Bearer token'})
#     assert response.status_code == 400
#     assert response.content_type == 'application/json'
#     print("Error:Group ID cannot be null in the request params")


# def test_detail_expense_invalid_token(test_client):
#     # Test invalid JWT token
#     response = test_client.get('/expense/detail?expense_id=123&group_id=456',
#                           headers={'Authorization': 'Bearer invalid'})
#     assert response.status_code == 401
#     assert response.content_type == 'application/json'
#     print("Message:Invalid token")

# def test_detail_expense_server_error(test_client):
#     # Test server error
#     mock.patch('modules.api.expense.expenseAPI.get_jwt_identity', return_value="test_user1@example.com")
#     with app.app_context():
#         app.testing = False
#         response = test_client.get('/expense/detail?expense_id=123&group_id=456',
#                               headers={'Authorization': 'Bearer token'})
#         assert response.status_code == 500
#         assert response.content_type == 'application/json'
#         print("Exception occurred")


# def test_create_expense_valid_request(test_client):
#     # Test valid request
#     data = {"group_id": 123, "amount": 100, "date": "2023-04-09T00:00:00.000Z"}
#     response = test_client.post('/expense/create', headers={
#                            'Authorization': 'Bearer token', 'Content-Type': 'application/json'}, json=data)
#     assert response.status_code == 201
#     assert response.content_type == 'application/json'
#     print("Expense 12345 Created")

# def test_create_expense_missing_group_id(test_client):
#     # Test missing group_id
#     data = {"amount": 100, "date": "2023-04-09T00:00:00.000Z"}
#     response = test_client.post('/expense/create', headers={
#                            'Authorization': 'Bearer token', 'Content-Type': 'application/json'}, json=data)
#     assert response.status_code == 400
#     assert response.content_type == 'application/json'
#     print("Fields: group_id not in request")
import json
from flask import current_app
from app import app

# test case when no users are in the group
def test_no_users():
    expenses = {'user1': 50, 'user2': 70, 'user3': 30}
    group = []
    with app.app_context():
        response = current_app.test_client().post(
            '/settleUp',
            data=json.dumps({'expenses': expenses, 'group': group}),
            content_type='application/json'
        )
        assert response.status_code == 405

# test case when expenses dictionary is empty
def test_no_expenses():
    expenses = {}
    group = ['user1', 'user2', 'user3']
    response = app.test_client().post(
        '/settleUp',
        data=json.dumps({'expenses': expenses, 'group': group}),
        content_type='application/json'
    )
    assert response.status_code == 405


# Test case for invalid input type
def test_netAmount_invalid_input_type():
    expenses = "invalid"
    group = "invalid"
    response = app.test_client().post(
        '/settleUp',
        data=json.dumps({'expenses': expenses, 'group': group}),
        content_type='application/json'
    )
    assert response.status_code == 405

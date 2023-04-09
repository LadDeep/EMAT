import json
import pytest
from app import app

# test case when no users are in the group
def test_no_users():
    expenses = {'user1': 50, 'user2': 70, 'user3': 30}
    group = []
    response = app.test_client().post(
        '/settleUp',
        data=json.dumps({'expenses': expenses, 'group': group}),
        content_type='application/json'
    )
    assert response.status_code == 400

# test case when expenses dictionary is empty
def test_no_expenses():
    expenses = {}
    group = ['user1', 'user2', 'user3']
    response = app.test_client().post(
        '/settleUp',
        data=json.dumps({'expenses': expenses, 'group': group}),
        content_type='application/json'
    )
    assert response.status_code == 400

# test case when all users have equal expenses
def test_equal_expenses():
    expenses = {'user1': 50, 'user2': 50, 'user3': 50}
    group = ['user1', 'user2', 'user3']
    response = app.test_client().post(
        '/settleUp',
        data=json.dumps({'expenses': expenses, 'group': group}),
        content_type='application/json'
    )
    data = json.loads(response.data)
    assert response.status_code == 200
    assert data['isZero'] == True
    assert data['Net amount']['user1'] == 0
    assert data['Net amount']['user2'] == 0
    assert data['Net amount']['user3'] == 0

# test case when one user owes money and others get money back
def test_unequal_expenses():
    expenses = {'user1': 20, 'user2': 60, 'user3': 20}
    group = ['user1', 'user2', 'user3']
    response = app.test_client().post(
        '/settleUp',
        data=json.dumps({'expenses': expenses, 'group': group}),
        content_type='application/json'
    )
    data = json.loads(response.data)
    assert response.status_code == 200
    assert data['isZero'] == True
    assert data['Net amount']['user1'] == -20
    assert data['Net amount']['user2'] == 40
    assert data['Net amount']['user3'] == -20



# Test case for valid input with equal expenses
def test_netAmount_equal_expenses():
    expenses = {'A': 50, 'B': 50, 'C': 50}
    group = ['A', 'B', 'C']
    response, status_code = netAmount(expenses=expenses, group=group)
    assert status_code == 200
    assert response['Net amount'] == {'A': 0, 'B': 0, 'C': 0}
    assert response['isZero'] == True

# Test case for valid input with unequal expenses
def test_netAmount_unequal_expenses():
    expenses = {'A': 100, 'B': 50, 'C': 25}
    group = ['A', 'B', 'C']
    response, status_code = netAmount(expenses=expenses, group=group)
    assert status_code == 200
    assert response['Net amount'] == {'A': 25, 'B': -25, 'C': -25}
    assert response['isZero'] == False

# Test case for valid input with extra users
def test_netAmount_extra_users():
    expenses = {'A': 100, 'B': 50, 'C': 25}
    group = ['A', 'B', 'C', 'D', 'E']
    response, status_code = netAmount(expenses=expenses, group=group)
    assert status_code == 200
    assert response['Net amount'] == {'A': 25, 'B': -25, 'C': -25, 'D': -25, 'E': -25}
    assert response['isZero'] == False

# Test case for valid input with missing expenses
def test_netAmount_missing_expenses():
    expenses = {'A': 100, 'B': 50}
    group = ['A', 'B', 'C']
    response, status_code = netAmount(expenses=expenses, group=group)
    assert status_code == 200
    assert response['Net amount'] == {'A': 16.67, 'B': -33.33, 'C': -33.33}
    assert response['isZero'] == False

# Test case for empty input
def test_netAmount_empty_input():
    expenses = {}
    group = []
    response, status_code = netAmount(expenses=expenses, group=group)
    assert status_code == 200
    assert response['Net amount'] == {}
    assert response['isZero'] == True

# Test case for invalid input type
def test_netAmount_invalid_input_type():
    expenses = "invalid"
    group = "invalid"
    response, status_code = netAmount(expenses=expenses, group=group)
    assert status_code == 400

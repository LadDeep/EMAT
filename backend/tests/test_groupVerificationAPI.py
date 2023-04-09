import pytest
from flask import json
import app

def test_group_verification_mail_missing_email(client):
    res = client.post('/groupVerificationMail')
    assert res.status_code == 400
    assert json.loads(res.data)['success'] == False

def test_group_verification_mail_valid_email(client):
    data = {'email': 'emat@example.com'}
    res = client.post('/groupVerificationMail', data=data)
    assert res.status_code == 200
    assert json.loads(res.data)['success'] == True

def test_verify_code_missing_email(client):
    data = {'code': '123456'}
    res = client.post('/verifyCode', data=data)
    assert res.status_code == 400
    assert json.loads(res.data)['success'] == False

def test_verify_code_missing_code(client):
    data = {'email': 'emat@example.com'}
    res = client.post('/verifyCode', data=data)
    assert res.status_code == 400
    assert json.loads(res.data)['success'] == False

def test_verify_code_invalid_email(client):
    data = {'email': 'fakeemail@example.com', 'code': '123456'}
    res = client.post('/verifyCode', data=data)
    assert res.status_code == 404
    assert json.loads(res.data)['success'] == False

def test_verify_code_invalid_code(client):
    data = {'email': 'emat@example.com', 'code': '000000'}
    res = client.post('/verifyCode', data=data)
    assert res.status_code == 401
    assert json.loads(res.data)['success'] == False

def test_verify_code_valid(client):
    # set up verification code for email
    data = {'email': 'emat@example.com'}
    res = client.post('/groupVerificationMail', data=data)
    assert res.status_code == 200
    assert json.loads(res.data)['success'] == True
    verification_code = json.loads(res.data)['verification_code']

    # verify email with correct code
    data = {'email': 'emat@example.com', 'code': verification_code}
    res = client.post('/verifyCode', data=data)
    assert res.status_code == 200
    assert json.loads(res.data)['success'] == True

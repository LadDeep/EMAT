import pytest
from app import app, sendVerificationEmail, verificationCodes

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_send_verification_email(client):
    email = "emat@example.com"
    code = sendVerificationEmail(email)
    assert code.isdigit() and len(code) == 6
    assert email in verificationCodes and verificationCodes[email] == code

def test_password_reset(client):
    response = client.post('/passwordResetMail', data={'email': 'emat@example.com'})
    assert response.status_code == 200
    assert b"Verification code sent successfully" in response.data

def test_verify_code(client):
    email = "email@example.com"
    code = verificationCodes[email]
    response = client.post('/verifyCode', data={'email': email, 'code': code})
    assert response.status_code == 200
    assert b"Email sent successfully" in response.data

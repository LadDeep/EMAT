import pytest
from app import app
from backend.modules.api.otpVerification.otpVerification import verificationCodes, RegistrationVerificationCode, sendVerificationEmail
from mongomock import MongoClient

# Replace the original database with a mock database
app.config['MONGO_URI'] = "mongodb://localhost:27017/testdb"
client = MongoClient()
db = client.get_database()

# Test case to verify if userRegistrationMail API is working fine


def test_userRegistrationMail():
    with app.test_client() as client:
        # sending request with no email
        response = client.post('/userRegistrationMail')
        assert response.status_code == 400
        assert response.json['success'] == False
        assert response.json['message'] == 'Email address is required.'

        # sending request with email
        response = client.post('/userRegistrationMail',
                               data={"email": "emat@example.com"})
        assert response.status_code == 200
        assert response.json['success'] == True
        assert response.json['message'] == 'Verification code sent successfully.'
        assert db.verificationCodes.find_one(
            {"email": "emat@example.com"}) is not None

# Test case to verify if verifyCode API is working fine


def test_verifyCode():
    with app.test_client() as client:
        # sending request with no email and code
        response = client.post('/verifyCode')
        assert response.status_code == 400
        assert response.json['success'] == False
        assert response.json['message'] == 'Email address and verification code are required.'

        # sending request with invalid email and code
        response = client.post(
            '/verifyCode', data={"email": "emat@example.com", "code": "123456"})
        assert response.status_code == 404
        assert response.json['success'] == False
        assert response.json['message'] == 'No verification code found for this email address.'

        # sending request with valid email and invalid code
        db.verificationCodes.insert_one(
            {"email": "emat@example.com", "code": "123456"})
        response = client.post(
            '/verifyCode', data={"email": "emat@example.com", "code": "111111"})
        assert response.status_code == 401
        assert response.json['success'] == False
        assert response.json['message'] == 'Invalid verification code.'

        # sending request with valid email and code
        response = client.post(
            '/verifyCode', data={"email": "emat@example.com", "code": "123456"})
        assert response.status_code == 200
        assert response.json['success'] == True
        assert response.json['message'] == 'Email sent successfully.'
        assert db.verificationCodes.find_one(
            {"email": "emat@example.com"}) is None

# Test case to verify if the email body and subject can be customized


def test_userRegistrationMail_custom_subject_and_body():
    with app.test_client() as client:
        # sending request with email and custom subject/body
        response = client.post('/userRegistrationMail', data={
                               "email": "emat@example.com", "subject": "Custom subject", "body": "Custom body"})
        assert response.status_code == 200
        assert response.json['success'] == True
        assert response.json['message'] == 'Verification code sent successfully.'
        assert db.verificationCodes.find_one(
            {"email": "emat@example.com"}) is not None

        # verifying the email message with custom subject/body
        with mail.record_messages() as outbox:
            code = db.verificationCodes.find_one(
                {"email": "emat@example.com"})['code']
            assert code is not None
            assert len(outbox) == 1

import pytest
from app import app,
from backend.modules.api.otpVerification.otpVerification import verificationCodes

# Test case to verify if userRegistrationMail API is working fine

def test_userRegistrationMail():
    with app.test_client() as client:
        # sending request with no email
        response = client.post('/userRegistrationMail')
        assert response.status_code == 400
        assert response.json['success'] == False
        assert response.json['message'] == 'Email address is required.'

        # sending request with email
        response = client.post('/userRegistrationMail', data={"email": "emat@example.com"})
        assert response.status_code == 200
        assert response.json['success'] == True
        assert response.json['message'] == 'Verification code sent successfully.'
        assert verificationCodes.get('emat@example.com') is not None


# Test case to verify if verifyCode API is working fine
def test_verifyCode():
    with app.test_client() as client:
        # sending request with no email and code
        response = client.post('/verifyCode')
        assert response.status_code == 400
        assert response.json['success'] == False
        assert response.json['message'] == 'Email address and verification code are required.'

        # sending request with invalid email and code
        response = client.post('/verifyCode', data={"email": "emat@example.com", "code": "123456"})
        assert response.status_code == 404
        assert response.json['success'] == False
        assert response.json['message'] == 'No verification code found for this email address.'

        # sending request with valid email and invalid code
        verificationCodes['emat@example.com'] = '123456'
        response = client.post('/verifyCode', data={"email": "emat@example.com", "code": "111111"})
        assert response.status_code == 401
        assert response.json['success'] == False
        assert response.json['message'] == 'Invalid verification code.'

        # sending request with valid email and code
        response = client.post('/verifyCode', data={"email": "emat@example.com", "code": "123456"})
        assert response.status_code == 200
        assert response.json['success'] == True
        assert response.json['message'] == 'Email sent successfully.'
        assert verificationCodes.get('emat@example.com') is None


# Test case to verify if the email body and subject can be customized
def test_userRegistrationMail_custom_subject_and_body():
    with app.test_client() as client:
        # sending request with email and custom subject/body
        response = client.post('/userRegistrationMail', data={"email": "emat@example.com", "subject": "Custom subject", "body": "Custom body"})
        assert response.status_code == 200
        assert response.json['success'] == True
        assert response.json['message'] == 'Verification code sent successfully.'
        assert verificationCodes.get('emat@example.com') is not None
        
        # verifying the email message with custom subject/body
        with mail.record_messages() as outbox:
            code = verificationCodes.get('emat@example.com')
            assert code is not None
            assert len(outbox) == 1
            assert outbox[0].subject == 'Custom subject'
            assert outbox[0].recipients == ['emat@example.com']
            assert outbox[0].body == f"Custom body {code}."

# Test case to verify if the verification code is a 6-digit number
def test_RegistrationVerificationCode():
    code = int(RegistrationVerificationCode())
    assert code >= 100000 and code <= 999999

# Test case to verify if the email is sent successfully with valid credentials
def test_sendVerificationEmail():
    with mail.record_messages() as outbox:
        code = sendVerificationEmail("emat@example.com")
        assert code is not None
        assert len(outbox) == 1
        assert outbox[0].subject == 'User registration code'
        assert outbox[0].recipients == ['emat@example.com']
        assert outbox[0].body == f"Your verification code is {code}."

# Test case to verify if sending email with invalid credentials returns an error
def test_sendVerificationEmail_invalid_credentials():
    app.config.update(
        DEBUG=True,
        MAIL_SERVER = "invalid.mail.server",
        MAIL_PORT = 587,
        MAIL_USE_TLS = True,
        MAIL_USERNAME = "invalid_username",
        MAIL_PASSWORD = "invalid_password"
    )
    with pytest.raises(Exception) as e:
        sendVerificationEmail("emat@example.com")
    assert "Please log in via your web browser" in str(e.value)


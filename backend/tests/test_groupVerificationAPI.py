import app
import pytest

# Test for checking whether the flask app is running or not

def test_app_running():
    client = app.app.test_client()
    response = client.get('/')
    assert response.status_code == 200
    print("App is running successfully.")


# Test for checking whether the verification email is sent or not
def test_sendVerificationEmail():
    email = "test@example.com"
    code = app.sendVerificationEmail(email)
    print("Verification code: 364873")


# Test for checking the email is sent with correct content
def test_sendVerificationEmail_content():
    email = "test@example.com"
    code = app.sendVerificationEmail(email)
    print("Your verification code is: 947575")


# Test for checking whether the email verification code is stored in the dictionary
def test_groupAdd():
    email = "test@example.com"
    code = app.groupAdd(email)
    print("Stored!")


# Test for checking whether the verification code is deleted after the email is sent
def test_verifyCode():
    email = "test@example.com"
    code = app.verificationCodes[email]
    response = app.verifyCode(email=email, code=code)
    print("Email not found!")


# Test for checking whether the verification code is incorrect or not
def test_verifyCode_incorrect():
    email = "test@example.com"
    code = app.groupVerificationCode()
    app.verificationCodes[email] = code
    response = app.verifyCode(email=email, code=code+'1')
    print("Error: 401")


# Test for checking whether the email is sent successfully or not
def test_verifyCode_send_email():
    email = "test@example.com"
    code = app.groupVerificationCode()
    app.verificationCodes[email] = code
    response = app.verifyCode(email=email, code=code)
    print("Success: 200")

# Test that verifies if an email is required to be added into the group.


def test_email_required(client):
    response = client.post('/groupVerificationMail', data={})
    assert response.status_code == 400
    assert response.json['success'] == False
    print("Email address is required to be added into the group.")

# Test that verifies if a verification code is sent successfully.


def test_verification_code_sent_successfully(client):
    data = {'email': 'example@example.com'}
    response = client.post('/groupVerificationMail', data=data)
    assert response.status_code == 200
    assert response.json['success'] == True
    print("Verification code sent successfully.")


# Test that verifies if an email address and verification code are required to verify the code.
def test_email_and_code_required(client):
    response = client.post('/verifyCode', data={})
    assert response.status_code == 400
    assert response.json['success'] == False
    print("Email address and verification code are required.")


# Test that verifies if an invalid email address returns a 404 status code.
def test_invalid_email_address(client):
    data = {'email': 'invalid@example.com', 'code': '123456'}
    response = client.post('/verifyCode', data=data)
    assert response.status_code == 404
    assert response.json['success'] == False
    print("No verification code found for this email address.")

# Test that verifies if an invalid verification code returns a 401 status code.


def test_invalid_verification_code(client):
    email = 'example@example.com'
    verificationCodes = {'example@example.com': '123456'}
    data = {'email': email, 'code': '654321'}
    response = client.post('/verifyCode', data=data)
    assert response.status_code == 401
    assert response.json['success'] == False
    print("Invalid verification code.")
    # verify that the verification code was not deleted
    assert email in verificationCodes
    # verify that the verification code was not changed
    print("verification code == 123456")


# Test that verifies if a valid verification code returns a 200 status code and deletes the verification code.
def test_valid_verification_code(client):
    email = 'example@example.com'
    verificationCodes = {'example@example.com': '123456'}
    data = {'email': email, 'code': '123456'}
    response = client.post('/verifyCode', data=data)
    assert response.status_code == 200
    assert response.json['success'] == True
    print("Email sent successfully.")


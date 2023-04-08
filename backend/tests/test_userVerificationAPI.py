import pytest
from flask import json
import app


# testcases for userVerification.


# check if code is 6 digits long

def test_registration_verification_code():
    code = app.RegistrationVerificationCode()
    assert len(code) == 6  
    

# check if email is added to verificationCodes
def test_send_verification_email():
    email = "emat@example.com"
    code = app.sendVerificationEmail(email)
    assert email in app.verificationCodes  
    
    
    # check if code is added to verificationCodes
    assert app.verificationCodes[email] == code  

    
# check if success message is returned

def test_user_registration_mail(client):
    response = client.post('/userRegistrationMail', data={"email": "emat@example.com"})
    assert response.status_code == 200
    assert b'"success":true' in response.data  
    
    
 # check if success message is returned
def test_verify_code(client):
    email = "emat@example.com"
    code = app.sendVerificationEmail(email)
    response = client.post('/verifyCode', data={"email": email, "code": code})
    assert response.status_code == 200
    assert b'"success":true' in response.data 

# Import the necessary libraries
import pytest
from unittest.mock import patch
from backend.modules.api.otpVerification.otpVerification import sendVerificationEmail, passwordReset

# Define test data for the functions
test_data = {
    "sendVerificationEmail": {
        "valid_email": "test@example.com",
        "invalid_email": "",
        "expected_success": True,
        "expected_message": "Verification code sent successfully."
    },
    "passwordReset": {
        "valid_email": "test@example.com",
        "invalid_email": "",
        "expected_success": True,
        "expected_message": "Verification code sent successfully."
    },
    "verifyCode": {
        "valid_email": "test@example.com",
        "valid_code": "123456",
        "invalid_email": "",
        "invalid_code": "",
        "expected_success": True,
        "expected_message": "Email sent successfully."
    }
}

# Define the fixtures needed for the tests
@pytest.fixture()
def mock_mail():
    with patch("backend.modules.api.otpVerification.otpVerification.Mail") as mock_mail:
        mock_mail.return_value.send.return_value = True
        yield mock_mail

@pytest.fixture()
def mock_passwordVerificationCode():
    with patch("backend.modules.api.otpVerification.otpVerification.passwordVerificationCode") as mock_passwordVerificationCode:
        mock_passwordVerificationCode.return_value = "123456"
        yield mock_passwordVerificationCode

@pytest.fixture()
def mock_verificationCodes():
    with patch("backend.modules.api.otpVerification.otpVerification.verificationCodes") as mock_verificationCodes:
        mock_verificationCodes.__contains__.return_value = True
        mock_verificationCodes.__getitem__.return_value = "123456"
        mock_verificationCodes.__delitem__.return_value = True
        yield mock_verificationCodes

# Define the tests for the functions
def test_sendVerificationEmail_valid_email(mock_mail):
    # Test sending a verification email with a valid email address
    response = sendVerificationEmail(test_data["sendVerificationEmail"]["valid_email"])
    assert response["success"] == test_data["sendVerificationEmail"]["expected_success"]
    assert response["message"] == test_data["sendVerificationEmail"]["expected_message"]
    mock_mail.assert_called_once()

def test_sendVerificationEmail_invalid_email(mock_mail):
    # Test sending a verification email with an invalid email address
    response = sendVerificationEmail(test_data["sendVerificationEmail"]["invalid_email"])
    assert response["success"] == False
    assert response["message"] == "Email address is required."
    mock_mail.assert_not_called()

def test_passwordReset_valid_email(mock_mail, mock_passwordVerificationCode):
    # Test generating a verification code and storing it in the verificationCodes dictionary
    response = passwordReset(test_data["passwordReset"]["valid_email"])
    assert response["success"] == test_data["passwordReset"]["expected_success"]
    assert response["message"] == test_data["passwordReset"]["expected_message"]
    mock_mail.assert_called_once()
    mock_passwordVerificationCode.assert_called_once()

def test_passwordReset_invalid_email(mock_mail, mock_passwordVerificationCode):
    # Test generating a verification code with an invalid email address
    response = passwordReset(test_data["passwordReset"]["invalid_email"])
    assert response["success"] == False
    assert response["message"] == "Email address is required."
    mock_mail.assert_not_called()
    mock_passwordVerificationCode.assert_not_called()

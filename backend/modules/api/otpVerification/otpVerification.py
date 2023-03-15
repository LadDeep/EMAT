#API for sending and verifying OTP during password reset!
#Importing Modules

from flask import Flask, request
from flask_mail import Mail, Message
import random

#Initializing flask-mail and adding admin email credentials

app = Flask(__name__)
app.config.update(
    DEBUG=True,
    MAIL_SERVER = "smtp.mail.yahoo.com.",
    MAIL_PORT = 587,
    MAIL_USE_TLS = True,
    MAIL_USERNAME = "ematemailverification@yahoo.com",
    MAIL_PASSWORD = "EjK6zTfZgwwySxK"  

)

mail = Mail(app)


#Generating random 6 digits verification codes

def passwordVerificationCode():
    return str(random.randint(100000, 999999))


#Sending verification email for user registration

# user's email as parameter into argument = to

def sendVerificationEmail(to):

    verificationCode = passwordVerificationCode()
    message = Message(

        subject = "Password reset code",
        recipients = [to],
        body = f"Your verification code is {verificationCode}."
    )

    mail.send(message)

    return verificationCode


# Using function in route to send and verify the code

#dictionary to store verification code, email as key and code as pair.
verificationCodes = {}

@app.route("/passwordResetMail", methods = ["POST"])

def passwordReset():

    email = request.form.get("email")

    #If no email is provided
    if not email:
        return "Email address is required.", 400
    
    subject = request.form.get("subject", "Verification code")
    body = request.form.get("body", "")

    #error handling using try-catch block
    #if any exception arise, trigger 500 response

    try:
        code = passwordReset(email)
        verificationCodes[email] = code
    
    except Exception as e:
        return f"Unable to send email: {str(e)}", 500
    return "Verification code sent succefully."



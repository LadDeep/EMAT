#This API sends and verify the OTP shared via Email during user registration

#Importing Modules

from flask import Flask, request
from flask_mail import Mail, Message
import random

#Initializing flask-mail and adding admin email credentials

app = Flask(__name__)
app.config.update(
    DEBUG=True,
    MAIL_SERVER = "smtp.gmail.com",
    MAIL_PORT = 587,
    MAIL_USE_TLS = True,
    MAIL_USERNAME = "NAME@gmail.com",
    MAIL_PASSWORD = "Password"  

)

mail = Mail(app)


#Generating random 6 digits verification codes

def RegistrationVerificationCode():
    return str(random.randint(100000, 999999))


#Sending verification email for user registration

def sendVerificationEmail(to):

    verificationCode = RegistrationVerificationCode()
    message = Message(

        subject = "User registration code email",
        recipients = [to],
        body = f"Your verification code is {verificationCode}."
    )

    mail.send(message)

    return verificationCode



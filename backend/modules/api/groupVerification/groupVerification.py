#API for sending and verifying OTP during adding user into the group.
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

def groupVerificationCode():
    return str(random.randint(100000, 999999))


#Sending verification email for user registration

# user's email as parameter into argument = to

def sendVerificationEmail(to):

    verificationCode = groupVerificationCode()
    message = Message(

        subject = "Group joining verification code",
        recipients = [to],
        body = f"Your verification code is {verificationCode}."
    )

    mail.send(message)

    return verificationCode


# Using function in route to send and verify the code

#dictionary to store verification code, email as key and code as pair.
verificationCodes = {}

@app.route("/groupVerificationMail", methods = ["POST"])

def groupAdd():

    email = request.form.get("email")

    #If no email is provided
    if not email:
        return "Email address is required.", 400
    
    subject = request.form.get("subject", "Verification code")
    body = request.form.get("body", "")

    #error handling using try-catch block
    #if any exception arise, trigger 500 response

    try:
        code = groupAdd(email)
        verificationCodes[email] = code
    
    except Exception as e:
        return f"Unable to send email: {str(e)}", 500
    return "Verification code sent succefully."



#API to verify the verification code

@app.route("/verifyCode", methods = ["POST"])

def verifyCode():

    email = request.form.get("email")
    code = request.form.get("code")

    #if email doesn't match with the vefification code

    if email or not code:
        return "Email and verification code are required.", 400
    
    if email not in verificationCodes:
        return "No verification code found for this email.", 404
    
    if verificationCodes[email] != code:
        return "Invalid verification code. Please request a new code", 401
    
    #Deleting verification code, so that new code can be store.
    del verificationCodes[email]


    #Email response format and error handling

    try:
        message = Message(
            subject = "Email confirmed",
            recipients = [email],
            body = "User's email has been verified."
        )
        mail.send(message)

    except Exception as e:
        return f"Failed to send email: {str(e)}", 500
    

    return "Email sent successfully."
    




#API for sending and verifying OTP during password reset!
#Importing Modules

from flask import Flask, jsonify, request
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
        return jsonify(success=False, message="Email address is required."), 400
    
    
    subject = request.form.get("subject", "Verification code")
    body = request.form.get("body", "")

    #error handling using try-catch block
    #if any exception arise, trigger 500 response

    try:
        code = passwordReset(email)
        verificationCodes[email] = code
    
    except Exception as e:
         return jsonify(success=False, message=f"Unable to send email: {str(e)}"), 500
    

    return jsonify(success=True, message="Verification code sent successfully.")




#API to verify the verification code

@app.route("/verifyCode", methods = ["POST"])

def verifyCode():

    email = request.form.get("email")
    code = request.form.get("code")

    #if email doesn't match with the vefification code

    if email or not code:
         return jsonify(success=False, message="Email address and verification code are required."), 400
    
    if email not in verificationCodes:
       return jsonify(success=False, message="No verification code found for this email address."), 404
    
    
    if verificationCodes[email] != code:
       return jsonify(success=False, message="Invalid verification code."), 401
    
    
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
    

    return jsonify(success=True, message="Email sent successfully.")




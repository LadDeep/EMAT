import datetime
import uuid
import json
from smtplib import SMTPAuthenticationError, SMTPServerDisconnected, SMTPException
from flask import request, jsonify, Blueprint, current_app, session
from flask_jwt_extended import create_access_token, decode_token, unset_jwt_cookies
from flask_mail import Message
from werkzeug.security import generate_password_hash
from modules.models.User import User
from mongoengine.errors import FieldDoesNotExist, DoesNotExist
from jwt.exceptions import ExpiredSignatureError, DecodeError, InvalidTokenError
from modules.utils.utilFunctions import sendEmail,generate_verification_code
import traceback
auth = Blueprint('auth', __name__)


# class CustError(Exception):
#     status_code = 400
#
#     def __init__(self, message, status_code=None, payload=None):
#         Exception.__init__(self)
#         self.message = message
#         if status_code is not None:
#             self.status_code = status_code
#         self.payload = payload
#
#     def dict_make(self):
#         resp = dict(self.payload or ())
#         resp["message"] = self.message
#         return resp


# @auth.errorhandler(CustError)
# def handle_error(e):
#     response = jsonify(e.dict_make())
#     response.status_code = e.status_code
#     return response


@auth.route("/register", methods=["GET", "POST"])
def register():
    status = True
    if request.method == "POST":
        result = {"status": False}
        try:
            data = request.get_json()
            email = data["email"]
            password = data["password"]
            first_name = data["first_name"]
            last_name = data["last_name"]
            currency = data["currency"]

            ## not needed email & password will be validated on the frontend
            # validate_email(email)
            # if not validate_password(password):
            #     return jsonify({"error": "Password is not valid"}), 400

            db_user = User.objects(email=email)
            # check if the user exists
            if db_user:
                status = False
                return jsonify({"status": status, "error": "User with the email has already existed"}), 409
            
            verification_code = generate_verification_code()
            user_id=uuid.uuid4()
            base_URL = current_app.config['BASE_URL']
            
            mail_object = {'subject': 'EMAT - Registration', 'message': f'Verification Code: "{verification_code}"'}
            sendEmail(mail_object,email)

            newUser = User(user_id=user_id, first_name=first_name,
                           last_name=last_name, email=email, currency = currency,verificationToken=verification_code)

            newUser.hash_password(password)

            newUser.save()
            return jsonify({
                "status": status,
                "message": "signup successfully"
            }), 200

        # except (EmailNotValidError, EmailSyntaxError):
        #     return jsonify({"error": "Email is not valid"}), 400
        except FieldDoesNotExist as e:
            status = False
            return jsonify({"status": status, "error": str(e)}), 400
        # except ValidationError as e:
        #     return jsonify({"error": str(e)}), 400
        except Exception as e:
            status = False
            return jsonify({"status": status, "error": str(e)}), 500


@auth.route("/login", methods=["POST", "GET"])
def login():
    status = True
    if request.method == 'POST':
        try:
            data = request.get_json()
            email = data["email"]
            password = data["password"]

            # check the user and password
            db_user = User.objects.get(email=email)

            if db_user.check_password(password):
                
                session["user_id"] = db_user.user_id
                access_token = create_access_token(identity=db_user.user_id)
                if access_token:
                    return jsonify({
                        "status": status,
                        "user_id": db_user.user_id,
                        "message": "login successfully",
                        "access_token": access_token
                    }), 200
            else:
                status = False
                return jsonify({"status": status, "message": "wrong password"})

        except DoesNotExist:
            status = False
            return jsonify({"status": status, "error": "User with the email not found"}), 404
        except Exception as e:
            print(traceback.format_exc())
            status = False
            return jsonify({"status": status, "error": str(e)}), 500


@auth.route("/logout", methods=["POST"])
def logout():
    status = True
    resp = jsonify({"status": status, "message": "logout successfully"})
    try:
        unset_jwt_cookies(resp)
        session.pop("user_id", None)
        return resp, 200
    except Exception as e:
        status = False
        return jsonify({"status": status, "error": str(e)}), 500


@auth.route("/reset", methods=["POST"])
def resetPasswordWithToken():
    try:
        data = request.get_json()
        email = data["email"]
        if not email:
            return jsonify({"message": "missing email"})

        db_user = User.objects.get(email=email)

        # if not db_user:
        #     raise CustError("User with the email not found", 404)

        reset_token = create_access_token(identity=str(db_user.user_id), expires_delta=datetime.timedelta(hours=12))
        send_email(reset_token, db_user)
        return {"status": "success", "message": "email has been sent", "reset_token": reset_token}, 200

    except DoesNotExist:
        return jsonify({"error": "User with the email not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@auth.route("/reset/<reset_token>", methods=["POST", "GET"])
def resetPassword(reset_token):
    if request.method == "POST":

        try:
            data = request.get_json()
            newPassword = data["password"]
            if not newPassword or not reset_token:
                return jsonify({"message": "The reset password and token are not provided"}), 400

            user_id = decode_token(reset_token)["sub"]
            user = User.objects.get(user_id=user_id)

            if user:
                user.update(password=generate_password_hash(newPassword))
                user.save()
                return {"status": "success", "message": "password reset successfully"}, 200

            else:
                return jsonify("message", "the reset token is not valid"), 400

        except DoesNotExist:
            return jsonify({"error": "User with the email not found"}), 404
        except ExpiredSignatureError:
            return jsonify({"error": "Token has expired"}), 403
        except (DecodeError, InvalidTokenError):
            return jsonify({"error": "Bad token"}), 403
        except Exception as e:
            return jsonify({"error": str(e)}), 500

@auth.route('/verify-user',methods=["GET"])
def verifyUser():
    user_id = request.args.get("user_id")
    verification_token = request.args.get("verification_code")
    result = {"status": False}
    if user_id is not None and verification_token is not None:
        try:
            db_user = User.objects.get_or_404(user_id=user_id)
            user_dict = json.loads(db_user.to_json())
            if user_dict.get("verificationToken",None) == verification_token:
                db_user["isEmailVerified"] = True
                db_user.save()
                result["status"] = True
                result["response"] = "User successfully verified"
            else:
                result["response"] = "Verification Token does not match for user {user_id}"
        except Exception as e:
            traceback_message = traceback.format_exc()
            print(traceback_message)
            result['error'] = f"{e.__class__.__name__} occured"
            result['traceback'] = traceback_message
    else:
        error_messages = []
        if user_id is None:
            error_messages.append("User ID 'user_id' must be present")
        
        if verification_token is None:
            error_messages.append("Verification Token 'verification_code' must be present")
        
        result["response"] = f"Incomplete Query Parameters: {' and '.join(error_messages)} in query parameters"

    return result

# def send_email(reset_token, user):
#     url = request.base_url
#     # user_token = user.get_reset_token()
#     message = Message(subject="Reset Password", recipients=[user.email], sender="noreply@google.com")
#     message.body = f''' 
    
#     A password reset for your account was requested.
#     Please click the link below to change your password.

#     {url + "/" + reset_token}

#     Note that this link is valid for 12 hours. After the time limit has expired, you will have to resubmit the request for a password reset.
    
    
#     '''

#     try:
#         current_app.mail.send(message)
#     except (SMTPAuthenticationError, SMTPServerDisconnected, SMTPException):
#         return jsonify({"error": "Mail server does not work"}), 400
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500


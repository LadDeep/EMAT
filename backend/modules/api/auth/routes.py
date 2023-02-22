import datetime
import re
import uuid
from smtplib import SMTPAuthenticationError, SMTPServerDisconnected, SMTPException
from flask import request, jsonify, Blueprint, current_app
from flask_jwt_extended import create_access_token, decode_token, unset_jwt_cookies
from flask_mail import Message
from werkzeug.security import generate_password_hash
from modules.models.User import User
from mongoengine.errors import ValidationError, FieldDoesNotExist, DoesNotExist
from jwt.exceptions import ExpiredSignatureError, DecodeError, InvalidTokenError
from email_validator import validate_email, EmailNotValidError, EmailSyntaxError

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
    if request.method == "POST":
        try:
            data = request.get_json()
            email = data["email"]
            password = data["password"]
            first_name = data["first_name"]
            last_name = data["last_name"]

            ## not needed email & password will be validated on the frontend
            # validate_email(email)
            # if not validate_password(password):
            #     return jsonify({"error": "Password is not valid"}), 400

            db_user = User.objects(email=email)
            # check if the user exists
            if db_user:
                return jsonify({"error": "User with the email has already existed"}), 409

            newUser = User(user_id=uuid.uuid4(), first_name=first_name,
                           last_name=last_name, email=email)

            newUser.hash_password(password)

            newUser.save()
            return jsonify({
                "status": "success",
                "message": "signup successfully"
            }), 200

        # except (EmailNotValidError, EmailSyntaxError):
        #     return jsonify({"error": "Email is not valid"}), 400
        except FieldDoesNotExist as e:
            return jsonify({"error": str(e)}), 400
        # except ValidationError as e:
        #     return jsonify({"error": str(e)}), 400
        except Exception as e:
            return jsonify({"error": str(e)}), 500


@auth.route("/login", methods=["POST", "GET"])
def login():
    if request.method == 'POST':
        try:
            data = request.get_json();
            email = data["email"]
            password = data["password"]

            # check the user and password
            db_user = User.objects.get(email=email)

            if db_user.check_password(password):

                access_token = create_access_token(identity=db_user.user_id, expires_delta=datetime.timedelta(hours=4))
                if access_token:
                    return jsonify({
                        "status": "success",
                        "message": "login successfully",
                        "access_token": access_token
                    }), 200
            else:
                return jsonify({"message": "wrong password"})

        except DoesNotExist:
            return jsonify({"error": "User with the email not found"}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 500


@auth.route("/logout", methods=["POST"])
def logout():
    resp = jsonify({"status": "success", "message": "logout successfully"})
    try:
        unset_jwt_cookies(resp)
        return resp, 200
    except Exception as e:
        jsonify({"error": str(e)}), 500


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


def send_email(reset_token, user):
    url = request.base_url
    # user_token = user.get_reset_token()
    message = Message(subject="Reset Password", recipients=[user.email], sender="noreply@google.com")
    message.body = f''' 
    
    A password reset for your account was requested.
    Please click the link below to change your password.

    {url + "/" + reset_token}

    Note that this link is valid for 12 hours. After the time limit has expired, you will have to resubmit the request for a password reset.
    
    
    '''

    try:
        current_app.mail.send(message)
    except (SMTPAuthenticationError, SMTPServerDisconnected, SMTPException):
        return jsonify({"error": "Mail server does not work"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# will add some routes about token later

def validate_password(password):
    if not password:
        return False

    if not re.search("[A-Z]", password):
        return False
    if not re.search("[a-z]", password):
        return False
    if not re.search("[0-9]", password):
        return False

    if len(password) < 8 or len(password) > 20:
        return False

    return True

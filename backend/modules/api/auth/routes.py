import datetime
import uuid
import json
from flask import request, jsonify, Blueprint, session
from flask_jwt_extended import create_access_token, decode_token, unset_jwt_cookies
from werkzeug.security import generate_password_hash
from modules.models.User import User
from mongoengine.errors import FieldDoesNotExist, DoesNotExist
from jwt.exceptions import ExpiredSignatureError, DecodeError, InvalidTokenError
from modules.utils.utilFunctions import send_email,generate_verification_code
import traceback
auth = Blueprint('auth', __name__)




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
            monthly_budget_amount = data["monthly_budget_amount"]
            warning_budget_amount = data["warning_budget_amount"]
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
            flag = True
            unique_user_id = None
            while flag:
                user_id=uuid.uuid4()
                user_obj = User.objects(user_id=user_id)
                if not user_obj:
                    unique_user_id = user_id
                    flag = False
            
            mail_object = {'subject': 'EMAT - Registration', 'message': f'Verification Code: "{verification_code}"'}
            send_email(mail_object,email)

            new_user = User(user_id=unique_user_id, first_name=first_name,
                           last_name=last_name, email=email, currency = currency,verificationToken=verification_code,monthly_budget_amount=monthly_budget_amount,warning_budget_amount=warning_budget_amount)

            new_user.hash_password(password)

            new_user.save()
            return jsonify({
                "user_id": user_id,
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
            result = authenticate_user(db_user,password)
            return result
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
def reset_password_with_token():
    try:
        data = request.get_json()
        email = data["email"]
        if not email:
            return jsonify({"message": "missing email"})

        db_user = User.objects.get(email=email)
        # if not db_user:
        #     raise CustError("User with the email not found", 404)

        reset_token = create_access_token(identity=str(db_user.user_id), expires_delta=datetime.timedelta(hours=12))
        send_email({"subject":"EMAT - password reset","message":f"RESET_TOKEN -{reset_token}"},email)
        return {"status": True, "message": "email has been sent", "reset_token": reset_token}, 200

    except DoesNotExist:
        return jsonify({"error": "User with the email not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@auth.route("/reset/<reset_token>", methods=["POST"])
def reset_password(reset_token):
    if request.method == "POST":
        try:
            data = request.get_json()
            new_password = data["password"]
            if not new_password or not reset_token:
                return jsonify({"message": "The reset password and token are not provided"}), 400

            user_id = decode_token(reset_token)["sub"]
            user = User.objects.get(user_id=user_id)

            if user:
                user.update(password=generate_password_hash(new_password))
                user.save()
                return {"status": True, "message": "password reset successfully"}, 200

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
def verify_user():
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
                result["response"] = {"verified": True,"message":"User successfully verified"}
            else:
                result["response"] = {"verified": False,"message":"Verification Token does not match for user {user_id}"}
                
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


def authenticate_user(db_user,password):
    result = {"status": True,"user_id": db_user.user_id}
    if db_user.check_password(password):
        if db_user.isEmailVerified is True:
            session["user_id"] = db_user.user_id
            access_token = create_access_token(identity=db_user.user_id)
            if access_token:    
                result["message"]= "login successfully"
                result["access_token"] =  access_token
        else:
            result["message"] = "User is not Verified"
    else:
        result["status"] = False
        result["message"] = "wrong password"
        
    return result
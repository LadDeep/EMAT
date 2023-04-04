from flask import Blueprint, jsonify, request

from modules.models import User
from flask_jwt_extended import jwt_required, get_jwt_identity
from mongoengine.errors import ValidationError, OperationError
import traceback

profile = Blueprint('profile', __name__)

# get user profile
@profile.route("/user", methods=["GET"])
@jwt_required()
def getProfile():

    try:

        userId = get_jwt_identity()
        user = User.objects(user_id = userId)
        if not user:
            return jsonify({"status": False, "error": "the user does not exist"}), 404
    
        return jsonify({"status": True, "message": user}), 200
    
    except OperationError as e:
        return jsonify({"status": False, "error": str(e)}), 401
    except Exception as e:
        return jsonify({"status": False, "error": str(e)}), 500


@profile.route("/update", methods=["PUT"])
@jwt_required()
def update_user():
    content_type = request.headers.get('Content-Type')
    user_id_verified = get_jwt_identity()
    result = {"status": False}
    if content_type == 'application/json':
        if user_id_verified:
            try:
                user = User.objects.get_or_404(user_id = user_id_verified)
                updatable_fields = ['first_name','last_name','currency','monthly_budget_amount','warning_budget_amount']
                json_data = request.json
                json_list_keys = list(json_data.keys())

                keys_to_update = [x for x in json_list_keys if x in updatable_fields]

                for key in keys_to_update:
                    user[key] = json_data[key]
                
                user.save()
                result['status'] = True
                result['response'] = f"User Details for {user_id_verified} updated"
            except Exception as e:
                traceback_message = traceback.format_exc()
                print(traceback_message)
                result['error'] = f"{e.__class__.__name__} occured"
                result['traceback'] = traceback_message
        else:
            result['response'] = 'User session Expired'
    else:
        result['response'] = f'Unsupported Content Type in Headers: {content_type} Supported: "application/json"'

    return result


# delete user
@profile.route("/delete_user")
@jwt_required()
def deleteUser():

    try:
        user = User.objects(user_id=get_jwt_identity())

        if not user:
            return jsonify({"status": False, "error": "the user does not exist"}), 401


        user.delete()
        return jsonify({"status": True, "message": "the user has been deleted successfully"}), 200
    
    except ValidationError as e:
        return jsonify({"status": False, "error": str(e)}), 403
    except Exception as e:
        return jsonify({"status": False, "error": str(e)}), 500


@profile.route("/email", methods=["GET"])
def getUserEmail():

    try:
        data = request.get_json()
        userId = data["user_id"]
        user = User.objects(user_id=userId)

        return jsonify({"status": True, "message": user.email}), 200
    except Exception as e:
        return jsonify({"status": False, "error": str(e)}), 500

@profile.route("/fullname", methods=["GET"])
def getFullName():

    try:
        data = request.get_json()
        userId = data["user_id"]
        user = User.objects(user_id=userId)

        return jsonify({"status": True, "message": user.first_name + " " + user.last_name}), 200
    
    except Exception as e:
        return jsonify({"status": False, "error": str(e)}), 500
    

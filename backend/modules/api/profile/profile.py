from flask import Blueprint, jsonify, request

from backend.modules.models import User
from flask_jwt_extended import jwt_required, get_jwt_identity
from mongoengine.errors import ValidationError, OperationError


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

# update user email
@profile.route("/update_email", methods=["PUT"])
@jwt_required()
def update_email():

    try:

        data = request.get_json()
        newEmail = data["email"]

        if newEmail == "":
            return jsonify({"status": False, "error": "the provided email is empty"}), 401
        elif User.objects(email=newEmail):
            return jsonify({"status": False, "error": "the email has already existed"}), 409
    
    # here @Nitesh will do the email verification
    # if not validate_email:
    #     return jsonify({"status": False, "error": "the email verfied is failed"}), 401

    
        user = User.objects(user_id=get_jwt_identity())
        user.update(email = newEmail)
        user.save()
        return jsonify({
            "status": True,
            "message": "Email updated successfully"
        }), 200
    
    except OperationError as e:
        return jsonify({"status": False, "error": str(e)}), 401
    except Exception as e:
        jsonify({"status": False, "error": str(e)}), 500

# update last_name 
@profile.route("/update_last_name", methods=["PUT"])
@jwt_required()
def update_last_name():

    try:

        data = request.get_json()
        new_last_name = data["last_name"]

        if new_last_name == "":
            return jsonify({"status": False, "error": "the provided user last name is empty"}), 401

        user = User.objects(user_id=get_jwt_identity())
        if user.last_name == new_last_name:
            return jsonify({"status": False, "error": "the last name has already existed"}), 409

        user.update(last_name = new_last_name)
        user.save()
        return jsonify({
            "status": True,
            "message": "Last name updated successfully"
        }), 200
    
    except OperationError as e:
        return jsonify({"status": False, "error": str(e)}), 401
    except Exception as e:
        jsonify({"status": False, "error": str(e)}), 500

# update first_name 
@profile.route("/update_first_name", methods=["PUT"])
@jwt_required()
def update_first_name():

    try:

        data = request.get_json()
        new_first_name = data["first_name"]

        if new_first_name == "":
            return jsonify({"status": False, "error": "the provided user first name is empty"}), 401

        user = User.objects(user_id=get_jwt_identity())
        if user.first_name == new_first_name:
            return jsonify({"status": False, "error": "the first name has already existed"}), 409


        user.update(first_name = new_first_name)
        user.save()
        return jsonify({
            "status": True,
            "message": "First name updated successfully"
        }), 200
    
    except OperationError as e:
        return jsonify({"status": False, "error": str(e)}), 401
    except Exception as e:
        jsonify({"status": False, "error": str(e)}), 500

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

    

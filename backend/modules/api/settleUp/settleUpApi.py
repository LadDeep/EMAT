from flask import Blueprint, jsonify, request

from modules.models.User import User
from modules.models.Group import Group
from flask_jwt_extended import jwt_required, get_jwt_identity
from mongoengine.errors import ValidationError, OperationError
import traceback
import json
from modules.utils.utilFunctions import sendEmail
settleUp = Blueprint('settleUp', __name__)

# get user profile
@settleUp.route("", methods=["GET"])
@jwt_required()
def whoOwesWhat():
    result = {"status": False}
    user_id_verified = get_jwt_identity()
    group_id = request.args.get("group_id")
    pipeline = [{ "$unwind": "$expenses" }, { "$group": { "_id": "$expenses.spent_by", "total": { "$sum": "$expenses.amount" } } }]
    if group_id:
        try:
            pipeline.insert(0,{ "$match": { "group_id": group_id } })
            group_stats = Group.objects.aggregate(*pipeline)
            group_stats_json = [dict(doc) for doc in group_stats]
            group_data = Group.objects.get_or_404(group_id=group_id)
            participants = group_data.participants
            user_spent = [x for x in group_stats_json if x["_id"] == user_id_verified]
            other_spent = [x for x in group_stats_json if x["_id"] != user_id_verified]
            
            print(group_stats_json)
            if len(user_spent) > 0:
                user_spent = user_spent[0]
            else:
                user_spent  = {"user_id": user_id_verified, "total": 0}

            for other_expense in other_spent:
                other_expense["total"] = (user_spent["total"]/len(participants)) - (other_expense["total"]/len(participants))
            
            result["status"] = True
            result["response"] = other_spent
        except Exception as e:
            traceback_message = traceback.format_exc()
            print(traceback_message)
            result['error'] = f"{e.__class__.__name__} occured"
            result['traceback'] = traceback_message
    else:
        result["response"] = "Incomplete Query Parameters: 'group_id'"
    
    return result

@settleUp.route("/notify",methods=["POST"])
@jwt_required()
def notify():
    result = {"status": False}
    content_type = request.headers.get('Content-Type')
    user_id_verified = get_jwt_identity()
    json_data = request.json
    if content_type == 'application/json':
        try:
            user = User.objects.get_or_404(user_id=user_id_verified)
            group_id = json_data.get("group_id",None)
            notify_users = json_data.get("notify_users",[])
            if group_id is not None and len(notify_users) > 0:
                group = Group.objects.get_or_404(group_id=group_id)
                group = json.loads(group.to_json())
                notify_user_ids = [x["user_id"] for x in notify_users]
                notify_user_objects = User.objects.filter(user_id__in=notify_user_ids)
                mail_object = {'subject': 'EMAT - Notify User for payment'}
                for notify_user_obj in notify_user_objects:
                    notify_user_obj = json.loads(notify_user_obj.to_json())
                    index = notify_user_ids.index(notify_user_obj.get("user_id"))
                    obj = notify_users[index]
                    mail_object["message"] = f'You owe amount {obj.get("amount","undefined")} {notify_user_obj.get("currency","undefined")} to {user.first_name} in {group.get("group_name","undefined")}'
                    sendEmail(mail_object,notify_user_obj.email)
            
            result["status"] = True
            result["response"] = "Users notified"
        except Exception as e:
            traceback_message = traceback.format_exc()
            print(traceback_message)
            result['error'] = f"{e.__class__.__name__} occured"
            result['traceback'] = traceback_message

        else:
            if group_id is None:
                result["response"] = "Group ID (group_id) not set in request body"
            elif len(notify_users) == 0:
                result["response"] = "Notify User Array (notify_users) cannot be empty in request body"
            
                
    else:
        result["response"] = f"Unsupported Content-Type: {content_type}"

    return result
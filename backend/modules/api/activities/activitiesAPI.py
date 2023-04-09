from flask import Blueprint,request
from flask_jwt_extended import jwt_required, get_jwt_identity
from modules.models.Group import Group
from modules.models.User import User
import json
import traceback

activities_bp = Blueprint('activities',__name__)

@activities_bp.route('/list',methods=['GET'])
@jwt_required()
def list_user_activities():
    user_id_verified = get_jwt_identity()
    result = {"status": False}
    status = None

    if user_id_verified:
        try:
            groups = Group.objects.filter(participants__in=[user_id_verified])
            groups = [json.loads(group.to_json()) for group in groups]
            userObject = User.objects.get_or_404(user_id=user_id_verified)
            response = create_group_activity_response(groups)
            
            settleUpList = [json.loads(x.to_json()) for x in userObject.settleUp]
            for settleUpObject in settleUpList:
                group_object = next(filter(lambda item: item['group_id'] == settleUpObject['group_id'], groups), None)
                
                if group_object is not None:
                    settleUpObject['group_name'] = group_object['group_name']
                else:
                    settleUpObject['group_name'] = group_object['group_id']

            result['response'] = {'groups': response, 'settleUps': settleUpList}
            result['status'] = True    
            status = 200
        except Exception as e:
            traceback_message = traceback.format_exc()
            print(traceback_message)
            result['error'] = f"{e.__class__.__name__} occured"
            result['traceback'] = traceback_message
            status = 500
    
    return result,status


def create_group_activity_response(groups):
    response = []
    for group in groups:
        for expense in group["expenses"]:
            activity = {}
            activity["group_name"] = group["group_name"]
            activity["group_id"] = group["group_id"]
            for key in list(expense.keys()):
                activity[key] = expense[key]
            response.append(activity)
        
    return response
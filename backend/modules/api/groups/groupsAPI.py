from flask import Blueprint,request
from flask_jwt_extended import jwt_required, get_jwt_identity
from modules.models.Group import Group
from modules.models.User import User
from modules.utils.utilFunctions import createObjectWithRequiredFields
import json
import traceback


group = Blueprint('group',__name__)

@group.route("/register",methods=['POST'])
@jwt_required()
def registerGroup():
    content_type = request.headers.get('Content-Type')
    user_id_verified = get_jwt_identity()
    result = {"status": False}
    status = None
    if content_type == 'application/json':
        if user_id_verified:
            try:
                json_data = request.json
                required_fields = ['group_name','group_currency']
                participants = json_data.get("participants",None)
                group = Group()
                description = json_data.get("group_description",None)
                if description is not None:
                    group.group_description = description
                
                if participants is not None:
                    group.participants = participants
                
                result = createObjectWithRequiredFields(group,required_fields,json_data,result) 
                status = 201
            except Exception as e:
                traceback_message = traceback.format_exc()
                print(traceback_message)
                result['error'] = f"{e.__class__.__name__} occured"
                result['traceback'] = traceback_message
                status = 500
            
    else:
        result["error"] = "Unsupported Content-Type in headers"
        status = 415
    return result,status

@group.route("/list",methods=['GET'])
@jwt_required()
def listGroups():
    result = {"status": True}
    user_id_verified = get_jwt_identity()
    status = None

    if user_id_verified:
        try:
            user = User.objects(user_id=user_id_verified).first()
            userObject = json.loads(user.to_json())
            # print(userObject.keys())
            email = userObject.get("email",None)
            if email is not None:
                groups = Group.objects.filter(participants__in=[email])
                groups = [json.loads(group.to_json()) for group in groups]
                result["response"] = groups
                status = 200
            else:
                result["status"] = False
                result["error"] = f"Email Field does not exist against User ID: {user_id_verified}"
                status=404

        except Exception as e:
            traceback_message = traceback.format_exc()
            print(traceback_message)
            result['error'] = f"{e.__class__.__name__} occured"
            result['traceback'] = traceback_message
            status = 500
       
    
    return result,status
        

@group.route("/delete",methods=['POST'])
@jwt_required()
def deleteGroup():
    content_type = request.headers.get('Content-Type')
    user_id_verified = get_jwt_identity()

    result = {"status": False}
    status = None
    
    if content_type == 'application/json':
        
        if user_id_verified:
            try:
                json_data = request.json
                group_id = json_data.get('group_id',None)
                if group_id is not None:
                    group = Group.objects.filter(group_id=group_id)
                    group.delete()
                    result["status"] = True
                    result["response"] = f"{group_id} Deleted"
                    status = 200
                else:
                    result["error"] = "Group ID cannot be null in request body"
                    status = 400
            except Exception as e:
                traceback_message = traceback.format_exc()
                print(traceback_message)
                result['error'] = f"{e.__class__.__name__} occured"
                result['traceback'] = traceback_message
                status = 500          
    else:
        result["error"] = "Unsupported Content-Type in headers"
        status = 415
    return result,status

@group.route("/update",methods=['PUT'])
@jwt_required()
def updateGroup():
    content_type = request.headers.get('Content-Type')
    user_id_verified = get_jwt_identity()
    result = {"status": False}
    status = None
    if content_type == 'application/json':
        if user_id_verified:
            try:
                json_data = request.json
                required_key = 'group_id'
                json_keys = list(json_data.keys())
                if required_key in json_keys:
                    group_id = json_data[required_key]
                    group = Group.objects.get_or_404(group_id=group_id)
                    keys_to_update = [x for x in json_keys if x != required_key]
                    for key in keys_to_update:
                        group[key] = json_data[key]
                    
                    group.save()
                    result["status"] = True
                    result["response"] = f"Group {group_id} updated"
                    status = 200
                else:
                    result["error"] = "Group ID cannot be null in request body" 
                    status = 400
            except Exception as e:
                traceback_message = traceback.format_exc()
                print(traceback_message)
                result['error'] = f"{e.__class__.__name__} occured"
                result['traceback'] = traceback_message
                status = 500   
    else:
        result["error"] = "Unsupported Content-Type in headers"
        status = 415
    
    return result,status

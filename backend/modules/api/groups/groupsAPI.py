from flask import Blueprint,request,jsonify
from modules.models.Group import Group
from modules.models.User import User
from modules.lib.utilFunctions import createObjectWithRequiredFields
import json


group = Group()
print(group.__class__.__name__)
group = Blueprint('group',__name__)

@group.route("/register",methods=['POST'])
def registerGroup():
    content_type = request.headers.get('Content-Type')
    result = {"status": False}
    status = None
    if content_type == 'application/json':
        json = request.json
        required_fields = ['group_name','group_currency']
        participants = json.get("participants",None)
        group = Group()
        description = json.get("group_description",None)
        if description is not None:
            group.group_description = description
        
        if participants is not None:
            group.participants = participants
        
        result = createObjectWithRequiredFields(group,required_fields,json,result) 
        status = 201   
    else:
        result["error"] = "Unsupported Content-Type in headers"
        status = 415
    return result,status

@group.route("/list",methods=['GET'])
def listGroups():
    user_id = request.args.get("user_id",None)
    result = {"status": True}
    status = None
    if user_id is not None:
        # print(user_id)
        user = User.objects(user_id=user_id).first()
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
            result["error"] = f"Email Field does not exist against User ID: {user_id}"
    else:
        result["status"] = False
        result["error"] = f"user_id Query Parameter does not exist"

    return result
        

@group.route("/delete",methods=['POST'])
def deleteGroup():
    content_type = request.headers.get('Content-Type')
    result = {"status": False}
    status = None
    if content_type == 'application/json':
        json = request.json
        group_id = json.get('group_id',None)
        if group_id is not None:
            group = Group.objects.filter(group_id=group_id)
            group.delete()
            result["status"] = True
            result["response"] = f"{group_id} Deleted"
        else:
            result["error"] = "Group ID cannot be null in request body"
        
    else:
        result["error"] = "Unsupported Content-Type in headers"
        
    return result

@group.route("/update",methods=['PUT'])
def updateGroup():
    content_type = request.headers.get('Content-Type')
    result = {"status": False}
    status = None
    if content_type == 'application/json':
        json = request.json
        required_key = 'group_id'
        json_keys = list(json.keys())
        if required_key in json_keys:
            group_id = json[required_key]
            group = Group.objects.get_or_404(group_id=group_id)
            keys_to_update = [x for x in json_keys if x != required_key]
            for key in keys_to_update:
                group[key] = json[key]
            
            group.save()
            result["status"] = True
            result["response"] = f"Group {group_id} updated"
        else:
            result["error"] = "Group ID cannot be null in request body" 
    else:
        result["error"] = "Unsupported Content-Type in headers"
        
    return result

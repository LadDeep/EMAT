from flask import Blueprint,request,abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from modules.models.Group import Group
from modules.models.User import User
from modules.utils.utilFunctions import createObjectWithRequiredFields,generate_verification_code,sendEmail
import json
import traceback
import uuid

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
                flag = True
                unique_group_id = None
                while flag:
                    group_id=uuid.uuid4()
                    group_obj = Group.objects(group_id=group_id)
                    if not group_obj:
                        unique_group_id = group_id
                        flag = False
                group.group_id=unique_group_id
                joiningToken = generate_verification_code()
                description = json_data.get("group_description",None)
                group.created_by = user_id_verified
                group.joiningToken = joiningToken
                if description is not None:
                    group.group_description = description
                
                if participants is not None:
                    
                    users = User.objects(email__in=participants)
                    users = [json.loads(x.to_json()) for x in users]

                    emails_registered = [x['email'] for x in users if x.get('email') is not None]
                    email_not_registered = [x for x in participants if x not in emails_registered]
                    created_user_object = User.objects.get_or_404(user_id=user_id_verified)
                    created_user_object = json.loads(created_user_object.to_json())
                    if created_user_object is not None:
                        created_email = created_user_object.get("email",None)
                        if created_email is not None:
                            registered_email_object = {"subject": f"{created_email} invited you to {json_data.get('group_name','Group')} on EMAT","message":f"Group Verification Code: {joiningToken}"}
                            for email in emails_registered:
                                print(registered_email_object)                    
                                sendEmail(registered_email_object,email)
                            
                            for email in email_not_registered:
                                print(registered_email_object)                    
                                sendEmail(registered_email_object,email)
                        
                    participants = [x['user_id'] for x in users if x.get('user_id') is not None]
                    participants.append(user_id_verified)
                    participants = list(set(participants))
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
            groups = Group.objects.filter(participants__in=[user_id_verified])
            groups = [json.loads(group.to_json()) for group in groups]
            user_id_vo = User.objects.get_or_404(user_id=user_id_verified)
            user_id_vo = json.loads(user_id_vo.to_json())
            for group in groups:
                user_names = User.objects.filter(user_id__in=group['participants'])
                user_names = [json.loads(x.to_json()) for x in user_names]
                group_object = next(filter(lambda x: x['group_id'] == group.get('group_id'),user_id_vo.get('settleUp',[])),None)
                
                print(user_id_verified)
                print(group.get('group_id'))
                spent = sum([expense.get("amount",0) for expense in group.get("expenses",[]) if expense.get('spent_by',None) == user_id_verified])
                owed = sum([expense.get("amount",0) for expense in group.get("expenses",[]) if expense.get('spent_by',None) != user_id_verified])
                
                spent -= spent/len(group.get('participants'))
                owed = owed/len(group.get('participants'))
                group['standing_amount'] = spent - owed  
                if group_object is not None:
                    if group_object.get('settling') is True:
                        group['standing_amount'] -= abs(group_object.get('amount',0))
                    elif group_object.get('settler') is True:
                        group['standing_amount'] += abs(group_object.get('amount',0))
                
                  

                for expense in group['expenses']:
                    user_object = next(filter(lambda x: x['user_id'] == expense['spent_by'],user_names),None)
                    expense['user_name'] = f"{user_object['first_name']} {user_object['last_name']}"

            result["response"] = groups
            status = 200
           

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

@group.route("/stats",methods=['GET'])
@jwt_required()
def getGroupStats():
    result = {"status": False}
    group_id = request.args.get("group_id")
    pipeline = [{ "$unwind": "$expenses" }, { "$group": { "_id": "$expenses.spent_by", "total": { "$sum": "$expenses.amount" } } }]
    if group_id:
        try:
            pipeline.insert(0,{ "$match": { "group_id": group_id } })
            group_stats = Group.objects.aggregate(*pipeline)
            group_stats_json = [dict(x) for x in group_stats]
            group = Group.objects.get_or_404(group_id=group_id)
            user_ids = [x["_id"] for x in group_stats_json]

            user_ids.extend(group.participants)
            user_ids = list(set(user_ids))
            
            for user_id in user_ids:
                spent_obj = next(filter(lambda item: item['_id'] == user_id, group_stats_json), None)
                if spent_obj is None:
                    group_stats_json.append({"_id":user_id,"total": 0})

            
            result["status"] = True
            if len(user_ids) > 0:
                users = User.objects.filter(user_id__in=user_ids)
                users = [json.loads(x.to_json()) for x in users]
                keys_needed = ['first_name','last_name','email']
                for user in users:
                    group_index = next((index for (index,d) in enumerate(group_stats_json) if d['_id'] == user['user_id']),None)
                    if group_index is not None:
                        for key in keys_needed:
                            group_stats_json[group_index][key] = user[key]
                
                result["response"] = {"max": max(group_stats_json,key=lambda x: x['total']),"min":min(group_stats_json,key=lambda x: x['total'])}
            else:
                result["response"] = f"No Expenses in group: {group_id}"
        except Exception as e:
            traceback_message = traceback.format_exc()
            print(traceback_message)
            result['error'] = f"{e.__class__.__name__} occured"
            result['traceback'] = traceback_message
    else:
        result["response"] = f"Incomplete Query Parameters: 'group_id' is missing"

    return result
            
@group.route("/join-group",methods=['GET'])
@jwt_required()
def joinGroup():
    user_id_verified = get_jwt_identity()
    result = {"status": False}
    verification_token = request.args.get("verification_code")

    if user_id_verified:
        if verification_token is not None:
            try:
                group_array = Group.objects.filter(joiningToken=verification_token)
                if not group_array:
                    abort(404)
                else:
                    group = group_array[0]
                    if user_id_verified not in group.participants:
                        group.participants.append(user_id_verified)
                        group.save()
                    else:
                        print(f"User Exists: {user_id_verified} in {group.participants}")
                    
                    result['status'] = True
                    result['response'] = f'User {user_id_verified} has joined group {group.name}'
            except Exception as e:
                traceback_message = traceback.format_exc()
                print(traceback_message)
                result['error'] = f"{e.__class__.__name__} occured"
                result['traceback'] = traceback_message

        else:
            result['status'] = False
            result['response'] = "Verification Token: verification_code should be set in query parameters"
    
    return result

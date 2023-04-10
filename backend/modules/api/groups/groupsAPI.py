from flask import Blueprint,request,abort,current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from modules.models.Group import Group
from modules.models.User import User
from modules.utils.utilFunctions import create_object_with_required_fields,generate_verification_code,send_email
import json
import traceback
import uuid

group = Blueprint('group',__name__)

@group.route("/register",methods=['POST'])
@jwt_required()
def register_group():
    """
    Creates a group with participants
    
    Returns:
        A python dictionary containing status & a response key-value pair on a successful response
    """
    content_type = request.headers.get('Content-Type')
    user_id_verified = get_jwt_identity()
    result = {"status": False}
    status = None
    if content_type == current_app.config["JSON-CONTENT-TYPE"]:
        if user_id_verified:
            try:
                json_data = request.json
                required_fields = ['group_name','group_currency']
                participants = json_data.get("participants",None)
                group = Group()
                flag = True
                unique_group_id = None

                # Below While Loop is needed to ensure uuids are unique 
                # tried with uuid1 and uuid4, since uuid1 is based on machine time, 
                # went ahead with uuid4 as characters in it are random

                while flag:
                    group_id=uuid.uuid4()
                    group_obj = Group.objects(group_id=group_id)
                    if not group_obj:
                        unique_group_id = group_id
                        flag = False

                group.group_id=unique_group_id
                joining_token = generate_verification_code()
                description = json_data.get("group_description",None)
                group.created_by = user_id_verified
                group.joiningToken = joining_token
                if description is not None:
                    group.group_description = description
                
                if participants is not None:
                    
                    users = User.objects(email__in=participants)
                    users = [json.loads(x.to_json()) for x in users]
                    # invites by email all users in the group that are participants
                    invite_users_to_join_group(users,participants,user_id_verified,json_data,joining_token)

                    # participants initially storing email of users is converted to user_ids
                    participants = [x['user_id'] for x in users if x.get('user_id') is not None]
                    participants.append(user_id_verified)
                    # make sure that each element in the participants array is unique
                    participants = list(set(participants))
                    group.participants = participants
                
                result = create_object_with_required_fields(group,required_fields,json_data,result) 
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
def list_groups():
    """
    List all group documents for a user
    
    Returns:
        A python dictionary containing status & a response key-value pair on a successful response
    """
    result = {"status": True}
    user_id_verified = get_jwt_identity()
    status = None

    if user_id_verified:
        try:
            # get all groups for a user based on user_id (that is decoded from the JWT token)
            groups = Group.objects.filter(participants__in=[user_id_verified])
            groups = [json.loads(group.to_json()) for group in groups]

            # fetch the user document that contains the settle Up information
            user_id_vo = User.objects.get_or_404(user_id=user_id_verified)
            user_id_vo = json.loads(user_id_vo.to_json())
            for group in groups:
                user_names = User.objects.filter(user_id__in=group['participants'])
                user_names = [json.loads(x.to_json()) for x in user_names]

                # get the settle Up object based on comparison between group_id
                group_object = next(filter(lambda x: x['group_id'] == group.get('group_id'),user_id_vo.get('settleUp',[])),None)
                
                print(user_id_verified)
                print(group.get('group_id'))

                # spent amounts: those that are spent by the user
                spent = sum([expense.get("amount",0) for expense in group.get("expenses",[]) if expense.get('spent_by',None) == user_id_verified])
                # owed amounts: those that are spent by other users
                owed = sum([expense.get("amount",0) for expense in group.get("expenses",[]) if expense.get('spent_by',None) != user_id_verified])
                
                # calculation logic for standing amount
                spent -= spent/len(group.get('participants'))
                owed = owed/len(group.get('participants'))
                group['standing_amount'] = spent - owed  

                if group_object is not None:
                    # account for settle up information
                    if group_object.get('settling') is True:
                        group['standing_amount'] -= abs(group_object.get('amount',0))
                    elif group_object.get('settler') is True:
                        group['standing_amount'] += abs(group_object.get('amount',0))
                
                  

                for expense in group['expenses']:
                    # gets the user object based on comparison between user_id & settleby
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
def delete_group():
    """
    Deletes a group
    
    Returns:
        A python dictionary containing status & a response key-value pair on a successful response
    """
    content_type = request.headers.get('Content-Type')
    user_id_verified = get_jwt_identity()

    result = {"status": False}
    status = None
    
    if content_type == current_app.config["JSON-CONTENT-TYPE"]:
        
        if user_id_verified:
            try:
                json_data = request.json
                group_id = json_data.get('group_id',None)
                if group_id is not None:
                    # gets the group object based on group_id
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
def update_group():
    """
    Updates a group
    
    Returns:
        A python dictionary containing status & a response key-value pair on a successful response
    """
    content_type = request.headers.get('Content-Type')
    user_id_verified = get_jwt_identity()
    result = {"status": False}
    status = None
    if content_type == current_app.config["JSON-CONTENT-TYPE"]:
        if user_id_verified:
            try:
                json_data = request.json
                required_key = 'group_id'
                json_keys = list(json_data.keys())
                # checks if group_id is in request body
                if required_key in json_keys:
                    group_id = json_data[required_key]
                    # gets group data based on group_id
                    group = Group.objects.get_or_404(group_id=group_id)
                    # all keys except group_id can be updated from the request body
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
def get_group_stats():
    """
    Gets the most spending & least spending user details for a group
    
    Returns:
        A python dictionary containing status & a response key-value pair on a successful response
    """
    result = {"status": False}
    group_id = request.args.get("group_id")
    pipeline = [{ "$unwind": "$expenses" }, { "$group": { "_id": "$expenses.spent_by", "total": { "$sum": "$expenses.amount" } } }]
    if group_id:
        try:
            pipeline.insert(0,{ "$match": { "group_id": group_id } })
            # runs an aggregate pipeline that unwinds the expenses sub array as root and
            # then for each spent_by (user_id) key all expense amounts are summed
            group_stats = Group.objects.aggregate(*pipeline)
            group_stats_json = [dict(x) for x in group_stats]
            group = Group.objects.get_or_404(group_id=group_id)
            user_ids = [x["_id"] for x in group_stats_json]

            user_ids.extend(group.participants)
            user_ids = list(set(user_ids))
            
            # gets the expense object for all user_ids in the group
            # if a user_id from participants is not present in the aggregate result,
            # that is appended with sum as 0
            for user_id in user_ids:
                spent_obj = next(filter(lambda item: item['_id'] == user_id, group_stats_json), None)
                if spent_obj is None:
                    group_stats_json.append({"_id":user_id,"total": 0})

            
            result["status"] = True
            if len(user_ids) > 0:
                group_stats_json = set_user_details_in_group_stats(user_ids,group_stats_json)
                
                result["response"] = {"max": max(group_stats_json,key=lambda x: x['total']),"min":min(group_stats_json,key=lambda x: x['total'])}
            else:
                result["response"] = f"No Expenses in group: {group_id}"
        except Exception as e:
            traceback_message = traceback.format_exc()
            print(traceback_message)
            result['error'] = f"{e.__class__.__name__} occured"
            result['traceback'] = traceback_message
    else:
        result["response"] = "Incomplete Query Parameters: 'group_id' is missing"

    return result
            
@group.route("/join-group",methods=['GET'])
@jwt_required()
def join_group():
    """
    Allows a user to join a group based on verification_token that is sent via E-mail on group registration
    
    Returns:
        A python dictionary containing status & a response key-value pair on a successful response
    """
    user_id_verified = get_jwt_identity()
    result = {"status": False}
    verification_token = request.args.get("verification_code")

    if user_id_verified:
        if verification_token is not None:
            try:
                # gets the group object based on verification_token
                group_array = Group.objects.filter(joiningToken=verification_token)
                if not group_array:
                    abort(404)
                
                group = group_array[0]
                # adds the user_id to participants array in the group if not present
                if user_id_verified not in group.participants:
                    group.participants.append(user_id_verified)
                    group.save()
                else:
                    print(f"User Exists: {user_id_verified} in {group.participants}")
                
                result['status'] = True
                result['response'] = f'User {user_id_verified} has joined group {group.group_name}'
            except Exception as e:
                traceback_message = traceback.format_exc()
                print(traceback_message)
                result['error'] = f"{e.__class__.__name__} occured"
                result['traceback'] = traceback_message

        else:
            result['status'] = False
            result['response'] = "Verification Token: verification_code should be set in query parameters"
    
    return result


def invite_users_to_join_group(users,participants,user_id_verified,json_data,joining_token):
    """
    Gets the most spending & least spending user details for a group

    Args:
        users: user object array from mongoDB
        participants: email_ids of all people to be added to the group coming from the request body
        user_id_verified: user_id of user that makes the API call
        json_data: request body
        joining_token: generated joining token
    
    Returns:
        A python dictionary containing status & a response key-value pair on a successful response
    """

    # filters all emails that are present as well as not present in EMAT
    emails_registered = [x['email'] for x in users if x.get('email') is not None]
    email_not_registered = [x for x in participants if x not in emails_registered]
    # gets the user object of the user that makes the API call (creates the group)
    created_user_object = User.objects.get_or_404(user_id=user_id_verified)
    created_user_object = json.loads(created_user_object.to_json())

    if created_user_object is not None:
        created_email = created_user_object.get("email",None)
        if created_email is not None:
            # sends email to all registered as well as non-registered users
            registered_email_object = {"subject": f"{created_email} invited you to {json_data.get('group_name','Group')} on EMAT","message":f"Group Verification Code: {joining_token}"}
            for email in emails_registered:
                print(registered_email_object)                    
                send_email(registered_email_object,email)
            
            for email in email_not_registered:
                print(registered_email_object)                    
                send_email(registered_email_object,email)

def set_user_details_in_group_stats(user_ids,group_stats_json):
    """
    Gets the most spending & least spending user details for a group

    Args:
        user_ids: list of user_ids (participants) in a group
        group_stats_json: sum of all expenses for all user_ids in a group
    
    Returns:
        A python dictionary containing status & a response key-value pair on a successful response
    """
    users = User.objects.filter(user_id__in=user_ids)
    users = [json.loads(x.to_json()) for x in users]
    keys_needed = ['first_name','last_name','email']
    for user in users:
        group_index = next((index for (index,d) in enumerate(group_stats_json) if d['_id'] == user['user_id']),None)
        # getting index if a user_id is matched in group_stats_json and setting each key in keys_needed
        if group_index is not None:
            for key in keys_needed:
                group_stats_json[group_index][key] = user[key]
    
    return group_stats_json
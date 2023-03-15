from flask import Blueprint,request
from modules.models.User import User

users = Blueprint('users',__name__)

@users.route("/register",methods=['POST'])
def register():
    content_type = request.headers.get('Content-Type')
    result = {"status": False}
    required_fields = ['email','first_name','last_name']
    if content_type == 'application/json':
        json = request.json
        result = createObjectWithRequiredFields(User(),required_fields,json,result)
             
    elif content_type == 'application/x-www-form-urlencoded':
        form = request.form.to_dict()
        result = createObjectWithRequiredFields(User(),required_fields,form,result) 
    else:
        result["error"] = f"Content-Type {content_type} not supported"
    return result


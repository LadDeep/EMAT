from flask import Blueprint,request
from modules.models.User import User

users = Blueprint('users',__name__)

@users.route("/register",methods=['POST'])
def register():
    content_type = request.headers.get('Content-Type')
    result = {"status": False}
    required_fields = ['first_name','last_name']
    if content_type == 'application/json':
        json = request.json
        result = createUserObject(required_fields,json,result)
             
    elif content_type == 'application/x-www-form-urlencoded':
        form = request.form.to_dict()
        result = createUserObject(required_fields,form,result) 
    else:
        result["error"] = f"Content-Type {content_type} not supported"
    return result


def createUserObject(required_fields,request_data,result):
    email = request_data.get('email',None)
    if email is not None:
        user = User(email=email)
        for field in required_fields:
            field_value = request_data.get(field,None)
            if field_value is not None:
                user[field] = field_value
            else:
                result["error"] = f"{field} is required"
                break
        
        if result.get("error",None) is None:
                user.save()
                result["status"] = True
                result["response"] = "User saved"
    else:
        result["response"] = "email Field is required"
    
    return result
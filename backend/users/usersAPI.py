from flask import Blueprint

users = Blueprint('users',__name__)

@users.route("",methods=['GET'])
def ping():
    return {"status": True, "response": 'pong'}
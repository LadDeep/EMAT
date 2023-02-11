from flask import Blueprint
from modules.models.User import User

users = Blueprint('users',__name__)

@users.route("/login",methods=['GET'])
def ping():
    user = User(first_name='test',last_name='user', email='test@gmail.com')
    user.save()
    return {"status": True, "response": 'pong'}
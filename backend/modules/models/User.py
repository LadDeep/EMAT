from database.database import db
import uuid

class User(db.Document):
    user_id = db.UUIDField(binary=False,default=uuid.uuid1())
    first_name = db.StringField(max_length=100)
    last_name = db.StringField(max_length=100)
    email = db.StringField(required=True)
    password = db.StringField()
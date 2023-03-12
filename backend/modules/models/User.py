from database.database import db
from werkzeug.security import generate_password_hash, check_password_hash
import uuid

class User(db.Document):
    user_id = db.UUIDField(binary=False,default=uuid.uuid4())
    first_name = db.StringField(max_length=100)
    last_name = db.StringField(max_length=100)
    email = db.StringField(required=True)
    password = db.StringField(required=True)  
    currency = db.StringField(required=True)


    def hash_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
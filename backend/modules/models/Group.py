from database.database import db
from modules.models.Expense import Expense
import uuid
import datetime

class Group(db.Document):
    group_id = db.UUIDField(binary=False,default=uuid.uuid4())
    group_name = db.StringField(max_length = 100, required=True)
    group_description = db.StringField()
    expenses = db.EmbeddedDocumentListField(Expense)
    participants = db.ListField()
    group_currency = db.StringField()
    isTemporary = db.BooleanField()
    destruction_date = db.DateTimeField()
    created_at = db.DateTimeField(default=datetime.datetime.utcnow())
    created_by = db.StringField()
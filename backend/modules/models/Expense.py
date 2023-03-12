from database.database import db
import uuid

class Expense(db.EmbeddedDocument):
    expense_id = db.UUIDField(binary=False,default=uuid.uuid4())
    group_id = db.StringField()
    spent_by = db.StringField()
    amount = db.FloatField()
    description = db.StringField()
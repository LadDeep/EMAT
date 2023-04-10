from database.database import db
import uuid
import datetime


class SettleUp(db.EmbeddedDocument):
    group_id = db.StringField()
    user_id = db.StringField()
    last_settled_at = db.DateTimeField(default=datetime.datetime.utcnow())
    amount = db.FloatField()
    settling = db.BooleanField(default=False)
    settler = db.BooleanField(default=False)
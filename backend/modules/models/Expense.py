from database.database import db

class Expense(db.EmbeddedDocument):
    group_id = db.StringField()
    spent_by = db.StringField()
    amount = db.FloatField()
    description = db.StringField()
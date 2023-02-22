from database.database import db

class CurrencyList(db.Document):
    symbol = db.StringField()
    name = db.StringField()
    symbol_native = db.StringField()
    code = db.StringField()
    name_plural = db.StringField()
    decimal_digits = db.IntField()
    rounding = db.IntField()

    
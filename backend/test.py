from modules.models.Group import Group
from flask import Flask
from database.database import db

app = Flask(__name__)

app.config["MONGODB_SETTINGS"] = [
    {"db": "EMAT", "host": "localhost"}
]
app.debug = True
db.init_app(app)

group = Group()
# print(group.__class__.__name__)/

if __name__ == '__main__':
    print(group.__class__.__name__)
else:
    app.run()
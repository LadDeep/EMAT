from flask import Flask
from users.usersAPI import users
from database.database import db


def create_app():
    app = Flask(__name__)

    app.config["MONGODB_SETTINGS"] = [
        {"db": "EMAT", "host": "mongo"}
    ]
    app.debug = True
    db.init_app(app)

    app.register_blueprint(users,url_prefix='/users')
    return app
# def ping():
#     return {"status": True, "response": 'pong'}

if __name__ == '__main__':
    app = create_app()
    app.run(host='172.17.2.41')
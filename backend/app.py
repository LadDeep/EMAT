from flask import Flask
from modules.api.users.usersAPI import users
from database.database import db
from modules.api.auth.routes import auth
from modules.api.groups.groupsAPI import group
from flask_jwt_extended import JWTManager
from flask_mail import Mail


def create_app():
    app = Flask(__name__)

    app.config["MONGODB_SETTINGS"] = [
        {"db": "EMAT", "host": "localhost"}
    ]
    app.debug = True
    db.init_app(app)

    app.config["JWT_SECRET_KEY"] = "secret-key"  # need to change this key and export in the env
    app.config["SMTP_SERVER"] = "smtp.gmail.com"
    app.config["SMTP_USERNAME"] = "username@google.com"
    app.config["SMTP_PASSWORD"] = "temppassword"
    app.config["SMTP_PORT"] = 587
    app.config["SMTP_TLS"] = True

    jwt = JWTManager(app)
    mail = Mail(app)
    app.mail = mail

    app.register_blueprint(users,url_prefix='/users')
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(group,url_prefix='/group')

    return app
# def ping():
#     return {"status": True, "response": 'pong'}

if __name__ == '__main__':
    app = create_app()
    app.run(host='172.17.2.41')
else:
    app = create_app()
    
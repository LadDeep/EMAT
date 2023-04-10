from flask import Flask
from database.database import db
from modules.api.auth.routes import auth
from modules.api.groups.groupsAPI import group
from modules.api.expense.expenseAPI import expense
from modules.api.activities.activitiesAPI import activities_bp
from modules.api.profile.profile import profile
from modules.api.currency.currency import currency
from modules.api.settleUp.settleUpApi import settleUp
from flask_mail import Mail
from flask_jwt_extended import JWTManager


def create_app():
    app = Flask(__name__)

    app.config["MONGODB_SETTINGS"] = [
        {"db": "EMAT", "host": "mongodb+srv://ematasdcg4:ematasdcg4@emat-atlas.z7lxpwg.mongodb.net/EMAT?retryWrites=true&w=majority"}
    ]
    app.debug = True
    app.secret_key = "secret-key"
    db.init_app(app)

    app.config["JWT_SECRET_KEY"] = "secret-key"  # need to change this key and export in the env
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = False # ensures that the token expiry length is unlimited
    
    app.config["JSON-CONTENT-TYPE"] = "application/json"
    app.config["SMTP_PORT"] = 587

    JWTManager(app)
   

    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(profile, url_prefix='/profile')
    app.register_blueprint(currency, url_prefix='/currency')
    app.register_blueprint(group, url_prefix='/group')
    app.register_blueprint(expense, url_prefix='/expense')
    app.register_blueprint(activities_bp, url_prefix='/activities')
    app.register_blueprint(settleUp, url_prefix='/settleUp')

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(port=5004)
else:
    app = create_app()

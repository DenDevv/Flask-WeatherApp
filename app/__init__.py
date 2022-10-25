from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from fake_useragent import UserAgent


# instantiate extensions
db = SQLAlchemy()
login_manager = LoginManager()
ua = UserAgent()


def create_app():
    from app.views import general_blueprint, auth_blueprint

    from app.models import (
        User
    )

    # Instantiate app.
    app = Flask(__name__)
    app.secret_key = 'secretfeg&*&2e32hjjzlea;LFLE'
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Set up extensions.
    db.init_app(app)

    with app.app_context():
        db.create_all()

    login_manager.init_app(app)

    # Register blueprints.
    app.register_blueprint(general_blueprint)
    app.register_blueprint(auth_blueprint)

    # Set up flask login.
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Щоб зберегти, увійдіть у свій обліковий запис.'
    login_manager.login_message_category = 'error'

    return app
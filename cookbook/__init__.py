from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from cookbook.config import Config
from sqlalchemy_utils import database_exists, create_database
from werkzeug.security import generate_password_hash

# Initialise The Database
db = SQLAlchemy()
migrate = Migrate()

# Flask Login Manager
login_manger = LoginManager()
login_manger.login_view = 'users.login'
login_manger.login_message_category = 'info'

mail = Mail()

def create_app(config_class=Config):
    app = Flask(__name__)
    # Using the config file to set the app's configuration rather than in this file (allows for easy reusing later on)
    app.config.from_object(config_class)

    app.debug = True

    db.init_app(app)
    migrate.init_app(app, db)
    login_manger.init_app(app)
    mail.init_app(app)

    # # Ensuring that if the db doesn't exists, it will be created, with the default user
    # from cookbook.models import Users
    # if database_exists(Config.SQLALCHEMY_DATABASE_URI):
    #     app.logger.info("database already exists")
    # else:
    #     app.logger.info("database doesn't exists")
    #     create_database(Config.SQLALCHEMY_DATABASE_URI)
    #     with app.app_context():
    #         db.create_all()
    #         user_id_1 = Users.query.get(1)
    #         # If user with id 1 doesn't exists:
    #         if (user_id_1 is None):
    #             hashed_pw = generate_password_hash("123", "sha256")
    #             user = Users(name="Anonymous", email="example@email.com", password_hash=hashed_pw)
    #             db.session.add(user)
    #             db.session.commit()

    # Adding the Blueprints to the app
    from cookbook.users.routes import users
    from cookbook.recipes.routes import recipes
    from cookbook.main.routes import main
    from cookbook.errors.handlers import errors
    app.register_blueprint(users)
    app.register_blueprint(recipes)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app

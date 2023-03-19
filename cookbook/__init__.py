from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from cookbook.config import Config

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

    db.init_app(app)
    migrate.init_app(app, db)
    login_manger.init_app(app)
    mail.init_app(app)

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

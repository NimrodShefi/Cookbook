from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

# CONFIG
app = Flask(__name__)
# Secret Key
app.config["SECRET_KEY"] = "mysecretkey"
# Add Database
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:123654@localhost/my_cookbook"
# Initialise The Database
db = SQLAlchemy(app)
migrate = Migrate(app, db)

## Flask Login Manager
login_manger = LoginManager()
login_manger.init_app(app)
login_manger.login_view = 'login'
login_manger.login_message_category = 'info'

from cookbook import routes
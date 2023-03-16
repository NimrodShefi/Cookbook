from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# CONFIG
app = Flask(__name__)
# Secret Key
app.config["SECRET_KEY"] = "mysecretkey"
# Add Database
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:123654@localhost/my_cookbook"
# Initialise The Database
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from cookbook import routes
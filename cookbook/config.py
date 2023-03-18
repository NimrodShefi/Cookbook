# This is a locally stored file that will not get uploaded to github
from cookbook.constants import SECRET_KEY, SQLALCHEMY_DATABASE_URI, MAIL_USERNAME, MAIL_PASSWORD

class Config:
    # Secret Key
    SECRET_KEY = SECRET_KEY
    # Add Database
    SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_POST = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = MAIL_USERNAME
    MAIL_PASSWORD = MAIL_PASSWORD

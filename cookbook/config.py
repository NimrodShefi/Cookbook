class Config:
    # Secret Key
    SECRET_KEY = "mysecretkey"
    # Add Database
    # SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://sxloeagbptbocu:268808b5ef2dd1d4a8210ab155ac13af599a81054b8b95a239449ae1d69c2bc7@ec2-34-233-242-44.compute-1.amazonaws.com:5432/dcv45k7ko53mlv"
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:123654@localhost/my_cookbook"
    # Mail related setting
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_POST = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = "namerspam@gmail.com"
    MAIL_PASSWORD = "gidtewluauzjsuqi"

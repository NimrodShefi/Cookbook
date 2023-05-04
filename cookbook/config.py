class Config:
    # Secret Key
    SECRET_KEY = "mysecretkey"
    # Add Database
    # SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://jflzrwnjnmvlof:a5f9a19dd442fb271a29ea5bf4b8d108a9b40cdb0a605b188756b9fa0ed969c8@ec2-35-169-9-79.compute-1.amazonaws.com:5432/dceeg83qo58e3t"
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:123654@localhost/my_cookbook"
    # Mail related setting
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_POST = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = "namerspam@gmail.com"
    MAIL_PASSWORD = "gidtewluauzjsuqi"

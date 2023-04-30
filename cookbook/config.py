class Config:
    # Secret Key
    SECRET_KEY = "mysecretkey"
    # Add Database
    SQLALCHEMY_DATABASE_URI = "postgresql://bbszrmeoacoinc:f431c1680330f0102af84b9f34ec4aeef9bb9b12e4c09d04867357871fa906cc@ec2-3-210-173-88.compute-1.amazonaws.com:5432/d4c4mslcts5ecg"
    # SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:123654@localhost/my_cookbook"
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_POST = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = "namerspam@gmail.com"
    MAIL_PASSWORD = "gidtewluauzjsuqi"

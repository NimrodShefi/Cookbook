
class Config:
    # Secret Key
    SECRET_KEY = "mysecretkey"
    # Add Database
    SQLALCHEMY_DATABASE_URI = "postgres://emmnolrfevgawp:4c13aca4ca03907b8df983bfaf70bb3dd3e737d6a995903c37a5afc045f2d98b@ec2-52-215-68-14.eu-west-1.compute.amazonaws.com:5432/d6bh4oucanhkha"
    # SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:123654@localhost/my_cookbook"
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_POST = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = "namerspam@gmail.com"
    MAIL_PASSWORD = "gidtewluauzjsuqi"

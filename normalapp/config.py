class MyConfig(object):
    DB_USER = "root"
    DB_PASSWD = "password"
    DB_HOST = "localhost"
    DB_PORT = 3306
    DB_NAME = "seckill"
    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{}:{}@{}:{}/{}".format(DB_USER, DB_PASSWD, DB_HOST, DB_PORT, DB_NAME)


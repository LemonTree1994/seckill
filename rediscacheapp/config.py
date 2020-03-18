class MyConfig(object):
    MYSQL_CONFIG = {
        "USER": "root",
        "PASSWD": "password",
        "HOST": "localhost",
        "PORT": 3306,
        "DB": "seckill"
    }
    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{USER}:{PASSWD}@{HOST}:{PORT}/{DB}".format(**MYSQL_CONFIG)

    REDIS_CONFIG = {
        "HOST": "localhost",
        "PORT": 6379,
        "PASSWD": "password",
        "DB": 0
    }
    # redis://[:password]@host:port/db
    REDIS_DATABASE_URI = "redis://:{PASSWD}@{HOST}:{PORT}/{DB}".format(**REDIS_CONFIG)

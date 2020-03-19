class MyConfig(object):
    REDIS_CONFIG = {
        "HOST": "localhost",
        "PORT": 6379,
        "PASSWD": "password",
        "DB": 0
    }
    # redis://[:password]@host:port/db
    REDIS_DATABASE_URI = "redis://:{PASSWD}@{HOST}:{PORT}/{DB}".format(**REDIS_CONFIG)

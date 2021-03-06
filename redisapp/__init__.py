from flask import Flask
import redis

from .config import MyConfig


pool = redis.ConnectionPool.from_url(MyConfig.REDIS_DATABASE_URI)
redis = redis.StrictRedis(connection_pool=pool)


def create_app():
    app = Flask(__name__)
    app.config.from_object(MyConfig)

    from .api import bp
    app.register_blueprint(bp)

    return app
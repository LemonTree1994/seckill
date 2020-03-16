from flask import Flask


from .config import MyConfig
from .models import db

def create_app():
    app = Flask(__name__)
    app.config.from_object(MyConfig)
    db.init_app(app)

    from .api import bp
    app.register_blueprint(bp)

    return app
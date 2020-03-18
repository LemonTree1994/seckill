import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Goods(db.Model):
    __tablename__ = "goods"
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64))
    stock = db.Column(db.Integer)

class Orders(db.Model):
    __tablename__ = "orders"
    id = db.Column(db.Integer,primary_key=True)
    userid = db.Column(db.Integer)
    goodid = db.Column(db.Integer)
    time = db.Column(db.DateTime,default=datetime.datetime.now)


from flask import Blueprint, request, jsonify
import threading

from .models import db, Goods, Orders

bp = Blueprint("api",__name__,url_prefix="/")


@bp.route("/buy")
def buy():
    data = request.args

    userid = data.get("userid")
    goodid = data.get("goodid")
    if not userid or not goodid:
        return "error",400

    good = Goods.query.filter_by(id=goodid).first()
    if not good:
        return "no this good"
    if good.stock < 1:
        return "out of stock"

    userorders = Orders.query.filter_by(userid=userid).all()
    if userorders:
        return "can only buy 1"

    try:
        good.stock -= 1
        order = Orders(goodid=goodid,userid=userid)
        db.session.add(order)
        db.session.commit()
        return str(order.id)
    except:
        db.session.rollback()
        return "server error",500

#look
lock = threading.Lock()

# 加锁位置不对
@bp.route("/buy2")
def buy2():
    data = request.args

    userid = data.get("userid")
    goodid = data.get("goodid")
    if not userid or not goodid:
        return "error",400

    good = Goods.query.filter_by(id=goodid).first()
    if not good:
        return "no this good"
    if good.stock < 1:
        return "out of stock"

    userorders = Orders.query.filter_by(userid=userid).all()
    if userorders:
        return "can only buy 1"

    try:
        lock.acquire()
        good.stock -= 1
        order = Orders(goodid=goodid,userid=userid)
        db.session.add(order)
        db.session.commit()
        return str(order.id)
    except:
        db.session.rollback()
        return "server error",500
    finally:
        lock.release()
#悲观锁
# 更换加锁位置
@bp.route("/buy3")
def buy3():
    data = request.args

    userid = data.get("userid")
    goodid = data.get("goodid")
    if not userid or not goodid:
        return "error",400

    try:
        lock.acquire()
        good = Goods.query.filter_by(id=goodid).first()
        if not good:
            return "no this good"
        if good.stock < 1:
            return "out of stock"

        userorders = Orders.query.filter_by(userid=userid).all()
        if userorders:
            return "can only buy 1"
        good.stock -= 1
        order = Orders(goodid=goodid,userid=userid)
        db.session.add(order)
        db.session.commit()
        return str(order.id)
    except:
        db.session.rollback()
        return "server error",500
    finally:
        lock.release()

# 乐观锁
@bp.route("/buy4")
def buy4():
    data = request.args

    userid = data.get("userid")
    goodid = data.get("goodid")
    if not userid or not goodid:
        return "error",400

    good = Goods.query.filter_by(id=goodid).first()
    if not good:
        return "no this good"
    if good.stock < 1:
        return "out of stock"
    temp_stock = good.stock
    userorders = Orders.query.filter_by(userid=userid).all()
    if userorders:
        return "can only buy 1"

    try:
        good = Goods.query.filter_by(id=goodid,stock=temp_stock).first()
        if not good:
            return "server error"
        good.stock -= 1
        order = Orders(goodid=goodid,userid=userid)
        db.session.add(order)
        db.session.commit()
        return str(order.id)
    except:
        db.session.rollback()
        return "server error",500

@bp.route("/")
def get_all_orders():
    orders = Orders.query.all()
    results = []
    for order in orders:
        results.append("Order<{}>: user<{}> good<{}>".format(order.id, order.userid,order.goodid))
    return jsonify(results)
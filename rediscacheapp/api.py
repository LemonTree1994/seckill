from flask import Blueprint, request, jsonify
import threading

from .models import db, Goods, Orders
from . import redis

bp = Blueprint("api",__name__,url_prefix="/")
keyname = "seckill:rediscacheapp:"
# 商品库存 string
gname = keyname + "good:"
# 商品已下单用户 set
uname = keyname + "user:"

@bp.route("/initredis")
def init_redis():
    ping = redis.ping()
    if not ping:
        return "redis connection error"

    goods = Goods.query.all()
    for good in goods:
        # 更新商品库存
        redis.set(gname+str(good.id),good.stock)
        # 删除原有购物用户记录
        if redis.exists(uname + str(good.id)):
            redis.delete(uname + str(good.id))

    orders = Orders.query.all()
    # 更新用户购物记录
    for order in orders:
        redis.sadd(uname+str(order.goodid),str(good.userid))
    return "init redis finished"

@bp.route("/buy")
def buy():
    data = request.args

    userid = data.get("userid")
    goodid = data.get("goodid")

    if not userid or not goodid:
        return "error",400

    try:
        if not redis.ping():
            return "redis server connection error"
        good_name = gname + str(goodid)
        user_name = uname + str(goodid)
        if redis.exists(good_name):
            stock = redis.get(good_name)
            stock = int(stock.decode("utf-8"))
            if stock>0:
                if redis.sismember(user_name,userid):
                    return "can only buy 1"
                else:
                    pipe = redis.pipeline()
                    pipe.multi()
                    new_stock = redis.incrby(good_name,-1)
                    redis.sadd(user_name,userid)
                    pipe.execute()
                    good = Goods.query.filter_by(id=goodid).first()
                    good.stock = new_stock
                    order = Orders(userid=userid,goodid=goodid)
                    db.session.add(order)
                    db.session.commit()
                    return str(order.id)
            else:
                return "out of stock"
        else:
            return "no this thing"
    except Exception as e:
        print(e)
        db.session.rollback()


#look
lock = threading.Lock()

#同步方法或代码块
@bp.route("/buy2")
def buy2():
    data = request.args

    userid = data.get("userid")
    goodid = data.get("goodid")

    if not userid or not goodid:
        return "error", 400

    try:
        if not redis.ping():
            return "redis server connection error"
        good_name = gname + str(goodid)
        user_name = uname + str(goodid)
        lock.acquire()
        if redis.exists(good_name):
            stock = redis.get(good_name)
            stock = int(stock.decode("utf-8"))
            if stock > 0:
                if redis.sismember(user_name, userid):
                    return "can only buy 1"
                else:
                    pipe = redis.pipeline()
                    pipe.multi()
                    new_stock = redis.incrby(good_name, -1)
                    redis.sadd(user_name, userid)
                    pipe.execute()
                    good = Goods.query.filter_by(id=goodid).first()
                    good.stock = new_stock
                    order = Orders(userid=userid, goodid=goodid)
                    db.session.add(order)
                    db.session.commit()
                    return str(order.id)
            else:
                return "out of stock"
        else:
            return "no this thing"
    except Exception as e:
        print(e)
        db.session.rollback()
    finally:
        lock.release()

@bp.route("/")
def get_all_orders():
    orders = Orders.query.all()
    results = []
    for order in orders:
        results.append("Order<{}>: user<{}> good<{}>".format(order.id, order.userid,order.goodid))
    return jsonify(results)
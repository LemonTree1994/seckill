from flask import Blueprint, request, jsonify
import threading

from . import redis

bp = Blueprint("api",__name__,url_prefix="/")
keyname = "seckill:rediscacheapp:"
# 商品库存 string
gname = keyname + "good:1"
# 商品已下单用户 set
uname = keyname + "user:1"
oname = keyname + "order:1"

@bp.route("/initredis")
def init_redis():

    stock = request.args.get("stock") or 10
    ping = redis.ping()
    if not ping:
        return "redis connection error"
    redis.set(gname, stock)
    if redis.exists(uname):
        redis.delete(uname)
    if redis.exists(oname):
        redis.delete(oname)

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
        if redis.exists(gname):
            stock = redis.get(gname)
            stock = int(stock.decode("utf-8"))
            if stock>0:
                if redis.sismember(uname,userid):
                    return "can only buy 1"
                else:
                    pipe = redis.pipeline()
                    pipe.multi()
                    redis.incrby(gname,-1)
                    redis.sadd(uname,userid)
                    redis.lpush(oname,str(userid)+"'s order")
                    pipe.execute()
                    return str(userid)+"'s order"
            else:
                return "out of stock"
        else:
            return "no this thing"
    except Exception as e:
        print(e)


#look
lock = threading.Lock()

#同步方法或代码块
@bp.route("/buy2")
def buy2():
    data = request.args

    userid = data.get("userid")
    goodid = data.get("goodid")

    if not userid or not goodid:
        return "error",400

    try:
        lock.acquire()
        if not redis.ping():
            return "redis server connection error"
        if redis.exists(gname):
            stock = redis.get(gname)
            stock = int(stock.decode("utf-8"))
            if stock>0:
                if redis.sismember(uname,userid):
                    return "can only buy 1"
                else:
                    pipe = redis.pipeline()
                    pipe.multi()
                    redis.incrby(gname,-1)
                    redis.sadd(uname,userid)
                    redis.lpush(oname,str(userid)+"'s order")
                    pipe.execute()
                    return str(userid)+"'s order"
            else:
                return "out of stock"
        else:
            return "no this thing"
    except Exception as e:
        print(e)
    finally:
        lock.release()

@bp.route("/")
def get_all_orders():
    orders = Orders.query.all()
    results = []
    for order in orders:
        results.append("Order<{}>: user<{}> good<{}>".format(order.id, order.userid,order.goodid))
    return jsonify(results)
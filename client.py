import requests
import threading
from concurrent.futures import ThreadPoolExecutor
import time
import sys
import getopt


def buy(userid,goodid):
    rpost = requests.get("http://127.0.0.1:9999/buy3", params={"userid":userid,"goodid":goodid})
    return rpost.text

def dec_buy(pool_input):
    return buy(pool_input[0],pool_input[1])
if __name__ == '__main__':
    args = sys.argv
    if len(args) != 2:
        print("<usage>:python client.py <user_num>")
    else:
        user_num = int(args[1])
        pool = ThreadPoolExecutor(max_workers=10,thread_name_prefix="req_")
        t1 = time.time()
        res = pool.map(dec_buy,[(i,1)for i in range(user_num)])
        for r in res:
            print(r)
        print("耗时：", time.time()-t1)

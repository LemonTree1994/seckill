import requests
import threading
from concurrent.futures import ThreadPoolExecutor
import time
import sys
import getopt


def buy(url,userid,goodid):
    rpost = requests.get("http://127.0.0.1:9999/"+url, params={"userid":userid,"goodid":goodid})
    return rpost.text

def dec_buy(pool_input):
    return buy(pool_input[0], pool_input[1], pool_input[2])
if __name__ == '__main__':
    args = sys.argv
    if len(args) != 3:
        print("<usage>:python client.py <url> <user_num>")
    else:
        url = args[1]
        user_num = int(args[2])
        pool = ThreadPoolExecutor(max_workers=10,thread_name_prefix="req_")
        t1 = time.time()
        res = pool.map(dec_buy,[(url,i,1)for i in range(user_num)])
        for r in res:
            print(r)
        print("耗时：", time.time()-t1)

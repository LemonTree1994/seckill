import requests
import threading
from concurrent.futures import ThreadPoolExecutor
import time
import sys
import getopt
import random


def buy(url,userid,goodid):
    rpost = requests.get("http://127.0.0.1:9999/"+url, params={"userid":userid,"goodid":goodid})
    return rpost.text

def dec_buy(pool_input):
    return buy(pool_input[0], pool_input[1], pool_input[2])
if __name__ == '__main__':
    args = sys.argv
    if len(args) ==3 or len(args) ==4:
        url = args[1]
        user_num = int(args[2])
        inputargs = [(url, i, 1) for i in range(user_num)]
        if len(args) == 4 and args[3] in ["repeat","r"]:
            inputargs = [(url, i//5, 1) for i in range(user_num)]
        pool = ThreadPoolExecutor(max_workers=100,thread_name_prefix="req_")
        t1 = time.time()
        res = pool.map(dec_buy,inputargs)
        for r in res:
            print(r)
        print("耗时：", time.time()-t1)
    else:
        print("<usage>:python client.py <url> <user_num> [repeat|r]")


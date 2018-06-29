# -*- coding:utf-8 -*-
# Author:lixuecheng

import asyncio

import time
import requests
# import json
import sys
from tqdm import tqdm
import concurrent.futures

# from multiprocessing import Pool, Process


async def hello1(sem, url):
    async with sem:
        loop = asyncio.get_event_loop()
        s = requests.session()
        d = await loop.run_in_executor(None, s.get,
                                       'http://172.16.32.40:8082/webapi/api/token/gettoken?openid=' + url)

        to = d.json()['resultData']['access_token']
        headers1 = {'Authorization': 'bearer ' + to}
        s.headers = headers1
        f = await loop.run_in_executor(None, s.get,
                                       'http://172.16.32.40:8082/webapi/api/Exam/GetUserInfo', )
        f.encoding = sys.getdefaultencoding()
        # p.update(1)
        print(1)
        return to, f.text
        # await asyncio.sleep(0.1)


def hh(tasks, sem):
    loop = asyncio.get_event_loop()
    # loop=asyncio.new_event_loop()
    # print(loop.is_running())
    tasks2 = [hello1(sem, t) for t in tasks]
    print(tasks2)

    aa, _ = loop.run_until_complete(asyncio.wait(tasks2))
    # loop.close()
    return aa


def ff(loop, pool, task):
    sem1 = asyncio.Semaphore(100)
    pool.apply(hh, (task, sem1))
    return 1


if __name__ == "__main__":
    ll = []
    tt = 132
    lll = []
    with open('d:/4.txt') as f:
        for line in f.readlines():
            ll.append(line)
    tasks = []
    s = time.time()

    # tq = tqdm(total=len(ll), ncols=75)
    pool = Pool()
    # pool = concurrent.futures.ProcessPoolExecutor()
    loop = asyncio.get_event_loop()

    if tt == 1:
        for i in range(1):
            tasks.append(i)
    else:
        for i in ll:
            if len(tasks) > 399:
                # print(2)
                # pool.apply_async(hh, args=(tasks, sem1,))
                ff(loop, pool, tasks)
                # print(f)
                # hh(tasks)
                # p = Process(target=hh, args=(tasks, sem1))
                # p.start()
                tasks = []
            else:
                if len(i) > 0:
                    tasks.append(i)
        # print(1)
        if len(tasks) > 0:
            ff(loop, pool, tasks)

        # loop.run_until_complete(asyncio.wait(lll))
        # loop.close()

        # print(3)
        # pool.apply_async(hh, args=(tasks, sem1,))
        # print(f)
        #     p = Process(target=hh, args=(tasks, sem1))
        #     p.start()

        # pool.close()
        # pool.join()

    # aa, bb = loop.run_until_complete(asyncio.wait(tasks))
    # with open('d:/5.txt', 'w') as f:
    #     for i in aa:
    #         f.write(i.result()[0] + ',,,,' + i.result()[1] + '\n')
    # tq.close()

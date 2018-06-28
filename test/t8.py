# -*- coding:utf-8 -*-
# Author:lixuecheng

import asyncio
import time
import requests
# import json
import sys
from tqdm import tqdm


async def hello1(sem, url, p):
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
        p.update(1)
        return to, f.text


if __name__ == "__main__":
    ll = []
    tt = 132
    with open('d:/4.txt') as f:
        for line in f.readlines():
            ll.append(line)
    tasks = []

    s = time.time()
    sem1 = asyncio.Semaphore(100)
    tq = tqdm(total=len(ll), ncols=75)
    if tt == 1:
        for i in range(1):
            tasks.append(hello1(sem1, 'f14f531c-2eef-4550-828b-0bdda49ae9dd', tq))
    else:
        for i in ll:
            if len(i) > 0:
                tasks.append(hello1(sem1, i, tq))

    loop = asyncio.get_event_loop()
    aa, bb = loop.run_until_complete(asyncio.wait(tasks))
    with open('d:/5.txt', 'w') as f:
        for i in aa:
            f.write(i.result()[0] + ',,,,' + i.result()[1] + '\n')
    tq.close()
    loop.close()

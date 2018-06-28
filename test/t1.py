# -*- coding:utf-8 -*-
# Author:lixuecheng

import asyncio
import time
import requests
import concurrent.futures
import os
import random


class A:
    async def a(self, a1):
        time.sleep(0.1)
        # print(a1)
        return a1 + 1

    async def b(self, b1):
        d = await self.a(b1)
        return d + 1


class B:

     def req(self, method,url, path,dict):
        a=time.time()
        r = requests.session().request(method, url + path)
        r.close()
        print(os.getpid(),'cost:',time.time()-a)
        return r


class C:
    def ppp(self, k):
        time.sleep(0.05)
        # time.sleep(random.random())
        print(k, os.getpid())
        return k + 1


def fan(a):
    if a < 200:
        a += 1
        a*=1.02
        a/=0.999
        if 'aaa'=='aaa':
            fan(a)


async def main():
    # cc = C()
    # bb=B()
    # l = [i for i in range(100)]
    # pool = concurrent.futures.ProcessPoolExecutor()
    loop = asyncio.get_event_loop()
    # a=time.time()
    # print('start_time:',a)
    # for _ in range(100):

        # res = await  loop.run_in_executor(pool, bb.req, 'http://172.16.32.40:8082', '/webapi/api/token/gettoken?openid=f14f531c-2eef-4550-828b-0bdda49ae9dd')
        # res = await  loop.run_in_executor(pool, time.sleep, 0.1)
    res = await  loop.run_in_executor(None, time.sleep, 0.1)

        # res = await  loop.run_in_executor(None, cc.ppp, l.pop())
        # fan(res)
        # print(res.status_code,time.time()-a)
    # pool.shutdown()
    # print(time.time()-a,1)

# async  def aa():
#     await main()


if __name__ == '__main__':
    print(os.getpid())
    st = time.time()
    loop = asyncio.get_event_loop()
    tasks=[main() for _ in range(200)]
    loop.run_until_complete(asyncio.wait(tasks))
    print(time.time() - st)
    loop.close()

# aa = A()
# bb = B()
# 1.3919999599456787 1.0190000534057617
#  10.760999917984009 10.152999877929688
#5.644999980926514 5.0950000286102295
# 5.0899999141693115


# tasks = loop.create_task(aa.b(1))


# tasks = loop.create_task(
#     bb.req('http://172.16.32.40:8082', '/webapi/api/token/gettoken?openid=f14f531c-2eef-4550-828b-0bdda49ae9dd'))
# v = loop.run_until_complete(tasks)
# print(tasks.result())
# print(v)

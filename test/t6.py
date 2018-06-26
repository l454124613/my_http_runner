# -*- coding:utf-8 -*-
# Author:lixuecheng
from core.Request import run, runnable, Request


@runnable
class tt(Request):
    def on_start(self):
        print('start')

    def on_end(self):
        print('end')

    @run
    def t1(self):
        self\
            .add_request('get',
                         'http://172.16.32.40:8082/webapi/api/token/gettoken?openid=f14f531c-2eef-4550-828b-0bdda49ae9dd') \
            .run()

    @run
    def t2(self):
        self\
            .add_request('get',
                         'http://172.16.32.40:8082/webapi/api/token/gettoken?openid=f14f531c-2eef-4550-828b-0bdda49ae9dd') \
            .run()

# async def main():
#     # cc = C()
#     bb=tt()
#     l = [i for i in range(100)]
#     pool = concurrent.futures.ProcessPoolExecutor()
#     loop = asyncio.get_event_loop()
#     a=time.time()
#     print('start_time:',a)
#     for _ in range(30):
#
#         res = await  loop.run_in_executor(pool, bb.req, 'http://172.16.32.40:8082', '/webapi/api/token/gettoken?openid=f14f531c-2eef-4550-828b-0bdda49ae9dd')
#
#         # res = await  loop.run_in_executor(None, cc.ppp, l.pop())
#         # fan(res)
#         print(res.status_code,time.time()-a)
#     pool.shutdown()
#     print(time.time()-a,1)
#
#
# if __name__ == '__main__':
#     print(os.getpid())
#     st = time.time()
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(main())
#     print(time.time() - st)
#     loop.close()

# -*- coding:utf-8 -*-
# Author:lixuecheng

import aiohttp
import  time
import asyncio



async def fetch_async(a):
    async with aiohttp.request('GET', 'http://172.16.32.40:8082/webapi/api/token/gettoken?openid='+a) as r:

        await r.wait_for_close()
        print(r.request_info)
        # r.headers['Content-Type'] == 'application/json'
    return 'a'


event_loop = asyncio.get_event_loop()
tasks = [fetch_async(num) for num in ['f14f531c-2eef-4550-828b-0bdda49ae9dd']]
event_loop.run_until_complete(asyncio.gather(*tasks))
# results = event_loop.run_until_complete(asyncio.gather(*tasks))
# print(results[0])
#
# for num, result in zip(['http://172.16.32.40:8082/webapi/api/token/gettoken?openid=f14f531c-2eef-4550-828b-0bdda49ae9dd','http://www.baidu.com'], results):
#     print('fetch({}) = {}'.format(num, result))
# -*- coding:utf-8 -*-
# Author:lixuecheng


import os
import sys
from locust import HttpLocust, TaskSet, task

sys.path.append(r'E:\pytest\my_http_runner')
from core.base_req import RunHttp


class website1(TaskSet):

    @task
    def get(self):
        RunHttp('http://172.16.32.40:8082').add_request('get',
                                                        '/webapi/api/token/gettoken?openid=f14f531c-2eef-4550-828b-0bdda49ae9dd',
                                                        name='test').run()


class WebUser(HttpLocust):
    task_set = website1
    host = 'http://xxxxx'
    min_wait = 100
    max_wait = 3000

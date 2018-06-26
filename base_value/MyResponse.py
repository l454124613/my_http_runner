# -*- coding:utf-8 -*-
# Author:lixuecheng

from locust.clients import ResponseContextManager


class MyResponse(ResponseContextManager):

    def __init__(self, response, is_locust=True):
        self.__dict__ = response.__dict__
        self.is_locust = is_locust

    def failure(self, exc):
        if self.is_locust:
            super(MyResponse, self).failure(exc)
        else:
            print('failure', exc)

    def success(self, exc='运行成功'):
        if self.is_locust:

            super(MyResponse, self).success()
        else:
            print('ok', exc)

# -*- coding:utf-8 -*-
# Author:lixuecheng
from requests import sessions
# from locust.clients import HttpSession
import time
import sys

# global ff
ff = []

is_ok = True


class Request:
    ff = []

    def __init__(self, http_session=None, not_locust=True, catch_dict=None):
        self.HttpSession = http_session
        self._not_locust = not_locust
        self.run_item_list = []
        self.res_dict = {}
        self.catch_dict = {} if catch_dict is None else catch_dict
        self._add_catch_dict = {}
        self._add_check_dict = {}
        pass

    def on_start(self):
        pass

    def on_end(self):
        pass

    def set_locust_host(self, host):
        if not host.startswith('http'):
            host = 'http://' + host
        from locust.clients import HttpSession
        self.HttpSession = HttpSession(host)
        print('set session ok:' + host)
        return self

    def is_locust(self):
        self._not_locust = False
        return self

    def run(self):
        # time.sleep(1)
        print('run ok')
        self.run_item_list = []
        pass

    def add_check(self, check):
        pass

    def add_catch(self, catch):
        pass

    def add_request(self, method, url, name=None, params=None, data=None, headers=None, files=None, auth=None,
                    timeout=None, allow_redirects=True, proxies=None, json=None, check=None, catch=None,
                    content_encoding='utf8'):
        print('add req ok')
        return self


def run(fn):
    def aa(*c):
        return fn(*c)

    ff.append(fn.__name__)
    print(1)
    return aa


def _check_ok():
    if 'wei_le_pi_liang_yun_xing' in sys.path:
        return False
    else:
        return True


def runnable(cls):
    if _check_ok():
        c = cls()
        c.on_start()
        for i in ff:
            if hasattr(c, i):
                c1 = getattr(c, i)
                c1()
        c.on_end()
    else:
        Request.ff=ff
    return cls

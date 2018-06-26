# -*- coding:utf-8 -*-
# Author:lixuecheng


class B:
    def __init__(self):
        pass

    def on_start(self):
        pass

    def on_end(self):
        pass

    def _ok(self):
        self.on_start()
        print('ok')

    def __getattr__(self, name):
        print("__getattr__() is called ")
        return name + " from getattr"


ff = []


def run(fn):
    def aa(*c):
        return fn(*c)

    ff.append(fn.__name__)
    return aa


def runnable(cls):
    c = cls()
    c.on_start()
    for i in ff:
        if hasattr(c, i):

            c1 = getattr(c, i)
            c1()
    c.on_end()



def conf(method):
    pass

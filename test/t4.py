# -*- coding:utf-8 -*-
# Author:lixuecheng

def onexit(f):
    import atexit
    atexit.register(f)
    return f


@onexit
def func(a):
    print(a)
func(1)
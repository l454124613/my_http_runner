# -*- coding:utf-8 -*-
# Author:lixuecheng

from multiprocessing import Pool, cpu_count, Queue, freeze_support
import os


# def get_num(num):
#     for i in range(num):
#         yield i


# l.sort(reverse=True)


# l.pop()
#
# print(l)

# g = get_num(50)
# # for i in g:
# # #     print(i)
# # print(g.__next__())
# # print(g.__next__())

# print(g.next())

def run_num(s):
    print(s.pop())


def f2(arg):
    print(arg)


# if __name__ == "__main__":
#     num = os.cpu_count()
#     p = Pool(num - 1)
#     for i in range(len(l)):
#         p.apply(func=run_num, args=(l,))
#     p.close()
#     p.join()
#     # for i in range(11):
#     #     run_num(l)
import os, time

q = Queue(100)
for i in range(10):
    q.put(i)


def ppp(k):
    time.sleep(0.1)
    print(k, os.getpid())


if __name__ == '__main__':
    # print()
    print("parent process %s" % (os.getpid()))

    p = Pool(cpu_count() - 1)

    while not q.empty():
        p.apply(func=ppp, args=(q.get(),))
    p.close()
    p.join()
# for i in range(10):
#     print(q.get())

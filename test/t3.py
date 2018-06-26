# -*- coding:utf-8 -*-
# Author:lixuecheng
from test.t2 import B, run, runnable


@runnable
class C(B):
    #
    # def on_start(self):
    #     self.c = 4
    #     print('startC')

    @run
    def cc(self):
        print(1)
        # print(self.e)
        self.d = 44

    @run
    def cd(self):
        print(2)
        print(self.d)
        # self.e=2

    # def on_end(self):
    #     print('end')

# dd = C()
# dd.cc()
# if __name__ == '__main__':
#     dd = C()
# print(dd.cc)
# print(hasattr(dd, 'cc'))
# print(getattr(dd, 'cc'))

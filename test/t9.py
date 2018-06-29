# -*- coding:utf-8 -*-
# Author:lixuecheng


import time
import zmq


def producer():
    context = zmq.Context()
    zmq_socket = context.socket(zmq.PUSH)
    zmq_socket.bind("tcp://127.0.0.1:5557")
    # 开始Producer之前必须先启动resultcollector和consumer
    for num in range(2000):
        work_message = {'num': num}
        zmq_socket.send_json(work_message)


producer()
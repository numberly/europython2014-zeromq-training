#!/usr/bin/env python
import zmq
import time

context = zmq.Context()

socket = context.socket(zmq.DEALER)

socket.connect('tcp://172.16.16.228:5555')
s = time.time()
for i in range(10000):
    socket.send_multipart([str(i)])
    socket.recv()

print time.time() - s

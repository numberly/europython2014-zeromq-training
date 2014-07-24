#!/usr/bin/env python
import zmq

context = zmq.Context()

socket = context.socket(zmq.DEALER)

socket.connect('tcp://172.16.16.228:5555')
for i in range(10):
    socket.send(str(i))
    print socket.recv()

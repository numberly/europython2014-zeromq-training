#!/usr/bin/env python
import zmq

context = zmq.Context()

socket = context.socket(zmq.DEALER)

socket.connect('tcp://127.0.0.1:5555')
for i in range(10):
    socket.send_multipart([str(i)])
    print socket.recv()

#!/usr/bin/env python
import zmq
import sys

server_address = sys.argv[1]

context = zmq.Context()

socket = context.socket(zmq.DEALER)

socket.connect('tcp://%s:5555' % server_address)
for i in range(10):
    socket.send(str(i))
    print socket.recv()

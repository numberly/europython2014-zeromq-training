#!/usr/bin/env python
import zmq
from config import SERVER_ADDRESS

context = zmq.Context()

socket = context.socket(zmq.DEALER)

socket.connect('tcp://{}'.format(SERVER_ADDRESS))
for i in range(10):
    socket.send(str(i))
    print socket.recv()

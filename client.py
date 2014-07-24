#!/usr/bin/env python
import zmq
import socket


def get_local_ip():
    """
    Retrieve the clients local ip address and return it as a string

    :returns IpAddress as String
    """
    ip = socket.gethostbyname(socket.gethostname())
    return ip

context = zmq.Context()

socket = context.socket(zmq.DEALER)

socket.connect('tcp://127.0.0.1:5555')
for i in range(10):
    msg = "Hi server this is my message {}".format(i)
    socket.send(msg)
    print socket.recv()

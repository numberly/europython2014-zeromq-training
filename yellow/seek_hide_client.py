#!/usr/bin/env python
import argparse
import zmq

def get_local_ip():
    """
    Retrieve the clients local ip address and return it as a string

    :returns IpAddress as String
    """
    import socket
    return socket.gethostbyname(socket.gethostname())


context = zmq.Context()

socket = context.socket(zmq.DEALER)

parser = argparse.ArgumentParser()
parser.add_argument('-c', '--connect-address', default='tcp://127.0.0.1:5555')

args = parser.parse_args()

socket.connect(args.connect_address)

ip = get_local_ip()
port = 5555
msg = "HELLOFROM {} {}".format(ip, port)
socket.send(msg)
response = socket.recv()
print response

#!/usr/bin/env python

import argparse
import zmq

context = zmq.Context()

socket = context.socket(zmq.DEALER)

parser = argparse.ArgumentParser()
parser.add_argument('-c', '--connect-address', default='tcp://127.0.0.1:5555')
parser.add_argument('-p', '--port', default='5556')

args = parser.parse_args()


def get_ip():
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('www.google.com', 80))
    ip = s.getsockname()[0]
    s.close()
    return ip

myip = get_ip()

socket.connect(args.connect_address)

# First just register to the server
command = '{}:{}'.format(myip, args.port)
socket.send_string(command)
print socket.recv_multipart()

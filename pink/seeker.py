#!/usr/bin/env python

import argparse
import socket
import zmq

context = zmq.Context()

zmq_socket = context.socket(zmq.DEALER)

parser = argparse.ArgumentParser()
parser.add_argument('-c', '--connect-address', default='tcp://127.0.0.1:5555')
parser.add_argument('-p', '--port', default='5556')

args = parser.parse_args()

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("gmail.com", 80))
myip = s.getsockname()[0]
s.close()

zmq_socket.connect(args.connect_address)

# First just register to the server
command = '{}:{}'.format(myip, args.port)
zmq_socket.send_string(command)
print zmq_socket.recv_multipart()

#!/usr/bin/env python
import argparse
import zmq
import socket as so

context = zmq.Context()

socket = context.socket(zmq.DEALER)

parser = argparse.ArgumentParser()
parser.add_argument('-l', '--local-address')
parser.add_argument('-c', '--connect-address', default='tcp://127.0.0.1:5555')

args = parser.parse_args()

socket.connect(args.connect_address)

ip = so.gethostbyname(so.gethostname())
socket.send(args.local_address)
response = socket.recv_string()
print response

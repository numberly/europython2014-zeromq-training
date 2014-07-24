#!/usr/bin/env python

import argparse
import zmq
import json
import socket


ip_address = socket.gethostbyname(socket.gethostname())
port = 5555
context = zmq.Context()
socket = context.socket(zmq.DEALER)

parser = argparse.ArgumentParser()
parser.add_argument('-c', '--connect-address', default='tcp://127.0.0.1:5555')
args = parser.parse_args()

socket.connect(args.connect_address)
msg = '{0}:{1}'.format(ip_address, port)
socket.send(msg)
print socket.recv()

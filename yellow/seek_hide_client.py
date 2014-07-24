#!/usr/bin/env python
import argparse
import zmq

from utils import get_local_ip

context = zmq.Context()

socket = context.socket(zmq.DEALER)

parser = argparse.ArgumentParser()
parser.add_argument('-c', '--connect-address', default='tcp://127.0.0.1:5555')

args = parser.parse_args()

socket.connect(args.connect_address)

ip = get_local_ip()
port = 5555
msg = "REGISTER {}:{}".format(ip, port)
socket.send(msg)
print "Waiting for response..."
response = socket.recv()
print response

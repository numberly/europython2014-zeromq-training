#!/usr/bin/env python

import argparse
import zmq

context = zmq.Context()

socket = context.socket(zmq.DEALER)

parser = argparse.ArgumentParser()
parser.add_argument('-c', '--connect-address', default='tcp://127.0.0.1:5555')
parser.add_argument('-p', '--port', default="4444")
parser.add_argument('-i', '--ip')

args = parser.parse_args()

socket.connect(args.connect_address)

# First just register to the server
command = '{}:{}'.format(args.ip, args.port)
socket.send_multipart([command])
print socket.recv_json()

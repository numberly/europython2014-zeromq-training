#!/usr/bin/env python
import argparse
import zmq

context = zmq.Context()

socket = context.socket(zmq.DEALER)

parser = argparse.ArgumentParser()
parser.add_argument('-c', '--connect-address', default='tcp://127.0.0.1:5555')
parser.add_argument('-i', '--ip-address', default='127.0.0.1')
parser.add_argument('-p', '--port', default='5555')

args = parser.parse_args()

socket.connect(args.connect_address)
socket.send(args.ip_address + ":" + args.port)
print socket.recv()

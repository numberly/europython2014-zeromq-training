#!/usr/bin/env python
import zmq
import argparse

parser = argparse.ArgumentParser()
parser.add_argument(
    '--connect', help='connection address (default: %(default)s)',
    default='tcp://127.0.0.1:5555')

args = parser.parse_args()


context = zmq.Context()

socket = context.socket(zmq.DEALER)

socket.connect(args.connect)
for i in range(10):
    socket.send_multipart([str(i)])
    print socket.recv()

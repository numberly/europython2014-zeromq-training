#!/usr/bin/env python2
import argparse
import zmq

context = zmq.Context()

s = context.socket(zmq.DEALER)

# @ep14 172.16.16.228:5555
parser = argparse.ArgumentParser()
parser.add_argument('-c', '--connect-address', default='tcp://127.0.0.1:5555')

args = parser.parse_args()

s.connect(args.connect_address)
for i in range(10):
    msg = "Hi server this is my message {}".format(i)
    s.send(msg)
    print(s.recv())

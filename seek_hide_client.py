#!/usr/bin/env python
import argparse
import zmq
import socket
import json
ip = socket.gethostbyname(socket.AF_APPLETALKgethostname())

context = zmq.Context()

socket = context.socket(zmq.DEALER)

parser = argparse.ArgumentParser()
parser.add_argument('-c', '--connect-address', default='tcp://127.0.0.1:5555')

args = parser.parse_args()

msg = {'msg' : "hello",
        "myip" : ip}


socket.connect(args.connect_address)
for i in range(10):
    socket.send(json.dumps(msg))
    print socket.recv()

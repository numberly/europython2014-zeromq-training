#!/usr/bin/env python
import argparse
import zmq
import socket
ip = socket.gethostbyname(socket.gethostname())
port = 5555

context = zmq.Context()

socket = context.socket(zmq.DEALER)

parser = argparse.ArgumentParser()
parser.add_argument('-c', '--connect-address', default='tcp://127.0.0.1:5555')

args = parser.parse_args()

msg = "HELLO {ip} {port}".format(ip=ip, port=port) 
socket.connect(args.connect_address)
for i in range(10):
    socket.send(msg)
    print socket.recv()

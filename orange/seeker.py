#!/usr/bin/env python

import argparse
import zmq

context = zmq.Context()

socket = context.socket(zmq.DEALER)

parser = argparse.ArgumentParser()
parser.add_argument('-c', '--connect-address', default='tcp://127.0.0.1:5555')
<<<<<<< HEAD
parser.add_argument('-p', '--port', default=5555)
=======
parser.add_argument('-p', '--port', default=5556)
>>>>>>> upstream/master

args = parser.parse_args()

import socket as socket2
myip = socket2.gethostbyname(socket2.gethostname())

socket.connect(args.connect_address)

# First just register to the server
command = '{}:{}'.format(myip, args.port)
socket.send(command)
<<<<<<< HEAD
resp = socket.recv()
print resp
=======
print(socket.recv_string())
>>>>>>> upstream/master

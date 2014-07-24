#!/usr/bin/env python

import argparse
import zmq
from utils import get_local_ip

context = zmq.Context()

socket = context.socket(zmq.DEALER)

parser = argparse.ArgumentParser()
parser.add_argument('-c', '--connect-address', default='tcp://127.0.0.1:5555')
parser.add_argument('-p', '--port', default=5555)

args = parser.parse_args()
myip = get_local_ip()

socket.connect(args.connect_address)

# First just register to the server
command = 'REGISTER {}:{}'.format(myip, args.port)
socket.send(command)
resp = socket.recv()
print resp

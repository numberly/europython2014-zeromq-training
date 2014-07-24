#!/usr/bin/env python

import argparse
import zmq
import utils

context = zmq.Context()

socket = context.socket(zmq.DEALER)

parser = argparse.ArgumentParser()
parser.add_argument('-c', '--connect-address', default='tcp://127.0.0.1:5555')
parser.add_argument('-p', '--port', default=4444)

args = parser.parse_args()

myip = utils.get_local_ip(args.connect_address.split('://')[1].split(':')[0])

socket.connect(args.connect_address)

# First just register to the server
command = '{}:{}'.format(myip, args.port)
socket.send(command)
print socket.recv()

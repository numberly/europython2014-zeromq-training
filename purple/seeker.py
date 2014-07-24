#!/usr/bin/env python

import argparse
import zmq
import utils

context = zmq.Context()

socket = context.socket(zmq.DEALER)

parser = argparse.ArgumentParser()
parser.add_argument('-c', '--connect-address', default='tcp://127.0.0.1:5555')
parser.add_argument('-p', '--port', default=4444)
parser.add_argument('-l', '--list-only', action='store_true', default=False)

args = parser.parse_args()

myip = utils.get_local_ip(args.connect_address.split('://')[1].split(':')[0])

socket.connect(args.connect_address)

if args.list_only:
  command = 'LIST'
else:
  command = 'REGISTER {}:{}'.format(myip, args.port)
print command
socket.send(command)
print socket.recv()

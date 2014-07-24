#!/usr/bin/env python
import argparse
import zmq
import socket

context = zmq.Context()

sock = context.socket(zmq.DEALER)

parser = argparse.ArgumentParser()
parser.add_argument('-l', '--local-address')
parser.add_argument('-c', '--connect-address', default='tcp://127.0.0.1:5555')

args = parser.parse_args()

local_address = args.local_address

if not local_address:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    _, scheme_host, port = args.connect_address.split(':')
    _, _, host = scheme_host.split('/')
    s.connect((host, int(port)))
    local_address = s.getsockname()[0]
    s.close()

sock.connect(args.connect_address)

sock.send(local_address)
response = sock.recv_string()
print response

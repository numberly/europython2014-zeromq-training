#!/usr/bin/env python
import argparse
import zmq
import socket


def get_local_ip():
    """
    Retrieve the clients local ip address and return it as a string

    :returns IpAddress as String
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect((args.connect_address, 0))
    ip = s.getsockname()[0]
    s.close()
    return ip


context = zmq.Context()

mysocket = context.socket(zmq.DEALER)

parser = argparse.ArgumentParser()
parser.add_argument('-c', '--connect-address', default='tcp://127.0.0.1:5555')
parser.add_argument('-l', '--local-address', default=None)

args = parser.parse_args()

mysocket.connect(args.connect_address)
if args.local_address is None:
  ip = get_local_ip()
else:
  ip = args.local_address
mysocket.send(ip + ":5555")
print(mysocket.recv())

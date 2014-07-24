#!/usr/bin/env python
import argparse
import zmq


def get_local_ip():
    """
    Retrieve the clients local ip address and return it as a string

    :returns IpAddress as String
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect((parser.broker_address, 0))
    ip = s.getsockname()[0]
    s.close()
    return ip


context = zmq.Context()

socket = context.socket(zmq.DEALER)

parser = argparse.ArgumentParser()
parser.add_argument('-c', '--connect-address', default='tcp://127.0.0.1:5555')

args = parser.parse_args()

socket.connect(args.connect_address)
for i in range(10):
    socket.send(str(i))
    print socket.recv()

#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import argparse
import zmq
import socket

context = zmq.Context()

sock = context.socket(zmq.DEALER)

parser = argparse.ArgumentParser()
parser.add_argument('-l', '--local-address')
parser.add_argument('-c', '--connect-address', default='tcp://127.0.0.1:5555')
parser.add_argument('city')

args = parser.parse_args()

local_address = args.local_address

if not local_address:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    _, scheme_host, port = args.connect_address.split(':')
    _, _, host = scheme_host.split('/')
    s.connect((host, int(port)))
    local_address = '{}:{}'.format(s.getsockname()[0], port)
    s.close()

sock.connect(args.connect_address)

sock.send('LIST')
response = sock.recv_string()
peers = response.split()

city = args.city

print 'Searching for {} on {} peers..'.format(city, len(peers))
print peers

for peer in peers:
    print 'Trying', peer
    peer_socket = context.socket(zmq.DEALER)
    peer_socket.connect('tcp://{}'.format(peer))
    peer_socket.send(city)
    result = peer_socket.recv_string()
    if result == 'CORRECT':
        print 'Found', city
    elif result == 'INCORRECT':
        print 'Incorrect guess'
    else:
        print 'invalid response:', result

